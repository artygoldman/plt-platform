"""
Tier 2: Medical Core Nodes (Parallel Fan-Out)
8 medical specialists running in parallel:
- Cardiologist, Endocrinologist, Metabolologist, Microbiome Specialist
- Dermatologist, Aesthetist, Orthopedist, Geneticist
"""

import asyncio
import logging
from datetime import datetime
from anthropic import AsyncAnthropic

from src.agents.state import PLTState
from src.agents.nodes.common import call_agent, log_decision, build_agent_context
from src.core.config import get_settings

logger = logging.getLogger(__name__)

# All 8 Tier 2 medical agents
MEDICAL_AGENTS = [
    "cardiologist",
    "endocrinologist",
    "metabolologist",
    "microbiome",
    "dermatologist",
    "aesthetist",
    "orthopedist",
    "geneticist",
]


async def _run_single_medical_agent(
    agent_id: str,
    state: PLTState,
    client: AsyncAnthropic,
) -> dict:
    """
    Helper: Run a single medical agent.

    Args:
        agent_id: e.g., "cardiologist"
        state: Current PLTState
        client: AsyncAnthropic client

    Returns:
        Opinion dict: {"agent_id": str, "opinion": dict, "confidence": int, "tokens": int}
    """
    user_id = state.get("user_id")
    session_id = state.get("session_id")

    try:
        # Build context for this agent
        user_message = build_agent_context(agent_id, state)

        # Call agent
        result = await call_agent(
            agent_id=agent_id,
            user_message=user_message,
            state=state,
            client=client,
        )

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id=agent_id,
            user_id=user_id,
            input_data=state.get("digital_twin", {}),
            output_data=result["output"],
            tokens=result["tokens"],
            latency_ms=result["latency_ms"],
        )

        # Return opinion
        return {
            "agent_id": agent_id,
            "opinion": result["output"],
            "confidence": result.get("confidence", 80),
            "tokens": result["tokens"],
            "latency_ms": result["latency_ms"],
        }

    except Exception as e:
        logger.error(
            f"Medical agent {agent_id} failed",
            extra={"user_id": user_id, "agent_id": agent_id, "error": str(e)},
            exc_info=True,
        )
        # Return error opinion instead of crashing
        return {
            "agent_id": agent_id,
            "opinion": {
                "status": "error",
                "error": str(e),
            },
            "confidence": 0,
            "tokens": 0,
            "latency_ms": 0,
            "failed": True,
        }


async def medical_core_node(state: PLTState) -> dict:
    """
    Medical Core Node: Runs all 8 medical agents in parallel via asyncio.gather().

    Fan-out pattern:
    1. Digital Twin snapshot is shared with all agents
    2. Each agent analyzes their specialty from the Twin
    3. All opinions are collected into medical_opinions list
    4. State aggregation via operator.add (LangGraph feature)

    Returns:
        Updated state with medical_opinions list
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "Medical Core: Starting parallel execution of 8 agents",
        extra={"user_id": user_id, "session_id": session_id},
    )

    try:
        # Run all medical agents in parallel
        tasks = [
            _run_single_medical_agent(agent_id, state, client)
            for agent_id in MEDICAL_AGENTS
        ]

        opinions = await asyncio.gather(*tasks, return_exceptions=False)

        # Track errors
        failed_agents = [op for op in opinions if op.get("failed", False)]
        successful_agents = [op for op in opinions if not op.get("failed", False)]

        if failed_agents:
            logger.warning(
                f"Medical Core: {len(failed_agents)} agents failed out of {len(MEDICAL_AGENTS)}",
                extra={
                    "user_id": user_id,
                    "failed_agents": [f["agent_id"] for f in failed_agents],
                },
            )

        # Aggregate tokens
        total_tokens = sum(op.get("tokens", 0) for op in opinions)

        logger.info(
            f"Medical Core: Completed. {len(successful_agents)}/{len(MEDICAL_AGENTS)} agents succeeded.",
            extra={
                "user_id": user_id,
                "session_id": session_id,
                "total_tokens": total_tokens,
            },
        )

        # Return state update
        # medical_opinions will be concatenated via operator.add
        return {
            "medical_opinions": opinions,
            "total_tokens": state.get("total_tokens", 0) + total_tokens,
        }

    except Exception as e:
        logger.error(
            "Medical Core node failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "medical_core_node",
                    "agent_id": "medical_core",
                    "error_type": "parallel_execution_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "medical_opinions": [],
        }
