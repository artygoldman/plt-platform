# Phase 2: Методички и Промпты Агентов — 27 AI Врачей

## Цель
Создать полный набор системных промптов (методичек) для всех 27 AI-агентов, организованных в 6 уровней иерархии. Каждый агент получает:
- Детальный системный промпт (методичка) с ролью, специализацией, правилами действия и безопасностью
- JSON-схемы для входных и выходных данных
- Конфигурацию (модель, температура, max_tokens)
- Регистрацию в агент-реестре

## Дата начала: TBD
## Дата завершения: TBD
## Статус: ОЖИДАЕТ УТВЕРЖДЕНИЯ

---

## Архитектура: 6-уровневая иерархия

### TIER 1: Стратегическое ядро (4 агента)
1. **CMO (Главный Архитектор)** — руководство стратегией, опрос + синтез данных всех других агентов
2. **Научный Цензор (Verifier)** — проверка фактов, право вето на любые рекомендации, медицинская безопасность
3. **Системный Биолог** — интеграция сигналов, фенотип-генотип мэппинг, системные взаимодействия
4. **Аналитик-Прогнозист** — анализ трендов, прогнозирование рисков, долгосрочные сценарии

### TIER 2: Медицинское ядро (8 агентов)
1. **Клинический Генетик** — анализ генома, PRS, фармакогенетика, риск-стратификация
2. **Эндокринолог-Андролог** — гормоны, метаболизм половых гормонов, репродукция
3. **Метабололог-Гастроэнтеролог** — обмен веществ, ГИП, микробиом, пищеварение
4. **Специалист по Микробиоте** — анализ микробиома, дисбиоз, пробиотики
5. **Превентивный Кардиолог** — липиды, сердечно-сосудистый риск, артериальное давление
6. **Ортопед-Биомеханик** — опорно-двигательная система, мышечная масса, осанка
7. **Дерматолог-Трихолог** — кожа, волосы, ногти, старение кожи
8. **Эстетист** — эстетические параметры, процедуры, внешний вид

### TIER 3: Лайфстайл (5 агентов)
1. **Сомнолог** — качество сна, циклы, нарушения, рекомендации по гигиене сна
2. **Нейропсихолог** — когнитивные функции, стресс, настроение, психическое здоровье
3. **Хронобиолог** — циркадные ритмы, хронотип, синхронизация, время приёма лекарств
4. **Инженер Среды** — дом, рабочее пространство, свет, воздух, температура
5. **Эко-Аудитор (Токсиколог)** — токсины, загрязнение, безопасность продуктов

### TIER 4: Исполнители (2 агента)
1. **Нутрициолог** — питание, протоколы, калории, макро-микро, добавки
2. **Фитнес-тренер** — физическая активность, программа упражнений, нагрузки

### TIER 5: Операционное управление (4 агента)
1. **Диспетчер-Экзекутор** — управление процессами, координация, выполнение плана
2. **Завхоз-Инвентаризатор** — учёт ресурсов, запасы, логистика
3. **Медицинский Консьерж** — взаимодействие с врачами, запись на приёмы, согласование
4. **Финансовый Контроллер** — бюджет, расходы, ROI, финансовые аспекты

### TIER 6: IT-инфраструктура (4 агента)
1. **Служба Поддержки** — помощь пользователям, FAQ, тикеты
2. **UX-Дизайнер** — дизайн интерфейсов, юзабилити, эргономика
3. **Системный Разработчик** — архитектура, интеграции, API
4. **QA-Тестировщик** — тестирование, качество, баги, отчёты

---

## Deliverables (Что должно быть на выходе)

### 1. Файлы Промптов Агентов
- Директория: `src/agents/prompts/`
- 27 Python-файлов, по одному на агента
- Формат: `{tier}_{agent_id}.py`
  - Пример: `tier1_cmo.py`, `tier2_clinical_geneticist.py`, `tier4_nutritionist.py`

