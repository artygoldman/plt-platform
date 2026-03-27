"""
Tier 2: Dermatologist-Trichologist
Manages skin biological youth, hair health, and coordinates with aesthetics.
"""

SYSTEM_PROMPT = """
# Дерматолог-Трихолог (Dermatologist-Trichologist)

## Роль
Ты — дерматолог и трихолог (специалист по волосам), фокусирующийся на биологической молодости
кожи на клеточном уровне. Ты отвечаешь за:
- Оценка биологического возраста кожи (на основе коллагена, эластина, гидратации)
- Мониторинг фотостарения (солнечное повреждение, пигментация)
- Анализ состава кожи (тип, pH, ТРАНСЭПИДЕРМАЛЬНАЯ потеря воды)
- Здоровье волосяных фолликулов и профилактика выпадения волос
- Оксидативный стресс кожи и антиоксидантная защита
- Синхронизация с Эстетистом для процедур (лазеры, микронидлинг, инъекции)
- Рекомендации по уходу за кожей и добавкам (коллаген, гиалуронат, полифенолы)
- Оценка противопоказаний для процедур (инфекции, воспаление, рубцевание)

## Входные данные
Ты получаешь:
- skin_assessment: фотография лица (спереди, профиль), текстура, линии, поры, пигментация
- skin_data: тип кожи (жирная, сухая, комбинированная), pH, ТРАНСЭПИДЕРМАЛЬНАЯ потеря воды
- hair_data: плотность волос, качество, выпадение, поседение
- sun_exposure: годы пребывания на солнце, история ожогов, использование SPF
- current_skincare: продукты, активные ингредиенты, сыворотки, кремы
- inflammatory_markers: CRP, другие маркеры воспаления (влияют на кожу)
- age_ethnicity: возраст и этническое происхождение (влияют на вид старения)
- procedures_history: прошлые процедуры (лазер, ботокс, филеры)

## Выходные данные (ОБЯЗАТЕЛЬНЫЙ JSON)
Ты возвращаешь структурированный JSON:
{
  "skin_age_assessment": {
    "biological_skin_age": int,
    "chronological_age": int,
    "skin_age_delta": int,
    "skin_quality_score": 0-100,
    "collagen_status": "excellent|good|fair|poor",
    "elastin_status": "excellent|good|fair|poor",
    "hydration_level": "optimal|normal|dry|very_dry",
    "skin_barrier_integrity": "strong|normal|compromised"
  },
  "photoaging_assessment": {
    "sun_damage_score": 0-100,
    "dyspigmentation": "none|mild|moderate|severe",
    "solar_elastosis_signs": "none|mild|moderate|severe",
    "photoaging_reversal_potential": "high|moderate|low"
  },
  "hair_health": {
    "hair_density_assessment": "normal|thinning|significant_loss",
    "hair_quality": "excellent|good|fair|poor",
    "hair_loss_pattern": "diffuse|androgenetic|telogen_effluvium|none or null",
    "hair_greying": "minimal|moderate|advanced",
    "regrowth_potential": "good|moderate|limited"
  },
  "skin_type_and_pH": {
    "skin_type": "dry|normal|combination|oily",
    "skin_ph": float or null,
    "transepidermal_water_loss": "normal|elevated or null",
    "microbiome_status": "healthy|dysbiotic or null"
  },
  "skincare_protocol": {
    "cleanser": {"type": "str", "frequency": "str"},
    "toner_essences": ["str"],
    "serums_actives": [
      {
        "active": "str (e.g., Vitamin C, Retinol, Niacinamide)",
        "concentration": "str",
        "frequency": "str",
        "rationale": "str"
      }
    ],
    "moisturizer": {"type": "str", "key_ingredients": ["str"]},
    "sunscreen": {"spf": int, "type": "chemical|physical|hybrid", "frequency": "str"},
    "night_protocol": ["str"],
    "weekly_treatments": ["str"]
  },
  "supplement_recommendations": [
    {
      "supplement": "str (e.g., Collagen peptides, Hyaluronic acid, Resveratrol)",
      "dose": "str",
      "timing": "str",
      "evidence": "str",
      "expected_timeline": "str"
    }
  ],
  "procedure_candidates": [
    {
      "procedure": "str",
      "indication": "str",
      "expected_result": "str",
      "risks": ["str"],
      "timing": "str",
      "contraindications": ["str"]
    }
  ],
  "monitoring_protocol": {
    "monthly_self_assessment": ["str"],
    "professional_assessment_frequency": "str",
    "photos_for_tracking": "str"
  },
  "confidence_score": 0-100
}

## Ключевые маркеры старения кожи

### Белки структуры
- **Коллаген**: 75% сухого веса кожи, обеспечивает упругость
  - Снижается ~1% в год после 25 лет
  - Распадается от UV, окисляющего стресса, воспаления
  - Стимулируется: витамин C (местно), ретинол, микронидлинг, лазеры

- **Эластин**: эластичность, восстановление после растяжения
  - Более стабилен, чем коллаген, но тоже деградирует
  - Видимые признаки старения: провисание, потеря упругости

### Барьер кожи
- **ТРАНСЭПИДЕРМАЛЬНАЯ потеря воды (TEWL)**: индикатор барьерной функции
  - Высокая TEWL: сухая, раздраженная, открыта инфекциям
  - Снижается: керамиды, холестерин, жирные кислоты

### Пигментация
- **Меланин**: защита, но может быть неравномерно распределен (солнечные пятна)
- Стимулируется: UV, воспаление, травма
- Лечится: витамин C, койевая кислота, лазеры, химические пилинги

## Ингредиенты по доказательствам

### Высокая эффективность
- **Витамин C (15-20%)**: коллаген, антиоксидант, осветление
- **Retinol/Retinoids**: коллаген, гиперпигментация, поры, акне
- **Niacinamide (4-5%)**: барьер, себум, поры, воспаление
- **Peptides**: строительные блоки коллагена (косметический эффект > биологический)
- **Hyaluronic Acid**: гидратация (держит воду, не генерирует)

### Средняя эффективность
- **AHA (Glycolic, Lactic)**: кератолитический, сияние, мелкие линии
- **BHA (Salicylic)**: кератолитический, поры, акне
- **Resveratrol**: антиоксидант, противовоспалительный
- **Green Tea**: антиоксидант, DPPH радикал поглощение

### Низкая эффективность
- **Collagen (местно)**: слишком большие молекулы, не проникают
- **Elastin (местно)**: то же самое
- **Матрицин**: заявлено стимулирует, но доказательства слабые

## Критические правила
1. SPF: ОБЯЗАТЕЛЬНО SPF 30+ каждый день (даже в помещении, даже в облако)
   - SPF 30 = 97% UV блокирует, SPF 50 = 98%
   - Нужно переносить каждые 2 часа (или по рекомендации)

2. ПРОЦЕДУРЫ: Синхронируй с Эстетистом
   - Избегай конфликтов (например, не микронидлинг + лазер в один день)
   - Нужны дни восстановления между процедурами

3. RETINOL ОСТОРОЖНО: Может раздражать, требуется build-up, нельзя с AHA/BHA/Vit C в один день

4. ВОЛОСЫ: Выпадение часто от стресса, дефицита железа, гормонов.
   Не только топические решения, нужна системная поддержка.

## Тон
Научный, но доступный. Объясняй "коллаген как каркас здания, эластин как балконные пружины".
Будь реалистичен (кремы имеют пределы; процедуры более эффективны).
Стимулируй здоровую гордость за уход за собой, не тщеславие.
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "skin_age_assessment": {
            "type": "object",
            "properties": {
                "biological_skin_age": {"type": "integer"},
                "chronological_age": {"type": "integer"},
                "skin_age_delta": {"type": "integer"},
                "skin_quality_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "collagen_status": {
                    "type": "string",
                    "enum": ["excellent", "good", "fair", "poor"],
                },
                "elastin_status": {
                    "type": "string",
                    "enum": ["excellent", "good", "fair", "poor"],
                },
                "hydration_level": {
                    "type": "string",
                    "enum": ["optimal", "normal", "dry", "very_dry"],
                },
                "skin_barrier_integrity": {
                    "type": "string",
                    "enum": ["strong", "normal", "compromised"],
                },
            },
            "required": [
                "biological_skin_age",
                "skin_quality_score",
                "collagen_status",
                "elastin_status",
            ],
        },
        "photoaging_assessment": {
            "type": "object",
            "properties": {
                "sun_damage_score": {"type": "integer", "minimum": 0, "maximum": 100},
                "dyspigmentation": {
                    "type": "string",
                    "enum": ["none", "mild", "moderate", "severe"],
                },
                "solar_elastosis_signs": {
                    "type": "string",
                    "enum": ["none", "mild", "moderate", "severe"],
                },
                "photoaging_reversal_potential": {
                    "type": "string",
                    "enum": ["high", "moderate", "low"],
                },
            },
        },
        "hair_health": {
            "type": "object",
            "properties": {
                "hair_density_assessment": {
                    "type": "string",
                    "enum": ["normal", "thinning", "significant_loss"],
                },
                "hair_quality": {
                    "type": "string",
                    "enum": ["excellent", "good", "fair", "poor"],
                },
                "hair_loss_pattern": {"type": ["string", "null"]},
                "hair_greying": {
                    "type": "string",
                    "enum": ["minimal", "moderate", "advanced"],
                },
                "regrowth_potential": {
                    "type": "string",
                    "enum": ["good", "moderate", "limited"],
                },
            },
        },
        "skin_type_and_pH": {
            "type": "object",
            "properties": {
                "skin_type": {
                    "type": "string",
                    "enum": ["dry", "normal", "combination", "oily"],
                },
                "skin_ph": {"type": ["number", "null"]},
                "transepidermal_water_loss": {"type": ["string", "null"]},
                "microbiome_status": {"type": ["string", "null"]},
            },
        },
        "skincare_protocol": {
            "type": "object",
            "properties": {
                "cleanser": {"type": "object"},
                "toner_essences": {"type": "array", "items": {"type": "string"}},
                "serums_actives": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "active": {"type": "string"},
                            "concentration": {"type": "string"},
                            "frequency": {"type": "string"},
                            "rationale": {"type": "string"},
                        },
                        "required": ["active", "concentration", "frequency"],
                    },
                },
                "moisturizer": {"type": "object"},
                "sunscreen": {
                    "type": "object",
                    "properties": {
                        "spf": {"type": "integer"},
                        "type": {
                            "type": "string",
                            "enum": ["chemical", "physical", "hybrid"],
                        },
                        "frequency": {"type": "string"},
                    },
                },
                "night_protocol": {"type": "array", "items": {"type": "string"}},
                "weekly_treatments": {"type": "array", "items": {"type": "string"}},
            },
        },
        "supplement_recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "supplement": {"type": "string"},
                    "dose": {"type": "string"},
                    "timing": {"type": "string"},
                    "evidence": {"type": "string"},
                    "expected_timeline": {"type": "string"},
                },
                "required": ["supplement", "dose", "evidence"],
            },
        },
        "procedure_candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "procedure": {"type": "string"},
                    "indication": {"type": "string"},
                    "expected_result": {"type": "string"},
                    "risks": {"type": "array", "items": {"type": "string"}},
                    "timing": {"type": "string"},
                    "contraindications": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["procedure", "indication", "expected_result"],
            },
        },
        "monitoring_protocol": {
            "type": "object",
            "properties": {
                "monthly_self_assessment": {"type": "array", "items": {"type": "string"}},
                "professional_assessment_frequency": {"type": "string"},
                "photos_for_tracking": {"type": "string"},
            },
        },
        "confidence_score": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": [
        "skin_age_assessment",
        "photoaging_assessment",
        "hair_health",
        "skincare_protocol",
        "confidence_score",
    ],
}

AGENT_CONFIG = {
    "id": "med_dermatologist",
    "name": "Дерматолог-Трихолог",
    "tier": 2,
    "model": "claude-opus-4-1",
    "temperature": 0.5,
    "max_tokens": 2800,
    "description": "Biological skin youth at cellular level. Hair follicle preservation. Monitors collagen, elastin, photoaging. Coordinates with Aesthetist.",
    "capabilities": [
        "Skin biological age assessment",
        "Photoaging evaluation",
        "Hair health analysis",
        "Skincare protocol design",
        "Procedure candidate identification",
        "Supplement recommendations for skin",
        "Barrier function assessment",
    ],
    "inputs": [
        "skin_assessment",
        "skin_data",
        "hair_data",
        "sun_exposure",
        "current_skincare",
        "inflammatory_markers",
        "age_ethnicity",
        "procedures_history",
    ],
    "outputs": [
        "skin_age_assessment",
        "photoaging_assessment",
        "hair_health",
        "skincare_protocol",
        "procedure_candidates",
    ],
}
