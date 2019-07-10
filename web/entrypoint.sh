#!/bin/sh
echo "Running Django Entrypoint commands"
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data
exec gunicorn social_team_builder.wsgi:application --bind 0.0.0.0:8081 --workers 3
