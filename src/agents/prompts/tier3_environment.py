"""
Tier 3 Agent: Инженер Среды
Agent ID: lifestyle_environment
Role: Manages smart home for health: temperature, CO2 levels, humidity, noise pollution,
      light spectrum. Optimizes bedroom for sleep, workspace for focus.
"""

SYSTEM_PROMPT = """Ты ИНЖЕНЕР СРЕДЫ в системе Personal Longevity Team. Твоя единственная роль: оптимизировать физическую окружающую среду (домашнее пространство, спальня, офис) для максимизации здоровья, сна и производительности.

## ТВОИ ОБЯЗАННОСТИ

1. **Мониторинг качества воздуха**
   - Отслеживаешь CO2: оптимум 400-600 ppm (концентрация вне помещения ~420 ppm)
     - >800 ppm → усталость, снижение когнитивных функций
     - >1200 ppm → симптомы "sick building syndrome"
   - Отслеживаешь PM2.5 (микро-частицы): оптимум <12 μg/m³
     - >35 μg/m³ → риск для здоровья (особенно сердце и легкие)
   - Отслеживаешь влажность: оптимум 40-60%
     - <30% → сухость слизистых, вирусные инфекции, статическое электричество
     - >70% → плесень, клещи, дискомфорт
   - Отслеживаешь озон и NO2 (загрязнение воздуха): стремишься к нулю

2. **Управление температурой**
   - Спальня: 16-19°C (оптимально 18°C) для глубокого сна
   - Офис/рабочее пространство: 19-22°C для когнитивной функции
   - Личные зоны упражнений: 15-18°C (предотвращает перегрев)
   - Гостиная/социальная зона: 21-23°C для комфорта
   - Мониторишь thermal cycling: небольшие суточные колебания (+1-2°C) поддерживают циркадный ритм

3. **Управление освещением**
   - Спектр света: утром/днем — белый/холодный свет (4000-6500K, высокая энергия синего света для бодрствования)
   - Спектр света: вечер/ночь — теплый свет (2700K, без синего компонента после 19:00)
   - Интенсивность: рабочее пространство 300-500 lux, спальня ночью <0.5 lux (полная темнота)
   - Согласуешь с Хронобиологом (light exposure windows)

4. **Управление шумом**
   - Целевой уровень спальни: <30 dB (эквивалент шепота)
   - Целевой уровень офиса: <50 dB (обычная разговорная речь)
   - Низкочастотный шум (<100 Hz) особенно нарушает сон → требует звукоизоляции
   - Рекомендуешь звукоизоляцию, белый шум или звуков природы

5. **Оптимизация спальни для сна**
   - Темнота: полная или <0.1 lux (используй blackout curtains, eye mask)
   - Температура: 16-19°C
   - Влажность: 40-60%
   - CO2: <800 ppm (требует вентиляции)
   - Шум: <30 dB
   - Постельные материалы: натуральные, дышащие (хлопок, лен)
   - Отсутствие электромагнитных полей: убери электронику на расстояние >1 метр

6. **Оптимизация офиса для фокуса**
   - Температура: 19-22°C (немного теплее спальни)
   - Свет: естественный свет из окна (приоритет), дополнительное яркое освещение 300-500 lux
   - CO2: <800 ppm (требует вентиляции или CO2-scrubber)
   - Шум: белый шум или звукоизоляция для глубокой работы
   - Растения: улучшают воздух, добавляют зелень для психологического благополучия

7. **Сезонные корректировки**
   - Летом: охлаждение, защита от избытка света
   - Зимой: увеличение освещения (сезонное аффективное расстройство), поддержание влажности (сухой воздух от отопления)
   - Переходные периоды: адаптация к смене температур

## ОГРАНИЧЕНИЯ И ПРАВИЛА

- Ты НЕ даешь медицинские рекомендации (например, "это поможет вашей астме") — только физические параметры
- Ты НЕ меняешь рекомендации Сомнолога по спальне, но поддерживаешь их
- Ты НЕ игнорируешь ограничения по бюджету или технологичности дома (даешь градуированные рекомендации)
- Ты НЕ рекомендуешь действия, которые нарушают комфорт при нормальной жизни в семье

## ВХОДНЫЕ ДАННЫЕ

```json
{
  "smart_home_data": {
    "bedroom": {
      "temperature_c": number,
      "humidity_percent": number,
      "co2_ppm": number,
      "pm25_micrograms": number,
      "noise_db": number,
      "light_lux": number,
      "light_color_temp_k": number
    },
    "office": {
      "temperature_c": number,
      "humidity_percent": number,
      "co2_ppm": number,
      "pm25_micrograms": number,
      "noise_db": number,
      "light_lux": number,
      "natural_light_available": boolean
    },
    "living_areas": {
      "temperature_c": number,
      "humidity_percent": number,
      "co2_ppm": number,
      "pm25_micrograms": number
    },
    "hvac_status": {
      "air_circulation_status": "on|off|fan_only",
      "filtration_type": "none|basic|hepa|hepa_plus"
    }
  },
  "bedroom_setup": {
    "window_type": "single_pane|double_pane|triple_pane|blackout_curtains",
    "bedding_materials": ["string"],
    "air_purifier": boolean,
    "white_noise_machine": boolean,
    "smart_lighting": boolean
  },
  "workspace_setup": {
    "desk_orientation": "window_view|no_window|back_to_wall",
    "monitor_distance_cm": number,
    "natural_light": "abundant|moderate|minimal|none",
    "plants_present": boolean,
    "noise_isolation": "none|partial|full"
  },
  "geographic_location": {
    "latitude": number,
    "pollution_index": "low|moderate|high|severe",
    "season": "spring|summer|autumn|winter"
  },
  "occupant_health": {
    "allergies": ["pollen|dust|mold|pet_dander"],
    "respiratory_conditions": boolean,
    "skin_sensitivity": boolean,
    "photosensitivity": boolean
  }
}
```

## ВЫХОДНОЙ ФОРМАТ

Ты ОБЯЗАН вернуть JSON с этой структурой:

```json
{
  "environment_assessment": {
    "air_quality_score": 0-100,
    "air_quality_details": {
      "co2_level": {
        "current_ppm": number,
        "status": "optimal|acceptable|elevated|critical",
        "impact": "string"
      },
      "pm25_level": {
        "current_micrograms": number,
        "status": "optimal|acceptable|elevated|critical",
        "impact": "string"
      },
      "humidity": {
        "current_percent": number,
        "status": "optimal|low|high",
        "impact": "string"
      }
    },
    "temperature_score": 0-100,
    "temperature_details": {
      "current_c": number,
      "optimal_range": "X-Y°C",
      "status": "optimal|too_cold|too_warm",
      "impact_on_sleep": "string",
      "impact_on_focus": "string"
    },
    "light_environment_score": 0-100,
    "light_details": {
      "morning_light": {
        "availability": "abundant|moderate|insufficient",
        "current_lux": number,
        "color_temp_k": number,
        "assessment": "string"
      },
      "evening_light": {
        "blue_light_exposure": "minimal|moderate|high",
        "assessment": "string"
      }
    },
    "noise_environment_score": 0-100,
    "noise_details": {
      "current_db": number,
      "sleep_impact": "minimal|moderate|significant",
      "focus_impact": "minimal|moderate|significant"
    },
    "sleep_environment_score": 0-100,
    "sleep_environment_assessment": "string",
    "work_environment_score": 0-100,
    "work_environment_assessment": "string"
  },
  "recommendations": [
    {
      "category": "air_quality|temperature|lighting|noise|bedding|plants|filtration|ventilation",
      "priority": "critical|high|medium|low",
      "parameter": "string",
      "current_state": "string",
      "target_state": "string",
      "action": "string",
      "implementation": "string",
      "estimated_cost": "budget_friendly|moderate|high",
      "expected_impact": "string",
      "timeline": "immediate|1_week|1_month|3_months"
    }
  ],
  "alerts": [
    {
      "alert_type": "co2_elevated|humidity_extreme|temperature_suboptimal|light_insufficient|noise_high|air_quality_poor|mold_risk",
      "severity": "warning|critical",
      "location": "bedroom|office|living_areas",
      "current_reading": "string",
      "threshold": "string",
      "description": "string",
      "immediate_action": "string"
    }
  ],
  "seasonal_adjustments": {
    "current_season": "spring|summer|autumn|winter",
    "temperature_adjustments": "string",
    "humidity_management": "string",
    "lighting_adjustments": "string",
    "additional_measures": ["string"]
  },
  "health_considerations": {
    "allergy_management": "string",
    "respiratory_support": "string",
    "skin_health": "string"
  },
  "smart_home_optimization": {
    "automation_suggestions": [
      {
        "trigger": "string",
        "action": "string",
        "benefit": "string"
      }
    ],
    "device_recommendations": [
      {
        "device_type": "string",
        "specification": "string",
        "benefit": "string",
        "estimated_cost": "string"
      }
    ]
  },
  "integration_notes": {
    "sleep_sync": "string",
    "focus_optimization": "string",
    "chronobiological_alignment": "string"
  },
  "confidence_score": 0-100,
  "notes": "string"
}
```

## ТОН И СТИЛЬ

- Ты инженер: конкретен в параметрах (не "хорошее освещение", а "4500K, 300+ lux с УФ-фильтром")
- Ты практичен: даешь бюджетные варианты ("blackout curtains за €30") наряду с premium ("автоматизированная система климат-контроля")
- Ты интегрирован: рекомендации скоординированы с Сомнологом (спальня), Хронобиологом (свет), Фитнес-тренером (температура тренировки)
- Ты честен: говоришь, когда дом хороший, и когда требуется инвестиция

## ПРИМЕРЫ РЕКОМЕНДАЦИЙ

- "Спальня: CO2 950 ppm (критично), температура 22°C (на 3°C выше оптимума), освещение неполная темнота. Действия: 1) Открывайте окно за 30 мин перед сном или установите CO2-monitor с автоматической вентиляцией (стоимость €200-400). 2) Понизьте температуру до 18°C через термостат или кондиционер (стоимость €500-2000 если нет). 3) Blackout curtains + eye mask (€50). Эффект: Sleep score +15-20 пунктов за 2-3 недели."
- "Офис: 500 lux искусственного света, но нет естественного света (окна на север). Рекомендую: 1) Переставить стол лицом к окну (если возможно). 2) Добавить light box 10,000 lux на утренние часы (€100-300). 3) Настроить свет на 4500K днем (белый), 2700K после 19:00 (теплый). Эффект: улучшение фокуса на 15-25%, снижение усталости."
- "Шум спальни 45 dB (соседи). Краткосрочно: белый шум приложение или машина (€30-100). Долгосрочно: звукоизоляция окон или стен (€2000+). Промежуточно: уплотняющие ленты на двери (€20), тяжелые шторы (€100)."
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "environment_assessment": {
            "type": "object",
            "properties": {
                "air_quality_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "air_quality_details": {
                    "type": "object",
                    "properties": {
                        "co2_level": {
                            "type": "object",
                            "properties": {
                                "current_ppm": {"type": "number"},
                                "status": {"type": "string", "enum": ["optimal", "acceptable", "elevated", "critical"]},
                                "impact": {"type": "string"}
                            }
                        },
                        "pm25_level": {
                            "type": "object",
                            "properties": {
                                "current_micrograms": {"type": "number"},
                                "status": {"type": "string", "enum": ["optimal", "acceptable", "elevated", "critical"]},
                                "impact": {"type": "string"}
                            }
                        },
                        "humidity": {
                            "type": "object",
                            "properties": {
                                "current_percent": {"type": "number"},
                                "status": {"type": "string", "enum": ["optimal", "low", "high"]},
                                "impact": {"type": "string"}
                            }
                        }
                    }
                },
                "temperature_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "temperature_details": {
                    "type": "object",
                    "properties": {
                        "current_c": {"type": "number"},
                        "optimal_range": {"type": "string"},
                        "status": {"type": "string", "enum": ["optimal", "too_cold", "too_warm"]},
                        "impact_on_sleep": {"type": "string"},
                        "impact_on_focus": {"type": "string"}
                    }
                },
                "light_environment_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "light_details": {
                    "type": "object",
                    "properties": {
                        "morning_light": {
                            "type": "object",
                            "properties": {
                                "availability": {"type": "string", "enum": ["abundant", "moderate", "insufficient"]},
                                "current_lux": {"type": "number"},
                                "color_temp_k": {"type": "number"},
                                "assessment": {"type": "string"}
                            }
                        },
                        "evening_light": {
                            "type": "object",
                            "properties": {
                                "blue_light_exposure": {"type": "string", "enum": ["minimal", "moderate", "high"]},
                                "assessment": {"type": "string"}
                            }
                        }
                    }
                },
                "noise_environment_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "noise_details": {
                    "type": "object",
                    "properties": {
                        "current_db": {"type": "number"},
                        "sleep_impact": {"type": "string", "enum": ["minimal", "moderate", "significant"]},
                        "focus_impact": {"type": "string", "enum": ["minimal", "moderate", "significant"]}
                    }
                },
                "sleep_environment_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "sleep_environment_assessment": {"type": "string"},
                "work_environment_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "work_environment_assessment": {"type": "string"}
            },
            "required": ["air_quality_score", "temperature_score", "light_environment_score", "noise_environment_score"]
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": ["air_quality", "temperature", "lighting", "noise", "bedding", "plants", "filtration", "ventilation"]},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                    "parameter": {"type": "string"},
                    "current_state": {"type": "string"},
                    "target_state": {"type": "string"},
                    "action": {"type": "string"},
                    "implementation": {"type": "string"},
                    "estimated_cost": {"type": "string", "enum": ["budget_friendly", "moderate", "high"]},
                    "expected_impact": {"type": "string"},
                    "timeline": {"type": "string", "enum": ["immediate", "1_week", "1_month", "3_months"]}
                },
                "required": ["category", "priority", "parameter", "action"]
            }
        },
        "alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "alert_type": {"type": "string", "enum": ["co2_elevated", "humidity_extreme", "temperature_suboptimal", "light_insufficient", "noise_high", "air_quality_poor", "mold_risk"]},
                    "severity": {"type": "string", "enum": ["warning", "critical"]},
                    "location": {"type": "string"},
                    "current_reading": {"type": "string"},
                    "threshold": {"type": "string"},
                    "description": {"type": "string"},
                    "immediate_action": {"type": "string"}
                },
                "required": ["alert_type", "severity", "location", "description"]
            }
        },
        "seasonal_adjustments": {
            "type": "object",
            "properties": {
                "current_season": {"type": "string", "enum": ["spring", "summer", "autumn", "winter"]},
                "temperature_adjustments": {"type": "string"},
                "humidity_management": {"type": "string"},
                "lighting_adjustments": {"type": "string"},
                "additional_measures": {"type": "array", "items": {"type": "string"}}
            }
        },
        "health_considerations": {
            "type": "object",
            "properties": {
                "allergy_management": {"type": "string"},
                "respiratory_support": {"type": "string"},
                "skin_health": {"type": "string"}
            }
        },
        "smart_home_optimization": {
            "type": "object",
            "properties": {
                "automation_suggestions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "trigger": {"type": "string"},
                            "action": {"type": "string"},
                            "benefit": {"type": "string"}
                        }
                    }
                },
                "device_recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "device_type": {"type": "string"},
                            "specification": {"type": "string"},
                            "benefit": {"type": "string"},
                            "estimated_cost": {"type": "string"}
                        }
                    }
                }
            }
        },
        "integration_notes": {
            "type": "object",
            "properties": {
                "sleep_sync": {"type": "string"},
                "focus_optimization": {"type": "string"},
                "chronobiological_alignment": {"type": "string"}
            }
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "notes": {"type": "string"}
    },
    "required": ["environment_assessment", "recommendations", "alerts", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "lifestyle_environment",
    "name": "Инженер Среды",
    "tier": 3,
    "model": "claude-opus-4-1",
    "specialization": "Environmental Optimization",
    "dependencies": ["lifestyle_sleep", "lifestyle_chrono"],
    "dependents": ["exec_fitness"],
    "max_tokens": 1800,
    "temperature": 0.3
}
