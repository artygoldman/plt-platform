"""
Tier 4: Executor Nodes (Sequential)
Nutritionist → Fitness Trainer
The trainer respects the nutrition plan and adds complementary fitness recommendations.
"""

import logging
from datetime import datetime
from anthropic import AsyncAnthropic

from src.agents.state import PLTState
from src.agents.nodes.common import call_agent, log_decision, build_agent_context
from src.core.config import get_settings

logger = logging.getLogger(__name__)


async def executors_node(state: PLTState) -> dict:
    """
    Executors Node: Runs Nutritionist and Fitness Trainer sequentially.

    Sequence:
    1. Nutritionist: Creates detailed nutrition plan from CMO decision
    2. Fitness Trainer: Creates fitness plan that respects nutrition + medical constraints

    Both agents respect all restrictions from medical_opinions and lifestyle_opinions.

    Returns:
        Updated state with execution_plan (nutrition + fitness)
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "Executors: Starting Nutritionist → Fitness Trainer",
        extra={"user_id": user_id, "session_id": session_id},
    )

    execution_plan = {}
    total_tokens = state.get("total_tokens", 0)

    try:
        # Step 1: Nutritionist
        logger.info(
            "Executors: Calling Nutritionist",
            extra={"user_id": user_id, "session_id": session_id},
        )

        user_message = build_agent_context("nutritionist", state)

        nutritionist_result = await call_agent(
            agent_id="nutritionist",
            user_message=user_message,
            state=state,
            client=client,
        )

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id="nutritionist",
            user_id=user_id,
            input_data=state.get("cmo_decision", {}),
            output_data=nutritionist_result["output"],
            tokens=nutritionist_result["tokens"],
            latency_ms=nutritionist_result["latency_ms"],
        )

        execution_plan["nutrition"] = nutritionist_result["output"]
        total_tokens += nutritionist_result["tokens"]

        logger.info(
            "Executors: Nutritionist completed",
            extra={"user_id": user_id, "tokens": nutritionist_result["tokens"]},
        )

        # Step 2: Fitness Trainer (gets nutrition plan in context)
        logger.info(
            "Executors: Calling Fitness Trainer",
            extra={"user_id": user_id, "session_id": session_id},
        )

        # Update state temporarily to include nutrition plan for trainer context
        state_with_nutrition = {
            **state,
            "execution_plan": execution_plan,
        }

        user_message = build_agent_context("fitness", state_with_nutrition)

        fitness_result = await call_agent(
            agent_id="fitness",
            user_message=user_message,
            state=state_with_nutrition,
            client=client,
        )

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id="fitness",
            user_id=user_id,
            input_data=state.get("cmo_decision", {}),
            output_data=fitness_result["output"],
            tokens=fitness_result["tokens"],
            latency_ms=fitness_result["latency_ms"],
        )

        execution_plan["fitness"] = fitness_result["output"]
        total_tokens += fitness_result["tokens"]

        logger.info(
            "Executors: Fitness Trainer completed",
            extra={"user_id": user_id, "tokens": fitness_result["tokens"]},
        )

        return {
            "execution_plan": execution_plan,
            "total_tokens": total_tokens,
        }

    except Exception as e:
        logger.error(
            "Executors node failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "executors_node",
                    "agent_id": "executors",
                    "error_type": "sequential_execution_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "execution_plan": execution_plan,
            "total_tokens": total_tokens,
        }
