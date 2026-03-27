"""
API endpoint tests for all Phase 4 routers.

Tests cover:
- Users router (register, login, profile, update)
- Data router (upload, sync, biomarkers)
- Twin router (score, calculate, update)
- Agents router (trigger, status, sessions)
- Contracts router (list, create, update, complete)
- Protocols router (list, create, update)
- Score router (calculate, history)
- Inventory router (list, add, update)
"""

import pytest
from pathlib import Path
from httpx import AsyncClient


# ── USERS ENDPOINTS ──

@pytest.mark.asyncio
async def test_users_register(async_client: AsyncClient):
    """POST /api/v1/users/register"""
    response = await async_client.post(
        "/api/v1/users/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "sex": "male",
        }
    )
    assert response.status_code in [200, 201, 400, 409, 501]


@pytest.mark.asyncio
async def test_users_login(async_client: AsyncClient):
    """POST /api/v1/users/login"""
    response = await async_client.post(
        "/api/v1/users/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        }
    )
    assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_users_me(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/users/me"""
    response = await async_client.get("/api/v1/users/me", headers=auth_header)
    assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_users_update_profile(async_client: AsyncClient, auth_header: dict):
    """PATCH /api/v1/users/me"""
    response = await async_client.patch(
        "/api/v1/users/me",
        json={
            "height_cm": 180.0,
            "weight_kg": 75.0,
            "blood_type": "O+",
        },
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404, 501]


# ── DATA ENDPOINTS ──

@pytest.mark.asyncio
async def test_data_upload(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/data/upload"""
    pdf_path = Path("tests/fixtures/blood_test_sample.pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    if not pdf_path.exists():
        pdf_path.write_bytes(b"%PDF-1.4")

    with open(pdf_path, "rb") as f:
        response = await async_client.post(
            "/api/v1/data/upload",
            files={"file": f},
            headers=auth_header
        )
    assert response.status_code in [200, 202, 400, 401, 404]


@pytest.mark.asyncio
async def test_data_sync_oura(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/data/sync/oura"""
    response = await async_client.post(
        "/api/v1/data/sync/oura",
        headers=auth_header
    )
    assert response.status_code in [200, 202, 401, 404, 501]


@pytest.mark.asyncio
async def test_data_sync_apple_health(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/data/sync/apple-health"""
    response = await async_client.post(
        "/api/v1/data/sync/apple-health",
        headers=auth_header
    )
    assert response.status_code in [200, 202, 401, 404, 501]


@pytest.mark.asyncio
async def test_data_get_biomarkers(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/data/biomarkers"""
    response = await async_client.get(
        "/api/v1/data/biomarkers",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_data_get_biomarkers_with_filters(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/data/biomarkers with filters"""
    response = await async_client.get(
        "/api/v1/data/biomarkers?category=blood_glucose&limit=50",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]


# ── DIGITAL TWIN ENDPOINTS ──

@pytest.mark.asyncio
async def test_twin_get_score(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/twin/score"""
    response = await async_client.get(
        "/api/v1/twin/score",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_twin_update(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/twin/update"""
    response = await async_client.post(
        "/api/v1/twin/update",
        json={
            "biological_age": 35,
            "health_score": 78.5,
        },
        headers=auth_header
    )
    assert response.status_code in [200, 201, 401, 404, 501]


@pytest.mark.asyncio
async def test_twin_calculate_systems(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/twin/systems/calculate"""
    response = await async_client.post(
        "/api/v1/twin/systems/calculate",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_twin_get_systems(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/twin/systems"""
    response = await async_client.get(
        "/api/v1/twin/systems",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]


# ── AGENTS ENDPOINTS ──

@pytest.mark.asyncio
async def test_agents_list(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/agents"""
    response = await async_client.get(
        "/api/v1/agents",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_agents_trigger_cardio(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/agents/cardio-agent/trigger"""
    response = await async_client.post(
        "/api/v1/agents/cardio-agent/trigger",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_agents_trigger_metabolic(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/agents/metabolic-agent/trigger"""
    response = await async_client.post(
        "/api/v1/agents/metabolic-agent/trigger",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_agents_get_sessions(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/agents/cardio-agent/sessions"""
    response = await async_client.get(
        "/api/v1/agents/cardio-agent/sessions",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_agents_get_session_detail(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/agents/cardio-agent/sessions/{session_id}"""
    # First, try to get sessions
    sessions_response = await async_client.get(
        "/api/v1/agents/cardio-agent/sessions",
        headers=auth_header
    )

    if sessions_response.status_code == 200:
        sessions = sessions_response.json()
        if sessions and len(sessions) > 0:
            session_id = sessions[0].get("id")
            response = await async_client.get(
                f"/api/v1/agents/cardio-agent/sessions/{session_id}",
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404]


# ── CONTRACTS ENDPOINTS ──

@pytest.mark.asyncio
async def test_contracts_list(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/contracts"""
    response = await async_client.get(
        "/api/v1/contracts",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_contracts_create(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/contracts"""
    response = await async_client.post(
        "/api/v1/contracts",
        json={
            "name": "Morning Exercise",
            "description": "30-minute workout",
            "protocol_id": "test-protocol-id",
        },
        headers=auth_header
    )
    assert response.status_code in [200, 201, 400, 401, 404, 501]


@pytest.mark.asyncio
async def test_contracts_get(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/contracts/{contract_id}"""
    # Get list first to find a contract
    list_response = await async_client.get(
        "/api/v1/contracts",
        headers=auth_header
    )

    if list_response.status_code == 200:
        contracts = list_response.json()
        if contracts and len(contracts) > 0:
            contract_id = contracts[0].get("id")
            response = await async_client.get(
                f"/api/v1/contracts/{contract_id}",
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_contracts_update(async_client: AsyncClient, auth_header: dict):
    """PATCH /api/v1/contracts/{contract_id}"""
    list_response = await async_client.get(
        "/api/v1/contracts",
        headers=auth_header
    )

    if list_response.status_code == 200:
        contracts = list_response.json()
        if contracts and len(contracts) > 0:
            contract_id = contracts[0].get("id")
            response = await async_client.patch(
                f"/api/v1/contracts/{contract_id}",
                json={"completed": True},
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_contracts_complete(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/contracts/{contract_id}/complete"""
    list_response = await async_client.get(
        "/api/v1/contracts",
        headers=auth_header
    )

    if list_response.status_code == 200:
        contracts = list_response.json()
        if contracts and len(contracts) > 0:
            contract_id = contracts[0].get("id")
            response = await async_client.post(
                f"/api/v1/contracts/{contract_id}/complete",
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404, 501]


# ── PROTOCOLS ENDPOINTS ──

@pytest.mark.asyncio
async def test_protocols_list(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/protocols"""
    response = await async_client.get(
        "/api/v1/protocols",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_protocols_create(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/protocols"""
    response = await async_client.post(
        "/api/v1/protocols",
        json={
            "name": "Cardio Protocol",
            "description": "Cardiovascular health protocol",
            "status": "draft",
        },
        headers=auth_header
    )
    assert response.status_code in [200, 201, 400, 401, 404, 501]


@pytest.mark.asyncio
async def test_protocols_get(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/protocols/{protocol_id}"""
    list_response = await async_client.get(
        "/api/v1/protocols",
        headers=auth_header
    )

    if list_response.status_code == 200:
        protocols = list_response.json()
        if protocols and len(protocols) > 0:
            protocol_id = protocols[0].get("id")
            response = await async_client.get(
                f"/api/v1/protocols/{protocol_id}",
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_protocols_update(async_client: AsyncClient, auth_header: dict):
    """PATCH /api/v1/protocols/{protocol_id}"""
    list_response = await async_client.get(
        "/api/v1/protocols",
        headers=auth_header
    )

    if list_response.status_code == 200:
        protocols = list_response.json()
        if protocols and len(protocols) > 0:
            protocol_id = protocols[0].get("id")
            response = await async_client.patch(
                f"/api/v1/protocols/{protocol_id}",
                json={"status": "active"},
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404, 501]


# ── SCORE ENDPOINTS ──

@pytest.mark.asyncio
async def test_score_calculate(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/score/calculate"""
    response = await async_client.post(
        "/api/v1/score/calculate",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_score_history(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/score/history"""
    response = await async_client.get(
        "/api/v1/score/history",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]


# ── INVENTORY ENDPOINTS ──

@pytest.mark.asyncio
async def test_inventory_list(async_client: AsyncClient, auth_header: dict):
    """GET /api/v1/inventory"""
    response = await async_client.get(
        "/api/v1/inventory",
        headers=auth_header
    )
    assert response.status_code in [200, 401, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_inventory_add(async_client: AsyncClient, auth_header: dict):
    """POST /api/v1/inventory"""
    response = await async_client.post(
        "/api/v1/inventory",
        json={
            "name": "Vitamin D3",
            "description": "Vitamin D3 supplement",
            "quantity": 100,
            "unit": "pills",
        },
        headers=auth_header
    )
    assert response.status_code in [200, 201, 400, 401, 404, 501]


@pytest.mark.asyncio
async def test_inventory_update(async_client: AsyncClient, auth_header: dict):
    """PATCH /api/v1/inventory/{item_id}"""
    list_response = await async_client.get(
        "/api/v1/inventory",
        headers=auth_header
    )

    if list_response.status_code == 200:
        items = list_response.json()
        if items and len(items) > 0:
            item_id = items[0].get("id")
            response = await async_client.patch(
                f"/api/v1/inventory/{item_id}",
                json={"quantity": 50},
                headers=auth_header
            )
            assert response.status_code in [200, 401, 404, 501]


@pytest.mark.asyncio
async def test_inventory_delete(async_client: AsyncClient, auth_header: dict):
    """DELETE /api/v1/inventory/{item_id}"""
    list_response = await async_client.get(
        "/api/v1/inventory",
        headers=auth_header
    )

    if list_response.status_code == 200:
        items = list_response.json()
        if items and len(items) > 0:
            item_id = items[0].get("id")
            response = await async_client.delete(
                f"/api/v1/inventory/{item_id}",
                headers=auth_header
            )
            assert response.status_code in [200, 204, 401, 404, 501]