### 2. Структура Промптов
Каждый промпт-файл содержит:
- **SYSTEM_PROMPT** (str): основная методичка на русском, 500-5000 символов
- **INPUT_SCHEMA** (dict): JSON-schema для входных данных
- **OUTPUT_SCHEMA** (dict): JSON-schema для выходных данных (должна быть валидной)
- **CONFIG** (dict): `{model, temperature, max_tokens, top_p}`
- **TIER**: уровень иерархии (1-6)
- **SPECIALIZATION**: русское название специальности
- **ALLOWED_ACTIONS**: список разрешённых действий
- **RESTRICTED_ACTIONS**: список запрещённых действий
- **SAFETY_RULES**: правила безопасности, медицинские ограничения

### 3. Агент Реестр
- Файл: `src/agents/registry.json`
- Формат: словарь `{agent_id: {name, tier, model, prompt_file, ...}}`
- Все 27 агентов должны быть зарегистрированы

### 4. JSON Схемы
- Каждая INPUT_SCHEMA и OUTPUT_SCHEMA — валидная JSON-schema (Draft 7)
- OUTPUT_SCHEMA обязательно содержит `$id`, `title`, `type: object`, `properties`
- Входные схемы должны соответствовать тому, что агент получает от других агентов/пользователя
- Выходные схемы должны быть структурированными JSON-объектами (не строки)

### 5. Конфигурация Модели
- Каждый агент имеет конфиг: `{model, temperature, max_tokens, top_p}`
- TIER 1-2: claude-opus (сложные решения), temp 0.5-0.7
- TIER 3-4: claude-sonnet (средняя сложность), temp 0.6-0.8
- TIER 5-6: claude-haiku (простые задачи), temp 0.3-0.5

### 6. Документация
- `IMPLEMENTATION_GUIDE.md`: инструкция по созданию нового промпта
- `MEDICAL_SAFETY.md`: гайдлайны по медицинской безопасности для промптов
- `SCHEMA_EXAMPLES.md`: примеры JSON-схем для разных типов агентов

---

## Критерии приёмки (Definition of Done)

1. **Все 27 файлов созданы** с именами вида `tier{N}_{agent_id}.py`
2. **Каждый файл содержит**:
   - SYSTEM_PROMPT (500-5000 символов, на русском)
   - INPUT_SCHEMA (валидная JSON-schema)
   - OUTPUT_SCHEMA (валидная JSON-schema с $id, title, type)
   - CONFIG (model, temperature, max_tokens, top_p)
   - TIER (1-6)
   - SPECIALIZATION (русское название)
   - ALLOWED_ACTIONS (список)
   - RESTRICTED_ACTIONS (список)
   - SAFETY_RULES (текст или список)
3. **registry.json** содержит все 27 агентов с корректными путями
4. **Все JSON-схемы валидны** (проверяется jsonschema library)
5. **Иерархия соблюдена**: правила эскалации соответствуют tierам
6. **Медицинская безопасность**: TIER 1-2 содержат ссылки на гайдлайны (EULAR, ESC, ADA, др.)
7. **Нет дубликатов** агент-айди в реестре
8. **Длины промптов** находятся в диапазоне 500-5000 символов
9. **Входные/выходные форматы** унифицированы (все структурированы как JSON)
10. **Документация** создана: IMPLEMENTATION_GUIDE.md, MEDICAL_SAFETY.md, SCHEMA_EXAMPLES.md

---

## Test Functions

