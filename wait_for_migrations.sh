#!/bin/bash

# Function to check if Django migrations are applied
check_migrations() {
    sleep 5
    python3 manage.py migrate --plan > /dev/null 2>&1
    return $?
}

# Check if migrations are applied, retrying every few seconds
echo "Waiting for migrations to be applied..."
while ! check_migrations; do
    sleep 5
    echo "Trying again!"
done

echo "Migrations applied. Starting Celery..."
# Start Celery here...
