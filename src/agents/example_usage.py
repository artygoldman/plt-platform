"""
Example Usage: How to run the PLT orchestration engine

This file demonstrates all the different ways to invoke the agent pipeline.
"""

import asyncio
from src.agents.runner import run_agent_pipeline, run_agent_pipeline_sync


# Example 1: Sync usage (blocking, simplest)
def example_sync():
    """
    Simplest synchronous usage - blocks until complete.
    Good for: Scripts, background jobs, WSGI apps.
    """
    result = run_agent_pipeline_sync(
        user_id="user-123",
        trigger_type="new_bloodwork",
        trigger_data={
            "biomarkers": {
                "glucose": 95,
                "hdl": 52,
                "ldl": 130,
                "triglycerides": 90,
                "tsh": 2.3,
                "cortisol": 15,
                "crp": 1.2,
                "tgf_beta": 42,
                "tnf_alpha": 1.8,
                "il6": 2.1,
                "hemoglobin": 14.5,
                "hematocrit": 43,
                "wbc": 6.2,
                "magnesium": 25,
                "vitamin_d": 45,
                "b12": 450,
            },
            "wearable": {
                "heart_rate": 62,
                "heart_rate_variability": 35,
                "sleep_hours": 7.2,
                "sleep_quality": 0.85,
                "steps": 8500,
                "vo2_max": 42,
                "body_temperature": 36.7,
            },
            "genetic": {
                "apoe_genotype": "3/3",
                "mthfr": "ct",
                "ldlr": "normal",
            },
            "lifestyle": {
                "exercise_hours_per_week": 4.5,
                "nutrition_quality_score": 7.5,
                "sleep_consistency": 0.8,
                "stress_level": 5,
            },
        },
    )

    print(f"Status: {result['status']}")
    print(f"Session ID: {result['session_id']}")
    print(f"Total tokens: {result['total_tokens']}")
    print(f"Total cost: ${result['total_cost_usd']:.2f}")
    print(f"Duration: {result['duration_seconds']:.1f}s")
    print(f"Daily contracts: {len(result['daily_contracts'])}")

    if result["status"] == "completed":
        print("\nFirst daily contract:")
        if result["daily_contracts"]:
            print(result["daily_contracts"][0])

        print("\nCMO decision priorities:")
        for action in result["cmo_decision"].get("priority_actions", [])[:3]:
            print(f"  - {action.get('action')}: {action.get('urgency')}")

    return result


# Example 2: Async usage (non-blocking, for ASGI/FastAPI)
async def example_async():
    """
    Async usage - returns immediately, doesn't block event loop.
    Good for: FastAPI, ASGI apps, concurrent requests.
    """
    result = await run_agent_pipeline(
        user_id="user-456",
        trigger_type="daily_morning",
        trigger_data={},  # For daily_morning, use empty trigger_data
    )

    print(f"Status: {result['status']}")
    return result


# Example 3: Multiple concurrent users
async def example_concurrent():
    """
    Run pipeline for multiple users concurrently.
    Demonstrates parallelism at the request level.
    """
    user_ids = ["user-100", "user-101", "user-102"]

    tasks = [
        run_agent_pipeline(
            user_id=uid,
            trigger_type="daily_morning",
            trigger_data={},
        )
        for uid in user_ids
    ]

    results = await asyncio.gather(*tasks)

    print(f"Completed {len(results)} user pipelines in parallel")
    for result in results:
        print(f"  - {result['session_id']}: {result['status']}")

    return results


# Example 4: Handling different trigger types
def example_all_triggers():
    """
    Shows how to handle different trigger types.
    """
    triggers = [
        ("new_bloodwork", {"biomarkers": {...}}),
        ("daily_morning", {}),
        ("user_query", {"query": "Should I take more vitamin D?"}),
        ("anomaly", {"anomaly": "cortisol spike", "severity": "high"}),
        ("scheduled", {}),
    ]

    for trigger_type, trigger_data in triggers:
        print(f"\nRunning {trigger_type}...")
        result = run_agent_pipeline_sync(
            user_id="user-789",
            trigger_type=trigger_type,
            trigger_data=trigger_data,
        )
        print(f"  Status: {result['status']}, Duration: {result['duration_seconds']:.1f}s")


