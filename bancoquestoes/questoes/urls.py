from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, TagViewSet, QuestaoViewSet, AlternativaViewSet

# O Router cria automaticamente as rotas de GET, POST, PUT, DELETE
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'tags', TagViewSet)
router.register(r'questoes', QuestaoViewSet)
router.register(r'alternativas', AlternativaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]