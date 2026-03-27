"""
Tier 5 Operations Agent: Финансовый Контроллер (Finance Controller)
Role: Optimizes costs, tracks spending, calculates ROI per item.
"""

SYSTEM_PROMPT = """Ты — Финансовый Контроллер, ответственный за финансовую оптимизацию всего процесса
долголетия пользователя. Твоя задача — найти лучшие цены, отследить затраты и показать,
сколько денег платит пользователь за каждый дополнительный день жизни.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Находить самые дешевые варианты клиник, лабораторий и поставщиков добавок
2. Отслеживать ежемесячные расходы на здоровье
3. Рассчитывать cost per life-day (стоимость каждого дополнительного дня жизни)
4. Оптимизировать выделение бюджета между тестами, процедурами и добавками
5. Идентифицировать лучший ROI (return on investment) для каждого компонента

ОСНОВНЫЕ ПОКАЗАТЕЛИ:

1. COST PER LIFE-DAY:
   Рассчитывается как: (годовая стоимость) / (количество добавленных дней в год)
   Например: добавка стоит 100$ в год и добавляет 50 дней жизни
   → 100 / 50 = 2$ за день жизни

2. MONTHLY HEALTH BUDGET REPORT:
   - Всего потрачено в месяц
   - По категориям: тесты, процедуры, добавки, консультации
   - Сравнение с бюджетом (превышение или экономия)
   - Тренд за 3-6 месяцев

3. COST OPTIMIZATION:
   - Предложи дешевые альтернативы для дорогостоящих анализов
   - Найди более дешевые источники добавок без потери качества
   - Рекомендуй комбо-пакеты от клиник (часто дешевле, чем по отдельности)

4. ROI RANKING:
   Ранжировать все компоненты протокола по эффективности затрат:
   - Лучший ROI сверху (те, что добавляют много дней за мало денег)
   - Худший ROI внизу (дорогие, но малый эффект)

ВХОДНЫЕ ДАННЫЕ:
- current_protocol: текущий одобренный протокол
  - Каждый компонент должен иметь эстимейт эффекта на Longevity Score

- clinic_options[]: варианты клиник для каждого теста
  - name
  - test_list (какие тесты делают)
  - price (за тест)
  - rating
  - travel_time

- supplement_prices[]: цены на добавки из разных источников
  - supplement_name
  - supplier_options[] (аптека, маркетплейс и т.д. с ценами)
  - quality_notes
  - bioavailability (степень усваиваемости)

- monthly_budget: сколько денег в месяц может потратить пользователь

- spending_history[]: история расходов за последние 3-6 месяцев
  - date
  - category: "test" | "procedure" | "supplement" | "consultation" | "device"
  - item_name
  - amount
  - category_notes

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. budget_report: детальный отчет о бюджете
   - total_monthly: сколько планируется потратить в месяц
   - by_category: расходы по категориям
   - vs_budget: сравнение с лимитом пользователя
   - trend: тренд за 3-6 месяцев
   - monthly_forecast_next_6_months: прогноз затрат

2. cost_optimization[]: список возможностей сэкономить
   - current_item: что сейчас используется
   - current_cost: текущая стоимость
   - suggested_alternative: что предлагаешь
   - alternative_cost: новая стоимость
   - savings_per_month: экономия в месяц
   - quality_impact: есть ли потеря качества?
   - switch_difficulty: "easy" | "medium" | "hard"

3. roi_per_item[]: рейтинг компонентов по эффективности затрат
   - Каждый компонент:
     - name: название компонента
     - annual_cost: годовая стоимость
     - estimated_longevity_gain_days: сколько дней добавляет
     - cost_per_life_day: стоимость дня жизни
     - roi_percentage: процент отдачи (как много жизни за деньги)
     - rank: порядковый номер (1 = лучший ROI)
     - recommendation: стоит ли включать в основной протокол

4. savings_recommendations[]: стратегические советы по экономии
   - Комбо-пакеты от клиник
   - Оптовые закупки добавок
   - Сезонные скидки
   - Программы лояльности
   - Дженерики вместо брендов

5. annual_forecast: прогноз на год
   - total_annual_cost: общая стоимость в год
   - cost_by_category: расходы по категориям за год
   - estimated_total_longevity_gain: сколько дней жизни можно добавить за год
   - cost_per_added_year: стоимость дополнительного года жизни
   - sustainability_analysis: устойчив ли этот бюджет?

6. budget_prioritization: как распределить бюджет, если нужно сокращать
   - Если бюджет < сумма всех компонентов, предложи приоритизацию
   - Какие компоненты cut, какие keep, какие downgrade

7. confidence_score: уверенность в анализе (0-100)

КРИТИЧЕСКИЕ ПРАВИЛА:
1. НИКОГДА не предлагай дешевые, но неэффективные добавки
2. Учитывай bioavailability (некоторые дешевые аналоги плохо усваиваются)
3. Проверяй подлинность источников (особенно для дорогих добавок)
4. Рассчитывай ROI только на основе данных Tier 2-3 о эффективности
5. Не забывай про доставку и таможню (если заказываешь из-за границы)
6. Обновляй price_history для отслеживания инфляции

МАТЕМАТИКА ROI:
ROI% = (Benefit / Cost) * 100
Где Benefit = количество добавленных дней * цена жизни-дня (условно: 100$)
Cost = годовая стоимость компонента

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Получаешь список необходимых добавок -> от ops_concierge
- Отправляешь лучшие цены -> ops_concierge для закупки
- Уведомляешь ops_dispatcher -> если бюджет превышен
- Получаешь данные о эффективности -> от Tier 2-3"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "budget_report": {
            "type": "object",
            "properties": {
                "reporting_period": {
                    "type": "string",
                    "description": "Period covered by this report"
                },
                "total_monthly": {
                    "type": "number",
                    "description": "Total planned monthly spending"
                },
                "total_annual": {
                    "type": "number",
                    "description": "Projected annual spending"
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code"
                },
                "by_category": {
                    "type": "object",
                    "properties": {
                        "tests": {
                            "type": "number",
                            "description": "Blood tests, diagnostics"
                        },
                        "procedures": {
                            "type": "number",
                            "description": "Medical procedures"
                        },
                        "supplements": {
                            "type": "number",
                            "description": "Vitamins, supplements, medications"
                        },
                        "consultations": {
                            "type": "number",
                            "description": "Doctor/specialist consultations"
                        },
                        "devices": {
                            "type": "number",
                            "description": "Tracking devices (Oura, Apple Watch, etc)"
                        }
                    },
                    "description": "Spending breakdown by category"
                },
                "vs_budget": {
                    "type": "object",
                    "properties": {
                        "user_budget": {
                            "type": "number",
                            "description": "User's monthly budget limit"
                        },
                        "total_planned_monthly": {
                            "type": "number",
                            "description": "Total planned spending this month"
                        },
                        "surplus_or_deficit": {
                            "type": "number",
                            "description": "Positive = under budget, negative = over"
                        },
                        "percentage_of_budget": {
                            "type": "number",
                            "description": "What % of budget this uses (0-100+)"
                        },
                        "within_budget": {
                            "type": "boolean",
                            "description": "Is the plan within budget?"
                        }
                    },
                    "required": ["user_budget", "total_planned_monthly", "within_budget"]
                },
                "trend": {
                    "type": "object",
                    "properties": {
                        "period": {
                            "type": "string",
                            "enum": ["3_months", "6_months"],
                            "description": "Period analyzed"
                        },
                        "average_monthly": {
                            "type": "number",
                            "description": "Average monthly spending over period"
                        },
                        "trend_direction": {
                            "type": "string",
                            "enum": ["increasing", "stable", "decreasing"],
                            "description": "Spending trajectory"
                        },
                        "trend_percentage": {
                            "type": "number",
                            "description": "% change from first to last month"
                        }
                    },
                    "description": "Historical spending trend"
                },
                "monthly_forecast_next_6_months": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "month": {
                                "type": "string",
                                "description": "Month name"
                            },
                            "estimated_cost": {
                                "type": "number"
                            },
                            "reason": {
                                "type": "string",
                                "description": "Why this amount (e.g., quarterly tests due)"
                            }
                        },
                        "required": ["month", "estimated_cost"]
                    },
                    "description": "6-month spending forecast"
                }
            },
            "required": ["reporting_period", "total_monthly", "by_category", "vs_budget"]
        },
        "cost_optimization": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Type of expense"
                    },
                    "current_item": {
                        "type": "string",
                        "description": "What user is currently using/paying"
                    },
                    "current_cost": {
                        "type": "number",
                        "description": "Current monthly/annual cost"
                    },
                    "suggested_alternative": {
                        "type": "string",
                        "description": "What to switch to"
                    },
                    "alternative_cost": {
                        "type": "number",
                        "description": "Cost of alternative"
                    },
                    "monthly_savings": {
                        "type": "number",
                        "description": "Monthly savings amount"
                    },
                    "annual_savings": {
                        "type": "number",
                        "description": "Annual savings"
                    },
                    "quality_impact": {
                        "type": "string",
                        "enum": ["none", "minimal", "moderate", "significant"],
                        "description": "Any loss in quality or effectiveness?"
                    },
                    "switch_difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"],
                        "description": "How hard to implement"
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Why this is a good alternative"
                    }
                },
                "required": ["current_item", "current_cost", "suggested_alternative", "alternative_cost", "annual_savings", "switch_difficulty", "quality_impact"]
            },
            "description": "Cost optimization opportunities"
        },
        "roi_per_item": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of component (test, supplement, procedure)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Category type"
                    },
                    "annual_cost": {
                        "type": "number",
                        "description": "Cost per year"
                    },
                    "estimated_longevity_gain_days": {
                        "type": "number",
                        "description": "Estimated additional days of life per year"
                    },
                    "estimated_longevity_gain_years": {
                        "type": "number",
                        "description": "Estimated additional years of life from this component"
                    },
                    "cost_per_life_day": {
                        "type": "number",
                        "description": "Annual cost / added days"
                    },
                    "roi_percentage": {
                        "type": "number",
                        "description": "Return on investment as percentage"
                    },
                    "rank": {
                        "type": "integer",
                        "description": "Ranking by ROI (1 = best)"
                    },
                    "recommendation": {
                        "type": "string",
                        "enum": ["essential", "recommended", "optional", "low_priority"],
                        "description": "Whether to include in protocol"
                    },
                    "confidence": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 100,
                        "description": "Confidence in ROI calculation"
                    }
                },
                "required": ["name", "annual_cost", "estimated_longevity_gain_days", "cost_per_life_day", "roi_percentage", "rank", "recommendation"]
            },
            "description": "Cost-effectiveness ranking of all protocol components"
        },
        "savings_recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "description": "Name of savings strategy"
                    },
                    "description": {
                        "type": "string",
                        "description": "How this works"
                    },
                    "estimated_savings": {
                        "type": "number",
                        "description": "Estimated annual savings"
                    },
                    "implementation_effort": {
                        "type": "string",
                        "enum": ["minimal", "low", "medium", "high"],
                        "description": "Effort required"
                    },
                    "applicable_items": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "What items this applies to"
                        }
                    }
                },
                "required": ["strategy", "description", "estimated_savings", "implementation_effort"]
            },
            "description": "Strategic recommendations for overall cost reduction"
        },
        "annual_forecast": {
            "type": "object",
            "properties": {
                "total_annual_cost": {
                    "type": "number",
                    "description": "Total annual health spending"
                },
                "cost_by_category": {
                    "type": "object",
                    "description": "Breakdown by category"
                },
                "estimated_total_longevity_gain_days": {
                    "type": "number",
                    "description": "Total additional life-days from all components"
                },
                "estimated_total_longevity_gain_years": {
                    "type": "number",
                    "description": "Total additional life-years"
                },
                "cost_per_added_year": {
                    "type": "number",
                    "description": "Total annual cost / added years of life"
                },
                "cost_per_added_day": {
                    "type": "number",
                    "description": "Total annual cost / added days of life"
                },
                "sustainability_analysis": {
                    "type": "string",
                    "description": "Can user sustain this budget long-term? Any concerns?"
                }
            },
            "required": ["total_annual_cost", "estimated_total_longevity_gain_days", "cost_per_added_year"]
        },
        "budget_prioritization": {
            "type": "object",
            "properties": {
                "needs_prioritization": {
                    "type": "boolean",
                    "description": "Does budget need to be cut?"
                },
                "target_budget": {
                    "type": "number",
                    "description": "Revised budget target if cutting"
                },
                "keep_items": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Essential items to keep"
                    },
                    "description": "Must-have components"
                },
                "downgrade_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "item": {
                                "type": "string"
                            },
                            "downgrade_option": {
                                "type": "string",
                                "description": "What to downgrade to"
                            },
                            "savings": {
                                "type": "number"
                            }
                        },
                        "required": ["item", "downgrade_option"]
                    },
                    "description": "Items to scale back"
                },
                "cut_items": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Items to cut if necessary"
                    },
                    "description": "Low-priority items to remove"
                }
            },
            "description": "Budget prioritization if cuts are needed"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in this financial analysis (0-100)"
        }
    },
    "required": ["budget_report", "roi_per_item", "annual_forecast", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "ops_finance",
    "name": "Финансовый Контроллер",
    "tier": 5,
    "display_name_en": "Finance Controller",
    "role": "financial_optimization",
    "specialization": "Cost analysis, ROI calculation, budget optimization",
    "model": "claude-opus-4-1",
    "max_tokens": 2500,
    "temperature": 0.3,
    "description": "Optimizes health spending, calculates cost-per-life-day, tracks budget.",
    "allowed_actions": [
        "analyze_pricing",
        "calculate_roi",
        "forecast_spending",
        "identify_savings_opportunities",
        "track_spending_history",
        "compare_alternatives"
    ],
    "restricted_actions": [
        "make_purchases",
        "access_payment_systems",
        "modify_protocol",
        "give_medical_advice"
    ],
    "escalation_rules": {
        "budget_exceeded": "escalate to ops_dispatcher",
        "unfeasible_protocol": "escalate to tier3_advisor",
        "major_cost_concern": "escalate to operations_lead"
    },
    "input_schema": {
        "current_protocol": "dict",
        "clinic_options": "list",
        "supplement_prices": "list",
        "monthly_budget": "number or None",
        "spending_history": "list"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
