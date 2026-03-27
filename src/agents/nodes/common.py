"""
Common utilities for agent orchestration.
Shared functions for API calls, logging, and context building.
"""

import json
import time
import logging
from typing import Optional
from datetime import datetime
import asyncio

from anthropic import AsyncAnthropic

from src.agents.state import PLTState
from src.core.config import get_settings

logger = logging.getLogger(__name__)


# Lazy-load prompts to avoid circular imports
def _get_prompt_module(agent_id: str):
    """Dynamically import agent prompt module."""
    # Map agent_id to module path
    # Tier 1
    if agent_id == "system_biologist":
        from src.agents.prompts.tier1_system_biologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "analyst":
        from src.agents.prompts.tier1_analyst import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "verifier":
        from src.agents.prompts.tier1_verifier import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "cmo":
        from src.agents.prompts.tier1_cmo import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    # Tier 2 (Medical)
    elif agent_id == "cardiologist":
        from src.agents.prompts.tier2_cardiologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "endocrinologist":
        from src.agents.prompts.tier2_endocrinologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "metabolologist":
        from src.agents.prompts.tier2_metabolologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "microbiome":
        from src.agents.prompts.tier2_microbiome import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "dermatologist":
        from src.agents.prompts.tier2_dermatologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "aesthetist":
        from src.agents.prompts.tier2_aesthetist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "orthopedist":
        from src.agents.prompts.tier2_orthopedist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "geneticist":
        from src.agents.prompts.tier2_geneticist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    # Tier 3 (Lifestyle)
    elif agent_id == "chronobiologist":
        from src.agents.prompts.tier3_chronobiologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "sleep":
        from src.agents.prompts.tier3_sleep import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "neuropsychologist":
        from src.agents.prompts.tier3_neuropsychologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "environment":
        from src.agents.prompts.tier3_environment import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "toxicologist":
        from src.agents.prompts.tier3_toxicologist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    # Tier 4 (Executors)
    elif agent_id == "nutritionist":
        from src.agents.prompts.tier4_nutritionist import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "fitness":
        from src.agents.prompts.tier4_fitness import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    # Tier 5 (Operations)
    elif agent_id == "dispatcher":
        from src.agents.prompts.tier5_dispatcher import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "inventory":
        from src.agents.prompts.tier5_inventory import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "finance":
        from src.agents.prompts.tier5_finance import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "concierge":
        from src.agents.prompts.tier5_concierge import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    # Tier 6 (Support)
    elif agent_id == "qa":
        from src.agents.prompts.tier6_qa import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "ux":
        from src.agents.prompts.tier6_ux import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "developer":
        from src.agents.prompts.tier6_developer import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    elif agent_id == "support":
        from src.agents.prompts.tier6_support import SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG
    else:
        raise ValueError(f"Unknown agent_id: {agent_id}")

    return SYSTEM_PROMPT, OUTPUT_SCHEMA, AGENT_CONFIG


async def call_agent(
    agent_id: str,
    user_message: str,
    state: PLTState,
    client: AsyncAnthropic,
) -> dict:
    """
    Universal function to call any agent via Claude API with structured output.

    Args:
        agent_id: Agent identifier (e.g., 'cmo', 'cardiologist')
        user_message: The prompt/question for the agent
        state: Current PLTState for context
        client: AsyncAnthropic client

    Returns:
        Parsed JSON response from the agent, plus metadata:
        {
            "agent_id": str,
            "output": dict,  # Parsed JSON from Claude
            "confidence": int,
            "tokens": int,
            "latency_ms": int,
            "model": str
        }
    """
    start_time = time.time()

    try:
        # Load agent prompt and config
        system_prompt, output_schema, agent_config = _get_prompt_module(agent_id)

        # Prepare Claude API call with structured output
        response = await client.messages.create(
            model=agent_config.get("model", "claude-opus-4-1"),
            max_tokens=agent_config.get("max_tokens", 3000),
            temperature=agent_config.get("temperature", 0.5),
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )

        # Parse response
        response_text = response.content[0].text

        # Extract JSON from markdown code blocks if present
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_str = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            json_str = response_text[json_start:json_end].strip()
        else:
            json_str = response_text

        parsed_output = json.loads(json_str)

        # Calculate tokens
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        latency_ms = int((time.time() - start_time) * 1000)

        logger.info(
            f"Agent call completed",
            extra={
                "agent_id": agent_id,
                "tokens": tokens_used,
                "latency_ms": latency_ms,
                "confidence": parsed_output.get("confidence_score", 0),
            },
        )

        return {
            "agent_id": agent_id,
            "output": parsed_output,
            "confidence": parsed_output.get("confidence_score", 80),
            "tokens": tokens_used,
            "latency_ms": latency_ms,
            "model": agent_config.get("model", "claude-opus-4-1"),
        }

    except Exception as e:
        logger.error(
            f"Agent call failed",
            extra={"agent_id": agent_id, "error": str(e)},
            exc_info=True,
        )
        raise


