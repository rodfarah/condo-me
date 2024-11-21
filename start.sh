#!/bin/bash

echo "🔄 Configuring environment for project setup..."

# Ajustar permissões para a pasta PostgreSQL
if [ -d "./data/postgres/data" ]; then
  echo "🔧 Setting correct permissions for PostgreSQL data directory..."
  sudo chown -R 1000:1000 ./data/postgres/data
  sudo chmod -R 775 ./data/postgres/data
else
  echo "📁 PostgreSQL data directory not found. Creating..."
  mkdir -p ./data/postgres/data
  sudo chown -R 1000:1000 ./data/postgres/data
  sudo chmod -R 775 ./data/postgres/data
fi

# Subir os containers com Docker Compose
echo "🚀 Running Dockerfile..."
docker compose --progress=plain build

echo "🚀 Running containers..."
docker compose up
