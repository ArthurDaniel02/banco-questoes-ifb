from pathlib import Path
import inspect, os
import dj_database_url
SECRET_KEY = os.environ.get('SECRET_KEY', '142f9aca8941e0d04b4efbf754361bb6')
DEBUG = 'RENDER' not in os.environ
ALLOWED_HOSTS = ['*']

BASE_DIR = Path(__file__).resolve().parent.parent

if not DEBUG:
    ALLOWED_HOSTS = ['api-banco-questoes.onrender.com', '*'] 
    CSRF_TRUSTED_ORIGINS = ['https://api-banco-questoes.onrender.com']
else:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar', 
    'questoes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bancoquestoes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bancoquestoes.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

REST_FRAMEWORK = {
 'DEFAULT_AUTHENTICATION_CLASSES': [
 'rest_framework.authentication.TokenAuthentication',
 'rest_framework.authentication.SessionAuthentication',
 'rest_framework_simplejwt.authentication.JWTAuthentication',
 ],
 'DEFAULT_PERMISSION_CLASSES': [
 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
 ],
 'DEFAULT_FILTER_BACKENDS': [
 'django_filters.rest_framework.DjangoFilterBackend',

 ],
 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
 
}



SPECTACULAR_SETTINGS = {
    'TITLE': 'API - Banco de Questões IFB ',
    'DESCRIPTION': inspect.cleandoc("""
    Bem-vindo(a) à documentação interativa da API do **Sistema de Banco de Questões**.
    Desenvolvido como parte do projeto de Residência Tecnológica do IFB - Campus São Sebastião.

    ---

    ###  Como Autenticar (Login)
    Esta API utiliza segurança baseada em **JWT (JSON Web Tokens)**. Para testar os endpoints trancados, siga estes passos:
    
    1. Vá até a rota **`POST /api/login/`** e insira seu usuário e senha.
    2. Copie o texto gigante que vai retornar no campo `access`.
    3. Clique no botão verde **Authorize**  no topo desta página.
    4. Cole o token copiado e clique em Authorize em jwtAuth. O Swagger cuidará do resto! 

    ###  Níveis de Acesso (RBAC)
    O sistema identifica automaticamente o seu perfil:
    * **Docentes:** Podem criar questões, gerenciar suas alternativas e visualizar o banco.
    * **Coordenadores:** Possuem privilégios administrativos para gerenciar os docentes e são permitidos a fazer todo o resto.

    """),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SECURITY': [{'jwtAuth': []}],
    'COMPONENTS': {
        'securitySchemes': {
            'jwtAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'O Swagger adicionará automaticamente o prefixo "Bearer " para você. Apenas cole o token gerado no login.',
            },
        },
    },

    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
