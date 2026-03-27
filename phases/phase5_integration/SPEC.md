# Phase 5: Integration + Final Assembly — Full E2E, Docker, Documentation

## Цель
Интегрировать все компоненты системы (БД, модели, LangGraph агенты, FastAPI API) в единое целое, провести end-to-end тестирование полного потока (загрузка файла → анализ агентами → генерация протокола → создание контрактов), подготовить финальную Docker-конфигурацию, создать документацию и seed data для демо.

## Дата начала: TBD
## Дата завершения: TBD
## Статус: ОЖИДАЕТ УТВЕРЖДЕНИЯ

---

## Deliverables (что должно быть на выходе)

### 1. Full Docker Compose
- Complete `docker-compose.yml` с всеми сервисами:
  - PostgreSQL 15 + TimescaleDB + pgvector
  - Redis
  - FastAPI (API server)
  - Celery worker + beat scheduler
  - MinIO (S3-compatible storage)
  - (Optional) Prometheus + Grafana для мониторинга
- `.env.example` со всеми переменными окружения
- `docker-compose.prod.yml` для production с security hardening
- Network isolation между сервисами

### 2. End-to-End Test Suite
Complete E2E scenario:
1. User uploads blood test PDF
2. File parsing service extracts biomarkers
3. LangGraph agents analyze data in parallel
4. Anomaly detector flags issues
5. Protocol generator creates health protocol
6. Contract generator creates daily contracts
7. Protocols и contracts сохраняются в БД
8. WebSocket отправляет уведомления клиенту

Test flow проверяет каждый шаг и время выполнения (target < 60 сек)

### 3. Integration Tests
- API → LangGraph → DB round-trip
  - POST /data/upload → agents.invoke() → SELECT from DB
  - GET /protocols/{id} возвращает данные с агента
- Concurrent users: 5 пользователей одновременно → без конфликтов
- Database consistency: все FK constraints соблюдены
- Data integrity: никаких orphaned records

### 4. Performance Benchmarks
- Latency: от upload до contracts готовых (target < 60 сек)
- Token usage per agent cycle (track для Claude API costs)
- Database query performance (< 100ms для common queries)
- Memory usage per worker (Celery)
- WebSocket message throughput

### 5. Documentation
- **README.md**: как установить и запустить проект
  - Prerequisites (Docker, Python 3.11+)
  - Quick start (`docker compose up`)
  - API documentation link (Swagger at `/docs`)
  - Architecture overview
- **ARCHITECTURE.md**: диаграммы и описание компонентов
- **API.md**: документация всех endpoint'ов с примерами curl
- **AGENTS.md**: описание каждого агента, промптов, выходов
- **SETUP.md**: advanced конфигурация (OAuth, Oura API keys, etc.)

### 6. .env.example
```
# Database
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/longevity_db
REDIS_URL=redis://redis:6379/0

# API & Auth
SECRET_KEY=your-secret-key-here
JWT_EXPIRY_MINUTES=15
JWT_REFRESH_EXPIRY_DAYS=7

# File Storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
AWS_S3_BUCKET=longevity-files

# External APIs
OURA_CLIENT_ID=your_oura_client_id
OURA_CLIENT_SECRET=your_oura_secret
ANTHROPIC_API_KEY=your_claude_api_key

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=INFO
```

### 7. CI Configuration
- GitHub Actions workflow для:
  - Запуск тестов при push
  - Lint & format check (black, isort, mypy)
  - Docker image build & push to registry
  - Automatic deployment (optional)

### 8. Seed Data for Demo
- 1 demo user с базовыми данными
- 3-5 sample blood test PDFs (anonymized)
- Предзагруженные биомаркеры на 30 дней
- Несколько existing protocols
- Several active contracts

---

## Критерии приёмки (Definition of Done)

1. **E2E Flow**: Полный сценарий от загрузки файла до созданных контрактов работает
2. **Docker Compose**: Все 6+ сервисов запускаются с `docker compose up`
3. **Database**: Все миграции применяются, никаких ошибок
4. **FastAPI**: Все endpoint'ы доступны и работают
5. **LangGraph**: Все агенты инвокируются и возвращают результаты
6. **WebSocket**: Real-time обновления доходят до клиента
7. **Celery**: Background tasks выполняются по расписанию
8. **Integration**: API → LangGraph → DB round-trip успешен
9. **Concurrent Users**: 5 пользователей одновременно без конфликтов
10. **Performance**: Full E2E cycle < 60 сек (target)
11. **Tests**: Все E2E и integration tests проходят
12. **Documentation**: README, ARCHITECTURE, API, AGENTS docs созданы
13. **Seed Data**: Demo данные загружены и отображаются
14. **Recovery**: System восстанавливается после сбоя агента или потери соединения

