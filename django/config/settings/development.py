"""
開発環境用の設定
django起動時のデフォルト設定
"""

from .base import *


DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# CORSのホワイトリスト
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
# CSRFのホワイトリスト
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 画像などのアップロードファイルを保存するパス(デバッグ用)
MEDIA_ROOT = BASE_DIR / "media"

# Google認証情報
GOOGLE_CLIENT_ID = (
    "150637606230-jtvhjc7kspor9gls59gerknguhrhlh5j.apps.googleusercontent.com"
)
SOCIAL_SECRET = "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"

# CookieのSameSite属性をNoneに設定(設定しないとCookieがブラウザで弾かれてセットされない)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"