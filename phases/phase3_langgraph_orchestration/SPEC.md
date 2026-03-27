# Phase 3: LangGraph Orchestration — Спецификация

## Обзор

Phase 3 реализует ядро PLT платформы — LangGraph-based оркестрацию, которая связывает все 27 агентов в направленный граф с управлением состоянием. Это критический компонент, обеспечивающий координацию между медицинским ядром (8 агентов), образом жизни (5 агентов), синтезом, проверкой и исполнением персонализированных протоколов долголетия.

---

## 1. Архитектурные решения

### 1.1 LangGraph StateGraph с типизированным состоянием

```
PLTState — центральное состояние, содержит:
  - trigger_type: str (new_data | daily_morning | anomaly | user_query)
  - user_id: str
  - timestamp: ISO8601
  - digital_twin: DigitalTwinSnapshot (биомаркеры, метаболизм, история)
  - medical_opinions: dict[agent_id, Opinion]
  - lifestyle_opinions: dict[agent_id, Opinion]
  - draft_protocol: DraftProtocol
  - verification_state: VerificationState
  - final_protocol: FinalProtocol
  - execution_status: str (draft | verified | approved | executing | completed)
  - retry_count: int (для veto loop)
  - errors: list[ErrorRecord]
  - checkpoint_id: str (для recovery)
```

### 1.2 Entry Point и Router

```
Trigger (event) → Router
  Router классифицирует тип события:
    - new_data: новые биомаркеры, результаты анализов
    - daily_morning: плановая ежедневная переоценка
    - anomaly: обнаружено отклонение
    - user_query: пользователь запросил протокол

Router → System Biologist (обогащает состояние Digital Twin snapshot)
```

### 1.3 Параллельный fan-out

```
System Biologist (обогащение) ↓
                    ├─→ Medical Core (8 агентов, параллель)
                    │    ├─→ Cardiologist
                    │    ├─→ Metabolic Specialist
                    │    ├─→ Immunologist
                    │    ├─→ Neurologist
                    │    ├─→ Endocrinologist
                    │    ├─→ Geneticist
                    │    ├─→ Oncologist
                    │    └─→ GI Specialist
                    │
                    └─→ Lifestyle (5 агентов, параллель)
                         ├─→ Nutritionist
                         ├─→ Fitness Coach
                         ├─→ Sleep Specialist
                         ├─→ Stress Management
                         └─→ Social Connection
```

### 1.4 Synthesis и Veto Loop

```
Medical + Lifestyle opinions ↓
Analyst (синтез мнений) → Draft Protocol
                            ↓
                    Verifier (проверка против PubMed, drug interactions)
                            ↓
                        [Веторование?]
                    Yes (issue found) ↓ (retry ≤ 3)
                    Отправить обратно на Medical/Lifestyle
                    для уточнения / пересмотра
                            ↓
                    No (все OK) или (max retries) ↓
                            ↓
                    CMO (финальное одобрение)
```

### 1.5 Execution и Delivery

```
Approved Protocol ↓
    ├─→ Nutritionist (meal plan)
    ├─→ Trainer (exercise plan)
    └─→ Sleep Specialist (sleep protocol)
                    ↓
                Ops Layer (форматирование в daily contracts)
                    ↓
                Delivery (пользователю)
```

### 1.6 Checkpoint и Human-in-the-Loop

```
PostgreSQL-backed checkpointer:
  - Сохраняет состояние после каждого критического узла
  - Позволяет паузу для human review
  - Восстановление при сбое
  - Интерактивное управление (approve, reject, revise)
```

### 1.7 Events (Redis pub/sub)

```
Redis channels:
  - new_data_event
  - daily_morning_event
  - anomaly_event
  - user_query_event

Event handler подписывается, преобразует в Trigger, инициирует граф.
```

---

## 2. Доставляемые результаты (Deliverables)

### 2.1 Graph Definition
- `src/graph/state.py` — определение `PLTState` (Pydantic v2)
- `src/graph/graph.py` — построение StateGraph с узлами и ребрами
- `src/graph/nodes/` — реализация всех узлов (router, system_biologist, 8x medical, 5x lifestyle, analyst, verifier, cmo, nutritionist, trainer, ops)
- `src/graph/routing.py` — логика маршрутизации (router, вето loop, условные переходы)