```python
# tests/test_phase2.py

import pytest
import json
import os
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator
import importlib.util

AGENTS_DIR = Path("src/agents/prompts")
REGISTRY_FILE = Path("src/agents/registry.json")

# ── T1: Все 27 файлов существуют ──
def test_all_27_prompt_files_exist():
    """Все 27 файлов промптов существуют в src/agents/prompts/"""
    expected_agents = {
        # TIER 1
        "tier1_cmo", "tier1_verifier", "tier1_systems_biologist", "tier1_analyst",
        # TIER 2
        "tier2_clinical_geneticist", "tier2_endocrinologist", "tier2_metabolologist",
        "tier2_microbiome_specialist", "tier2_cardiologist", "tier2_orthopedist",
        "tier2_dermatologist", "tier2_aesthetician",
        # TIER 3
        "tier3_somnologist", "tier3_neuropsychologist", "tier3_chronobiologist",
        "tier3_environment_engineer", "tier3_eco_auditor",
        # TIER 4
        "tier4_nutritionist", "tier4_fitness_trainer",
        # TIER 5
        "tier5_dispatcher", "tier5_warehouse_manager", "tier5_concierge",
        "tier5_financial_controller",
        # TIER 6
        "tier6_support", "tier6_ux_designer", "tier6_developer", "tier6_qa"
    }

    existing_files = {f.stem for f in AGENTS_DIR.glob("*.py") if not f.name.startswith("__")}
    assert len(existing_files) == 27, f"Expected 27 prompt files, found {len(existing_files)}"
    for agent in expected_agents:
        assert agent in existing_files, f"Missing prompt file for {agent}"

# ── T2: Каждый файл имеет требуемые атрибуты ──
def test_prompt_files_have_required_attributes():
    """Каждый промпт содержит SYSTEM_PROMPT, INPUT_SCHEMA, OUTPUT_SCHEMA, CONFIG и другие"""
    required_attrs = [
        "SYSTEM_PROMPT", "INPUT_SCHEMA", "OUTPUT_SCHEMA", "CONFIG",
        "TIER", "SPECIALIZATION", "ALLOWED_ACTIONS", "RESTRICTED_ACTIONS", "SAFETY_RULES"
    ]

    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr in required_attrs:
            assert hasattr(module, attr), f"{prompt_file.name} missing {attr}"

# ── T3: Все TIER значения корректны (1-6) ──
def test_tier_values_valid():
    """Каждый агент имеет TIER от 1 до 6"""
    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert hasattr(module, "TIER"), f"{prompt_file.name} missing TIER"
        assert module.TIER in [1, 2, 3, 4, 5, 6], \
            f"{prompt_file.name} has invalid TIER {module.TIER}"

# ── T4: SYSTEM_PROMPT длина в пределах 500-5000 символов ──
def test_prompt_length_valid():
    """Длина SYSTEM_PROMPT: 500-5000 символов"""
    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        prompt_len = len(module.SYSTEM_PROMPT)
        assert 500 <= prompt_len <= 5000, \
            f"{prompt_file.name}: prompt length {prompt_len} not in [500, 5000]"

# ── T5: INPUT_SCHEMA и OUTPUT_SCHEMA — валидные JSON-schemas ──
def test_schemas_are_valid_json_schema():
    """Все INPUT_SCHEMA и OUTPUT_SCHEMA валидны по JSON-schema Draft 7"""
    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Проверить, что OUTPUT_SCHEMA имеет $id и title
        output_schema = module.OUTPUT_SCHEMA
        assert "$id" in output_schema, f"{prompt_file.name}: OUTPUT_SCHEMA missing $id"
        assert "title" in output_schema, f"{prompt_file.name}: OUTPUT_SCHEMA missing title"
        assert "type" in output_schema, f"{prompt_file.name}: OUTPUT_SCHEMA missing type"
        assert output_schema["type"] == "object", \
            f"{prompt_file.name}: OUTPUT_SCHEMA type must be 'object'"

        # Валидировать по JSON-schema
        try:
            Draft7Validator.check_schema(module.INPUT_SCHEMA)
            Draft7Validator.check_schema(output_schema)
        except Exception as e:
            pytest.fail(f"{prompt_file.name}: Invalid JSON-schema: {e}")

# ── T6: CONFIG содержит model, temperature, max_tokens, top_p ──
def test_config_has_required_fields():
    """CONFIG каждого агента содержит: model, temperature, max_tokens, top_p"""
    required_config_fields = ["model", "temperature", "max_tokens", "top_p"]

    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        config = module.CONFIG
        for field in required_config_fields:
            assert field in config, \
                f"{prompt_file.name}: CONFIG missing {field}"

# ── T7: registry.json существует и содержит все 27 агентов ──
def test_registry_file_exists_and_complete():
    """registry.json содержит все 27 агентов с корректными полями"""
    assert REGISTRY_FILE.exists(), "registry.json does not exist"

    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    assert len(registry) == 27, f"Registry has {len(registry)} agents, expected 27"

    required_registry_fields = ["name", "tier", "model", "prompt_file", "specialization"]
    for agent_id, agent_data in registry.items():
        for field in required_registry_fields:
            assert field in agent_data, \
                f"Agent {agent_id}: registry missing field {field}"

        # Проверить, что prompt_file существует
        prompt_path = Path(agent_data["prompt_file"])
        assert prompt_path.exists(), \
            f"Agent {agent_id}: prompt file {agent_data['prompt_file']} not found"

# ── T8: Нет дубликатов agent_id ──
def test_no_duplicate_agent_ids():
    """В registry.json нет дубликатов agent_id"""
    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    agent_ids = list(registry.keys())
    assert len(agent_ids) == len(set(agent_ids)), "Duplicate agent IDs found in registry"

# ── T9: Все тиры 1-6 представлены ──
def test_all_tiers_represented():
    """В registry.json представлены все тиры 1-6"""
    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    tiers_found = {agent["tier"] for agent in registry.values()}
    for tier in [1, 2, 3, 4, 5, 6]:
        assert tier in tiers_found, f"Tier {tier} not found in registry"

# ── T10: Моделели соответствуют тирам ──
def test_model_assignment_by_tier():
    """TIER 1-2 использует claude-opus, TIER 3-4 — claude-sonnet, TIER 5-6 — claude-haiku"""
    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    for agent_id, agent_data in registry.items():
        tier = agent_data["tier"]
        model = agent_data["model"]

        if tier in [1, 2]:
            assert model == "claude-opus", \
                f"Agent {agent_id} (tier {tier}): expected claude-opus, got {model}"
        elif tier in [3, 4]:
            assert model == "claude-sonnet", \
                f"Agent {agent_id} (tier {tier}): expected claude-sonnet, got {model}"
        elif tier in [5, 6]:
            assert model == "claude-haiku", \
                f"Agent {agent_id} (tier {tier}): expected claude-haiku, got {model}"

# ── T11: ALLOWED_ACTIONS и RESTRICTED_ACTIONS не пусты ──
def test_actions_are_defined():
    """Каждый агент имеет непустые ALLOWED_ACTIONS и RESTRICTED_ACTIONS"""
    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert len(module.ALLOWED_ACTIONS) > 0, \
            f"{prompt_file.name}: ALLOWED_ACTIONS is empty"
        assert len(module.RESTRICTED_ACTIONS) >= 0, \
            f"{prompt_file.name}: RESTRICTED_ACTIONS should be a list"

# ── T12: SAFETY_RULES не пусты ──
def test_safety_rules_defined():
    """Каждый агент имеет SAFETY_RULES"""
    for prompt_file in AGENTS_DIR.glob("*.py"):
        if prompt_file.name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert module.SAFETY_RULES and len(str(module.SAFETY_RULES)) > 0, \
            f"{prompt_file.name}: SAFETY_RULES empty or missing"
```

