#!/bin/sh

export DJANGO_SETTINGS_MODULE=core.settings

python manage.py collectstatic --noinput

echo 'Applying migrations...'
python manage.py migrate

gunicorn core.wsgi:application --bind 0.0.0.0:$PORT