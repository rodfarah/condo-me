#!/bin/bash

echo "🔄 Configuring environment for project setup..."

# Adjusting permissions for PostgreSQL folder
if [ ! -d "./data/postgres/data" ]; then
  echo "📁 PostgreSQL data directory not found. Creating..."
  mkdir -p ./data/postgres/data
fi

echo "🔧 Setting correct permissions for PostgreSQL data directory..."
sudo chown -R 1000:1000 ./data/postgres/data
sudo chmod -R 775 ./data/postgres/data

# Run containers with docker-compose
echo "🚀 Running Dockerfile..."
docker compose --progress=plain build

echo "🚀 Running containers..."
docker compose up
