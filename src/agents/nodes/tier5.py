"""
Tier 5: Operations Nodes (Sequential)
Dispatcher → Inventory Check → Finance → Concierge (optional)

Creates actionable daily contracts and checks feasibility.
"""

import json
import logging
from datetime import datetime
from anthropic import AsyncAnthropic

from src.agents.state import PLTState
from src.agents.nodes.common import call_agent, log_decision, build_agent_context
from src.core.config import get_settings

logger = logging.getLogger(__name__)


async def ops_node(state: PLTState) -> dict:
    """
    Operations Node: Creates and validates daily action contracts.

    Sequence:
    1. Dispatcher: Converts execution_plan into daily_contracts
    2. Inventory: Checks if supplements/items are in stock
    3. Finance: Calculates costs and checks budget
    4. Concierge: (Optional) Schedules medical appointments if needed

    Returns:
        Updated state with daily_contracts and final metadata
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "Operations: Starting Dispatcher → Inventory → Finance pipeline",
        extra={"user_id": user_id, "session_id": session_id},
    )

    daily_contracts = []
    total_tokens = state.get("total_tokens", 0)

    try:
        # Step 1: Dispatcher - Create daily contracts
        logger.info(
            "Operations: Calling Dispatcher",
            extra={"user_id": user_id, "session_id": session_id},
        )

        user_message = build_agent_context("dispatcher", state)

        dispatcher_result = await call_agent(
            agent_id="dispatcher",
            user_message=user_message,
            state=state,
            client=client,
        )

        await log_decision(
            session_id=session_id,
            agent_id="dispatcher",
            user_id=user_id,
            input_data=state.get("execution_plan", {}),
            output_data=dispatcher_result["output"],
            tokens=dispatcher_result["tokens"],
            latency_ms=dispatcher_result["latency_ms"],
        )

        daily_contracts = dispatcher_result["output"].get("daily_contracts", [])
        total_tokens += dispatcher_result["tokens"]

        logger.info(
            f"Operations: Dispatcher created {len(daily_contracts)} daily contracts",
            extra={"user_id": user_id, "tokens": dispatcher_result["tokens"]},
        )

        # Step 2: Inventory Check
        logger.info(
            "Operations: Calling Inventory",
            extra={"user_id": user_id, "session_id": session_id},
        )

        # Build inventory context
        inventory_message = f"""
User ID: {user_id}

Daily Contracts to fulfill:
{json.dumps(daily_contracts, indent=2)}

Please check inventory for all required items (supplements, foods, equipment).
Return availability status and suggest substitutions if needed.
"""

        inventory_result = await call_agent(
            agent_id="inventory",
            user_message=inventory_message,
            state=state,
            client=client,
        )

        await log_decision(
            session_id=session_id,
            agent_id="inventory",
            user_id=user_id,
            input_data={"daily_contracts": daily_contracts},
            output_data=inventory_result["output"],
            tokens=inventory_result["tokens"],
            latency_ms=inventory_result["latency_ms"],
        )

        inventory_status = inventory_result["output"]
        total_tokens += inventory_result["tokens"]

        logger.info(
            "Operations: Inventory check completed",
            extra={"user_id": user_id, "tokens": inventory_result["tokens"]},
        )

        # Step 3: Finance - Calculate costs
        logger.info(
            "Operations: Calling Finance",
            extra={"user_id": user_id, "session_id": session_id},
        )

        finance_message = f"""
User ID: {user_id}

Daily Contracts:
{json.dumps(daily_contracts, indent=2)}

Inventory Status:
{json.dumps(inventory_status, indent=2)}

Please calculate total costs, check budget constraints, and provide cost breakdown.
"""

        finance_result = await call_agent(
            agent_id="finance",
            user_message=finance_message,
            state=state,
            client=client,
        )

        await log_decision(
            session_id=session_id,
            agent_id="finance",
            user_id=user_id,
            input_data={"daily_contracts": daily_contracts, "inventory": inventory_status},
            output_data=finance_result["output"],
            tokens=finance_result["tokens"],
            latency_ms=finance_result["latency_ms"],
        )

        finance_analysis = finance_result["output"]
        total_tokens += finance_result["tokens"]
        total_cost_usd = finance_analysis.get("total_cost_usd", 0.0)

        logger.info(
            "Operations: Finance analysis completed",
            extra={
                "user_id": user_id,
                "total_cost_usd": total_cost_usd,
                "tokens": finance_result["tokens"],
            },
        )

        # Step 4: Concierge (optional - only if medical appointments needed)
        concierge_result = {}
        cmo_decision = state.get("cmo_decision", {})
        medical_actions = cmo_decision.get("approved_protocol", {}).get("medical_actions", [])

        if medical_actions:
            logger.info(
                "Operations: Calling Concierge for appointment scheduling",
                extra={"user_id": user_id, "session_id": session_id},
            )

            concierge_message = f"""
User ID: {user_id}

Medical actions requiring scheduling:
{json.dumps(medical_actions, indent=2)}

Please create appointment requests and provide calendar links.
"""

            concierge_result = await call_agent(
                agent_id="concierge",
                user_message=concierge_message,
                state=state,
                client=client,
            )

            await log_decision(
                session_id=session_id,
                agent_id="concierge",
                user_id=user_id,
                input_data={"medical_actions": medical_actions},
                output_data=concierge_result["output"],
                tokens=concierge_result["tokens"],
                latency_ms=concierge_result["latency_ms"],
            )

            total_tokens += concierge_result["tokens"]

            logger.info(
                "Operations: Concierge scheduling completed",
                extra={"user_id": user_id, "tokens": concierge_result["tokens"]},
            )

        return {
            "daily_contracts": daily_contracts,
            "inventory_status": inventory_status,
            "finance_analysis": finance_analysis,
            "concierge_result": concierge_result,
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost_usd,
        }

    except Exception as e:
        logger.error(
            "Operations node failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "ops_node",
                    "agent_id": "ops",
                    "error_type": "operations_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "daily_contracts": daily_contracts,
            "total_tokens": total_tokens,
            "total_cost_usd": state.get("total_cost_usd", 0.0),
        }
