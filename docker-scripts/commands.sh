#!/bin/sh

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

# Create temporary directory for static files
log "Creating temporary directory for static files..."
mkdir -p $TEMP_STATIC

# Colect static files
log "Running 'collectstatic' to gather static files..."
poetry run python /app/src/manage.py collectstatic --noinput -i admin --clear --settings=$DJANGO_SETTINGS_MODULE -v 2
log "✅ Static files collected successfully."

# Migrate database
log "Applying database migrations..."
poetry run python $APP_HOME/src/manage.py makemigrations --noinput
poetry run python $APP_HOME/src/manage.py migrate --noinput
log "✅ Database migrations completed."

# Copy static files from temporary folder into final destiny
log "Copying temp_static files to final directory..."
cp -r $TEMP_STATIC/* $APP_HOME/data/web/static/
log "✅ Static files copied to '$APP_HOME/data/web/static'."

# # # Remove temporary static directory
# log "Adjusting permissions and removing temporary directory..."
# chmod -R 777 $TEMP_STATIC
# rm -rf $TEMP_STATIC || echo "Failed to remove temp static directory"
# log "✅ Temporary directory removed."

# Inicia o servidor Django
log "Starting Django development server..."
exec poetry run python $APP_HOME/src/manage.py runserver 0.0.0.0:8000