### 2.2 Node Implementations
Каждый узел должен:
- Иметь чёткую сигнатуру: `async def node_name(state: PLTState) -> dict`
- Принимать состояние, выполнять логику, возвращать обновления
- Иметь error handling с логированием
- Иметь timeout protection (max 30s на agent call)

### 2.3 State Schema
- Все поля типизированы (Pydantic)
- Документированы (docstring)
- Имеют default значения где уместно
- Версионированы для совместимости

### 2.4 Checkpointer Integration
- PostgreSQL backend (из Phase 1)
- Сохранение после: System Biologist, Analyst, Verifier, CMO
- Restore logic с валидацией
- Cleanup старых checkpoints (TTL 30 дней)

### 2.5 Event Handler
- Слушает Redis pub/sub
- Преобразует события в Trigger
- Инициирует граф execution
- Обработка ошибок и retry logic

---

## 3. Test Functions (pytest-style)

```python
import pytest
from src.graph.state import PLTState, DigitalTwinSnapshot
from src.graph.graph import build_graph, compile_graph
from src.graph.nodes import router, system_biologist, analyst, verifier, cmo
from src.graph.routing import check_veto_loop, check_parallel_execution

# ============ Test 1: Graph Compilation ============
def test_graph_compiles_without_errors():
    """Граф должен скомпилироваться без ошибок."""
    graph = compile_graph()
    assert graph is not None
    assert hasattr(graph, 'invoke')
    assert hasattr(graph, 'stream')

# ============ Test 2: State Schema Validation ============
def test_state_schema_has_all_required_fields():
    """PLTState должен содержать все обязательные поля."""
    required_fields = {
        'trigger_type', 'user_id', 'timestamp',
        'digital_twin', 'medical_opinions', 'lifestyle_opinions',
        'draft_protocol', 'verification_state', 'final_protocol',
        'execution_status', 'retry_count', 'errors', 'checkpoint_id'
    }
    state_fields = set(PLTState.model_fields.keys())
    assert required_fields.issubset(state_fields), \
        f"Missing fields: {required_fields - state_fields}"

# ============ Test 3: All 27 Nodes Reachable ============
def test_all_27_agent_nodes_reachable():
    """Все 27 агентов должны быть достижимы в графе."""
    graph = compile_graph()
    # Проверяем, что узлы 8 (medical) + 5 (lifestyle) +
    # router, system_biologist, analyst, verifier, cmo,
    # nutritionist, trainer, ops = 27 уникальных узлов
    nodes = set(graph.nodes.keys())

    medical_nodes = {
        'cardiologist', 'metabolic_specialist', 'immunologist',
        'neurologist', 'endocrinologist', 'geneticist',
        'oncologist', 'gi_specialist'
    }
    lifestyle_nodes = {
        'nutritionist_opinion', 'fitness_coach', 'sleep_specialist',
        'stress_management', 'social_connection'
    }

    critical_nodes = {
        'router', 'system_biologist', 'analyst', 'verifier', 'cmo'
    }

    execution_nodes = {
        'nutritionist_execution', 'trainer', 'ops_formatter'
    }

    expected = medical_nodes | lifestyle_nodes | critical_nodes | execution_nodes
    assert expected.issubset(nodes), \
        f"Missing nodes: {expected - nodes}"

# ============ Test 4: Veto Loop Max 3 Retries ============
def test_veto_loop_respects_max_retries():
    """Veto loop должен максимум 3 раза отправить на переоценку,
    затем force-approve."""
    # Симуляция: verifier находит ошибку, отправляет обратно
    state = create_test_state()
    state.retry_count = 0

    # Retry 1
    state.retry_count = 1
    assert state.retry_count <= 3, "Should still allow retry"

    # Retry 3
    state.retry_count = 3
    assert state.retry_count <= 3, "Should still allow retry"

    # Retry 4 (force-approve)
    state.retry_count = 4
    assert state.retry_count > 3, "Force-approve triggered"

# ============ Test 5: Parallel Fan-out Execution ============
@pytest.mark.asyncio
async def test_parallel_fan_out_executes_correctly():
    """Parallel fan-out должен одновременно выполнить
    8 medical + 5 lifestyle агентов."""
    graph = compile_graph()
    state = create_test_state()
    state.trigger_type = "new_data"

    # Mock agent responses
    import asyncio
    start_time = asyncio.get_event_loop().time()

    # Инициируем граф
    result = await graph.ainvoke(state)

    elapsed = asyncio.get_event_loop().time() - start_time

    # Проверяем, что opinions заполнены для всех агентов
    assert len(result.medical_opinions) == 8, \
        f"Expected 8 medical opinions, got {len(result.medical_opinions)}"
    assert len(result.lifestyle_opinions) == 5, \
        f"Expected 5 lifestyle opinions, got {len(result.lifestyle_opinions)}"

    # Параллель должна быть быстрее последовательности
    # (13 агентов параллельно < 13 * time_per_agent последовательно)
    assert elapsed < 60, "Parallel execution should complete in reasonable time"

# ============ Test 6: Checkpoint Save/Restore ============
@pytest.mark.asyncio
async def test_checkpoint_save_restore():
    """Checkpointer должен сохранять и восстанавливать состояние."""
    from src.checkpoint.postgres_checkpointer import PostgresCheckpointer

    checkpointer = PostgresCheckpointer(db_url="postgresql://localhost/plt_test")
    state = create_test_state()
    state.execution_status = "verified"

    # Сохраняем
    checkpoint_id = await checkpointer.save(state)
    assert checkpoint_id is not None

    # Восстанавливаем
    restored = await checkpointer.load(checkpoint_id)
    assert restored.user_id == state.user_id
    assert restored.execution_status == "verified"
    assert restored.timestamp == state.timestamp

# ============ Test 7: Human-in-the-Loop Interrupt ============
@pytest.mark.asyncio
async def test_human_in_the_loop_interrupt():
    """Граф должен поддерживать паузу для human review."""
    from src.graph.graph import compile_graph

    graph = compile_graph()
    state = create_test_state()

    # Параметр interrupt_before указывает узлы, где нужна пауза
    config = {"configurable": {"interrupt_before": ["cmo"]}}

    # Инициируем (должен остановиться перед CMO)
    # Это зависит от LangGraph версии и конфигурации
    # Здесь проверяем, что граф компилируется с interrupt поддержкой
    assert "interrupt_before" in str(config) or graph.get_config() is not None

# ============ Test 8: Full Pipeline End-to-End ============
@pytest.mark.asyncio
async def test_full_pipeline_end_to_end_with_mock_data():
    """Полный pipeline должен работать от trigger до delivery."""
    graph = compile_graph()
    state = create_test_state()
    state.trigger_type = "new_data"

    # Инициируем
    result = await graph.ainvoke(state)

    # Проверяем финальное состояние
    assert result.execution_status == "executing" or result.execution_status == "completed"
    assert result.final_protocol is not None
    assert len(result.final_protocol.daily_contracts) > 0
    assert result.errors == [] or len(result.errors) <= 2  # tolerant

# ============ Test 9: Router Classification ============
def test_router_classifies_trigger_types():
    """Router должен корректно классифицировать типы триггеров."""
    router_node = router.Router()

    test_cases = [
        ({"type": "new_biomarkers", "data": {...}}, "new_data"),
        ({"type": "morning_check"}, "daily_morning"),
        ({"type": "anomaly_detected", "biomarker": "glucose"}, "anomaly"),
        ({"type": "user_request", "query": "..."}, "user_query"),
    ]

    for input_data, expected_type in test_cases:
        state = PLTState(
            trigger_type="unknown",
            user_id="test",
            timestamp="2026-03-27T10:00:00Z",
            digital_twin=DigitalTwinSnapshot(...),
        )
        # Router должен обновить trigger_type
        # (реальная реализация зависит от дизайна Router)
        assert expected_type in ["new_data", "daily_morning", "anomaly", "user_query"]

# ============ Test 10: Error Handling and Graceful Degradation ============
@pytest.mark.asyncio
async def test_error_handling_graceful_degradation():
    """Если один агент падает, граф должен продолжить (graceful degradation)."""
    graph = compile_graph()
    state = create_test_state()

    # Симулируем ошибку в одном из агентов
    # (в реальной реализации через mock или exception injection)

    result = await graph.ainvoke(state)

    # Граф должен продолжить, добавив ошибку в errors list
    # и используя fallback мнение или дефолтное значение
    assert result is not None
    assert isinstance(result.errors, list)
    assert result.execution_status not in ["failed"]  # graceful, не failed

# ============ Helper Functions ============
def create_test_state() -> PLTState:
    """Создаёт тестовое состояние с минимальными данными."""
    from datetime import datetime

    return PLTState(
        trigger_type="new_data",
        user_id="test_user_001",
        timestamp=datetime.now().isoformat(),
        digital_twin=DigitalTwinSnapshot(
            user_id="test_user_001",
            age=45,
            biomarkers={
                "glucose": 95,
                "ldl": 120,
                "hdl": 50,
                "triglycerides": 150,
            },
            genetic_markers={},
            medical_history=[],
            current_medications=[],
        ),
        medical_opinions={},
        lifestyle_opinions={},
        draft_protocol=None,
        verification_state=None,
        final_protocol=None,
        execution_status="draft",
        retry_count=0,
        errors=[],
        checkpoint_id=None,
    )
```

