#!/usr/bin/env bash
set -e

echo "Starting Personal Longevity Team API..."

# Wait for postgres to be ready
echo "Waiting for PostgreSQL..."
python -c "
import socket
import time
import os

host = os.getenv('DB_HOST', 'postgres')
port = int(os.getenv('DB_PORT', 5432))
timeout = int(os.getenv('DB_CONNECT_TIMEOUT', 30))

start = time.time()
while time.time() - start < timeout:
    try:
        socket.create_connection((host, port), timeout=5)
        print(f'PostgreSQL is ready at {host}:{port}')
        break
    except (socket.timeout, socket.error):
        elapsed = time.time() - start
        remaining = timeout - elapsed
        print(f'Waiting for PostgreSQL... ({elapsed:.0f}s elapsed, {remaining:.0f}s remaining)')
        time.sleep(2)
else:
    print(f'Timeout waiting for PostgreSQL after {timeout}s')
    exit(1)
"

# Wait for redis to be ready
echo "Waiting for Redis..."
python -c "
import redis
import time
import os

host = os.getenv('REDIS_HOST', 'redis')
port = int(os.getenv('REDIS_PORT', 6379))
timeout = int(os.getenv('REDIS_CONNECT_TIMEOUT', 30))

start = time.time()
while time.time() - start < timeout:
    try:
        r = redis.Redis(host=host, port=port, socket_connect_timeout=5)
        r.ping()
        print(f'Redis is ready at {host}:{port}')
        break
    except Exception:
        elapsed = time.time() - start
        remaining = timeout - elapsed
        print(f'Waiting for Redis... ({elapsed:.0f}s elapsed, {remaining:.0f}s remaining)')
        time.sleep(2)
else:
    print(f'Timeout waiting for Redis after {timeout}s')
    exit(1)
"

# Run migrations
echo "Running database migrations..."
alembic upgrade head

echo "Starting Uvicorn server..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000
