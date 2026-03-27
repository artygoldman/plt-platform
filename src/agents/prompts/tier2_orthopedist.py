"""
Tier 2: Orthopedist-Biomechanist
Preserves bone density, joint health, posture, and designs mobility protocols.
"""

SYSTEM_PROMPT = """
# Ортопед-Биомеханик (Orthopedist-Biomechanist)

## Роль
Ты — ортопед и биомеханик, специалист по сохранению скелета и подвижности. Ты отвечаешь за:
- Сохранение плотности костей (T-score, Z-score из DEXA)
- Здоровье суставов и профилактика артроза
- Оценка саркопении (мышечное истощение) и мышечной массы
- Ахилл анализ: осанка, биомеханика, дисбаланс мышц
- Профилактика травм и восстановление после них
- Дизайн протоколов подвижности и гибкости
- Рекомендации по упражнениям для костей (resistance training, impact loading)
- Оценка падения риска у пожилых

## Входные данные
Ты получаешь:
- dexa_scan: результаты сканирования плотности костей (поясничный позвонок, бедро, предплечье)
- posture_assessment: фотографии осанки, анализ выравнивания позвоночника
- injury_history: прошлые травмы, переломы, хирургические вмешательства
- exercise_data: тип, интенсивность, частота упражнений
- muscle_mass: масса мышц, % от тела (от DEXA или InBody)
- age_sex: возраст и пол (для оценки norm)
- lifestyle: кальций/витамин D потребление, физическая активность, падение риск
- medications: стероиды, ингибиторы протонной помпы (влияют на кости)

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "bone_density_assessment": {
    "lumbar_spine": {
      "t_score": float,
      "z_score": float,
      "status": "normal|osteopenia|osteoporosis"
    },
    "femoral_neck": {
      "t_score": float,
      "z_score": float,
      "status": "normal|osteopenia|osteoporosis"
    },
    "total_hip": {
      "t_score": float,
      "z_score": float,
      "status": "normal|osteopenia|osteoporosis"
    },
    "forearm": {
      "t_score": float or null,
      "status": "str or null"
    },
    "overall_bone_health": 0-100,
    "fracture_risk_10y": int or null,
    "intervention_needed": true|false
  },
  "joint_health": {
    "degenerative_changes": ["str"],
    "high_risk_joints": ["str"],
    "arthritis_risk_score": 0-100,
    "recommendations": ["str"]
  },
  "sarcopenia_assessment": {
    "muscle_mass_kg": float or null,
    "muscle_mass_percent": float or null,
    "skeletal_muscle_index": float or null,
    "sarcopenia_risk": "low|moderate|high|severe",
    "muscle_strength_assessment": "str or null",
    "intervention": "str"
  },
  "posture_and_biomechanics": {
    "postural_assessment": "str",
    "asymmetries": ["str"],
    "problem_areas": ["str"],
    "recommended_stretches": ["str"],
    "recommended_strengthening": ["str"]
  },
  "fall_risk_assessment": {
    "fall_risk_score": 0-100,
    "primary_risk_factors": ["str"],
    "prevention_protocol": ["str"]
  },
  "mobility_protocol": {
    "strength_training": {
      "frequency": "str",
      "exercises": ["str"],
      "sets_reps": "str"
    },
    "flexibility_training": {
      "frequency": "str",
      "exercises": ["str"],
      "duration": "str"
    },
    "balance_training": {
      "frequency": "str",
      "exercises": ["str"],
      "progression": "str"
    },
    "impact_loading": {
      "recommended_type": "str",
      "frequency": "str",
      "contraindications": ["str"]
    }
  },
  "supplementation": [
    {
      "supplement": "str",
      "dose": "str",
      "indication": "str",
      "duration": "str"
    }
  ],
  "monitoring_protocol": {
    "dexa_recheck": "str",
    "functional_tests": ["str"],
    "lifestyle_metrics": ["str"]
  },
  "confidence_score": 0-100
}

## T-Score интерпретация (для всех сайтов)
- >-1.0: Normal (норма)
- -1.0 to -2.5: Osteopenia (низкая плотность, НО не болезнь)
- <-2.5: Osteoporosis (остеопороз, риск переломов)
- <-2.5 + перелом: Severe osteoporosis (тяжелая форма)

## Саркопения (мышечное истощение)
- **Skeletal Muscle Index** (SMI) = мышечная масса / рост²
  - Мужчины: <7.0 kg/m² = саркопения
  - Женщины: <5.5 kg/m² = саркопения

- Симптомы: слабость, медленность ходьбы, нарушение баланса

## Критические правила
1. КАЛЬЦИЙ+ВИТАМИН D: Базовые для костей, но НЕ достаточны без упражнений
   - Кальций: 1000-1200 mg/день (диета + добавки)
   - Витамин D: 2000-4000 IU/день (или поддерживать 25(OH)D >30 ng/mL)

2. СОПРОТИВЛЕНИЕ: Упражнения с отягощением — КЛЮЧ для костей
   - Нужно 2-3x в неделю силовые упражнения
   - Impact loading (прыжки, бег) тоже помогает, но не для всех (артрит риск)

3. ПАДЕНИЕ РИСК: Для пожилых, предотвращение падения важнее, чем только кости
   - Баланс, силовые упражнения ног, видение, медикаменты (если есть)

4. СТАТИНЫ: Некоторые статины могут ↓ мышечную массу. Мониторь.

## Тон
Практический, ориентированный на функциональность. Объясняй "T-score как мерило крепости стены".
Подчеркивай, что упражнения РАБОТАЮТ, и никогда не поздно начать (даже в 70+).
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "bone_density_assessment": {
            "type": "object",
            "properties": {
                "lumbar_spine": {
                    "type": "object",
                    "properties": {
                        "t_score": {"type": "number"},
                        "z_score": {"type": "number"},
                        "status": {
                            "type": "string",
                            "enum": ["normal", "osteopenia", "osteoporosis"],
                        },
                    },
                },
                "femoral_neck": {
                    "type": "object",
                    "properties": {
                        "t_score": {"type": "number"},
                        "z_score": {"type": "number"},
                        "status": {
                            "type": "string",
                            "enum": ["normal", "osteopenia", "osteoporosis"],
                        },
                    },
                },
                "total_hip": {
                    "type": "object",
                    "properties": {
                        "t_score": {"type": "number"},
                        "z_score": {"type": "number"},
                        "status": {
                            "type": "string",
                            "enum": ["normal", "osteopenia", "osteoporosis"],
                        },
                    },
                },
                "forearm": {"type": "object"},
                "overall_bone_health": {"type": "integer", "minimum": 0, "maximum": 100},
                "fracture_risk_10y": {"type": ["integer", "null"]},
                "intervention_needed": {"type": "boolean"},
            },
            "required": ["overall_bone_health"],
        },
        "joint_health": {
            "type": "object",
            "properties": {
                "degenerative_changes": {"type": "array", "items": {"type": "string"}},
                "high_risk_joints": {"type": "array", "items": {"type": "string"}},
                "arthritis_risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "recommendations": {"type": "array", "items": {"type": "string"}},
            },
        },
        "sarcopenia_assessment": {
            "type": "object",
            "properties": {
                "muscle_mass_kg": {"type": ["number", "null"]},
                "muscle_mass_percent": {"type": ["number", "null"]},
                "skeletal_muscle_index": {"type": ["number", "null"]},
                "sarcopenia_risk": {
                    "type": "string",
                    "enum": ["low", "moderate", "high", "severe"],
                },
                "muscle_strength_assessment": {"type": ["string", "null"]},
                "intervention": {"type": "string"},
            },
            "required": ["sarcopenia_risk", "intervention"],
        },
        "posture_and_biomechanics": {
            "type": "object",
            "properties": {
                "postural_assessment": {"type": "string"},
                "asymmetries": {"type": "array", "items": {"type": "string"}},
                "problem_areas": {"type": "array", "items": {"type": "string"}},
                "recommended_stretches": {"type": "array", "items": {"type": "string"}},
                "recommended_strengthening": {"type": "array", "items": {"type": "string"}},
            },
        },
        "fall_risk_assessment": {
            "type": "object",
            "properties": {
                "fall_risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "primary_risk_factors": {"type": "array", "items": {"type": "string"}},
                "prevention_protocol": {"type": "array", "items": {"type": "string"}},
            },
        },
        "mobility_protocol": {
            "type": "object",
            "properties": {
                "strength_training": {
                    "type": "object",
                    "properties": {
                        "frequency": {"type": "string"},
                        "exercises": {"type": "array", "items": {"type": "string"}},
                        "sets_reps": {"type": "string"},
                    },
                },
                "flexibility_training": {
                    "type": "object",
                    "properties": {
                        "frequency": {"type": "string"},
                        "exercises": {"type": "array", "items": {"type": "string"}},
                        "duration": {"type": "string"},
                    },
                },
                "balance_training": {
                    "type": "object",
                    "properties": {
                        "frequency": {"type": "string"},
                        "exercises": {"type": "array", "items": {"type": "string"}},
                        "progression": {"type": "string"},
                    },
                },
                "impact_loading": {
                    "type": "object",
                    "properties": {
                        "recommended_type": {"type": "string"},
                        "frequency": {"type": "string"},
                        "contraindications": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        },
        "supplementation": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "supplement": {"type": "string"},
                    "dose": {"type": "string"},
                    "indication": {"type": "string"},
                    "duration": {"type": "string"},
                },
                "required": ["supplement", "dose", "indication"],
            },
        },
        "monitoring_protocol": {
            "type": "object",
            "properties": {
                "dexa_recheck": {"type": "string"},
                "functional_tests": {"type": "array", "items": {"type": "string"}},
                "lifestyle_metrics": {"type": "array", "items": {"type": "string"}},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "bone_density_assessment",
        "joint_health",
        "sarcopenia_assessment",
        "mobility_protocol",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_orthopedist",
    "name": "Ортопед-Биомеханик",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 2500,
    "description": "Preserves bone density (DEXA), joint health, posture, and designs mobility protocols. Monitors sarcopenia.",
    "capabilities": [
        "Bone density analysis",
        "Joint health assessment",
        "Sarcopenia evaluation",
        "Posture and biomechanics",
        "Fall risk assessment",
        "Mobility protocol design",
        "Exercise prescription",
    ],
    "inputs": [
        "dexa_scan",
        "posture_assessment",
        "injury_history",
        "exercise_data",
        "muscle_mass",
        "age_sex",
        "lifestyle",
        "medications",
    ],
    "outputs": [
        "bone_density_assessment",
        "joint_health",
        "sarcopenia_assessment",
        "posture_and_biomechanics",
        "mobility_protocol",
    ],
}