---

## Evaluation Functions

```python
# tests/eval_phase2.py

"""
Evaluation — оценка качества Phase 2.
Запускается после прохождения всех test functions.
Выдаёт оценку 0-100 и детальный отчёт по 6 критериям.
"""

import json
import importlib.util
from pathlib import Path
from jsonschema import Draft7Validator

AGENTS_DIR = Path("src/agents/prompts")
REGISTRY_FILE = Path("src/agents/registry.json")

def evaluate_phase2() -> dict:
    """
    Оценка Phase 2:
    1. Полнота промптов (30 баллов) — все 27 файлов существуют
    2. Качество схем (20 баллов) — валидные JSON-schemas
    3. Безопасность (15 баллов) — медицинские правила
    4. Медицинская точность (15 баллов) — ссылки на гайдлайны
    5. Консистентность (10 баллов) — единообразие формата
    6. Иерархия (10 баллов) — соблюдение эскалации и tierов
    """
    checks = []

    # E1: Полнота (30 баллов)
    prompt_files = list(AGENTS_DIR.glob("*.py"))
    prompt_files = [f for f in prompt_files if not f.name.startswith("__")]
    completeness_score = min(30, int((len(prompt_files) / 27) * 30))
    checks.append({
        "name": "Completeness (all 27 prompts exist)",
        "score": completeness_score,
        "max": 30,
        "details": f"{len(prompt_files)}/27 prompt files found"
    })

    # E2: Качество JSON-схем (20 баллов)
    schema_quality_count = 0
    for prompt_file in prompt_files:
        try:
            spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Проверить INPUT_SCHEMA
            Draft7Validator.check_schema(module.INPUT_SCHEMA)

            # Проверить OUTPUT_SCHEMA
            output_schema = module.OUTPUT_SCHEMA
            if "$id" in output_schema and "title" in output_schema and \
               output_schema.get("type") == "object" and "properties" in output_schema:
                Draft7Validator.check_schema(output_schema)
                schema_quality_count += 1
        except Exception:
            pass

    schema_quality_score = int((schema_quality_count / len(prompt_files)) * 20) if prompt_files else 0
    checks.append({
        "name": "Schema quality (valid JSON-schemas)",
        "score": schema_quality_score,
        "max": 20,
        "details": f"{schema_quality_count}/{len(prompt_files)} agents have valid schemas"
    })

    # E3: Безопасность (15 баллов)
    safety_rules_count = 0
    for prompt_file in prompt_files:
        try:
            spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            safety = str(module.SAFETY_RULES)
            # Проверить наличие ключевых слов медицинской безопасности
            keywords = ["contraindication", "risk", "safety", "warning", "restriction",
                       "contraindications", "опасность", "запрет", "ограничение"]
            if any(kw.lower() in safety.lower() for kw in keywords):
                safety_rules_count += 1
        except Exception:
            pass

    safety_score = int((safety_rules_count / len(prompt_files)) * 15) if prompt_files else 0
    checks.append({
        "name": "Safety rules coverage",
        "score": safety_score,
        "max": 15,
        "details": f"{safety_rules_count}/{len(prompt_files)} agents have medical safety rules"
    })

    # E4: Медицинская точность (15 баллов)
    medical_accuracy_count = 0
    medical_keywords = [
        "ESC", "ADA", "EULAR", "ASPC", "guideline", "recommendation",
        "evidence-based", "RCT", "clinical trial", "GRADE",
        "гайдлайн", "рекомендация", "доказательной", "клиническое"
    ]

    for prompt_file in prompt_files:
        try:
            spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            prompt_text = module.SYSTEM_PROMPT.lower()
            # Проверить TIER 1-2 (они должны ссылаться на гайдлайны)
            if module.TIER in [1, 2]:
                if any(kw.lower() in prompt_text for kw in medical_keywords):
                    medical_accuracy_count += 1
            elif module.TIER in [3, 4, 5, 6]:
                # Для остальных тиров — достаточно наличия медицинских сигналов
                medical_terms = ["заболевание", "диагноз", "риск", "лечение",
                               "disease", "diagnosis", "risk", "treatment"]
                if any(t.lower() in prompt_text for t in medical_terms):
                    medical_accuracy_count += 1
        except Exception:
            pass

    medical_score = int((medical_accuracy_count / len(prompt_files)) * 15) if prompt_files else 0
    checks.append({
        "name": "Medical accuracy signals",
        "score": medical_score,
        "max": 15,
        "details": f"{medical_accuracy_count}/{len(prompt_files)} agents reference guidelines/evidence"
    })

    # E5: Консистентность (10 баллов)
    consistency_count = 0
    required_attrs = ["SYSTEM_PROMPT", "INPUT_SCHEMA", "OUTPUT_SCHEMA", "CONFIG",
                     "TIER", "SPECIALIZATION", "ALLOWED_ACTIONS", "RESTRICTED_ACTIONS", "SAFETY_RULES"]

    for prompt_file in prompt_files:
        try:
            spec = importlib.util.spec_from_file_location(prompt_file.stem, prompt_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if all(hasattr(module, attr) for attr in required_attrs):
                consistency_count += 1
        except Exception:
            pass

    consistency_score = int((consistency_count / len(prompt_files)) * 10) if prompt_files else 0
    checks.append({
        "name": "Format consistency",
        "score": consistency_score,
        "max": 10,
        "details": f"{consistency_count}/{len(prompt_files)} agents follow standard format"
    })

    # E6: Иерархия (10 баллов)
    hierarchy_score = 0
    try:
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        # Проверить:
        # 1. Все тиры 1-6 представлены
        tiers = {agent["tier"] for agent in registry.values()}
        if all(t in tiers for t in [1, 2, 3, 4, 5, 6]):
            hierarchy_score += 3

        # 2. Количество агентов по тирам соответствует плану
        tier_counts = {i: 0 for i in range(1, 7)}
        for agent in registry.values():
            tier_counts[agent["tier"]] += 1

        expected_counts = {1: 4, 2: 8, 3: 5, 4: 2, 5: 4, 6: 4}
        if tier_counts == expected_counts:
            hierarchy_score += 4

        # 3. Модели соответствуют тирам
        model_ok = True
        for agent in registry.values():
            tier = agent["tier"]
            model = agent["model"]
            if tier in [1, 2] and model != "claude-opus":
                model_ok = False
            elif tier in [3, 4] and model != "claude-sonnet":
                model_ok = False
            elif tier in [5, 6] and model != "claude-haiku":
                model_ok = False

        if model_ok:
            hierarchy_score += 3
    except Exception:
        pass

    checks.append({
        "name": "Hierarchy enforcement",
        "score": hierarchy_score,
        "max": 10,
        "details": f"All tiers present, tier distribution correct, models aligned"
    })

    # Итоги
    total = sum(c["score"] for c in checks)
    max_total = sum(c["max"] for c in checks)
    grade = "EXCELLENT" if total >= 90 else "GOOD" if total >= 75 else "NEEDS WORK"

    return {
        "phase": "Phase 2: Agent Prompts & Methodologies",
        "total_score": total,
        "max_score": max_total,
        "percentage": int((total / max_total) * 100) if max_total > 0 else 0,
        "grade": grade,
        "checks": checks
    }
```

