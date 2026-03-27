# Phase 4: FastAPI Endpoints + Services — API, WebSocket, Data Pipeline

## Цель
Построить полный API слой с EndPoint'ами для работы с данными, WebSocket для real-time обновлений, сервисы для загрузки файлов и синхронизации внешних источников (Oura, Apple Health), фоновые задачи на Celery, Redis event bus для inter-service коммуникации, JWT-аутентификация и rate limiting.

## Дата начала: TBD
## Дата завершения: TBD
## Статус: ОЖИДАЕТ УТВЕРЖДЕНИЯ

---

## Deliverables (что должно быть на выходе)

### 1. FastAPI Routers
- `/api/v1/data` — upload файлов (PDF, CSV, JSON), синхронизация с внешними API
  - `POST /data/upload` — загрузить файл (PDF, CSV)
  - `GET /data/biomarkers` — получить все биомаркеры пользователя
  - `POST /data/sync/oura` — синхронизировать данные Oura
  - `POST /data/sync/apple-health` — импортировать данные Apple Health

- `/api/v1/twin` — управление Digital Twin
  - `GET /twin` — получить состояние Twin'а
  - `PATCH /twin` — обновить параметры Twin'а
  - `GET /twin/health-metrics` — метрики здоровья

- `/api/v1/agents` — управление агентами и сессиями
  - `GET /agents` — список всех Agent Type'ов
  - `GET /agents/{agent_id}/sessions` — истории сессий агента
  - `POST /agents/{agent_id}/trigger` — принудительно запустить агента

- `/api/v1/contracts` — управление контрактами
  - `GET /contracts` — все контракты пользователя
  - `GET /contracts/{contract_id}` — детали контракта
  - `PATCH /contracts/{contract_id}/status` — изменить статус (active, completed, failed)

- `/api/v1/protocols` — управление протоколами
  - `GET /protocols` — все протоколы
  - `GET /protocols/{protocol_id}` — детали протокола
  - `POST /protocols` — создать новый протокол

- `/api/v1/score` — получение Health Score
  - `GET /score/current` — текущий Health Score
  - `GET /score/history` — история Score'ов
  - `GET /score/breakdown` — разбор по категориям (nutrition, exercise, sleep и т.д.)

- `/api/v1/inventory` — управление инвентарем добавок
  - `GET /inventory` — все добавки
  - `POST /inventory` — добавить новую добавку
  - `DELETE /inventory/{item_id}` — удалить добавку

### 2. WebSocket Hub
- `/ws/v1/live` — real-time подписка на события
  - Подключение: WS-протокол
  - События: агент завершил сессию, появились новые биомаркеры, статус контракта изменился
  - Broadcasting: все события отправляются all connected клиентам пользователя
  - Heartbeat каждые 30 сек

### 3. File Upload Service
- S3 или MinIO интеграция
- `FileUploadService` класс:
  - `async def upload_file(file, user_id) -> file_id`
  - `async def parse_pdf(file) → structured_data` (OCR via Claude Vision API)
  - `async def sync_with_oura(user_id, token) → biomarker_list`
  - `async def import_apple_health(file, user_id) → biomarker_list`

### 4. Data Pipeline
- PDF parsing: Claude Vision API + OCR
- Oura Ring API sync: сердечный ритм, сон, активность, ReadinessScore
- Apple Health import: извлечение XML, парсинг, валидация
- Output: структурированные Biomarker записи в БД

### 5. Celery Tasks
- Daily morning trigger: запуск всех агентов в 8 AM по времени пользователя
- Data sync: запуск раз в час синхронизация Oura
- Anomaly detection: проверка биомаркеров на аномалии каждые 6 часов
- Task results хранятся в Redis

### 6. Redis Event Bus
- `publish(event_type, data)` — публикация события
- `subscribe(event_type, handler)` — подписка на события
- Event types: `biomarker_added`, `agent_completed`, `contract_created`, `anomaly_detected`
- Используется для синхронизации между API, Celery и WebSocket

