# Agent Documentation: The 27-Agent Medical Hierarchy

## Overview

The PLT platform orchestrates **27 specialized AI agents** across 6 hierarchical tiers to deliver comprehensive health optimization. Each agent is a Claude LLM with a specialized system prompt, designed to excel in its medical domain.

**North Star Metrics:**
- **DunedinPACE**: Biological aging pace (lower is better)
- **Biological Age**: Calculated from epigenetic markers and system scores
- **Healthspan Forecast**: Years of healthy life remaining
- **Longevity Score**: 0-100 composite metric integrating all systems

---

## Tier 1: Strategic Foundation (4 Agents)

### Roles
- **System Biologist**: Aggregate all data → unified Digital Twin
- **Analyst**: Synthesize specialist opinions → draft protocol
- **Verifier**: Validate against knowledge base → veto loop
- **CMO**: Final approval → biological age forecast

### 1.1 System Biologist

**ID**: `system_biologist`
**Role**: Digital Twin Builder
**Tier**: 1 (Strategic)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Complete biomarker history (all 100+ markers)
- User profile (genetics, medications, lifestyle)
- Wearable data (Oura: sleep, HRV, respiratory rate)
- Historical twin snapshots (for trend analysis)
- Trigger data (new anomalies, user query context)

**Output Schema:**
```json
{
  "digital_twin_snapshot": {
    "timestamp": "2026-03-27T10:30:00Z",
    "chronological_age": 45.0,
    "biological_age": 42.5,
    "biological_age_ci_lower": 40.2,
    "biological_age_ci_upper": 44.8,
    "dunedin_pace": 0.95,
    "system_scores": {
      "cardiovascular": 78,
      "metabolic": 65,
      "cognitive": 82,
      "immune": 71,
      "hormonal": 75,
      "neurological": 80,
      "renal": 88,
      "hepatic": 85,
      "bone": 72,
      "muscular": 70,
      "sleep_circadian": 68
    },
    "overall_health_score": 76,
    "anomalies_detected": [
      {
        "system": "cardiovascular",
        "marker": "ApoB",
        "value": 95,
        "optimal_range": "0-70",
        "severity": "moderate",
        "recommendation": "Review statin therapy"
      }
    ],
    "cross_system_correlations": [
      {
        "system_a": "metabolic",
        "system_b": "cardiovascular",
        "correlation": 0.78,
        "interpretation": "Elevated glucose correlates with ApoB"
      }
    ],
    "trend_analysis": {
      "biological_age_trend": "stable",
      "velocity_months": 0.1,
      "forecast_5yr": 45.0
    }
  }
}
```

**Example Decision:**
- **Input**: New blood test shows ApoB 95, hsCRP 3.2
- **Analysis**: Cardiovascular risk elevated, inflammation present
- **Output**: Twin update with cardiovascular score 68→65, flags for cardiologist review
- **Confidence**: 92%

---

### 1.2 Analyst

**ID**: `analyst`
**Role**: Opinion Synthesizer
**Tier**: 1 (Strategic)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Digital Twin snapshot (from System Biologist)
- 8 medical opinions (from Tier 2 specialists)
- 5 lifestyle opinions (from Tier 3 experts)
- User profile (allergies, medications, contraindications)
- ROI data (cost-effectiveness of interventions)

**Output Schema:**
```json
{
  "draft_protocol": {
    "nutrition": {
      "macro_targets": {
        "protein_g": 120,
        "fat_g": 80,
        "carbs_g": 200,
        "fiber_g": 30
      },
      "micronutrient_focus": [
        {"name": "magnesium", "reason": "cardiovascular_health"},
        {"name": "vitamin_d3", "reason": "immune_bone_metabolic"}
      ],
      "dietary_pattern": "mediterranean_modified",
      "restriction_rationale": "limit_refined_carbs_due_to_glucose_trend"
    },
    "supplements": [
      {
        "name": "NAD+",
        "dosage": "500mg",
        "frequency": "daily",
        "evidence_grade": "B",
        "rationale": "Supports mitochondrial function, energy metabolism"
      },
      {
        "name": "Omega-3 (EPA+DHA)",
        "dosage": "2000mg",
        "frequency": "daily",
        "evidence_grade": "A",
        "rationale": "Cardiovascular protection, anti-inflammatory"
      }
    ],
    "fitness": {
      "cardio_weekly_minutes": 150,
      "cardio_intensity": "moderate (zone 2-3)",
      "strength_weekly_sessions": 3,
      "strength_focus": "full_body_compound_movements",
      "flexibility": "daily_10min_yoga",
      "rationale": "Support cardiovascular and metabolic health"
    },
    "sleep": {
      "target_duration_hours": 8.0,
      "consistent_bedtime": "22:30",
      "consistent_wake_time": "06:30",
      "sleep_environment": "cool_65F_dark_quiet",
      "pre_sleep_routine": "dim_lights_2h_before"
    },
    "medical_actions": [
      {
        "action": "consult_cardiologist",
        "priority": "high",
        "reason": "Review statin therapy given elevated ApoB",
        "timeline_days": 7
      }
    ]
  },
  "roi_analysis": [
    {
      "action": "take_omega3_2g_daily",
      "roi_score": 9.2,
      "cost_per_day_usd": 0.35,
      "expected_impact": "10% cardiovascular risk reduction",
      "impact_type": "long_term_5yr"
    },
    {
      "action": "exercise_150min_weekly",
      "roi_score": 9.5,
      "cost_per_day_usd": 0.0,
      "expected_impact": "15% all_cause_mortality_reduction",
      "impact_type": "long_term_10yr"
    }
  ],
  "conflict_resolution": {
    "conflicts_identified": 1,
    "example": {
      "agent_a": "cardiologist",
      "agent_a_recommendation": "high_dose_statin",
      "agent_b": "endocrinologist",
      "agent_b_recommendation": "moderate_statin_with_lifestyle",
      "resolution": "adopted_moderate_approach_given_user_muscle_issues"
    }
  }
}
```

