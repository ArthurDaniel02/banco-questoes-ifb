from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaViewSet, 
    TagViewSet, 
    QuestaoViewSet, 
    AlternativaViewSet,
    GerenciamentoUsuariosViewSet,
    GerarQuestaoIAView
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'tags', TagViewSet)
router.register(r'questoes', QuestaoViewSet, basename='questoes')
router.register(r'alternativas', AlternativaViewSet)
router.register(r'usuarios', GerenciamentoUsuariosViewSet, basename='usuarios')

urlpatterns = [

    path('', include(router.urls)),
    path('questoes-gerar-ia/', GerarQuestaoIAView.as_view(), name='gerar-questao-ia'),
]