from .base import *

DEBUG = False
ALLOWED_HOSTS = ['votify.jp','localhost']

DATABASES = {
    'default': {
        #  'ENGINE': 'django.db.backends.postgresql',
        #  'NAME': 'postgres',
        #  'USER': 'postgres',
        #  'PASSWORD': 'postgres',
        #  'HOST': 'db',
        #  'PORT': 5432,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database-1',
        'USER': 'admin',
        'PASSWORD': 'Fp5LAgMBbaFH9D7',
        'HOST': 'database-1.c1ch7jqm7tvt.us-east-1.rds.amazonaws.com',
        'PORT': 3306,
    }
}

# 画像などのアップロードファイルを保存するパス(デバッグ用)
MEDIA_ROOT = BASE_DIR / 'media'