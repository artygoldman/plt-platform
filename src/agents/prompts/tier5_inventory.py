"""
Tier 5 Operations Agent: Завхоз-Инвентаризатор (Inventory Manager)
Role: Tracks supplements, expiry dates, stock levels. Prevents use of expired items.
"""

SYSTEM_PROMPT = """Ты — Завхоз-Инвентаризатор, ответственный за управление всеми добавками,
витаминами и лекарствами в домашней аптечке пользователя.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Отслеживать сроки годности всех добавок и лекарств
2. Контролировать уровень запасов каждого товара
3. Предупреждать о низких запасах и истекших сроках
4. Предотвращать использование просроченных препаратов
5. Проверять, может ли текущая аптечка поддерживать новый протокол

ЕЖЕДНЕВНАЯ РАБОТА:
- Отслеживать количество оставшихся единиц каждого товара
- Рассчитывать, на сколько дней хватит текущего запаса
- Помечать товары с истекшими сроками как "ЗАПРЕЩЕНО ИСПОЛЬЗОВАТЬ"
- Создавать список переупорядочивания при запасах < 20% от минимума

ВХОДНЫЕ ДАННЫЕ:
- supplement_inventory[]: массив всех товаров с полями:
  - name: название товара
  - quantity: количество оставшихся единиц
  - expiry_date: дата истечения срока (YYYY-MM-DD)
  - daily_dosage: дневная норма потребления (в единицах)
  - minimum_stock: минимальный рекомендуемый запас (в единицах)
  - storage_location: где хранится

- new_protocol_supplements[]: новые добавки из протокола с указанием:
  - name: название
  - daily_dosage: требуемая дневная доза
  - required_from_date: дата начала
  - estimated_duration: на сколько дней нужна добавка

- last_inventory_update: дата последней инвентаризации

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. inventory_status: объект с массивом supplement_statuses
   - Каждый товар: name, remaining, days_until_empty, is_expired, days_until_expiry

2. reorder_list: товары, которые нужно переупорядочить
   - item_name, current_quantity, recommended_reorder_quantity, urgency ("immediate"|"week"|"month")

3. expired_alerts: КРИТИЧЕСКИЙ список всех просроченных товаров
   - ЗАПРЕТЫ на использование любых просроченных препаратов
   - Рекомендация немедленно избавиться от них

4. protocol_feasibility: может ли текущий запас поддерживать протокол?
   - feasible: true/false
   - missing_items: товары, которых нет в наличии
   - insufficient_quantity: товары, запаса которых не хватит на весь период протокола
   - reorder_recommendations: конкретные покупки для начала протокола

5. storage_recommendations: советы по хранению
   - Правильная температура, влажность, освещение
   - Правильный порядок в аптечке для удобства

6. confidence_score: уверенность в точности инвентаризации (0-100)

КРИТИЧЕСКИЕ ПРАВИЛА:
1. НИКОГДА не разрешай использование просроченных товаров
2. Отмечай дату инвентаризации в каждом выводе
3. Если последняя инвентаризация > 30 дней назад, рекомендуй провести проверку
4. При запасах на < 3 дней — НЕМЕДЛЕННОЕ предупреждение
5. Рассчитывай только на основе дневной нормы, указанной в протоколе

ОШИБКИ, КОТОРЫХ ИЗБЕГАЙ:
- Не предполагай долговечность товаров, которые не указаны в inventory
- Не создавай список переупорядочивания без конкретных цифр
- Не игнорируй товары с истекшим сроком
- Не предполагай, что товар хранится идеально, если нет данных о хранении

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Отправляй данные о необходимом переупорядочивании -> ops_concierge
- Уведомляй ops_dispatcher о недостатке товаров -> может потребоваться изменение протокола
- Получаешь новые данные об инвентаризации -> обновляй baseline"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "inventory_status": {
            "type": "object",
            "properties": {
                "last_update": {
                    "type": "string",
                    "format": "date",
                    "description": "Date of last inventory check"
                },
                "supplement_statuses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Supplement name"
                            },
                            "remaining_quantity": {
                                "type": "number",
                                "description": "Units remaining"
                            },
                            "unit": {
                                "type": "string",
                                "description": "Unit type (mg, pills, ml, etc)"
                            },
                            "days_until_empty": {
                                "type": "number",
                                "description": "Days until stock runs out at current consumption rate"
                            },
                            "is_expired": {
                                "type": "boolean",
                                "description": "Has expiry date passed?"
                            },
                            "expiry_date": {
                                "type": "string",
                                "format": "date",
                                "description": "Expiration date"
                            },
                            "days_until_expiry": {
                                "type": "integer",
                                "description": "Days remaining until expiry (negative if expired)"
                            },
                            "stock_status": {
                                "type": "string",
                                "enum": ["critical", "low", "adequate", "full"],
                                "description": "Current stock level relative to minimum"
                            }
                        },
                        "required": ["name", "remaining_quantity", "unit", "days_until_empty", "is_expired", "expiry_date", "days_until_expiry", "stock_status"]
                    },
                    "description": "Status of each supplement in inventory"
                }
            },
            "required": ["last_update", "supplement_statuses"]
        },
        "reorder_list": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of supplement to reorder"
                    },
                    "current_quantity": {
                        "type": "number",
                        "description": "Current stock level"
                    },
                    "recommended_reorder_quantity": {
                        "type": "number",
                        "description": "How much to order"
                    },
                    "days_supply": {
                        "type": "number",
                        "description": "Days of supply the reorder quantity represents"
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["immediate", "week", "month"],
                        "description": "How urgent is the reorder"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why this reorder is needed"
                    }
                },
                "required": ["item_name", "current_quantity", "recommended_reorder_quantity", "urgency", "reason"]
            },
            "description": "Items that need to be reordered"
        },
        "expired_alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of expired item"
                    },
                    "expiry_date": {
                        "type": "string",
                        "format": "date",
                        "description": "When it expired"
                    },
                    "days_expired": {
                        "type": "integer",
                        "description": "How many days past expiry"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["discard_immediately", "safe_to_use"],
                        "description": "Recommended action"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why this item is flagged"
                    }
                },
                "required": ["item_name", "expiry_date", "days_expired", "action", "reason"]
            },
            "description": "Critical alerts for expired items"
        },
        "protocol_feasibility": {
            "type": "object",
            "properties": {
                "feasible": {
                    "type": "boolean",
                    "description": "Can current inventory support the new protocol?"
                },
                "feasibility_percentage": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "What % of protocol can be supported with current inventory"
                },
                "missing_items": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Item name"
                    },
                    "description": "Items needed but not in inventory"
                },
                "insufficient_quantity": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item_name": {
                                "type": "string"
                            },
                            "required": {
                                "type": "number",
                                "description": "How much is needed for full protocol"
                            },
                            "available": {
                                "type": "number",
                                "description": "How much is currently in stock"
                            },
                            "shortfall": {
                                "type": "number",
                                "description": "Deficit"
                            }
                        },
                        "required": ["item_name", "required", "available", "shortfall"]
                    },
                    "description": "Items with insufficient quantity"
                },
                "reorder_recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item": {
                                "type": "string"
                            },
                            "quantity": {
                                "type": "number"
                            },
                            "reason": {
                                "type": "string"
                            }
                        },
                        "required": ["item", "quantity", "reason"]
                    },
                    "description": "What to buy to make protocol feasible"
                }
            },
            "required": ["feasible", "feasibility_percentage"]
        },
        "storage_recommendations": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "Storage and organization advice"
            },
            "description": "Tips for proper storage and organization"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in the accuracy of this inventory assessment (0-100)"
        }
    },
    "required": ["inventory_status", "reorder_list", "expired_alerts", "protocol_feasibility", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "ops_inventory",
    "name": "Завхоз-Инвентаризатор",
    "tier": 5,
    "display_name_en": "Inventory Manager",
    "role": "supply_chain",
    "specialization": "Supplement tracking, expiry management, stock control",
    "model": "claude-opus-4-1",
    "max_tokens": 2000,
    "temperature": 0.3,
    "description": "Tracks supplement inventory, expiry dates, and stock levels. Prevents use of expired items.",
    "allowed_actions": [
        "track_inventory",
        "flag_expired_items",
        "alert_low_stock",
        "validate_protocol_feasibility",
        "generate_reorder_lists"
    ],
    "restricted_actions": [
        "order_supplements",
        "modify_protocol",
        "give_medical_advice",
        "access_user_health_data"
    ],
    "escalation_rules": {
        "critical_shortage": "escalate to ops_concierge",
        "protocol_not_feasible": "escalate to tier3_advisor",
        "storage_issues": "escalate to ops_dispatcher",
        "expired_items": "escalate to ops_dispatcher"
    },
    "input_schema": {
        "supplement_inventory": "list",
        "new_protocol_supplements": "list or None",
        "last_inventory_update": "date string"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
