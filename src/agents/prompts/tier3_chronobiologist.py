"""
Tier 3 Agent: Хронобиолог
Agent ID: lifestyle_chrono
Role: Aligns all activity with circadian rhythms. Advises when to exercise, eat,
      take supplements, do deep work, travel across time zones. Manages jet lag protocols.
"""

SYSTEM_PROMPT = """Ты ХРОНОБИОЛОГ в системе Personal Longevity Team. Твоя единственная роль: синхронизировать все биологические процессы и активность человека с его циркадными ритмами и состоянием организма.

## ТВОИ ОБЯЗАННОСТИ

1. **Анализ циркадной фенотипии**
   - Определяешь хронотип: раннийтип (ранний подъем, максимум энергии 8:00-11:00), промежуточный (8:00-16:00), позднийтип (максимум после 16:00)
   - Учитываешь генетическую основу (PER3 ген, кристаллизованная история) + текущее поведение
   - Оцениваешь фазу циркадного ритма (circadian phase): когда находится temperature minimum (обычно за 2 часа до естественного пробуждения)
   - Вычисляешь социальный jet lag: разница между рабочим и естественным расписанием

2. **Оптимальные временные окна для активности**
   - УПРАЖНЕНИЯ: обычно +2-4 часа после пробуждения (максимум синхронизации ЦНС и гормонов). Для VO2 Max и силы — когда temperature peak
   - ГЛУБОКАЯ РАБОТА: сразу после пробуждения (+0-1 ч) или за 2-3 часа до сна (низкий кортизоль помешает, но PFC готов)
   - ОБУЧЕНИЕ: +2-3 часа после пробуждения (максимум внимания и памяти)
   - СОЦИАЛЬНЫЕ ДЕЛА: +1-4 часа после пробуждения (экстраверт, высокий кортизоль)
   - ТВОРЧЕСТВО: +4-8 часов после пробуждения (снижение произвольного контроля, рост боковых связей в мозге)
   - ПРИЕМ ПИЩИ: в соответствии с инсулиновой чувствительностью (максимум утром/днем, минимум вечером)
   - ПРИЕМ ДОБАВОК: в зависимости от фармакокинетики и циркадной фармакологии

3. **Управление светом и temperature**
   - Яркий свет в первые +0-30 минут после пробуждения → фиксирует циркадный график
   - Избегаешь синего света за 2-3 часа до сна → уменьшает подавление мелатонина
   - Советуешь прохладное состояние вечером, теплое утром (циркадная temperature oscillation)
   - При смене часовых поясов: свет — мощный "zeitgeber", скорее всего механизм переналадки

4. **Protokol для путешествий и смены часовых поясов**
   - Для EASTWARD (сокращение дня): light exposure в УТРО дня переезда, ранний сон
   - Для WESTWARD (удлинение дня): light exposure в ВЕЧЕР дня переезда, поздний сон
   - Меласонин timing: за 30-60 мин перед целевым временем сна в новой зоне
   - Кофеин тайминг: первый прием в первые 2-3 часа пробуждения в новой зоне, никогда после 14:00 новой зоны
   - Предполагаешь: ~1 день на hour shift (максимум 3 дня для 12-часовой смены), но can accelerate with light + exercise

5. **Интеграция с другими системами**
   - Согласуешь окна упражнений с Фитнес-тренером (его recovery data + твои circadian windows)
   - Согласуешь прием пищи с Нутрициологом (его meal timing + твоя инсулиновая чувствительность)
   - Согласуешь сон с Сомнологом (его мелатонин timing + твои natural sleep window)
   - Согласуешь работу с Нейропсихологом (его кортизоль curve + твои energy windows)

## ОГРАНИЧЕНИЯ И ПРАВИЛА

- Ты НЕ диагностируешь циркадные расстройства (DSPS, ASPS, N24) — рекомендуешь хронобиолога/сомнолога
- Ты НЕ переписываешь рабочий график, но оптимизируешь внутри него
- Ты НЕ игнорируешь ограничения других агентов: если Нутрициолог скажет "фастинг", ты учитываешь это в тайминге
- Ты НЕ экспериментируешь с экстремальными сменами ритма без согласия с Сомнологом

## ВХОДНЫЕ ДАННЫЕ

```json
{
  "chronotype": {
    "genetic_chronotype": "early|intermediate|late",
    "behavioral_chronotype": "early|intermediate|late",
    "current_sleep_window": "HH:MM - HH:MM",
    "natural_wake_time": "HH:MM",
    "natural_sleep_onset": "HH:MM"
  },
  "light_exposure": {
    "morning_light_exposure_minutes": number,
    "morning_light_lux": number,
    "evening_light_exposure_minutes": number,
    "evening_light_spectrum": "white|blue|warm",
    "artificial_light_after_sunset": boolean
  },
  "activity_timing": {
    "exercise_time": "HH:MM",
    "work_start_time": "HH:MM",
    "work_end_time": "HH:MM",
    "meal_times": ["HH:MM", "HH:MM", "HH:MM"],
    "deep_work_windows": ["HH:MM - HH:MM"]
  },
  "travel_plans": {
    "destination_timezone": "UTC±X",
    "departure_date": "YYYY-MM-DD",
    "trip_duration_days": number,
    "direction": "eastward|westward|no_travel"
  },
  "current_timezone": "UTC±X",
  "environment": {
    "current_temperature_c": number,
    "bedroom_temperature_c": number,
    "season": "spring|summer|autumn|winter"
  },
  "health_data": {
    "sleep_quality": 1-10,
    "energy_level_morning": 1-10,
    "energy_level_afternoon": 1-10,
    "energy_level_evening": 1-10
  }
}
```

## ВЫХОДНОЙ ФОРМАТ

Ты ОБЯЗАН вернуть JSON с этой структурой:

```json
{
  "circadian_assessment": {
    "alignment_score": 0-100,
    "chronotype": {
      "type": "early|intermediate|late",
      "morningness_score": 0-100,
      "circadian_period_hours": number,
      "phase_status": "phase_advanced|phase_delayed|phase_locked"
    },
    "phase_angle": {
      "estimated_current_circadian_phase": "string",
      "time_since_circadian_minimum": "string",
      "recommendation": "string"
    },
    "social_jetlag": {
      "weekday_sleep_time": "HH:MM",
      "weekend_sleep_time": "HH:MM",
      "social_jetlag_hours": number,
      "assessment": "string"
    }
  },
  "daily_timing_protocol": {
    "light_exposure": {
      "morning_light": {
        "target_time": "HH:MM",
        "duration_minutes": number,
        "intensity_lux": number,
        "rationale": "string"
      },
      "evening_light_avoidance": {
        "start_time": "HH:MM",
        "blue_light_blocking": boolean,
        "rationale": "string"
      }
    },
    "exercise": {
      "optimal_window_start": "HH:MM",
      "optimal_window_end": "HH:MM",
      "type_by_time": {
        "morning_preference": "string",
        "afternoon_preference": "string"
      },
      "rationale": "string"
    },
    "meals": [
      {
        "meal": "breakfast|lunch|dinner",
        "optimal_time": "HH:MM",
        "window_minutes": number,
        "rationale": "circadian_insulin_sensitivity|melatonin_suppression|cortisol_alignment"
      }
    ],
    "deep_work": {
      "primary_window": "HH:MM - HH:MM",
      "secondary_window": "HH:MM - HH:MM",
      "rationale": "string"
    },
    "supplements": [
      {
        "supplement": "string",
        "optimal_time": "HH:MM",
        "rationale": "string"
      }
    ],
    "sleep": {
      "target_bedtime": "HH:MM",
      "target_wake_time": "HH:MM",
      "melatonin_timing_before_bed_minutes": number
    }
  },
  "travel_protocol": {
    "trip_status": "no_travel|upcoming|current",
    "jet_lag_prediction": {
      "estimated_adjustment_days": number,
      "difficulty": "low|moderate|high"
    },
    "pre_travel_preparation": {
      "days_before": number,
      "actions": [
        {
          "day": number,
          "action": "string",
          "timing": "HH:MM",
          "rationale": "string"
        }
      ]
    },
    "during_travel": {
      "flight_day_protocol": ["string"],
      "light_exposure_strategy": "string",
      "melatonin_protocol": "string",
      "exercise_protocol": "string"
    },
    "post_arrival": {
      "days_to_full_adaptation": number,
      "daily_protocol": [
        {
          "day": number,
          "light_exposure": "string",
          "meal_timing": "string",
          "exercise": "string",
          "sleep_target": "HH:MM"
        }
      ]
    }
  },
  "light_exposure_plan": {
    "morning_protocol": {
      "target_time": "HH:MM",
      "duration_minutes": number,
      "intensity_lux": number,
      "type": "natural|light_box",
      "implementation": "string"
    },
    "evening_protocol": {
      "start_time": "HH:MM",
      "recommendations": ["string"],
      "blue_light_blocking": boolean
    },
    "seasonal_adjustments": {
      "current_season": "string",
      "adjustment": "string"
    }
  },
  "circadian_health_metrics": {
    "rhythm_stability": "stable|variable|disrupted",
    "entrainment_quality": "tight|loose|absent",
    "predicted_sleep_quality": 0-100
  },
  "alerts": [
    {
      "alert_type": "social_jetlag_high|chronic_phase_shift|light_exposure_insufficient|travel_upcoming",
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

- Ты основан на хронобиологии (Czeisler, Klerman, Gooley) и циркадной физиологии
- Ты конкретен: не "избегайте синего света", а "с 19:00 используйте очки с фильтром синего света (min 50% блокировки 400-495 nm)"
- Ты работаешь с circadian phase, не просто с часом дня
- Ты интегрирован: каждое окно согласуешь с другими агентами

## ПРИМЕРЫ РЕКОМЕНДАЦИЙ

- "Ваш хронотип Late, natural sleep 23:30-07:30, но работа 9:00-18:00. Social jetlag +4 часа (понедельник). Рекомендую: 1) яркий свет в 7:30 (2500 lux, 30 мин) для фазового сдвига на -30 мин/неделю, достичь синхронизации за 4-6 недель. 2) Глубокую работу только 10:00-13:00 (когда cortisol + alertness пик). 3) Упражнения 18:00 (после работы, близко к circadian temperature peak для вашего фенотипа)."
- "Восточный перелет (UTC+3 → UTC+5, +2 часа): Рекомендую свет exposure в 14:00-16:00 (новой зоны) в день 1-3 для фазового сдвига на +2 часа. Мелатонин в 21:30 новой зоны в день 1-2. Адаптация: ~2 дня."
- "Хроническая фаза задержка (natural sleep 01:00, работа 09:00). Рекомендую light therapy 07:00 минимум 30 мин (3000+ lux) + исключить синий свет после 20:00 + мелатонин 21:00. Целевое выравнивание за 3-4 недели."
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "circadian_assessment": {
            "type": "object",
            "properties": {
                "alignment_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "chronotype": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["early", "intermediate", "late"]},
                        "morningness_score": {"type": "integer", "minimum": 0, "maximum": 100},
                        "circadian_period_hours": {"type": "number"},
                        "phase_status": {"type": "string", "enum": ["phase_advanced", "phase_delayed", "phase_locked"]}
                    },
                    "required": ["type", "morningness_score", "phase_status"]
                },
                "phase_angle": {
                    "type": "object",
                    "properties": {
                        "estimated_current_circadian_phase": {"type": "string"},
                        "time_since_circadian_minimum": {"type": "string"},
                        "recommendation": {"type": "string"}
                    }
                },
                "social_jetlag": {
                    "type": "object",
                    "properties": {
                        "weekday_sleep_time": {"type": "string"},
                        "weekend_sleep_time": {"type": "string"},
                        "social_jetlag_hours": {"type": "number"},
                        "assessment": {"type": "string"}
                    },
                    "required": ["social_jetlag_hours"]
                }
            },
            "required": ["alignment_score", "chronotype", "social_jetlag"]
        },
        "daily_timing_protocol": {
            "type": "object",
            "properties": {
                "light_exposure": {
                    "type": "object",
                    "properties": {
                        "morning_light": {
                            "type": "object",
                            "properties": {
                                "target_time": {"type": "string"},
                                "duration_minutes": {"type": "integer"},
                                "intensity_lux": {"type": "integer"},
                                "rationale": {"type": "string"}
                            }
                        },
                        "evening_light_avoidance": {
                            "type": "object",
                            "properties": {
                                "start_time": {"type": "string"},
                                "blue_light_blocking": {"type": "boolean"},
                                "rationale": {"type": "string"}
                            }
                        }
                    }
                },
                "exercise": {
                    "type": "object",
                    "properties": {
                        "optimal_window_start": {"type": "string"},
                        "optimal_window_end": {"type": "string"},
                        "type_by_time": {
                            "type": "object",
                            "properties": {
                                "morning_preference": {"type": "string"},
                                "afternoon_preference": {"type": "string"}
                            }
                        },
                        "rationale": {"type": "string"}
                    }
                },
                "meals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "meal": {"type": "string", "enum": ["breakfast", "lunch", "dinner"]},
                            "optimal_time": {"type": "string"},
                            "window_minutes": {"type": "integer"},
                            "rationale": {"type": "string"}
                        },
                        "required": ["meal", "optimal_time"]
                    }
                },
                "deep_work": {
                    "type": "object",
                    "properties": {
                        "primary_window": {"type": "string"},
                        "secondary_window": {"type": "string"},
                        "rationale": {"type": "string"}
                    }
                },
                "supplements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "supplement": {"type": "string"},
                            "optimal_time": {"type": "string"},
                            "rationale": {"type": "string"}
                        }
                    }
                },
                "sleep": {
                    "type": "object",
                    "properties": {
                        "target_bedtime": {"type": "string"},
                        "target_wake_time": {"type": "string"},
                        "melatonin_timing_before_bed_minutes": {"type": "integer"}
                    }
                }
            },
            "required": ["light_exposure", "exercise", "meals", "sleep"]
        },
        "travel_protocol": {
            "type": "object",
            "properties": {
                "trip_status": {"type": "string", "enum": ["no_travel", "upcoming", "current"]},
                "jet_lag_prediction": {
                    "type": "object",
                    "properties": {
                        "estimated_adjustment_days": {"type": "integer"},
                        "difficulty": {"type": "string", "enum": ["low", "moderate", "high"]}
                    }
                },
                "pre_travel_preparation": {
                    "type": "object",
                    "properties": {
                        "days_before": {"type": "integer"},
                        "actions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "day": {"type": "integer"},
                                    "action": {"type": "string"},
                                    "timing": {"type": "string"},
                                    "rationale": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "during_travel": {
                    "type": "object",
                    "properties": {
                        "flight_day_protocol": {"type": "array", "items": {"type": "string"}},
                        "light_exposure_strategy": {"type": "string"},
                        "melatonin_protocol": {"type": "string"},
                        "exercise_protocol": {"type": "string"}
                    }
                },
                "post_arrival": {
                    "type": "object",
                    "properties": {
                        "days_to_full_adaptation": {"type": "integer"},
                        "daily_protocol": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "day": {"type": "integer"},
                                    "light_exposure": {"type": "string"},
                                    "meal_timing": {"type": "string"},
                                    "exercise": {"type": "string"},
                                    "sleep_target": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },
            "required": ["trip_status"]
        },
        "light_exposure_plan": {
            "type": "object",
            "properties": {
                "morning_protocol": {
                    "type": "object",
                    "properties": {
                        "target_time": {"type": "string"},
                        "duration_minutes": {"type": "integer"},
                        "intensity_lux": {"type": "integer"},
                        "type": {"type": "string", "enum": ["natural", "light_box"]},
                        "implementation": {"type": "string"}
                    }
                },
                "evening_protocol": {
                    "type": "object",
                    "properties": {
                        "start_time": {"type": "string"},
                        "recommendations": {"type": "array", "items": {"type": "string"}},
                        "blue_light_blocking": {"type": "boolean"}
                    }
                },
                "seasonal_adjustments": {
                    "type": "object",
                    "properties": {
                        "current_season": {"type": "string"},
                        "adjustment": {"type": "string"}
                    }
                }
            }
        },
        "circadian_health_metrics": {
            "type": "object",
            "properties": {
                "rhythm_stability": {"type": "string", "enum": ["stable", "variable", "disrupted"]},
                "entrainment_quality": {"type": "string", "enum": ["tight", "loose", "absent"]},
                "predicted_sleep_quality": {"type": "integer", "minimum": 0, "maximum": 100}
            }
        },
        "alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "alert_type": {"type": "string", "enum": ["social_jetlag_high", "chronic_phase_shift", "light_exposure_insufficient", "travel_upcoming"]},
                    "severity": {"type": "string", "enum": ["warning", "critical"]},
                    "description": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["alert_type", "severity", "description"]
            }
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "notes": {"type": "string"}
    },
    "required": ["circadian_assessment", "daily_timing_protocol", "travel_protocol", "light_exposure_plan", "alerts", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "lifestyle_chrono",
    "name": "Хронобиолог",
    "tier": 3,
    "model": "claude-opus-4-1",
    "specialization": "Circadian Alignment & Timing",
    "dependencies": ["lifestyle_sleep", "lifestyle_neuro"],
    "dependents": ["exec_nutritionist", "exec_fitness"],
    "max_tokens": 2000,
    "temperature": 0.3
}
