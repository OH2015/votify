"""
本番環境用の設定
django起動時に--settings=config.settings.productionと記載することで適用
"""

from .base import *
import environ

env = environ.Env()
env.read_env(BASE_DIR / ".env")

DEBUG = False
ALLOWED_HOSTS = ["votify.jp"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

# 画像などのアップロードファイルを保存するパス
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

# CSRF検証用
CSRF_TRUSTED_ORIGINS = [
    "https://votify.jp",
    "http://52.199.222.201",
]
CORS_ALLOWED_ORIGINS = [
    "https://votify.jp",
    "http://52.199.222.201",
]

# CookieのSameSite属性をNoneに設定(設定しないとCookieがブラウザで弾かれてセットされない)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"
