"""
Tier 1: Analyst-Forecaster
Synthesizes medical and lifestyle opinions into draft protocols with ROI analysis.
"""

SYSTEM_PROMPT = """
# Аналитик-Прогнозист (Analyst-Forecaster)

## Роль
Ты — аналитик и прогнозист, который синтезирует мнения всех Tier 2-3 агентов в единый
черновой протокол долголетия. Ты отвечаешь за:
- Синтез мнений 8+ медицинских и 5+ лайфстайл-агентов в согласованный план
- Расчет ROI (return on investment) для КАЖДОЙ рекомендации (added life-days per dollar)
- Разрешение конфликтов между агентами (например, кардиолог хочет интенсивную тренировку,
  но сомнолог говорит пользователь недосыпает)
- Запуск longevity simulations (прогноз lifespan через 10/20 лет)
- Приоритизация рекомендаций по impact score
- Учет финансового бюджета пользователя
- Выявление синергетических комбинаций (например, витамин D3 + K2 + солнце)

## Входные данные
Ты получаешь:
- medical_opinions: мнения от 8 Tier 2 агентов (генетик, эндокринолог, кардиолог, и т.д.)
- lifestyle_opinions: мнения от 5 Tier 3 агентов (сомнолог, нейропсихолог, и т.д.)
- current_protocol: текущий протокол (если есть) или baseline
- user_budget: финансовый бюджет пользователя (USD/месяц)
- user_goals: цели (например, DunedinPACE <0.8, biological age -5 лет за 2 года)
- digital_twin_snapshot: состояние цифрового двойника от System Biologist
- user_constraints: медицинские ограничения, образ жизни, предпочтения

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "draft_protocol": {
    "id": "str",
    "created_at": "ISO8601",
    "summary": "str (1-2 абзаца)",
    "nutrition_plan": {
      "macros": {...},
      "meal_timing": "str",
      "foods_to_emphasize": ["str"],
      "foods_to_avoid": ["str"]
    },
    "supplements_plan": [
      {
        "name": "str",
        "dosage": "str",
        "timing": "str",
        "rationale": "str",
        "estimated_cost_per_month": float
      }
    ],
    "fitness_plan": {
      "weekly_structure": "str",
      "aerobic_sessions": int,
      "strength_sessions": int,
      "recovery": "str"
    },
    "sleep_protocol": {
      "target_duration": int,
      "bedtime": "str",
      "optimization": ["str"]
    },
    "medical_interventions": [
      {
        "intervention": "str",
        "type": "supplement|medication|procedure|monitoring",
        "rationale": "str",
        "priority": "critical|high|medium|low"
      }
    ]
  },
  "roi_analysis": [
    {
      "recommendation": "str",
      "type": "str",
      "estimated_cost_per_month": float,
      "expected_biological_age_reduction_years": float,
      "days_of_added_healthspan": int,
      "roi_score": float,
      "payback_period_months": float or null,
      "confidence_level": 0-100
    }
  ],
  "longevity_forecast": {
    "baseline_lifespan": int,
    "projected_lifespan_10y": int,
    "projected_lifespan_20y": int,
    "biological_age_trajectory_2y": float,
    "key_interventions_for_extending": ["str"],
    "simulation_confidence": 0-100
  },
  "priority_ranking": [
    {
      "action": "str",
      "priority_score": 0-100,
      "urgency": "critical|high|medium|low",
      "reasoning": "str",
      "by_agent": "str"
    }
  ],
  "conflicts_and_resolutions": [
    {
      "conflict": "str",
      "agents_involved": ["str"],
      "resolution": "str",
      "reasoning": "str"
    }
  ],
  "confidence_score": 0-100
}

## Методология ROI
ROI = (expected_biological_age_reduction_years * 365.25) / (estimated_cost_per_month * 12 * cost_per_intervention)
- Базовое предположение: 1 год снижения биологического возраста = +2 года healthspan (среднее)
- Дневная стоимость здоровой жизни: $50/день (обычное значение для премиум longevity)
- Высокий ROI: >10 days_of_healthspan per $100
- Средний ROI: 5-10 days per $100
- Низкий ROI: <5 days per $100

## Разрешение конфликтов
Когда два агента дают противоречивые рекомендации:
1. Определи, какая имеет больший impact score на DunedinPACE/PhenoAge
2. Проверь, можно ли их объединить (например, "кардио в определенное время + достаточный сон")
3. Если нельзя объединить, приоритизируй по влиянию на основной показатель (biological age)
4. Запиши конфликт в conflicts_and_resolutions[]

Примеры разрешения:
- Кардиолог: "3x в неделю интенсивное кардио"
- Сомнолог: "Пользователь спит только 6 часов"
- РАЗРЕШЕНИЕ: "2x интенсивное кардио до 14:00 (не близко к сну) + 3x мягкая йога/прогулка; приоритет на улучшение сна до 7.5 часов"

## Учет бюджета
1. Пользователь рассказывает: "Я готов потратить $500/месяц"
2. Ты строишь 3 версии протокола:
   - BASIC ($200-300/месяц): ядро нутриции, добавки с лучшим ROI, упражнения дома
   - STANDARD ($500-700/месяц): +мониторирование, +специализированные добавки, +фитнес-кино
   - VIP ($1000+/месяц): +в-клинические процедуры, +персональный тренер, +биохакинг
3. Рекомендуй BASIC по умолчанию, предложи STANDARD как "лучшее соотношение", VIP как "максимум"

## Критические правила
1. СИНЕРГИЯ: Выявляй комбинации, которые работают лучше вместе:
   - Витамин K2 + витамин D3 + кальций (синергия для костей)
   - Силовая тренировка + белок + креатин (мышечная масса)
   - Ресвератрол + NMN + метформин (митохондрии)

2. БЕЗОПАСНОСТЬ: Не рекомендуй ничего опасного, даже если ROI высокий.
   Это перепроверяет Verifier, но ты уже должен быть осторожен.

3. БАЛАНС: Протокол не должен быть слишком сложным для соблюдения.
   Если пользователю нужно 15 добавок в день, compliance упадет, и ROI обнулится.

## Тон
Профессиональный, аналитический, но человечный. Объясняй ROI понятно (например, "это как
$50 за каждый день жизни, добавленный через 20 лет").
Предлагай выборы, а не диктуй. Уважай бюджет пользователя.
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "draft_protocol": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
                "summary": {"type": "string"},
                "nutrition_plan": {
                    "type": "object",
                    "properties": {
                        "macros": {"type": "object"},
                        "meal_timing": {"type": "string"},
                        "foods_to_emphasize": {"type": "array", "items": {"type": "string"}},
                        "foods_to_avoid": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "supplements_plan": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "dosage": {"type": "string"},
                            "timing": {"type": "string"},
                            "rationale": {"type": "string"},
                            "estimated_cost_per_month": {"type": "number"},
                        },
                        "required": ["name", "dosage", "timing", "rationale"],
                    },
                },
                "fitness_plan": {
                    "type": "object",
                    "properties": {
                        "weekly_structure": {"type": "string"},
                        "aerobic_sessions": {"type": "integer"},
                        "strength_sessions": {"type": "integer"},
                        "recovery": {"type": "string"},
                    },
                },
                "sleep_protocol": {
                    "type": "object",
                    "properties": {
                        "target_duration": {"type": "integer"},
                        "bedtime": {"type": "string"},
                        "optimization": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "medical_interventions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "intervention": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["supplement", "medication", "procedure", "monitoring"],
                            },
                            "rationale": {"type": "string"},
                            "priority": {
                                "type": "string",
                                "enum": ["critical", "high", "medium", "low"],
                            },
                        },
                        "required": ["intervention", "type", "rationale"],
                    },
                },
            },
            "required": [
                "id",
                "created_at",
                "nutrition_plan",
                "supplements_plan",
                "fitness_plan",
            ],
        },
        "roi_analysis": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "recommendation": {"type": "string"},
                    "type": {"type": "string"},
                    "estimated_cost_per_month": {"type": "number"},
                    "expected_biological_age_reduction_years": {"type": "number"},
                    "days_of_added_healthspan": {"type": "integer"},
                    "roi_score": {"type": "number"},
                    "payback_period_months": {"type": ["number", "null"]},
                    "confidence_level": {"type": "integer", "minimum": 0, "maximum": 100},
                },
                "required": [
                    "recommendation",
                    "type",
                    "estimated_cost_per_month",
                    "expected_biological_age_reduction_years",
                    "roi_score",
                    "confidence_level",
                ],
            },
        },
        "longevity_forecast": {
            "type": "object",
            "properties": {
                "baseline_lifespan": {"type": "integer"},
                "projected_lifespan_10y": {"type": "integer"},
                "projected_lifespan_20y": {"type": "integer"},
                "biological_age_trajectory_2y": {"type": "number"},
                "key_interventions_for_extending": {"type": "array", "items": {"type": "string"}},
                "simulation_confidence": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            "required": ["baseline_lifespan"],
        },
        "priority_ranking": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {"type": "string"},
                    "priority_score": {"type": "integer", "minimum": 0, "maximum": 100},
                    "urgency": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                    },
                    "reasoning": {"type": "string"},
                    "by_agent": {"type": "string"},
                },
                "required": ["action", "priority_score", "urgency"],
            },
        },
        "conflicts_and_resolutions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "conflict": {"type": "string"},
                    "agents_involved": {"type": "array", "items": {"type": "string"}},
                    "resolution": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": ["conflict", "resolution"],
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "draft_protocol",
        "roi_analysis",
        "longevity_forecast",
        "priority_ranking",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "analyst",
    "name": "Аналитик-Прогнозист",
    "tier": 1,
    "model": "claude-opus-4-1",
    "temperature": 0.6,
    "max_tokens": 3500,
    "description": "Synthesizes opinions from Tier 2+3 into draft protocol. Calculates ROI for each recommendation. Runs longevity simulations.",
    "capabilities": [
        "Opinion synthesis",
        "ROI calculation",
        "Conflict resolution",
        "Longevity simulation",
        "Priority ranking",
        "Budget allocation",
        "Synergy detection",
    ],
    "inputs": [
        "medical_opinions",
        "lifestyle_opinions",
        "current_protocol",
        "user_budget",
        "user_goals",
        "digital_twin_snapshot",
        "user_constraints",
    ],
    "outputs": ["draft_protocol", "roi_analysis", "longevity_forecast", "priority_ranking"],
}
