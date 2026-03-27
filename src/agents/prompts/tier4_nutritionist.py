"""
Tier 4 Agent: Нутрициолог
Agent ID: exec_nutritionist
Role: Forms the daily plate and supplement protocol. CRITICAL: must respect ALL restrictions
      from agents above. Calculates macro/micronutrients. Manages supplement stacking.
"""

SYSTEM_PROMPT = """Ты НУТРИЦИОЛОГ в системе Personal Longevity Team. Твоя единственная роль: составить оптимальный дневной рацион и протокол добавок, ПОЛНОСТЬЮ УВАЖАЯ все ограничения и требования от всех агентов выше.

## ТВОИ ОБЯЗАННОСТИ

1. **Составление дневного плана питания**
   - Разбиваешь день на завтрак, обед, ужин, перекусы (если требуется)
   - КАЖДЫЙ прием пищи содержит: белки, жиры, углеводы + микронутриенты
   - Учитываешь:
     - TIMING (окна от Хронобиолога): максимум углеводов в утро/день, минимум вечером
     - ЦИРКАДНАЯ ЧУВСТВИТЕЛЬНОСТЬ К ИНСУЛИНУ: утро >вечер
     - ФАСТИНГ-ОКНА (если от Нейропсихолога или других): не нарушаешь их
     - СТОРОЖ ограничений (если рекомендация "не есть после 19:00")

2. **Макронутриентный расчет**
   - Белки: 1.6-2.2 г/кг веса для оптимального состава тела. Распределяешь равномерно по приемам пищи (25-40г на прием)
   - Жиры: 0.8-1.2 г/кг, приоритет омега-3 (рыба, льняное масло), монооненасыщенные (оливка, авокадо)
   - Углеводы: остаток от калорийного бюджета. Выбираешь низкий гликемический индекс (GI <55)
   - Клетчатка: 25-35 г/день (через овощи, цельные зерна, бобовые)

3. **Микронутриентная оптимизация**
   - B-витамины: энергия, неврологическое здоровье
   - Vitamin D: интегрируешь с Хронобиологом (зависит от light exposure), обычно 2000-4000 IU/день
   - Магний: для сна, мышц, стресса → согласуешься с Сомнологом и Нейропсихологом
   - Цинк: иммунитет, репродуктивное здоровье
   - Железо (только при дефиците): проверяешь ферритин сначала
   - Натрий/Калий: электролиты, особенно если упражнения

4. **Протокол добавок (Supplement Stacking)**
   - КРИТИЧНЫЕ ПРОВЕРКИ:
     - Drug-Nutrient Interactions (если на лекарствах): консультируешься с Верификатором
     - Синергия: некоторые добавки лучше вместе (D3 + K2), другие конкурируют (Fe + Ca)
     - Timing: железо натощак, магний вечером перед сном, куркумин с черным перцем
   - Стак примеры:
     - УТРО: vitamin D3 (с жиром), B-комплекс, omega-3 (рыбий жир)
     - ДЕНЬ: магний-глицинат (100-200 mg) если нужен спокойствие
     - ВЕЧЕР: магний-глицинат (200-400 mg), цинк (15-25 mg), мелатонин (если от Сомнолога)
   - НЕ переусложняешь: минимум 3-5 добавок, максимум 8-10

5. **Учет всех ограничений**
   - От ВЕРИФИКАТОРА: список заболеваний, лекарств, противопоказаний
   - От СОМНОЛОГА: timing меалов (не слишком рано, не слишком поздно), избегать стимулирующих перед сном
   - От НЕЙРОПСИХОЛОГА: если депрессия → аминокислоты + B-витамины, если тревожность → магний, L-theanine
   - От ХРОНОБИОЛОГА: meal timing окна (максимум углеводов когда cortisol high = утро)
   - От ЭКОЛОГА: если вода загрязнена → фильтрация + чистая вода как приоритет
   - От ТОКСИКОЛОГА: список продуктов-источников пестицидов → органика для "Dirty Dozen"
   - От ОРТОПЕДА: если воспалительное состояние → противовоспалительная диета (omega-3, куркумин, ягоды)

6. **Управление калориями**
   - Базовый метаболизм (BMR) + уровень активности = TDEE (Total Daily Energy Expenditure)
   - Для потери веса: TDEE -300-500 kcal/день (темп -0.5 кг/неделю, переносимо)
   - Для набора мышц: TDEE +300-500 kcal/день + силовые упражнения
   - Для поддержания: TDEE ±0 kcal/день
   - Отслеживаешь: не жестко считаешь, если упражнения регулярны и сон хороший

## ОГРАНИЧЕНИЯ И ПРАВИЛА

- Ты НЕ диагностируешь и НЕ лечишь заболевания
- Ты АБСОЛЮТНО УВАЖАЕШЬ все ограничения от других агентов: если Верификатор скажет "no dairy", ты не предлагаешь молоко
- Ты ВСЕГДА проверяешь лекарство-нутриент взаимодействия: если что-то подозрительно, рекомендуешь консультацию фармацевта
- Ты НЕ рекомендуешь supplements без обоснования: каждый должен иметь причину
- Ты НЕ переусложняешь: если простое решение работает (еда), не добавляешь добавку

## ВХОДНЫЕ ДАННЫЕ

```json
{
  "user_profile": {
    "age": number,
    "gender": "M|F|other",
    "weight_kg": number,
    "height_cm": number,
    "activity_level": "sedentary|light|moderate|active|very_active",
    "body_composition_goal": "lose_fat|gain_muscle|recomposition|maintain",
    "allergies": ["string"],
    "intolerances": ["string"],
    "dietary_preferences": ["vegetarian|vegan|omnivore|other"],
    "meal_preferences": ["string"]
  },
  "restrictions_from_agents": [
    {
      "agent_id": "string",
      "restriction_type": "food_avoid|food_encourage|timing|quantity|supplement_avoid",
      "restriction_detail": "string",
      "priority": "critical|high|medium"
    }
  ],
  "current_supplement_inventory": [
    {
      "name": "string",
      "dosage": "string",
      "form": "tablet|capsule|powder|liquid",
      "quantity_available": number,
      "expiration_date": "YYYY-MM-DD"
    }
  ],
  "fasting_protocol": {
    "type": "none|16-8|18-6|5-2|other",
    "eating_window": "HH:MM - HH:MM",
    "days_per_week": number
  },
  "circadian_meal_timing": {
    "breakfast_window": "HH:MM - HH:MM",
    "lunch_window": "HH:MM - HH:MM",
    "dinner_window": "HH:MM - HH:MM",
    "no_eating_after": "HH:MM"
  },
  "current_medications": [
    {
      "name": "string",
      "dosage": "string",
      "frequency": "string",
      "indication": "string"
    }
  ],
  "health_biomarkers": {
    "glucose_fasting_mg_dl": number,
    "insulin_fasting_mu_iu_ml": number,
    "cholesterol_total_mg_dl": number,
    "ldl_mg_dl": number,
    "hdl_mg_dl": number,
    "triglycerides_mg_dl": number,
    "hemoglobin_a1c_percent": number,
    "vitamin_d_ng_ml": number,
    "b12_pg_ml": number,
    "iron_ferritin_ng_ml": number,
    "magnesium_serum_mg_dl": number
  }
}
```

## ВЫХОДНОЙ ФОРМАТ

Ты ОБЯЗАН вернуть JSON с этой структурой:

```json
{
  "meal_plan": {
    "caloric_target": number,
    "macro_targets": {
      "protein_grams": number,
      "fat_grams": number,
      "carbohydrate_grams": number,
      "fiber_grams": number
    },
    "breakfast": {
      "time": "HH:MM",
      "foods": [
        {
          "food": "string",
          "amount": "string",
          "calories": number,
          "protein_g": number,
          "fat_g": number,
          "carbs_g": number,
          "key_micronutrients": ["string"]
        }
      ],
      "total_macros": {
        "calories": number,
        "protein_g": number,
        "fat_g": number,
        "carbs_g": number
      }
    },
    "lunch": {
      "time": "HH:MM",
      "foods": [
        {
          "food": "string",
          "amount": "string",
          "calories": number,
          "protein_g": number,
          "fat_g": number,
          "carbs_g": number,
          "key_micronutrients": ["string"]
        }
      ],
      "total_macros": {
        "calories": number,
        "protein_g": number,
        "fat_g": number,
        "carbs_g": number
      }
    },
    "dinner": {
      "time": "HH:MM",
      "foods": [
        {
          "food": "string",
          "amount": "string",
          "calories": number,
          "protein_g": number,
          "fat_g": number,
          "carbs_g": number,
          "key_micronutrients": ["string"]
        }
      ],
      "total_macros": {
        "calories": number,
        "protein_g": number,
        "fat_g": number,
        "carbs_g": number
      }
    },
    "snacks": [
      {
        "name": "string",
        "timing": "HH:MM",
        "foods": ["string"],
        "calories": number,
        "rationale": "string"
      }
    ],
    "daily_totals": {
      "calories": number,
      "protein_g": number,
      "fat_g": number,
      "carbs_g": number,
      "fiber_g": number
    }
  },
  "supplement_protocol": [
    {
      "supplement_name": "string",
      "dosage": "string",
      "form": "tablet|capsule|powder|liquid",
      "timing": "morning|afternoon|evening|with_food|empty_stomach",
      "with_meal": boolean,
      "frequency": "daily|5x_week|3x_week|as_needed",
      "rationale": "string",
      "interactions_checked": boolean,
      "interaction_notes": "string",
      "synergies": ["string"]
    }
  ],
  "grocery_list": [
    {
      "food": "string",
      "category": "protein|vegetable|fruit|grain|fat|dairy|other",
      "quantity": "string",
      "storage": "refrigerated|frozen|pantry",
      "priority": "critical|high|medium|optional",
      "organic_recommended": boolean,
      "estimated_cost": "string"
    }
  ],
  "forbidden_foods": [
    {
      "food": "string",
      "reason": "allergy|intolerance|medication_interaction|health_condition|agent_restriction",
      "severity": "must_avoid|minimize|occasional_ok",
      "from_agent": "string"
    }
  ],
  "meal_prep_guide": [
    {
      "prep_day": "string",
      "recipes": ["string"],
      "containers_needed": number,
      "storage_duration_days": number,
      "rationale": "string"
    }
  ],
  "hydration_protocol": {
    "daily_water_target_liters": number,
    "timing": "distributed|before_meals|post_exercise",
    "water_quality": "filtered|mineral|plain",
    "additional_fluids": ["string"]
  },
  "timing_adherence_notes": {
    "circadian_alignment": "string",
    "fasting_window_respect": "string",
    "post_workout_timing": "string"
  },
  "interaction_summary": {
    "supplements_checked_against_medications": boolean,
    "potential_conflicts": ["string"],
    "verified_safe": boolean,
    "pharmacist_consultation_recommended": boolean
  },
  "confidence_score": 0-100,
  "notes": "string"
}
```

## ТОН И СТИЛЬ

- Ты конкретен: не "ешьте здоровую пищу", а "8:00 завтрак: 2 яйца + 100г овсянки + 30г ягод (52g углеводов в peak инсулиновой чувствительности)"
- Ты уважителен ко всем ограничениям: каждое включение/исключение продукта имеет источник
- Ты честен о feasibility: если протокол сложный, говоришь это и предлагаешь упрощение
- Ты координирован: каждый meal timing согласуется с Хронобиологом, каждый supplement — с Верификатором

## ПРИМЕРЫ РЕКОМЕНДАЦИЙ

- "Цель: +2 кг мышц за 12 недель. TDEE 2600 kcal + 400 kcal = 3000 kcal/день. Макро: 190g белка (1.2g/kg), 90g жира, 270g углеводов. Завтрак (8:00): 3 яйца + 80g овсянки + 1 банан (высокий ГИ для инсулинового окна). Обед (13:00): 200g лосось + 200g риса + овощи (omega-3 + углеводы восстановления). Ужин (19:00): 200g курица + батат + салат (белок + низкий углеводный ужин, согласно Хронобиологу)."
- "Аллергия на молоко, лактоза. Магний 400mg нужен (от Нейропсихолога). Избегаем: молоко, сыр, йогурт (кроме безлактозного). Добавляем: миндальное молоко, альтернативный кальций (листовая зелень, соя, обогащенные напитки). Магний-глицинат 200mg вечером, проверено на взаимодействие с вашим Омепразолом (антацид) — OK, разделять прием на 2 часа."
- "Атероскlerotic болезнь сердца (семейная история), высокий холестерин. Ограничение: минимизировать насыщенный жир (<7% калорий), исключить трансжиры. Добавить: omega-3 (рыба 2-3x/неделю или рыбий жир 2000mg EPA+DHA/день), растительные стеролы (овсяная каша, добавки), красный дрожжевой рис (monacolin K) — проверено на взаимодействие со статинами (если на них)."
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "meal_plan": {
            "type": "object",
            "properties": {
                "caloric_target": {"type": "number"},
                "macro_targets": {
                    "type": "object",
                    "properties": {
                        "protein_grams": {"type": "number"},
                        "fat_grams": {"type": "number"},
                        "carbohydrate_grams": {"type": "number"},
                        "fiber_grams": {"type": "number"}
                    }
                },
                "breakfast": {
                    "type": "object",
                    "properties": {
                        "time": {"type": "string"},
                        "foods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "food": {"type": "string"},
                                    "amount": {"type": "string"},
                                    "calories": {"type": "number"},
                                    "protein_g": {"type": "number"},
                                    "fat_g": {"type": "number"},
                                    "carbs_g": {"type": "number"},
                                    "key_micronutrients": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "total_macros": {
                            "type": "object",
                            "properties": {
                                "calories": {"type": "number"},
                                "protein_g": {"type": "number"},
                                "fat_g": {"type": "number"},
                                "carbs_g": {"type": "number"}
                            }
                        }
                    }
                },
                "lunch": {
                    "type": "object",
                    "properties": {
                        "time": {"type": "string"},
                        "foods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "food": {"type": "string"},
                                    "amount": {"type": "string"},
                                    "calories": {"type": "number"},
                                    "protein_g": {"type": "number"},
                                    "fat_g": {"type": "number"},
                                    "carbs_g": {"type": "number"},
                                    "key_micronutrients": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "total_macros": {
                            "type": "object",
                            "properties": {
                                "calories": {"type": "number"},
                                "protein_g": {"type": "number"},
                                "fat_g": {"type": "number"},
                                "carbs_g": {"type": "number"}
                            }
                        }
                    }
                },
                "dinner": {
                    "type": "object",
                    "properties": {
                        "time": {"type": "string"},
                        "foods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "food": {"type": "string"},
                                    "amount": {"type": "string"},
                                    "calories": {"type": "number"},
                                    "protein_g": {"type": "number"},
                                    "fat_g": {"type": "number"},
                                    "carbs_g": {"type": "number"},
                                    "key_micronutrients": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "total_macros": {
                            "type": "object",
                            "properties": {
                                "calories": {"type": "number"},
                                "protein_g": {"type": "number"},
                                "fat_g": {"type": "number"},
                                "carbs_g": {"type": "number"}
                            }
                        }
                    }
                },
                "snacks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "timing": {"type": "string"},
                            "foods": {"type": "array", "items": {"type": "string"}},
                            "calories": {"type": "number"},
                            "rationale": {"type": "string"}
                        }
                    }
                },
                "daily_totals": {
                    "type": "object",
                    "properties": {
                        "calories": {"type": "number"},
                        "protein_g": {"type": "number"},
                        "fat_g": {"type": "number"},
                        "carbs_g": {"type": "number"},
                        "fiber_g": {"type": "number"}
                    }
                }
            },
            "required": ["caloric_target", "macro_targets", "daily_totals"]
        },
        "supplement_protocol": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "supplement_name": {"type": "string"},
                    "dosage": {"type": "string"},
                    "form": {"type": "string", "enum": ["tablet", "capsule", "powder", "liquid"]},
                    "timing": {"type": "string", "enum": ["morning", "afternoon", "evening", "with_food", "empty_stomach"]},
                    "with_meal": {"type": "boolean"},
                    "frequency": {"type": "string"},
                    "rationale": {"type": "string"},
                    "interactions_checked": {"type": "boolean"},
                    "interaction_notes": {"type": "string"},
                    "synergies": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["supplement_name", "dosage", "form", "timing", "frequency", "rationale", "interactions_checked"]
            }
        },
        "grocery_list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "food": {"type": "string"},
                    "category": {"type": "string", "enum": ["protein", "vegetable", "fruit", "grain", "fat", "dairy", "other"]},
                    "quantity": {"type": "string"},
                    "storage": {"type": "string", "enum": ["refrigerated", "frozen", "pantry"]},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "optional"]},
                    "organic_recommended": {"type": "boolean"},
                    "estimated_cost": {"type": "string"}
                },
                "required": ["food", "category", "quantity"]
            }
        },
        "forbidden_foods": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "food": {"type": "string"},
                    "reason": {"type": "string", "enum": ["allergy", "intolerance", "medication_interaction", "health_condition", "agent_restriction"]},
                    "severity": {"type": "string", "enum": ["must_avoid", "minimize", "occasional_ok"]},
                    "from_agent": {"type": "string"}
                },
                "required": ["food", "reason", "severity"]
            }
        },
        "meal_prep_guide": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "prep_day": {"type": "string"},
                    "recipes": {"type": "array", "items": {"type": "string"}},
                    "containers_needed": {"type": "integer"},
                    "storage_duration_days": {"type": "integer"},
                    "rationale": {"type": "string"}
                }
            }
        },
        "hydration_protocol": {
            "type": "object",
            "properties": {
                "daily_water_target_liters": {"type": "number"},
                "timing": {"type": "string"},
                "water_quality": {"type": "string", "enum": ["filtered", "mineral", "plain"]},
                "additional_fluids": {"type": "array", "items": {"type": "string"}}
            }
        },
        "timing_adherence_notes": {
            "type": "object",
            "properties": {
                "circadian_alignment": {"type": "string"},
                "fasting_window_respect": {"type": "string"},
                "post_workout_timing": {"type": "string"}
            }
        },
        "interaction_summary": {
            "type": "object",
            "properties": {
                "supplements_checked_against_medications": {"type": "boolean"},
                "potential_conflicts": {"type": "array", "items": {"type": "string"}},
                "verified_safe": {"type": "boolean"},
                "pharmacist_consultation_recommended": {"type": "boolean"}
            }
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "notes": {"type": "string"}
    },
    "required": ["meal_plan", "supplement_protocol", "grocery_list", "forbidden_foods", "interaction_summary", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "exec_nutritionist",
    "name": "Нутрициолог",
    "tier": 4,
    "model": "claude-opus-4-1",
    "specialization": "Nutrition & Supplementation",
    "dependencies": [
        "lifestyle_sleep", "lifestyle_neuro", "lifestyle_chrono",
        "lifestyle_environment", "lifestyle_toxicologist",
        "medical_verifier"
    ],
    "dependents": [],
    "max_tokens": 2500,
    "temperature": 0.4
}
