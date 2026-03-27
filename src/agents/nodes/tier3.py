"""
Tier 3: Lifestyle Core Nodes (Parallel Fan-Out)
5 lifestyle specialists running in parallel:
- Chronobiologist, Sleep Specialist, Neuropsychologist, Environment Specialist, Toxicologist
"""

import asyncio
import logging
from datetime import datetime
from anthropic import AsyncAnthropic

from src.agents.state import PLTState
from src.agents.nodes.common import call_agent, log_decision, build_agent_context
from src.core.config import get_settings

logger = logging.getLogger(__name__)

# All 5 Tier 3 lifestyle agents
LIFESTYLE_AGENTS = [
    "chronobiologist",
    "sleep",
    "neuropsychologist",
    "environment",
    "toxicologist",
]


async def _run_single_lifestyle_agent(
    agent_id: str,
    state: PLTState,
    client: AsyncAnthropic,
) -> dict:
    """
    Helper: Run a single lifestyle agent.

    Args:
        agent_id: e.g., "chronobiologist", "sleep"
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
            f"Lifestyle agent {agent_id} failed",
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


async def lifestyle_node(state: PLTState) -> dict:
    """
    Lifestyle Node: Runs all 5 lifestyle agents in parallel via asyncio.gather().

    Fan-out pattern:
    1. Digital Twin snapshot is shared with all agents
    2. Each agent analyzes their specialty from the Twin
    3. All opinions are collected into lifestyle_opinions list
    4. State aggregation via operator.add (LangGraph feature)

    Returns:
        Updated state with lifestyle_opinions list
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "Lifestyle Core: Starting parallel execution of 5 agents",
        extra={"user_id": user_id, "session_id": session_id},
    )

    try:
        # Run all lifestyle agents in parallel
        tasks = [
            _run_single_lifestyle_agent(agent_id, state, client)
            for agent_id in LIFESTYLE_AGENTS
        ]

        opinions = await asyncio.gather(*tasks, return_exceptions=False)

        # Track errors
        failed_agents = [op for op in opinions if op.get("failed", False)]
        successful_agents = [op for op in opinions if not op.get("failed", False)]

        if failed_agents:
            logger.warning(
                f"Lifestyle Core: {len(failed_agents)} agents failed out of {len(LIFESTYLE_AGENTS)}",
                extra={
                    "user_id": user_id,
                    "failed_agents": [f["agent_id"] for f in failed_agents],
                },
            )

        # Aggregate tokens
        total_tokens = sum(op.get("tokens", 0) for op in opinions)

        logger.info(
            f"Lifestyle Core: Completed. {len(successful_agents)}/{len(LIFESTYLE_AGENTS)} agents succeeded.",
            extra={
                "user_id": user_id,
                "session_id": session_id,
                "total_tokens": total_tokens,
            },
        )

        # Return state update
        # lifestyle_opinions will be concatenated via operator.add
        return {
            "lifestyle_opinions": opinions,
            "total_tokens": state.get("total_tokens", 0) + total_tokens,
        }

    except Exception as e:
        logger.error(
            "Lifestyle Core node failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "lifestyle_node",
                    "agent_id": "lifestyle_core",
                    "error_type": "parallel_execution_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "lifestyle_opinions": [],
        }
