#!/bin/bash
set -e

cd /usr/src/backend/anwesha

echo "=== Starting Django migrations ==="
python manage.py migrate --verbosity 2

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --verbosity 2

echo "=== Starting Gunicorn ==="
exec gunicorn anwesha.wsgi:application --bind 0.0.0.0:8080 --workers 4
