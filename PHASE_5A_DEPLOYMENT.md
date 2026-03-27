# Phase 5A: Docker Orchestration & CI/CD Configuration

## Overview
Complete Docker orchestration, CI/CD pipeline, and environment configuration for Personal Longevity Team platform.

## Files Created/Updated

### Docker Compose Files
1. **docker-compose.yml** — Development environment
   - PostgreSQL 16 (TimescaleDB + pgvector)
   - Redis 7
   - MinIO S3-compatible storage
   - FastAPI application
   - Celery worker and beat scheduler
   - Health checks on all services
   - Shared network: plt-network
   - Volumes: postgres_data, redis_data, minio_data

2. **docker-compose.prod.yml** — Production environment
   - No port exposure except API (8000)
   - Resource limits per service
   - restart: unless-stopped policy
   - Read-only root filesystems with tmpfs
   - security_opt: no-new-privileges
   - Parameterized secrets via env vars
   - Database password, Redis password, MinIO credentials

3. **docker-compose.test.yml** — Integration test environment
   - postgres, redis, minio services
   - postgres_test_data, redis_test_data, minio_test_data volumes
   - plt-test-network isolation

### Dockerfile
**Multi-stage build** (optimized production image)
- Stage 1: builder — install dependencies
- Stage 2: runtime — minimal image with only needed files
- Python 3.12-slim base
- Non-root user (appuser:1000)
- Health check: curl to /health endpoint
- Entry command: uvicorn server on port 8000
- PYTHONUNBUFFERED and PYTHONDONTWRITEBYTECODE flags

### Environment Files
1. **.env** — Development (currently populated)
   - Database credentials, Redis URL, MinIO config
   - JWT settings, Anthropic API key
   - Oura integration placeholders

2. **.env.example** — Template with all required variables
   - Database, Redis, MinIO, JWT, Anthropic, Oura
   - Celery broker/result backend
   - CORS origins, logging, file upload limits
   - Email configuration (optional)

3. **.env.test** — Test environment
   - PostgreSQL test database (plt_test_db)
   - Test Redis and MinIO endpoints
   - Debug logging, test secret keys

### CI/CD Pipeline
**.github/workflows/ci.yml** — GitHub Actions
- **Triggers**: push to main/develop, PRs
- **Lint job**: black, isort, mypy checks
- **Test job**: pytest with postgres/redis services, coverage report
- **Build job**: Docker image build on main branch push
- Codecov integration

### Testing Configuration
1. **tests/conftest.py** — Pytest fixtures
   - async_client (httpx.AsyncClient)
   - db_session (async SQLAlchemy session)
   - auth_header (JWT token for single user)
   - auth_headers_list (5 different test users)
   - redis_client (Redis fixture with auto-cleanup)
   - cleanup_db (auto-cleanup between tests)

2. **pytest.ini** — Pytest configuration
   - asyncio_mode: auto
   - Test path discovery rules
   - Markers: @pytest.mark.asyncio, @pytest.mark.integration, @pytest.mark.slow

### Scripts
1. **scripts/entrypoint.sh** — Docker entrypoint
   - Waits for PostgreSQL ready
   - Waits for Redis ready
   - Runs Alembic migrations
   - Starts Uvicorn server

2. **scripts/wait_for_it.sh** — Service wait utility
   - TCP connection probe with timeout
   - Used in docker-compose dependencies

### Configuration Files
1. **.dockerignore** — Excludes unnecessary files from Docker build
2. **.gitignore** — Standard Python/Docker exclusions
3. **Makefile** — Development commands
   - up/down, logs, test, lint, format, migrate
   - make help for full list

## Key Features

### Networking
- Isolated bridge network (plt-network) for secure inter-service communication
- Services reach each other by container name (postgres, redis, minio)

### Health Checks
- PostgreSQL: pg_isready
- Redis: redis-cli ping
- MinIO: HTTP /minio/health/live
- API: HTTP GET /health

### Security (Production)
- Non-root user in containers
- Read-only root filesystems
- No privilege escalation (no_new_privileges)
- Resource limits (CPU, memory) per service
- Secrets parameterized via environment variables

### Database
- PostgreSQL with TimescaleDB extension (time-series)
- pgvector extension (embeddings)
- Alembic migrations
- Async support (asyncpg)

### Async/Background Jobs
- Celery worker for async task processing
- Celery beat for scheduled tasks
- Redis broker and result backend

### Storage
- MinIO (S3-compatible) on ports 9000/9001
- Console access on port 9001
- Persistent volume storage

## Usage

### Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Run tests
docker-compose exec api pytest tests/

# Format code
docker-compose exec api bash -c "black src tests && isort src tests"

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Set environment variables in .env
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

### Integration Testing
```bash
# Start test services
docker-compose -f docker-compose.test.yml up -d

# Run tests against test environment
DATABASE_URL=postgresql+asyncpg://plt:plt_test@localhost:5432/plt_test_db \
REDIS_URL=redis://localhost:6379/0 \
pytest tests/

# Stop test services
docker-compose -f docker-compose.test.yml down -v
```

## Environment Variables

### Required (Development)
- DATABASE_URL, DATABASE_URL_SYNC
- REDIS_URL
- SECRET_KEY
- JWT_ALGORITHM
- ANTHROPIC_API_KEY

### Optional
- OURA_CLIENT_ID, OURA_CLIENT_SECRET
- SMTP_* (email configuration)
- S3_* (MinIO configuration)

### Production Only
- DB_PASSWORD (parameterized)
- REDIS_PASSWORD (parameterized)
- All secrets from secure vault

## Dependencies
- Python 3.12
- PostgreSQL 16 + TimescaleDB
- Redis 7
- MinIO (latest)
- FastAPI 0.115+
- SQLAlchemy 2.0+
- Celery 5.4+
- pytest 8.3+

## Next Steps
1. Update requirements.txt with test dependencies (pytest-httpx, moto)
2. Implement /health endpoint in FastAPI app
3. Configure Alembic initial migration
4. Deploy to staging environment
5. Load test under expected production load
