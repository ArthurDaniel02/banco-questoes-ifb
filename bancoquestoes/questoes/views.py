from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Tag, Questao, Alternativa
from .serializers import CategoriaSerializer, TagSerializer, QuestaoSerializer, AlternativaSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCoordenadorOrReadOnly

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    permission_classes = [IsCoordenadorOrReadOnly]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [IsAuthenticated]

class QuestaoViewSet(viewsets.ModelViewSet):
    queryset = Questao.objects.all()
    serializer_class = QuestaoSerializer
    permission_classes = [IsAuthenticated]
    
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'autor', 'tags', 'dificuldade']
    search_fields = ['enunciado']
    
    def perform_create(self, serializer):
        usuario = self.request.user if self.request.user.is_authenticated else None
        serializer.save(autor=usuario)

class AlternativaViewSet(viewsets.ModelViewSet):
    queryset = Alternativa.objects.all()
    serializer_class = AlternativaSerializer
    permission_classes = [IsAuthenticated]