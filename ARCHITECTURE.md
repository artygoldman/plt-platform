# PLT Platform Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Applications                            │
│              (Web Dashboard, Mobile, Third-party Apps)              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FastAPI REST API Layer                            │
│   ┌──────────┬────────┬──────┬───────┬──────────┬──────────┐        │
│   │ Users    │ Data   │ Twin │Agents │Contracts │Protocols │        │
│   │ Routers  │ Router │Router│Router │ Router   │ Router   │        │
│   └────┬─────┴────┬───┴──┬───┴───┬───┴───┬──────┴────┬─────┘        │
│        └─────────────────┼────────┼───────┼──────────┘              │
│                          │        │       │                         │
│   JWT Middleware  ◄─────┴─┐      │       │                         │
│   CORS Middleware         │      │       │                         │
└──────────────────────────┬┼──────┼───────┼─────────────────────────┘
                           ││      │       │
         ┌─────────────────┘│      │       │
         │                  │      │       │
         ▼                  ▼      ▼       ▼
┌────────────────────────────────────────────────────────────────────┐
│          LangGraph Orchestration Engine (State Machine)             │
│                                                                     │
│   Entry: Router Node ──┐                                           │
│                         │                                          │
│                    ┌────▼───────────────────┐                      │
│                    │  System Biologist      │ Builds Digital Twin  │
│                    │  (Tier 1)              │                      │
│                    └────┬──────────────────┘                       │
│                         │                                          │
│        ┌────────────────┴────────────────┐                         │
│        │                                 │                         │
│   ┌────▼────────┐              ┌────────▼────────┐                │
│   │Medical Core │              │   Lifestyle     │ Parallel       │
│   │(Tier 2: 8)  │              │  (Tier 3: 5)    │ Fan-Out        │
│   ├─Cardiologist├              ├─Sleep Specialist├                │
│   ├─Endocrinolo-├              ├─Neuropsycholog-├                │
│   ├─Metabololog-├              ├─Chronobiologist├                │
│   ├─Geneticist ├              ├─Toxicologist   ├                │
│   ├─Dermatolog-├              └─Nutritionist   ┘                │
│   ├─Orthopedist├                 (Tier 3)                        │
│   ├─Microbiome ├                                                 │
│   └─Aesthetist ┘                                                 │
│   (Tier 2)                                                       │
│        │                                 │                       │
│        └────────────────┬────────────────┘                        │
│                         │ Both complete                           │
│                    ┌────▼─────────────┐                           │
│                    │   Analyst Node   │ Synthesize opinions      │
│                    │   (Tier 1)       │ + ROI analysis            │
│                    └────┬─────────────┘                           │
│                         │                                         │
│                    ┌────▼──────────────┐                          │
│                    │  Verifier Node    │ Check knowledge base     │
│                    │  (Tier 1)         │                          │
│                    └────┬──────────────┘                          │
│                         │                                         │
│              ┌──────────┴──────────┐                              │
│              │ Vetoed?             │ Approved?                   │
│         ┌────▼────┐           ┌────▼────┐                        │
│         │ Loop ◄──┴─(x < 3)   │ Proceed │                        │
│         │ Back to │            │ to CMO  │                        │
│         │Medical  │            └────┬────┘                        │
│         │Core     │                 │                            │
│         └─────────┘            ┌────▼──────────┐                 │
│                                │  CMO Node     │ Final approval  │
│                                │  (Tier 1)     │                 │
│                                └────┬──────────┘                 │
│                                     │                            │
│                            ┌────────▼────────┐                   │
│                            │ Executors Node  │ Translate to     │
│                            │ (Tier 4: 2)     │ executable plans │
│                            ├─Fitness Trainer │                  │
│                            └─Nutritionist    │                  │
│                                (Tier 4)      │                  │
│                                     │        │                  │
│                            ┌────────▼────────┐                   │
│                            │    Ops Node     │ Generate daily   │
│                            │   (Tier 5: 3)   │ contracts        │
│                            ├─Dispatcher      │                  │
│                            ├─Inventory Mgr   │                  │
│                            └─Concierge       │                  │
│                                (Tier 5)      │                  │
│                                              │                  │
│   Checkpointing: PostgreSQL LangGraph      │                  │
│   Thread persistence for resumption        │                  │
│                                              │                  │
└──────────────────────────────────────────────┼──────────────────┘
                                               │
         ┌─────────────────────────────────────┼─────────────────────┐
         │                                     │                     │
         ▼                                     ▼                     ▼
   ┌──────────────┐                    ┌────────────────┐     ┌──────────┐
   │  PostgreSQL  │                    │     Redis      │     │  MinIO   │
   │   16 + TS    │                    │      7-alpine  │     │ S3 API   │
   ├──────────────┤                    ├────────────────┤     ├──────────┤
   │ biomarkers   │                    │ session_cache  │     │ uploads/ │
   │ users        │                    │ pubsub         │     │ exports/ │
   │ protocols    │                    │ job_queue      │     │ files/   │
   │ contracts    │                    │ rate_limiting  │     └──────────┘
   │ agents       │                    │                │
   │ decisions    │                    │ WebSocket→API  │
   │ (hypertables)│                    │ notifications  │
   └──────────────┘                    └────────────────┘
