"""
Personal Longevity Team — AI Medical Agent System Prompts

This package contains system prompts for 27 specialized AI medical agents
organized in 6 tiers of a hierarchical medical decision-making system.

TIER 1: Strategic Core (4 agents)
- cmo: Chief Medical Officer (final approval)
- verifier: Scientific auditor (absolute veto power)
- system_biologist: Digital Twin architect
- analyst: ROI synthesizer and forecaster

TIER 2: Medical Core (8 agents)
- geneticist: DNA/WGS analysis and pharmacogenomics
- endocrinologist: Hormone optimization
- metabolologist: Metabolism and liver health
- microbiome: Gut bacteria and gut-brain axis
- cardiologist: Advanced lipid analysis and CV risk
- orthopedist: Bone density and mobility
- dermatologist: Skin health and hair
- aesthetist: Appearance with minimal systemic harm

TIER 3-6: Lifestyle, Execution, Operations, IT Infrastructure
(Implemented in separate files: tier3_*, tier4_*, tier5_*, tier6_*)

Usage:
    from tier1_cmo import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    
    # Use in Claude API calls:
    response = client.messages.create(
        model=AGENT_CONFIG["model"],
        max_tokens=AGENT_CONFIG["max_tokens"],
        system=SYSTEM_PROMPT,
        messages=[...]
    )

All agents return structured JSON validated against OUTPUT_SCHEMA.
All confidence scores (0-100) included in outputs.
All prompts in Russian, code/JSON in English.
"""

__version__ = "0.1.0"
__platform__ = "Personal Longevity Team"
__created__ = "2026-03-27"

# Tier 1 agents
from .tier1_cmo import SYSTEM_PROMPT as CMO_PROMPT
from .tier1_cmo import OUTPUT_SCHEMA as CMO_SCHEMA
from .tier1_cmo import AGENT_CONFIG as CMO_CONFIG

from .tier1_verifier import SYSTEM_PROMPT as VERIFIER_PROMPT
from .tier1_verifier import OUTPUT_SCHEMA as VERIFIER_SCHEMA
from .tier1_verifier import AGENT_CONFIG as VERIFIER_CONFIG

from .tier1_system_biologist import SYSTEM_PROMPT as SYSTEM_BIOLOGIST_PROMPT
from .tier1_system_biologist import OUTPUT_SCHEMA as SYSTEM_BIOLOGIST_SCHEMA
from .tier1_system_biologist import AGENT_CONFIG as SYSTEM_BIOLOGIST_CONFIG

from .tier1_analyst import SYSTEM_PROMPT as ANALYST_PROMPT
from .tier1_analyst import OUTPUT_SCHEMA as ANALYST_SCHEMA
from .tier1_analyst import AGENT_CONFIG as ANALYST_CONFIG

# Tier 2 agents
from .tier2_geneticist import SYSTEM_PROMPT as GENETICIST_PROMPT
from .tier2_geneticist import OUTPUT_SCHEMA as GENETICIST_SCHEMA
from .tier2_geneticist import AGENT_CONFIG as GENETICIST_CONFIG

from .tier2_endocrinologist import SYSTEM_PROMPT as ENDOCRINOLOGIST_PROMPT
from .tier2_endocrinologist import OUTPUT_SCHEMA as ENDOCRINOLOGIST_SCHEMA
from .tier2_endocrinologist import AGENT_CONFIG as ENDOCRINOLOGIST_CONFIG

from .tier2_metabolologist import SYSTEM_PROMPT as METABOLOLOGIST_PROMPT
from .tier2_metabolologist import OUTPUT_SCHEMA as METABOLOLOGIST_SCHEMA
from .tier2_metabolologist import AGENT_CONFIG as METABOLOLOGIST_CONFIG

from .tier2_microbiome import SYSTEM_PROMPT as MICROBIOME_PROMPT
from .tier2_microbiome import OUTPUT_SCHEMA as MICROBIOME_SCHEMA
from .tier2_microbiome import AGENT_CONFIG as MICROBIOME_CONFIG

