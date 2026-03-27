# Personal Longevity Team API - Phase 1C Endpoints

## Health & Status
- `GET /health` → `{"status": "ok", "version": "0.1.0", "timestamp": "..."}`

## WebSocket
- `WS /ws/v1/live` — Real-time updates (echo server placeholder)

## Data Management (`/api/v1/data`)
- `POST /data/upload` — Upload biomarker file
  - Returns: `{"id": uuid, "status": "processing", "filename": "..."}`
  
- `POST /data/sync/oura` — Sync Oura Ring data
  - Returns: `{"status": "syncing", "source": "oura", "last_sync": null, "data_points": 0}`
  
- `POST /data/sync/apple-health` — Sync Apple Health data
  - Returns: `{"status": "syncing", "source": "apple_health", "last_sync": null, "data_points": 0}`

## Digital Twin (`/api/v1/twin`)
- `GET /twin/{user_id}` → `DigitalTwinResponse`
  - Fields: user_id, biological_age, chronological_age, dunedin_pace, longevity_score, healthspan_forecast_years, mortality_risk_score, systems_status, last_updated
  
- `GET /twin/{user_id}/history` → Twin history timeline
  - Returns: `{"user_id": uuid, "snapshots": [], "metrics_over_time": {}, "trend_analysis": {}}`

## Agent Management (`/api/v1/agents`)
- `POST /agents/run` — Trigger agent cycle
  - Request: `{"user_id": uuid, "trigger_type": "new_data|daily|user_query|alert", "trigger_data": {}}`
  - Returns: `{"session_id": uuid, "status": "running", "trigger_type": "..."}`
  
- `GET /agents/sessions/{session_id}` → `AgentSessionResponse`
  - Fields: id, status, trigger_type, started_at, completed_at, total_tokens, decisions[]

## Daily Contracts (`/api/v1/contracts`)
- `GET /contracts/today` → `ContractResponse`
  - Fields: id, date, contracts[], completion_rate, longevity_delta
  
- `PATCH /contracts/{contract_id}/complete` — Mark contract done
  - Returns: `{"contract_id": uuid, "completed": true, "longevity_impact": 0.0}`

## Longevity Protocols (`/api/v1/protocols`)
- `GET /protocols/active` → `ProtocolResponse`
  - Fields: id, version, status, nutrition_plan, supplement_plan, fitness_plan, sleep_protocol, environment, medical_actions, valid_from, valid_until, approved_by, created_at

## Longevity Score (`/api/v1/score`)
- `GET /score/longevity` → `LongevityScoreResponse`
  - Fields: longevity_score, biological_age, chronological_age, age_delta, dunedin_pace, healthspan_forecast_years, mortality_risk_score, trend_30d, projected_lifespan

## Supplement Inventory (`/api/v1/inventory`)
- `GET /inventory/` → `list[SupplementResponse]`
  - Returns empty list initially
  
- `POST /inventory/` → `SupplementResponse` (201 Created)
  - Request: `{"name": str, "brand": str|null, "dosage_per_unit": str|null, "units_remaining": int|null, "expiry_date": date|null, "auto_reorder": bool}`
  
- `PATCH /inventory/{item_id}` → `SupplementResponse`
  - Request: `{"units_remaining": int|null, "expiry_date": date|null, "auto_reorder": bool|null}`

## Response Types Summary

### UserResponse
- id, email, name, date_of_birth, sex, created_at, subscription_tier

### BiomarkerResponse
- id, time, source, category, marker_name, value, unit, reference_low, reference_high, optimal_low, optimal_high

### DigitalTwinResponse
- user_id, biological_age, chronological_age, dunedin_pace, longevity_score, healthspan_forecast_years, mortality_risk_score, systems_status{}, last_updated

### SystemStatus
- score (0-100), trend (improving|stable|declining), alerts[]

### AgentSessionResponse
- id, status, trigger_type, started_at, completed_at, total_tokens, decisions[]

### AgentDecisionResponse
- id, agent_id, confidence, was_vetoed, output_data, created_at

### ContractResponse
- id, date, contracts[], completion_rate, longevity_delta

### ProtocolResponse
- id, version, status, nutrition_plan, supplement_plan, fitness_plan, sleep_protocol, environment, medical_actions, valid_from, valid_until, approved_by, created_at

### LongevityScoreResponse
- longevity_score, biological_age, chronological_age, age_delta, dunedin_pace, healthspan_forecast_years, mortality_risk_score, trend_30d, projected_lifespan

### SupplementResponse
- id, name, brand, dosage_per_unit, units_remaining, expiry_date, auto_reorder, updated_at

## Error Handling
- 403 Forbidden — Access denied (user_id mismatch)
- 404 Not Found — Resource not found (implied for routes)
- 201 Created — Resource created successfully (POST /inventory/)
- 200 OK — Success (default)

## Authentication (Phase 4)
Currently uses mock user. Will be replaced with JWT tokens in Phase 4.

## CORS
Allows all origins, credentials, methods, and headers (development mode).

