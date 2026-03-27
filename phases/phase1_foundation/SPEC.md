# Phase 1: Фундамент — БД, Модели, Docker

## Цель
Создать рабочее dev-окружение: PostgreSQL + TimescaleDB + pgvector + Redis в Docker Compose, SQLAlchemy-модели всех таблиц, Alembic-миграции, базовый FastAPI skeleton.

## Дата начала: TBD
## Дата завершения: TBD
## Статус: ОЖИДАЕТ УТВЕРЖДЕНИЯ

---

## Deliverables (что должно быть на выходе)

### 1. Docker Compose
- `docker-compose.yml` с сервисами: postgres (TimescaleDB + pgvector), redis, api (FastAPI)
- `.env.example` с переменными окружения
- Один `docker compose up` поднимает всё

### 2. SQLAlchemy Models
- `users` + `user_profiles`
- `biomarkers` (TimescaleDB hypertable)
- `digital_twin`
- `agents` + `agent_sessions` + `agent_decisions`
- `protocols` + `daily_contracts`
- `user_files`
- `supplement_inventory`
- `knowledge_chunks` (pgvector)

### 3. Alembic Migrations
- Инициализация Alembic
- Первая миграция: создание всех таблиц
- TimescaleDB hypertable для biomarkers
- pgvector extension + index для knowledge_chunks

### 4. FastAPI Skeleton
- `main.py` с health check endpoint
- Подключение к БД через async SQLAlchemy
- Структура проекта (роутеры, зависимости, конфиг)
- Pydantic-схемы для всех моделей

### 5. Конфигурация
- `pyproject.toml` или `requirements.txt`
- `.env.example`
- `README.md` с инструкцией запуска

---

## Критерии приёмки (Definition of Done)

1. `docker compose up -d` запускается без ошибок
2. PostgreSQL доступен, TimescaleDB extension активен
3. pgvector extension активен
4. Redis доступен
5. Alembic миграции проходят: `alembic upgrade head`
6. FastAPI запускается: `GET /health` возвращает `{"status": "ok"}`
7. Все 8 таблиц существуют в БД
8. biomarkers — hypertable (TimescaleDB)
9. knowledge_chunks имеет vector index

---

## Test Functions

```python
# tests/test_phase1.py

import pytest
import asyncio
from sqlalchemy import text
from httpx import AsyncClient

# ── T1: Docker services are up ──
def test_postgres_connection(db_session):
    """PostgreSQL доступен и отвечает"""
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

def test_timescaledb_extension(db_session):
    """TimescaleDB extension установлен"""
    result = db_session.execute(
        text("SELECT extname FROM pg_extension WHERE extname = 'timescaledb'")
    )
    assert result.scalar() == "timescaledb"

def test_pgvector_extension(db_session):
    """pgvector extension установлен"""
    result = db_session.execute(
        text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
    )
    assert result.scalar() == "vector"

def test_redis_connection(redis_client):
    """Redis доступен"""
    redis_client.set("test_key", "ok")
    assert redis_client.get("test_key") == "ok"

# ── T2: All tables exist ──
EXPECTED_TABLES = [
    "users", "user_profiles", "biomarkers", "digital_twin",
    "agents", "agent_sessions", "agent_decisions",
    "protocols", "daily_contracts", "user_files",
    "supplement_inventory", "knowledge_chunks"
]

def test_all_tables_exist(db_session):
    """Все 12 таблиц созданы"""
    result = db_session.execute(text(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    ))
    tables = {row[0] for row in result}
    for table in EXPECTED_TABLES:
        assert table in tables, f"Table {table} not found"

# ── T3: TimescaleDB hypertable ──
def test_biomarkers_is_hypertable(db_session):
    """biomarkers — TimescaleDB hypertable"""
    result = db_session.execute(text(
        "SELECT hypertable_name FROM timescaledb_information.hypertables "
        "WHERE hypertable_name = 'biomarkers'"
    ))
    assert result.scalar() == "biomarkers"

# ── T4: Vector index exists ──
def test_knowledge_vector_index(db_session):
    """knowledge_chunks имеет vector index"""
    result = db_session.execute(text(
        "SELECT indexname FROM pg_indexes "
        "WHERE tablename = 'knowledge_chunks' AND indexdef LIKE '%vector%'"
    ))
    assert result.scalar() is not None

# ── T5: FastAPI health ──
@pytest.mark.asyncio
async def test_health_endpoint(test_client: AsyncClient):
    """GET /health возвращает 200"""
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# ── T6: CRUD операции ──
@pytest.mark.asyncio
async def test_create_user(db_session):
    """Можно создать пользователя"""
    from app.db.models import User
    user = User(email="test@example.com", name="Test User",
                date_of_birth="1990-01-01", sex="male")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None

@pytest.mark.asyncio
async def test_insert_biomarker(db_session):
    """Можно вставить биомаркер в hypertable"""
    result = db_session.execute(text("""
        INSERT INTO biomarkers (time, user_id, source, category, marker_name, value, unit)
        VALUES (NOW(), :user_id, 'blood_test', 'lipids', 'ApoB', 1.12, 'g/L')
        RETURNING marker_name
    """), {"user_id": "..."})
    assert result.scalar() == "ApoB"

@pytest.mark.asyncio
async def test_insert_knowledge_with_vector(db_session):
    """Можно вставить запись с embedding в knowledge_chunks"""
    import numpy as np
    embedding = np.random.rand(1536).tolist()
    result = db_session.execute(text("""
        INSERT INTO knowledge_chunks (source, content, category, embedding)
        VALUES ('pubmed', 'Test content', 'cardiology', :emb)
        RETURNING id
    """), {"emb": str(embedding)})
    assert result.scalar() is not None

# ── T7: Alembic consistency ──
def test_alembic_heads(alembic_runner):
    """Только одна head-ревизия (нет конфликтов миграций)"""
    heads = alembic_runner.heads()
    assert len(heads) == 1
```

