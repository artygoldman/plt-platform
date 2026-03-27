"""
LangGraph Graph Assembly: THE MAIN ORCHESTRATION ENGINE
Defines the directed graph with all nodes, edges, conditionals, and checkpointing.
"""

import logging
from typing import Literal

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

from src.agents.state import PLTState
from src.agents.nodes import (
    router_node,
    system_biologist_node,
    analyst_node,
    verifier_node,
    cmo_node,
    medical_core_node,
    lifestyle_node,
    executors_node,
    ops_node,
)
from src.agents.nodes.router import should_update_digital_twin, should_run_full_pipeline
from src.core.config import get_settings

logger = logging.getLogger(__name__)


def create_graph():
    """
    Create and compile the PLT orchestration graph.

    Graph structure:
    ```
    router
      ├─→ system_biologist (conditional: if new bloodwork/anomaly)
      │     ├─→ medical_core (fan-out: 8 agents in parallel)
      │     └─→ lifestyle (fan-out: 5 agents in parallel)
      │           ├─→ analyst (join point)
      │           └─→ verifier
      │                 ├─→ CONDITIONAL: if vetoed AND veto_count < 3
      │                 │     └─→ medical_core (loop back)
      │                 └─→ cmo
      │                       └─→ executors
      │                             └─→ ops
      │                                   └─→ END
      └─→ (if daily_morning, skip to executors directly)
    ```

    Returns:
        Compiled graph with PostgreSQL checkpointing
    """
    settings = get_settings()

    # Create state graph
    graph = StateGraph(PLTState)

    # Add all nodes
    graph.add_node("router", router_node)
    graph.add_node("system_biologist", system_biologist_node)
    graph.add_node("medical_core", medical_core_node)
    graph.add_node("lifestyle", lifestyle_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("verifier", verifier_node)
    graph.add_node("cmo", cmo_node)
    graph.add_node("executors", executors_node)
    graph.add_node("ops", ops_node)

    # Add edges
    # Entry point
    graph.add_edge("__start__", "router")

    # Router → system_biologist (conditional)
    graph.add_conditional_edges(
        "router",
        lambda state: "system_biologist"
        if should_update_digital_twin(state)
        else "executors",
    )

    # System Biologist → parallel fan-out
    graph.add_edge("system_biologist", "medical_core")
    graph.add_edge("system_biologist", "lifestyle")

    # Parallel fan-out → analyst (both must complete)
    graph.add_edge("medical_core", "analyst")
    graph.add_edge("lifestyle", "analyst")

    # Analyst → verifier
    graph.add_edge("analyst", "verifier")

    # Verifier → conditional veto loop
    def should_reveto(state: PLTState) -> Literal["medical_core", "cmo"]:
        """
        Conditional: if vetoed and veto_count < 3, loop back to medical_core.
        Otherwise proceed to CMO.
        """
        verifier_result = state.get("verifier_result", {})
        verdict = verifier_result.get("verdict", "approved")
        veto_count = state.get("veto_count", 0)

        if verdict == "vetoed" and veto_count < 3:
            logger.warning(
                f"Verifier veto loop #{veto_count + 1}",
                extra={"user_id": state.get("user_id")},
            )
            return "medical_core"
        else:
            return "cmo"

    graph.add_conditional_edges("verifier", should_reveto)

    # CMO → executors
    graph.add_edge("cmo", "executors")

    # Executors → ops
    graph.add_edge("executors", "ops")

    # Ops → END
    graph.add_edge("ops", END)

    # Compile with PostgreSQL checkpointer
    checkpointer = PostgresSaver(
        sync_connection_string=settings.database_url_sync,
    )

    compiled_graph = graph.compile(checkpointer=checkpointer)

    logger.info("Graph compiled successfully with PostgreSQL checkpointing")

    return compiled_graph


def get_graph():
    """
    Lazy-load singleton for the compiled graph.
    Caches on first call.
    """
    if not hasattr(get_graph, "_instance"):
        get_graph._instance = create_graph()
    return get_graph._instance
