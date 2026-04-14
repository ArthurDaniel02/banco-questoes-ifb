from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

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
    
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.categoria.nome}] Questão {self.id} - {self.enunciado[:30]}..."

class Alternativa(models.Model):
    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)
    texto = models.TextField()
    is_correta = models.BooleanField(default=False)

    def __str__(self):
        return f"{'[X]' if self.is_correta else '[ ]'} {self.texto[:40]}"