```

## Data Flow: From Upload to Daily Contracts

### 1. User Data Ingestion

```
User uploads blood test PDF
        │
        ▼
POST /api/v1/data/upload
        │
        ▼
[Background Task] Parse PDF
├─ Extract biomarker values
├─ Detect lab-specific reference ranges
├─ Store in biomarkers table
└─ Trigger agent pipeline if new anomalies
        │
        ▼
Biomarker records created in PostgreSQL (hypertable)
├─ time: timestamp of blood draw
├─ user_id: UUID of user
├─ marker_name: "ApoB", "hsCRP", etc.
├─ value: numeric value
├─ reference_low/high: lab normal range
├─ optimal_low/high: longevity-optimized range
└─ metadata: test_id, facility, assay_method
```

### 2. Digital Twin Construction

```
PLTState.trigger_data contains:
{
  "new_biomarkers": [...],
  "anomalies_detected": [
    {"marker": "ApoB", "value": 95, "status": "suboptimal"}
  ],
  "user_id": "uuid-123"
}
        │
        ▼
Router Node → System Biologist Node
        │
        ▼
System Biologist:
1. Queries all recent biomarkers for user
2. Groups by category: lipids, hormones, inflammation, etc.
3. Calculates 11 biological system scores:
   ├─ Cardiovascular (lipids, BP, arterial stiffness)
   ├─ Metabolic (glucose, insulin, mitochondrial markers)
   ├─ Immune (inflammation, infection markers, lymphocytes)
   ├─ Hormonal (cortisol, testosterone, thyroid, estrogen)
   ├─ Neurological (homocysteine, brain-derived neurotrophic factor)
   ├─ Renal (creatinine, eGFR, protein)
   ├─ Hepatic (liver enzymes, albumin)
   ├─ Bone (calcium, phosphate, alkaline phosphatase)
   ├─ Muscular (creatine kinase, muscle mass biomarkers)
   ├─ Sleep & Circadian (melatonin, cortisol rhythm)
   └─ Environmental Resilience (antioxidant capacity, detox markers)
4. Computes biological age using DunedinPACE algorithm
5. Detects anomalies: values outside optimal ranges
6. Identifies cross-system correlations
7. Produces Digital Twin snapshot:
   {
     "timestamp": "2026-03-27T10:30:00Z",
     "biological_age": 42.5,
     "chronological_age": 45.0,
     "system_scores": {
       "cardiovascular": 78,
       "metabolic": 65,
       ...
     },
     "anomalies_detected": [...],
     "trend_analysis": {...}
   }
```

### 3. Parallel Medical & Lifestyle Analysis

```
Medical Core (Tier 2) ──┐
├─ Cardiologist         │
├─ Endocrinologist      │
├─ Metabolologist       │
├─ Geneticist           │
├─ Dermatologist        │
├─ Orthopedist          ├─ Parallel execution
├─ Microbiome Specialist│
└─ Aesthetist           │
                        │
