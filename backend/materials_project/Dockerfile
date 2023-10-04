FROM python:3.7-slim

# Install PostgreSQL client and development headers
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["daphne", "-u", "/tmp/daphne.sock", "-b", "0.0.0.0", "-p", "8000", "-v", "2", "materials_project.asgi:application"]
