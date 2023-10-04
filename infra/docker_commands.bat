@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Start Docker Compose
docker-compose up --build -d --remove-orphans

REM Wait for backend container to be ready
:wait_for_backend
docker-compose exec -T backend python manage.py check
if %ERRORLEVEL% NEQ 0 (
    echo Waiting for backend container to be ready...
    timeout /t 5
    goto wait_for_backend
)

REM Migrate the database
docker-compose exec backend python manage.py migrate --noinput

REM Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

REM Set superuser password
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') | docker-compose exec -T backend python manage.py shell

REM Load materials
docker-compose exec backend python manage.py load_materials

ENDLOCAL
exit /b