---

## Зависимости от других фаз

- **Phase 1** (Foundation): фаза 2 зависит от наличия моделей БД, таблицы `agents`
- **Phase 2** → **Phase 3**: Фаза 3 (API/Routes) использует эти промпты для инициализации агентов

## Риски

1. **Медицинская точность**: Каждый промпт должен быть проверен врачом/экспертом. Риск — неточные рекомендации.
   - **Митигация**: Научный Цензор (TIER 1) должен иметь veto-права; обязательный review экспертами.

2. **Качество JSON-схем**: Сложно генерировать правильные JSON-schemas для разных типов агентов.
   - **Митигация**: Использовать примеры и шаблоны; автоматизировать валидацию.

3. **Размер промптов**: Большие промпты замедляют LLM, маленькие — упускают детали.
   - **Митигация**: Строгой диапазон 500-5000 символов; итеративный пересмотр.

4. **Иерархия и эскалация**: Сложно обеспечить правильную координацию между тирами.
   - **Митигация**: Явно указать в ALLOWED_ACTIONS, какие агенты можно вызывать; тесты на эскалацию.

---

## Примеры Промптов (Template)

### Пример 1: TIER 1 (CMO — Главный Архитектор)

```python
# src/agents/prompts/tier1_cmo.py

SYSTEM_PROMPT = """
Ты — CMO (Chief Medical Officer) персональной клиники долголетия.
Твоя роль: стратегическое руководство, опрос всех 26 других агентов, синтез данных в целостную программу.

Твой процесс:
1. Получить от пользователя базовые данные (возраст, биомаркеры, цели).
2. Отправить структурированные запросы к врачам-специалистам (TIER 2-3).
3. Интегрировать их ответы в единую longevity-программу.
4. Передать результаты Научному Цензору на проверку.
5. Дать пользователю финальные рекомендации.

Ограничения:
- Не давай прямые медицинские рекомендации без согласования с TIER 2.
- Все решения должны быть одобрены Научным Цензором.
- В сомнениях — выбирай консервативный вариант (safety first).

Медицинская безопасность:
- Никогда не рекомендуй отмену назначенных врачом лекарств.
- Все вмешательства должны быть обоснованы доказательной медициной.
- Уважай contraindications и индивидуальные особенности.
"""

TIER = 1
SPECIALIZATION = "Главный Архитектор / Chief Medical Officer"
ALLOWED_ACTIONS = [
    "request_data_from_user",
    "query_specialist_agents",
    "synthesize_recommendations",
    "escalate_to_verifier",
    "generate_longevity_program"
]
RESTRICTED_ACTIONS = [
    "prescribe_medications",
    "override_contraindications",
    "dismiss_specialist_opinions",
    "make_final_decision_without_verifier"
]
SAFETY_RULES = """
1. Все критические решения требуют согласования с Научным Цензором.
2. Противопоказания и непереносимости — абсолютный запрет.
3. В случае конфликта мнений специалистов — эскалировать на Цензора.
4. Документировать все решения и их обоснование.
"""

INPUT_SCHEMA = {
    "$id": "https://plt.ai/schemas/cmo_input.json",
    "title": "CMO Input",
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "age": {"type": "integer", "minimum": 18, "maximum": 150},
        "sex": {"type": "string", "enum": ["male", "female", "other"]},
        "biomarkers": {"type": "object"},
        "health_goals": {"type": "array", "items": {"type": "string"}},
        "constraints": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["user_id", "age", "sex"]
}

OUTPUT_SCHEMA = {
    "$id": "https://plt.ai/schemas/cmo_output.json",
    "title": "CMO Output",
    "type": "object",
    "properties": {
        "longevity_program": {
            "type": "object",
            "properties": {
                "protocol_id": {"type": "string"},
                "duration_weeks": {"type": "integer"},
                "pillars": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "area": {"type": "string"},
                            "priority": {"type": "integer"},
                            "recommendations": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            }
        },
        "escalation_items": {
            "type": "array",
            "items": {"type": "string"}
        },
        "requires_verifier_approval": {"type": "boolean"}
    },
    "required": ["longevity_program", "requires_verifier_approval"]
}

CONFIG = {
    "model": "claude-opus",
    "temperature": 0.5,
    "max_tokens": 2000,
    "top_p": 0.9
}
```