**Example Decision:**
- **Input**: Cardiologist: "High-dose statin" vs Endocrinologist: "Lifestyle modification first"
- **Conflict**: User reports muscle pain with statins
- **Resolution**: Recommend moderate statin with aggressive lifestyle changes
- **Output**: Draft protocol prioritizing exercise + supplements over medication
- **Confidence**: 87%

---

### 1.3 Verifier

**ID**: `verifier`
**Role**: Knowledge Base Validator, Safety Guard
**Tier**: 1 (Strategic)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Draft protocol (from Analyst)
- User profile (medications, allergies, contraindications, genetic risks)
- Knowledge base (semantic search via pgvector)
- Evidence database (recent meta-analyses, RCTs, guidelines)

**Output Schema:**
```json
{
  "verdict": "approved|vetoed|needs_revision",
  "confidence": 95,
  "issues": [
    {
      "severity": "critical|high|medium|low",
      "issue": "Drug interaction detected",
      "details": "Omega-3 + warfarin increases bleeding risk",
      "recommendation": "Reduce omega-3 to 1g daily or consult cardiologist"
    }
  ],
  "knowledge_base_checks": {
    "supplement_interactions": "passed",
    "drug_interactions": "failed",
    "contraindications": "passed",
    "evidence_grade": "A_and_B_only"
  },
  "recommendations": [
    "Reduce omega-3 dosage given user takes warfarin",
    "Add INR monitoring schedule",
    "Consult cardiologist before protocol start"
  ],
  "veto_reason": null,
  "evidence_citations": [
    {
      "title": "Omega-3 and anticoagulation interaction",
      "authors": "Smith J, et al.",
      "year": 2023,
      "journal": "Thrombosis Research"
    }
  ]
}
```

**Veto Loop Logic:**
```
If verdict == "vetoed":
  ├─ veto_count += 1
  ├─ If veto_count < 3:
  │  └─ Loop back to Tier 2 Medical Core
  │     (provide feedback, re-synthesize)
  └─ Else:
     └─ Escalate to CMO for final decision
```

**Example Verdict:**
- **Input**: Draft recommends NAD+ 500mg + user on beta-blockers
- **Check**: Knowledge base shows NAD+ may affect BP control
- **Verdict**: "needs_revision" (VETO 1/3)
- **Feedback**: "Reduce NAD+ to 250mg, monitor blood pressure weekly"
- **Outcome**: Tier 2 adjusts, re-synthesizes, passes to Analyst again

---

### 1.4 Chief Medical Officer (CMO)

**ID**: `cmo`
**Role**: Final Arbiter, Escalation, Biological Age Forecasting
**Tier**: 1 (Strategic)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Verified protocol (from Verifier)
- Digital Twin (from System Biologist)
- All Tier 2 & 3 agent decisions (full audit trail)
- User health history (past protocols, outcomes, adherence)
- Escalation context (any human-in-the-loop flags)

**Output Schema:**
```json
{
  "approved_protocol": {
    ...  // Same as verified protocol from Verifier
  },
  "priority_actions": [
    {
      "rank": 1,
      "action": "Increase omega-3 to 2g daily",
      "longevity_gain_years": 2.3,
      "feasibility": "easy",
      "adherence_probability": 0.92,
      "timeline_weeks": 1
    },
    {
      "rank": 2,
      "action": "Exercise 150 min/week moderate cardio",
      "longevity_gain_years": 3.5,
      "feasibility": "moderate",
      "adherence_probability": 0.65,
      "timeline_weeks": 2
    }
  ],
  "biological_age_forecast": {
    "current_biological_age": 42.5,
    "chronological_age": 45.0,
    "forecast_5yr_if_protocol_followed": 39.2,
    "forecast_5yr_if_no_changes": 45.0,
    "estimated_lifespan_extension": 3.8,
    "confidence": 0.75,
    "methodology": "DunedinPACE_projection_with_intervention_adjustment"
  },
  "escalation_needed": false,
  "escalation_reason": null,
  "physician_consultations_required": [
    {
      "specialty": "cardiology",
      "reason": "Statin therapy review",
      "urgency": "high",
      "timeline_days": 7
    }
  ],
  "confidence_score": 92,
  "override_flags": [],
  "notes": "Strong evidence for aggressive lifestyle intervention. User engaged and motivated."
}
```

**Escalation Criteria:**
- Any recommendation requiring prescription change
- Contraindication detected (user has metal implant, pregnancy suspected)
- Conflicting medical opinions not resolved by Verifier
- High-risk interventions (surgery, experimental treatment)

---

## Tier 2: Medical Specialists (8 Agents)

