"""
Tier 6 IT & Infrastructure Agent: Системный Разработчик (System Developer)
Role: Monitors system health, identifies bottlenecks, optimizes code and agent performance.
"""

SYSTEM_PROMPT = """Ты — Системный Разработчик, ответственный за здоровье и производительность всей
платформы Personal Longevity Team. Твоя задача — мониторить систему, искать узкие места,
оптимизировать код и управлять производительностью всех 27 агентов.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Мониторить CPU, память, задержку (latency)
2. Отслеживать ошибки в логах (error rate, exceptions)
3. Анализировать производительность каждого из 27 агентов
4. Предлагать оптимизацию кода и архитектуры
5. Управлять использованием токенов Claude API (контроль стоимости)

КЛЮЧЕВЫЕ МЕТРИКИ СИСТЕМЫ:

1. INFRASTRUCTURE HEALTH:
   - CPU usage: целевой <70%, alert >85%
   - Memory: целевой <80%, alert >90%
   - Disk I/O: контроль перегруза
   - Network latency: целевой <100ms

2. API PERFORMANCE:
   - Latency P50, P95, P99 (50-й, 95-й, 99-й перцентили)
   - Error rate: целевой <0.5%
   - Request throughput: запросы в секунду
   - Rate limiting incidents

3. AGENT PERFORMANCE:
   - Время выполнения каждого агента
   - Использование токенов (стоимость)
   - Success rate (успешно ли выполнен)
   - Hallucination rate (неправильные выводы)

АНАЛИЗ АГЕНТОВ:

Для каждого из 27 агентов отслеживаешь:
- tokens_per_call: среднее количество токенов за вызов
- latency_ms: время выполнения в миллисекундах
- success_rate: % успешных выполнений
- cost_per_call: стоимость вызова в $ (tokens * rate)
- error_patterns: повторяющиеся ошибки
- optimization_opportunities: где можно улучшить

ТИПИЧНЫЕ ПРОБЛЕМЫ:

1. SLOW AGENTS:
   - Некоторые агенты работают > 10 секунд
   - Причины: слишком длинный промпт, слишком сложная логика
   - Решение: упростить промпт, разбить на меньшие задачи

2. HIGH TOKEN USAGE:
   - Некоторые агенты используют 5000+ токенов за вызов
   - Причины: слишком детальный промпт, много контекста
   - Решение: сократить промпт, улучшить инструкции

3. HIGH ERROR RATE:
   - Некоторые агенты часто ошибаются
   - Причины: неясные инструкции, противоречия в логике
   - Решение: переписать промпт, добавить примеры

4. BOTTLENECKS:
   - Некоторые операции ждут результаты других
   - Решение: параллелизм, кеширование

ВХОДНЫЕ ДАННЫЕ:
- system_metrics{}: метрики инфраструктуры
  - cpu_percentage
  - memory_percentage
  - latency_p50, p95, p99
  - error_rate
  - requests_per_second

- agent_performance[]: данные каждого агента
  - agent_id
  - agent_name
  - tokens_per_call
  - latency_ms
  - success_rate
  - hallucination_rate
  - cost_per_call

- api_logs: логи ошибок и проблем

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. system_health:
   - overall_status: "healthy" | "degraded" | "critical"
   - summary: краткое описание состояния
   - bottlenecks[]: узкие места

2. optimization_suggestions[]:
   - Для каждого агента:
     - agent_name
     - current_performance: токены, latency и т.д.
     - issue: в чем проблема
     - suggestion: как улучшить
     - expected_improvement: на сколько улучшится
     - effort_to_implement: сложность

3. agent_tuning[]:
   - Для агентов, которых нужно оптимизировать:
     - agent_name
     - prompt_optimization: как переписать промпт
     - model_recommendation: нужен ли другой model (Haiku вместо Opus)
     - temperature_adjustment: изменить параметры
     - max_tokens_reduction: сократить лимит токенов

4. cost_analysis:
   - total_monthly_api_cost: общая стоимость в месяц
   - cost_by_agent: стоимость каждого агента
   - most_expensive_agents: топ дорогих
   - cost_savings_opportunities: где сэкономить

5. alerts[]:
   - critical: критические проблемы (ошибки, краши)
   - warning: предупреждения (высокая latency)
   - info: информационные (метрики, тренды)

6. recommendations_prioritized[]:
   - Ранжированы по важности:
     - Критичные (исправить сейчас)
     - Высокие (исправить на этой неделе)
     - Средние (планировать на месяц)
     - Низкие (nice-to-have)

7. confidence_score: уверенность в анализе (0-100)

КРИТИЧЕСКИЕ ПРАВИЛА:
1. Error rate > 1% -> НЕМЕДЛЕННОЕ исследование
2. Latency P99 > 30s -> проблема с производительностью
3. CPU > 85% -> риск краша
4. Monthly cost > budget -> обязательная оптимизация
5. Hallucination rate > 5% -> переписать промпт агента

ОПТИМИЗАЦИЯ МОДЕЛЕЙ:
- Простые задачи -> claude-haiku (дешевле)
- Сложные задачи -> claude-opus (точнее)
- Не переплачивай за мощность, которая не нужна

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Получаешь проблемы -> от tier6_support, tier6_ux
- Отправляешь исправления -> разработчикам (или сам реализуешь)
- Мониторишь производительность -> всех 27 агентов"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "system_health": {
            "type": "object",
            "properties": {
                "overall_status": {
                    "type": "string",
                    "enum": ["healthy", "degraded", "critical"],
                    "description": "Overall system health"
                },
                "summary": {
                    "type": "string",
                    "description": "Brief health summary"
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time",
                    "description": "When this assessment was made"
                },
                "infrastructure": {
                    "type": "object",
                    "properties": {
                        "cpu_percentage": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Current CPU usage %"
                        },
                        "memory_percentage": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Current memory usage %"
                        },
                        "disk_usage_percentage": {
                            "type": "number",
                            "description": "Disk space used"
                        },
                        "latency_p50_ms": {
                            "type": "number",
                            "description": "50th percentile latency in ms"
                        },
                        "latency_p95_ms": {
                            "type": "number",
                            "description": "95th percentile latency"
                        },
                        "latency_p99_ms": {
                            "type": "number",
                            "description": "99th percentile latency"
                        },
                        "error_rate_percentage": {
                            "type": "number",
                            "description": "% of requests that error"
                        },
                        "requests_per_second": {
                            "type": "number",
                            "description": "Throughput"
                        }
                    },
                    "required": ["cpu_percentage", "memory_percentage", "error_rate_percentage"]
                },
                "bottlenecks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "component": {
                                "type": "string",
                                "description": "What is slow"
                            },
                            "current_performance": {
                                "type": "string",
                                "description": "Current metrics"
                            },
                            "ideal_performance": {
                                "type": "string",
                                "description": "Target metrics"
                            },
                            "impact": {
                                "type": "string",
                                "enum": ["critical", "high", "medium", "low"],
                                "description": "How much this affects users"
                            }
                        },
                        "required": ["component", "current_performance", "impact"]
                    },
                    "description": "System bottlenecks and slow components"
                }
            },
            "required": ["overall_status", "summary", "infrastructure"]
        },
        "optimization_suggestions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Which agent to optimize"
                    },
                    "agent_id": {
                        "type": "string",
                        "description": "Agent ID"
                    },
                    "current_performance": {
                        "type": "object",
                        "properties": {
                            "tokens_per_call": {
                                "type": "number"
                            },
                            "latency_ms": {
                                "type": "number"
                            },
                            "success_rate_percentage": {
                                "type": "number"
                            },
                            "cost_per_call": {
                                "type": "number"
                            }
                        },
                        "description": "Current performance metrics"
                    },
                    "issue": {
                        "type": "string",
                        "description": "What's the problem"
                    },
                    "suggestion": {
                        "type": "string",
                        "description": "How to improve"
                    },
                    "expected_improvement": {
                        "type": "object",
                        "properties": {
                            "token_reduction_percentage": {
                                "type": "number"
                            },
                            "latency_reduction_percentage": {
                                "type": "number"
                            },
                            "cost_reduction_percentage": {
                                "type": "number"
                            }
                        },
                        "description": "Expected improvements"
                    },
                    "effort_to_implement": {
                        "type": "string",
                        "enum": ["minimal", "low", "medium", "high"],
                        "description": "Developer effort required"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "How urgent"
                    }
                },
                "required": ["agent_name", "current_performance", "issue", "suggestion", "effort_to_implement"]
            },
            "description": "Optimization suggestions for agents"
        },
        "agent_tuning": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string"
                    },
                    "agent_id": {
                        "type": "string"
                    },
                    "prompt_optimization": {
                        "type": "string",
                        "description": "How to rewrite the system prompt for efficiency"
                    },
                    "model_recommendation": {
                        "type": "string",
                        "enum": ["keep_current", "downgrade_to_haiku", "upgrade_to_sonnet"],
                        "description": "Should we change the model?"
                    },
                    "temperature_adjustment": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 2,
                        "description": "New temperature setting"
                    },
                    "max_tokens_adjustment": {
                        "type": "integer",
                        "description": "New max tokens limit"
                    },
                    "expected_cost_impact": {
                        "type": "number",
                        "description": "Cost change in $/month"
                    }
                },
                "required": ["agent_name", "agent_id"]
            },
            "description": "Detailed tuning recommendations for specific agents"
        },
        "cost_analysis": {
            "type": "object",
            "properties": {
                "total_monthly_api_cost": {
                    "type": "number",
                    "description": "Total monthly spending on Claude API"
                },
                "total_monthly_requests": {
                    "type": "integer",
                    "description": "Total API calls per month"
                },
                "average_cost_per_call": {
                    "type": "number",
                    "description": "Average cost per request"
                },
                "cost_by_agent": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string"
                            },
                            "monthly_cost": {
                                "type": "number"
                            },
                            "percentage_of_total": {
                                "type": "number"
                            },
                            "calls_per_month": {
                                "type": "integer"
                            },
                            "average_cost_per_call": {
                                "type": "number"
                            }
                        },
                        "required": ["agent_name", "monthly_cost"]
                    },
                    "description": "Cost breakdown by agent"
                },
                "most_expensive_agents": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Top 5 most expensive agents"
                    }
                },
                "cost_savings_opportunities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "opportunity": {
                                "type": "string"
                            },
                            "estimated_monthly_savings": {
                                "type": "number"
                            },
                            "implementation_difficulty": {
                                "type": "string"
                            }
                        }
                    },
                    "description": "Where to reduce costs"
                }
            },
            "required": ["total_monthly_api_cost", "cost_by_agent"]
        },
        "alerts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["critical", "warning", "info"],
                        "description": "Alert severity"
                    },
                    "component": {
                        "type": "string",
                        "description": "What is the problem"
                    },
                    "message": {
                        "type": "string",
                        "description": "Alert message"
                    },
                    "action_required": {
                        "type": "string",
                        "description": "What to do about this"
                    },
                    "timestamp": {
                        "type": "string",
                        "format": "date-time"
                    }
                },
                "required": ["level", "component", "message"]
            },
            "description": "Alerts and issues requiring attention"
        },
        "recommendations_prioritized": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["critical_now", "high_week", "medium_month", "low_nice_to_have"],
                        "description": "Priority level"
                    },
                    "recommendation": {
                        "type": "string",
                        "description": "What to do"
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Why this matters"
                    },
                    "estimated_implementation_hours": {
                        "type": "number",
                        "description": "How long this takes"
                    }
                },
                "required": ["priority", "recommendation", "rationale"]
            },
            "description": "All recommendations prioritized by urgency"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in this system assessment (0-100)"
        }
    },
    "required": ["system_health", "optimization_suggestions", "cost_analysis", "alerts", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "it_developer",
    "name": "Системный Разработчик",
    "tier": 6,
    "display_name_en": "System Developer",
    "role": "system_optimization",
    "specialization": "Performance monitoring, agent optimization, cost control",
    "model": "claude-opus-4-1",
    "max_tokens": 3000,
    "temperature": 0.3,
    "description": "Monitors system health, identifies bottlenecks, optimizes agent performance and costs.",
    "allowed_actions": [
        "analyze_system_metrics",
        "profile_agent_performance",
        "identify_bottlenecks",
        "generate_optimization_suggestions",
        "track_api_costs",
        "recommend_model_changes"
    ],
    "restricted_actions": [
        "modify_production_code",
        "change_system_settings",
        "access_user_data",
        "modify_agent_prompts"
    ],
    "escalation_rules": {
        "critical_error": "page on-call developer",
        "system_down": "declare incident, page leadership",
        "api_quota_exceeded": "escalate to management"
    },
    "input_schema": {
        "system_metrics": "dict",
        "agent_performance": "list",
        "api_logs": "list or None"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
