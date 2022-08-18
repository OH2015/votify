#!/bin/bash

# Djangoプロジェクトフォルダに移動
cd django
# テスト実行(設定は本番用を使用)
python manage.py test polls --settings=config.settings.production
# マイグレーション
python manage.py migrate --settings=config.settings.production
# ゲストユーザ作成(カスタムコマンド)
python manage.py guest --settings=config.settings.production
# gunicorn起動
gunicorn config.wsgi:application --bind 0.0.0.0:8000
