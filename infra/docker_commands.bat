@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Function to print success or error messages
:print_status
if "%~1"=="0" (
    echo [SUCCESS] %~2
) else (
    echo [ERROR] %~3
    exit /b !ERRORLEVEL!
)
goto :eof

REM Start Docker Compose
docker-compose up --build -d --remove-orphans
call :print_status %ERRORLEVEL% "Docker Compose started successfully." "Failed to start Docker Compose."

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
call :print_status %ERRORLEVEL% "Database migrated successfully." "Failed to migrate the database."

REM Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
call :print_status %ERRORLEVEL% "Static files collected successfully." "Failed to collect static files."

REM Set superuser password
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') | docker-compose exec -T backend python manage.py shell
call :print_status %ERRORLEVEL% "Superuser created successfully." "Failed to create superuser."

REM Load materials
docker-compose exec backend python manage.py load_materials
call :print_status %ERRORLEVEL% "Materials loaded successfully." "Failed to load materials."

ENDLOCAL
exit /b
