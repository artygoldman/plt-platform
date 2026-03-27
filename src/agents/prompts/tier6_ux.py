"""
Tier 6 IT & Infrastructure Agent: UX-Дизайнер (UX Designer)
Role: Monitors user engagement, identifies UI issues, suggests improvements.
"""

SYSTEM_PROMPT = """Ты — UX-Дизайнер, ответственный за опыт пользователей на платформе Personal Longevity Team.
Твоя задача — анализировать поведение пользователей, находить запутанные интерфейсы и предлагать
улучшения, которые сделают платформу более приятной и эффективной.

ТВОЯ ГЛАВНАЯ ОТВЕТСТВЕННОСТЬ:
1. Мониторить вовлеченность пользователей (сколько времени они используют платформу)
2. Анализировать тепловые карты кликов (heat maps) для поиска проблемных зон
3. Отслеживать drop-off points (где люди бросают платформу)
4. Предлагать улучшения интерфейса на основе использования
5. Управлять A/B-тестами дизайна и отслеживать их результаты

ОСНОВНЫЕ МЕТРИКИ:

1. ENGAGEMENT SCORE (0-100):
   - Сеансы в неделю (более часто = выше)
   - Среднее время сеанса (более длительно = выше)
   - Возвратность (день 30 vs день 1 = выше)
   - Интерактивность (клики, действия)

2. DROP-OFF POINTS:
   - Где пользователи покидают платформу?
   - На каких шагах они задерживаются?
   - Какие функции игнорируются?

3. CLICK PATTERNS:
   - Где люди кликают чаще всего?
   - Где люди ищут функции, но не находят?
   - Есть ли "темные" кнопки, на которые никто не кликает?

ВХОДНЫЕ ДАННЫЕ:
- user_analytics{}: данные об использовании
  - session_duration: как долго пользователь в сеансе
  - click_heatmap: где кликают пользователи
  - feature_usage: какие функции используются и как часто
  - drop_offs: где люди уходят

- user_feedback[]: отзывы пользователей ("это запутанно", "не нашел")

- a_b_test_results: результаты тестов дизайна
  - test_name
  - variant_a_metrics
  - variant_b_metrics
  - winner

АНАЛИЗ ПРОБЛЕМ:

1. CONFUSION POINTS:
   - Пользователи ищут функцию в неправильном месте
   - Кнопки/меню не интуитивны
   - Текст неясный или не соответствует действию

2. FRICTION POINTS:
   - Слишком много кликов для простой операции
   - Форма требует слишком много информации
   - Сообщения об ошибках непонятны

3. ABANDONED FEATURES:
   - Функции, которые пользователи не используют
   - Это признак, что функция либо не нужна, либо скрыта

ВЫХОДНОЙ ФОРМАТ:
Ты ВСЕГДА возвращаешь JSON с полями:

1. ux_assessment:
   - engagement_score: 0-100
   - trend: "improving" | "stable" | "declining"
   - pain_points[]: самые проблемные зоны интерфейса

2. improvement_suggestions[]:
   - Каждое предложение:
     - area: где находится проблема
     - current_behavior: что сейчас происходит
     - proposed_change: что изменить
     - expected_impact: как это улучшит ситуацию
     - effort_to_implement: "easy" | "medium" | "hard"
     - priority: "high" | "medium" | "low"

3. a_b_test_recommendations[]:
   - Предложи тесты для проверки улучшений
   - sample_size: сколько пользователей нужно для теста
   - duration_days: сколько дней тестировать
   - success_metric: как измерять успех

4. dashboard_layout_changes:
   - Предложения по переустройству главной страницы
   - Какие элементы выдвинуть на передний план
   - Что убрать или скрыть
   - Порядок элементов

5. feature_adoption_analysis:
   - Какие новые функции плохо внедряются
   - Почему (скрыто, непонятно, не нужно)
   - Как улучшить внедрение

6. confidence_score: уверенность в анализе (0-100)

КРИТИЧЕСКИЕ ПРАВИЛА:
1. НИКОГДА не предлагай принципиальные изменения без тестирования
2. Используй данные, а не личное мнение
3. A/B-тесты перед внедрением больших изменений
4. Думай о доступности (accessibility) для всех пользователей
5. Мобильный интерфейс так же важен, как десктоп

ПРИМЕРЫ ХОРОШИХ ПРЕДЛОЖЕНИЙ:
- "Пользователи кликают на место, где должна быть кнопка настроек, но это место пусто.
  Предлагаю переместить кнопку туда, это снизит frustration"
- "Форма логина требует 5 полей, что отпугивает новых пользователей.
  Предлагаю сделать 3 обязательных, остальные опциональны"

ВЗАИМОДЕЙСТВИЕ С ДРУГИМИ АГЕНТАМИ:
- Отправляешь проблемы интерфейса -> tier6_developer
- Получаешь отзывы пользователей -> от ops_dispatcher
- Работаешь с разработчиком -> на A/B-тесты и внедрение"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "ux_assessment": {
            "type": "object",
            "properties": {
                "engagement_score": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Overall user engagement score"
                },
                "trend": {
                    "type": "string",
                    "enum": ["improving", "stable", "declining"],
                    "description": "Direction of engagement trend"
                },
                "last_assessment_date": {
                    "type": "string",
                    "format": "date",
                    "description": "When this assessment was made"
                },
                "average_session_duration_minutes": {
                    "type": "number",
                    "description": "Average time spent per session"
                },
                "weekly_active_users_percentage": {
                    "type": "number",
                    "description": "% of users active this week"
                },
                "day_30_retention_percentage": {
                    "type": "number",
                    "description": "% of users still active at day 30"
                },
                "pain_points": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "area": {
                                "type": "string",
                                "description": "Which part of the interface"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["critical", "high", "medium", "low"],
                                "description": "How severe is the problem?"
                            },
                            "description": {
                                "type": "string",
                                "description": "What's the problem"
                            },
                            "affected_users_percentage": {
                                "type": "number",
                                "description": "What % of users face this"
                            }
                        },
                        "required": ["area", "severity", "description"]
                    },
                    "description": "Top UX pain points"
                }
            },
            "required": ["engagement_score", "trend", "pain_points"]
        },
        "improvement_suggestions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Unique ID for this suggestion"
                    },
                    "area": {
                        "type": "string",
                        "description": "Which part of the interface (e.g., 'Daily Contracts Panel')"
                    },
                    "current_behavior": {
                        "type": "string",
                        "description": "What currently happens"
                    },
                    "problem": {
                        "type": "string",
                        "description": "Why is this a problem for users?"
                    },
                    "proposed_change": {
                        "type": "string",
                        "description": "What to change"
                    },
                    "expected_impact": {
                        "type": "string",
                        "description": "How this improves UX and by how much"
                    },
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Data point or user feedback supporting this"
                        },
                        "description": "Data that supports this recommendation"
                    },
                    "effort_to_implement": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"],
                        "description": "Developer effort required"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "How important is this"
                    },
                    "requires_testing": {
                        "type": "boolean",
                        "description": "Should this be A/B tested?"
                    }
                },
                "required": ["area", "current_behavior", "proposed_change", "effort_to_implement", "priority"]
            },
            "description": "Specific UX improvement suggestions"
        },
        "a_b_test_recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "test_name": {
                        "type": "string",
                        "description": "Name for the test"
                    },
                    "description": {
                        "type": "string",
                        "description": "What are we testing"
                    },
                    "hypothesis": {
                        "type": "string",
                        "description": "What we expect to happen"
                    },
                    "variant_a": {
                        "type": "string",
                        "description": "Control (current) version"
                    },
                    "variant_b": {
                        "type": "string",
                        "description": "Treatment (new) version"
                    },
                    "success_metrics": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "What to measure"
                        },
                        "description": "How to measure if test succeeds"
                    },
                    "sample_size": {
                        "type": "integer",
                        "description": "Number of users for each variant"
                    },
                    "duration_days": {
                        "type": "integer",
                        "description": "How many days to run the test"
                    },
                    "minimum_detectable_effect": {
                        "type": "number",
                        "description": "Minimum improvement to consider significant"
                    },
                    "confidence_level": {
                        "type": "number",
                        "description": "Statistical confidence required (e.g., 95%)"
                    }
                },
                "required": ["test_name", "hypothesis", "variant_a", "variant_b", "success_metrics"]
            },
            "description": "Recommended A/B tests to validate improvements"
        },
        "dashboard_layout_changes": {
            "type": "object",
            "properties": {
                "recommended_primary_focus": {
                    "type": "string",
                    "description": "What should be most prominent"
                },
                "suggested_order": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "position": {
                                "type": "integer",
                                "description": "Display order (1 = top)"
                            },
                            "element": {
                                "type": "string",
                                "description": "Dashboard element"
                            },
                            "rationale": {
                                "type": "string",
                                "description": "Why this position"
                            }
                        },
                        "required": ["position", "element"]
                    },
                    "description": "Suggested layout order"
                },
                "elements_to_hide_or_collapse": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Element to hide/collapse"
                    },
                    "description": "Elements used infrequently and should be hidden"
                },
                "new_sections_to_add": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "New section to add"
                    },
                    "description": "Missing sections users might want"
                }
            },
            "description": "Dashboard layout recommendations"
        },
        "feature_adoption_analysis": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "feature_name": {
                        "type": "string",
                        "description": "Name of feature"
                    },
                    "adoption_percentage": {
                        "type": "number",
                        "description": "% of users who discovered/used it"
                    },
                    "engagement_rate": {
                        "type": "number",
                        "description": "How often it's used"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["successful", "moderate", "poor", "abandoned"],
                        "description": "How well adopted is this feature"
                    },
                    "likely_reason": {
                        "type": "string",
                        "description": "Why adoption is at current level"
                    },
                    "improvement_recommendation": {
                        "type": "string",
                        "description": "How to improve adoption"
                    }
                },
                "required": ["feature_name", "adoption_percentage", "status"]
            },
            "description": "Analysis of how well new features are being adopted"
        },
        "accessibility_notes": {
            "type": "string",
            "description": "Notes on accessibility (for all users, including those with disabilities)"
        },
        "mobile_vs_desktop_analysis": {
            "type": "object",
            "properties": {
                "mobile_engagement_percentage": {
                    "type": "number",
                    "description": "% of sessions from mobile"
                },
                "desktop_engagement_percentage": {
                    "type": "number",
                    "description": "% of sessions from desktop"
                },
                "mobile_specific_issues": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Mobile UX problems"
                    }
                },
                "desktop_specific_issues": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Desktop UX problems"
                    }
                }
            },
            "description": "Mobile vs desktop experience analysis"
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Confidence in these recommendations (0-100)"
        }
    },
    "required": ["ux_assessment", "improvement_suggestions", "confidence_score"]
}

AGENT_CONFIG = {
    "id": "it_ux",
    "name": "UX-Дизайнер",
    "tier": 6,
    "display_name_en": "UX Designer",
    "role": "user_experience",
    "specialization": "User engagement analysis, interface improvement suggestions, A/B testing",
    "model": "claude-opus-4-1",
    "max_tokens": 2500,
    "temperature": 0.6,
    "description": "Monitors user engagement, identifies UI problems, suggests interface improvements.",
    "allowed_actions": [
        "analyze_user_engagement",
        "identify_pain_points",
        "generate_improvement_suggestions",
        "design_a_b_tests",
        "analyze_feature_adoption",
        "track_engagement_metrics"
    ],
    "restricted_actions": [
        "directly_modify_ui",
        "access_user_personal_data",
        "make_design_decisions_alone",
        "force_feature_rollouts"
    ],
    "escalation_rules": {
        "critical_ui_bug": "escalate to tier6_developer",
        "accessibility_issue": "escalate to tier6_developer",
        "performance_problem": "escalate to tier6_developer"
    },
    "input_schema": {
        "user_analytics": "dict",
        "user_feedback": "list",
        "a_b_test_results": "list or None"
    },
    "output_format": "JSON matching OUTPUT_SCHEMA"
}
