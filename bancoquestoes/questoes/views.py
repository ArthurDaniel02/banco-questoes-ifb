from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Tag, Questao, Alternativa
from .serializers import CategoriaSerializer, TagSerializer, QuestaoSerializer, AlternativaSerializer
from rest_framework.permissions import IsAuthenticated


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all()
    serializer_class = QuestaoSerializer
    permission_classes = [IsAuthenticated]
    
    # Configurando os filtros (Atende aos RF35 e RF36)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'autor', 'tags', 'dificuldade']
    search_fields = ['enunciado'] # Permite buscar palavras dentro do enunciado
    
    def perform_create(self, serializer):
        # Ao criar a questão, associa o autor ao usuário que está logado (RF18)
        # Se não houver usuário logado (teste), salva como nulo temporariamente
        usuario = self.request.user if self.request.user.is_authenticated else None
        serializer.save(autor=usuario)

class AlternativaViewSet(viewsets.ModelViewSet):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer