"""
Tier 6 IT & Infrastructure Agent: QA-Тестировщик (QA Tester)
Role: Validates agent outputs, checks for hallucinations and inconsistencies.
"""

SYSTEM_PROMPT = """Ты — QA-Тестировщик, ответственный за качество всех решений, которые генерируют 27 агентов
в системе Personal Longevity Team. Твоя задача — проверять каждый вывод на ошибки,
галлюцинации, противоречия и логические несоответствия.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Проверять выходные данные всех агентов на корректность
2. Обнаруживать галлюцинации (выдумки, неподтвержденные факты)
3. Находить противоречия между решениями разных агентов
4. Проверять логику и математику (ROI, расчеты и т.д.)
5. Валидировать протоколы на реалистичность и безопасность

ТИПЫ ПРОВЕРОК:

1. HALLUCINATION DETECTION (обнаружение галлюцинаций):
   Агент может выдумать:
   - "Лучшая клиника в городе" (не проверил)
   - "Этот препарат добавляет 100 дней жизни" (нет данных)
   - "API доступен, все работает" (не проверил)

   Как ловить:
   - Проверить, есть ли источник информации
   - Есть ли цитирование базы данных/конфига
   - Реалистично ли утверждение?

2. CONSISTENCY CHECKS (проверка согласованности):
   - Агент A говорит "нужна добавка X", агент B говорит "добавка X противопоказана"
   - Агент A заказал 100 пилюль на год, агент B говорит "на 6 месяцев хватит"
   - Цена тестя у разных агентов отличается на 500%

   Как проверять:
   - Сравнить выводы всех агентов за сеанс
   - Найти противоречия
   - Определить, какой агент прав

3. SANITY CHECKS (проверка логики):
   - Пациент 25 лет -> предлагаем анализ гормонов каждый месяц (слишком часто)
   - Пациент весит 50 кг, рост 140 см -> предлагаем добавку по 5g в день (слишком много)
   - Бюджет 100$/месяц -> заказываем процедуры на 500$ (нереально)

   Как проверять:
   - Применить здравый смысл
   - Проверить медицинские рекомендации
   - Проверить математику

4. PROTOCOL VALIDATION (валидация протокола):
   - Является ли протокол безопасным?
   - Есть ли опасные комбинации добавок?
   - Рекомендации соответствуют профилю пользователя?

ВХОДНЫЕ ДАННЫЕ:
- agent_outputs[]: все решения всех агентов за сеанс
  - agent_id
  - agent_name
  - output_json: полный выход агента
  - confidence_score: уверенность агента

- protocol_draft: черновик итогового протокола
  - supplements: список добавок
  - tests: список анализов
  - procedures: процедуры
  - frequency: как часто

- known_constraints: что мы знаем об истинности
  - medical_facts: проверенные медицинские факты
  - price_list: известные цены
  - clinic_database: проверенные клиники

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. qa_report:
   - overall_quality_score: 0-100
   - status: "approved" | "needs_review" | "rejected"
   - summary: общее резюме

2. hallucination_checks[]:
   - Каждый потенциальный выдумка:
     - claim: что агент сказал
     - source_verification: можно ли это проверить?
     - verification_status: "verified" | "unverifiable" | "false"
     - evidence: если верно, приведи доказательство

3. consistency_checks[]:
   - Когда два агента противоречат друг другу:
     - agent_a_id, agent_a_claim
     - agent_b_id, agent_b_claim
     - conflict_description: в чем противоречие
     - resolution: какой агент прав и почему
     - severity: "critical" | "high" | "medium" | "low"

4. sanity_flags[]:
   - Когда что-то кажется нереалистичным:
     - flag_description: что не так
     - reason: почему это странно
     - severity: критичность
     - correction: что должно быть вместо этого

5. protocol_validation:
   - safety_check_passed: безопасен ли протокол?
   - dangerous_combinations[]: опасные комбинации добавок
   - frequency_appropriateness: подходит ли частота анализов?
   - budget_feasibility: реально ли осуществить с бюджетом?
   - compliance_with_medical_guidelines: соответствует ли мед.стандартам?

6. recommendations:
   - Что нужно переделать перед одобрением
   - Какие агенты дали неправильные ответы
   - Как исправить

7. confidence_score: уверенность в QA (0-100)

КРИТИЧЕСКИЕ ПРАВИЛА:
1. Если hallucination -> требуется переделать выход агента
2. Если critical contradiction -> требуется переделать оба выхода
3. Если safety concern -> REJECT протокол, эскалировать на Tier 2
4. Если математическая ошибка -> требует исправления
5. Не доверяй агентам, которые показывают low confidence

КОГДА ОДОБРЯТЬ:
- Нет галлюцинаций (или только minor, clearly marked)
- Нет критических противоречий
- Математика правильная
- Протокол безопасен
- Соответствует профилю пользователя

КОГДА ТРЕБОВАТЬ ПЕРЕДЕЛКУ:
- Halllucination rate > 5%
- Есть critical contradictions
- Математические ошибки
- Небезопасный протокол
- Нереальные рекомендации

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Получаешь выходы -> от всех 27 агентов
- Отправляешь feedback -> агентам для переделки
- Эскалируешь на Tier 2-3 -> если safety concern
- Логируешь все проблемы -> для анализа качества"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "qa_report": {
            "type": "object",
            "properties": {
                "overall_quality_score": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Overall quality of this round of agent outputs"
                },
                "status": {
                    "type": "string",
                    "enum": ["approved", "needs_review", "rejected"],
                    "description": "Can this be approved or needs work?"
                },
                "summary": {
                    "type": "string",
                    "description": "Executive summary of QA findings"
                },
                "assessment_timestamp": {
                    "type": "string",
                    "format": "date-time",
                    "description": "When this assessment was made"
                },
                "total_agents_evaluated": {
                    "type": "integer",
                    "description": "How many agents were checked"
                }
            },
            "required": ["overall_quality_score", "status", "summary"]
        },
        "hallucination_checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Which agent made the claim"
                    },
                    "agent_id": {
                        "type": "string"
                    },
                    "claim": {
                        "type": "string",
                        "description": "What the agent claimed"
                    },
                    "claim_type": {
                        "type": "string",
                        "enum": ["factual", "numerical", "medical", "pricing", "clinic_info", "other"],
                        "description": "What kind of claim is this?"
                    },
                    "source_verification_possible": {
                        "type": "boolean",
                        "description": "Can this claim be verified?"
                    },
                    "verification_status": {
                        "type": "string",
                        "enum": ["verified", "unverifiable", "likely_false", "false"],
                        "description": "Is the claim true?"
                    },
                    "evidence": {
                        "type": "string",
                        "description": "If verified, what is the evidence? If false, what is correct?"
                    },
                    "confidence": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 100,
                        "description": "Confidence in this verification"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "How bad is this if wrong?"
                    },
                    "action_required": {
                        "type": "string",
                        "enum": ["reject_output", "request_source", "request_correction", "approve"],
                        "description": "What to do"
                    }
                },
                "required": ["agent_name", "claim", "verification_status", "severity"]
            },
            "description": "Hallucination detection results"
        },
        "consistency_checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "agent_a_id": {
                        "type": "string",
                        "description": "First agent involved"
                    },
                    "agent_a_name": {
                        "type": "string"
                    },
                    "agent_a_claim": {
                        "type": "string",
                        "description": "What agent A said"
                    },
                    "agent_b_id": {
                        "type": "string",
                        "description": "Second agent involved"
                    },
                    "agent_b_name": {
                        "type": "string"
                    },
                    "agent_b_claim": {
                        "type": "string",
                        "description": "What agent B said"
                    },
                    "conflict_type": {
                        "type": "string",
                        "enum": ["direct_contradiction", "quantitative_mismatch", "logical_conflict"],
                        "description": "Type of disagreement"
                    },
                    "conflict_description": {
                        "type": "string",
                        "description": "What's the disagreement"
                    },
                    "who_is_correct": {
                        "type": "string",
                        "enum": ["agent_a", "agent_b", "both_wrong", "both_valid"],
                        "description": "Which agent is right?"
                    },
                    "resolution": {
                        "type": "string",
                        "description": "What's the truth and why"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "How serious is this disagreement?"
                    },
                    "impact_on_protocol": {
                        "type": "string",
                        "description": "How does this affect the final protocol?"
                    }
                },
                "required": ["agent_a_id", "agent_b_id", "conflict_description", "severity"]
            },
            "description": "Consistency checks between different agents"
        },
        "sanity_flags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "flag_type": {
                        "type": "string",
                        "enum": ["medical_concern", "dosage_issue", "frequency_issue", "cost_issue", "timeline_issue", "logical_issue"],
                        "description": "Type of sanity check"
                    },
                    "flag_description": {
                        "type": "string",
                        "description": "What looks wrong"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why this is concerning"
                    },
                    "expected_norm": {
                        "type": "string",
                        "description": "What would be normal"
                    },
                    "actual_value": {
                        "type": "string",
                        "description": "What was recommended"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "How serious"
                    },
                    "suggested_correction": {
                        "type": "string",
                        "description": "How to fix this"
                    }
                },
                "required": ["flag_type", "flag_description", "severity"]
            },
            "description": "Sanity check failures (illogical recommendations)"
        },
        "protocol_validation": {
            "type": "object",
            "properties": {
                "safety_check_passed": {
                    "type": "boolean",
                    "description": "Is the protocol safe?"
                },
                "safety_issues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "issue": {
                                "type": "string",
                                "description": "What's the safety concern"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["critical", "high", "medium", "low"]
                            },
                            "recommendation": {
                                "type": "string"
                            }
                        },
                        "required": ["issue", "severity"]
                    },
                    "description": "Any safety concerns with the protocol"
                },
                "dangerous_combinations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "combination": {
                                "type": "string",
                                "description": "Which items conflict"
                            },
                            "interaction_type": {
                                "type": "string",
                                "description": "What kind of interaction"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["critical", "high", "medium", "low"]
                            },
                            "medical_reference": {
                                "type": "string",
                                "description": "Source of this information"
                            }
                        }
                    },
                    "description": "Dangerous supplement/medication combinations"
                },
                "frequency_appropriateness": {
                    "type": "boolean",
                    "description": "Is the testing frequency appropriate?"
                },
                "frequency_notes": {
                    "type": "string",
                    "description": "Notes on testing frequency"
                },
                "budget_feasibility": {
                    "type": "boolean",
                    "description": "Can user afford this protocol?"
                },
                "budget_notes": {
                    "type": "string",
                    "description": "Financial feasibility analysis"
                },
                "compliance_with_medical_guidelines": {
                    "type": "boolean",
                    "description": "Does protocol follow medical standards?"
                },
                "guideline_notes": {
                    "type": "string",
                    "description": "How well does it align with medical guidelines"
                }
            },
            "required": ["safety_check_passed", "frequency_appropriateness", "budget_feasibility"]
        },
        "quality_metrics": {
            "type": "object",
            "properties": {
                "hallucination_rate_percentage": {
                    "type": "number",
                    "description": "% of claims that were hallucinations"
                },
                "contradiction_count": {
                    "type": "integer",
                    "description": "Number of contradictions found"
                },
                "sanity_flag_count": {
                    "type": "integer",
                    "description": "Number of sanity check failures"
                },
                "average_agent_confidence": {
                    "type": "number",
                    "description": "Average confidence score of all agents"
                }
            },
            "description": "Quantitative quality metrics"
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "recommendation": {
                        "type": "string",
                        "description": "What needs to be fixed"
                    },
                    "affected_agents": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Agent IDs involved"
                        }
                    },
                    "action_type": {
                        "type": "string",
                        "enum": ["reject_rerun", "request_source", "request_clarification", "auto_fix"],
                        "description": "What action to take"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "Urgency"
                    }
                },
                "required": ["recommendation", "action_type", "priority"]
            },
            "description": "Recommendations for fixes"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in this QA assessment (0-100)"
        }
    },
    "required": ["qa_report", "hallucination_checks", "consistency_checks", "sanity_flags", "protocol_validation", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "it_qa",
    "name": "QA-Тестировщик",
    "tier": 6,
    "display_name_en": "QA Tester",
    "role": "quality_assurance",
    "specialization": "Output validation, hallucination detection, consistency checking",
    "model": "claude-opus-4-1",
    "max_tokens": 3000,
    "temperature": 0.3,
    "description": "Validates agent outputs, detects hallucinations, checks consistency and safety.",
    "allowed_actions": [
        "validate_agent_outputs",
        "detect_hallucinations",
        "check_consistency",
        "validate_protocols",
        "check_mathematical_accuracy",
        "verify_medical_safety"
    ],
    "restricted_actions": [
        "modify_agent_outputs",
        "access_user_data",
        "make_medical_decisions",
        "override_safety_checks"
    ],
    "escalation_rules": {
        "hallucination_detected": "request agent re-run",
        "critical_inconsistency": "escalate to Tier 3 for review",
        "safety_concern": "immediately escalate to Tier 2/3",
        "repeated_errors": "escalate to tier6_developer"
    },
    "input_schema": {
        "agent_outputs": "list",
        "protocol_draft": "dict",
        "known_constraints": "dict"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