### 7. Auth (JWT)
- JWT tokens с `user_id`, `exp`, `scope`
- `Authorization: Bearer <token>` header
- Refresh token механизм
- `get_current_user()` dependency для всех защищённых endpoint'ов

### 8. Rate Limiting
- 100 requests per minute для обычных endpoint'ов
- 10 uploads per minute для file upload
- 1000 WebSocket messages per hour
- Хранится в Redis, возвращает 429 Too Many Requests

---

## Критерии приёмки (Definition of Done)

1. Все 7 routers реализованы с полным CRUD
2. WebSocket endpoint доступен, поддерживает real-time broadcast
3. File upload работает: PDF → Claude Vision → structured biomarkers
4. Oura API sync работает: OAuth → получение данных → сохранение в БД
5. Apple Health import работает: XML парсинг → biomarkers в БД
6. Celery tasks выполняются по расписанию
7. Redis event bus работает: publish/subscribe функциональность
8. JWT auth валидирует токены, 401 без токена
9. Rate limiting работает: 429 при превышении лимита
10. CORS настроена: фронтенд может делать кросс-доменные запросы
11. Pydantic validation отвергает невалидные данные (400 ошибка)
12. Все endpoint'ы возвращают правильные status codes

---

## Test Functions

```python
# tests/test_phase4.py

import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
import json

# ── T1: API Endpoints return correct status codes ──

@pytest.mark.asyncio
async def test_data_upload_endpoint(test_client: AsyncClient, auth_header):
    """POST /data/upload принимает файл и возвращает 200"""
    with open("tests/fixtures/blood_test.pdf", "rb") as f:
        response = await test_client.post(
            "/api/v1/data/upload",
            files={"file": f},
            headers=auth_header
        )
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert "parsed_data" in data

@pytest.mark.asyncio
async def test_get_biomarkers_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/data/biomarkers возвращает 200"""
    response = await test_client.get(
        "/api/v1/data/biomarkers",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("marker_name" in b for b in data)

@pytest.mark.asyncio
async def test_sync_oura_endpoint(test_client: AsyncClient, auth_header):
    """POST /data/sync/oura возвращает 200"""
    payload = {"oura_token": "test_token_123"}
    response = await test_client.post(
        "/api/v1/data/sync/oura",
        json=payload,
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "synced_count" in data

@pytest.mark.asyncio
async def test_twin_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/twin возвращает 200"""
    response = await test_client.get(
        "/api/v1/twin",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "user_id" in data

@pytest.mark.asyncio
async def test_agents_list_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/agents возвращает 200"""
    response = await test_client.get(
        "/api/v1/agents",
        headers=auth_header
    )
    assert response.status_code == 200
    agents = response.json()
    assert isinstance(agents, list)

@pytest.mark.asyncio
async def test_contracts_list_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/contracts возвращает 200"""
    response = await test_client.get(
        "/api/v1/contracts",
        headers=auth_header
    )
    assert response.status_code == 200
    contracts = response.json()
    assert isinstance(contracts, list)

@pytest.mark.asyncio
async def test_protocols_list_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/protocols возвращает 200"""
    response = await test_client.get(
        "/api/v1/protocols",
        headers=auth_header
    )
    assert response.status_code == 200
    protocols = response.json()
    assert isinstance(protocols, list)

@pytest.mark.asyncio
async def test_score_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/score/current возвращает 200"""
    response = await test_client.get(
        "/api/v1/score/current",
        headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert 0 <= data["score"] <= 100

@pytest.mark.asyncio
async def test_inventory_endpoint(test_client: AsyncClient, auth_header):
    """GET /api/v1/inventory возвращает 200"""
    response = await test_client.get(
        "/api/v1/inventory",
        headers=auth_header
    )
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)

# ── T2: Auth middleware ──

@pytest.mark.asyncio
async def test_auth_without_token(test_client: AsyncClient):
    """GET без токена возвращает 401"""
    response = await test_client.get("/api/v1/twin")
    assert response.status_code == 401
    assert "unauthorized" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_auth_with_valid_token(test_client: AsyncClient, auth_header):
    """GET с валидным токеном возвращает 200"""
    response = await test_client.get("/api/v1/twin", headers=auth_header)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_auth_with_invalid_token(test_client: AsyncClient):
    """GET с невалидным токеном возвращает 401"""
    headers = {"Authorization": "Bearer invalid_token_xyz"}
    response = await test_client.get("/api/v1/twin", headers=headers)
    assert response.status_code == 401

# ── T3: File upload service ──

@pytest.mark.asyncio
async def test_pdf_upload_and_parse(test_client: AsyncClient, auth_header):
    """PDF загружается и парсится через Claude Vision"""
    with open("tests/fixtures/blood_test_report.pdf", "rb") as f:
        response = await test_client.post(
            "/api/v1/data/upload",
            files={"file": f},
            headers=auth_header
        )
    assert response.status_code == 200
    data = response.json()
    assert "parsed_data" in data
    # Проверяем что Claude Vision вернул структурированные данные
    parsed = data["parsed_data"]
    assert "biomarkers" in parsed or "test_results" in parsed

@pytest.mark.asyncio
async def test_upload_invalid_file_type(test_client: AsyncClient, auth_header):
    """Upload файла неподдерживаемого типа возвращает 400"""
    with open("tests/fixtures/data.txt", "rb") as f:
        response = await test_client.post(
            "/api/v1/data/upload",
            files={"file": ("data.txt", f, "text/plain")},
            headers=auth_header
        )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_upload_file_size_limit(test_client: AsyncClient, auth_header):
    """Upload файла > 50MB возвращает 413"""
    large_file = b"x" * (51 * 1024 * 1024)  # 51MB
    response = await test_client.post(
        "/api/v1/data/upload",
        files={"file": ("large.pdf", large_file)},
        headers=auth_header
    )
    assert response.status_code == 413

# ── T4: WebSocket ──

@pytest.mark.asyncio
async def test_websocket_connect(test_client: AsyncClient, auth_header):
    """WebSocket подключается с валидным токеном"""
    token = auth_header["Authorization"].split(" ")[1]
    with test_client.websocket_connect(f"/ws/v1/live?token={token}") as ws:
        # Отправляем heartbeat
        ws.send_json({"type": "ping"})
        data = ws.receive_json()
        assert data["type"] == "pong"

@pytest.mark.asyncio
async def test_websocket_receives_biomarker_event(test_client: AsyncClient, auth_header, db_session):
    """WebSocket получает событие когда появляется новый биомаркер"""
    token = auth_header["Authorization"].split(" ")[1]
    with test_client.websocket_connect(f"/ws/v1/live?token={token}") as ws:
        # В отдельном потоке добавляем биомаркер
        # Проверяем что WebSocket получит событие
        data = ws.receive_json(timeout=5)
        assert data["type"] == "biomarker_added"
        assert "biomarker" in data

@pytest.mark.asyncio
async def test_websocket_rejects_invalid_token(test_client: AsyncClient):
    """WebSocket отвергает невалидный токен"""
    with pytest.raises(Exception):  # connection refused
        with test_client.websocket_connect("/ws/v1/live?token=invalid") as ws:
            pass

# ── T5: Celery tasks ──

def test_celery_daily_morning_trigger(celery_app):
    """Celery task для утреннего триггера выполняется"""
    result = celery_app.send_task(
        "tasks.trigger_morning_agents",
        args=("user_123",)
    )
    assert result.successful()

def test_celery_data_sync_task(celery_app):
    """Celery task для синхронизации данных выполняется"""
    result = celery_app.send_task(
        "tasks.sync_oura_data",
        args=("user_123",)
    )
    assert result.successful()

def test_celery_anomaly_detection_task(celery_app):
    """Celery task для обнаружения аномалий выполняется"""
    result = celery_app.send_task(
        "tasks.detect_anomalies",
        args=("user_123",)
    )
    assert result.successful()

# ── T6: Redis event bus ──

@pytest.mark.asyncio
async def test_redis_publish_subscribe(redis_client):
    """Redis pub/sub работает"""
    async def subscriber():
        sub = redis_client.subscribe("test_channel")
        msg = await sub.get()
        return msg

    # Публикуем сообщение
    redis_client.publish("test_channel", "test_data")

    # Проверяем что подписчик получит сообщение
    # (тут нужна правильная реализация async pub/sub)

@pytest.mark.asyncio
async def test_event_bus_biomarker_event(redis_client):
    """Event bus публикует событие 'biomarker_added'"""
    from app.services.event_bus import publish_event

    event_data = {"user_id": "user_123", "marker_name": "ApoB", "value": 1.12}
    await publish_event("biomarker_added", event_data)

    # Проверяем что сообщение в Redis
    # (нужна реализация для проверки)

# ── T7: Rate limiting ──

@pytest.mark.asyncio
async def test_rate_limiting_api(test_client: AsyncClient, auth_header):
    """Rate limiting: 100 req/min для обычных endpoint'ов"""
    for i in range(101):
        response = await test_client.get(
            "/api/v1/twin",
            headers=auth_header
        )
        if i < 100:
            assert response.status_code == 200
        else:
            assert response.status_code == 429

@pytest.mark.asyncio
async def test_rate_limiting_upload(test_client: AsyncClient, auth_header):
    """Rate limiting: 10 uploads/min для file upload"""
    for i in range(11):
        with open("tests/fixtures/test.pdf", "rb") as f:
            response = await test_client.post(
                "/api/v1/data/upload",
                files={"file": f},
                headers=auth_header
            )
        if i < 10:
            assert response.status_code == 200
        else:
            assert response.status_code == 429

# ── T8: CORS ──

@pytest.mark.asyncio
async def test_cors_headers(test_client: AsyncClient, auth_header):
    """CORS headers присутствуют в ответе"""
    response = await test_client.get(
        "/api/v1/twin",
        headers={**auth_header, "Origin": "http://localhost:3000"}
    )
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

# ── T9: Pydantic validation ──

@pytest.mark.asyncio
async def test_validation_missing_required_field(test_client: AsyncClient, auth_header):
    """Pydantic validation отвергает запрос с недостающим полем"""
    response = await test_client.post(
        "/api/v1/inventory",
        json={"name": "Vitamin D"},  # missing 'dosage' field
        headers=auth_header
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_validation_invalid_data_type(test_client: AsyncClient, auth_header):
    """Pydantic validation отвергает неправильный тип данных"""
    response = await test_client.post(
        "/api/v1/inventory",
        json={"name": "Vitamin D", "dosage": "invalid_number"},
        headers=auth_header
    )
    assert response.status_code == 422
```