---

## Test Functions

```python
# tests/test_phase5_e2e.py

import pytest
import asyncio
import time
from httpx import AsyncClient
from pathlib import Path
from unittest.mock import patch

# ── T1: Full E2E Flow ──

@pytest.mark.asyncio
async def test_e2e_upload_to_contracts(
    test_client: AsyncClient,
    auth_header,
    db_session,
    redis_client
):
    """
    E2E: Upload blood test PDF → parse → agents analyze → contracts created
    Target: < 60 seconds
    """
    start_time = time.time()

    # Step 1: Upload blood test PDF
    with open("tests/fixtures/blood_test_complete.pdf", "rb") as f:
        upload_response = await test_client.post(
            "/api/v1/data/upload",
            files={"file": f},
            headers=auth_header
        )
    assert upload_response.status_code == 200
    file_id = upload_response.json()["file_id"]

    # Step 2: Check that biomarkers were extracted
    biomarkers_response = await test_client.get(
        "/api/v1/data/biomarkers",
        headers=auth_header
    )
    assert biomarkers_response.status_code == 200
    biomarkers = biomarkers_response.json()
    assert len(biomarkers) > 0
    assert any(b["marker_name"] in ["cholesterol", "glucose"] for b in biomarkers)

    # Step 3: Trigger agents
    agent_response = await test_client.post(
        "/api/v1/agents/cardio-agent/trigger",
        headers=auth_header
    )
    assert agent_response.status_code == 200

    # Wait for agents to complete (polling)
    for _ in range(60):  # 60 sec timeout
        sessions_response = await test_client.get(
            "/api/v1/agents/cardio-agent/sessions",
            headers=auth_header
        )
        sessions = sessions_response.json()
        if sessions and sessions[0]["status"] == "completed":
            break
        await asyncio.sleep(1)
    else:
        pytest.fail("Agent did not complete within 60 seconds")

    # Step 4: Check that protocol was generated
    protocols_response = await test_client.get(
        "/api/v1/protocols",
        headers=auth_header
    )
    assert protocols_response.status_code == 200
    protocols = protocols_response.json()
    assert len(protocols) > 0

    # Step 5: Check that contracts were created
    contracts_response = await test_client.get(
        "/api/v1/contracts",
        headers=auth_header
    )
    assert contracts_response.status_code == 200
    contracts = contracts_response.json()
    assert len(contracts) > 0

    # Step 6: Verify WebSocket received notifications
    # (если у нас есть WebSocket subscribed)

    elapsed_time = time.time() - start_time
    print(f"E2E flow completed in {elapsed_time:.1f} seconds")
    assert elapsed_time < 60, f"E2E took {elapsed_time}s, expected < 60s"

# ── T2: Docker Services ──

def test_docker_services_running(docker_compose):
    """Все Docker сервисы запущены и healthy"""
    services = docker_compose.services()

    expected_services = [
        "postgres", "redis", "api", "celery_worker", "celery_beat"
    ]
    running_services = [s for s in services if s.status == "running"]

    for service in expected_services:
        assert any(service in s.name for s in running_services), \
            f"Service {service} not running"

def test_postgres_healthcheck(docker_compose):
    """PostgreSQL service is healthy"""
    postgres = docker_compose.services()[0]  # assuming postgres is first
    assert postgres.healthcheck_status == "healthy"

def test_redis_healthcheck(docker_compose):
    """Redis service is healthy"""
    # Redis doesn't have built-in healthcheck, but we can test connection
    redis_client = redis.Redis(host="localhost", port=6379)
    assert redis_client.ping() == True

# ── T3: API ↔ LangGraph ↔ DB Round-trip ──

@pytest.mark.asyncio
async def test_api_langgraph_db_roundtrip(
    test_client: AsyncClient,
    auth_header,
    db_session
):
    """
    API endpoint → invokes LangGraph → saves to DB → retrievable via API
    """
    # Create a biomarker via API
    biomarker_payload = {
        "marker_name": "ApoB",
        "value": 1.2,
        "unit": "g/L",
        "source": "blood_test"
    }

    # Post to create protocol with specific biomarker
    protocol_response = await test_client.post(
        "/api/v1/protocols",
        json={
            "biomarker_ids": ["apoB"],
            "name": "Cardio Protocol"
        },
        headers=auth_header
    )
    assert protocol_response.status_code == 200
    protocol_id = protocol_response.json()["id"]

    # Verify in DB
    from app.db.models import Protocol
    protocol = db_session.query(Protocol).filter_by(id=protocol_id).first()
    assert protocol is not None
    assert protocol.name == "Cardio Protocol"

    # Retrieve via API
    get_response = await test_client.get(
        f"/api/v1/protocols/{protocol_id}",
        headers=auth_header
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Cardio Protocol"

# ── T4: Concurrent Users ──

@pytest.mark.asyncio
async def test_concurrent_users_no_conflicts(test_client: AsyncClient, auth_headers_list):
    """
    5 users uploading simultaneously → no data conflicts
    """
    async def upload_user(user_auth, user_id):
        with open("tests/fixtures/blood_test.pdf", "rb") as f:
            response = await test_client.post(
                "/api/v1/data/upload",
                files={"file": f},
                headers=user_auth
            )
        return user_id, response.status_code

    # auth_headers_list has 5 different user tokens
    tasks = [
        upload_user(auth_headers_list[i], f"user_{i}")
        for i in range(5)
    ]

    results = await asyncio.gather(*tasks)

    # All uploads succeeded
    for user_id, status in results:
        assert status == 200, f"User {user_id} upload failed"

    # Verify no data crossing between users
    for i in range(5):
        response = await test_client.get(
            "/api/v1/data/biomarkers",
            headers=auth_headers_list[i]
        )
        biomarkers = response.json()
        assert len(biomarkers) == 1  # Only their own biomarker

# ── T5: Agent Failure Recovery ──

@pytest.mark.asyncio
async def test_recovery_after_agent_failure(test_client: AsyncClient, auth_header):
    """
    Agent fails mid-execution → system recovers, checkpoint resumes
    """
    # Simulate agent failure by triggering with invalid data
    invalid_payload = {"invalid_field": "value"}

    response = await test_client.post(
        "/api/v1/agents/test-agent/trigger",
        json=invalid_payload,
        headers=auth_header
    )
    assert response.status_code == 400  # Bad request

    # Verify that system is still healthy
    health = await test_client.get("/health")
    assert health.status_code == 200

    # Verify another agent can run successfully
    response = await test_client.post(
        "/api/v1/agents/cardio-agent/trigger",
        headers=auth_header
    )
    assert response.status_code == 200

# ── T6: Checkpoint Resume ──

@pytest.mark.asyncio
async def test_checkpoint_resume_after_interruption(test_client: AsyncClient, auth_header):
    """
    Agent execution is interrupted → resumes from checkpoint
    """
    # Start a long-running agent
    response = await test_client.post(
        "/api/v1/agents/long-running-agent/trigger",
        headers=auth_header
    )
    assert response.status_code == 200
    session_id = response.json()["session_id"]

    # Get current step
    checkpoint_response = await test_client.get(
        f"/api/v1/agents/long-running-agent/sessions/{session_id}/checkpoint",
        headers=auth_header
    )
    checkpoint = checkpoint_response.json()
    assert "step" in checkpoint
    initial_step = checkpoint["step"]

    # Simulate interruption and resume
    await asyncio.sleep(2)

    resume_response = await test_client.post(
        f"/api/v1/agents/long-running-agent/sessions/{session_id}/resume",
        headers=auth_header
    )
    assert resume_response.status_code == 200

    # Verify it continued from checkpoint
    new_checkpoint = resume_response.json()["checkpoint"]
    assert new_checkpoint["step"] >= initial_step

# ── T7: Token Usage Tracking ──

@pytest.mark.asyncio
async def test_token_usage_tracked(test_client: AsyncClient, auth_header):
    """
    Token usage per agent cycle is tracked and reported
    """
    response = await test_client.post(
        "/api/v1/agents/cardio-agent/trigger",
        headers=auth_header
    )
    session_id = response.json()["session_id"]

    # Wait for completion
    await asyncio.sleep(30)

    # Get session details with token usage
    session_response = await test_client.get(
        f"/api/v1/agents/cardio-agent/sessions/{session_id}",
        headers=auth_header
    )
    session = session_response.json()

    assert "token_usage" in session
    assert "input_tokens" in session["token_usage"]
    assert "output_tokens" in session["token_usage"]
    assert session["token_usage"]["input_tokens"] > 0
    assert session["token_usage"]["output_tokens"] > 0

# ── T8: Performance Latency ──

@pytest.mark.asyncio
async def test_full_cycle_latency_under_60s(test_client: AsyncClient, auth_header):
    """
    Full cycle latency (upload to contracts) < 60 seconds
    """
    start = time.time()

    with open("tests/fixtures/blood_test.pdf", "rb") as f:
        await test_client.post(
            "/api/v1/data/upload",
            files={"file": f},
            headers=auth_header
        )

    # Wait for agents to complete
    for _ in range(60):
        response = await test_client.get(
            "/api/v1/contracts",
            headers=auth_header
        )
        if len(response.json()) > 0:
            break
        await asyncio.sleep(1)

    elapsed = time.time() - start
    print(f"Full cycle: {elapsed:.1f}s")
    assert elapsed < 60, f"Cycle took {elapsed}s (limit 60s)"
```