Lifestyle (Tier 3) ────┤
├─ Sleep Specialist     │
├─ Neuropsychologist    │
├─ Chronobiologist      │
├─ Toxicologist         │
└─ Nutritionist         │
                        ▼
            Each agent receives:
            {
              "digital_twin": {...},
              "user_profile": {...},
              "biomarkers": [...],
              "trigger_data": {...}
            }

            Each agent returns:
            {
              "opinion": {
                "findings": "...",
                "recommendations": [...],
                "risk_factors": [...]
              },
              "confidence": 85,
              "tokens_used": 1250
            }

            Results accumulated in PLTState:
            medical_opinions: [
              {"agent_id": "cardiologist", "opinion": {...}, "confidence": 85},
              {"agent_id": "endocrinologist", "opinion": {...}, "confidence": 92},
              ...
            ]
            lifestyle_opinions: [
              {"agent_id": "sleep_specialist", "opinion": {...}, "confidence": 78},
              ...
            ]
```

### 4. Synthesis & Verification

```
Analyst Node (Tier 1)
├─ Input: medical_opinions + lifestyle_opinions
├─ Resolves conflicts: if 2+ agents contradict, applies voting
├─ Prioritizes by confidence score
├─ Produces draft_protocol:
│  {
│    "nutrition": {
│      "macro_targets": {"protein_g": 120, "fat_g": 80, "carbs_g": 200},
│      "micronutrient_focus": ["magnesium", "vitamin_d3", "omega_3"]
│    },
│    "supplements": [
│      {"name": "NAD+", "dosage": "500mg", "frequency": "daily", "rationale": "..."}
│    ],
│    "fitness": {
│      "cardio": "150 min/week moderate intensity",
│      "strength": "3x/week full body",
│      "flexibility": "daily 10 min yoga"
│    },
│    "medical_actions": [
│      {"action": "consult_cardiologist", "priority": "high", "reason": "..."}
│    ]
│  }
│
└─ Also produces roi_analysis:
   [
     {
       "action": "take_magnesium_glycinate_300mg_daily",
       "roi_score": 8.5,    # 0-10 impact per unit cost
       "cost_usd": 0.25,    # per day
       "impact": "improves sleep quality, reduces anxiety, supports bone health"
     },
     ...
   ]
           │
           ▼
Verifier Node (Tier 1)
├─ Knowledge base semantic search:
│  - Check recommendations against published research
│  - Verify drug interactions
│  - Confirm supplement synergies
│  - Review contraindications
├─ Verdict logic:
│  if critical_issue then "vetoed"
│  elif minor_concern then "needs_revision"
│  else "approved"
├─ On veto: loop_back_to_medical_core (max 3 loops)
│  └─ Provide feedback: "too much magnesium for kidney function"
│     → Cardiologist reduces dosage
│     → Re-synthesize → re-verify
└─ On approval: verifier_result = {
     "verdict": "approved",
     "issues": [],
     "recommendations": [...]
   }
```

### 5. CMO Final Decision

```
CMO Node (Tier 1)
├─ Input: draft_protocol + verifier_result
├─ Decisions:
│  ├─ Escalation check: any medical actions requiring physician sign-off?
│  ├─ Conflict resolution: address any remaining contradictions
│  ├─ Priority ranking: order actions by impact/feasibility
│  └─ Biological age forecast: 5-year projection if protocol followed
├─ Output: cmo_decision = {
│    "approved_protocol": {...},
│    "priority_actions": [
│      {
│        "action": "reduce_refined_carbs",
│        "priority": 1,
│        "longevity_gain_years": 2.3,
│        "adherence_difficulty": "low"
│      },
│      ...
│    ],
│    "biological_age_forecast": {
│      "if_protocol_followed": 39.2,
│      "if_no_changes": 45.0,
│      "confidence": 0.75
│    },
│    "escalation_needed": false,
│    "confidence_score": 92
│  }
└─ Store as Protocol record in database
```

### 6. Execution & Daily Contracts

```
Executors Node (Tier 4)
├─ Fitness Trainer:
│  └─ Converts "150 min cardio" into weekly schedule
│     {
│       "monday": "30 min running, zone 2",
│       "wednesday": "30 min cycling, zone 3",
│       "saturday": "90 min hike, zone 2"
│     }
├─ Nutritionist:
│  └─ Meal planning based on protocol
│     {
│       "breakfast": "scrambled eggs + berries + coffee",
│       "lunch": "grilled chicken + quinoa + vegetables",
│       "dinner": "salmon + sweet potato + leafy greens"
│     }
└─ Output: execution_plan = {
     "nutrition_plan": {...},
     "fitness_plan": {...},
     "timeline": {"start_date": "2026-03-28", "duration_days": 90}
   }
           │
           ▼
