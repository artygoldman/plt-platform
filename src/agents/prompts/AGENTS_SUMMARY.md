# Personal Longevity Team Platform - Agent Prompts

## Overview
This module contains system prompts and output schemas for all agents in the Personal Longevity Team (PLT) platform. Currently implemented: **Tier 5 (Operations)** and **Tier 6 (IT & Infrastructure)**.

## Tier 5: Operations (4 agents)

### 1. ops_dispatcher (Диспетчер-Экзекутор)
**Role:** Only agent that communicates directly with users  
**Specialization:** Daily contract generation, user motivation, protocol simplification  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Creates 3-5 daily health contracts each morning
- Translates medical protocols into simple language
- Sends motivational nudges
- Gamifies health improvements (shows impact on Longevity Score)

**Key Output:** Daily message with contracts, motivation, notification schedule

---

### 2. ops_inventory (Завхоз-Инвентаризатор)
**Role:** Supply chain management  
**Specialization:** Supplement tracking, expiry management, stock control  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Tracks supplement/medication inventory
- Alerts on expiry dates (CRITICAL: prevents use of expired items)
- Tracks stock levels and predicts when supplies run out
- Validates if current inventory can support new protocols

**Key Output:** Inventory status, reorder lists, expired alerts, protocol feasibility

---

### 3. ops_concierge (Медицинский Консьерж)
**Role:** Logistics coordination  
**Specialization:** Appointment booking, supplement purchasing, schedule coordination  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Searches and books blood tests at best clinics
- Coordinates medical procedures
- Finds and purchases supplements at optimal prices
- Manages medical appointment calendar
- Provides preparation instructions

**Key Output:** Appointment plan, purchase list, cost summary, follow-up schedule

---

### 4. ops_finance (Финансовый Контроллер)
**Role:** Financial optimization  
**Specialization:** Cost analysis, ROI calculation, budget optimization  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Finds cheapest options for clinics, labs, supplements
- Tracks monthly health spending by category
- Calculates cost per life-day (how much each added day costs)
- Ranks all protocol components by ROI (return on investment)
- Identifies cost-saving opportunities

**Key Output:** Budget report, cost optimization suggestions, ROI rankings, annual forecast

---

## Tier 6: IT & Infrastructure (4 agents)

### 5. it_support (Служба Поддержки)
**Role:** Technical support  
**Specialization:** Device sync troubleshooting, FAQ, user support  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Diagnoses technical issues (device sync, data upload, authentication)
- Provides step-by-step troubleshooting solutions
- Manages FAQ database
- Escalates critical issues to developers

**Key Output:** Diagnosis, solution steps, escalation decision, FAQ matches

---

### 6. it_ux (UX-Дизайнер)
**Role:** User experience  
**Specialization:** User engagement analysis, interface improvement suggestions, A/B testing  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Monitors user engagement metrics (session duration, click heatmaps)
- Identifies UI pain points and confusing flows
- Recommends dashboard improvements
- Designs A/B tests for UI changes
- Tracks feature adoption rates

**Key Output:** UX assessment, improvement suggestions, A/B test recommendations, layout changes

---

### 7. it_developer (Системный Разработчик)
**Role:** System optimization  
**Specialization:** Performance monitoring, agent optimization, cost control  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Monitors system infrastructure (CPU, memory, latency, errors)
- Profiles performance of all 27 agents
- Identifies bottlenecks and optimization opportunities
- Manages API token usage and costs
- Recommends model downgrades for simple tasks

**Key Output:** System health report, optimization suggestions, agent tuning, cost analysis

---

### 8. it_qa (QA-Тестировщик)
**Role:** Quality assurance  
**Specialization:** Output validation, hallucination detection, consistency checking  
**Model:** claude-opus-4-1  
**Responsibilities:**
- Validates all agent outputs for correctness
- Detects hallucinations (made-up facts)
- Finds contradictions between agents
- Checks protocol safety and medical guidelines
- Validates mathematical calculations

**Key Output:** QA report, hallucination checks, consistency checks, sanity flags, safety validation

