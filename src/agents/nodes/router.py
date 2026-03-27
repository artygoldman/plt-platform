"""
Router Node: Entry point that determines the execution path based on trigger_type.
"""

import logging
from src.agents.state import PLTState

logger = logging.getLogger(__name__)


def router_node(state: PLTState) -> dict:
    """
    Router node that determines which path to take based on trigger_type.

    Paths:
    - "new_bloodwork" → full pipeline (system_biologist → medical → lifestyle → analyst → verifier → cmo → executors → ops)
    - "daily_morning" → skip system_biologist, go straight to executors (replay existing protocol)
    - "user_query" → route to specific specialist based on query intent
    - "anomaly" → full pipeline
    - "scheduled" → full pipeline or replay depending on config

    Args:
        state: Current PLTState

    Returns:
        Updated state dict with routing decision
    """
    trigger_type = state.get("trigger_type", "unknown")
    user_id = state.get("user_id", "unknown")

    logger.info(
        f"Router node: processing {trigger_type} trigger",
        extra={"user_id": user_id, "trigger_type": trigger_type},
    )

    # All paths lead to system_biologist first (if new data) or directly to executors
    # The actual graph edges will handle the conditional logic

    # Update state with routing metadata
    return {
        "router_decision": trigger_type,
    }


def should_update_digital_twin(state: PLTState) -> bool:
    """
    Conditional: whether to call system_biologist (update digital twin).

    True for: new_bloodwork, anomaly, scheduled
    False for: daily_morning (use existing twin), user_query (optional)
    """
    trigger_type = state.get("trigger_type", "unknown")
    return trigger_type in ["new_bloodwork", "anomaly", "scheduled"]


def should_run_full_pipeline(state: PLTState) -> bool:
    """
    Conditional: whether to run full pipeline vs. quick execution path.

    True for: new_bloodwork, anomaly, scheduled, user_query (complex)
    False for: daily_morning (quick replay)
    """
    trigger_type = state.get("trigger_type", "unknown")
    return trigger_type != "daily_morning"