---

## Evaluation Functions

```python
# tests/eval_phase1.py

"""
Evaluation — оценка качества Phase 1.
Запускается после прохождения всех test functions.
Выдаёт score 0-100 и детальный отчёт.
"""

def evaluate_phase1() -> dict:
    checks = []

    # E1: Структура проекта (15 баллов)
    required_files = [
        "docker-compose.yml", ".env.example", "requirements.txt",
        "src/api/main.py", "src/db/models/__init__.py",
        "alembic.ini", "alembic/versions/"
    ]
    existing = sum(1 for f in required_files if os.path.exists(f))
    score_structure = int((existing / len(required_files)) * 15)
    checks.append({"name": "Project structure", "score": score_structure, "max": 15})

    # E2: Все модели определены (20 баллов)
    from app.db import models
    required_models = [
        "User", "UserProfile", "Biomarker", "DigitalTwin",
        "Agent", "AgentSession", "AgentDecision",
        "Protocol", "DailyContract", "UserFile",
        "SupplementInventory", "KnowledgeChunk"
    ]
    found_models = [m for m in required_models if hasattr(models, m)]
    score_models = int((len(found_models) / len(required_models)) * 20)
    checks.append({"name": "SQLAlchemy models", "score": score_models, "max": 20})

    # E3: Pydantic schemas (15 баллов)
    from app.api import schemas
    required_schemas = [
        "UserCreate", "UserResponse", "BiomarkerCreate",
        "DigitalTwinResponse", "ProtocolResponse", "ContractResponse"
    ]
    found_schemas = [s for s in required_schemas if hasattr(schemas, s)]
    score_schemas = int((len(found_schemas) / len(required_schemas)) * 15)
    checks.append({"name": "Pydantic schemas", "score": score_schemas, "max": 15})

    # E4: Docker Compose quality (15 баллов)
    import yaml
    with open("docker-compose.yml") as f:
        dc = yaml.safe_load(f)
    services = dc.get("services", {})
    has_postgres = "postgres" in services or "db" in services
    has_redis = "redis" in services
    has_api = "api" in services
    has_volumes = any("volumes" in s for s in services.values())
    has_healthcheck = any("healthcheck" in s for s in services.values())
    dc_score = sum([has_postgres, has_redis, has_api, has_volumes, has_healthcheck])
    score_docker = int((dc_score / 5) * 15)
    checks.append({"name": "Docker Compose quality", "score": score_docker, "max": 15})

    # E5: Миграции (15 баллов)
    migration_files = glob.glob("alembic/versions/*.py")
    has_migrations = len(migration_files) > 0
    # Check migration creates hypertable
    has_hypertable = any("create_hypertable" in open(f).read() for f in migration_files)
    has_pgvector = any("vector" in open(f).read() for f in migration_files)
    score_migrations = sum([has_migrations, has_hypertable, has_pgvector]) * 5
    checks.append({"name": "Alembic migrations", "score": score_migrations, "max": 15})

    # E6: Relationships & constraints (10 баллов)
    # Check foreign keys, indexes, constraints
    score_relations = check_foreign_keys_and_indexes()  # helper
    checks.append({"name": "DB relationships", "score": score_relations, "max": 10})

    # E7: Code quality (10 баллов)
    # Type hints, docstrings, no hardcoded values
    score_quality = check_code_quality()  # helper
    checks.append({"name": "Code quality", "score": score_quality, "max": 10})

    total = sum(c["score"] for c in checks)
    return {
        "phase": "Phase 1: Foundation",
        "total_score": total,
        "max_score": 100,
        "grade": "PASS" if total >= 75 else "NEEDS WORK",
        "checks": checks
    }
```

---

## Зависимости от других фаз
- Phase 1 не зависит ни от чего (первая фаза)
- Phase 2, 3, 4 зависят от Phase 1

## Риски
- TimescaleDB Docker image может не включать pgvector → нужен кастомный Dockerfile
- Async SQLAlchemy + TimescaleDB — проверить совместимость
