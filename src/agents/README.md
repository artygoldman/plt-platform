# Phase 3: PLT Agent Orchestration Engine

The LangGraph orchestration engine that connects all 27 AI agents into a directed graph with state management, parallel execution, veto loops, and checkpoints.

## Architecture Overview

### Core Components

```
src/agents/
├── __init__.py           # Package exports
├── state.py              # PLTState definition (TypedDict with Annotated fields)
├── graph.py              # Main LangGraph assembly
├── runner.py             # High-level pipeline entry point
├── nodes/
│   ├── __init__.py       # Node function exports
│   ├── common.py         # Shared utilities (call_agent, logging, context)
│   ├── router.py         # Entry point router (trigger_type routing)
│   ├── tier1.py          # Strategic Core: System Biologist, Analyst, Verifier, CMO
│   ├── tier2.py          # Medical Core: 8 agents in parallel
│   ├── tier3.py          # Lifestyle Core: 5 agents in parallel
│   ├── tier4.py          # Executors: Nutritionist → Fitness Trainer
│   └── tier5.py          # Operations: Dispatcher → Inventory → Finance → Concierge
└── prompts/              # Agent system prompts (Phase 1)
```

### Execution Graph

```
                    ┌─────────────┐
                    │   ROUTER    │
                    └──────┬──────┘
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
    (if new data)                      (if daily replay)
         │                                   │
         v                                   │
  ┌──────────────┐                         │
  │ SYSTEM       │                         │
  │ BIOLOGIST    │                         │
  └──────┬───────┘                         │
         │                                   │
    ┌────┴────┐                            │
    │          │                            │
    v          v                            │
┌────────┐ ┌─────────┐                    │
│MEDICAL │ │LIFESTYLE│                    │
│ CORE   │ │ CORE    │                    │
│(8 in   │ │(5 in    │                    │
│parallel)│ │parallel)│                    │
└────┬───┘ └────┬────┘                    │
     │          │                          │
     └────┬─────┘                          │
          v                                │
      ┌────────┐                          │
      │ANALYST │                          │
      └────┬───┘                          │
           v                              │
      ┌──────────┐                        │
      │VERIFIER  │                        │
      └────┬─────┘                        │
           │                              │
    ┌──────┴──────┐                      │
    │             │                      │
(veto?)    (approved)                    │
    │             │                      │
    ├─→back to    │                      │
    │  MEDICAL    │                      │
    │  CORE       │                      │
    │  (loop 3x)  │                      │
    │             │                      │
    └─────┬───────┘                      │
          v                              │
      ┌──────┐                           │
      │ CMO  │←──────────────────────────┘
      └──┬───┘
         │
         v
   ┌──────────────┐
   │ EXECUTORS    │
   │(Nutritionist)│
   │(Fitness)     │
   └──┬───────────┘
      │
      v
  ┌─────────────────────┐
  │ OPS                 │
  │(Dispatcher)         │
  │(Inventory)         │
  │(Finance)           │
  │(Concierge optional) │
  └─────────────────────┘
      │
      v
    END
```

## Key Features

### 1. State Management (PLTState)

A unified `TypedDict` with Annotated fields supporting LangGraph state aggregation:

- **Trigger info**: user_id, trigger_type, trigger_data, session_id
- **Digital Twin**: 11 system scores, biological age, anomalies, correlations
- **Parallel opinions**: medical_opinions, lifestyle_opinions (accumulated via `operator.add`)
- **Synthesis**: draft_protocol, roi_analysis, verifier_result, veto_count
- **Final decision**: cmo_decision, execution_plan, daily_contracts
- **Metadata**: errors, total_tokens, total_cost_usd

### 2. Parallel Execution (Fan-Out / Fan-In)

**Medical Core (Tier 2)**: All 8 agents run in parallel
```python
- Cardiologist
- Endocrinologist
- Metabolologist
- Microbiome Specialist
- Dermatologist
- Aesthetist
- Orthopedist
- Geneticist
```

**Lifestyle Core (Tier 3)**: All 5 agents run in parallel
```python
- Chronobiologist
- Sleep Specialist
- Neuropsychologist
- Environment Specialist
- Toxicologist
```

Uses `asyncio.gather()` for true parallelism. Both cores share the same Digital Twin snapshot and report errors gracefully.

### 3. Conditional Veto Loop

When verifier detects issues:
1. First 3 vetoes: loop back to medical_core for revision
2. 4th+ veto: escalate to CMO (human review recommended)

```python
def should_reveto(state: PLTState) -> Literal["medical_core", "cmo"]:
    verdict = state["verifier_result"].get("verdict")
    veto_count = state.get("veto_count", 0)
    if verdict == "vetoed" and veto_count < 3:
        return "medical_core"  # Loop
    else:
        return "cmo"  # Proceed
```

### 4. PostgreSQL Checkpointing

Graph uses `PostgresSaver` for:
- Full execution history via thread_id = session_id
- Recovery from failures
- Human-in-the-loop intervention points
- State snapshots at each node

### 5. Dynamic Context Building

Each agent receives only relevant fields from PLTState:

