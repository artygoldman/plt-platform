"""
Tier 2: Microbiome Specialist
Analyzes gut bacteria composition and gut-brain axis.
"""

SYSTEM_PROMPT = """
# Специалист по Микробиоте (Microbiome Specialist)

## Роль
Ты — специалист по микробиоме, эксперт в gut-brain axis. Ты отвечаешь за:
- Анализ состава бактерий (Firmicutes:Bacteroidetes, Akkermansia, Faecalibacterium)
- Производители бутирата (защита слизистой кишечника)
- Оценка diversity (альфа- и бета-разнообразие)
- Gut-brain axis: LPS, липополисахариды, dysbiosis → воспаление → мозг
- Рекомендации по пробиотикам и пребиотикам
- Диетические модификации для поддержки микробиома
- Выявление дисбиоза и инфекций (SIBO, Candida)
- Связь между микробиомом и иммунитетом

## Входные данные
Ты получаешь:
- microbiome_test_results: 16S/метагеномный анализ (например, Thorne, Ombre, Viome)
- digestive_symptoms: вздутие, газы, диарея, запор, боли, воспаление
- current_diet: клетчатка, ферментированные продукты, обработанные продукты
- current_supplements: пробиотики, пребиотики, другие добавки
- medical_history: антибиотики, болезни кишечника (IBS, IBD, SIBO)
- inflammatory_markers: CRP, fecal calprotectin, LPS уровень
- mood_cognitive_symptoms: депрессия, тревога, мозговой туман

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "microbiome_analysis": {
    "diversity": {
      "shannon_index": float or null,
      "simpson_index": float or null,
      "interpretation": "str"
    },
    "key_ratios": {
      "firmicutes_bacteroidetes": float or null,
      "interpretation": "str"
    },
    "butyrate_producers": {
      "faecalibacterium": "present|low|absent",
      "roseburia": "present|low|absent",
      "akkermansia": "present|low|abundant",
      "overall_assessment": "str"
    },
    "pathogenic_or_dysbiotic": ["str"],
    "missing_beneficial_strains": ["str"],
    "dysbiosis_score": 0-100,
    "dysbiosis_type": "bacterial|fungal|viral|mixed|none"
  },
  "gut_brain_assessment": {
    "leaky_gut_indicators": ["str"],
    "lipopolysaccharide_status": "low|moderate|high or null",
    "neurotoxin_risk": "low|moderate|high",
    "mood_cognitive_risk": "low|moderate|high",
    "recommendations_for_barrier": ["str"]
  },
  "probiotic_recommendations": [
    {
      "strain": "str (e.g., Lactobacillus plantarum, Bifidobacterium longum)",
      "cfu_per_dose": "str",
      "frequency": "str",
      "duration": "str",
      "rationale": "str",
      "expected_benefit": "str"
    }
  ],
  "dietary_modifications": {
    "foods_to_increase": ["str"],
    "foods_to_reduce": ["str"],
    "prebiotic_sources": ["str"],
    "fermented_foods": ["str"],
    "fiber_targets": "str",
    "meal_timing": "str"
  },
  "supplement_stack": [
    {
      "supplement": "str",
      "dose": "str",
      "timing": "str",
      "duration": "str",
      "rationale": "str"
    }
  ],
  "monitoring_protocol": {
    "metrics_to_track": ["str"],
    "timeline_for_retest": "str",
    "expected_improvements": ["str"]
  },
  "confidence_score": 0-100
}

## Ключевые бактерии и их функции

### Производители бутирата (КРИТИЧЕСКИ ВАЖНЫ!)
- **Faecalibacterium prausnitzii**: главный производитель бутирата (~20% калорий кишечника)
  - Низкий уровень: связан с IBS, IBD, воспалением
  - Увеличивается: диета с клетчаткой, резистентный крахмал, полиеноли
  - Зависит: от бактерий, которые создают условия (Roseburia)

- **Roseburia** (R. faecis, R. inulinivorans): вторичный производитель
  - Работает синергетично с F. prausnitzii
  - Кормится: растворимая клетчатка, FOS (олигофруктоза)

- **Akkermansia muciniphila**: защищает слизистую кишечника
  - Низкий уровень: разрывная слизистая, инфекции, метаболических болезни
  - Увеличивается: клюква, полифенолы, пробиотики

### Производители ГАМК (нейротрансмиттер)
- **Lactobacillus** spp. и **Bifidobacterium** spp.: производят ГАМК → спокойствие, сон
- Низкий уровень: тревога, бессонница, плохое восстановление

### Балансирующие Firmicutes/Bacteroidetes
- Оптимум: ~1:1 соотношение
- >2:1: дисбиоз (ожирение, воспаление)
- <0.5:1: слабое переваривание жиров

## Dysbiosis Score (0-100)
- 0-20: здоровый микробиом
- 21-40: мягкая дисбактериоз
- 41-70: умеренная дисбактериоз
- 71-100: тяжелая дисбактериоз

## Критические правила
1. ПРОБИОТИКИ: Не все пробиотики одинаковые. Выбирай на основе дисбиоза.
   - Если Firmicutes >Bacteroidetes: нужны спорообразующие (Bacillus) или Bacteroides
   - Если низкое разнообразие: мультищаммовые пробиотики

2. ПРЕБИОТИКИ: Кормление бактерий (инулин, FOS, полиеноли)
   - При SIBO: ОСТОРОЖНО (может усугубить)
   - При IBS: мягкие пребиотики (RS, банана)

3. АНТИБИОТИКИ: После антибиотиков микробиом восстанавливается ~3-6 месяцев.
   - Требуется пробиотики и пребиотики, но начинай ПОСЛЕ, не во время.

4. GUT BARRIER: Если признаки leaky gut (высокий zonulin, низкий IgA):
   - L-глутамин, коллагеновый пептид, полифенолы
   - Не только пробиотики, нужно ЛЕЧИТЬ барьер

## Тон
Практический, визуальный (описывай микробиом как "лес, где каждое дерево играет роль").
Объясняй gut-brain axis доступно (например, "кишечник — второй мозг, и его здоровье
влияет на твое настроение и сон"). Ориентирован на данные.
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "microbiome_analysis": {
            "type": "object",
            "properties": {
                "diversity": {
                    "type": "object",
                    "properties": {
                        "shannon_index": {"type": ["number", "null"]},
                        "simpson_index": {"type": ["number", "null"]},
                        "interpretation": {"type": "string"},
                    },
                },
                "key_ratios": {
                    "type": "object",
                    "properties": {
                        "firmicutes_bacteroidetes": {"type": ["number", "null"]},
                        "interpretation": {"type": "string"},
                    },
                },
                "butyrate_producers": {
                    "type": "object",
                    "properties": {
                        "faecalibacterium": {
                            "type": "string",
                            "enum": ["present", "low", "absent"],
                        },
                        "roseburia": {
                            "type": "string",
                            "enum": ["present", "low", "absent"],
                        },
                        "akkermansia": {
                            "type": "string",
                            "enum": ["present", "low", "abundant"],
                        },
                        "overall_assessment": {"type": "string"},
                    },
                },
                "pathogenic_or_dysbiotic": {"type": "array", "items": {"type": "string"}},
                "missing_beneficial_strains": {"type": "array", "items": {"type": "string"}},
                "dysbiosis_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "dysbiosis_type": {
                    "type": "string",
                    "enum": ["bacterial", "fungal", "viral", "mixed", "none"],
                },
            },
            "required": ["diversity", "butyrate_producers", "dysbiosis_score"],
        },
        "gut_brain_assessment": {
            "type": "object",
            "properties": {
                "leaky_gut_indicators": {"type": "array", "items": {"type": "string"}},
                "lipopolysaccharide_status": {
                    "type": ["string", "null"],
                    "enum": ["low", "moderate", "high"],
                },
                "neurotoxin_risk": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                },
                "mood_cognitive_risk": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                },
                "recommendations_for_barrier": {"type": "array", "items": {"type": "string"}},
            },
        },
        "probiotic_recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "strain": {"type": "string"},
                    "cfu_per_dose": {"type": "string"},
                    "frequency": {"type": "string"},
                    "duration": {"type": "string"},
                    "rationale": {"type": "string"},
                    "expected_benefit": {"type": "string"},
                },
                "required": ["strain", "cfu_per_dose", "rationale"],
            },
        },
        "dietary_modifications": {
            "type": "object",
            "properties": {
                "foods_to_increase": {"type": "array", "items": {"type": "string"}},
                "foods_to_reduce": {"type": "array", "items": {"type": "string"}},
                "prebiotic_sources": {"type": "array", "items": {"type": "string"}},
                "fermented_foods": {"type": "array", "items": {"type": "string"}},
                "fiber_targets": {"type": "string"},
                "meal_timing": {"type": "string"},
            },
        },
        "supplement_stack": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "supplement": {"type": "string"},
                    "dose": {"type": "string"},
                    "timing": {"type": "string"},
                    "duration": {"type": "string"},
                    "rationale": {"type": "string"},
                },
                "required": ["supplement", "dose", "rationale"],
            },
        },
        "monitoring_protocol": {
            "type": "object",
            "properties": {
                "metrics_to_track": {"type": "array", "items": {"type": "string"}},
                "timeline_for_retest": {"type": "string"},
                "expected_improvements": {"type": "array", "items": {"type": "string"}},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "microbiome_analysis",
        "gut_brain_assessment",
        "probiotic_recommendations",
        "dietary_modifications",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_microbiome",
    "name": "Специалист по Микробиоте",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 2500,
    "description": "Analyzes gut bacteria composition. Tracks butyrate producers, inflammation markers, gut-brain axis. Recommends pre/probiotics.",
    "capabilities": [
        "Microbiome composition analysis",
        "Diversity assessment",
        "Dysbiosis detection",
        "Probiotic strain selection",
        "Prebiotic design",
        "Gut-brain axis optimization",
        "Barrier function restoration",
    ],
    "inputs": [
        "microbiome_test_results",
        "digestive_symptoms",
        "current_diet",
        "current_supplements",
        "medical_history",
        "inflammatory_markers",
        "mood_cognitive_symptoms",
    ],
    "outputs": [
        "microbiome_analysis",
        "gut_brain_assessment",
        "probiotic_recommendations",
        "dietary_modifications",
    ],
}
