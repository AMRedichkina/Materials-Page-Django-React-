#!/bin/bash

# Function to print success or error messages
print_status() {
    if [ $? -eq 0 ]; then
        echo -e "\033[1;32m[SUCCESS]\033[0m $1"
    else
        echo -e "\033[1;31m[ERROR]\033[0m $2"
        exit 1
    fi
}

# Start Docker Compose
docker-compose up --build -d --remove-orphans
print_status "Docker Compose started successfully." "Failed to start Docker Compose."

# Wait for backend container to be ready
until sudo docker-compose exec -T backend python manage.py check; do
    echo "Waiting for backend container to be ready..."
    sleep 5
done

# Migrate the database
sudo docker-compose exec backend python manage.py migrate --noinput
print_status "Database migrated successfully." "Failed to migrate the database."

# Collect static files
sudo docker-compose exec backend python manage.py collectstatic --noinput
print_status "Static files collected successfully." "Failed to collect static files."

# Set superuser password
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | sudo docker-compose exec -T backend python manage.py shell
print_status "Superuser created successfully." "Failed to create superuser."

# Load materials
sudo docker-compose exec backend python manage.py load_materials
print_status "Materials loaded successfully." "Failed to load materials."