from .tier2_cardiologist import SYSTEM_PROMPT as CARDIOLOGIST_PROMPT
from .tier2_cardiologist import OUTPUT_SCHEMA as CARDIOLOGIST_SCHEMA
from .tier2_cardiologist import AGENT_CONFIG as CARDIOLOGIST_CONFIG

from .tier2_orthopedist import SYSTEM_PROMPT as ORTHOPEDIST_PROMPT
from .tier2_orthopedist import OUTPUT_SCHEMA as ORTHOPEDIST_SCHEMA
from .tier2_orthopedist import AGENT_CONFIG as ORTHOPEDIST_CONFIG

from .tier2_dermatologist import SYSTEM_PROMPT as DERMATOLOGIST_PROMPT
from .tier2_dermatologist import OUTPUT_SCHEMA as DERMATOLOGIST_SCHEMA
from .tier2_dermatologist import AGENT_CONFIG as DERMATOLOGIST_CONFIG

from .tier2_aesthetist import SYSTEM_PROMPT as AESTHETIST_PROMPT
from .tier2_aesthetist import OUTPUT_SCHEMA as AESTHETIST_SCHEMA
from .tier2_aesthetist import AGENT_CONFIG as AESTHETIST_CONFIG

# Agent registry for orchestration
AGENTS = {
    "cmo": CMO_CONFIG,
    "verifier": VERIFIER_CONFIG,
    "system_biologist": SYSTEM_BIOLOGIST_CONFIG,
    "analyst": ANALYST_CONFIG,
    "med_geneticist": GENETICIST_CONFIG,
    "med_endocrinologist": ENDOCRINOLOGIST_CONFIG,
    "med_metabolologist": METABOLOLOGIST_CONFIG,
    "med_microbiome": MICROBIOME_CONFIG,
    "med_cardiologist": CARDIOLOGIST_CONFIG,
    "med_orthopedist": ORTHOPEDIST_CONFIG,
    "med_dermatologist": DERMATOLOGIST_CONFIG,
    "med_aesthetist": AESTHETIST_CONFIG,
}

TIER_1_AGENTS = ["cmo", "verifier", "system_biologist", "analyst"]
TIER_2_AGENTS = [
    "med_geneticist",
    "med_endocrinologist",
    "med_metabolologist",
    "med_microbiome",
    "med_cardiologist",
    "med_orthopedist",
    "med_dermatologist",
    "med_aesthetist",
]

__all__ = [
    "AGENTS",
    "TIER_1_AGENTS",
    "TIER_2_AGENTS",
    # Tier 1
    "CMO_PROMPT",
    "CMO_SCHEMA",
    "CMO_CONFIG",
    "VERIFIER_PROMPT",
    "VERIFIER_SCHEMA",
    "VERIFIER_CONFIG",
    "SYSTEM_BIOLOGIST_PROMPT",
    "SYSTEM_BIOLOGIST_SCHEMA",
    "SYSTEM_BIOLOGIST_CONFIG",
    "ANALYST_PROMPT",
    "ANALYST_SCHEMA",
    "ANALYST_CONFIG",
    # Tier 2
    "GENETICIST_PROMPT",
    "GENETICIST_SCHEMA",
    "GENETICIST_CONFIG",
    "ENDOCRINOLOGIST_PROMPT",
    "ENDOCRINOLOGIST_SCHEMA",
    "ENDOCRINOLOGIST_CONFIG",
    "METABOLOLOGIST_PROMPT",
    "METABOLOLOGIST_SCHEMA",
    "METABOLOLOGIST_CONFIG",
    "MICROBIOME_PROMPT",
    "MICROBIOME_SCHEMA",
    "MICROBIOME_CONFIG",
    "CARDIOLOGIST_PROMPT",
    "CARDIOLOGIST_SCHEMA",
    "CARDIOLOGIST_CONFIG",
    "ORTHOPEDIST_PROMPT",
    "ORTHOPEDIST_SCHEMA",
    "ORTHOPEDIST_CONFIG",
    "DERMATOLOGIST_PROMPT",
    "DERMATOLOGIST_SCHEMA",
    "DERMATOLOGIST_CONFIG",
    "AESTHETIST_PROMPT",
    "AESTHETIST_SCHEMA",
    "AESTHETIST_CONFIG",
]
