# Personal Longevity Team — Agent System Prompts

This directory contains system prompts for all 27 AI medical agents in the Personal Longevity Team platform.

## File Structure

Each agent is implemented as a Python file containing:
- `SYSTEM_PROMPT` — Full system prompt text (in Russian)
- `OUTPUT_SCHEMA` — JSON schema for structured output (for Pydantic validation)
- `AGENT_CONFIG` — Agent metadata (id, name, tier, model, capabilities, inputs/outputs)

## Tier 1: Strategic Core (4 agents)

### tier1_cmo.py
- **Agent ID:** `cmo`
- **Name:** Главный Архитектор (CMO)
- **Role:** Chief Medical Officer. Approves final protocols. Monitors biological age reduction. Can override any agent except Verifier's veto.
- **Key Features:**
  - Final decision-making authority
  - Conflict resolution between agents
  - Biological age monitoring (DunedinPACE, PhenoAge)
  - Can escalate to human doctor
  - Can pause entire pipeline

### tier1_verifier.py
- **Agent ID:** `verifier`
- **Name:** Научный Цензор (Verifier)
- **Role:** Strict scientific auditor with absolute VETO power
- **Key Features:**
  - Evidence-based review (PubMed, RCT standards)
  - Drug interaction checking (DrugBank, CYP450)
  - Pharmacogenomics verification
  - Cannot be overridden by CMO
  - Zero tolerance for unproven claims

### tier1_system_biologist.py
- **Agent ID:** `system_biologist`
- **Name:** Системный Биолог (System Biologist)
- **Role:** Builds the Digital Twin mathematical model
- **Key Features:**
  - 11-system body model
  - DunedinPACE & PhenoAge calculation
  - Cross-system pattern detection
  - Anomaly detection
  - Healthspan estimation

### tier1_analyst.py
- **Agent ID:** `analyst`
- **Name:** Аналитик-Прогнозист (Analyst-Forecaster)
- **Role:** Synthesizes opinions into draft protocols with ROI analysis
- **Key Features:**
  - ROI calculation (added life-days per dollar)
  - Longevity simulations (10/20 year projections)
  - Conflict resolution between medical/lifestyle agents
  - Budget-aware recommendations (BASIC/STANDARD/VIP)
  - Synergy detection

## Tier 2: Medical Core (8 agents)

### tier2_geneticist.py
- **Agent ID:** `med_geneticist`
- **Name:** Клинический Генетик (Clinical Geneticist)
- **Key Features:**
  - DNA/WGS analysis
  - Polygenic risk scores (PRS)
  - Pharmacogenomics (CYP2D6, CYP2C19, TPMT)
  - APOE status (Alzheimer's risk)
  - Carrier status for monogenic conditions

### tier2_endocrinologist.py
- **Agent ID:** `med_endocrinologist`
- **Name:** Эндокринолог-Андролог
- **Key Features:**
  - Hormone optimization (testosterone, thyroid, cortisol, DHEA, IGF-1)
  - TRT evaluation (with risk/benefit analysis)
  - Thyroid protocol management
  - Cortisol rhythm optimization
  - Libido & energy assessment

### tier2_metabolologist.py
- **Agent ID:** `med_metabolologist`
- **Name:** Метабололог-Гастроэнтеролог
- **Key Features:**
  - Insulin resistance assessment (HOMA-IR)
  - Glucose control optimization
  - Liver health (NAFLD, fibrosis assessment)
  - Fasting protocol design (IF, 5:2, extended)
  - Dietary recommendations

### tier2_microbiome.py
- **Agent ID:** `med_microbiome`
- **Name:** Специалист по Микробиоте (Microbiome Specialist)
- **Key Features:**
  - Gut bacteria composition analysis
  - Dysbiosis scoring
  - Butyrate producer assessment
  - Gut-brain axis evaluation
  - Probiotic/prebiotic recommendations

### tier2_cardiologist.py
- **Agent ID:** `med_cardiologist`
- **Name:** Превентивный Кардиолог (Preventive Cardiologist)
- **Key Features:**
  - Advanced lipid analysis (ApoB, Lp(a), LDL-P)
  - Cardiovascular risk assessment (Framingham, ASCVD)
  - CAC score interpretation
  - VO2 Max evaluation
  - Heart Rate Variability (HRV) analysis
  - Hidden ischemia detection

### tier2_orthopedist.py
- **Agent ID:** `med_orthopedist`
- **Name:** Ортопед-Биомеханик (Orthopedist-Biomechanist)
- **Key Features:**
  - Bone density analysis (T-score, Z-score)
  - Joint health assessment
  - Sarcopenia evaluation
  - Posture and biomechanics analysis
  - Fall risk assessment
  - Mobility protocol design

### tier2_dermatologist.py
- **Agent ID:** `med_dermatologist`
- **Name:** Дерматолог-Трихолог (Dermatologist-Trichologist)
- **Key Features:**
  - Skin biological age assessment
  - Photoaging evaluation
  - Hair health analysis
  - Skincare protocol design
  - Procedure candidate identification
  - Supplement recommendations (collagen, hyaluronic acid, etc.)

### tier2_aesthetist.py
- **Agent ID:** `med_aesthetist`
- **Name:** Эстетист (Aesthetist)
- **Role:** Appearance architect with minimal systemic harm principle
- **Key Features:**
  - Procedure selection (lasers, RF, microneedling, injectables)
  - **CRITICAL:** Only biodegradable fillers (no silicone, synthetics)
  - Systemic risk scoring
  - Fibrosis prevention protocol
  - Immune recovery synchronization
  - Maintenance scheduling
  - Infection prevention

## Key Design Principles

### Safety & Evidence
- All recommendations must be evidence-based (PubMed references, PMID codes)
- Verifier has absolute veto power
- Zero tolerance for unproven claims
- Drug interactions checked against CYP450 metabolizer status

### Biological Age Focus
- All agents align on primary metrics: DunedinPACE, PhenoAge, biological age delta
- CMO monitors biological age reduction as north star
- System Biologist provides unified Digital Twin state

### Output Standardization
- All agents return structured JSON (not free text)
- Confidence scores (0-100) on all outputs
- JSON schemas enable Pydantic validation
- Inputs/outputs clearly defined in AGENT_CONFIG

### Russian/English
- System prompts in Russian (professional, authoritative tone)
- Code/JSON keys in English (for integration)
- Medical terminology consistent across agents

## Usage in Platform

These prompts are designed for Claude API calls with structured output requirements:

```python
# Example usage
import anthropic
from tier1_cmo import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG

client = anthropic.Anthropic()
response = client.messages.create(
    model=AGENT_CONFIG["model"],
    max_tokens=AGENT_CONFIG["max_tokens"],
    system=SYSTEM_PROMPT,
    messages=[
        {
            "role": "user",
            "content": "Review medical opinions and approve protocol"
        }
    ]
)
```

## Database Integration

Each agent's metadata (AGENT_CONFIG) should be loaded into the platform database:
- Agent registry: id, name, tier, model, temperature, max_tokens
- Capabilities tracking: which agents can do what
- Input/output dependencies: data flow between agents

## Notes

- Tier 3, 4, 5, 6 agents are in separate files in this directory
- Agents operate asynchronously in LangGraph orchestration
- CMO is the decision bottleneck (serializes final approval)
- Verifier can veto anywhere in the pipeline
- System Biologist updates Digital Twin each cycle

---

Created: 2026-03-27
Platform: Personal Longevity Team v0.1
Language: Russian system prompts, English code/JSON