Ops Node (Tier 5)
├─ Dispatcher:
│  └─ Breaks execution_plan into daily_contracts
│     for next 30 days
│     {
│       "date": "2026-03-28",
│       "contracts": [
│         {
│           "time": "07:00",
│           "action": "exercise_30min_running",
│           "priority": 1,
│           "points": 5,
│           "is_binding": true
│         },
│         {
│           "time": "12:00",
│           "action": "eat_lunch_as_planned",
│           "priority": 2,
│           "points": 3,
│           "is_binding": false
│         }
│       ]
│     }
├─ Inventory Manager:
│  └─ Books supplement orders
│     ├─ Checks current stock
│     ├─ Orders if running low
│     ├─ Sets expiry alerts
│     └─ Updates supplement_inventory table
└─ Concierge:
   └─ Prepares human handoff (if needed)
      ├─ Schedules physician consultations
      └─ Generates user-friendly summary
```

## 6-Tier Agent Hierarchy

| Tier | Purpose | Agent Count | Key Responsibility |
|------|---------|------------|-------------------|
| **1** | Strategic Foundation | 4 | Orchestration, synthesis, verification, final approval |
| **2** | Medical Analysis | 8 | Biomarker interpretation, pathology detection |
| **3** | Lifestyle Integration | 5 | Behavioral data, environmental factors |
| **4** | Execution Planning | 2 | Convert protocols to actionable plans |
| **5** | Operations | 3 | Daily contracts, inventory, human handoff |
| **6** | UX & Support | 5 | Engagement, testing, analytics, support |

### Tier 1: Strategic Foundation
- **System Biologist**: Aggregates 11 biological systems into unified twin
- **Analyst**: Synthesizes 13 specialist opinions into coherent protocol
- **Verifier**: Guards against evidence gaps and clinical errors
- **CMO**: Final arbiter, escalation decisions, biological age forecasting

### Tier 2: Medical Specialists (parallel execution)
- **Cardiologist**: ApoB, blood pressure, arterial stiffness, heart rate variability
- **Endocrinologist**: HbA1c, fasting glucose, insulin, thyroid (TSH, free T4, free T3), cortisol
- **Metabolologist**: Mitochondrial ATP production, metabolic rate, energy efficiency
- **Geneticist**: APOE, MTHFR, ACE, FTO, CYP450 variants; methylation status
- **Dermatologist**: Skin elasticity, collagen cross-linking, UV damage, skin health aging
- **Orthopedist**: Bone mineral density, muscle mass, joint health, inflammation
- **Microbiome Specialist**: Firmicutes/Bacteroidetes ratio, microbial diversity, dysbiosis markers
- **Aesthetist**: Aesthetic anti-aging, collagen remodeling, stem cell markers

### Tier 3: Lifestyle Experts (parallel execution)
- **Sleep Specialist**: Sleep architecture, REM/NREM ratio, circadian phase, sleep consistency
- **Neuropsychologist**: Cognition (MMSE equivalent), stress hormones, depression/anxiety markers
- **Chronobiologist**: Diurnal cortisol rhythm, circadian-aligned meal timing, seasonal patterns
- **Toxicologist**: Heavy metal load, persistent organic pollutants, detoxification capacity
- **Nutritionist**: Macronutrient balance, micronutrient sufficiency, food synergies, allergies

### Tier 4: Executors (sequential)
- **Fitness Trainer**: Exercise prescriptions (zone, duration, frequency, modality)
- **Nutritionist**: Meal plans (macros, timing, food quality, supplementation)

### Tier 5: Operations (sequential)
- **Dispatcher**: Daily contract generation, prioritization by impact
- **Inventory Manager**: Supplement ordering, stock tracking, expiry management
- **Concierge**: Human-in-the-loop coordination, physician consultations, logistics

### Tier 6: UX & Support (async)
- **UX Designer**: Dashboard insights, celebration milestones, engagement nudges
- **QA Tester**: Decision validation, edge case discovery, regression testing
- **Developer**: System integration, API coherence, tool availability
- **Support Agent**: FAQ, troubleshooting, user education, onboarding
- **Data Analyst**: Trend reports, outcome metrics, platform improvements

## LangGraph Orchestration Details

### State Machine (PLTState)

```python
class PLTState(TypedDict):
    # Trigger
    user_id: str
    session_id: str
    trigger_type: str  # "new_bloodwork" | "daily_morning" | "user_query" | "anomaly"
    trigger_data: dict
    started_at: str

    # Tier 1: System Biologist output
    digital_twin: dict

    # Tier 2 & 3: Parallel opinions (Annotated with operator.add)
    medical_opinions: Annotated[list[dict], operator.add]
    lifestyle_opinions: Annotated[list[dict], operator.add]

    # Tier 1: Analyst & Verifier
    draft_protocol: dict
    roi_analysis: list[dict]
    verifier_result: dict
    veto_count: int

    # Tier 1: CMO
    cmo_decision: dict

    # Tier 4: Executors
    execution_plan: dict

    # Tier 5: Ops
    daily_contracts: list[dict]

    # Metadata
    errors: Annotated[list[dict], operator.add]
    total_tokens: int
    total_cost_usd: float
