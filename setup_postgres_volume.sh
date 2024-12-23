#!/bin/sh

# 1. Create volume folder on host if it doesn't exist:
echo "Checking PostgreSQL volume directory..."
if [ ! -d "./data/postgres/data" ]; then
    echo "Creating PostgreSQL volume directory..."
    mkdir -p ./data/postgres/data
else
    echo "PostgreSQL volume directory already exists. Skipping creation..."
fi

# 2. Create 'POSTGRES_USER' on .env
if ! grep -q "^POSTGRES_USER=" .env; then
    echo "Setting POSTGRES_USER in .env..."
    echo "POSTGRES_USER=$(whoami)" >> .env
else
    echo "POSTGRES_USER already set in .env. Skipping..."
fi

# 3. Change ownership of PostgreSQL volume to local user
echo "Changing ownership of PostgreSQL volume to local user..."
sudo chown -R $(whoami):$(whoami) ./data/postgres/

# 4. Set permissions for PostgreSQL container access (container UID=999)
echo "Setting permissions for PostgreSQL container access..."
sudo chmod -R 700 ./data/postgres/
sudo chown -R 999:$(id -g) ./data/postgres/

echo "PostgreSQL volume setup completed!"
