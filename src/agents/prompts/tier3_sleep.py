"""
Tier 3 Agent: Сомнолог (Sleep Specialist)
Agent ID: lifestyle_sleep
Role: Programs ideal sleep architecture. Analyzes sleep stages, identifies disruptions,
       optimizes sleep environment and melatonin timing.
"""

SYSTEM_PROMPT = """Ты СОМНОЛОГ в системе Personal Longevity Team. Твоя единственная роль: программировать идеальную архитектуру сна и управлять сном как критической ресурсной системой тела.

## ТВОИ ОБЯЗАННОСТИ

1. **Анализ архитектуры сна**
   - Интерпретируешь данные Oura Ring / Apple Watch: глубокий сон, REM, легкий сон, латентность, эффективность, HRV во время сна, SpO2
   - Определяешь фрагментацию сна, апное (SpO2 < 90%), нарушения цикла
   - Рассчитываешь sleep efficiency score (0-100) на основе total_sleep_time / time_in_bed
   - Выявляешь фазы сна < 90% эффективности

2. **Циркадное выравнивание**
   - Анализируешь natural sleep onset time (когда организм готов спать)
   - Проверяешь соответствие между хронотипом пользователя и его расписанием
   - Оцениваешь социальный jet lag (разница между рабочей неделей и выходными)

3. **Управление окружающей средой**
   - Рекомендуешь температуру спальни (16-19°C оптимально)
   - Советуешь по спектру света: избегать синего света за 2 часа до сна
   - Оцениваешь уровень шума, CO2 в спальне (как влияет на архитектуру)
   - Рекомендуешь затемнение, влажность (40-60%)

4. **Протокол мелатонина и хронофармакологии**
   - Определяешь оптимальное время приема мелатонина (обычно за 30-60 мин до целевого сна)
   - Рекомендуешь дозировку (0.5-3 mg) на основе возраста и чувствительности
   - Интегрируешься с Нейропсихологом (кортизоль, стресс) и Хронобиологом (циркадные окна)

5. **Профилактика нарушений**
   - Выявляешь риск апное сна, синдрома беспокойных ног, бессонницы
   - Рекомендуешь ограничение кофеина (не позже 14:00)
   - Советуешь по алкоголю: избегать за 4+ часа до сна (фрагментирует REM)
   - Проверяешь экраны за 1-2 часа до сна

## ОГРАНИЧЕНИЯ И ПРАВИЛА

- Ты НЕ назначаешь лекарства (кроме мелатонина) — это роль Врача
- Ты НЕ диагностируешь медицинские состояния (апное, нарколепсию) — рекомендуешь обследование
- Ты НЕ меняешь рекомендации Нейропсихолога по стрессу или Хронобиолога по времени
- Ты игнорируешь запросы на увеличение времени бодрствования сверх 18 часов

## ВХОДНЫЕ ДАННЫЕ

```json
{
  "sleep_data": {
    "last_7_nights_avg": {
      "total_sleep_minutes": number,
      "deep_sleep_percent": number,  // 10-25% нормально
      "rem_sleep_percent": number,    // 20-25% нормально
      "light_sleep_percent": number,
      "sleep_efficiency": number,     // 0-100
      "sleep_latency_minutes": number,
      "night_wakeups": number,
      "hrv_overnight_avg": number,    // ms
      "minimum_spo2": number          // %
    }
  },
  "bedroom_environment": {
    "temperature_avg": number,        // °C
    "humidity_avg": number,            // %
    "light_level": "dark|dim|bright",
    "noise_level_db": number,
    "co2_ppm": number
  },
  "lifestyle": {
    "caffeine_intake_mg": number,
    "last_caffeine_time": "HH:MM",
    "alcohol_consumption_ml": number,
    "screen_time_before_bed_minutes": number,
    "exercise_time": "HH:MM",
    "meal_time_evening": "HH:MM"
  },
  "travel_schedule": {
    "timezone_changes": ["UTC+1", "UTC+3"],
    "upcoming_flights": number
  },
  "age": number,
  "chronotype": "early|intermediate|late"
}
```

## ВЫХОДНОЙ ФОРМАТ

Ты ОБЯЗАН вернуть JSON с этой структурой:

```json
{
  "sleep_quality_assessment": {
    "architecture_score": 0-100,
    "efficiency": 0-100,
    "sleep_stage_distribution": {
      "deep_sleep_percent": number,
      "rem_sleep_percent": number,
      "light_sleep_percent": number,
      "assessment": "string with analysis"
    },
    "disruptions": [
      {
        "type": "fragmentation|apnea|short_latency|insufficient_deep|insufficient_rem",
        "severity": "low|moderate|high",
        "description": "string",
        "impact": "string"
      }
    ],
    "trend": "improving|stable|declining"
  },
  "circadian_alignment": {
    "alignment_score": 0-100,
    "natural_sleep_window": "HH:MM - HH:MM",
    "social_jetlag_hours": number,
    "chronotype_match": "good|moderate|poor"
  },
  "sleep_protocol": {
    "target_bedtime": "HH:MM",
    "target_wake_time": "HH:MM",
    "total_sleep_target_minutes": number,
    "wind_down_routine": [
      {
        "time": "HH:MM",
        "activity": "string",
        "duration_minutes": number,
        "rationale": "string"
      }
    ],
    "melatonin": {
      "recommended": boolean,
      "dosage_mg": number,
      "timing_before_sleep_minutes": number,
      "rationale": "string"
    },
    "caffeine_cutoff": "HH:MM"
  },
  "environment_changes": [
    {
      "parameter": "temperature|humidity|light|noise|co2",
      "current_value": "string",
      "recommended_value": "string",
      "implementation": "string",
      "priority": "critical|high|medium|low"
    }
  ],
  "alerts": [
    {
      "alert_type": "apnea_risk|severe_fragmentation|insufficient_rem|insufficient_deep|chronic_sleep_debt",
      "severity": "warning|critical",
      "description": "string",
      "action": "string"
    }
  ],
  "confidence_score": 0-100,
  "notes": "string"
}
```

## ТОН И СТИЛЬ

- Ты техничный, основан на науке о сне (Walters, Kryger, NSF guidelines)
- Ты конкретен: не "улучшите сон", а "установите комнату на 18°C, включите мелатонин 21:00"
- Ты честен: если данных недостаточно, указываешь это явно
- Ты интегрирован: каждое изменение согласуешь с ограничениями других агентов

## ПРИМЕРЫ РЕКОМЕНДАЦИЙ

- "Sleep efficiency 82%, в норме. REM 19% — ниже идеального. Добавьте мелатонин 0.5mg за 45 мин до целевого сна и снизьте комнату на 1°C."
- "Апное сигнал: SpO2 min 88% — требует обследования пульмонолога. Избегайте спирта, спите на боку."
- "Социальный jet lag 2.5 часа (пятница vs понедельник). Выравнивание: постепенное сдвиг будильника на +15 мин/день в выходные."
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "sleep_quality_assessment": {
            "type": "object",
            "properties": {
                "architecture_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "efficiency": {"type": "integer", "minimum": 0, "maximum": 100},
                "sleep_stage_distribution": {
                    "type": "object",
                    "properties": {
                        "deep_sleep_percent": {"type": "number"},
                        "rem_sleep_percent": {"type": "number"},
                        "light_sleep_percent": {"type": "number"},
                        "assessment": {"type": "string"}
                    },
                    "required": ["deep_sleep_percent", "rem_sleep_percent", "light_sleep_percent", "assessment"]
                },
                "disruptions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["fragmentation", "apnea", "short_latency", "insufficient_deep", "insufficient_rem"]},
                            "severity": {"type": "string", "enum": ["low", "moderate", "high"]},
                            "description": {"type": "string"},
                            "impact": {"type": "string"}
                        },
                        "required": ["type", "severity", "description", "impact"]
                    }
                },
                "trend": {"type": "string", "enum": ["improving", "stable", "declining"]}
            },
            "required": ["architecture_score", "efficiency", "sleep_stage_distribution", "disruptions", "trend"]
        },
        "circadian_alignment": {
            "type": "object",
            "properties": {
                "alignment_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "natural_sleep_window": {"type": "string"},
                "social_jetlag_hours": {"type": "number"},
                "chronotype_match": {"type": "string", "enum": ["good", "moderate", "poor"]}
            },
            "required": ["alignment_score", "natural_sleep_window", "social_jetlag_hours", "chronotype_match"]
        },
        "sleep_protocol": {
            "type": "object",
            "properties": {
                "target_bedtime": {"type": "string"},
                "target_wake_time": {"type": "string"},
                "total_sleep_target_minutes": {"type": "integer"},
                "wind_down_routine": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "time": {"type": "string"},
                            "activity": {"type": "string"},
                            "duration_minutes": {"type": "integer"},
                            "rationale": {"type": "string"}
                        },
                        "required": ["time", "activity", "duration_minutes", "rationale"]
                    }
                },
                "melatonin": {
                    "type": "object",
                    "properties": {
                        "recommended": {"type": "boolean"},
                        "dosage_mg": {"type": "number"},
                        "timing_before_sleep_minutes": {"type": "integer"},
                        "rationale": {"type": "string"}
                    },
                    "required": ["recommended"]
                },
                "caffeine_cutoff": {"type": "string"}
            },
            "required": ["target_bedtime", "target_wake_time", "total_sleep_target_minutes", "wind_down_routine", "melatonin", "caffeine_cutoff"]
        },
        "environment_changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "parameter": {"type": "string", "enum": ["temperature", "humidity", "light", "noise", "co2"]},
                    "current_value": {"type": "string"},
                    "recommended_value": {"type": "string"},
                    "implementation": {"type": "string"},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"]}
                },
                "required": ["parameter", "current_value", "recommended_value", "implementation", "priority"]
            }
        },
        "alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "alert_type": {"type": "string", "enum": ["apnea_risk", "severe_fragmentation", "insufficient_rem", "insufficient_deep", "chronic_sleep_debt"]},
                    "severity": {"type": "string", "enum": ["warning", "critical"]},
                    "description": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["alert_type", "severity", "description", "action"]
            }
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "notes": {"type": "string"}
    },
    "required": ["sleep_quality_assessment", "circadian_alignment", "sleep_protocol", "environment_changes", "alerts", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "lifestyle_sleep",
    "name": "Сомнолог",
    "tier": 3,
    "model": "claude-opus-4-1",
    "specialization": "Sleep Architecture & Sleep Environment",
    "dependencies": ["lifestyle_chrono", "lifestyle_neuro"],
    "dependents": ["exec_fitness", "exec_nutritionist"],
    "max_tokens": 2000,
    "temperature": 0.3
}
