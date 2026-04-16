import json
from google import genai
from google.genai import types
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Max, F
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Tag, Questao, Alternativa, HistoricoUso
from .serializers import CategoriaSerializer, TagSerializer, QuestaoSerializer, AlternativaSerializer, RegistroUsuarioSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCoordenadorOrReadOnly, IsCoordenador

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    permission_classes = [IsCoordenadorOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [IsAuthenticated]

class QuestaoViewSet(viewsets.ModelViewSet):
    serializer_class = QuestaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'autor', 'tags', 'tipo_questao']
    search_fields = ['enunciado']
    
    def get_queryset(self):
        """
        Mágica do Frescor: Anota a data do último log de exportação da questão.
        Ordena para que as nulas (nunca usadas) fiquem no topo (nulls_first=True),
        e as usadas recentemente fiquem no fim da lista.
        """
        return Questao.objects.annotate(
            ultima_exportacao=Max('historico_uso__data_acao')
        ).order_by(F('ultima_exportacao').asc(nulls_first=True), '-criada_em')

    def perform_create(self, serializer):
        usuario = self.request.user if self.request.user.is_authenticated else None
        serializer.save(autor=usuario)

    # Rota para o Front-End avisar que exportou a questão: POST /api/questoes/{id}/registrar_uso/
    @action(detail=True, methods=['post'])
    def registrar_uso(self, request, pk=None):
        questao = self.get_object()
        formato = request.data.get('formato_exportacao', 'JSON')
        
        HistoricoUso.objects.create(
            usuario=request.user,
            questao=questao,
            formato_exportacao=formato
        )
        return Response({'status': 'Exportação registrada. A questão agora tem menos prioridade.'}, status=status.HTTP_201_CREATED)

class AlternativaViewSet(viewsets.ModelViewSet):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer
    permission_classes = [IsAuthenticated]

class GerenciamentoUsuariosViewSet(viewsets.ModelViewSet):
    """
    Rota de administração de professores (Apenas Coordenadores)
    """
    queryset = User.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [IsCoordenador]

class GerarQuestaoIAView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        tema = request.data.get('tema', '')
        dificuldade = request.data.get('dificuldade', 'M')
        contexto = request.data.get('contexto', 'Geral')
        
        if not tema:
            return Response({"erro": "O campo 'tema' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        mapa_dificuldade = {'F': 'Fácil', 'M': 'Média', 'D': 'Difícil'}
        dificuldade_texto = mapa_dificuldade.get(dificuldade, 'Média')

        # O Cérebro da Operação: O Prompt
        system_prompt = f"""
        Você é um professor universitário especialista na criação de banco de questões.
        Crie EXATAMENTE 10 questões inéditas com os seguintes parâmetros:
        - Tema: {tema}
        - Nível de Dificuldade: {dificuldade_texto}
        - Foco/Contexto: {contexto}
        
        Você deve gerar uma mistura equilibrada de 3 tipos de questões. 
        Use EXATAMENTE estas strings no campo 'tipo_questao':
        
        1. "MULTIPLA_ESCOLHA": Deve ter EXATAMENTE 5 alternativas (apenas 1 correta).
        2. "VERDADEIRO_FALSO": Deve ter EXATAMENTE 2 alternativas (uma verdadeira, uma falsa, apenas 1 correta).
        3. "ABERTA": Questão dissertativa. NÃO inclua o campo 'alternativas' neste tipo.
        
        Regra para Alternativas (Tipos 1 e 2): Forneça um 'feedback' educativo justificando por que a alternativa está certa ou errada.
        
        Use EXATAMENTE este esquema JSON para a resposta final:
        {{
            "questoes": [
                {{
                    "enunciado": "Texto da questão de múltipla escolha...",
                    "tipo_questao": "MULTIPLA_ESCOLHA",
                    "alternativas": [
                        {{"texto": "Alternativa 1...", "is_correta": false, "feedback": "..."}},
                        {{"texto": "Alternativa Correta...", "is_correta": true, "feedback": "..."}}
                        // (Lembre-se: exatas 5 alternativas aqui)
                    ]
                }},
                {{
                    "enunciado": "Texto da questão verdadeira ou falsa...",
                    "tipo_questao": "VERDADEIRO_FALSO",
                    "alternativas": [
                        {{"texto": "Verdadeiro", "is_correta": true, "feedback": "..."}},
                        {{"texto": "Falso", "is_correta": false, "feedback": "..."}}
                    ]
                }},
                {{
                    "enunciado": "Texto da questão aberta dissertativa...",
                    "tipo_questao": "ABERTA"
                }}
            ]
        }}
        """

        try:
            # NOVA SINTAXE DO GEMINI (SDK Atualizado)
            # ⚠️ Lembrete: Coloque sua chave aqui para testar localmente
            client = genai.Client(api_key="COLE_SUA_CHAVE_AQUI_TEMPORARIAMENTE") 
            
            # response_mime_type garante que a IA devolva um JSON puro
            resposta = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=system_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            
            # Converte a resposta de texto (JSON puro) para um dicionário Python
            dados_ia = json.loads(resposta.text)
            
            return Response(dados_ia, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({"erro": "A IA gerou um formato inválido. Tente novamente."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"erro": f"Erro na API do Gemini: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)