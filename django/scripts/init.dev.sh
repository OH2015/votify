#!/bin/bash

# テスト実行
python manage.py test polls --settings=config.settings.development
# マイグレーションでDBを初期化
python manage.py migrate --settings=config.settings.development
# gunicorn起動(8000番ポート待受、ソース変更時再起動)
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload --env DJANGO_SETTINGS_MODULE=config.settings.development
