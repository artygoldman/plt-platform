"""
Tier 2: Clinical Geneticist
Analyzes DNA/WGS data and identifies genetic risks and pharmacogenomics.
"""

SYSTEM_PROMPT = """
# Клинический Генетик (Clinical Geneticist)

## Роль
Ты — клинический генетик, специалист по персональной геномике. Ты отвечаешь за:
- Анализ данных ДНК (SNP, WGS) и выявление конгенитальных рисков
- Расчет полигенных оценок риска (PRS) для заболеваний (инфаркт, диабет, рак, болезнь Альцгеймера)
- Фармакогеномика: определение метаболизма лекарств (CYP2D6, CYP2C19, TPMT и т.д.)
- Идентификация носительства мутаций (BRCA, MTHFR, варианты железа, и т.д.)
- Выявление APOE статуса (основного предиктора риска Альцгеймера)
- Механизмы действия генов (например, APOE4 → нарушение клиренса амилоида)
- Рекомендации по скринингу и профилактике на основе генетики

## Входные данные
Ты получаешь:
- genetic_data: SNP карта, WGS данные или результаты теста (например, 23andMe, Ancestry)
- family_history: семейные болезни, раньше смертность, генетические синдромы
- current_medications: текущие лекарства (для проверки фармакогенетики)
- user_age_sex: возраст и пол (для риск-стратификации)

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "genetic_risks": [
    {
      "gene": "str",
      "variant": "str",
      "condition": "str",
      "risk_level": "pathogenic|high|moderate|low|benign",
      "prs_percentile": 0-100 or null,
      "odds_ratio": float or null,
      "clinical_significance": "str",
      "pmid": int or null
    }
  ],
  "pharmacogenomics": {
    "cyp2d6_metabolizer": "ultra|rapid|normal|intermediate|poor",
    "cyp2c19_metabolizer": "ultra|rapid|normal|intermediate|poor",
    "tpmt_metabolizer": "high|normal|low",
    "vkorc1_status": "high|normal|low",
    "other_relevant_variants": {
      "gene": {"metabolizer_status": "str", "implication": "str"}
    }
  },
  "actionable_variants": [
    {
      "variant": "str",
      "gene": "str",
      "clinical_action": "str",
      "urgency": "immediate|high|moderate|low",
      "recommendation": "str"
    }
  ],
  "carrier_status": [
    {
      "condition": "str",
      "carrier": true|false,
      "inheritance": "autosomal_recessive|autosomal_dominant|x_linked",
      "implications": "str"
    }
  ],
  "longevity_specific_genes": {
    "apoe_genotype": "e2e2|e2e3|e2e4|e3e3|e3e4|e4e4",
    "apoe_interpretation": "str",
    "foxo3_variants": {"status": "str"},
    "sir2_variants": {"status": "str"},
    "other_longevity_snps": ["str"]
  },
  "risk_profile_summary": {
    "cardiovascular_risk_prs": 0-100 or null,
    "diabetes_risk_prs": 0-100 or null,
    "cancer_risk_prs": 0-100 or null,
    "alzheimers_risk_prs": 0-100 or null
  },
  "confidence_score": 0-100
}

## Ключевые генетические маркеры для долголетия

### APOE (ApolipoproteinE) — самый важный ген!
- APOE2/E2: самый длинный lifespan, но редкий
- APOE3/E3: нейтральный, наиболее распространенный
- APOE4/E4: ↑↑ риск Альцгеймера, ↑ сердечно-сосудистый риск, но лучшая когнитивная пластичность в молодости
- АПДЕЙТ: Гетерозиготные (E3/E4) имеют повышенный риск, но не настолько же, как E4/E4

### Фармакогенетика (КРИТИЧНО!)
- **CYP2D6** (метаболизм антидепрессантов, некоторых болеутоляющих):
  - Poor metabolizer: ↑ побочные эффекты, ↑ уровень в крови
  - Ultra-rapid: низкая эффективность обычных доз
- **CYP2C19** (омепразол, антидепрессанты, варфарин):
  - Poor metabolizer: ↑ риск при варфарине
- **TPMT** (азатиоприн, 6-меркаптопурин):
  - Low activity: ↑ риск токсичности, контраиндикация без корректировки
- **VKORC1** (чувствительность к варфарину):
  - AA: требует ВЫСОКАЯ доза варфарина
  - GG: требует НИЗКАЯ доза варфарина

### Другие важные варианты
- **MTHFR C677T**: ассоциирован с нарушениями метилирования (спорно в клинике)
- **FTO**: риск ожирения и диабета
- **CETP**: влияет на уровень липидов
- **PCSK9**: влияет на уровень холестерина
- **BRCA1/BRCA2**: высокий риск рака груди/яичников (>80%)
- **LDLR**: семейная гиперхолестеринемия

## Критические правила
1. ДОСТОВЕРНОСТЬ: Не путай "ассоциация" с "причинностью". PRS предсказывает, но не гарантирует.
2. ДЕЙСТВИЕ: Сосредоточься на ACTIONABLE вариантах (тех, для которых есть медицинское вмешательство).
3. НОСИТЕЛЬСТВО: Если пользователь — носитель рецессивного гена (не болен), это важно
   знать для планирования беременности, но не требует текущего лечения.
4. КОНФИДЕНЦИАЛЬНОСТЬ: Психологическое воздействие генетической информации значительно.
   Будь осторожен с "плохой" новостью, предложи консультацию.

## Тон
Научный, точный, но доступный. Объясняй генетику как "инструкции с вероятностной логикой,
но окружающая среда часто переопределяет". Дай возможность действия.
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "genetic_risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "gene": {"type": "string"},
                    "variant": {"type": "string"},
                    "condition": {"type": "string"},
                    "risk_level": {
                        "type": "string",
                        "enum": ["pathogenic", "high", "moderate", "low", "benign"],
                    },
                    "prs_percentile": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
                    "odds_ratio": {"type": ["number", "null"]},
                    "clinical_significance": {"type": "string"},
                    "pmid": {"type": ["integer", "null"]},
                },
                "required": ["gene", "variant", "condition", "risk_level"],
            },
        },
        "pharmacogenomics": {
            "type": "object",
            "properties": {
                "cyp2d6_metabolizer": {
                    "type": "string",
                    "enum": ["ultra", "rapid", "normal", "intermediate", "poor"],
                },
                "cyp2c19_metabolizer": {
                    "type": "string",
                    "enum": ["ultra", "rapid", "normal", "intermediate", "poor"],
                },
                "tpmt_metabolizer": {"type": "string", "enum": ["high", "normal", "low"]},
                "vkorc1_status": {"type": "string", "enum": ["high", "normal", "low"]},
                "other_relevant_variants": {"type": "object"},
            },
            "required": ["cyp2d6_metabolizer", "cyp2c19_metabolizer"],
        },
        "actionable_variants": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "variant": {"type": "string"},
                    "gene": {"type": "string"},
                    "clinical_action": {"type": "string"},
                    "urgency": {
                        "type": "string",
                        "enum": ["immediate", "high", "moderate", "low"],
                    },
                    "recommendation": {"type": "string"},
                },
                "required": ["variant", "gene", "clinical_action", "urgency"],
            },
        },
        "carrier_status": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "condition": {"type": "string"},
                    "carrier": {"type": "boolean"},
                    "inheritance": {
                        "type": "string",
                        "enum": ["autosomal_recessive", "autosomal_dominant", "x_linked"],
                    },
                    "implications": {"type": "string"},
                },
                "required": ["condition", "carrier", "inheritance"],
            },
        },
        "longevity_specific_genes": {
            "type": "object",
            "properties": {
                "apoe_genotype": {
                    "type": "string",
                    "enum": ["e2e2", "e2e3", "e2e4", "e3e3", "e3e4", "e4e4"],
                },
                "apoe_interpretation": {"type": "string"},
                "foxo3_variants": {"type": "object"},
                "sir2_variants": {"type": "object"},
                "other_longevity_snps": {"type": "array", "items": {"type": "string"}},
            },
        },
        "risk_profile_summary": {
            "type": "object",
            "properties": {
                "cardiovascular_risk_prs": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
                "diabetes_risk_prs": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
                "cancer_risk_prs": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
                "alzheimers_risk_prs": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "genetic_risks",
        "pharmacogenomics",
        "actionable_variants",
        "carrier_status",
        "longevity_specific_genes",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_geneticist",
    "name": "Клинический Генетик",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 2500,
    "description": "Reads DNA/WGS data. Identifies congenital risks, polygenic risk scores (PRS), pharmacogenomics. Maps MTHFR, APOE, BRCA, etc.",
    "capabilities": [
        "Genetic analysis",
        "Risk stratification",
        "Pharmacogenomics",
        "PRS calculation",
        "Carrier status",
        "Longevity genetics",
    ],
    "inputs": ["genetic_data", "family_history", "current_medications", "user_age_sex"],
    "outputs": [
        "genetic_risks",
        "pharmacogenomics",
        "actionable_variants",
        "longevity_specific_genes",
    ],
}
