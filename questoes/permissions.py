from rest_framework import permissions

class IsCoordenador(permissions.BasePermission):
    """
    Permite acesso APENAS aos Coordenadores ou ao Superuser (Admin).
    """
    def has_permission(self, request, view):
        # Proteção básica: Tem que estar logado
        if not request.user or not request.user.is_authenticated:
            return False
            
        # O Superuser (criado no terminal) sempre passa
        if request.user.is_superuser:
            return True
            
        # Verifica se o usuário tem a caixinha 'is_coordenador' marcada no perfil
        return hasattr(request.user, 'perfil') and request.user.perfil.is_coordenador

class IsCoordenadorOrReadOnly(permissions.BasePermission):
    """
    Qualquer professor logado pode ler (GET), mas apenas Coordenadores podem criar/editar/apagar (POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Se for só leitura (GET), libera geral para quem tá logado
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Se for escrita/deleção, aplica a mesma regra do Coordenador
        if request.user.is_superuser:
            return True
            
        return hasattr(request.user, 'perfil') and request.user.perfil.is_coordenador