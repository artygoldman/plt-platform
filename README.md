# Personal Longevity Team (PLT) Platform

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-blueviolet)](https://www.langchain.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-24+-2496ED)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Personal Longevity Team (PLT) is an AI-powered health optimization platform that orchestrates 27 specialized medical agents across 6 tiers to deliver personalized longevity protocols. The platform ingests biomarker data (blood tests, wearables, genetic profiles) and synthesizes recommendations through a hierarchical agent network, producing actionable daily contracts with evidence-based rationale.

**North Star Metrics:**
- Biological age (DunedinPACE algorithm)
- Healthspan forecast (years of healthy life remaining)
- Longevity score (0-100, composite metric)
- Daily contract adherence rate

## Quick Start

### Prerequisites
- Docker 24+ and Docker Compose
- Python 3.12+ (for local development)
- Anthropic API key ([get here](https://console.anthropic.com/))
- Oura API credentials (optional, for wearable sync)

### Start with Docker Compose

```bash
# Clone repository
git clone https://github.com/yourorg/plt-platform.git
cd plt-platform

# Create .env file with required variables
cp .env.example .env
# Edit .env with your API keys

# Start all services (PostgreSQL, Redis, MinIO, FastAPI, Celery)
docker compose up -d

# Wait for services to be healthy (~15s)
docker compose ps

# API is now available at http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

### Local Development Setup

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
export DATABASE_URL="postgresql+asyncpg://plt:plt_dev_2026@localhost:5432/plt_db"
export DATABASE_URL_SYNC="postgresql://plt:plt_dev_2026@localhost:5432/plt_db"
export REDIS_URL="redis://localhost:6379/0"
export ANTHROPIC_API_KEY="your-key-here"
export S3_ENDPOINT="http://localhost:9000"

# Run migrations
alembic upgrade head

# Start API server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Celery worker
celery -A src.core.celery_app worker -l info

# In another terminal, start Celery beat scheduler
celery -A src.core.celery_app beat -l info
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI 0.115 | REST API with async/await, automatic OpenAPI docs |
| **Orchestration** | LangGraph 0.2 | State-based agent graph with conditional edges, checkpointing |
| **LLM** | Anthropic Claude (Sonnet 4.6) | 27 specialized medical agents |
| **Database** | PostgreSQL 16 + TimescaleDB | Time-series biomarkers, user data, agent logs |
| **Vector Store** | pgvector | Embeddings for knowledge base semantic search |
| **Caching/PubSub** | Redis 7 | Session cache, real-time WebSocket events, Celery broker |
| **File Storage** | MinIO (S3-compatible) | PDF uploads, blood test files, health exports |
| **Background Jobs** | Celery + Beat | Async task queue, scheduled triggers (daily pipeline, Oura sync) |
| **Async Runtime** | asyncpg + uvicorn | PostgreSQL async driver, production ASGI server |
| **Authentication** | JWT + bcrypt | Bearer tokens, password hashing |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI REST API                       │
│  /api/v1/{users|data|twin|agents|contracts|protocols|...}  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              LangGraph Orchestration Engine                  │
│  ┌─Router─┬─System Biologist─┬─Medical Core─┬─Analyst       │
│  │        │ (Digital Twin)   │  (Tier 2: 8) │─Verifier      │
│  │        └─────────┬────────┤  Parallel    │  (Veto Loop)  │
│  │                  └─Lifestyle────┤        │  CMO (Approve)│
│  │                     (Tier 3: 5) └────────┴─Executors─Ops │
│  └────────────────────────────────────────────────────────┘
│
│  Checkpointing: PostgreSQL (LangGraph threads)
│  Event Streaming: Redis Pub/Sub + WebSocket
└──────────────────────┬──────────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼────┐  ┌──────────▼────┐  ┌─────────▼────┐
│PostgreSQL  │    Redis      │  │   MinIO      │
│ Biomarkers │  Session Cache│  │ PDF Files    │
│ Protocols  │  WebSocket    │  │ Exports      │
│ Contracts  │  Job Queue    │  │              │
└───────────┘  └───────────────┘  └──────────────┘

Background: Celery Workers + Beat Scheduler
├─ Daily health analysis (9 AM user timezone)
├─ Oura Ring sync (every 4 hours)
├─ Biomarker anomaly detection (continuous)
└─ Protocol archive (monthly)
```

## 6-Tier Agent Hierarchy

The platform orchestrates **27 specialized medical agents** across 6 hierarchical tiers:

### Tier 1: Strategic Foundation (4 agents)
- **System Biologist**: Builds Digital Twin (11 biological systems, anomalies, trends)
- **Analyst**: Synthesizes medical + lifestyle opinions into draft protocol
- **Verifier**: Validates protocol against knowledge base, triggers veto loop if needed
- **Chief Medical Officer (CMO)**: Final approval, escalation decisions, biological age forecast

### Tier 2: Medical Specialists (8 agents)
Analyze bloodwork, genetic data, and medical history in parallel:
- **Cardiologist**: Cardiovascular markers (lipids, blood pressure, arterial stiffness)
- **Endocrinologist**: Hormones, glucose control, thyroid function
- **Metabolologist**: Mitochondrial health, energy metabolism, obesity markers
- **Geneticist**: Genetic risk interpretation, pharmacogenomics, methylation
- **Dermatologist**: Skin aging, UV damage, collagen integrity
- **Orthopedist**: Bone density, muscle mass, joint health
- **Microbiome Specialist**: Gut microbiota, dysbiosis, microbial diversity
- **Aesthetist**: Aesthetic aging markers, anti-aging compound recommendations

### Tier 3: Lifestyle Experts (5 agents)
Integrate behavioral data and environmental factors in parallel:
- **Sleep Specialist**: Sleep architecture, circadian alignment, sleep hygiene
- **Neuropsychologist**: Cognitive function, stress markers, emotional health
- **Chronobiologist**: Time-of-day optimization, seasonal patterns, jet lag
- **Toxicologist**: Environmental toxin exposure, detox protocols
- **Nutritionist**: Macros, micronutrients, food synergies, dietary patterns

### Tier 4: Executors (2 agents)
Translate recommendations into executable, time-bound protocols:
- **Fitness Trainer**: Exercise prescription (strength, cardio, flexibility, duration)
- **Nutritionist**: Meal planning, supplement stacks, food sourcing

### Tier 5: Operations & Personalization (3 agents)
Convert protocols into daily commitments and manage lifecycle:
- **Dispatcher**: Generates daily contracts, prioritizes actions by impact
- **Inventory Manager**: Supplement ordering, stock tracking, expiry alerts
- **Concierge**: Human-in-the-loop requests, protocol adjustment logistics

### Tier 6: UX & Support (5 agents)
User-facing engagement and system maintenance:
- **UX Designer**: Dashboard insights, milestone celebrations, engagement hooks
- **QA Tester**: Decision validation, edge case discovery, regression testing
- **Developer**: System integration, API coherence, documentation generation
- **Support Agent**: FAQ, troubleshooting, user education
- **Data Analyst**: Trend reports, outcome metrics, platform improvements

## API Endpoints Summary

**42 endpoints** across 8 routers:

| Router | Count | Examples |
|--------|-------|----------|
| **Users** | 4 | POST /register, POST /login, GET /me, PUT /me |
| **Data** | 5 | POST /upload, POST /sync/oura, POST /sync/apple-health, GET /biomarkers |
| **Twin** | 5 | GET /twin, POST /rebuild, GET /systems, GET /history, GET /score |
| **Agents** | 5 | POST /run, GET /sessions, GET /sessions/{id}, GET /decisions, GET /status |
| **Contracts** | 6 | GET /today, POST /complete, POST /skip, GET /streak, GET /history, GET /stats |
| **Protocols** | 5 | GET /active, GET /, GET /history, POST /approve, GET /{id} |
| **Score** | 5 | GET /, GET /breakdown, GET /forecast, GET /trends, GET /leaderboard |
| **Inventory** | 7 | GET /, POST /, POST /consume, GET /reorder, GET /expiry, DELETE /{id}, PUT /{id} |

See [API.md](API.md) for complete endpoint documentation with request/response examples.

## Environment Variables

```bash
# Database (TimescaleDB)
DATABASE_URL=postgresql+asyncpg://plt:password@localhost:5432/plt_db
DATABASE_URL_SYNC=postgresql://plt:password@localhost:5432/plt_db

# Cache & Broker
REDIS_URL=redis://localhost:6379/0

# LLM Provider
ANTHROPIC_API_KEY=sk-ant-...

# File Storage (MinIO/S3)
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=plt-uploads

# Security
SECRET_KEY=your-secret-key-for-jwt
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Integrations (Optional)
OURA_CLIENT_ID=your-oura-client-id
OURA_CLIENT_SECRET=your-oura-secret
```

See [SETUP.md](SETUP.md) for detailed configuration instructions.

## Development Workflow

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src

# Run specific test file
pytest tests/api/test_users.py -v

# Run tests matching a pattern
pytest -k "test_register" -v

# Run with asyncio markers
pytest tests/ -v --asyncio-mode=auto
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "add_new_column"

# Apply pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history --verbose
```

### Checking Code Quality

```bash
# Format with Black
black src/

# Lint with Ruff
ruff check src/

# Type checking with mypy
mypy src/
```

## Project Structure

```
plt-platform/
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   ├── routers/             # 8 endpoint routers
│   │   ├── schemas/             # Pydantic request/response models
│   │   ├── middleware/          # Authentication, CORS
│   │   ├── deps.py              # Dependency injection (get_db, get_current_user)
│   │   └── websocket.py         # WebSocket handlers
│   ├── agents/
│   │   ├── graph.py             # LangGraph orchestration engine
│   │   ├── state.py             # PLTState TypedDict definition
│   │   ├── runner.py            # Execute compiled graph
│   │   ├── nodes/               # 9 node functions (by tier)
│   │   ├── prompts/             # System prompts for 27 agents
│   │   └── example_usage.py     # Usage example
│   ├── db/
│   │   ├── base.py              # SQLAlchemy Base, init_db
│   │   ├── models/              # 8 SQLAlchemy models
│   │   └── migrations/          # Alembic schema versions
│   └── core/
│       ├── config.py            # Settings from environment
│       ├── celery_app.py        # Celery configuration
│       └── celery_tasks.py      # Background job definitions
├── tests/                        # Pytest suite
├── docker-compose.yml           # Local dev environment
├── Dockerfile                   # API image
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── API.md                       # API documentation
├── ARCHITECTURE.md              # System design details
├── AGENTS.md                    # Agent specifications
└── SETUP.md                     # Advanced setup guide
```

## Contributing

1. **Create a feature branch**: `git checkout -b feature/your-feature`
2. **Make changes** following [PEP 8](https://pep8.org/)
3. **Write tests**: Aim for >80% coverage on new code
4. **Run quality checks**:
   ```bash
   black src/
   ruff check src/ --fix
   pytest tests/ -v --cov=src
   ```
5. **Commit** with clear message: `git commit -m "feat: add new agent"`
6. **Push** to your fork and create a Pull Request
7. **Ensure CI passes** (tests, linting, coverage)

## Troubleshooting

### Services won't start
```bash
# Check service logs
docker compose logs postgres  # Replace with service name
docker compose logs -f api    # Follow logs

# Verify PostgreSQL is healthy
psql -h localhost -U plt -d plt_db -c "SELECT 1"

# Check Redis connection
redis-cli -h localhost ping
```

### Agent pipeline hangs
- Check Celery worker logs: `docker compose logs -f celery_worker`
- Verify PostgreSQL checkpoint table: `SELECT * FROM checkpoint` in PLT database
- Increase API timeout in `docker compose up --timeout 120`

### Database connection errors
```bash
# Verify credentials in .env match docker-compose.yml
# Default credentials: plt / plt_dev_2026

# Reset database
docker compose down -v
docker compose up -d postgres
# Wait ~10s, then: alembic upgrade head
```

### Out of memory on LLM calls
- Reduce context window in agent prompts (see [AGENTS.md](AGENTS.md))
- Batch biomarker requests instead of loading all at once
- Enable streaming responses for large result sets

## Performance Considerations

- **Biomarker queries**: Use TimescaleDB `time_bucket()` for aggregation
- **Agent parallelization**: Tiers 2 & 3 run in parallel via LangGraph fan-out
- **Token optimization**: Cache system prompts, reuse embeddings
- **Database**: Enable pgvector indexing on knowledge base (HNSW algorithm)
- **Caching**: Redis stores session state, user profiles, recent twin snapshots

## License

MIT License. See [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md), [AGENTS.md](AGENTS.md), [SETUP.md](SETUP.md)
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Security**: Report security issues to security@yourorg.com
- **Status**: [Health check](http://localhost:8000/health)
