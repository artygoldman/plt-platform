# Phase 1C: FastAPI Application Skeleton & Pydantic Schemas

## Overview
Created complete FastAPI application structure with 7 routers and 9 Pydantic schema modules. All endpoints are properly typed with docstrings and marked with `# TODO` comments for Phase 4 implementation.

## Files Created

### Core Application
- **src/api/__init__.py** — Empty package marker
- **src/api/main.py** — FastAPI app with:
  - Title: "Personal Longevity Team API"
  - Version: "0.1.0"
  - Lifespan context manager (creates DB tables on startup via `init_db()`)
  - CORS middleware (allow all origins for development)
  - Health check: `GET /health` → `{"status": "ok", "version": "0.1.0", "timestamp": ...}`
  - All routers included with `/api/v1` prefix
  - WebSocket placeholder at `/ws/v1/live` (echo server for testing)

### Dependencies
- **src/api/deps.py** — Dependency injection:
  - `get_db()` — Async generator for AsyncSession
  - `get_current_user()` — Mock user (will be JWT in Phase 4)

### Routers (all with `/api/v1` prefix)
- **src/api/routers/data.py** (prefix="/data", tags=["Data"])
  - `POST /upload` — File upload placeholder
  - `POST /sync/oura` — Oura Ring sync placeholder
  - `POST /sync/apple-health` — Apple Health sync placeholder

- **src/api/routers/twin.py** (prefix="/twin", tags=["Digital Twin"])
  - `GET /{user_id}` — Get current digital twin state (mock data)
  - `GET /{user_id}/history` — Get twin history (placeholder)

- **src/api/routers/agents.py** (prefix="/agents", tags=["Agents"])
  - `POST /run` — Trigger agent cycle
  - `GET /sessions/{session_id}` — Get session status and decisions (placeholder)

- **src/api/routers/contracts.py** (prefix="/contracts", tags=["Contracts"])
  - `GET /today` — Get today's contracts for current user
  - `PATCH /{contract_id}/complete` — Mark contract as completed

- **src/api/routers/protocols.py** (prefix="/protocols", tags=["Protocols"])
  - `GET /active` — Get active protocol for current user (placeholder)

- **src/api/routers/score.py** (prefix="/score", tags=["Score"])
  - `GET /longevity` — Get longevity score + forecast (mock data)

- **src/api/routers/inventory.py** (prefix="/inventory", tags=["Inventory"])
  - `GET /` — List supplements
  - `POST /` — Add supplement (returns 201)
  - `PATCH /{item_id}` — Update supplement

### Pydantic Schemas
All in `src/api/schemas/` with proper type hints and `ConfigDict(from_attributes=True)`:

- **user.py**
  - `UserCreate` — Email, name, DOB, sex, timezone
  - `UserResponse` — User with UUID and metadata
  - `UserProfileResponse` — Height, weight, blood type, allergies, meds, genetic risks, goals

- **biomarker.py**
  - `BiomarkerCreate` — Source, category, marker name, value, unit, reference/optimal ranges
  - `BiomarkerResponse` — Complete biomarker measurement
  - `BiomarkerHistory` — Historical trend data

- **twin.py**
  - `SystemStatus` — Score (0-100), trend, alerts
  - `DigitalTwinResponse` — Biological/chronological age, dunedin pace, scores, systems status

- **agent.py**
  - `AgentRunRequest` — User ID, trigger type, trigger data
  - `AgentDecisionResponse` — Agent output with confidence and veto status
  - `AgentSessionResponse` — Session with all decisions and token counts

- **protocol.py**
  - `ProtocolResponse` — Full protocol with nutrition/supplement/fitness/sleep/environment/medical plans
  - `ContractItem` — Single actionable commitment (ID, text, category, agent, completion, impact)
  - `ContractResponse` — Daily contracts with completion rate

- **inventory.py**
  - `SupplementCreate` — Name, brand, dosage, units, expiry, auto-reorder
  - `SupplementResponse` — Supplement with UUID and timestamp
  - `SupplementUpdate` — Partial update fields

- **score.py**
  - `LongevityScoreResponse` — Score, biological/chronological age, delta, pace, healthspan, mortality risk, trend, projected lifespan

### Package Init
- **src/api/schemas/__init__.py** — Re-exports all schemas for clean imports

## Key Design Decisions

1. **Mock Data**: All endpoints return mock/placeholder data to demonstrate structure
2. **TODO Comments**: Clear markers for Phase 4 implementation in all routers
3. **Access Control**: Routes check `current_user["id"]` against path parameters for basic authorization
4. **Status Codes**: Proper HTTP codes (201 for creation, 403 for access denied, 404 implied)
5. **Async-first**: All functions are async, ready for AsyncSession
6. **Type Hints**: Complete type hints on all parameters and return values
7. **Docstrings**: All functions have docstrings explaining params and returns

## Dependencies Expected
- FastAPI
- Pydantic with EmailStr
- SQLAlchemy async (AsyncSession)
- `src.db.base` module with `init_db()` and `get_session()`
- `src.db.models` module (assumed but not imported yet)

## Next Steps (Phase 4)
- Implement actual database queries in all routers
- Add JWT authentication in `deps.py`
- Implement agent orchestration logic
- Add file parsing for data imports
- Implement 3rd-party API integrations (Oura, Apple Health)
- Add biomarker calculation engines
- Implement digital twin computation
- Add contract management logic
