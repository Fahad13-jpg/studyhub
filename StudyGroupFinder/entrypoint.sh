#!/bin/sh
set -e

# Optional: wait for DB to be ready (simple loop could be added here)

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn StudyGroupFinder.wsgi:application --workers 3 --bind 0.0.0.0:8000