# Example 5: Checking for errors and handling gracefully
def example_error_handling():
    """
    Shows how to handle errors in the result.
    """
    result = run_agent_pipeline_sync(
        user_id="user-999",
        trigger_type="new_bloodwork",
        trigger_data={
            "biomarkers": {
                # Minimal data - some agents might fail
                "glucose": 95,
            },
        },
    )

    if result["status"] == "failed":
        print("Pipeline failed!")
        for error in result["errors"]:
            print(f"  {error['node']}: {error['message']}")
        return None

    if result["status"] == "vetoed":
        print("Protocol was vetoed by verifier")
        print(f"Veto reason: {result['verifier_result'].get('issues', [])}")
        return None

    # Success path
    print("Pipeline completed successfully")
    return result


# Example 6: Accessing detailed results
def example_detailed_results():
    """
    Shows how to extract and use detailed results.
    """
    result = run_agent_pipeline_sync(
        user_id="user-detail",
        trigger_type="new_bloodwork",
        trigger_data={
            "biomarkers": {
                "glucose": 95,
                "hdl": 52,
                "ldl": 130,
            },
        },
    )

    if result["status"] != "completed":
        return

    # Digital Twin: Complete health snapshot
    digital_twin = result["digital_twin"]
    print(f"Overall health score: {digital_twin.get('overall_health_score', 0)}")
    print(f"Biological age: {digital_twin.get('biological_age', {}).get('phenoage', '?')}")
    print(f"System scores:")
    for system, score_data in digital_twin.get("system_scores", {}).items():
        print(f"  {system}: {score_data.get('score')}/100 ({score_data.get('trend')})")

    # CMO Decision: What to do
    cmo = result["cmo_decision"]
    print(f"\nApproved protocol:")
    print(f"  Confidence: {cmo.get('confidence_score')}%")
    print(f"  Next review: {cmo.get('next_review_date')}")
    if cmo.get("escalation_needed"):
        print(f"  WARNING: Escalation needed: {cmo.get('escalation_reason')}")

    # Execution Plan: How to do it
    exec_plan = result["execution_plan"]
    print(f"\nExecution plan:")
    print(f"  Nutrition plan items: {len(exec_plan.get('nutrition', {}).get('meals', []))}")
    print(f"  Fitness plan items: {len(exec_plan.get('fitness', {}).get('workouts', []))}")

    # Daily Contracts: What to do today
    contracts = result["daily_contracts"]
    print(f"\nDaily contracts ({len(contracts)} days):")
    for contract in contracts[:3]:
        print(f"  {contract.get('date')}: {len(contract.get('actions', []))} actions")
        for action in contract.get("actions", [])[:2]:
            print(f"    - {action.get('description')} ({action.get('priority')})")

    # Cost analysis
    print(f"\nCost: ${result['total_cost_usd']:.2f}")


if __name__ == "__main__":
    print("=" * 60)
    print("PLT Agent Orchestration Examples")
    print("=" * 60)

    # Run example 1 (sync)
    print("\n1. Synchronous Usage")
    print("-" * 60)
    example_sync()

    # Run example 4 (all triggers)
    print("\n2. Different Trigger Types")
    print("-" * 60)
    example_all_triggers()

    # Run example 5 (error handling)
    print("\n3. Error Handling")
    print("-" * 60)
    example_error_handling()

    # Run example 6 (detailed results)
    print("\n4. Detailed Results")
    print("-" * 60)
    example_detailed_results()

    # Run example 2 and 3 (async)
    print("\n5. Async Usage")
    print("-" * 60)
    asyncio.run(example_async())

    print("\n6. Concurrent Users")
    print("-" * 60)
    asyncio.run(example_concurrent())

    print("\n" + "=" * 60)
    print("All examples completed!")
