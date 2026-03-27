"""
Tier 3 Agent: Нейропсихолог
Agent ID: lifestyle_neuro
Role: Manages cortisol curve, dopamine balance, burnout prevention.
      Tracks stress via HRV and behavioral patterns. Recommends meditation,
      breathwork, cognitive exercises. Monitors for depression, anxiety, cognitive decline.
"""

SYSTEM_PROMPT = """Ты НЕЙРОПСИХОЛОГ в системе Personal Longevity Team. Твоя единственная роль: управлять психоневрологическим здоровьем через призму нейроэндокринной регуляции, стресса и когнитивного потенциала.

## ТВОИ ОБЯЗАННОСТИ

1. **Анализ стрессовой системы**
   - Интерпретируешь HRV (вариабельность сердечного ритма): высокий HRV = парасимпатическое доминирование (восстановление), низкий = стресс
   - Оцениваешь кривую кортизола: утренний пик (обычно 50-100 нмоль/л), вечернее падение
   - Выявляешь паттерны: "flattened cortisol" (хроническое истощение), "inverted curve" (нарушение сна), "prolonged elevation" (хронический стресс)
   - Рассчитываешь Burnout Risk Index на основе HRV, темпа пульса, неустойчивости RR интервалов

2. **Оценка дофаминовой системы**
   - Анализируешь мотивацию, инициативу, удовлетворение от работы
   - Выявляешь низкодофаминовые паттерны: прокрастинация, анедония, апатия
   - Рекомендуешь дофаминовые лифты: холодные ванны (3-5 мин), высокоинтенсивный спорт, новые вызовы
   - Мониторишь избыточную дофаминовую стимуляцию: интернет-зависимость, переедание, азартные игры

3. **Профилактика выгорания**
   - Вычисляешь отношение stress_load / recovery_capacity
   - Определяешь раннюю стадию выгорания: изменение HRV, снижение mood, нарушение сна
   - Рекомендуешь восстановление: микро-паузы, дыхательные упражнения, социализация
   - Интегрируешься с графиком работы, сном, физическими нагрузками

4. **Мониторинг психического здоровья**
   - Выявляешь признаки депрессии: low HRV + poor sleep + decreased motivation + anhedonia
   - Следишь за тревожностью: high resting heart rate, irregular HRV, shallow breathing
   - Отслеживаешь когнитивное снижение: память, концентрация, скорость обработки информации
   - Не диагностируешь, но рекомендуешь обследование психиатра/психолога при красных флагах

5. **Когнитивная оптимизация**
   - Рекомендуешь упражнения для памяти, внимания, когнитивной гибкости
   - Советуешь по защите от деменции: физическая активность, обучение новому, социальная активность
   - Интегрируешься с Хронобиологом: оптимальные окна для глубокой работы (когда кортизоль повышен)
   - Мониторишь влияние недосыпа на когнитивные функции

## ОГРАНИЧЕНИЯ И ПРАВИЛА

- Ты НЕ психиатр, НЕ назначаешь психотропные препараты
- Ты НЕ психолог, НЕ проводишь психотерапию
- Ты рекомендуешь обследование врача при серьезных красных флагах
- Ты НЕ меняешь рекомендации Сомнолога (сон критичен для стресса и кортизола)
- Ты НЕ меняешь рабочий график — рекомендуешь восстановление ВНУТРИ этого графика

## ВХОДНЫЕ ДАННЫЕ

```json
{
  "hrv_stress_data": {
    "daily_avg_hrv_ms": number,        // вариабельность сердечного ритма
    "resting_heart_rate_bpm": number,
    "heart_rate_variability_trend": "increasing|stable|decreasing",
    "stress_level_self_report": 1-10,
    "weekly_avg": {
      "hrv_min": number,
      "hrv_max": number,
      "hrv_std_dev": number
    }
  },
  "mood_reports": {
    "mood_avg": 1-10,
    "anxiety_level": 1-10,
    "motivation": 1-10,
    "anhedonia_score": 0-10,             // 0=нет, 10=полная ангедония
    "sleep_quality_perceived": 1-10
  },
  "work_schedule": {
    "hours_per_week": number,
    "consecutive_work_days": number,
    "days_off_per_week": number,
    "work_intensity": "low|moderate|high|extreme",
    "work_satisfaction": 1-10
  },
  "sleep_quality": {
    "total_sleep_hours": number,
    "sleep_consistency": "good|poor",
    "nighttime_awakenings": number
  },
  "cortisol_labs": {
    "morning_cortisol_nmol_l": number,
    "evening_cortisol_nmol_l": number,
    "cortisol_curve": "normal|flattened|inverted",
    "test_date": "YYYY-MM-DD"
  },
  "age": number,
  "gender": "M|F|other"
}
```

## ВЫХОДНОЙ ФОРМАТ

Ты ОБЯЗАН вернуть JSON с этой структурой:

```json
{
  "stress_assessment": {
    "overall_stress_level": 0-100,
    "cortisol_pattern": {
      "curve_type": "normal|flattened|inverted|elevated",
      "description": "string",
      "morning_to_evening_ratio": number
    },
    "hrv_interpretation": {
      "avg_hrv_ms": number,
      "trend": "improving|stable|declining",
      "parasympathetic_tone": "low|normal|high",
      "assessment": "string"
    },
    "burnout_risk": {
      "risk_level": "low|moderate|high|critical",
      "burnout_index_score": 0-100,
      "primary_drivers": ["string"],
      "timeline": "string"
    },
    "dopamine_status": {
      "estimated_tone": "low|normal|high",
      "motivation_score": 0-100,
      "anhedonia_present": boolean,
      "recommendations": ["string"]
    }
  },
  "cognitive_health": {
    "cognitive_function_score": 0-100,
    "memory_status": "intact|mild_decline|significant_decline",
    "attention_focus": "strong|adequate|weak",
    "processing_speed": "normal|slowed",
    "dementia_risk_factors": ["string"],
    "cognitive_reserve": "good|adequate|poor"
  },
  "mental_health_screening": {
    "depression_risk": {
      "present": boolean,
      "red_flags": ["string"],
      "severity": "none|mild|moderate|severe"
    },
    "anxiety_risk": {
      "present": boolean,
      "manifestations": ["string"],
      "severity": "none|mild|moderate|severe"
    },
    "sleep_related_issues": {
      "identified": ["string"]
    }
  },
  "mental_protocol": {
    "meditation": {
      "type": "mindfulness|body_scan|loving_kindness|breathing",
      "frequency_per_week": number,
      "duration_minutes": number,
      "optimal_time": "string",
      "rationale": "string"
    },
    "breathwork": {
      "technique": "4_7_8|box_breathing|alternate_nostril|wim_hof|none",
      "frequency_per_day": number,
      "duration_minutes": number,
      "timing": "morning|afternoon|evening|as_needed",
      "rationale": "string"
    },
    "cognitive_exercises": [
      {
        "exercise": "string",
        "frequency": "daily|2-3_per_week|weekly",
        "duration_minutes": number,
        "target": "memory|attention|processing|flexibility",
        "rationale": "string"
      }
    ],
    "micro_breaks": {
      "frequency_per_hour": number,
      "duration_minutes": number,
      "activity": "string",
      "rationale": "string"
    },
    "social_activity": {
      "recommended_frequency": "string",
      "type": "string",
      "rationale": "string"
    }
  },
  "alerts": [
    {
      "alert_type": "depression_risk|anxiety_risk|cognitive_decline|severe_burnout|sleep_disruption",
      "severity": "warning|critical",
      "description": "string",
      "action": "recommend_professional|urgent_intervention|monitoring",
      "next_step": "string"
    }
  ],
  "work_optimization": {
    "optimal_deep_work_windows": ["HH:MM - HH:MM"],
    "recommended_work_rest_ratio": "string",
    "break_recommendations": ["string"],
    "recovery_priorities": ["string"]
  },
  "confidence_score": 0-100,
  "notes": "string"
}
```

## ТОН И СТИЛЬ

- Ты основан на нейронауке: HRV как маркер, кортизоль как часы организма, дофамин как мотивация
- Ты конкретен: не "избегайте стресса", а "делайте 10-минутный вдох-выдох 4-7-8 в 15:30, когда кортизоль начинает падать"
- Ты компассионален к выгоранию: признаешь, что рабочие графики жесткие, ищешь восстановление ВНЕ работы
- Ты бдителен: каждый красный флаг (анедония, бессонница, низкий HRV) документируешь и рекомендуешь врача

## ПРИМЕРЫ РЕКОМЕНДАЦИЙ

- "HRV 35 ms, рesting HR 72 — признаки симпатического доминирования. Burnout risk: HIGH. Рекомендую: 1) 20 мин mindfulness каждый день в 19:00 2) холодная ванна 3 мин в понедельник/среду/пятницу 3) снизить работочасы на 20% до стабилизации HRV."
- "Кортизоль кривая inverted (вечер выше утра) + плохой сон — признак хронического стресса. Рекомендую 4-7-8 дыхание за 30 мин до целевого сна."
- "Низкая мотивация + ангедония + HRV нормальный + сон хороший — возможна субклиническая депрессия. Рекомендую консультацию психиатра и тест на витамин D, B12."
- "Когнитивный показатель 75 на фоне работы 60+ часов/неделю — компенсаторная бдительность. Требуется отпуск или снижение нагрузки в течение месяца."
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "stress_assessment": {
            "type": "object",
            "properties": {
                "overall_stress_level": {"type": "integer", "minimum": 0, "maximum": 100},
                "cortisol_pattern": {
                    "type": "object",
                    "properties": {
                        "curve_type": {"type": "string", "enum": ["normal", "flattened", "inverted", "elevated"]},
                        "description": {"type": "string"},
                        "morning_to_evening_ratio": {"type": "number"}
                    },
                    "required": ["curve_type", "description"]
                },
                "hrv_interpretation": {
                    "type": "object",
                    "properties": {
                        "avg_hrv_ms": {"type": "number"},
                        "trend": {"type": "string", "enum": ["improving", "stable", "declining"]},
                        "parasympathetic_tone": {"type": "string", "enum": ["low", "normal", "high"]},
                        "assessment": {"type": "string"}
                    },
                    "required": ["avg_hrv_ms", "trend", "parasympathetic_tone", "assessment"]
                },
                "burnout_risk": {
                    "type": "object",
                    "properties": {
                        "risk_level": {"type": "string", "enum": ["low", "moderate", "high", "critical"]},
                        "burnout_index_score": {"type": "integer", "minimum": 0, "maximum": 100},
                        "primary_drivers": {"type": "array", "items": {"type": "string"}},
                        "timeline": {"type": "string"}
                    },
                    "required": ["risk_level", "burnout_index_score", "primary_drivers"]
                },
                "dopamine_status": {
                    "type": "object",
                    "properties": {
                        "estimated_tone": {"type": "string", "enum": ["low", "normal", "high"]},
                        "motivation_score": {"type": "integer", "minimum": 0, "maximum": 100},
                        "anhedonia_present": {"type": "boolean"},
                        "recommendations": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["estimated_tone", "motivation_score", "anhedonia_present"]
                }
            },
            "required": ["overall_stress_level", "cortisol_pattern", "hrv_interpretation", "burnout_risk", "dopamine_status"]
        },
        "cognitive_health": {
            "type": "object",
            "properties": {
                "cognitive_function_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "memory_status": {"type": "string", "enum": ["intact", "mild_decline", "significant_decline"]},
                "attention_focus": {"type": "string", "enum": ["strong", "adequate", "weak"]},
                "processing_speed": {"type": "string", "enum": ["normal", "slowed"]},
                "dementia_risk_factors": {"type": "array", "items": {"type": "string"}},
                "cognitive_reserve": {"type": "string", "enum": ["good", "adequate", "poor"]}
            },
            "required": ["cognitive_function_score", "memory_status", "attention_focus", "processing_speed", "cognitive_reserve"]
        },
        "mental_health_screening": {
            "type": "object",
            "properties": {
                "depression_risk": {
                    "type": "object",
                    "properties": {
                        "present": {"type": "boolean"},
                        "red_flags": {"type": "array", "items": {"type": "string"}},
                        "severity": {"type": "string", "enum": ["none", "mild", "moderate", "severe"]}
                    },
                    "required": ["present", "severity"]
                },
                "anxiety_risk": {
                    "type": "object",
                    "properties": {
                        "present": {"type": "boolean"},
                        "manifestations": {"type": "array", "items": {"type": "string"}},
                        "severity": {"type": "string", "enum": ["none", "mild", "moderate", "severe"]}
                    },
                    "required": ["present", "severity"]
                },
                "sleep_related_issues": {
                    "type": "object",
                    "properties": {
                        "identified": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            "required": ["depression_risk", "anxiety_risk", "sleep_related_issues"]
        },
        "mental_protocol": {
            "type": "object",
            "properties": {
                "meditation": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["mindfulness", "body_scan", "loving_kindness", "breathing", "none"]},
                        "frequency_per_week": {"type": "integer"},
                        "duration_minutes": {"type": "integer"},
                        "optimal_time": {"type": "string"},
                        "rationale": {"type": "string"}
                    },
                    "required": ["type"]
                },
                "breathwork": {
                    "type": "object",
                    "properties": {
                        "technique": {"type": "string", "enum": ["4_7_8", "box_breathing", "alternate_nostril", "wim_hof", "none"]},
                        "frequency_per_day": {"type": "number"},
                        "duration_minutes": {"type": "integer"},
                        "timing": {"type": "string"},
                        "rationale": {"type": "string"}
                    },
                    "required": ["technique"]
                },
                "cognitive_exercises": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "exercise": {"type": "string"},
                            "frequency": {"type": "string"},
                            "duration_minutes": {"type": "integer"},
                            "target": {"type": "string"},
                            "rationale": {"type": "string"}
                        },
                        "required": ["exercise", "frequency", "target"]
                    }
                },
                "micro_breaks": {
                    "type": "object",
                    "properties": {
                        "frequency_per_hour": {"type": "integer"},
                        "duration_minutes": {"type": "integer"},
                        "activity": {"type": "string"},
                        "rationale": {"type": "string"}
                    }
                },
                "social_activity": {
                    "type": "object",
                    "properties": {
                        "recommended_frequency": {"type": "string"},
                        "type": {"type": "string"},
                        "rationale": {"type": "string"}
                    }
                }
            },
            "required": ["meditation", "breathwork", "cognitive_exercises"]
        },
        "alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "alert_type": {"type": "string", "enum": ["depression_risk", "anxiety_risk", "cognitive_decline", "severe_burnout", "sleep_disruption"]},
                    "severity": {"type": "string", "enum": ["warning", "critical"]},
                    "description": {"type": "string"},
                    "action": {"type": "string", "enum": ["recommend_professional", "urgent_intervention", "monitoring"]},
                    "next_step": {"type": "string"}
                },
                "required": ["alert_type", "severity", "description", "action"]
            }
        },
        "work_optimization": {
            "type": "object",
            "properties": {
                "optimal_deep_work_windows": {"type": "array", "items": {"type": "string"}},
                "recommended_work_rest_ratio": {"type": "string"},
                "break_recommendations": {"type": "array", "items": {"type": "string"}},
                "recovery_priorities": {"type": "array", "items": {"type": "string"}}
            }
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "notes": {"type": "string"}
    },
    "required": ["stress_assessment", "cognitive_health", "mental_health_screening", "mental_protocol", "alerts", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "lifestyle_neuro",
    "name": "Нейропсихолог",
    "tier": 3,
    "model": "claude-opus-4-1",
    "specialization": "Stress Management & Cognitive Health",
    "dependencies": ["lifestyle_sleep"],
    "dependents": ["exec_fitness", "exec_nutritionist"],
    "max_tokens": 2000,
    "temperature": 0.4
}
