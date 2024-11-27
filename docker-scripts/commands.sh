#!/bin/bash

# shell will finish script execution if a command fails
set -e

# Function to show logs with a prefix
log() {
  echo "🔹 $1"
}

# Wait for Postgres initialization
log "Checking PostgreSQL availability at $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  log "Waiting for PostgreSQL to start..."
  sleep 2
done
log "✅ PostgreSQL is available at $POSTGRES_HOST:$POSTGRES_PORT"

# Activate virtual environment
export VIRTUAL_ENV="/app/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Colect static files
log "Running 'collectstatic' to gather static files..."
poetry run python /app/src/manage.py collectstatic --noinput -i admin --clear --settings=$DJANGO_SETTINGS_MODULE -v 2
log "✅ Static files collected successfully."

# Migrate database
log "Applying database migrations..."
poetry run python $APP_HOME/src/manage.py makemigrations --noinput
poetry run python $APP_HOME/src/manage.py migrate --noinput
log "✅ Database migrations completed."

# Inicia o servidor Django
log "Starting Django development server..."
exec poetry run python $APP_HOME/src/manage.py runserver 0.0.0.0:8000
