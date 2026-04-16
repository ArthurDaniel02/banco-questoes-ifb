from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria, Tag, Questao, Alternativa, Perfil

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = ['id', 'texto', 'is_correta', 'feedback'] 

class QuestaoSerializer(serializers.ModelSerializer):
    # required=False porque questões ABERTAS não enviarão alternativas
    alternativas = AlternativaSerializer(many=True, required=False)

    class Meta:
        model = Questao
        fields = '__all__'
        read_only_fields = ['autor', 'criada_em', 'atualizada_em']

    def validate(self, data):
        """
        Valida a quantidade de alternativas de acordo com o TIPO da questão.
        """
        # Pega o tipo da questão (se for atualização, pega do banco)
        tipo = data.get('tipo_questao', getattr(self.instance, 'tipo_questao', 'MULTIPLA_ESCOLHA'))
        alternativas = data.get('alternativas', [])

        if tipo == 'ABERTA':
            if len(alternativas) > 0:
                raise serializers.ValidationError({"alternativas": "Questões do tipo 'Aberta' não podem ter alternativas."})
        
        elif tipo == 'VERDADEIRO_FALSO':
            if len(alternativas) != 2:
                raise serializers.ValidationError({"alternativas": "Questões 'Verdadeiro ou Falso' exigem exatamente 2 alternativas."})
            if sum(1 for alt in alternativas if alt.get('is_correta', False)) != 1:
                raise serializers.ValidationError({"alternativas": "Exatamente uma alternativa deve ser a correta."})
                
        elif tipo == 'MULTIPLA_ESCOLHA':
            if len(alternativas) != 5:
                raise serializers.ValidationError({"alternativas": "Questões de 'Múltipla Escolha' exigem exatamente 5 alternativas."})
            if sum(1 for alt in alternativas if alt.get('is_correta', False)) != 1:
                raise serializers.ValidationError({"alternativas": "Exatamente uma alternativa deve ser a correta."})

        return data

    def create(self, validated_data):
        # O .pop() com [] garante que não dê erro se vier vazio (Questão Aberta)
        alternativas_data = validated_data.pop('alternativas', [])
        tags_data = validated_data.pop('tags', [])
        
        questao = Questao.objects.create(**validated_data)
        
        for tag in tags_data:
            questao.tags.add(tag)
            
        for alt_data in alternativas_data:
            Alternativa.objects.create(questao=questao, **alt_data)
            
        return questao

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    is_coordenador = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_coordenador']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}, # Obriga o Front a mandar o Email
            'first_name': {'required': True}, # Obriga o Nome
            'last_name': {'required': True}   # Obriga o Sobrenome
        }

    def create(self, validated_data):
        is_coord = validated_data.pop('is_coordenador', False)
        # O Django cria o User com a senha criptografada em segurança
        user = User.objects.create_user(**validated_data)
        # Cria a caixinha do Perfil ligada a esse usuário
        Perfil.objects.create(usuario=user, is_coordenador=is_coord)
        return user