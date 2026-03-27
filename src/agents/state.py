"""
PLT Orchestration State Definition
Shared TypedDict with Annotated fields for LangGraph state management.
"""

from typing import Annotated, TypedDict
import operator
from datetime import datetime


class PLTState(TypedDict):
    """
    Unified state object for the entire orchestration graph.

    Annotated fields with operator.add support list concatenation for parallel fan-out.
    """

    # ==== TRIGGER / SESSION ====
    user_id: str
    """UUID of the user triggering the pipeline."""

    session_id: str
    """Unique session ID for this execution run."""

    trigger_type: str
    """Type of trigger: 'new_bloodwork', 'daily_morning', 'user_query', 'anomaly', 'scheduled'."""

    trigger_data: dict
    """Raw data that triggered the pipeline (e.g., bloodwork results, user question)."""

    started_at: str
    """ISO 8601 timestamp when the session started."""

    # ==== DIGITAL TWIN (Tier 1) ====
    digital_twin: dict
    """
    Complete snapshot of the Digital Twin (all 11 systems, biological age, anomalies).
    Populated by system_biologist_node.

    Structure:
    {
        "timestamp": str,
        "biological_age": {...},
        "system_scores": {...},
        "overall_health_score": int,
        "cross_system_correlations": [...],
        "anomalies_detected": [...],
        "trend_analysis": {...}
    }
    """

    # ==== PARALLEL OPINIONS (Tier 2 & 3) ====
    medical_opinions: Annotated[list[dict], operator.add]
    """
    List of structured opinions from all 8 medical agents (Tier 2).
    Each item: {"agent_id": str, "opinion": dict, "confidence": int, "tokens": int}
    Accumulated via operator.add for parallel fan-out.
    """

    lifestyle_opinions: Annotated[list[dict], operator.add]
    """
    List of structured opinions from all 5 lifestyle agents (Tier 3).
    Each item: {"agent_id": str, "opinion": dict, "confidence": int, "tokens": int}
    Accumulated via operator.add for parallel fan-out.
    """

    # ==== SYNTHESIS (Tier 1 Analyst & Verifier) ====
    draft_protocol: dict
    """
    First-pass synthesis of all opinions by analyst_node.
    Structure: {"nutrition": {...}, "supplements": {...}, "fitness": {...}, "medical_actions": [...]}
    """

    roi_analysis: list[dict]
    """
    ROI/effectiveness analysis for each proposed action.
    Each item: {"action": str, "roi_score": float, "cost_estimate": float, "impact": str}
    """

    verifier_result: dict
    """
    Result of knowledge-base verification by verifier_node.
    Structure: {
        "verdict": "approved"|"vetoed"|"needs_revision",
        "issues": [...],
        "severity": "critical"|"high"|"medium"|"low",
        "recommendations": [...]
    }
    """

    veto_count: int
    """Number of times the draft_protocol has been vetoed and sent back to medical_core."""

    # ==== FINAL DECISION (Tier 1 CMO) ====
    cmo_decision: dict
    """
    Final approved protocol from CMO node.
    Structure: {
        "approved_protocol": {...},
        "priority_actions": [...],
        "biological_age_forecast": {...},
        "escalation_needed": bool,
        "confidence_score": int
    }
    """

    # ==== EXECUTION (Tier 4) ====
    execution_plan: dict
    """
    Detailed execution plan from executors_node (Nutritionist + Fitness Trainer).
    Structure: {
        "nutrition_plan": {...},
        "fitness_plan": {...},
        "timeline": {...}
    }
    """

    # ==== DAILY CONTRACTS (Tier 5) ====
    daily_contracts: list[dict]
    """
    List of actionable daily contracts from dispatcher_node.
    Each item: {
        "date": str,
        "actions": [...],
        "priority": int,
        "is_binding": bool
    }
    """

    # ==== METADATA & ERRORS ====
    errors: Annotated[list[dict], operator.add]
    """
    List of errors encountered during execution.
    Each item: {
        "node": str,
        "agent_id": str,
        "error_type": str,
        "message": str,
        "timestamp": str
    }
    Accumulated via operator.add for collecting errors from parallel nodes.
    """

    total_tokens: int
    """Total tokens consumed by all agent calls in this session."""

    total_cost_usd: float
    """Total estimated cost of this session in USD."""