---

## File Structure

```
tier5_dispatcher.py      → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
tier5_inventory.py       → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
tier5_concierge.py       → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
tier5_finance.py         → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG

tier6_support.py         → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
tier6_ux.py              → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
tier6_developer.py       → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
tier6_qa.py              → SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG

__init__.py              → Master index with utility functions
```

## Key Features

### 1. Structured JSON Output
Every agent returns strict JSON with:
- Type definitions for all fields
- Required vs optional fields
- Validation of arrays and objects
- Confidence scores (0-100) for all outputs

### 2. Russian System Prompts
- All instructions in Russian for clarity
- Clear role definitions and responsibilities
- Explicit allowed/restricted actions
- Escalation rules for complex situations

### 3. Comprehensive Metadata
Each agent has:
- `id`: Unique identifier
- `name`: Russian name
- `tier`: Hierarchy level (5-6)
- `role`: Functional role
- `specialization`: Domain expertise
- `model`: Claude model (all using opus-4-1)
- `allowed_actions`: What this agent can do
- `restricted_actions`: What this agent cannot do
- `escalation_rules`: When to involve other agents

### 4. Module API
```python
from prompts import (
    get_agent_prompt(agent_id),      # Get system prompt
    get_agent_schema(agent_id),      # Get output schema
    get_agent_config(agent_id),      # Get agent metadata
    get_agents_by_tier(tier),        # Get all agents in tier
    get_all_agent_ids(),             # Get all agent IDs
    AGENTS_BY_TIER,                  # Dict: tier → agents
    ALL_AGENTS,                      # Dict: id → module
)
```

## Important Notes

### Safety & Quality
- **QA Agent** validates all outputs before they reach users
- **Support Agent** escalates critical issues immediately
- **Developer Agent** monitors system reliability 24/7
- Hallucination detection is mandatory

### Cost Optimization
- **Finance Agent** tracks every dollar spent
- ROI calculated for each component
- Suggests cheaper alternatives without quality loss
- Monthly budget forecasting and cost per life-day metrics

### User Experience
- **Dispatcher Agent** uses simple language (NO medical jargon)
- Gamification with Longevity Score impact
- Motivational tone in all communications
- Accessibility for all device types

## Integration Points

```
Tier 1-3 (Clinicians)
    ↓
Tier 4 (Nutritionist)
    ↓
Tier 5 (Operations) ← THESE AGENTS
    ├─ Dispatcher (→ User)
    ├─ Inventory (↔ Concierge)
    ├─ Concierge (→ Supply chain)
    └─ Finance (→ Budget)
    ↓
Tier 6 (IT & Infrastructure) ← THESE AGENTS
    ├─ Support (← User issues)
    ├─ UX (← Analytics)
    ├─ Developer (← System health)
    └─ QA (← Quality control)
```

## Usage Example

```python
from prompts import get_agent_prompt, get_agent_config

# Get dispatcher configuration
config = get_agent_config("ops_dispatcher")
print(f"Agent: {config['name']}")
print(f"Role: {config['role']}")
print(f"Model: {config['model']}")

# Get system prompt for API call
prompt = get_agent_prompt("ops_dispatcher")

# Use in Claude API call
response = client.messages.create(
    model=config["model"],
    max_tokens=config["max_tokens"],
    system=prompt,
    messages=[
        {
            "role": "user",
            "content": "Create daily contracts for user based on protocol..."
        }
    ]
)
```

## Metrics & Performance

Current agent stats:
- **Total Agents (Tier 5-6):** 8
- **Tier 5 (Operations):** 4 agents
- **Tier 6 (IT & Infrastructure):** 4 agents
- **Prompt Size:** 2.8-4.9K characters each
- **Schema Size:** 2.5-7.5K characters each
- **Model:** claude-opus-4-1 for all
- **Max Tokens:** 2000-3000 per call

## Version History

- **v1.0** (Current): Tier 5 & 6 agents (8 agents)
- **Future**: Tier 1-4 agents (19 agents) - placeholders exist