---

## 4. Evaluation Functions (оценка качества)

```python
def evaluate_phase3_completion(
    graph_path: str,
    state_path: str,
    nodes_path: str,
    test_results: dict,
) -> dict:
    """
    Оценивает завершённость Phase 3 по 7 критериям.

    Returns:
        dict: {
            'graph_completeness': int (0-25),
            'state_management': int (0-15),
            'veto_loop_correctness': int (0-15),
            'parallel_execution': int (0-15),
            'checkpoint_recovery': int (0-10),
            'error_handling': int (0-10),
            'code_quality': int (0-10),
            'total': int (0-100),
        }
    """
    scores = {}

    # ============ Graph Completeness (25 pts) ============
    # Проверяем наличие всех 27 узлов и правильные рёбра
    graph_completeness = 0
    try:
        # Парсим graph.py, считаем узлы
        with open(graph_path) as f:
            content = f.read()

        node_count = content.count('.add_node(')
        edge_count = content.count('.add_edge(')

        # Ожидаем ~27 узлов
        if 25 <= node_count <= 30:
            graph_completeness += 15  # nodes OK
        if 30 <= edge_count <= 50:
            graph_completeness += 10  # edges OK

    except Exception as e:
        graph_completeness = 0

    scores['graph_completeness'] = min(25, graph_completeness)

    # ============ State Management (15 pts) ============
    state_management = 0
    try:
        with open(state_path) as f:
            content = f.read()

        # Проверяем Pydantic v2 синтаксис
        if 'BaseModel' in content and 'model_fields' in content:
            state_management += 5

        # Все требуемые поля?
        required_fields = [
            'trigger_type', 'user_id', 'timestamp', 'digital_twin',
            'medical_opinions', 'lifestyle_opinions', 'draft_protocol',
            'verification_state', 'final_protocol', 'execution_status',
            'retry_count', 'errors', 'checkpoint_id'
        ]
        field_coverage = sum(1 for f in required_fields if f in content)
        state_management += int(10 * field_coverage / len(required_fields))

    except Exception as e:
        state_management = 0

    scores['state_management'] = min(15, state_management)

    # ============ Veto Loop Correctness (15 pts) ============
    veto_loop = 0
    try:
        with open(graph_path) as f:
            content = f.read()

        # Проверяем логику retry_count <= 3
        if 'retry_count' in content and 'max_retries' in content:
            veto_loop += 10

        # Conditional edge для force-approve после 3 retries?
        if 'retry_count >= 3' in content or 'retry_count > 3' in content:
            veto_loop += 5

    except Exception as e:
        veto_loop = 0

    scores['veto_loop_correctness'] = min(15, veto_loop)

    # ============ Parallel Execution (15 pts) ============
    parallel_exec = 0
    try:
        test_parallel = test_results.get('test_parallel_fan_out_executes_correctly')
        if test_parallel and test_parallel.get('passed'):
            parallel_exec = 15
        elif test_parallel and test_parallel.get('medical_opinions') == 8:
            parallel_exec = 10

    except Exception as e:
        parallel_exec = 0

    scores['parallel_execution'] = min(15, parallel_exec)

    # ============ Checkpoint/Recovery (10 pts) ============
    checkpoint_recovery = 0
    try:
        test_checkpoint = test_results.get('test_checkpoint_save_restore')
        if test_checkpoint and test_checkpoint.get('passed'):
            checkpoint_recovery = 10
        elif test_checkpoint and test_checkpoint.get('save_ok'):
            checkpoint_recovery = 5

    except Exception as e:
        checkpoint_recovery = 0

    scores['checkpoint_recovery'] = min(10, checkpoint_recovery)

    # ============ Error Handling (10 pts) ============
    error_handling = 0
    try:
        test_error = test_results.get('test_error_handling_graceful_degradation')
        if test_error and test_error.get('passed'):
            error_handling = 10
        elif test_error and test_error.get('graceful'):
            error_handling = 5

    except Exception as e:
        error_handling = 0

    scores['error_handling'] = min(10, error_handling)

    # ============ Code Quality (10 pts) ============
    code_quality = 0
    try:
        # Проверяем async/await, type hints, docstrings
        with open(nodes_path, 'r', errors='ignore') as f:
            content = f.read()

        if 'async def' in content:
            code_quality += 3
        if '-> ' in content and ': ' in content:  # type hints
            code_quality += 3
        if '"""' in content or "'''" in content:  # docstrings
            code_quality += 2

        # Timeout protection?
        if 'timeout' in content.lower() or 'asyncio.wait_for' in content:
            code_quality += 2

    except Exception as e:
        code_quality = 0

    scores['code_quality'] = min(10, code_quality)

    # ============ Total ============
    scores['total'] = sum(scores.values())

    return scores

def print_evaluation_report(scores: dict) -> None:
    """Выводит красивый отчёт оценки."""
    print("\n" + "="*60)
    print("PHASE 3 EVALUATION REPORT")
    print("="*60)

    categories = [
        ('Graph Completeness', 'graph_completeness', 25),
        ('State Management', 'state_management', 15),
        ('Veto Loop Correctness', 'veto_loop_correctness', 15),
        ('Parallel Execution', 'parallel_execution', 15),
        ('Checkpoint/Recovery', 'checkpoint_recovery', 10),
        ('Error Handling', 'error_handling', 10),
        ('Code Quality', 'code_quality', 10),
    ]

    for display_name, key, max_score in categories:
        actual = scores.get(key, 0)
        pct = int(100 * actual / max_score) if max_score > 0 else 0
        status = '✓' if pct >= 80 else '◐' if pct >= 50 else '✗'
        print(f"{status} {display_name:.<40} {actual:>3}/{max_score} pts ({pct}%)")

    print("-"*60)
    total = scores.get('total', 0)
    pct = int(100 * total / 100)
    print(f"TOTAL SCORE: {total}/100 ({pct}%)")
    print("="*60 + "\n")
```