```

### Conditional Edges (Routing Logic)

```python
# Router Node: Should we update Digital Twin?
if should_update_digital_twin(state):
    → system_biologist
else:
    → executors  # Skip to daily contracts if just routine

# Verifier Node: Veto loop
if verifier_verdict == "vetoed" and veto_count < 3:
    → medical_core  # Loop back, max 3 times
else:
    → cmo  # Proceed to approval
```

### Parallel Fan-Out & Accumulation

**Tier 2 & 3 parallel execution:**
```
system_biologist
    ├─ add_edge → medical_core (Tier 2)
    ├─ add_edge → lifestyle (Tier 3)
    └─ Both accumulate opinions via operator.add
       medical_opinions += [cardiologist_opinion]
       medical_opinions += [endocrinologist_opinion]
       lifestyle_opinions += [sleep_specialist_opinion]
       ...

analyst_node waits for both:
    ├─ add_edge ← medical_core
    └─ add_edge ← lifestyle
```

### Checkpointing & Resumption

```
PostgreSQL Checkpointer
├─ Storage: langgraph_checkpoints table
├─ Thread ID: UUID identifying execution thread
├─ Checkpoint data: Serialized PLTState at each node
├─ Use case: Resume after failure or explicit pause
│  Example:
│  - Pipeline halts at Verifier (veto)
│  - Human reviews recommendations
│  - Resume execution from Verifier with updated state
└─ Autosave: Before and after each node execution
```

## Database Schema

### Core Tables

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    sex VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    subscription_tier VARCHAR(50) DEFAULT 'premium',
    timezone VARCHAR(100) DEFAULT 'UTC'
);
```

#### biomarkers (TimescaleDB Hypertable)
```sql
CREATE TABLE biomarkers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    time TIMESTAMPTZ NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source VARCHAR(50) NOT NULL,  -- blood_test, oura, apple_watch, cgm
    category VARCHAR(100) NOT NULL,  -- lipids, hormones, inflammation
    marker_name VARCHAR(100) NOT NULL,  -- ApoB, testosterone, hsCRP
    value NUMERIC(12,4) NOT NULL,
    unit VARCHAR(30) NOT NULL,
    reference_low NUMERIC(12,4),
    reference_high NUMERIC(12,4),
    optimal_low NUMERIC(12,4),
    optimal_high NUMERIC(12,4),
    metadata JSON DEFAULT '{}'::json
);
CREATE INDEX idx_biomarkers_user_marker ON biomarkers (user_id, marker_name);
CREATE INDEX idx_biomarkers_time ON biomarkers (time);
CREATE INDEX idx_biomarkers_user_time ON biomarkers (user_id, time);
-- Convert to hypertable for time-series optimization
SELECT create_hypertable('biomarkers', 'time', if_not_exists => true);
```