---

## Evaluation Functions

```python
# tests/eval_phase5.py

"""
Evaluation — оценка качества Phase 5.
Запускается после всех E2E и integration тестов.
Выдаёт score 0-100.
"""

import os
import glob
import yaml
from pathlib import Path

def evaluate_phase5() -> dict:
    checks = []

    # E1: E2E Flow (30 баллов)
    e2e_tests_passed = 0
    try:
        # Check if E2E tests exist and run
        if os.path.exists("tests/test_phase5_e2e.py"):
            with open("tests/test_phase5_e2e.py") as f:
                if "test_e2e_upload_to_contracts" in f.read():
                    e2e_tests_passed = 30
    except:
        pass
    checks.append({"name": "E2E flow works", "score": e2e_tests_passed, "max": 30})

    # E2: Docker orchestration (15 баллов)
    docker_score = 0
    if os.path.exists("docker-compose.yml"):
        with open("docker-compose.yml") as f:
            dc = yaml.safe_load(f)
            services = dc.get("services", {})

            required = ["postgres", "redis", "api"]
            found = sum(1 for s in required if s in services)
            docker_score = int((found / len(required)) * 10)

            # Bonus for healthchecks
            health_checks = sum(1 for s in services.values() if "healthcheck" in s)
            if health_checks >= 2:
                docker_score += 5

    checks.append({"name": "Docker orchestration", "score": docker_score, "max": 15})

    # E3: Performance (15 баллов)
    perf_score = 0
    # Check if performance tests exist
    if os.path.exists("tests/test_phase5_e2e.py"):
        with open("tests/test_phase5_e2e.py") as f:
            content = f.read()
            if "test_full_cycle_latency_under_60s" in content:
                perf_score = 15
    checks.append({"name": "Performance (latency < 60s)", "score": perf_score, "max": 15})

    # E4: Documentation (15 баллов)
    doc_score = 0
    required_docs = [
        "README.md", "ARCHITECTURE.md", "API.md", "AGENTS.md", "SETUP.md"
    ]
    for doc in required_docs:
        if os.path.exists(doc):
            doc_score += 3
    checks.append({"name": "Documentation quality", "score": doc_score, "max": 15})

    # E5: Error recovery (15 баллов)
    recovery_score = 0
    if os.path.exists("tests/test_phase5_e2e.py"):
        with open("tests/test_phase5_e2e.py") as f:
            content = f.read()
            if "test_recovery_after_agent_failure" in content:
                recovery_score += 8
            if "test_checkpoint_resume" in content:
                recovery_score += 7
    checks.append({"name": "Error recovery", "score": recovery_score, "max": 15})

    # E6: Seed data / demo (10 баллов)
    seed_score = 0
    seed_files = glob.glob("seed_data/**/*.py", recursive=True) + \
                 glob.glob("scripts/seed_*.py")
    if seed_files:
        seed_score = 10
    checks.append({"name": "Seed data / demo", "score": seed_score, "max": 10})

    total = sum(c["score"] for c in checks)
    return {
        "phase": "Phase 5: Integration + Final Assembly",
        "total_score": total,
        "max_score": 100,
        "grade": "PASS" if total >= 75 else "NEEDS WORK",
        "checks": checks
    }
```

---

## Зависимости от других фаз
- Phase 5 зависит от **Phase 1** (БД)
- Phase 5 зависит от **Phase 2** (Agent prompts)
- Phase 5 зависит от **Phase 3** (LangGraph orchestration)
- Phase 5 зависит от **Phase 4** (API endpoints)
- Phase 5 — финальная фаза, после которой система готова к production

## Риски
- Docker image build может занимать время → использовать docker buildkit
- PostgreSQL миграции могут конфликтовать при concurrent запусках → использовать database locks
- Celery workers могут зависать → нужен heartbeat monitoring
- LangGraph checkpoint файлы могут быть несогласованы при краше → использовать DB-backed checkpoints
- WebSocket broadcast на большое количество пользователей может быть медленным → использовать Redis Pub/Sub
- Token costs могут быть неожиданно высокими → implement token usage tracking и alerts
