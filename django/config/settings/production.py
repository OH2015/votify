from .base import *

DEBUG = False
ALLOWED_HOSTS = ['votify.jp','localhost']

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'postgres',
         'USER': 'postgres',
         'PASSWORD': 'postgres',
         'HOST': 'db',
         'PORT': 5432,
    }
}

# 画像などのアップロードファイルを保存するパス(デバッグ用)
MEDIA_ROOT = BASE_DIR / 'media'