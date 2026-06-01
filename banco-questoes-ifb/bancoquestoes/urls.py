from django.contrib import admin
from django.urls import path, re_path, include
from django.http import JsonResponse
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class LoginTokenObtainPairView(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {
                'detail': 'Este endpoint aceita apenas POST. Envie usuário e senha para /api/login/.'
            },
            status=405,
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', RedirectView.as_view(pattern_name='token_obtain_pair', permanent=False)),
    re_path(r'^api/login/?$', LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/', include('questoes.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]