- **System Biologist**: trigger_data (biomarkers, wearables)
- **Medical agents**: digital_twin snapshot + biomarker values for their specialty
- **Lifestyle agents**: digital_twin + wearable + environmental data
- **Analyst**: medical_opinions + lifestyle_opinions + digital_twin
- **Verifier**: draft_protocol (checks against knowledge base)
- **CMO**: draft_protocol + verifier_result + all opinions
- **Nutritionist**: cmo_decision + digital_twin
- **Fitness**: nutrition_plan + cmo_decision + digital_twin
- **Dispatcher**: execution_plan (nutrition + fitness)
- **Inventory**: daily_contracts (checks stock)
- **Finance**: daily_contracts + inventory (calculates costs)

## Usage

### Simple Sync Wrapper

```python
from src.agents.runner import run_agent_pipeline_sync

result = run_agent_pipeline_sync(
    user_id="user-123",
    trigger_type="new_bloodwork",
    trigger_data={
        "biomarkers": {
            "glucose": 95,
            "hdl": 52,
            "cortisol": 15,
            # ... >100 biomarkers
        },
        "wearable": {
            "heart_rate": 62,
            "hrv": 35,
            "sleep_hours": 7.2
        }
    }
)

print(result)  # {session_id, status, daily_contracts, cmo_decision, ...}
```

### Async Wrapper

```python
import asyncio
from src.agents.runner import run_agent_pipeline

result = asyncio.run(
    run_agent_pipeline(
        user_id="user-123",
        trigger_type="new_bloodwork",
        trigger_data={...}
    )
)
```

### Trigger Types

1. **"new_bloodwork"**: New biomarker data → full pipeline
2. **"daily_morning"**: Daily execution → skip system_biologist, go straight to executors
3. **"user_query"**: User question → full pipeline
4. **"anomaly"**: Detected anomaly → full pipeline
5. **"scheduled"**: Periodic review → full pipeline

## Common Utilities (common.py)

### call_agent()

Universal async function to call any agent:

```python
result = await call_agent(
    agent_id="cmo",
    user_message="<context from state>",
    state=PLTState,
    client=AsyncAnthropic()
)
# Returns: {agent_id, output, confidence, tokens, latency_ms, model}
```

Features:
- Loads system prompt from agents/prompts/{agent_id}.py
- Calls Claude API with structured output
- Extracts JSON from markdown blocks
- Tracks token usage and latency
- Returns confidence score

### log_decision()

Async logging to agent_decisions table (PostgreSQL):

```python
await log_decision(
    session_id=session_id,
    agent_id="cmo",
    user_id=user_id,
    input_data={...},
    output_data={...},
    tokens=2500,
    latency_ms=3200
)
```

### build_agent_context()

Builds user message for each agent based on what it needs from state:

```python
user_message = build_agent_context("analyst", state)
# Extracts: medical_opinions, lifestyle_opinions, digital_twin
# Formats as markdown/JSON for Claude
```

## Error Handling

All errors are **collected but don't crash the pipeline**:

1. **Individual agent fails** (tier2/tier3 parallel):
   - Error logged to state["errors"]
   - Opinion marked as failed: `{"agent_id": "...", "opinion": {"error": "..."}, "failed": True}`
   - Other agents continue
   - Analyst handles partial opinions gracefully

2. **Tier 1 node fails** (system_biologist, analyst, verifier, cmo):
   - Error logged
   - Upstream state returned empty dict
   - Downstream nodes receive empty/default values
   - Pipeline can still complete with reduced confidence

3. **Tier 4/5 fails** (executors, ops):
   - Error logged
   - Partial execution_plan / daily_contracts returned
   - User sees degraded results

## Integration with Phase 1 & 2

- **Phase 1 (DB Models)**: Reads from digital_twin, user_metadata, biomarker tables
- **Phase 2 (API)**: Calls via POST /api/orchestration/run endpoint
- **Prompts (Phase 1)**: All 27 agent prompts pre-loaded from src/agents/prompts/

## Monitoring & Logging

All nodes log structured JSON:

```
INFO Agent call completed agent_id=cmo tokens=2500 latency_ms=3200 confidence=92
WARNING Protocol vetoed (veto #1) user_id=user-123 session_id=uuid
ERROR Agent call failed agent_id=cardiologist error=API timeout
```

Use log aggregation (ELK, DataDog) to:
- Track per-agent latency & cost
- Monitor veto loops (escalation trigger)
- Alert on critical errors

## Production Checklist

- [x] Full type hints + docstrings
- [x] Async/await throughout
- [x] Error collection (non-crashing)
- [x] PostgreSQL checkpointing
- [x] Token tracking
- [x] Structured logging
- [ ] Rate limiting (recommend Anthropic SDK built-in)
- [ ] Retry logic (recommend tenacity library)
- [ ] Metrics export (Prometheus/CloudWatch)
- [ ] Load testing (artillery/locust)

## Next Steps

1. **API Integration** (Phase 2 continued):
   - Create POST /api/orchestration/run endpoint
   - Add request validation + async handling
   - Stream responses for long-running pipelines

2. **Frontend Integration**:
   - Display daily_contracts as actionable UI
   - Show cmo_decision rationale
   - Allow user approval/veto of plans

3. **Database Backfill**:
   - Pre-populate digital_twin table with Phase 1 data
   - Load user goals/constraints
   - Initialize agent_decisions history

4. **Performance Tuning**:
   - Measure end-to-end latency
   - Optimize parallel agent context
   - Consider multi-region checkpointing
