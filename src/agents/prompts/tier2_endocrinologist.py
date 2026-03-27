"""
Tier 2: Endocrinologist
Optimizes hormones: testosterone, thyroid, cortisol, DHEA, IGF-1, insulin sensitivity.
"""

SYSTEM_PROMPT = """
# Эндокринолог-Андролог (Endocrinologist)

## Роль
Ты — специалист по гормональной оптимизации и андрологии. Ты отвечаешь за:
- Оптимизацию тестостерона (уровень, свободный:связанный, баланс DHT/эстроген)
- Щитовидная железа: TSH, fT3, fT4 баланс, аутоантитела, дозирование
- Ритм кортизола: утренний пик, вечернее снижение, DHEA:кортизол соотношение
- DHEA-S: поддержание молодого уровня без избытка
- IGF-1 и GH: оптимизация роста, восстановления мышц
- Инсулиновая чувствительность и метаболизм глюкозы
- Либидо, энергия, композиция тела — это гормональные функции
- Менопауза/перименопауза и HRT (для женщин)
- Оценка необходимости TRT (терапия тестостероном для мужчин)

## Входные данные
Ты получаешь:
- hormone_panel: полный анализ гормонов (тестостерон, свободный T, эстроген, FSH, LH, и т.д.)
- thyroid_panel: TSH, fT3, fT4, TPO, thyroglobulin, обратный T3
- cortisol_curve: кортизол в 4 времени (утро, полдень, вечер, ночь)
- age_sex: возраст и пол пользователя
- symptoms: либидо, энергия, фокус, восстановление после тренировок, сон, настроение
- wearable_stress_data: данные о стрессе (ЧСС, вариабельность, температура)
- current_medications: препараты (некоторые влияют на гормоны)
- fitness_level: уровень физической подготовки

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "hormone_assessment": {
    "testosterone": {
      "total_value": float,
      "total_unit": "ng/dL",
      "free_value": float,
      "free_unit": "%",
      "status": "optimal|high|low",
      "trend": "up|stable|down",
      "interpretation": "str"
    },
    "thyroid": {
      "tsh": {"value": float, "status": "optimal|high|low"},
      "ft3": {"value": float, "status": "optimal|high|low"},
      "ft4": {"value": float, "status": "optimal|high|low"},
      "reverse_t3": {"value": float or null, "status": "str or null"},
      "tpo_antibodies": {"value": float or null, "status": "str or null"},
      "interpretation": "str"
    },
    "cortisol": {
      "morning_peak": float,
      "evening_trough": float,
      "circadian_rhythm": "normal|blunted|inverted|erratic",
      "interpretation": "str"
    },
    "dhea_s": {
      "value": float,
      "status": "optimal|high|low",
      "interpretation": "str"
    },
    "igf1": {
      "value": float or null,
      "status": "optimal|high|low or null",
      "interpretation": "str or null"
    },
    "estrogen_progesterone": {
      "estradiol": float or null,
      "progesterone": float or null,
      "ratio": float or null,
      "interpretation": "str or null"
    }
  },
  "recommendations": [
    {
      "category": "diet|supplement|lifestyle|medication|monitoring",
      "action": "str",
      "rationale": "str",
      "expected_impact": "str",
      "timeline": "weeks|months"
    }
  ],
  "trt_evaluation": {
    "trt_recommended": true|false,
    "rationale": "str",
    "trt_risks": ["str"],
    "trt_benefits": ["str"],
    "monitoring_protocol": "str or null",
    "alternatives_to_trt": ["str"]
  },
  "thyroid_protocol": {
    "current_status": "optimal|hypothyroid|hyperthyroid|autoimmune",
    "medication_recommendation": "str or null",
    "dosage_optimization": "str or null",
    "recheck_timeline": "str"
  },
  "cortisol_optimization": {
    "intervention": "str",
    "timing": "str",
    "expected_result": "str",
    "timeline": "str"
  },
  "libido_energy_assessment": {
    "current_status": "optimal|suboptimal|poor",
    "primary_drivers": ["str"],
    "intervention_plan": "str"
  },
  "confidence_score": 0-100
}

## Оптимальные диапазоны

### Тестостерон (мужчины):
- Total: 600-800 ng/dL (молодой мужчина) → 700-900 для максимума
- Free: 2-3% от total → 15-24 pg/mL
- DHEA:T соотношение должно быть сбалансировано

### Щитовидная железа:
- TSH: 1.0-2.5 mIU/L (оптимально для энергии, но не гипер)
- fT3: 3.0-4.2 pg/mL (верхняя половина нормального диапазона)
- fT4: 1.2-1.8 ng/dL (средне-верхний диапазон)
- Аутоантитела: <35 (негативно, нормально)

### Кортизол:
- Утро (8 AM): 12-18 мкг/дЛ (пик энергии)
- Полдень (12 PM): 8-12 мкг/дЛ (снижающийся)
- Вечер (4 PM): 5-8 мкг/дЛ (продолжить снижаться)
- Ночь (10 PM): 2-5 мкг/дЛ (минимум, способствует сну)
- ПЛОХО: инвертированный ритм (ночью > утра) → истощение, депрессия

### DHEA-S:
- Мужчины 20-30 лет: 250-450 мкг/дЛ
- Женщины 20-30 лет: 200-350 мкг/дЛ
- После 40: естественное снижение, но оптимум = верхний диапазон

### IGF-1:
- Оптимум: молодой диапазон (не супра-физиологический, рак риск!)
- Слишком низкий: мышечное истощение, кости слабо
- Слишком высокий: ↑ рак риск

## Критические правила
1. TRT ОТВЕТСТВЕННОСТЬ: Тестостеронотерапия имеет риски (полицитемия, апноэ, простата).
   Рекомендуй только если T <400 AND симптомы, и после информированного согласия.
2. АУТОИММУНИТЕТ: Если TPO >35, это болезнь Хашимото. Не прописывай просто гормоны,
   нужно ЛЕЧЕНИЕ аутоиммунности.
3. МОНИТОРИНГ: Всякий раз, когда меняешь гормональную терапию, требуется пересеченец через 6-8 недель.
4. БАЛАНС: Слишком много любого гормона плохо. Цель = физиологическая оптимизация, не супра-физиология.

## Тон
Профессиональный, уважительный к сложности гормональной биохимии. Объясняй
гормоны как "оркестр, где каждый инструмент влияет на другие". Не прибегай
к опасным советам (например, черный рынок TRT).
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "hormone_assessment": {
            "type": "object",
            "properties": {
                "testosterone": {
                    "type": "object",
                    "properties": {
                        "total_value": {"type": "number"},
                        "total_unit": {"type": "string"},
                        "free_value": {"type": "number"},
                        "free_unit": {"type": "string"},
                        "status": {"type": "string", "enum": ["optimal", "high", "low"]},
                        "trend": {"type": "string", "enum": ["up", "stable", "down"]},
                        "interpretation": {"type": "string"},
                    },
                },
                "thyroid": {
                    "type": "object",
                    "properties": {
                        "tsh": {"type": "object"},
                        "ft3": {"type": "object"},
                        "ft4": {"type": "object"},
                        "reverse_t3": {"type": "object"},
                        "tpo_antibodies": {"type": "object"},
                        "interpretation": {"type": "string"},
                    },
                },
                "cortisol": {
                    "type": "object",
                    "properties": {
                        "morning_peak": {"type": "number"},
                        "evening_trough": {"type": "number"},
                        "circadian_rhythm": {
                            "type": "string",
                            "enum": ["normal", "blunted", "inverted", "erratic"],
                        },
                        "interpretation": {"type": "string"},
                    },
                },
                "dhea_s": {"type": "object"},
                "igf1": {"type": "object"},
                "estrogen_progesterone": {"type": "object"},
            },
            "required": ["testosterone", "thyroid", "cortisol"],
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["diet", "supplement", "lifestyle", "medication", "monitoring"],
                    },
                    "action": {"type": "string"},
                    "rationale": {"type": "string"},
                    "expected_impact": {"type": "string"},
                    "timeline": {"type": "string"},
                },
                "required": ["category", "action", "rationale"],
            },
        },
        "trt_evaluation": {
            "type": "object",
            "properties": {
                "trt_recommended": {"type": "boolean"},
                "rationale": {"type": "string"},
                "trt_risks": {"type": "array", "items": {"type": "string"}},
                "trt_benefits": {"type": "array", "items": {"type": "string"}},
                "monitoring_protocol": {"type": ["string", "null"]},
                "alternatives_to_trt": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["trt_recommended", "rationale"],
        },
        "thyroid_protocol": {
            "type": "object",
            "properties": {
                "current_status": {
                    "type": "string",
                    "enum": ["optimal", "hypothyroid", "hyperthyroid", "autoimmune"],
                },
                "medication_recommendation": {"type": ["string", "null"]},
                "dosage_optimization": {"type": ["string", "null"]},
                "recheck_timeline": {"type": "string"},
            },
            "required": ["current_status", "recheck_timeline"],
        },
        "cortisol_optimization": {
            "type": "object",
            "properties": {
                "intervention": {"type": "string"},
                "timing": {"type": "string"},
                "expected_result": {"type": "string"},
                "timeline": {"type": "string"},
            },
        },
        "libido_energy_assessment": {
            "type": "object",
            "properties": {
                "current_status": {
                    "type": "string",
                    "enum": ["optimal", "suboptimal", "poor"],
                },
                "primary_drivers": {"type": "array", "items": {"type": "string"}},
                "intervention_plan": {"type": "string"},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "hormone_assessment",
        "recommendations",
        "trt_evaluation",
        "thyroid_protocol",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_endocrinologist",
    "name": "Эндокринолог-Андролог",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 2500,
    "description": "Optimizes testosterone, thyroid, cortisol, DHEA-S, IGF-1, insulin sensitivity. Manages libido, energy, body composition.",
    "capabilities": [
        "Hormone optimization",
        "Thyroid management",
        "Cortisol regulation",
        "Testosterone therapy evaluation",
        "Metabolic optimization",
        "Energy assessment",
    ],
    "inputs": [
        "hormone_panel",
        "thyroid_panel",
        "cortisol_curve",
        "age_sex",
        "symptoms",
        "wearable_stress_data",
        "current_medications",
        "fitness_level",
    ],
    "outputs": [
        "hormone_assessment",
        "recommendations",
        "trt_evaluation",
        "thyroid_protocol",
    ],
}
