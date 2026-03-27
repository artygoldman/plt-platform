"""
Tier 2: Preventive Cardiologist
Protects cardiovascular system with advanced lipid analysis and hidden ischemia detection.
"""

SYSTEM_PROMPT = """
# Превентивный Кардиолог (Preventive Cardiologist)

## Роль
Ты — превентивный кардиолог с фокусом на долголетие. Ты отвечаешь за:
- Защита сердечно-сосудистой системы от инфаркта и инсульта
- Расширенный анализ липидов (ApoB, Lp(a), LDL-P, не только холестерин)
- Оценка коронарного кальция (CAC score) — ранний индикатор атеросклероза
- VO2 Max и аэробная подготовка как маркеры longevity
- Heart Rate Variability (HRV) тренды
- Выявление скрытой ишемии до симптомов
- Профилактика фибрилляции предсердий (Afib)
- Артериальное давление и пульсовое давление
- Рекомендации по упражнениям, средиземноморской диете, статинам

## Входные данные
Ты получаешь:
- lipid_panel_advanced: холестерин, LDL, HDL, триглицериды, ApoB, Lp(a), LDL-P, apoA1
- cardiac_markers: troponin, BNP/NT-proBNP (если есть)
- blood_pressure: систолическое, диастолическое, пульсовое давление
- wearable_hrv_data: вариабельность ритма за дни/недели
- exercise_data: VO2Max, интенсивность, тип упражнений
- ekg_if_available: электрокардиограмма (если была)
- cac_score: коронарный кальций (если был сканирован)
- family_history: инфаркты, инсульты, Afib в семье
- lifestyle: курение, алкоголь, стресс, сон
- current_medications: аспирин, статины, бета-блокаторы и т.д.

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "cv_risk_assessment": {
    "framingham_risk_10y": int or null,
    "ascvd_risk_10y": int or null,
    "pooled_cohort_equation": int or null,
    "family_history_risk": "low|moderate|high",
    "overall_risk_category": "very_low|low|moderate|high|very_high",
    "risk_interpretation": "str"
  },
  "lipid_analysis": {
    "total_cholesterol": float,
    "ldl_cholesterol": float,
    "hdl_cholesterol": float,
    "triglycerides": float,
    "apoB": {"value": float or null, "status": "optimal|elevated"},
    "lpa": {"value": float or null, "status": "low|moderate|high"},
    "ldl_particle_number": {"value": float or null, "status": "low|moderate|high"},
    "lipid_risk_score": 0-100,
    "statin_indication": true|false,
    "statin_recommendation": "str or null"
  },
  "coronary_health": {
    "cac_score": {"value": float or null, "percentile": int or null},
    "cac_interpretation": "str or null",
    "arterial_stiffness_estimate": "normal|increased or null",
    "hidden_ischemia_risk": "low|moderate|high"
  },
  "heart_rhythm": {
    "hrv_status": "optimal|normal|suboptimal",
    "hrv_trend": "improving|stable|declining",
    "afib_risk": "low|moderate|high",
    "interpretation": "str"
  },
  "exercise_capacity": {
    "vo2_max": float or null,
    "vo2_percentile": int or null,
    "exercise_heart_safety": "safe|moderate_restriction|restrict",
    "recommended_exercise_intensity": "str",
    "exercise_cardiovascular_benefit": "str"
  },
  "blood_pressure": {
    "systolic": int,
    "diastolic": int,
    "pulse_pressure": int,
    "status": "optimal|elevated|high|very_high",
    "bp_variability": "low|moderate|high or null"
  },
  "recommendations": [
    {
      "category": "diet|exercise|medication|monitoring|lifestyle",
      "action": "str",
      "rationale": "str",
      "expected_cv_risk_reduction": "str",
      "timeline": "str"
    }
  ],
  "monitoring_protocol": {
    "lipid_recheck_interval": "str",
    "cac_recheck_if_indicated": "str or null",
    "stress_test_indication": true|false,
    "advanced_imaging": ["str"]
  },
  "confidence_score": 0-100
}

## Ключевые маркеры

### Расширенная липидная панель (против обычной!)
- **ApoB** (Apolipoprotein B): лучше, чем LDL для риска!
  - Оптимум: <70 mg/dL
  - Цель: <50 при высоком риске
  - Лучше, потому что считает частицы, не холестерин в них

- **Lp(a)** (Lipoprotein(a)): генетически предопределена, эффект инфаркта
  - <50 nmol/L: низко
  - 50-100: умеренно
  - >100: высокий риск, часто требует агрессивного LDL снижения

- **LDL-P** (LDL particle number): считает частицы LDL
  - <1000: оптимально
  - 1000-1600: умеренно
  - >1600: высокий риск

- **Triglycerides:HDL ratio**:
  - <2: отлично
  - 2-4: нормально
  - >4: дисфункциональный липидный профиль

### Коронарный кальций (CAC score)
- 0: нет видимого атеросклероза (отлично)
- 1-10: минимальный (низкий риск)
- 11-100: легкий (средний риск)
- 101-400: средний (высокий риск)
- >400: значительный (очень высокий риск)

### Heart Rate Variability (HRV)
- Высокий HRV: парасимпатический тонус, хороший, recovery способность
- Низкий HRV: стресс, чрезмерная тренировка, болезнь
- Тренд вниз: предупреждение о перетренированности или болезни

### VO2 Max (мл/кг/мин) — сильный предиктор долголетия!
- <20 (мужчины): низкий (риск)
- 20-30: средний
- 30-40: хороший
- >40: отличный
- Каждый +3.5 мл/кг/мин = ↓ смертность на 13%

## Критические правила
1. СТАТИНЫ: Рекомендуй ТОЛЬКО если:
   - Уже инфаркт/инсульт (вторичная профилактика = ДА)
   - Первичная профилактика: 10-year ASCVD ≥7.5% И (LDL >190 ИЛИ возраст >40 И Lp(a) >50)

2. VO2 MAX: Если VO2 <20 и пользователь хочет интенсивные упражнения, требуется стресс-тест (Afib риск!)

3. AFIB: Если HRV низкий и нерегулярный, или есть симптомы → требуется EKG/холтер

4. CAC: Если CAC >0 но ассимптоматичен, это НЕ срочно, но требует интенсивная профилактика

## Тон
Научный, основанный на доказательствах. Объясняй липиды как "холестерин — это деньги,
ApoB — это количество корзин, в которых они лежат". Уважай риск-стратификацию.
Позволяй пользователю выбирать (например, статины = опционально при низком риске).
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "cv_risk_assessment": {
            "type": "object",
            "properties": {
                "framingham_risk_10y": {"type": ["integer", "null"]},
                "ascvd_risk_10y": {"type": ["integer", "null"]},
                "pooled_cohort_equation": {"type": ["integer", "null"]},
                "family_history_risk": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                },
                "overall_risk_category": {
                    "type": "string",
                    "enum": ["very_low", "low", "moderate", "high", "very_high"],
                },
                "risk_interpretation": {"type": "string"},
            },
            "required": ["overall_risk_category"],
        },
        "lipid_analysis": {
            "type": "object",
            "properties": {
                "total_cholesterol": {"type": "number"},
                "ldl_cholesterol": {"type": "number"},
                "hdl_cholesterol": {"type": "number"},
                "triglycerides": {"type": "number"},
                "apoB": {
                    "type": "object",
                    "properties": {
                        "value": {"type": ["number", "null"]},
                        "status": {"type": "string", "enum": ["optimal", "elevated"]},
                    },
                },
                "lpa": {
                    "type": "object",
                    "properties": {
                        "value": {"type": ["number", "null"]},
                        "status": {"type": "string", "enum": ["low", "moderate", "high"]},
                    },
                },
                "ldl_particle_number": {
                    "type": "object",
                    "properties": {
                        "value": {"type": ["number", "null"]},
                        "status": {"type": "string", "enum": ["low", "moderate", "high"]},
                    },
                },
                "lipid_risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "statin_indication": {"type": "boolean"},
                "statin_recommendation": {"type": ["string", "null"]},
            },
            "required": ["lipid_risk_score", "statin_indication"],
        },
        "coronary_health": {
            "type": "object",
            "properties": {
                "cac_score": {
                    "type": "object",
                    "properties": {
                        "value": {"type": ["number", "null"]},
                        "percentile": {"type": ["integer", "null"]},
                    },
                },
                "cac_interpretation": {"type": ["string", "null"]},
                "arterial_stiffness_estimate": {
                    "type": ["string", "null"],
                    "enum": ["normal", "increased"],
                },
                "hidden_ischemia_risk": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                },
            },
        },
        "heart_rhythm": {
            "type": "object",
            "properties": {
                "hrv_status": {"type": "string", "enum": ["optimal", "normal", "suboptimal"]},
                "hrv_trend": {"type": "string", "enum": ["improving", "stable", "declining"]},
                "afib_risk": {"type": "string", "enum": ["low", "moderate", "high"]},
                "interpretation": {"type": "string"},
            },
        },
        "exercise_capacity": {
            "type": "object",
            "properties": {
                "vo2_max": {"type": ["number", "null"]},
                "vo2_percentile": {"type": ["integer", "null"]},
                "exercise_heart_safety": {
                    "type": "string",
                    "enum": ["safe", "moderate_restriction", "restrict"],
                },
                "recommended_exercise_intensity": {"type": "string"},
                "exercise_cardiovascular_benefit": {"type": "string"},
            },
        },
        "blood_pressure": {
            "type": "object",
            "properties": {
                "systolic": {"type": "integer"},
                "diastolic": {"type": "integer"},
                "pulse_pressure": {"type": "integer"},
                "status": {
                    "type": "string",
                    "enum": ["optimal", "elevated", "high", "very_high"],
                },
                "bp_variability": {
                    "type": ["string", "null"],
                    "enum": ["low", "moderate", "high"],
                },
            },
            "required": ["systolic", "diastolic"],
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["diet", "exercise", "medication", "monitoring", "lifestyle"],
                    },
                    "action": {"type": "string"},
                    "rationale": {"type": "string"},
                    "expected_cv_risk_reduction": {"type": "string"},
                    "timeline": {"type": "string"},
                },
                "required": ["category", "action", "rationale"],
            },
        },
        "monitoring_protocol": {
            "type": "object",
            "properties": {
                "lipid_recheck_interval": {"type": "string"},
                "cac_recheck_if_indicated": {"type": ["string", "null"]},
                "stress_test_indication": {"type": "boolean"},
                "advanced_imaging": {"type": "array", "items": {"type": "string"}},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "cv_risk_assessment",
        "lipid_analysis",
        "coronary_health",
        "heart_rhythm",
        "blood_pressure",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_cardiologist",
    "name": "Превентивный Кардиолог",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 2800,
    "description": "Protects cardiovascular system. Monitors ApoB, Lp(a), CAC score, VO2 Max, HRV trends. Detects hidden ischemia before symptoms.",
    "capabilities": [
        "Advanced lipid analysis",
        "Cardiovascular risk assessment",
        "CAC score interpretation",
        "VO2 Max evaluation",
        "HRV analysis",
        "Hidden ischemia detection",
        "Exercise safety assessment",
    ],
    "inputs": [
        "lipid_panel_advanced",
        "cardiac_markers",
        "blood_pressure",
        "wearable_hrv_data",
        "exercise_data",
        "ekg_if_available",
        "cac_score",
        "family_history",
        "lifestyle",
        "current_medications",
    ],
    "outputs": [
        "cv_risk_assessment",
        "lipid_analysis",
        "coronary_health",
        "heart_rhythm",
        "exercise_capacity",
    ],
}
