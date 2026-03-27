"""
High-Level Runner: Entry point for executing the PLT orchestration pipeline.
"""

import uuid
import logging
from datetime import datetime
from typing import Optional

from src.agents.graph import get_graph
from src.agents.state import PLTState

logger = logging.getLogger(__name__)


async def run_agent_pipeline(
    user_id: str,
    trigger_type: str,
    trigger_data: dict = None,
) -> dict:
    """
    Main entry point: Run the complete agent orchestration pipeline.

    This is the high-level interface that:
    1. Creates a unique session ID
    2. Initializes PLTState
    3. Runs the LangGraph orchestration
    4. Returns final results (daily_contracts, protocol, etc.)

    Args:
        user_id: User UUID (string or UUID)
        trigger_type: Type of trigger
            - "new_bloodwork": New biomarker data
            - "daily_morning": Daily protocol execution
            - "user_query": User asked a specific question
            - "anomaly": System detected an anomaly
            - "scheduled": Scheduled review
        trigger_data: Raw data that triggered the pipeline (biomarkers, query, etc.)

    Returns:
        Dictionary with results:
        {
            "session_id": str,
            "status": "completed"|"failed"|"vetoed",
            "daily_contracts": [...],
            "cmo_decision": {...},
            "execution_plan": {...},
            "digital_twin": {...},
            "errors": [...],
            "total_tokens": int,
            "total_cost_usd": float,
            "duration_seconds": float
        }
    """
    session_id = str(uuid.uuid4())
    start_time = datetime.utcnow()

    logger.info(
        "Agent pipeline started",
        extra={
            "user_id": user_id,
            "session_id": session_id,
            "trigger_type": trigger_type,
        },
    )

    if trigger_data is None:
        trigger_data = {}

    try:
        # Get compiled graph
        graph = get_graph()

        # Initialize state
        initial_state: PLTState = {
            "user_id": str(user_id),
            "session_id": session_id,
            "trigger_type": trigger_type,
            "trigger_data": trigger_data,
            "started_at": start_time.isoformat(),
            "digital_twin": {},
            "medical_opinions": [],
            "lifestyle_opinions": [],
            "draft_protocol": {},
            "roi_analysis": [],
            "verifier_result": {},
            "veto_count": 0,
            "cmo_decision": {},
            "execution_plan": {},
            "daily_contracts": [],
            "errors": [],
            "total_tokens": 0,
            "total_cost_usd": 0.0,
        }

        # Run graph with checkpoint (thread_id = session_id for history)
        final_state = await graph.ainvoke(
            initial_state,
            config={
                "configurable": {"thread_id": session_id},
            },
        )

        # Extract results
        status = "completed"
        if final_state.get("errors"):
            if any(err.get("node") == "verifier_node" for err in final_state["errors"]):
                status = "vetoed"
            else:
                status = "failed"

        duration_seconds = (datetime.utcnow() - start_time).total_seconds()

        result = {
            "session_id": session_id,
            "status": status,
            "daily_contracts": final_state.get("daily_contracts", []),
            "cmo_decision": final_state.get("cmo_decision", {}),
            "execution_plan": final_state.get("execution_plan", {}),
            "digital_twin": final_state.get("digital_twin", {}),
            "verifier_result": final_state.get("verifier_result", {}),
            "errors": final_state.get("errors", []),
            "total_tokens": final_state.get("total_tokens", 0),
            "total_cost_usd": final_state.get("total_cost_usd", 0.0),
            "duration_seconds": duration_seconds,
        }

        logger.info(
            "Agent pipeline completed",
            extra={
                "user_id": user_id,
                "session_id": session_id,
                "status": status,
                "duration_seconds": duration_seconds,
                "tokens": result["total_tokens"],
                "cost_usd": result["total_cost_usd"],
            },
        )

        return result

    except Exception as e:
        logger.error(
            "Agent pipeline failed",
            extra={"user_id": user_id, "session_id": session_id, "error": str(e)},
            exc_info=True,
        )

        duration_seconds = (datetime.utcnow() - start_time).total_seconds()

        return {
            "session_id": session_id,
            "status": "failed",
            "daily_contracts": [],
            "cmo_decision": {},
            "execution_plan": {},
            "digital_twin": {},
            "verifier_result": {},
            "errors": [
                {
                    "node": "runner",
                    "agent_id": "runner",
                    "error_type": "pipeline_execution_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "duration_seconds": duration_seconds,
        }


def run_agent_pipeline_sync(
    user_id: str,
    trigger_type: str,
    trigger_data: dict = None,
) -> dict:
    """
    Synchronous wrapper for run_agent_pipeline (for non-async contexts).

    Uses asyncio.run() internally.

    Args:
        user_id: User UUID
        trigger_type: Trigger type
        trigger_data: Raw trigger data

    Returns:
        Same as run_agent_pipeline
    """
    import asyncio

    return asyncio.run(
        run_agent_pipeline(user_id=user_id, trigger_type=trigger_type, trigger_data=trigger_data)
    )
