"""
Tier 6 IT & Infrastructure Agent: Служба Поддержки (Support Service)
Role: Handles user technical issues, device sync, data upload, FAQ.
"""

SYSTEM_PROMPT = """Ты — Служба Поддержки, первая линия защиты против технических проблем пользователя.
Твоя задача — быстро диагностировать и решать проблемы с устройствами, синхронизацией данных
и платформой PLT.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Диагностировать технические проблемы пользователя
2. Решать проблемы синхронизации устройств (Oura Ring, Apple Watch, CGM и т.д.)
3. Помогать с загрузкой данных на платформу
4. Отвечать на часто задаваемые вопросы (FAQ)
5. Эскалировать сложные проблемы на tier6_developer

ПОДДЕРЖИВАЕМЫЕ УСТРОЙСТВА:
- Oura Ring (вне сегодня, физическая активность, ХР)
- Apple Watch (пульс, активность, сон)
- Continuous Glucose Monitor (CGM): FreeStyle Libre, Dexcom
- Garmin watches (ХП, активность)
- Fitbit (активность, сон)
- iPhone Health App (интеграция)
- Android devices (через Google Fit)
- Блютус весы, тонометры

ТИПИЧНЫЕ ПРОБЛЕМЫ И РЕШЕНИЯ:

1. СИНХРОНИЗАЦИЯ НЕ РАБОТАЕТ:
   - Проверить: WiFi/мобильный интернет включен?
   - Проверить: приложение разрешено подключаться?
   - Попробовать: переподключиться к Bluetooth
   - Попробовать: перезагрузить приложение
   - Попробовать: перезагрузить устройство
   - Проверить: версия приложения актуальна?

2. ДАННЫЕ НЕ ЗАГРУЖАЮТСЯ:
   - Убедиться: файл корректного формата (CSV, JSON, etc)
   - Проверить: размер файла не превышает лимит
   - Проверить: у пользователя права на загрузку
   - Попробовать: загрузить по частям

3. ПРОБЛЕМЫ С АУТЕНТИФИКАЦИЕЙ:
   - Предложить сброс пароля
   - Проверить двухфакторную аутентификацию
   - Убедиться, что используется правильный email

ВХОДНЫЕ ДАННЫЕ:
- user_issue: описание проблемы пользователем
- device_status{}: информация о подключенных устройствах и их статусе
- sync_logs[]: логи синхронизации за последние попытки
- common_issues_db: база известных проблем и решений

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. diagnosis:
   - issue_type: "device_sync" | "authentication" | "data_upload" | "performance" | "faq" | "unknown"
   - severity: "critical" | "high" | "medium" | "low"
   - description: что, по-видимому, происходит
   - root_cause: вероятная причина

2. solution_steps[]: пошаговые инструкции для решения
   - step_number
   - action: что делать
   - expected_result: что должно произойти
   - troubleshooting_tips: если не сработало, попробовать это

3. escalation_needed: нужна ли эскалация на developer?

4. faq_match: если это FAQ, ссылка на статью
   - matched_faq_id
   - relevance_score: 0-100

5. devices_affected[]: какие устройства затронуты

6. confidence_score: уверенность в диагнозе (0-100)

ЯЗЫКОВЫЕ ПРАВИЛА:
- Дружелюбный, поддерживающий тон
- НИКОГДА не обвиняй пользователя ("вы сделали что-то не так")
- Объясни техническое так, чтобы поняли все
- Предложи несколько вариантов решения

КРИТИЧЕСКИЕ ПРАВИЛА:
1. Не проси пароли или токены
2. Не давай доступ администратора
3. Если критическая проблема (потеря данных) -> немедленная эскалация
4. Логируй все попытки решения
5. Если проблема повторяется > 3 раз -> эскалация на developer

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Получаешь проблемы -> от пользователя через ops_dispatcher
- Отправляешь на разработчиков -> tier6_developer (критические баги)
- Отправляешь улучшения UX -> tier6_ux (проблемы с интерфейсом)"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "diagnosis": {
            "type": "object",
            "properties": {
                "issue_type": {
                    "type": "string",
                    "enum": ["device_sync", "authentication", "data_upload", "performance", "faq", "unknown"],
                    "description": "Type of issue"
                },
                "severity": {
                    "type": "string",
                    "enum": ["critical", "high", "medium", "low"],
                    "description": "How severe is this issue?"
                },
                "description": {
                    "type": "string",
                    "description": "What appears to be happening"
                },
                "root_cause": {
                    "type": "string",
                    "description": "Likely cause of the problem"
                },
                "affected_systems": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "System or component affected"
                    },
                    "description": "Which parts of the system are affected"
                }
            },
            "required": ["issue_type", "severity", "description"]
        },
        "solution_steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step_number": {
                        "type": "integer",
                        "description": "Sequential step number"
                    },
                    "action": {
                        "type": "string",
                        "description": "What the user should do (simple, clear language)"
                    },
                    "expected_result": {
                        "type": "string",
                        "description": "What should happen after this step"
                    },
                    "time_estimate_minutes": {
                        "type": "integer",
                        "description": "Estimated time for this step"
                    },
                    "technical_details": {
                        "type": "string",
                        "description": "For advanced users, technical explanation"
                    },
                    "troubleshooting_if_fails": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "What to try if step fails"
                        },
                        "description": "Alternative approaches if this step doesn't work"
                    }
                },
                "required": ["step_number", "action", "expected_result"]
            },
            "description": "Step-by-step solution instructions"
        },
        "escalation_needed": {
            "type": "boolean",
            "description": "Does this need escalation to developer?"
        },
        "escalation_reason": {
            "type": "string",
            "description": "If escalation needed, why?"
        },
        "faq_match": {
            "type": "object",
            "properties": {
                "matched": {
                    "type": "boolean",
                    "description": "Is there a matching FAQ?"
                },
                "faq_id": {
                    "type": "string",
                    "description": "ID of matching FAQ article"
                },
                "faq_title": {
                    "type": "string",
                    "description": "Title of FAQ article"
                },
                "relevance_score": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "How relevant is this FAQ (0-100)"
                }
            },
            "description": "Matching FAQ or support article if one exists"
        },
        "devices_affected": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "device_name": {
                        "type": "string",
                        "description": "Name of device (e.g., 'Oura Ring Gen3')"
                    },
                    "device_type": {
                        "type": "string",
                        "description": "Type (ring, watch, scale, etc)"
                    },
                    "is_affected": {
                        "type": "boolean",
                        "description": "Is this device involved in the issue?"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["offline", "syncing", "idle", "error", "unknown"],
                        "description": "Current status of device"
                    }
                },
                "required": ["device_name", "device_type", "is_affected"]
            },
            "description": "Status of connected devices"
        },
        "additional_notes": {
            "type": "string",
            "description": "Any additional important information or context"
        },
        "support_ticket_recommended": {
            "type": "boolean",
            "description": "Should a support ticket be created?"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in this diagnosis and solution (0-100)"
        }
    },
    "required": ["diagnosis", "solution_steps", "escalation_needed", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "it_support",
    "name": "Служба Поддержки",
    "tier": 6,
    "display_name_en": "Support Service",
    "role": "technical_support",
    "specialization": "Device sync troubleshooting, FAQ, user support",
    "model": "claude-opus-4-1",
    "max_tokens": 2000,
    "temperature": 0.5,
    "description": "Handles technical issues, device sync, data upload, answers FAQ.",
    "allowed_actions": [
        "diagnose_issues",
        "provide_troubleshooting_steps",
        "search_faq",
        "check_device_status",
        "view_sync_logs",
        "create_support_tickets"
    ],
    "restricted_actions": [
        "modify_user_data",
        "access_passwords",
        "reset_devices",
        "modify_system_settings",
        "access_other_users_data"
    ],
    "escalation_rules": {
        "critical_data_loss": "escalate to tier6_developer immediately",
        "repeated_issue": "escalate to tier6_developer after 3 failed attempts",
        "security_concern": "escalate to tier6_developer",
        "ui_problem": "escalate to tier6_ux"
    },
    "input_schema": {
        "user_issue": "string",
        "device_status": "dict",
        "sync_logs": "list or None",
        "common_issues_db": "dict"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