#### protocols
```sql
CREATE TABLE protocols (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES agent_sessions(id) ON DELETE SET NULL,
    version INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, approved, active, archived
    nutrition_plan JSON,
    supplement_plan JSON,
    fitness_plan JSON,
    sleep_protocol JSON,
    environment JSON,
    medical_actions JSON,
    valid_from DATE,
    valid_until DATE,
    approved_by VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_protocols_user_status ON protocols (user_id, status);
```

#### daily_contracts
```sql
CREATE TABLE daily_contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    protocol_id UUID NOT NULL REFERENCES protocols(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    contracts JSON NOT NULL,  -- Array of {time, action, priority, points, is_binding}
    completion_rate NUMERIC(3,2) DEFAULT 0,
    longevity_delta NUMERIC(5,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_daily_contracts_user_date ON daily_contracts (user_id, date);
```

#### agent_sessions
```sql
CREATE TABLE agent_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    trigger_type VARCHAR(50) NOT NULL,  -- new_data, daily, user_query, alert
    trigger_data JSON DEFAULT '{}'::json,
    status VARCHAR(20) DEFAULT 'running',  -- running, completed, failed, vetoed
    langgraph_thread_id VARCHAR(255),
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    total_tokens INT DEFAULT 0,
    total_cost_usd NUMERIC(8,4) DEFAULT 0
);
CREATE INDEX idx_agent_sessions_user ON agent_sessions (user_id);
CREATE INDEX idx_agent_sessions_status ON agent_sessions (status);
```

#### agent_decisions
```sql
CREATE TABLE agent_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL REFERENCES agents(id),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    input_data JSON NOT NULL,
    output_data JSON NOT NULL,
    confidence INT,  -- 0-100
    was_vetoed BOOLEAN DEFAULT false,
    veto_reason TEXT,
    vetoed_by VARCHAR(50),
    approved_by VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    tokens_used INT,
    latency_ms INT
);
CREATE INDEX idx_agent_decisions_session ON agent_decisions (session_id);
CREATE INDEX idx_agent_decisions_agent ON agent_decisions (agent_id);
```

#### agents
```sql
CREATE TABLE agents (
    id VARCHAR(50) PRIMARY KEY,  -- cmo, med_cardio, etc.
    name VARCHAR(255) NOT NULL,
    tier INT NOT NULL,  -- 1-6
    specialty VARCHAR(255),
    system_prompt TEXT NOT NULL,
    model VARCHAR(100) DEFAULT 'claude-sonnet-4-6',
    is_active BOOLEAN DEFAULT true,
    config JSON DEFAULT '{}'::json
);
```

### Indexes for Performance

```sql
-- Time-series queries
CREATE INDEX idx_biomarkers_user_time_marker
  ON biomarkers (user_id, time DESC, marker_name);

-- Protocol queries
CREATE INDEX idx_protocols_user_active
  ON protocols (user_id, status)
  WHERE status = 'active';

-- Daily contracts queries
CREATE INDEX idx_daily_contracts_user_date_recent
  ON daily_contracts (user_id, date DESC);

-- pgvector embeddings (knowledge base)
CREATE INDEX idx_knowledge_embeddings
  ON knowledge_base
  USING hnsw (embedding vector_cosine_ops);
```

## Event System: Redis Pub/Sub & WebSocket

### Real-Time Updates

```
Agent Pipeline Progress:
  agent:pipeline:start → {session_id, user_id, timestamp}
  agent:tier1:system_biologist → {session_id, status, progress}
  agent:tier2:medical_core → {session_id, agent_id, confidence}
  agent:tier3:lifestyle → {session_id, agent_id, opinion}
  agent:pipeline:complete → {session_id, protocol_id, contracts_count}

WebSocket Connection:
  ws://localhost:8000/ws/v1/live
  ├─ Subscribe to user's session: "user:123:sessions"
  ├─ Receive: {event: "tier_complete", tier: 2, duration_ms: 4500}
  ├─ Receive: {event: "protocol_approved", protocol_id: "xyz"}
  └─ Receive: {event: "contract_generated", date: "2026-03-28", count: 8}
```

