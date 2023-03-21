"""
開発環境用の設定
django起動時のデフォルト設定
"""

from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 画像などのアップロードファイルを保存するパス(デバッグ用)
MEDIA_ROOT = BASE_DIR / 'media'

# Google認証の接続情報
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '150637606230-obhuv1372472qk1qjrgs2uvk4lkohk5g.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