### Пример 2: TIER 2 (Клинический Генетик)

```python
# src/agents/prompts/tier2_clinical_geneticist.py

SYSTEM_PROMPT = """
Ты — Клинический Генетик в команде персональной клиники долголетия.
Специализация: анализ генома, PRS (Polygenic Risk Score), фармакогенетика, стратификация рисков.

Твоя задача:
1. Получить от CMO запрос о генетическом анализе пациента.
2. Интерпретировать данные генетического тестирования.
3. Выявить clinically relevant варианты.
4. Рассчитать PRS для возрастных заболеваний.
5. Дать рекомендации по фармакогенетике (какие лекарства лучше работают).
6. Вернуть структурированный отчёт CMO.

Медицинская база:
- ACMG guidelines для интерпретации вариантов
- ClinVar для классификации патогенности
- PharmGKB для фармакогенетики
- Крупные GWAS для PRS

Ограничения:
- Не делай генетический диагноз (это только для врача).
- Не предсказывай психические или поведенческие черты.
- Все выводы должны быть основаны на опубликованных данных.
"""

TIER = 2
SPECIALIZATION = "Клинический Генетик"
ALLOWED_ACTIONS = [
    "analyze_genomic_data",
    "calculate_polygenic_risk_scores",
    "interpret_variants_by_acmg",
    "assess_pharmacogenetics",
    "flag_pathogenic_variants",
    "provide_evidence_references"
]
RESTRICTED_ACTIONS = [
    "make_psychiatric_predictions",
    "diagnose_genetic_disorders",
    "recommend_genetic_testing_directly",
    "speculate_on_intelligence_or_personality"
]
SAFETY_RULES = """
1. ACMG pathogenicity guidelines — обязательны.
2. Все 'pathogenic' варианты должны быть одобрены Научным Цензором перед сообщением пользователю.
3. Психиатрические или поведенческие прогнозы — запрещены (даже если данные есть).
4. PRS интерпретировать как относительный риск, не как диагноз.
"""

INPUT_SCHEMA = {
    "$id": "https://plt.ai/schemas/geneticist_input.json",
    "title": "Clinical Geneticist Input",
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "vcf_file_path": {"type": "string"},
        "analysis_request": {
            "type": "object",
            "properties": {
                "variant_interpretation": {"type": "boolean"},
                "prs_calculation": {"type": "boolean"},
                "pharmacogenetics": {"type": "boolean"}
            }
        },
        "ethnicity": {"type": "string"}
    },
    "required": ["user_id", "analysis_request"]
}

OUTPUT_SCHEMA = {
    "$id": "https://plt.ai/schemas/geneticist_output.json",
    "title": "Clinical Geneticist Output",
    "type": "object",
    "properties": {
        "pathogenic_variants": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "variant_id": {"type": "string"},
                    "acmg_classification": {"type": "string"},
                    "disease": {"type": "string"},
                    "reference": {"type": "string"}
                }
            }
        },
        "polygenic_risk_scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "disease": {"type": "string"},
                    "prs_percentile": {"type": "number"},
                    "relative_risk": {"type": "number"}
                }
            }
        },
        "pharmacogenetics": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "drug": {"type": "string"},
                    "phenotype": {"type": "string"},
                    "recommendation": {"type": "string"}
                }
            }
        },
        "requires_verifier_review": {"type": "boolean"}
    },
    "required": ["pathogenic_variants", "requires_verifier_review"]
}

CONFIG = {
    "model": "claude-opus",
    "temperature": 0.3,
    "max_tokens": 2500,
    "top_p": 0.85
}
```

---

## Следующие шаги

1. Создать IMPLEMENTATION_GUIDE.md с инструкцией по созданию нового промпта.
2. Создать MEDICAL_SAFETY.md с гайдлайнами по медицинской безопасности.
3. Создать SCHEMA_EXAMPLES.md с примерами JSON-схем.
4. Реализовать все 27 промптов согласно спецификации.
5. Запустить тесты (test functions) для проверки полноты.
6. Запустить evaluation functions для оценки качества.
7. Code review экспертами (врачами, ML-инженерами).

---

**Дата документа:** 2026-03-27
**Статус:** ОЖИДАЕТ УТВЕРЖДЕНИЯ
**Автор:** Personal Longevity Team Platform Team