**Execution**: Parallel fan-out from System Biologist
**Wait Point**: Analyst node (waits for all 8 opinions)

### 2.1 Cardiologist

**ID**: `med_cardiologist`
**Role**: Cardiovascular System Analysis
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Lipid panel (Total cholesterol, LDL, HDL, triglycerides, **ApoB**)
- Blood pressure (systolic, diastolic, pulse pressure)
- Arterial stiffness markers (pulse wave velocity, augmentation index)
- Cardiac biomarkers (troponin, BNP, high-sensitivity CRP)
- Heart rate variability (from Oura or wearables)
- Family history of cardiovascular disease

**Output Schema:**
```json
{
  "cardiovascular_risk_assessment": {
    "overall_risk": "moderate",
    "short_term_mace_risk_10yr": 8.5,
    "framingham_score": 12,
    "key_findings": [
      "ApoB elevated (95 mg/dL, optimal <70)",
      "LDL particle number high despite acceptable LDL-C",
      "Blood pressure excellent (120/78)"
    ]
  },
  "recommendations": [
    {
      "recommendation": "Consider statin therapy or review current dose",
      "rationale": "ApoB elevation is strongest LDL predictor",
      "evidence_grade": "A",
      "priority": "high"
    },
    {
      "recommendation": "Omega-3 supplementation 2g EPA+DHA daily",
      "rationale": "Triglyceride reduction, inflammation control",
      "evidence_grade": "B",
      "priority": "medium"
    },
    {
      "recommendation": "Maintain current exercise regimen",
      "rationale": "Cardiovascular fitness excellent per HRV",
      "evidence_grade": "A",
      "priority": "maintenance"
    }
  ],
  "contraindications": [
    {
      "substance": "NSAIDs",
      "reason": "Increase cardiovascular event risk"
    }
  ],
  "confidence": 92,
  "tokens_used": 1240
}
```

**Example Decision:**
- **Input**: ApoB 95, LDL 120, HDL 45, triglycerides 180
- **Analysis**: Atherogenic dyslipidemia pattern; ApoB most predictive
- **Recommendation**: Consider statin; aggressive omega-3; low-carb diet
- **Confidence**: 92%
- **Veto Risk**: LOW (strong evidence base)

---

### 2.2 Endocrinologist

**ID**: `med_endocrinologist`
**Role**: Hormonal & Glucose Metabolism
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Glucose markers (fasting glucose, HbA1c, insulin, C-peptide, HOMA-IR)
- Thyroid panel (TSH, free T4, free T3, TPO antibodies)
- Adrenal hormones (cortisol AM/PM, DHEA-S)
- Reproductive hormones (testosterone, estradiol, progesterone, SHBG, LH, FSH)
- Prolactin, growth hormone indicators

**Output Schema:**
```json
{
  "endocrine_assessment": {
    "glucose_metabolism": {
      "status": "suboptimal",
      "fasting_glucose": 110,
      "hba1c": 5.8,
      "insulin_resistance": "present",
      "homa_ir": 2.3
    },
    "thyroid_function": {
      "status": "optimal",
      "tsh": 1.8,
      "free_t4": "upper_normal"
    },
    "cortisol_rhythm": {
      "status": "disrupted",
      "am_cortisol": 18,
      "pm_cortisol": 4,
      "assessment": "Adequate amplitude, but elevated evening"
    }
  },
  "recommendations": [
    {
      "recommendation": "Reduce refined carbohydrate intake",
      "rationale": "Improve insulin sensitivity, lower HbA1c trajectory",
      "priority": "high"
    },
    {
      "recommendation": "Evening light exposure reduction",
      "rationale": "Lower cortisol at night, improve circadian alignment",
      "priority": "high"
    }
  ],
  "confidence": 88
}
```

---

### 2.3 Metabolologist

**ID**: `med_metabolologist`
**Role**: Mitochondrial Health & Energy Metabolism
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Mitochondrial markers (carnitine, CoQ10, citrate, isocitrate)
- Energy metabolism (lactate, pyruvate, ATP/ADP ratio inferred from glucose)
- NAD+/NADH ratio (if available)
- Metabolic rate estimation
- Body composition (muscle vs. fat from DEXA or estimation)
- Age-adjusted metabolic capacity

**Output Schema:**
```json
{
  "mitochondrial_assessment": {
    "mitochondrial_function": "good",
    "estimated_atp_production": "normal_for_age",
    "lactate_clearance": "efficient",
    "nad_plus_status": "suboptimal_age_45"
  },
  "recommendations": [
    {
      "recommendation": "NAD+ supplementation 500mg daily",
      "rationale": "Restore NAD+ levels, enhance mitochondrial sirtuin activity",
      "priority": "medium"
    },
    {
      "recommendation": "CoQ10 200mg daily",
      "rationale": "Support electron transport chain",
      "priority": "low"
    }
  ],
  "confidence": 80
}
```

---

### 2.4 Geneticist

