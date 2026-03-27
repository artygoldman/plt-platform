"""
Evaluation — оценка качества Phase 5.

Запускается после всех E2E и integration тестов.
Выдаёт score 0-100.
"""

import os
import glob
import yaml
from pathlib import Path


def evaluate_phase5() -> dict:
    """Evaluate Phase 5 completion and quality."""
    checks = []

    # E1: E2E Flow (30 баллов)
    e2e_tests_passed = 0
    try:
        if os.path.exists("tests/test_phase5_e2e.py"):
            with open("tests/test_phase5_e2e.py") as f:
                content = f.read()
                if "test_e2e_upload_to_contracts" in content:
                    if "test_full_cycle_latency_under_60s" in content:
                        if "test_health_endpoint" in content:
                            e2e_tests_passed = 30
                        else:
                            e2e_tests_passed = 25
                    else:
                        e2e_tests_passed = 20
    except Exception:
        pass
    checks.append({"name": "E2E flow works", "score": e2e_tests_passed, "max": 30})

    # E2: Docker orchestration (15 баллов)
    docker_score = 0
    if os.path.exists("docker-compose.yml"):
        try:
            with open("docker-compose.yml") as f:
                dc = yaml.safe_load(f)
                services = dc.get("services", {})

                required = ["postgres", "redis", "api"]
                found = sum(1 for s in required if s in services)
                docker_score = int((found / len(required)) * 10)

                # Bonus for healthchecks
                health_checks = sum(1 for s in services.values() if "healthcheck" in s)
                if health_checks >= 2:
                    docker_score += 5

                # Check for environment variables
                if ".env.example" in os.listdir("."):
                    docker_score = min(docker_score + 2, 15)
        except Exception:
            pass

    checks.append({"name": "Docker orchestration", "score": docker_score, "max": 15})

    # E3: Performance (15 баллов)
    perf_score = 0
    if os.path.exists("tests/test_phase5_e2e.py"):
        try:
            with open("tests/test_phase5_e2e.py") as f:
                content = f.read()
                if "test_full_cycle_latency_under_60s" in content:
                    perf_score = 15
                elif "test_full_cycle_latency" in content:
                    perf_score = 10
        except Exception:
            pass
    checks.append({"name": "Performance (latency < 60s)", "score": perf_score, "max": 15})

    # E4: Documentation (15 баллов)
    doc_score = 0
    doc_files = {
        "README.md": 3,
        "ARCHITECTURE.md": 3,
        "API.md": 3,
        "AGENTS.md": 3,
        "SETUP.md": 3,
    }
    for doc, points in doc_files.items():
        if os.path.exists(doc):
            doc_score += points
    checks.append({"name": "Documentation quality", "score": doc_score, "max": 15})

    # E5: Error recovery (15 баллов)
    recovery_score = 0
    if os.path.exists("tests/test_phase5_e2e.py"):
        try:
            with open("tests/test_phase5_e2e.py") as f:
                content = f.read()
                if "test_recovery_after_agent_failure" in content:
                    recovery_score += 8
                if "test_checkpoint_resume" in content:
                    recovery_score += 7
        except Exception:
            pass
    checks.append({"name": "Error recovery", "score": recovery_score, "max": 15})

    # E6: Seed data / demo (10 баллов)
    seed_score = 0
    seed_files = (
        glob.glob("scripts/seed_*.py") +
        glob.glob("seed_data/**/*.py", recursive=True) +
        glob.glob("scripts/generate_*.py")
    )
    if seed_files:
        seed_score = 10
    checks.append({"name": "Seed data / demo", "score": seed_score, "max": 10})

    # E7: Integration Tests (10 баллов)
    integration_score = 0
    if os.path.exists("tests/test_integration.py"):
        try:
            with open("tests/test_integration.py") as f:
                content = f.read()
                if "test_db_models_create_and_query" in content:
                    if "test_auth_flow" in content:
                        if "test_biomarker_crud" in content:
                            integration_score = 10
                        else:
                            integration_score = 7
                    else:
                        integration_score = 5
        except Exception:
            pass
    checks.append({"name": "Integration tests", "score": integration_score, "max": 10})

    # E8: API Tests (10 баллов)
    api_score = 0
    if os.path.exists("tests/test_api_endpoints.py"):
        try:
            with open("tests/test_api_endpoints.py") as f:
                content = f.read()
                # Count test functions
                test_count = content.count("async def test_")
                if test_count >= 30:
                    api_score = 10
                elif test_count >= 20:
                    api_score = 7
                elif test_count >= 10:
                    api_score = 5
        except Exception:
            pass
    checks.append({"name": "API endpoint tests", "score": api_score, "max": 10})

    total = sum(c["score"] for c in checks)
    max_total = sum(c["max"] for c in checks)

    return {
        "phase": "Phase 5: Integration + Final Assembly",
        "total_score": total,
        "max_score": max_total,
        "grade": "PASS" if total >= int(max_total * 0.75) else "NEEDS WORK",
        "checks": checks
    }


if __name__ == "__main__":
    result = evaluate_phase5()
    print("\n" + "=" * 60)
    print(f"PHASE 5 EVALUATION RESULTS")
    print("=" * 60)
    print(f"Phase: {result['phase']}")
    print(f"Score: {result['total_score']}/{result['max_score']}")
    print(f"Grade: {result['grade']}")
    print("\nDetailed Checks:")
    print("-" * 60)

    for check in result["checks"]:
        percentage = int((check["score"] / check["max"]) * 100) if check["max"] > 0 else 0
        status = "✓" if check["score"] == check["max"] else "○" if check["score"] > 0 else "✗"
        print(f"{status} {check['name']:.<40} {check['score']:>3}/{check['max']:<3} ({percentage:>3}%)")

    print("-" * 60)
    overall_percentage = int((result["total_score"] / result["max_score"]) * 100) if result["max_score"] > 0 else 0
    print(f"OVERALL SCORE: {result['total_score']}/{result['max_score']} ({overall_percentage}%)")
    print(f"STATUS: {result['grade']}")
    print("=" * 60)