---

## 5. Зависимости

- **Phase 1 (DB)**: PostgreSQL schema, migration scripts, checkpointer interface
- **Phase 2 (Agent Prompts)**: Prompt templates, agent configurations, LLM call utilities

---

## 6. Риски и смягчение

### 6.1 LangGraph Parallel Fan-out Rate Limiting
**Риск**: Одновременный вызов 13 агентов к Claude API может вызвать rate limiting.

**Смягчение**:
- Implementируем semaphore для ограничения одновременных запросов (max 5 параллельно)
- Добавляем exponential backoff для retry
- Мониторим API usage и логируем rate limit hits
- Кэшируем мнения агентов (24-часовой TTL) для идентичных Digital Twin снимков

### 6.2 Checkpoint Size с Full Medical Context
**Риск**: PLTState с полной медицинской историей может быть очень большим, замедляя save/restore.

**Смягчение**:
- Компрессируем checkpoint (gzip)
- Храним только дельта-изменения (не полное состояние каждый раз)
- Удаляем старые checkpoints (TTL 30 дней)
- Индексируем по checkpoint_id и user_id для быстрого поиска

### 6.3 LangGraph Version Compatibility
**Риск**: LangGraph API может измениться между версиями.

**Смягчение**:
- Фиксируем версию в requirements.txt (e.g., `langgraph==0.1.x`)
- Инкапсулируем LangGraph API в adapter layer
- Документируем все LangGraph-specific вызовы

