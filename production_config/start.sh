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

# Adjusting permissions for bin folder (in order to run selenium)
echo "🔧 Setting correct permissions for Chromedriver directory..."
sudo chown -R 1000:1000 ./bin/chromedriver-linux64
sudo chmod -R 775 ./bin/chromedriver-linux64

# Adjusting permissions for Coverage folder and files
if [ ! -d "./htmlcov" ]; then
 echo "📁 Coverage report directory not found. Creating..."
 mkdir -p ./htmlcov
fi
echo "🔧 Setting correct permissions for coverage files..."
sudo chown -R 1000:1000 ./htmlcov
sudo chmod -R 775 ./htmlcov

if [ ! -f "./.coverage" ]; then
 echo "📄 .coverage file not found. Initializing..."
 touch ./.coverage
 sudo chown 1000:1000 ./.coverage
 sudo chmod 664 ./.coverage
fi

if [ ! -f "./.coveragerc" ]; then
 echo "🔧 .coveragerc file not found. Creating default..."
 touch ./.coveragerc
 sudo chown 1000:1000 ./.coveragerc
 sudo chmod 664 ./.coveragerc
fi

# Run containers with docker-compose
echo "🚀 Running Dockerfile..."
docker compose build

echo "🚀 Running containers..."
docker compose up
