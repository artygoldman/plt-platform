"""
Tier 1: Strategic Core Nodes
System Biologist, Analyst, Verifier, CMO
"""

import json
import logging
from datetime import datetime
from anthropic import AsyncAnthropic

from src.agents.state import PLTState
from src.agents.nodes.common import call_agent, log_decision, build_agent_context
from src.core.config import get_settings

logger = logging.getLogger(__name__)


async def system_biologist_node(state: PLTState) -> dict:
    """
    System Biologist Node: Loads and updates the Digital Twin.

    Aggregates all data sources (biomarkers, wearables, genetic, lifestyle, environmental)
    into a unified Digital Twin model with 11 system scores, biological age, anomalies.

    Returns:
        Updated state with digital_twin populated
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "System Biologist: Building Digital Twin",
        extra={"user_id": user_id, "session_id": session_id},
    )

    try:
        # Build context from state
        user_message = build_agent_context("system_biologist", state)

        # Call agent
        result = await call_agent(
            agent_id="system_biologist",
            user_message=user_message,
            state=state,
            client=client,
        )

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id="system_biologist",
            user_id=user_id,
            input_data=state.get("trigger_data", {}),
            output_data=result["output"],
            tokens=result["tokens"],
            latency_ms=result["latency_ms"],
        )

        # Update state
        return {
            "digital_twin": result["output"].get("digital_twin_snapshot", {}),
            "total_tokens": state.get("total_tokens", 0) + result["tokens"],
        }

    except Exception as e:
        logger.error(
            "System Biologist failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "system_biologist_node",
                    "agent_id": "system_biologist",
                    "error_type": "api_call_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "digital_twin": {},  # Empty twin on error
        }


async def analyst_node(state: PLTState) -> dict:
    """
    Analyst Node: Synthesizes opinions into a draft protocol and ROI analysis.

    Takes medical_opinions and lifestyle_opinions (accumulated from parallel agents),
    combines with digital_twin snapshot, and produces:
    - draft_protocol: combined recommendations
    - roi_analysis: effectiveness scores for each recommendation
    - conflict_resolution: how conflicts between agents were resolved

    Returns:
        Updated state with draft_protocol and roi_analysis
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "Analyst: Synthesizing opinions",
        extra={
            "user_id": user_id,
            "session_id": session_id,
            "medical_opinions": len(state.get("medical_opinions", [])),
            "lifestyle_opinions": len(state.get("lifestyle_opinions", [])),
        },
    )

    try:
        # Build context
        user_message = build_agent_context("analyst", state)

        # Call agent
        result = await call_agent(
            agent_id="analyst",
            user_message=user_message,
            state=state,
            client=client,
        )

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id="analyst",
            user_id=user_id,
            input_data={
                "medical_opinions": state.get("medical_opinions", []),
                "lifestyle_opinions": state.get("lifestyle_opinions", []),
            },
            output_data=result["output"],
            tokens=result["tokens"],
            latency_ms=result["latency_ms"],
        )

        # Update state
        return {
            "draft_protocol": result["output"].get("draft_protocol", {}),
            "roi_analysis": result["output"].get("roi_analysis", []),
            "conflict_resolution": result["output"].get("conflict_resolution", []),
            "total_tokens": state.get("total_tokens", 0) + result["tokens"],
        }

    except Exception as e:
        logger.error(
            "Analyst failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "analyst_node",
                    "agent_id": "analyst",
                    "error_type": "api_call_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "draft_protocol": {},
            "roi_analysis": [],
        }


async def verifier_node(state: PLTState) -> dict:
    """
    Verifier Node: Checks draft protocol against knowledge base.

    Validates:
    - Evidence level for each recommendation (PubMed references)
    - Drug interactions
    - Contraindications
    - Safety concerns
    - Dosage appropriateness

    Returns verdict: "approved", "vetoed", or "needs_revision"

    Returns:
        Updated state with verifier_result and conditional veto_count
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "Verifier: Checking draft protocol",
        extra={"user_id": user_id, "session_id": session_id},
    )

    try:
        # Build context
        user_message = build_agent_context("verifier", state)

        # Call agent
        result = await call_agent(
            agent_id="verifier",
            user_message=user_message,
            state=state,
            client=client,
        )

        verifier_result = result["output"]

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id="verifier",
            user_id=user_id,
            input_data=state.get("draft_protocol", {}),
            output_data=verifier_result,
            tokens=result["tokens"],
            latency_ms=result["latency_ms"],
        )

        # Check verdict
        verdict = verifier_result.get("verdict", "needs_revision")
        veto_count = state.get("veto_count", 0)

        if verdict == "vetoed":
            veto_count += 1
            logger.warning(
                f"Protocol vetoed (veto #{veto_count})",
                extra={"user_id": user_id, "session_id": session_id},
            )

        return {
            "verifier_result": verifier_result,
            "veto_count": veto_count,
            "total_tokens": state.get("total_tokens", 0) + result["tokens"],
        }

    except Exception as e:
        logger.error(
            "Verifier failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "verifier_node",
                    "agent_id": "verifier",
                    "error_type": "api_call_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "verifier_result": {"verdict": "needs_revision", "issues": []},
        }


async def cmo_node(state: PLTState) -> dict:
    """
    CMO Node: Final approval and protocol synthesis.

    Chief Medical Officer makes final decisions:
    - Approves, modifies, or rejects recommendations
    - Resolves conflicts between agents
    - Sets action priorities
    - Checks financial constraints
    - Generates biological age forecast
    - Flags escalations to human doctor

    Returns:
        Updated state with cmo_decision
    """
    settings = get_settings()
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    user_id = state.get("user_id")
    session_id = state.get("session_id")

    logger.info(
        "CMO: Approving protocol",
        extra={"user_id": user_id, "session_id": session_id},
    )

    try:
        # Build context
        user_message = build_agent_context("cmo", state)

        # Call agent
        result = await call_agent(
            agent_id="cmo",
            user_message=user_message,
            state=state,
            client=client,
        )

        cmo_decision = result["output"]

        # Log decision
        await log_decision(
            session_id=session_id,
            agent_id="cmo",
            user_id=user_id,
            input_data=state.get("draft_protocol", {}),
            output_data=cmo_decision,
            tokens=result["tokens"],
            latency_ms=result["latency_ms"],
        )

        # Check for escalation
        escalation_needed = cmo_decision.get("escalation_needed", False)
        if escalation_needed:
            logger.warning(
                f"CMO escalation required: {cmo_decision.get('escalation_reason', 'unknown')}",
                extra={"user_id": user_id, "session_id": session_id},
            )

        return {
            "cmo_decision": cmo_decision,
            "total_tokens": state.get("total_tokens", 0) + result["tokens"],
        }

    except Exception as e:
        logger.error(
            "CMO failed",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True,
        )
        return {
            "errors": [
                {
                    "node": "cmo_node",
                    "agent_id": "cmo",
                    "error_type": "api_call_failed",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
            "cmo_decision": {},
        }