## Background Tasks: Celery

### Scheduled Tasks

```python
# Daily health analysis (9 AM user timezone)
CELERY_BEAT_SCHEDULE = {
    'daily-health-analysis': {
        'task': 'src.core.celery_tasks.daily_health_analysis',
        'schedule': crontab(hour=9, minute=0),  # user's local 9 AM
        'kwargs': {'trigger_type': 'daily_morning'}
    },
    # Oura Ring sync (every 4 hours)
    'sync-oura-rings': {
        'task': 'src.core.celery_tasks.sync_oura_rings',
        'schedule': crontab(minute=0, hour='*/4')
    },
    # Biomarker anomaly detection (every hour)
    'detect-anomalies': {
        'task': 'src.core.celery_tasks.detect_biomarker_anomalies',
        'schedule': crontab(minute=0)
    },
    # Protocol archive (monthly, first day)
    'archive-old-protocols': {
        'task': 'src.core.celery_tasks.archive_old_protocols',
        'schedule': crontab(day_of_month=1, hour=2, minute=0)
    }
}
```

### Task Examples

```python
@app.task
def run_agent_pipeline(session_id: str, user_id: str, trigger_type: str, trigger_data: dict):
    """Execute full 6-tier pipeline."""
    graph = get_graph()

    initial_state = {
        "user_id": user_id,
        "session_id": session_id,
        "trigger_type": trigger_type,
        "trigger_data": trigger_data,
        "started_at": datetime.utcnow().isoformat(),
        "digital_twin": {},
        "medical_opinions": [],
        "lifestyle_opinions": [],
        "errors": [],
        "total_tokens": 0,
        "total_cost_usd": 0.0,
    }

    # Execute graph with thread ID for checkpointing
    output = graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": str(session_id)}}
    )

    # Persist results to database
    save_session_results(user_id, session_id, output)

    # Publish WebSocket event
    redis.publish(f"user:{user_id}:sessions",
                  json.dumps({"event": "pipeline_complete"}))
```

## Security Model

### Authentication
- **JWT Tokens**: Issued on login, stored in `Authorization: Bearer <token>` header
- **Token Expiration**: Default 24 hours, refresh endpoint available
- **Password Hashing**: bcrypt (cost factor 12)

### Authorization
- **RBAC**: subscription_tier (free, premium, enterprise)
- **Data Isolation**: Users see only their own biomarkers, protocols, contracts
- **Row-Level Security**: PostgreSQL policies enforce user_id filtering

### API Security
- **CORS**: Allowed origins configurable per environment
- **Rate Limiting**: Redis-backed rate limiter (100 req/min per user)
- **HTTPS**: Required in production (enforced via ASGI middleware)

## Performance Optimizations

### Database
- **TimescaleDB Hypertables**: Biomarker queries optimized for time-series
- **pgvector Indexing**: HNSW algorithm for knowledge base semantic search
- **Connection Pooling**: asyncpg maintains pool of 10-20 connections
- **Query Caching**: Recent protocols, biomarker summaries cached in Redis

### API
- **Async/Await**: All database I/O non-blocking via asyncpg
- **Dependency Caching**: `get_settings()` cached via `@lru_cache`
- **Pagination**: Biomarker history limited to 100 items per request

### Agent Orchestration
- **Parallel Execution**: Tier 2 & 3 agents run simultaneously via LangGraph fan-out
- **Token Optimization**: System prompts cached, reused across sessions
- **Streaming**: Large result sets returned as server-sent events (optional)

## Monitoring & Observability

### Logging
- **Structured Logging**: JSON format with user_id, session_id context
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Aggregation**: All logs to stdout (container-friendly)

### Metrics (optional Prometheus integration)
```python
# Instrumentable metrics
- agent_pipeline_duration_seconds
- agent_decision_tokens_used
- biomarker_upload_processing_time_seconds
- protocol_generation_cost_usd
- daily_contract_completion_rate
- user_session_count
```

### Health Checks
```
GET /health
→ {
    "status": "ok",
    "version": "0.1.0",
    "timestamp": "2026-03-27T10:30:00Z"
  }
```
