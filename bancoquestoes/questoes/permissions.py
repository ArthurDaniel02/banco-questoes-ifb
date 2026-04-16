from rest_framework import permissions

class IsCoordenador(permissions.BasePermission):
    """
    Permite acesso apenas a usuários que possuem o perfil de Coordenador.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'perfil_coordenador'))

class IsDocente(permissions.BasePermission):
    """
    Permite acesso apenas a usuários que possuem o perfil de Docente.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'perfil_docente'))

class IsCoordenadorOrReadOnly(permissions.BasePermission):
    """
    Qualquer um logado pode ler (GET), mas apenas Coordenadores podem alterar (POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'perfil_coordenador'))