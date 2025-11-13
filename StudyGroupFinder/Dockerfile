# Dockerfile — place at repo root
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps for psycopg2 build
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy project files
COPY . /app/

# Collect static files (STATIC_ROOT must be set)
ENV DJANGO_SETTINGS_MODULE=StudyGroupFinder.settings
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Entrypoint script to run migrations and start gunicorn
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