async def log_decision(
    session_id: str,
    agent_id: str,
    user_id: str,
    input_data: dict,
    output_data: dict,
    tokens: int,
    latency_ms: int,
) -> None:
    """
    Log an agent decision to the database (async placeholder).

    In production, this would insert into agent_decisions table.
    For now, it's logged to the application log.

    Args:
        session_id: Session UUID
        agent_id: Agent identifier
        user_id: User UUID
        input_data: Input to the agent
        output_data: Output from the agent
        tokens: Tokens consumed
        latency_ms: Latency in milliseconds
    """
    logger.info(
        f"Agent decision logged",
        extra={
            "session_id": session_id,
            "agent_id": agent_id,
            "user_id": user_id,
            "tokens": tokens,
            "latency_ms": latency_ms,
        },
    )
    # TODO: Insert into agent_decisions table when DB session available


def build_agent_context(agent_id: str, state: PLTState) -> str:
    """
    Build the user message for an agent based on what it needs from state.

    Each agent receives only the relevant context from PLTState.

    Args:
        agent_id: Agent identifier
        state: Current PLTState

    Returns:
        Formatted user message for the agent
    """
    digital_twin = state.get("digital_twin", {})
    medical_opinions = state.get("medical_opinions", [])
    lifestyle_opinions = state.get("lifestyle_opinions", [])
    draft_protocol = state.get("draft_protocol", {})

    if agent_id == "system_biologist":
        # Gets trigger_data (biomarkers, wearable, etc.)
        trigger_data = state.get("trigger_data", {})
        return f"""
Please update the Digital Twin based on the latest data:

Trigger Type: {state.get("trigger_type")}
User ID: {state.get("user_id")}

Latest Data:
{json.dumps(trigger_data, indent=2)}

Please return a complete Digital Twin snapshot with all 11 system scores, biological age metrics, anomalies, and cross-system correlations.
"""

    elif agent_id == "analyst":
        # Gets medical_opinions + lifestyle_opinions
        return f"""
Please synthesize these opinions into a draft protocol:

Digital Twin Snapshot:
{json.dumps(digital_twin, indent=2)}

Medical Opinions (from 8 agents):
{json.dumps(medical_opinions, indent=2)}

Lifestyle Opinions (from 5 agents):
{json.dumps(lifestyle_opinions, indent=2)}

Please create a draft protocol, calculate ROI for each recommendation, and identify conflicts.
"""

    elif agent_id == "verifier":
        # Gets draft_protocol
        return f"""
Please verify this draft protocol against PubMed knowledge base and drug interactions:

Draft Protocol:
{json.dumps(draft_protocol, indent=2)}

Please check for:
1. Evidence level for each recommendation
2. Drug interactions
3. Contraindications
4. Safety concerns

Return verdict: approved, vetoed, or needs_revision.
"""

    elif agent_id == "cmo":
        # Gets all opinions + digital_twin + draft_protocol + verifier_result
        verifier_result = state.get("verifier_result", {})
        return f"""
Please review and approve the protocol as CMO:

Digital Twin:
{json.dumps(digital_twin, indent=2)}

Draft Protocol:
{json.dumps(draft_protocol, indent=2)}

Verifier Feedback:
{json.dumps(verifier_result, indent=2)}

Please make final decisions, resolve conflicts, and set priorities.
"""

    elif agent_id == "nutritionist":
        # Gets execution plan context
        cmo_decision = state.get("cmo_decision", {})
        return f"""
Please create a detailed nutrition plan based on CMO approval:

CMO Decision:
{json.dumps(cmo_decision, indent=2)}

Digital Twin:
{json.dumps(digital_twin, indent=2)}

Please return a week-by-week nutrition plan with specific foods, macros, and timing.
"""

    elif agent_id == "fitness":
        # Gets nutrition plan + cmo decision
        execution_plan = state.get("execution_plan", {})
        return f"""
Please create a detailed fitness plan based on nutrition plan:

Execution Plan (Nutrition):
{json.dumps(execution_plan, indent=2)}

CMO Decision:
{json.dumps(state.get("cmo_decision", {}), indent=2)}

Digital Twin:
{json.dumps(digital_twin, indent=2)}

Please return a week-by-week fitness plan that complements the nutrition strategy.
"""

    elif agent_id == "dispatcher":
        # Gets execution_plan
        execution_plan = state.get("execution_plan", {})
        return f"""
Please create daily action contracts from this execution plan:

Execution Plan:
{json.dumps(execution_plan, indent=2)}

Please break down into daily, actionable contracts that the user can execute.
"""

    else:
        # Generic fallback for medical/lifestyle agents
        return f"""
User ID: {state.get("user_id")}

Digital Twin Snapshot:
{json.dumps(digital_twin, indent=2)}

Trigger Type: {state.get("trigger_type")}
Trigger Data:
{json.dumps(state.get("trigger_data", {}), indent=2)}

Please provide your expert opinion and recommendations.
"""