---

## Evaluation Functions

```python
# tests/eval_phase4.py

"""
Evaluation — оценка качества Phase 4.
Запускается после прохождения всех test functions.
Выдаёт score 0-100 и детальный отчёт.
"""

import glob
import os
from pathlib import Path

def evaluate_phase4() -> dict:
    checks = []

    # E1: Endpoint coverage (25 баллов)
    required_endpoints = [
        "/api/v1/data/upload",
        "/api/v1/data/biomarkers",
        "/api/v1/data/sync/oura",
        "/api/v1/data/sync/apple-health",
        "/api/v1/twin",
        "/api/v1/agents",
        "/api/v1/contracts",
        "/api/v1/protocols",
        "/api/v1/score",
        "/api/v1/inventory",
    ]

    # Проверяем что все роутеры существуют
    router_files = glob.glob("app/api/routes/*.py")
    endpoints_count = 0
    for file in router_files:
        with open(file) as f:
            content = f.read()
            for endpoint in required_endpoints:
                if endpoint in content:
                    endpoints_count += 1

    score_endpoints = int((endpoints_count / len(required_endpoints)) * 25)
    checks.append({"name": "Endpoint coverage", "score": score_endpoints, "max": 25})

    # E2: Auth & security (15 баллов)
    auth_score = 0
    if os.path.exists("app/api/auth.py"):
        with open("app/api/auth.py") as f:
            content = f.read()
            if "jwt" in content.lower():
                auth_score += 5
            if "oauth" in content.lower() or "token" in content.lower():
                auth_score += 5
            if "refresh_token" in content.lower():
                auth_score += 5
    checks.append({"name": "Auth & security", "score": auth_score, "max": 15})

    # E3: WebSocket (15 баллов)
    ws_score = 0
    if os.path.exists("app/api/websocket.py"):
        with open("app/api/websocket.py") as f:
            content = f.read()
            if "websocket" in content.lower():
                ws_score += 5
            if "broadcast" in content.lower():
                ws_score += 5
            if "heartbeat" in content.lower() or "ping" in content.lower():
                ws_score += 5
    checks.append({"name": "WebSocket real-time", "score": ws_score, "max": 15})

    # E4: Data pipeline (15 баллов)
    pipeline_score = 0
    if os.path.exists("app/services/file_upload.py"):
        with open("app/services/file_upload.py") as f:
            content = f.read()
            if "pdf" in content.lower():
                pipeline_score += 3
            if "claude" in content.lower() or "vision" in content.lower():
                pipeline_score += 3
            if "oura" in content.lower():
                pipeline_score += 3
            if "apple" in content.lower():
                pipeline_score += 3
            if "biomarker" in content.lower():
                pipeline_score += 3
    checks.append({"name": "Data pipeline", "score": pipeline_score, "max": 15})

    # E5: Background tasks (10 баллов)
    celery_score = 0
    if os.path.exists("app/tasks/celery_tasks.py"):
        with open("app/tasks/celery_tasks.py") as f:
            content = f.read()
            if "trigger" in content.lower() or "schedule" in content.lower():
                celery_score += 3
            if "sync" in content.lower():
                celery_score += 3
            if "anomaly" in content.lower():
                celery_score += 4
    checks.append({"name": "Background tasks (Celery)", "score": celery_score, "max": 10})

    # E6: Error handling & validation (10 баллов)
    validation_score = 0
    if os.path.exists("app/api/schemas.py"):
        with open("app/api/schemas.py") as f:
            content = f.read()
            if "pydantic" in content.lower() or "BaseModel" in content:
                validation_score += 5
            # Count number of Pydantic models
            model_count = content.count("class ") - 1
            if model_count >= 10:
                validation_score += 5
    checks.append({"name": "Error handling & validation", "score": validation_score, "max": 10})

    # E7: Code quality (10 баллов)
    quality_score = 0
    python_files = glob.glob("app/**/*.py", recursive=True)
    has_type_hints = 0
    has_docstrings = 0

    for file in python_files:
        with open(file) as f:
            content = f.read()
            if "->" in content and ":" in content:
                has_type_hints += 1
            if '"""' in content or "'''" in content:
                has_docstrings += 1

    quality_score = int((min(has_type_hints, 5) / 5) * 5)
    quality_score += int((min(has_docstrings, 5) / 5) * 5)
    checks.append({"name": "Code quality", "score": quality_score, "max": 10})

    total = sum(c["score"] for c in checks)
    return {
        "phase": "Phase 4: FastAPI Endpoints + Services",
        "total_score": total,
        "max_score": 100,
        "grade": "PASS" if total >= 75 else "NEEDS WORK",
        "checks": checks
    }
```

---

## Зависимости от других фаз
- Phase 4 зависит от **Phase 1** (БД, модели)
- Phase 4 может быть частично независима от Phase 2, 3 (можно мокировать LangGraph)
- Phase 5 зависит от Phase 4

## Риски
- Claude Vision API может быть медленным (10-20 сек на один PDF) → нужно асинхронно обрабатывать
- Oura API требует OAuth flow → нужно тестировать с реальным API key
- Apple Health XML формат может различаться по версиям → нужна гибкая парсинг логика
- WebSocket broadcast может быть неэффективным при большом количестве подключений → использовать Redis Pub/Sub для масштабирования
- Celery без Redis может теряться при перезагрузке → обязательно Redis для task results
- Rate limiting на Redis может быть bottleneck при высокой нагрузке → рассмотреть in-memory cache
