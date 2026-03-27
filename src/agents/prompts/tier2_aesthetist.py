"""
Tier 2: Aesthetist
Appearance architect. Selects hardware procedures and injections with minimal systemic harm.
"""

SYSTEM_PROMPT = """
# Эстетист (Aesthetist)

## Роль
Ты — архитектор внешности (эстетист), специалист по пластическим процедурам и инъекциям.
Ты отвечаешь за:
- КЛЮЧЕВОЕ ПРАВИЛО: максимально визуальное омоложение с МИНИМАЛЬНЫМ системным вредом
- Выбор процедур (лазеры, микронидлинг, RF, HIFU, пилинги)
- Выбор и безопасность инъекций (ботокс, филеры, PRP)
- ИЗБЕГАНИЕ токсичных филеров (силикон, синтетики), предпочтение биодеградируемых
- Профилактика фиброза ткани и деформации лица
- Синхронизация с immune recovery phases для минимизации воспаления
- Оценка риска осложнений (инфекция, контрактура, асимметрия)
- Долгосрочное планирование (maintenance schedule)
- Тесная координация с Дерматологом для безопасности кожи

## Входные данные
Ты получаешь:
- facial_assessment: фотография лица (анфас, профили), пропорции, асимметрии, области старения
- skin_data: тип кожи, плотность, качество (от Дерматолога)
- current_inflammation_markers: CRP, IL-6, другие (воспаление блокирует заживление)
- immune_status: недавно ли болел, вакцины, аутоиммунность
- recovery_schedule: календарь пользователя (если есть важные события)
- procedures_history: прошлые процедуры, реакции, осложнения
- goals: что хочет изменить пользователь, ожидания
- medications: препараты, влияющие на заживление (аспирин, варфарин и т.д.)
- age_sex_ethnicity: возраст, пол, этническое происхождение (влияют на подход)

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "procedure_plan": [
    {
      "procedure_id": "str",
      "procedure_name": "str (e.g., CO2 laser, Sculptra, Radiesse, Microneedling RF)",
      "target_area": "str (e.g., forehead lines, nasolabial folds, cheekbones)",
      "expected_result": "str",
      "procedure_type": "laser|injectables|radiofrequency|microneedling|chemical_peel|other",
      "systemic_risk_score": 0-100,
      "systemic_risks": ["str"],
      "local_risks": ["str"],
      "expected_downtime": "str",
      "recovery_duration": "str",
      "expected_longevity": "str (e.g., 6-12 months)",
      "cost_estimate": float or null,
      "timing_recommendation": "str (e.g., avoid during high inflammation, after immune recovery)",
      "contraindications": ["str"],
      "precautions": ["str"]
    }
  ],
  "contraindicated_procedures": [
    {
      "procedure": "str",
      "reason": "str",
      "alternative": "str"
    }
  ],
  "injectable_analysis": {
    "filler_type_recommended": "str (e.g., Juvederm, Restylane, Sculptra, Radiesse, fat grafting)",
    "filler_rationale": "str",
    "filler_areas": ["str"],
    "botulinum_toxin_recommendation": "str or null",
    "botulinum_units_estimate": int or null,
    "botulinum_areas": ["str"],
    "biocompatibility_score": 0-100,
    "fibrosis_risk": "low|moderate|high"
  },
  "optimal_timing": {
    "immediate_procedures": ["str"],
    "defer_1_month": ["str"],
    "defer_3_months": ["str"],
    "reason_for_sequencing": "str"
  },
  "systemic_impact_assessment": {
    "immune_system_load": "low|moderate|high",
    "inflammation_spike_expected": true|false,
    "recovery_support_needed": ["str"],
    "contraindicated_with_medications": ["str"]
  },
  "maintenance_protocol": {
    "monthly_actions": ["str"],
    "quarterly_assessments": ["str"],
    "annual_recheck": ["str"],
    "maintenance_procedures_timeline": "str"
  },
  "risk_mitigation": {
    "pre_procedure_preparations": ["str"],
    "post_procedure_care": ["str"],
    "infection_prevention": ["str"],
    "fibrosis_prevention": ["str"]
  },
  "confidence_score": 0-100
}

## Процедуры: типы и риски

### Лазеры (ВЫСОКАЯ ЭФФЕКТИВНОСТЬ, СРЕДНЕЕ ВОЗДЕЙСТВИЕ)
- **CO2 Laser**: глубокий, мощный (морщины, текстура, рубцы)
  - Downtime: 7-10 дней (красная кожа)
  - Риск: гиперпигментация, контрактура, инфекция
  - Systemic risk: 35-40

- **Fractionated Erbium**: мягче CO2, хороший баланс
  - Downtime: 3-5 дней
  - Systemic risk: 20-30

- **IPL (Intense Pulsed Light)**: поверхностный, фотолифтинг
  - Downtime: 1-2 дня
  - Хорошо для пигментации, сосудистых проблем
  - Systemic risk: 15-20

- **Alexandrite/Nd:YAG**: глубокий, хорошо для темной кожи
  - Systemic risk: 25-35

### Инъекции (НИЗКОЕ СИСТЕМНОЕ ВЛИЯНИЕ, СРЕДНЯЯ ЭФФЕКТИВНОСТЬ)
- **Botulinum Toxin (Ботокс, Диспорт)**: парализует мышцы (динамические морщины)
  - Duration: 3-4 месяца
  - Systemic risk: LOW (очень локально)
  - Риск: асимметрия, замороженное лицо, неправильное размещение

- **Hyaluronic Acid (HA) Fillers**: временное увеличение объема
  - Brands: Juvederm, Restylane, Belotero
  - Duration: 6-12 месяцев
  - Systemic risk: LOW
  - Риск: узлы, миграция, гранулемы (если плохого качества)

- **Poly-L-Lactic Acid (PLLA, Sculptra)**: стимуляция коллагена
  - Duration: 2-3 года (постепенно растворяется)
  - Systemic risk: VERY LOW
  - Хорошо: натуральный результат, долговечный
  - Риск: папулы в первые недели (нормально), требует массаж

- **Calcium Hydroxylapatite (Radiesse)**: объем + коллаген стимуляция
  - Duration: 12-18 месяцев
  - Systemic risk: LOW
  - Риск: гранулемы (редко)

- **PRP (Platelet-Rich Plasma)**: собственная кровь пациента
  - Duration: 3-6 месяцев (биологический эффект)
  - Systemic risk: VERY LOW (аутолог)
  - Хорошо: натурально, безопасно
  - Минус: дороговато, результаты вариабельны

- **ИЗБЕГАТЬ**: силиконовые имплантаты, синтетические полимеры, неизвестные филеры

### Микронидлинг + RF (СРЕДНЕЕ-НИЗКОЕ ВЛИЯНИЕ)
- Микронидлинг: создает "контролируемые раны" для коллагена
  - Downtime: 1-2 дня
  - Systemic risk: 10-15
  - Хорошо комбинируется: PRP, серум витамина C

- RF (Radiofrequency): тепловой стимулятор коллагена
  - Downtime: минимум
  - Systemic risk: 10-20
  - Примеры: Thermage, eMatrix, RF микронидлинг

## Критические правила БЕЗОПАСНОСТИ

1. БИОДЕГРАДИРУЕМОСТЬ: Используй ТОЛЬКО биодеградируемые филеры
   - HA, PLLA, CaHA: растворяются за 6-24 месяца ✓
   - Силикон, PMMA, другие синтетики: НАВСЕГДА, риск гранулем, миграции ✗

2. НИКАКОЙ ТОКСИЧНОСТИ: Минимизируй системное воспаление
   - Проверь CRP перед процедурой (>5 = отложить)
   - Избегай нескольких больших процедур подряд
   - Требуется 4-6 недель между лазерами

3. ФИБРОЗ ПРОФИЛАКТИКА:
   - Избегай избыточных повторных процедур в одном месте
   - Требуется 3-6 месяцев между процедурами в одной зоне
   - Следи за признаками (затвердение, стянутость)

4. ИНФЕКЦИЯ ПРОФИЛАКТИКА:
   - Требуется стерильность для инъекций
   - Требуется антибиотик крем после лазера (если есть открытые раны)
   - Избегай горячей воды 24-48 часов после

5. АСИММЕТРИЯ РИСК: Требуется опытный injector
   - Start conservative (мало филера лучше, чем много)
   - Требуется follow-up в 2 недели (коррекция)

## Тон
Консервативный, ориентированный на долголетие. Объясняй "красота как здоровье, не как совершенство".
Прозрачен о рисках. Предпочитаю естественный результат (выглядит лучше, чем "сделано").
Защищай пациента от чрезмерных процедур. Уважай желания, но при необходимости скажи "нет".
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "procedure_plan": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "procedure_id": {"type": "string"},
                    "procedure_name": {"type": "string"},
                    "target_area": {"type": "string"},
                    "expected_result": {"type": "string"},
                    "procedure_type": {
                        "type": "string",
                        "enum": [
                            "laser",
                            "injectables",
                            "radiofrequency",
                            "microneedling",
                            "chemical_peel",
                            "other",
                        ],
                    },
                    "systemic_risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
                    "systemic_risks": {"type": "array", "items": {"type": "string"}},
                    "local_risks": {"type": "array", "items": {"type": "string"}},
                    "expected_downtime": {"type": "string"},
                    "recovery_duration": {"type": "string"},
                    "expected_longevity": {"type": "string"},
                    "cost_estimate": {"type": ["number", "null"]},
                    "timing_recommendation": {"type": "string"},
                    "contraindications": {"type": "array", "items": {"type": "string"}},
                    "precautions": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "procedure_id",
                    "procedure_name",
                    "target_area",
                    "expected_result",
                    "procedure_type",
                    "systemic_risk_score",
                ],
            },
        },
        "contraindicated_procedures": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "procedure": {"type": "string"},
                    "reason": {"type": "string"},
                    "alternative": {"type": "string"},
                },
                "required": ["procedure", "reason"],
            },
        },
        "injectable_analysis": {
            "type": "object",
            "properties": {
                "filler_type_recommended": {"type": "string"},
                "filler_rationale": {"type": "string"},
                "filler_areas": {"type": "array", "items": {"type": "string"}},
                "botulinum_toxin_recommendation": {"type": ["string", "null"]},
                "botulinum_units_estimate": {"type": ["integer", "null"]},
                "botulinum_areas": {"type": "array", "items": {"type": "string"}},
                "biocompatibility_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "fibrosis_risk": {"type": "string", "enum": ["low", "moderate", "high"]},
            },
        },
        "optimal_timing": {
            "type": "object",
            "properties": {
                "immediate_procedures": {"type": "array", "items": {"type": "string"}},
                "defer_1_month": {"type": "array", "items": {"type": "string"}},
                "defer_3_months": {"type": "array", "items": {"type": "string"}},
                "reason_for_sequencing": {"type": "string"},
            },
        },
        "systemic_impact_assessment": {
            "type": "object",
            "properties": {
                "immune_system_load": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                },
                "inflammation_spike_expected": {"type": "boolean"},
                "recovery_support_needed": {"type": "array", "items": {"type": "string"}},
                "contraindicated_with_medications": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        },
        "maintenance_protocol": {
            "type": "object",
            "properties": {
                "monthly_actions": {"type": "array", "items": {"type": "string"}},
                "quarterly_assessments": {"type": "array", "items": {"type": "string"}},
                "annual_recheck": {"type": "array", "items": {"type": "string"}},
                "maintenance_procedures_timeline": {"type": "string"},
            },
        },
        "risk_mitigation": {
            "type": "object",
            "properties": {
                "pre_procedure_preparations": {"type": "array", "items": {"type": "string"}},
                "post_procedure_care": {"type": "array", "items": {"type": "string"}},
                "infection_prevention": {"type": "array", "items": {"type": "string"}},
                "fibrosis_prevention": {"type": "array", "items": {"type": "string"}},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "procedure_plan",
        "contraindicated_procedures",
        "injectable_analysis",
        "optimal_timing",
        "systemic_impact_assessment",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_aesthetist",
    "name": "Эстетист",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 3000,
    "description": "Appearance architect. Selects hardware procedures (SMAS, lasers) and injections. Maximize visual rejuvenation with MINIMAL systemic harm. No toxic fillers, prevent fibrosis.",
    "capabilities": [
        "Procedure selection",
        "Injectable expertise",
        "Systemic risk assessment",
        "Fibrosis prevention",
        "Timing optimization",
        "Recovery planning",
        "Maintenance scheduling",
    ],
    "inputs": [
        "facial_assessment",
        "skin_data",
        "current_inflammation_markers",
        "immune_status",
        "recovery_schedule",
        "procedures_history",
        "goals",
        "medications",
        "age_sex_ethnicity",
    ],
    "outputs": [
        "procedure_plan",
        "contraindicated_procedures",
        "injectable_analysis",
        "optimal_timing",
        "systemic_impact_assessment",
    ],
}
