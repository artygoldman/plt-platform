# Advanced Setup Guide

This guide covers production and advanced development setups for the Personal Longevity Team platform.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Database Setup](#database-setup)
3. [Redis Configuration](#redis-configuration)
4. [MinIO/S3 Setup](#minios3-setup)
5. [External API Integrations](#external-api-integrations)
6. [Celery Configuration](#celery-configuration)
7. [Production Deployment](#production-deployment)
8. [Monitoring & Logging](#monitoring--logging)
9. [Troubleshooting](#troubleshooting)

---

## Development Environment Setup

### Prerequisites

- **Python 3.12+**: [Download here](https://www.python.org/downloads/)
- **PostgreSQL 16**: [Installation guide](https://www.postgresql.org/download/)
- **Redis 7**: [Installation guide](https://redis.io/download)
- **Git**: For cloning the repository

### Step 1: Clone Repository

```bash
git clone https://github.com/yourorg/plt-platform.git
cd plt-platform
```

### Step 2: Create Virtual Environment

```bash
# Create venv
python3.12 -m venv venv

# Activate venv
source venv/bin/activate              # macOS/Linux
# or
.\venv\Scripts\activate               # Windows
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Optional: Install dev dependencies for testing/linting
pip install pytest pytest-asyncio black ruff mypy
```

### Step 4: Create .env File

Create `.env` in project root:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://plt:plt_dev_2026@localhost:5432/plt_db
DATABASE_URL_SYNC=postgresql://plt:plt_dev_2026@localhost:5432/plt_db

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM Provider
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx  # Get from https://console.anthropic.com/

# File Storage (MinIO/S3)
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=plt-uploads

# Security
SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Optional: Oura API
OURA_CLIENT_ID=your-oura-client-id
OURA_CLIENT_SECRET=your-oura-secret
```

### Step 5: Run Database Migrations

```bash
# Create database
createdb -U postgres plt_db

# Run migrations
alembic upgrade head
```

### Step 6: Start Services (Development Mode)

**Terminal 1: API Server**
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2: Celery Worker**
```bash
celery -A src.core.celery_app worker -l info
```

**Terminal 3: Celery Beat Scheduler**
```bash
celery -A src.core.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Access API at: `http://localhost:8000`
Swagger docs: `http://localhost:8000/docs`

---

## Database Setup

### TimescaleDB Installation

PostgreSQL with TimescaleDB extension for time-series optimization.

#### macOS (Homebrew)
```bash
brew install timescaledb

# Start PostgreSQL service
brew services start postgresql

# Connect and enable extension
psql -U postgres -d plt_db
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

#### Linux (Ubuntu)
```bash
# Add TimescaleDB PPA
sudo add-apt-repository ppa:timescale/timescaledb-ppa
sudo apt-get update
sudo apt-get install timescaledb-postgresql-16

# Enable extension
sudo -u postgres psql -d plt_db -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

#### Docker
```bash
docker run -d \
  --name plt-postgres \
  -e POSTGRES_USER=plt \
  -e POSTGRES_PASSWORD=plt_dev_2026 \
  -e POSTGRES_DB=plt_db \
  -p 5432:5432 \
  timescale/timescaledb-ha:pg16
```

### pgvector Installation (Vector Embeddings)

For knowledge base semantic search:

```bash
# macOS
brew install pgvector

# Linux (Ubuntu)
sudo apt-get install postgresql-16-pgvector

# Connect and enable
psql -U postgres -d plt_db
CREATE EXTENSION IF NOT EXISTS vector;
```

### Create Hypertables

Convert biomarker table to TimescaleDB hypertable:

```sql
-- Run in psql as postgres user
\c plt_db

-- Convert biomarkers table to hypertable
SELECT create_hypertable('biomarkers', 'time', if_not_exists => true);

-- Create index for optimal queries
CREATE INDEX idx_biomarkers_user_time_marker
  ON biomarkers (user_id, time DESC, marker_name);
```

### Backup & Restore

```bash
# Backup
pg_dump -U plt plt_db > backup.sql

# Restore
psql -U plt plt_db < backup.sql
```

---

## Redis Configuration

### Installation

#### macOS (Homebrew)
```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu)
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Docker
```bash
docker run -d \
  --name plt-redis \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:7-alpine redis-server --appendonly yes
```

### Verify Connection

```bash
redis-cli ping
# Expected output: PONG
```

### Optional: Redis Configuration File

Create `redis.conf` for production:

```conf
# Memory management
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1       # Save every 900 seconds if ≥1 key changed
appendonly yes   # AOF persistence

# Logging
loglevel warning
logfile "/var/log/redis/redis-server.log"

# Network
bind 127.0.0.1 ::1  # Change to 0.0.0.0 for Docker
protected-mode yes
port 6379
```

---

## MinIO/S3 Setup

MinIO provides S3-compatible object storage for PDF uploads and exports.

### Installation & Setup

#### Docker (Recommended)
```bash
docker run -d \
  --name plt-minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -v minio_data:/data \
  minio/minio server /data --console-address ":9001"
```

Access MinIO console at: `http://localhost:9001`
- Username: `minioadmin`
- Password: `minioadmin`

#### macOS
```bash
brew install minio/stable/minio
minio server ~/MinIO
```

### Create S3 Bucket

```bash
# Using AWS CLI with MinIO endpoint
aws --endpoint-url http://localhost:9000 \
  s3 mb s3://plt-uploads
```

Or via MinIO console: Click "Create Bucket" → name: "plt-uploads"

### Configure S3 Access Keys

**Option 1: Use Default Credentials**
```
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
```

**Option 2: Create New Access Key** (MinIO console)
1. Navigate to Access Keys
2. Click "Create New Key"
3. Copy Access Key and Secret Key to `.env`

---

## External API Integrations

### Anthropic API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Go to "API Keys"
3. Create new key
4. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```

### Oura Ring API (Optional)

Enable Oura Ring wearable data sync.

#### Step 1: Register Oura Application

1. Go to [Oura Developer Portal](https://cloud.ouraring.com/oauth/applications)
2. Click "Create Application"
3. Fill in:
   - **Name**: PLT Platform
   - **Redirect URI**: `http://localhost:8000/api/v1/auth/oura/callback`
4. Save Client ID and Secret

#### Step 2: Add to .env

```env
OURA_CLIENT_ID=your-client-id
OURA_CLIENT_SECRET=your-client-secret
OURA_REDIRECT_URI=http://localhost:8000/api/v1/auth/oura/callback
```

#### Step 3: User Oura Authorization Flow

```bash
# User visits this URL to authorize
http://localhost:8000/api/v1/auth/oura/authorize

# Redirects back with authorization code
# API exchanges code for refresh token
# Token stored in user_profile.oura_refresh_token
```

#### Step 4: Test Sync

```bash
curl -X POST http://localhost:8000/api/v1/data/sync/oura \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### Apple Health Data Export (Manual)

Users manually export Apple Health data:

1. Open Health app → Account → Export Health Data
2. Save `apple_health_export.zip`
3. Upload via `POST /api/v1/data/sync/apple-health`

---

## Celery Configuration

### Broker & Backend

Configure Redis as broker and PostgreSQL as result backend.

### settings.py (or environment-based)

```python
# In src/core/celery_app.py

from celery import Celery
from src.core.config import get_settings

settings = get_settings()

app = Celery('plt')

# Broker: Redis
app.conf.broker_url = settings.redis_url

# Backend: PostgreSQL (for persistent result storage)
app.conf.result_backend = settings.database_url_sync

# Task settings
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.result_serializer = 'json'
app.conf.timezone = 'UTC'
app.conf.enable_utc = True

# Task time limits
app.conf.task_time_limit = 30 * 60  # 30 minutes hard limit
app.conf.task_soft_time_limit = 25 * 60  # 25 minutes soft limit

# Retry policy
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_max_retries = 3
```

### Scheduled Tasks

Celery Beat schedule (runs daily health analysis, Oura sync, etc.):

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'daily-health-analysis': {
        'task': 'src.core.celery_tasks.daily_health_analysis',
        'schedule': crontab(hour=9, minute=0),  # 9 AM daily
    },
    'oura-sync': {
        'task': 'src.core.celery_tasks.sync_oura_rings',
        'schedule': crontab(minute=0, hour='*/4'),  # Every 4 hours
    },
    'detect-anomalies': {
        'task': 'src.core.celery_tasks.detect_biomarker_anomalies',
        'schedule': crontab(minute=0, hour='*/1'),  # Hourly
    },
}
```

### Start Workers

```bash
# Development worker (single process)
celery -A src.core.celery_app worker -l info

# Production worker (4 processes, pool=prefork)
celery -A src.core.celery_app worker -l info -c 4 --pool=prefork

# Beat scheduler (separate process)
celery -A src.core.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Monitor Tasks

```bash
# Flower (web-based monitoring)
pip install flower
celery -A src.core.celery_app events

# In another terminal
flower -A src.core.celery_app --port 5555

# Access at http://localhost:5555
```

---

## Production Deployment

### Docker Compose Production Setup

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  postgres:
    image: timescale/timescaledb-ha:pg16
    restart: always
    env_file: .env.prod
    environment:
      POSTGRES_USER: plt
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: plt_db
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U plt"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data_prod:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    env_file: .env.prod
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      start_period: 5s
      retries: 3
    environment:
      DATABASE_URL: postgresql+asyncpg://plt:${POSTGRES_PASSWORD}@postgres:5432/plt_db
      DATABASE_URL_SYNC: postgresql://plt:${POSTGRES_PASSWORD}@postgres:5432/plt_db
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0
      ENVIRONMENT: production

  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    env_file: .env.prod
    command: celery -A src.core.celery_app worker -l info -c 4 --pool=prefork
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql+asyncpg://plt:${POSTGRES_PASSWORD}@postgres:5432/plt_db
      DATABASE_URL_SYNC: postgresql://plt:${POSTGRES_PASSWORD}@postgres:5432/plt_db
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0

  celery_beat:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    env_file: .env.prod
    command: celery -A src.core.celery_app beat -l info
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql+asyncpg://plt:${POSTGRES_PASSWORD}@postgres:5432/plt_db
      DATABASE_URL_SYNC: postgresql://plt:${POSTGRES_PASSWORD}@postgres:5432/plt_db
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0

volumes:
  postgres_data_prod:
  redis_data_prod:
```

### Deploy with Docker Compose

```bash
# Create .env.prod with production credentials
cp .env.example .env.prod
# Edit .env.prod with real API keys, strong passwords

# Start services
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f api
```

### Kubernetes Deployment (Optional)

For large-scale deployments, use Kubernetes with Helm charts:

```bash
# Build and push Docker image to registry
docker build -t registry.example.com/plt-api:v1.0 .
docker push registry.example.com/plt-api:v1.0

# Deploy with Helm
helm install plt ./helm-chart \
  --set image.repository=registry.example.com/plt-api:v1.0 \
  --set postgresql.password=YOUR_SECURE_PASSWORD
```

### HTTPS/TLS Setup

Use Nginx as reverse proxy with Let's Encrypt SSL:

```nginx
server {
    listen 443 ssl http2;
    server_name api.longevity.health;

    ssl_certificate /etc/letsencrypt/live/api.longevity.health/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.longevity.health/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring & Logging

### Prometheus Metrics (Optional)

Add Prometheus instrumentation:

```bash
pip install prometheus-client
```

Example endpoint:

```python
from prometheus_client import Counter, Histogram
import time

agent_calls = Counter('agent_calls_total', 'Total agent API calls', ['agent_id'])
agent_latency = Histogram('agent_latency_seconds', 'Agent call latency', ['agent_id'])

@app.get("/agents/run")
async def run_agent_pipeline(...):
    agent_calls.labels(agent_id="system_biologist").inc()
    start = time.time()
    # ... execution ...
    agent_latency.labels(agent_id="system_biologist").observe(time.time() - start)
```

Expose metrics at `/metrics` for Prometheus scraping.

### Grafana Dashboard

Create Grafana dashboard:
1. Add Prometheus data source: `http://prometheus:9090`
2. Import dashboard with metrics:
   - `agent_calls_total`
   - `agent_latency_seconds`
   - `database_query_duration_seconds`
   - `api_request_duration_seconds`

### Structured Logging

All logs use JSON format for aggregation:

```python
import logging
import json

logger = logging.getLogger(__name__)

logger.info(
    "Agent execution completed",
    extra={
        "user_id": str(user_id),
        "session_id": str(session_id),
        "agent_id": "cardiologist",
        "tokens": 1240,
        "latency_ms": 4500,
    }
)
```

Forward to centralized logging (ELK stack, Datadog, etc.):
- All logs to stdout (Docker-friendly)
- Parse JSON fields for structured search

---

## Troubleshooting

### Database Connection Errors

```bash
# Check PostgreSQL is running
psql -U plt -d plt_db -c "SELECT 1;"

# Check credentials in .env match docker-compose.yml
grep POSTGRES_ .env
grep POSTGRES_ docker-compose.yml

# Verify DATABASE_URL format
# Should be: postgresql+asyncpg://user:password@host:port/database
```

### Redis Connection Errors

```bash
# Check Redis is running
redis-cli ping
# Expected: PONG

# Check Redis credentials
redis-cli -a YOUR_PASSWORD ping

# Verify REDIS_URL in .env
# Should be: redis://[:password]@host:port/database
```

### Agent Pipeline Hangs

```bash
# Check Celery worker logs
celery -A src.core.celery_app inspect active

# Check for stuck tasks
celery -A src.core.celery_app purge  # Clear queue

# Check PostgreSQL checkpoint table for stuck threads
psql -U plt -d plt_db -c "SELECT * FROM checkpoint LIMIT 10;"

# Increase timeouts if needed
TASK_TIME_LIMIT=3600  # 1 hour
TASK_SOFT_TIME_LIMIT=3300  # 55 min
```

### Out of Memory on LLM Calls

```bash
# Reduce context window in agent prompts
# src/agents/prompts/tier2_cardiologist.py:
# system_prompt should limit biomarker count

# Or paginate biomarker queries
GET /api/v1/data/biomarkers?skip=0&limit=50

# Check memory usage
docker stats plt-api
```

### Migration Issues

```bash
# Show migration history
alembic history --verbose

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Upgrade to head
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "add_new_field"
```

### Test Database Connection

```bash
python3 -c "
from src.db.base import engine, init_db
import asyncio

async def test():
    async with engine.begin() as conn:
        result = await conn.execute('SELECT 1')
        print('✓ Database connected')

asyncio.run(test())
"
```

### Clear Cache/Sessions

```bash
# Redis: Clear all keys
redis-cli FLUSHALL

# PostgreSQL: Clear checkpoint data
psql -U plt -d plt_db -c "DELETE FROM checkpoint;"

# Celery: Clear task queue
celery -A src.core.celery_app purge
```

---

## Environment Variables Reference

**Required:**
```
DATABASE_URL
DATABASE_URL_SYNC
REDIS_URL
ANTHROPIC_API_KEY
S3_ENDPOINT
S3_ACCESS_KEY
S3_SECRET_KEY
S3_BUCKET
SECRET_KEY
```

**Optional:**
```
JWT_ALGORITHM (default: HS256)
JWT_EXPIRATION_MINUTES (default: 1440)
OURA_CLIENT_ID
OURA_CLIENT_SECRET
LOG_LEVEL (default: INFO)
ENVIRONMENT (default: development)
```

---

## Next Steps

1. **Read the main README**: [README.md](README.md)
2. **Explore the architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Review API docs**: [API.md](API.md)
4. **Understand agents**: [AGENTS.md](AGENTS.md)

For production deployments, also consider:
- Setting up monitoring (Prometheus + Grafana)
- Configuring backup strategy (PostgreSQL WAL archiving)
- Implementing CDN for static assets
- Setting up rate limiting (via Nginx or API gateway)
- Configuring auto-scaling policies (if using Kubernetes)
