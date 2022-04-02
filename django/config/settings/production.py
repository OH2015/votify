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
