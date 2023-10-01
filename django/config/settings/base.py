import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-skhk7tx@d%r3%$%l_hn*po2xa+g1lr8j-%o5$pm)c_q1mt@=d1'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework', # REST Framework
    'rest_framework.authtoken', # OAuth認証
    'bootstrap4', 
    'environ',
    'storages',
    'polls.apps.PollsConfig',
    'social_django', # OAuth認証
    'corsheaders', # CORS設定
    'drf_social_oauth2', # OAuth認証
    'oauth2_provider', # OAuth認証
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',  # OAuth認証
    'corsheaders.middleware.CorsMiddleware', # CORS設定
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',       # OAuth
                'social_django.context_processors.login_redirect', # OAuth
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


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

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# staticフォルダにアクセスするURL
STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# アップロードファイルアクセスURL
MEDIA_URL = '/media/'

# 認証機能で使用するモデル
AUTH_USER_MODEL = 'polls.User'

# メール送信設定
# 本番用
EMAIL_HOST = 'mail86.onamae.ne.jp'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'admin@votify.jp'
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.get_value('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
SERVER_EMAIL = 'admin@votify.jp'

# テスト用(メールサーバ代がかかるため)
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'fibo2955@gmail.com'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER # send_mailのfromがNoneの場合自動で入る。
# EMAIL_HOST_PASSWORD = env.get_value('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True

LOGIN_URL = 'login'
LOGOUT_URL = '/'

# CORS
CORS_ALLOW_CREDENTIALS = True

# 日付型のフォーマット
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y/%m/%d %H:%M',
    'DEFAULT_AUTHENTICATION_CLASSES': (
      'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
      'drf_social_oauth2.authentication.SocialAuthentication',
   ),
}
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
   'https://www.googleapis.com/auth/userinfo.email',
   'https://www.googleapis.com/auth/userinfo.profile',
]

# CookieのSameSite属性をNoneに設定
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'