"""
Tier 5 Operations Agent: Медицинский Консьерж (Medical Concierge)
Role: Books appointments, purchases supplements, manages logistics.
"""

SYSTEM_PROMPT = """Ты — Медицинский Консьерж, виртуальный помощник пользователя, который занимается
всеми логистическими деталями его здоровья: бронирует анализы крови, связывается с клиниками,
покупает добавки и лекарства, управляет расписанием.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Бронировать анализы крови в лучших доступных лабораториях
2. Координировать медицинские процедуры с клиниками
3. Находить и закупать требуемые добавки и лекарства по лучшим ценам
4. Управлять календарем приемов и анализов
5. Обеспечивать инструкции по подготовке к процедурам

ЭТАПЫ РАБОТЫ:

1. ПОИСК КЛИНИК И ЛАБОРАТОРИЙ:
   - Использовать user_location для поиска ближайших учреждений
   - Проверять рейтинги и отзывы клиник
   - Предпочитать клиники из preferred_clinics, если указаны
   - Рассчитывать время в пути и удобство графика

2. БРОНИРОВАНИЕ АНАЛИЗОВ:
   - Проверять доступные даты и время
   - Выбирать наиболее удобные слоты для пользователя
   - Учитывать требования к подготовке (натощак, без лекарств и т.д.)
   - Подтверждать бронирование (с оговоркой, что это требует подтверждения)

3. ЗАКУПКА ДОБАВОК И ЛЕКАРСТВ:
   - Проверять несколько поставщиков (аптеки, маркетплейсы)
   - Находить лучшие цены за качество
   - Учитывать доставку и сроки
   - Проверять подлинность для дорогостоящих товаров

4. УПРАВЛЕНИЕ ЛОГИСТИКОЙ:
   - Синхронизировать все сроки (анализы должны быть до назначения препаратов)
   - Учитывать графики пользователя (schedule_constraints)
   - Оптимизировать количество визитов в клинику
   - Отслеживать доставки и статусы заказов

ВХОДНЫЕ ДАННЫЕ:
- required_tests[]: анализы, которые нужно провести
  - test_name: название анализа
  - urgency: "immediate" | "week" | "month"
  - fasting_required: нужен ли натощак
  - frequency: сколько раз в год / в какие сроки

- required_procedures[]: процедуры (УЗИ, ЭКГ и т.д.)
  - procedure_name
  - urgency
  - estimated_duration
  - prerequisites (например, "анализ крови")

- user_location: город, адрес пользователя (для поиска клиник)

- preferred_clinics[]: список предпочитаемых клиник и лабораторий

- budget: месячный или полугодовой бюджет на медицинские услуги

- schedule_constraints: ограничения по времени
  - preferred_days: какие дни удобны
  - working_hours: когда пользователь работает
  - travel_time_acceptable: максимальное время в пути

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. appointment_plan: массив всех бронирований
   - Каждое бронирование:
     - type: "blood_test" | "ultrasound" | "ecg" | "procedure" | "consultation"
     - name: название
     - clinic_name: где проводится
     - clinic_address: адрес
     - recommended_date: рекомендуемая дата (с учетом schedule_constraints)
     - time_slot: время в формате HH:MM
     - duration_minutes: сколько минут займет
     - cost_estimate: примерная стоимость
     - preparation_instructions: как готовиться (натощак, отмена лекарств и т.д.)
     - booking_status: "proposed" | "confirmed_pending_user" | "confirmed"
     - notes: дополнительные замечания

2. purchase_list: товары, которые нужно купить
   - item_name: название добавки/лекарства
   - quantity: количество упаковок
   - unit_price: цена за единицу
   - best_source: где купить (аптека, маркетплейс, сайт)
     - supplier_name
     - supplier_url или phone
     - estimated_delivery_days
   - total_cost: стоимость позиции
   - priority: "high" | "medium" | "low"
   - prescription_required: нужен ли рецепт

3. logistics_notes: общие замечания по логистике
   - critical_path: последовательность действий (например: анализ кровь -> тетрапак -> консультация)
   - optimal_schedule: рекомендуемое расписание на неделю/месяц
   - budget_impact: сколько денег потребуется и на что
   - risk_mitigation: возможные проблемы и как их избежать

4. cost_summary:
   - total_estimated_cost
   - tests_cost
   - procedures_cost
   - supplements_cost
   - travel_cost_estimate
   - cost_vs_budget: вмещается ли в бюджет?

5. follow_up_schedule: когда нужны повторные анализы
   - type: "repeat_test"
   - test_name
   - recommended_timeframe: "monthly" | "quarterly" | "6_months" | "annual"

6. confidence_score: уверенность в плане (0-100)

КРИТИЧЕСКИЕ ПРАВИЛА:
1. НИКОГДА не обещай забронировать без подтверждения пользователя
2. Используй фразу "предлагаю забронировать" или "рекомендую"
3. Указывай contact_info клиник для подтверждения
4. Проверяй наличие рецепта для лекарств, требующих рецепта
5. Учитывай время в пути, чтобы не создавать нереальный график
6. Выбирай добавки только известных производителей

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Получаешь необходимые тесты и процедуры -> от Tier 2-3
- Отправляешь закупки -> ops_finance для проверки цен
- Уведомляешь ops_dispatcher -> чтобы добавить напоминания в контракты
- Отправляешь информацию о доставке -> ops_inventory"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "appointment_plan": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["blood_test", "ultrasound", "ecg", "procedure", "consultation", "other"],
                        "description": "Type of appointment"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of test or procedure"
                    },
                    "clinic_name": {
                        "type": "string",
                        "description": "Clinic or lab name"
                    },
                    "clinic_address": {
                        "type": "string",
                        "description": "Full address including city"
                    },
                    "contact_info": {
                        "type": "object",
                        "properties": {
                            "phone": {
                                "type": "string"
                            },
                            "website": {
                                "type": "string"
                            },
                            "email": {
                                "type": "string"
                            }
                        },
                        "description": "How to contact the clinic"
                    },
                    "recommended_date": {
                        "type": "string",
                        "format": "date",
                        "description": "Proposed date (respects user schedule)"
                    },
                    "time_slot": {
                        "type": "string",
                        "pattern": "^([0-1][0-9]|2[0-3]):[0-5][0-9]$",
                        "description": "Time in HH:MM format"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Estimated duration in minutes"
                    },
                    "cost_estimate": {
                        "type": "number",
                        "description": "Estimated cost in local currency"
                    },
                    "currency": {
                        "type": "string",
                        "description": "Currency code (RUB, USD, EUR, etc)"
                    },
                    "preparation_instructions": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Preparation step"
                        },
                        "description": "How to prepare (fasting, medication adjustments, etc)"
                    },
                    "booking_status": {
                        "type": "string",
                        "enum": ["proposed", "confirmed_pending_user", "confirmed"],
                        "description": "Current booking status"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional information"
                    }
                },
                "required": ["type", "name", "clinic_name", "clinic_address", "recommended_date", "time_slot", "duration_minutes", "cost_estimate", "booking_status", "preparation_instructions"]
            },
            "description": "Plan of all appointments and tests to book"
        },
        "purchase_list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of supplement/medication"
                    },
                    "dosage": {
                        "type": "string",
                        "description": "Dosage (e.g., '500mg per pill', '2% solution')"
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Number of units to purchase"
                    },
                    "unit": {
                        "type": "string",
                        "description": "Unit (pills, bottles, grams, etc)"
                    },
                    "unit_price": {
                        "type": "number",
                        "description": "Price per unit"
                    },
                    "currency": {
                        "type": "string",
                        "description": "Currency code"
                    },
                    "total_cost": {
                        "type": "number",
                        "description": "Total cost for this item"
                    },
                    "best_source": {
                        "type": "object",
                        "properties": {
                            "supplier_name": {
                                "type": "string"
                            },
                            "supplier_url": {
                                "type": "string"
                            },
                            "phone": {
                                "type": "string"
                            },
                            "estimated_delivery_days": {
                                "type": "integer",
                                "description": "Days until delivery"
                            }
                        },
                        "required": ["supplier_name"],
                        "description": "Best place to buy"
                    },
                    "alternative_sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "supplier_name": {
                                    "type": "string"
                                },
                                "unit_price": {
                                    "type": "number"
                                },
                                "estimated_delivery_days": {
                                    "type": "integer"
                                }
                            },
                            "required": ["supplier_name"]
                        },
                        "description": "Alternative purchasing options"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                        "description": "Urgency of this purchase"
                    },
                    "prescription_required": {
                        "type": "boolean",
                        "description": "Is a prescription needed?"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Quality notes, authenticity tips, etc"
                    }
                },
                "required": ["item_name", "quantity", "unit", "unit_price", "total_cost", "best_source", "priority", "prescription_required"]
            },
            "description": "List of supplements and medications to purchase"
        },
        "logistics_notes": {
            "type": "object",
            "properties": {
                "critical_path": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Step in the critical path"
                    },
                    "description": "Sequence that must be followed (e.g., tests before treatment)"
                },
                "optimal_schedule": {
                    "type": "string",
                    "description": "Recommended weekly/monthly schedule"
                },
                "budget_impact": {
                    "type": "string",
                    "description": "Financial summary and budget fit"
                },
                "risk_mitigation": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "risk": {
                                "type": "string",
                                "description": "Potential problem"
                            },
                            "mitigation": {
                                "type": "string",
                                "description": "How to prevent or handle it"
                            }
                        },
                        "required": ["risk", "mitigation"]
                    },
                    "description": "Potential issues and how to avoid them"
                }
            },
            "description": "Overall logistics and coordination notes"
        },
        "cost_summary": {
            "type": "object",
            "properties": {
                "total_estimated_cost": {
                    "type": "number",
                    "description": "Total cost of all appointments and purchases"
                },
                "tests_cost": {
                    "type": "number",
                    "description": "Total cost of blood tests and diagnostics"
                },
                "procedures_cost": {
                    "type": "number",
                    "description": "Total cost of procedures"
                },
                "supplements_cost": {
                    "type": "number",
                    "description": "Total cost of supplements and medications"
                },
                "travel_cost_estimate": {
                    "type": "number",
                    "description": "Estimated travel costs"
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code"
                },
                "user_budget": {
                    "type": "number",
                    "description": "User's available budget"
                },
                "within_budget": {
                    "type": "boolean",
                    "description": "Does plan fit in user's budget?"
                },
                "budget_remaining": {
                    "type": "number",
                    "description": "Budget remaining after this plan"
                }
            },
            "required": ["total_estimated_cost", "currency", "within_budget"]
        },
        "follow_up_schedule": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "test_name": {
                        "type": "string",
                        "description": "Name of test to repeat"
                    },
                    "recommended_timeframe": {
                        "type": "string",
                        "enum": ["monthly", "quarterly", "6_months", "annual", "as_needed"],
                        "description": "How often this test should be repeated"
                    },
                    "next_scheduled_date": {
                        "type": "string",
                        "format": "date",
                        "description": "When to schedule the next one"
                    }
                },
                "required": ["test_name", "recommended_timeframe"]
            },
            "description": "Schedule for follow-up tests and monitoring"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in this logistics plan (0-100)"
        }
    },
    "required": ["appointment_plan", "purchase_list", "cost_summary", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "ops_concierge",
    "name": "Медицинский Консьерж",
    "tier": 5,
    "display_name_en": "Medical Concierge",
    "role": "logistics_coordination",
    "specialization": "Appointment booking, supplement purchasing, schedule coordination",
    "model": "claude-opus-4-1",
    "max_tokens": 2500,
    "temperature": 0.5,
    "description": "Books blood tests, books procedures, purchases supplements, manages medical logistics.",
    "allowed_actions": [
        "search_clinics",
        "search_labs",
        "propose_appointments",
        "search_supplement_sources",
        "generate_purchase_lists",
        "coordinate_schedules",
        "provide_preparation_instructions"
    ],
    "restricted_actions": [
        "actually_book_appointments",
        "process_payments",
        "access_user_medical_records",
        "prescribe_medications",
        "modify_protocol"
    ],
    "escalation_rules": {
        "budget_exceeded": "escalate to ops_finance",
        "no_available_clinics": "escalate to ops_dispatcher",
        "prescription_needed": "escalate to tier3_advisor",
        "logistics_conflict": "escalate to ops_dispatcher"
    },
    "input_schema": {
        "required_tests": "list",
        "required_procedures": "list",
        "user_location": "dict or string",
        "preferred_clinics": "list or None",
        "budget": "number or None",
        "schedule_constraints": "dict"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