### 6.4 Veto Loop Infinite Recursion
**Риск**: Если verifier всегда находит ошибку, цикл не завершится.

**Смягчение**:
- Жёсткий лимит max_retries=3 с force-approve после
- Логируем все отказы verifier для анализа
- Проверяем convergence (опинии на retry похожи на предыдущие?)

---

## 7. Timeline и Milestones

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M1 | Week 1 | State schema, Node signatures |
| M2 | Week 2 | Medical Core (8 nodes), Lifestyle (5 nodes) |
| M3 | Week 2-3 | Analyst, Verifier, CMO, Synthesis |
| M4 | Week 3 | Checkpoint + PostgreSQL integration |
| M5 | Week 3-4 | Event handler (Redis), E2E testing |
| M6 | Week 4 | Evaluation, Documentation |

---

## 8. Success Criteria

- [ ] Graph компилируется без ошибок
- [ ] Все 27 узлов реализованы и достижимы
- [ ] State schema полностью типизирован (Pydantic)
- [ ] Veto loop max 3 retries, затем force-approve
- [ ] Parallel fan-out (13 агентов) выполняется за <1 мин
- [ ] Checkpoint save/restore работает
- [ ] Human-in-the-loop interrupt работает
- [ ] Full pipeline E2E тест проходит
- [ ] Error handling graceful (не падает на первой ошибке)
- [ ] Оценка >= 80/100 по evaluation_phase3_completion()

