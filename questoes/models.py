from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. PERFIL E CONTROLE DE ACESSO
# ==========================================
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    is_coordenador = models.BooleanField(
        default=False, 
        help_text="Marque para dar poderes de Coordenador. Desmarque para perfil Professor."
    )

    def __str__(self):
        tipo = "Coordenador" if self.is_coordenador else "Professor"
        return f"[{tipo}] {self.usuario.get_full_name() or self.usuario.username}"

# ==========================================
# 2. TABELAS INDEPENDENTES
# ==========================================
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

# ==========================================
# 3. TABELA CENTRAL (QUESTÃO)
# ==========================================
class Questao(models.Model):
    TIPO_CHOICES = [
        ('MULTIPLA_ESCOLHA', 'Múltipla Escolha'),
        ('VERDADEIRO_FALSO', 'Verdadeiro ou Falso'),
        ('ABERTA', 'Aberta (Dissertação)'),
    ]

    tipo_questao = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES, 
        default='MULTIPLA_ESCOLHA'
    )
    enunciado = models.TextField(help_text="Aceita formatação básica e markdown")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='questoes')
    tags = models.ManyToManyField(Tag, blank=True)
    
    # O User do Django já tem email e nome, acessamos via autor.get_full_name() ou autor.email
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    ativo = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_tipo_questao_display()}] {self.enunciado[:30]}..."

# ==========================================
# 4. DEPENDENTES DA QUESTÃO
# ==========================================
class Alternativa(models.Model):
    # Nota: No Serializer, garantiremos que questões 'ABERTA' não tenham alternativas
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.TextField()
    is_correta = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{'[X]' if self.is_correta else '[ ]'} {self.texto[:40]}"

# ==========================================
# 5. HISTÓRICO DE EXPORTAÇÃO (LOGS)
# ==========================================
class HistoricoUso(models.Model):
    # Foco exclusivo em exportação para controle de frescor da questão
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_acoes')
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='historico_uso')
    data_acao = models.DateTimeField(auto_now_add=True)
    formato_exportacao = models.CharField(max_length=10, help_text="Ex: JSON, PDF, XML")

    def __str__(self):
        return f"Q{self.questao.id} usada por {self.usuario.username} em {self.data_acao}"