from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. PERFIS E CONTROLE DE ACESSO 
# ==========================================
class Docente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_docente')
    matricula = models.CharField(max_length=20, unique=True)
    area = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Prof. {self.usuario.first_name} ({self.matricula})"

class Coordenador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_coordenador')
    setor_coordenacao = models.CharField(max_length=100)

    def __str__(self):
        return f"Coord. {self.usuario.first_name} - {self.setor_coordenacao}"


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
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Médio'),
        ('D', 'Difícil'),
    ]

    enunciado = models.TextField(help_text="Aceita formatação básica e markdown")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='questoes')
    tags = models.ManyToManyField(Tag, blank=True)
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES, default='M')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Controle de status (Soft Delete)
    ativo = models.BooleanField(default=True)

    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.categoria.nome}] Questão {self.id} - {self.enunciado[:30]}..."


# ==========================================
# 4. DEPENDENTES DA QUESTÃO
# ==========================================
class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.TextField()
    is_correta = models.BooleanField(default=False)
    
    # Campo para o Moodle XML
    feedback = models.TextField(blank=True, null=True, help_text="Exibido quando o aluno seleciona esta opção")

    def __str__(self):
        return f"{'[X]' if self.is_correta else '[ ]'} {self.texto[:40]}"

class Midia(models.Model):
    questao = models.ForeignKey(Questao, related_name='midias', on_delete=models.CASCADE)
    # Requer instalação da biblioteca Pillow (pip  install Pillow)
    arquivo = models.ImageField(upload_to='questoes_imagens/') 
    legenda = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"Mídia da Questão {self.questao.id}"


# ==========================================
# 5. TABELA ASSOCIATIVA (LOGS)
# ==========================================
class HistoricoUso(models.Model):
    ACOES_CHOICES = [
        ('CRIACAO', 'Criação'),
        ('EDICAO', 'Edição'),
        ('EXPORTACAO', 'Exportação'),
        ('VISUALIZACAO', 'Visualização'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_acoes')
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name='historico_uso')
    data_acao = models.DateTimeField(auto_now_add=True)
    tipo_acao = models.CharField(max_length=20, choices=ACOES_CHOICES)
    
    # Caso a ação seja "EXPORTACAO", preenchemos se foi PDF, CSV ou XML
    formato_exportacao = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_acao} - Q{self.questao.id}"