# PLT Platform — Инструкция по запуску

## Что тебе понадобится

- **Docker Desktop** (24+) — [скачать](https://www.docker.com/products/docker-desktop/)
- **Node.js** (18+) — [скачать](https://nodejs.org/)
- **Anthropic API Key** — [получить](https://console.anthropic.com/)
- ~4 GB свободного RAM для Docker

---

## Шаг 1: Подготовка

Открой Terminal и перейди в папку проекта:

```bash
cd ~/path/to/Personal\ Longevity\ Team/plt-platform
```

Скопируй файл окружения и вставь свой API ключ:

```bash
cp .env.example .env
```

Открой `.env` в редакторе и замени строку:
```
ANTHROPIC_API_KEY=sk-ant-xxx
```
на свой реальный ключ от Anthropic.

---

## Шаг 2: Запуск бэкенда (Docker)

```bash
# Убедись что Docker Desktop запущен, затем:
docker compose up -d
```

Это запустит 6 сервисов:

| Сервис | Порт | Назначение |
|--------|------|-----------|
| PostgreSQL (TimescaleDB) | 5432 | База данных + time-series |
| Redis | 6379 | Кэш + event bus |
| MinIO | 9000 / 9001 | S3-хранилище файлов |
| FastAPI | **8000** | API сервер |
| Celery Worker | — | Фоновые задачи |
| Celery Beat | — | Планировщик задач |

Проверь что всё поднялось:

```bash
docker compose ps
```

Все сервисы должны быть в статусе `running` или `healthy`.

---

## Шаг 3: Применение миграций БД

```bash
docker compose exec api alembic upgrade head
```

Это создаст все таблицы: users, biomarkers, digital_twins, protocols, contracts, agents и т.д.

---

## Шаг 4: Загрузка демо-данных (опционально)

```bash
docker compose exec api python -m scripts.seed_data
```

Создаст:
- Демо-пользователя: `demo@longevity.ai` / `demo123`
- 300 записей биомаркеров (30 дней)
- Digital Twin с 11 системами
- 3 протокола здоровья
- 7 дневных контрактов
- 5 добавок в инвентаре

---

## Шаг 5: Проверка бэкенда

Открой в браузере:

- **API Health**: http://localhost:8000/health
- **Swagger Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (логин: minioadmin / minioadmin)

Быстрый тест через curl:

```bash
# Health check
curl http://localhost:8000/health

# Регистрация пользователя
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123", "name": "Test User"}'

# Логин (получить JWT токен)
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123"}'
```

---

## Шаг 6: Запуск фронтенда

В **новом** окне Terminal:

```bash
cd frontend
npm install
npm run dev
```

Фронтенд откроется на: **http://localhost:3000**

---

## Что ты увидишь

### Фронтенд (localhost:3000)
- **Dashboard** — Longevity Score, Biological Age, виджеты
- **Digital Twin** — 11 систем тела с оценками
- **Biomarkers** — 21 биомаркер с графиками
- **Daily Contracts** — чеклист задач на день
- **Agents** — 27 AI-агентов в 6 тирах
- **Upload** — загрузка PDF анализов
- **Protocols** — протоколы здоровья
- **Profile** — настройки и подключения

### API (localhost:8000/docs)
- 42 endpoint'a с интерактивной документацией Swagger
- Авторизация через JWT

---

## Полезные команды

```bash
# Логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f api

# Перезапуск API после изменений
docker compose restart api

# Остановить всё
docker compose down

# Остановить и удалить данные
docker compose down -v

# Пересобрать после изменений в коде
docker compose up -d --build
```

---

## Устранение проблем

**Docker не запускается:**
- Убедись что Docker Desktop запущен (иконка в меню)
- На Mac: System Settings → Privacy → Full Disk Access → Docker

**Порт 5432 занят:**
- Локальный PostgreSQL работает. Останови его: `brew services stop postgresql`
- Или измени порт в docker-compose.yml: `"5433:5432"`

**Порт 8000 занят:**
- Измени в docker-compose.yml: `"8001:8000"`
- Обнови CORS_ORIGINS в .env

**API возвращает 500:**
- Проверь логи: `docker compose logs api`
- Убедись что миграции применены: `docker compose exec api alembic upgrade head`

**Фронтенд не подключается к API:**
- Проверь что API работает: `curl http://localhost:8000/health`
- Проверь CORS_ORIGINS в .env включает `http://localhost:3000`

**"Cannot connect to Docker daemon":**
- Docker Desktop не запущен → открой его
- Linux: `sudo systemctl start docker`