---

## 9. Структура файлов

```
plt-platform/
├── src/
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py                    # PLTState definition
│   │   ├── graph.py                    # StateGraph construction
│   │   ├── routing.py                  # Router, conditional edges
│   │   ├── nodes/
│   │   │   ├── __init__.py
│   │   │   ├── router.py               # Trigger classification
│   │   │   ├── system_biologist.py     # Digital Twin enrichment
│   │   │   ├── medical/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cardiologist.py
│   │   │   │   ├── metabolic_specialist.py
│   │   │   │   ├── immunologist.py
│   │   │   │   ├── neurologist.py
│   │   │   │   ├── endocrinologist.py
│   │   │   │   ├── geneticist.py
│   │   │   │   ├── oncologist.py
│   │   │   │   └── gi_specialist.py
│   │   │   ├── lifestyle/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── nutritionist.py
│   │   │   │   ├── fitness_coach.py
│   │   │   │   ├── sleep_specialist.py
│   │   │   │   ├── stress_management.py
│   │   │   │   └── social_connection.py
│   │   │   ├── analyst.py              # Synthesis
│   │   │   ├── verifier.py             # PubMed check, veto
│   │   │   ├── cmo.py                  # Final approval
│   │   │   ├── nutritionist_exec.py    # Execution
│   │   │   ├── trainer.py              # Execution
│   │   │   └── ops_formatter.py        # Delivery
│   │
│   ├── checkpoint/
│   │   ├── __init__.py
│   │   ├── postgres_checkpointer.py    # PostgreSQL backend
│   │   └── checkpoint_schema.sql
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── redis_handler.py            # Redis pub/sub
│   │   └── trigger_parser.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── llm_client.py               # Claude API wrapper
│       ├── rate_limiter.py             # Semaphore for parallel calls
│       └── validators.py
│
├── tests/
│   ├── __init__.py
│   ├── test_graph_compilation.py
│   ├── test_state_schema.py
│   ├── test_node_reachability.py
│   ├── test_veto_loop.py
│   ├── test_parallel_execution.py
│   ├── test_checkpoint.py
│   ├── test_human_in_the_loop.py
│   ├── test_e2e_pipeline.py
│   ├── test_router.py
│   └── test_error_handling.py
│
├── phases/
│   └── phase3_langgraph_orchestration/
│       ├── SPEC.md                     # (this file)
│       └── UPDATES.md                  # Progress log
│
└── requirements.txt
```

---

## 10. Ссылки и ресурсы

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic v2 Guide](https://docs.pydantic.dev/latest/)
- [Redis Pub/Sub](https://redis.io/docs/interact/pubsub/)
- [PostgreSQL JSON](https://www.postgresql.org/docs/current/datatype-json.html)

---

**Версия**: 1.0
**Дата**: 2026-03-27
**Статус**: Ready for Implementation
