#!/bin/bash

python manage.py test --settings=config.settings.production
python manage.py migrate --settings=config.settings.production
python manage.py guest --settings=config.settings.production
gunicorn config.wsgi:application --bind 0.0.0.0:8000