**ID**: `med_geneticist`
**Role**: Genetic Risk Interpretation & Pharmacogenomics
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Genetic variants (APOE, MTHFR, CYP450 polymorphisms, ACE, FTO)
- Methylation status (if 5mC data available)
- Familial health history (Alzheimer's, cardiovascular disease, cancer, longevity)
- Pharmacogenomic profile (for medication metabolism)

**Output Schema:**
```json
{
  "genetic_assessment": {
    "apoe_status": "E3E3",
    "apoe_interpretation": "average_alzheimer_risk"
  },
  "genetic_risks": [
    {
      "variant": "APOE4_negative",
      "implication": "Lower Alzheimer's risk than APOE4 carriers",
      "action": "Maintain cognitive engagement, manage cardiovascular health"
    }
  ],
  "pharmacogenomics": {
    "cyp3a4": "normal_metabolizer",
    "cyp2c9": "normal_metabolizer",
    "clinical_implications": [
      "Standard statin dosing appropriate",
      "No expected warfarin interactions"
    ]
  },
  "recommendations": [
    {
      "recommendation": "Maintain cognitive stimulation",
      "priority": "medium"
    }
  ],
  "confidence": 85
}
```

---

### 2.5 Dermatologist

**ID**: `med_dermatologist`
**Role**: Skin Aging & Collagen Integrity
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Skin elasticity assessments
- Collagen cross-linking markers (if advanced bloodwork)
- Sun exposure history, past burns
- Skin microbiome status (if available)
- Aesthetic aging markers (visual assessment or photography)

**Output Schema:**
```json
{
  "dermatologic_assessment": {
    "skin_age": "similar_to_chronological",
    "collagen_integrity": "good",
    "sun_damage_assessment": "moderate"
  },
  "recommendations": [
    {
      "recommendation": "Sunscreen SPF 30+ daily",
      "priority": "high"
    },
    {
      "recommendation": "Retinol or retinoid 2-3x per week",
      "rationale": "Support collagen remodeling, prevent further photoaging",
      "priority": "medium"
    },
    {
      "recommendation": "Vitamin C serum daily",
      "priority": "medium"
    }
  ],
  "confidence": 78
}
```

---

### 2.6 Orthopedist

**ID**: `med_orthopedist`
**Role**: Bone Density, Joint Health, Muscle Mass
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Bone mineral density (DEXA scan T-score)
- Bone turnover markers (CTX, P1NP, alkaline phosphatase)
- Muscle mass (from DEXA or BIA estimation)
- Calcium, phosphate, magnesium, vitamin D
- Joint pain/injury history
- Inflammation markers (hsCRP)

**Output Schema:**
```json
{
  "musculoskeletal_assessment": {
    "bone_density": "normal_age_matched",
    "muscle_mass": "above_average_for_age",
    "joint_health": "good"
  },
  "recommendations": [
    {
      "recommendation": "Strength training 3x/week",
      "priority": "high"
    },
    {
      "recommendation": "Vitamin D3 4000 IU daily",
      "priority": "medium"
    },
    {
      "recommendation": "Resistance band or weight exercise",
      "priority": "high"
    }
  ],
  "confidence": 86
}
```

---

### 2.7 Microbiome Specialist

**ID**: `med_microbiome`
**Role**: Gut Microbiota, Dysbiosis Detection
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Microbiome composition (Firmicutes/Bacteroidetes ratio, diversity index)
- Short-chain fatty acid producers
- Pathogenic bacteria detection
- Intestinal permeability markers (zonulin, lipopolysaccharide)
- Dietary fiber intake
- Probiotic/prebiotic use

**Output Schema:**
```json
{
  "microbiome_assessment": {
    "diversity": "good",
    "firmicutes_bacteroidetes_ratio": 1.1,
    "dysbiosis": "absent",
    "pathogenic_load": "low"
  },
  "recommendations": [
    {
      "recommendation": "Maintain high fiber intake (30g+/day)",
      "priority": "high"
    },
    {
      "recommendation": "Fermented foods (yogurt, kimchi, sauerkraut)",
      "priority": "medium"
    }
  ],
  "confidence": 82
}
```

---

### 2.8 Aesthetist

**ID**: `med_aesthetist`
**Role**: Aesthetic Anti-Aging Compounds & Stem Cell Markers
**Tier**: 2 (Medical)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Skin appearance metrics
- Facial structure, skin tone
- Anti-aging biomarkers (sirtuins, NAD+, cellular senescence markers)
- Aesthetic intervention history (Botox, fillers, procedures)
- Hormone levels affecting appearance (testosterone, estradiol)

**Output Schema:**
```json
{
  "aesthetic_assessment": {
    "visual_age": "younger_than_chronological_by_3yr",
    "stem_cell_activity": "good_for_age",
    "skin_quality": "excellent"
  },
  "recommendations": [
    {
      "recommendation": "Continue current skincare regimen",
      "priority": "maintenance"
    },
    {
      "recommendation": "NAD+ supplementation for sirtuin activation",
      "priority": "low_optional"
    }
  ],
  "confidence": 75
}
```

---

## Tier 3: Lifestyle Experts (5 Agents)

**Execution**: Parallel fan-out from System Biologist
**Wait Point**: Analyst node (waits for all 5 opinions)

### 3.1 Sleep Specialist

**ID**: `lifestyle_sleep`
**Role**: Sleep Architecture & Sleep Hygiene
**Tier**: 3 (Lifestyle)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Sleep duration (from Oura, Apple Watch, self-report)
- Sleep stages (REM %, NREM %, deep sleep %)
- Sleep quality score, restlessness
- Circadian phase alignment (bedtime consistency)
- Sleep debt/sleep drive
- Caffeine/alcohol intake timing

**Output Schema:**
```json
{
  "sleep_assessment": {
    "sleep_duration": 7.5,
    "sleep_quality": "good",
    "rem_percentage": 22,
    "deep_sleep_percentage": 15,
    "sleep_consistency": "excellent",
    "circadian_alignment": "good"
  },
  "sleep_hygiene_recommendations": [
    {
      "recommendation": "Maintain consistent sleep/wake times",
      "priority": "high"
    },
    {
      "recommendation": "Dim lights 2 hours before bed",
      "priority": "high"
    },
    {
      "recommendation": "Avoid caffeine after 2 PM",
      "priority": "medium"
    },
    {
      "recommendation": "Cool bedroom (65-68F)",
      "priority": "medium"
    }
  ],
  "supplements": [
    {
      "supplement": "Magnesium glycinate 300mg at bedtime",
      "rationale": "Improve sleep quality, relaxation"
    }
  ],
  "confidence": 89
}
```

---

### 3.2 Neuropsychologist

**ID**: `lifestyle_neuropsych`
**Role**: Cognitive Function & Mental Health
**Tier**: 3 (Lifestyle)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Cognitive assessment (if available: MMSE, MoCA, or self-report)
- Mental health screening (depression, anxiety, stress levels)
- Stress biomarkers (cortisol, heart rate variability)
- Sleep quality (affects cognition)
- Social engagement, learning activities
- Alcohol consumption, substance use

**Output Schema:**
```json
{
  "cognitive_neuropsych_assessment": {
    "cognitive_function": "excellent_for_age",
    "memory": "strong",
    "processing_speed": "normal_for_age",
    "mental_health": "good",
    "stress_level": "moderate"
  },
  "recommendations": [
    {
      "recommendation": "Daily cognitive engagement (learning, puzzles, reading)",
      "priority": "high"
    },
    {
      "recommendation": "Meditation or mindfulness 10min daily",
      "rationale": "Reduce stress, enhance attention",
      "priority": "medium"
    },
    {
      "recommendation": "Social engagement 2+ times per week",
      "priority": "high"
    }
  ],
  "confidence": 87
}
```

---

### 3.3 Chronobiologist

**ID**: `lifestyle_chronobiologist`
**Role**: Circadian Rhythm Optimization & Time-of-Day Effects
**Tier**: 3 (Lifestyle)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Sleep/wake times, circadian phase
- Meal timing relative to circadian rhythm
- Light exposure (morning sunlight, evening blue light)
- Activity timing (exercise time of day)
- Seasonal patterns (if multi-year data)
- Work schedule (shift work, jet lag history)

**Output Schema:**
```json
{
  "circadian_assessment": {
    "circadian_alignment": "good",
    "optimal_sleep_window": "22:30-06:30",
    "optimal_exercise_time": "15:00-17:00",
    "optimal_meal_timing": "early_dinner_before_19:00"
  },
  "recommendations": [
    {
      "recommendation": "Morning sunlight exposure within 30min of waking",
      "rationale": "Entrain circadian phase, improve alertness",
      "priority": "high"
    },
    {
      "recommendation": "Meal timing: breakfast 7am, lunch 12:30pm, dinner 6:30pm",
      "rationale": "Align with circadian-metabolic optimum",
      "priority": "medium"
    },
    {
      "recommendation": "Exercise afternoon (3-5pm) for best performance",
      "priority": "medium"
    }
  ],
  "confidence": 84
}
```

---

### 3.4 Toxicologist

**ID**: `lifestyle_toxicologist`
**Role**: Environmental Toxin Exposure & Detoxification
**Tier**: 3 (Lifestyle)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Environmental toxin exposures (heavy metals, POPs from history)
- Liver function markers (ALT, AST, GGT, albumin)
- Detoxification gene variants (if genetic data available)
- Home environment assessment (VOCs, mold, off-gassing)
- Water quality (if known)
- Occupational exposures

**Output Schema:**
```json
{
  "toxicology_assessment": {
    "toxic_burden": "moderate",
    "liver_detox_capacity": "adequate",
    "key_exposures": [
      "plastic_food_containers_BPA",
      "non_stick_cookware_PFOA"
    ]
  },
  "recommendations": [
    {
      "recommendation": "Replace plastic food storage with glass",
      "priority": "high"
    },
    {
      "recommendation": "Use cast iron or stainless steel cookware",
      "priority": "high"
    },
    {
      "recommendation": "Sauna 2-3x per week for enhanced detoxification",
      "rationale": "Mobilize fat-soluble toxins, improve elimination",
      "priority": "medium"
    },
    {
      "recommendation": "Liver support: milk thistle, NAC, brassicas",
      "priority": "medium"
    }
  ],
  "confidence": 79
}
```

---

### 3.5 Nutritionist

**ID**: `lifestyle_nutritionist`
**Role**: Nutrition Optimization & Food Synergies
**Tier**: 3 (Lifestyle)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Dietary intake (macros, micros, from food diary or recall)
- Micronutrient status (vitamin levels, mineral levels)
- Dietary pattern (Mediterranean, ketogenic, vegan, etc.)
- Food allergies/intolerances
- Digestive function (GI symptoms, gut health)
- Supplement interactions with food

**Output Schema:**
```json
{
  "nutrition_assessment": {
    "macronutrient_balance": "good",
    "micronutrient_status": "mostly_adequate",
    "vitamin_d": "suboptimal_25ng_ml",
    "magnesium": "suboptimal_based_on_markers",
    "dietary_pattern_adherence": "mediterranean_85%"
  },
  "recommendations": [
    {
      "recommendation": "Increase magnesium-rich foods: spinach, pumpkin seeds, almonds",
      "priority": "high"
    },
    {
      "recommendation": "Vitamin D3 4000 IU daily (recheck levels in 3mo)",
      "priority": "high"
    },
    {
      "recommendation": "Maintain current high vegetable intake (good fiber, polyphenols)",
      "priority": "maintenance"
    },
    {
      "recommendation": "Protein at each meal for muscle maintenance",
      "priority": "high"
    }
  ],
  "confidence": 90
}
```

---

## Tier 4: Executors (2 Agents)

**Sequential execution**: After CMO approval
**Output**: Actionable execution plans

### 4.1 Fitness Trainer

**ID**: `executor_fitness`
**Role**: Exercise Prescription & Training Schedule
**Tier**: 4 (Execution)
**Model**: Claude Sonnet 4.6

**Input Data:**
- CMO-approved fitness recommendations
- User fitness level, past injuries
- Available equipment, gym access
- Time constraints
- Preferences (solo vs. group, indoor vs. outdoor)

**Output Schema:**
```json
{
  "fitness_plan": {
    "weekly_schedule": {
      "monday": {
        "activity": "running",
        "duration_min": 30,
        "intensity": "zone_2_easy_pace",
        "description": "120-135 bpm, conversational pace"
      },
      "tuesday": {
        "activity": "strength_training",
        "duration_min": 45,
        "focus": "lower_body",
        "exercises": [
          "squats_4x8",
          "deadlifts_3x5",
          "leg_press_3x10"
        ]
      },
      "wednesday": {
        "activity": "cycling",
        "duration_min": 30,
        "intensity": "zone_3",
        "terrain": "flat"
      },
      "thursday": "rest",
      "friday": {
        "activity": "strength_training",
        "duration_min": 45,
        "focus": "upper_body",
        "exercises": [
          "bench_press_4x8",
          "rows_4x8",
          "shoulder_press_3x8"
        ]
      },
      "saturday": {
        "activity": "hiking",
        "duration_min": 90,
        "intensity": "zone_2_moderate",
        "terrain": "varied_elevation"
      },
      "sunday": "rest"
    },
    "progression_schedule": {
      "weeks_1_2": "adaptation_phase",
      "weeks_3_4": "increase_volume_10%",
      "weeks_5_8": "periodization_with_deload"
    },
    "equipment_needed": [
      "running_shoes",
      "dumbbells",
      "pull_up_bar",
      "bicycle"
    ]
  }
}
```

---

### 4.2 Nutritionist (Executor)

**ID**: `executor_nutritionist`
**Role**: Meal Planning & Supplement Stack
**Tier**: 4 (Execution)
**Model**: Claude Sonnet 4.6

**Input Data:**
- CMO-approved nutrition plan
- User food preferences, restrictions
- Cooking skill/time availability
- Budget constraints
- Food access (grocery stores, markets)
- Supplement plan from Analyst

**Output Schema:**
```json
{
  "nutrition_plan": {
    "meal_structure": {
      "breakfast_7am": {
        "option_1": {
          "foods": ["3_eggs", "1_slice_toast", "berries_handful", "coffee"],
          "macros": {"protein_g": 18, "fat_g": 10, "carbs_g": 30}
        },
        "option_2": {
          "foods": ["greek_yogurt_150g", "granola_30g", "honey_1tbsp"],
          "macros": {"protein_g": 15, "fat_g": 5, "carbs_g": 35}
        }
      },
      "lunch_12_30pm": {
        "template": "Protein + whole grain + vegetables",
        "examples": [
          {"grilled_chicken_150g": "protein", "quinoa_cup": "carbs", "roasted_vegetables": "fiber_micronutrients"}
        ]
      },
      "dinner_6_30pm": {
        "template": "Fatty fish + sweet potato + greens",
        "example": {
          "salmon_150g": "omega3_protein",
          "sweet_potato_150g": "carbs_potassium",
          "spinach_salad": "micronutrients"
        }
      },
      "snacks": "if_needed: almonds, fruit, protein_shake"
    },
    "supplement_schedule": [
      {
        "supplement": "Omega-3 (EPA+DHA) 2000mg",
        "timing": "with_lunch",
        "frequency": "daily"
      },
      {
        "supplement": "Magnesium glycinate 300mg",
        "timing": "before_bedtime",
        "frequency": "daily"
      },
      {
        "supplement": "Vitamin D3 4000 IU",
        "timing": "with_breakfast",
        "frequency": "daily"
      }
    ],
    "grocery_list": [
      "eggs", "chicken_breast", "salmon_fillet", "greek_yogurt",
      "spinach", "broccoli", "berries", "sweet_potato", "quinoa"
    ],
    "shopping_budget_weekly": "$120"
  }
}
```

---

## Tier 5: Operations & Personalization (3 Agents)

**Sequential execution**: After Executors complete
**Output**: Daily contracts, inventory management, concierge logistics

### 5.1 Dispatcher

**ID**: `ops_dispatcher`
**Role**: Daily Contract Generation, Prioritization
**Tier**: 5 (Operations)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Fitness plan (from Fitness Trainer)
- Nutrition plan (from Nutritionist)
- User schedule (work hours, free time)
- User adherence history (past completion rates)
- Protocol validity dates

**Output Schema:**
```json
{
  "daily_contracts": [
    {
      "date": "2026-03-28",
      "contracts": [
        {
          "id": "contract_morning_exercise",
          "time": "07:00",
          "action": "exercise_30min_running",
          "description": "30 min running at easy pace (zone 2)",
          "priority": 1,
          "points": 5,
          "is_binding": true,
          "longevity_impact_days": 0.15
        },
        {
          "id": "contract_breakfast",
          "time": "07:45",
          "action": "eat_breakfast",
          "description": "3 eggs, toast, berries, coffee",
          "priority": 2,
          "points": 2,
          "is_binding": false,
          "longevity_impact_days": 0.02
        },
        {
          "id": "contract_supplements_breakfast",
          "time": "07:45",
          "action": "take_supplements",
          "description": "Vitamin D3 4000 IU with breakfast",
          "priority": 2,
          "points": 1,
          "is_binding": false,
          "longevity_impact_days": 0.01
        },
        {
          "id": "contract_lunch",
          "time": "12:30",
          "action": "eat_lunch",
          "description": "Grilled chicken 150g, quinoa, roasted vegetables",
          "priority": 2,
          "points": 2,
          "is_binding": false,
          "longevity_impact_days": 0.02
        },
        {
          "id": "contract_supplements_lunch",
          "time": "12:30",
          "action": "take_supplements",
          "description": "Omega-3 2000mg with lunch",
          "priority": 2,
          "points": 1,
          "is_binding": false,
          "longevity_impact_days": 0.03
        },
        {
          "id": "contract_evening",
          "time": "19:00",
          "action": "prepare_dinner",
          "description": "Salmon 150g, sweet potato, spinach salad",
          "priority": 2,
          "points": 2,
          "is_binding": false,
          "longevity_impact_days": 0.02
        },
        {
          "id": "contract_sleep_hygiene",
          "time": "22:00",
          "action": "sleep_hygiene",
          "description": "Dim lights, cool room 65F, magnesium 300mg supplement",
          "priority": 2,
          "points": 3,
          "is_binding": false,
          "longevity_impact_days": 0.05
        }
      ],
      "total_possible_points": 16,
      "total_longevity_impact_days": 0.30
    }
  ]
}
```

---

### 5.2 Inventory Manager

**ID**: `ops_inventory`
**Role**: Supplement Ordering, Stock Tracking
**Tier**: 5 (Operations)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Supplement plan (from Executor Nutritionist)
- Current inventory (supplement_inventory table)
- Supplier options (pricing, delivery times)
- User auto-reorder preferences

**Output Schema:**
```json
{
  "inventory_actions": {
    "to_reorder": [
      {
        "supplement": "Omega-3 (EPA+DHA)",
        "brand": "Nordic Naturals",
        "dosage": "1000mg",
        "units_needed": 60,
        "reason": "Current stock 12 units, expires 2026-09-15",
        "supplier": "Amazon",
        "cost_per_unit": "$0.45",
        "delivery_days": 2,
        "recommended_order": true
      }
    ],
    "stock_levels": {
      "NAD+_500mg": {
        "current": 30,
        "monthly_consumption": 30,
        "reorder_threshold": 10,
        "status": "adequate"
      }
    },
    "expiry_alerts": [
      {
        "supplement": "Magnesium glycinate",
        "expiry_date": "2026-04-30",
        "days_remaining": 34,
        "units": 45,
        "action": "use_by_expiry_or_reorder"
      }
    ]
  }
}
```

---

### 5.3 Concierge

**ID**: `ops_concierge`
**Role**: Human-in-the-Loop Coordination, Lifestyle Logistics
**Tier**: 5 (Operations)
**Model**: Claude Sonnet 4.6

**Input Data:**
- Full protocol (all tiers' outputs)
- User engagement level, past adherence
- Escalations from other agents
- Any manual override requests from user

**Output Schema:**
```json
{
  "concierge_services": {
    "physician_consultations_needed": [
      {
        "specialty": "cardiology",
        "reason": "Statin therapy review for suboptimal ApoB",
        "urgency": "within 7 days",
        "suggested_questions": [
          "Is my current statin dose appropriate for my ApoB?",
          "Should I switch to a more potent statin?",
          "What are my options for non-statin therapy?"
        ]
      }
    ],
    "lifestyle_coaching": [
      {
        "topic": "Exercise adherence",
        "approach": "Gamification: award points for completed workouts",
        "milestones": ["1 week consistent", "1 month consistent", "90 days consistent"]
      }
    ],
    "support_resources": [
      {
        "resource": "Meal prep guides",
        "link": "in-app://meal_prep_videos"
      }
    ],
    "check_in_schedule": [
      {
        "week": 1,
        "message": "Great start! How are the new routines feeling?"
      },
      {
        "month": 1,
        "message": "Congratulations on 1 month! Let's review progress."
      }
    ]
  }
}
```

---

## Tier 6: UX & Support (5 Agents)

**Async execution**: Non-blocking support functions
**Output**: User engagement, quality assurance, analytics

### 6.1 UX Designer

**ID**: `ux_designer`
**Role**: Dashboard Insights, Engagement Nudges
**Tier**: 6 (UX)
**Model**: Claude Sonnet 4.6

**Input Data:**
- User behavior analytics (app usage, contract completion)
- Protocol recommendations
- Longevity score trends
- Milestone achievements

**Output Schema:**
```json
{
  "ux_recommendations": {
    "dashboard_widgets": [
      {
        "widget": "Today's contracts",
        "prominence": "hero",
        "content": "Highlight 3 priority actions with progress bars"
      },
      {
        "widget": "Longevity score",
        "prominence": "secondary",
        "trend": "improving",
        "trend_icon": "📈"
      }
    ],
    "engagement_nudges": [
      {
        "trigger": "contract_completion_milestone",
        "milestone": "10 consecutive days",
        "message": "🎉 Amazing! You're building momentum. Keep it up!",
        "reward": "unlock_badge_10_day_streak"
      }
    ]
  }
}
```

### 6.2-6.5 Other Tier 6 Agents

(QA Tester, Developer, Support Agent, Data Analyst) — Similar structures for validation, integration testing, FAQ management, and analytics.

---

## Special Mechanics

### Veto Loop (Verifier)

```
Tier 2 Medical Core
        ↓ (opinions)
Tier 1 Analyst
        ↓ (draft protocol)
Tier 1 Verifier
        ↓
    Verdict?
    ├─ "Approved" → proceed to CMO
    ├─ "Needs Revision" → Feedback to Analyst
    └─ "Vetoed" (veto_count < 3)
        ├─ Send feedback to Tier 2
        ├─ Tier 2 re-analyzes with new context
        ├─ Analyst re-synthesizes
        ├─ Verifier re-checks
        └─ Loop (max 3 times total)

If veto_count >= 3:
    └─ Escalate to CMO for final decision
```

### Parallel Fan-Out (Tier 2 & 3)

```
System Biologist
    ├─ Add edge → Medical Core (Tier 2)
    │   ├─ Cardiologist (parallel)
    │   ├─ Endocrinologist (parallel)
    │   ├─ Metabolologist (parallel)
    │   ├─ Geneticist (parallel)
    │   ├─ Dermatologist (parallel)
    │   ├─ Orthopedist (parallel)
    │   ├─ Microbiome Specialist (parallel)
    │   └─ Aesthetist (parallel)
    │
    ├─ Add edge → Lifestyle (Tier 3)
    │   ├─ Sleep Specialist (parallel)
    │   ├─ Neuropsychologist (parallel)
    │   ├─ Chronobiologist (parallel)
    │   ├─ Toxicologist (parallel)
    │   └─ Nutritionist (parallel)
    │
    └─ Analyst waits for both to complete
       (medical_opinions += [...], lifestyle_opinions += [...])
```

### Human-in-the-Loop

When protocol recommends:
- Prescription change (statin dose, add new medication)
- Surgical intervention (joint surgery, cardiovascular procedure)
- Experimental treatment
- High-risk supplement combinations

→ Concierge escalates to user for physician consultation before approval

---

## North Star Metrics

### 1. DunedinPACE Biological Aging Rate
- Measures rate of biological aging
- Target: <1.0 (aging slower than chronological time)
- 27 epigenetic markers tracked
- Recalculated annually

### 2. Biological Age
- Current estimate from System Biologist
- Target: Chronological age - 5 years or more
- Formula: Baseline epigenetic age + DunedinPACE × time_elapsed

### 3. Healthspan Forecast
- Years of healthy life remaining
- Target: Increase by 5+ years in 12 months with protocol adherence
- Based on mortality risk models + system scores

### 4. Longevity Score
- 0-100 composite metric
- Weighted average of 11 system scores
- Target: 70+ at baseline, 80+ within 12 months of protocol adherence

---

## Integration Points

### Knowledge Base (pgvector)
- Verifier searches embeddings for clinical evidence
- Semantic search: drug interactions, contraindications, supplement synergies
- Updated monthly with latest meta-analyses

### Biomarker Database (PostgreSQL + TimescaleDB)
- System Biologist queries all markers for user
- Time-bucketed aggregation for trends
- Hypertables optimize queries on (time, user_id)

### Celery Background Tasks
- Individual agent execution queued if needed for async updates
- Tier 2-3 agents run in parallel via LangGraph (not Celery)
- Only Tier 4-5 operations might use Celery for external integrations

### WebSocket Events
- Real-time pipeline progress to frontend
- Each tier completion triggers WebSocket emit
- Allows live dashboard updates during orchestration

---

## Prompt Engineering Best Practices

1. **System Prompt Structure**:
   ```
   You are a specialized medical AI assistant: [Specialty]
   Role: [Specific responsibility]

   You have deep expertise in:
   - [Domain 1]
   - [Domain 2]
   - [Domain 3]

   Your output should be JSON with the following schema: [schema]
   ```

2. **Context Injection**: Each agent receives relevant context before query:
   ```json
   {
     "digital_twin": {...},
     "user_profile": {...},
     "biomarkers": [...],
     "other_agent_opinions": [...]
   }
   ```

3. **Confidence Scoring**: Each agent rates confidence 0-100
   - Enables downstream filtering and retry logic
   - Low confidence (<70) may trigger escalation

4. **Token Optimization**:
   - Cache system prompts across sessions
   - Reuse agent definitions (don't regenerate each run)
   - Batch similar queries when possible
