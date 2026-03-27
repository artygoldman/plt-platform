# API Documentation

## Base Information

- **Base URL**: `http://localhost:8000/api/v1`
- **Protocol**: HTTPS (localhost HTTP for development)
- **Response Format**: JSON
- **Pagination**: Uses `skip` (default 0) and `limit` (default 50)
- **Date Format**: ISO 8601 (e.g., `2026-03-27T10:30:00Z`)
- **UUID Format**: Standard UUID v4

## Authentication

All endpoints (except `/users/register` and `/users/login`) require JWT Bearer token authentication.

```bash
curl -H "Authorization: Bearer <your_jwt_token>" http://localhost:8000/api/v1/users/me
```

**Token Format**: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Token Expiration**: 24 hours (configurable via `JWT_EXPIRATION_MINUTES`)

**Refresh Token**: Send to `POST /api/v1/users/refresh` to get new token

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `202 Accepted`: Async task queued
- `400 Bad Request`: Invalid parameters or validation failure
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Insufficient permissions (e.g., wrong user_id)
- `404 Not Found`: Resource does not exist
- `422 Unprocessable Entity`: Request body validation error
- `500 Internal Server Error`: Server error

---

## Users Router (`/api/v1/users`)

### Register User

**POST** `/users/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "date_of_birth": "1981-03-27",
  "sex": "male"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "name": "John Doe",
    "subscription_tier": "premium",
    "timezone": "UTC"
  }
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!",
    "name": "John Doe",
    "date_of_birth": "1981-03-27",
    "sex": "male"
  }'
```

**Errors:**
- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Password too short (<8 chars) or invalid date_of_birth

---

### Login User

**POST** `/users/login`

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "name": "John Doe",
    "subscription_tier": "premium",
    "timezone": "UTC"
  }
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

**Errors:**
- `401 Unauthorized`: Invalid email or password

---

### Get Current User Profile

**GET** `/users/me`

Retrieve profile of authenticated user.

**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "name": "John Doe",
  "date_of_birth": "1981-03-27",
  "sex": "male",
  "subscription_tier": "premium",
  "timezone": "UTC",
  "profile": {
    "height_cm": 180.0,
    "weight_kg": 82.5,
    "blood_type": "O+",
    "allergies": ["peanuts", "shellfish"],
    "medications": ["metformin_500mg_daily"],
    "contraindications": ["statins_cause_myalgia"],
    "genetic_risks": {
      "APOE4": true,
      "familial_hypercholesterolemia": false
    },
    "goals": ["reduce_biological_age", "improve_sleep", "increase_muscle_mass"]
  }
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Update User Profile

**PUT** `/users/me`

Update profile information (height, weight, allergies, medications, goals, etc.).

**Request Body:**
```json
{
  "height_cm": 180.0,
  "weight_kg": 82.5,
  "blood_type": "O+",
  "allergies": ["peanuts", "shellfish"],
  "medications": ["metformin_500mg_daily"],
  "goals": ["reduce_biological_age", "improve_sleep"]
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "profile": {
    "height_cm": 180.0,
    "weight_kg": 82.5,
    ...
  }
}
```

---

## Data Router (`/api/v1/data`)

### Upload Biomarker File

**POST** `/data/upload`

Upload PDF blood test or biomarker file. Returns immediately with upload_id; processing happens in background.

**Request:**
```
multipart/form-data
- file: <PDF, CSV, or JSON file>
```

**Response (202 Accepted):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "processing",
  "filename": "blood_test_2026_03_27.pdf",
  "message": "File is being processed. Check /upload/{id} for status."
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/data/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@blood_test.pdf"
```

---

### Sync Oura Ring Data

**POST** `/data/sync/oura`

Synchronize sleep, activity, and readiness data from Oura API.

**Request Body:** (empty)

**Response (202 Accepted):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "syncing",
  "source": "oura",
  "message": "Oura Ring sync started"
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/v1/data/sync/oura \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Sync Apple Health Data

**POST** `/data/sync/apple-health`

Process exported Apple Health XML to extract health metrics.

**Request Body:** (empty, or attach XML file)

**Response (202 Accepted):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "status": "syncing",
  "source": "apple_health",
  "message": "Apple Health sync started"
}
```

---

### Get Biomarker History

**GET** `/data/biomarkers`

Retrieve paginated biomarker history.

**Query Parameters:**
- `marker_name` (optional): Filter by marker (e.g., "ApoB", "hsCRP")
- `category` (optional): Filter by category (e.g., "lipids", "inflammation")
- `days` (default 365): Look back this many days
- `skip` (default 0): Pagination offset
- `limit` (default 100): Pagination limit

**Response (200 OK):**
```json
{
  "markers": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440010",
      "time": "2026-03-27T10:30:00Z",
      "marker_name": "ApoB",
      "category": "lipids",
      "value": 85.5,
      "unit": "mg/dL",
      "reference_low": 0.0,
      "reference_high": 130.0,
      "optimal_low": 0.0,
      "optimal_high": 70.0,
      "source": "blood_test",
      "status": "optimal"
    },
    ...
  ],
  "total": 42,
  "skip": 0,
  "limit": 100
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/v1/data/biomarkers?category=lipids&days=90" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Get Single Biomarker

**GET** `/data/biomarkers/{biomarker_id}`

Retrieve a specific biomarker record.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440010",
  "time": "2026-03-27T10:30:00Z",
  "marker_name": "ApoB",
  "category": "lipids",
  "value": 85.5,
  "unit": "mg/dL",
  "source": "blood_test"
}
```

---

## Twin Router (`/api/v1/twin`)

### Get Current Digital Twin

**GET** `/twin`

Retrieve the latest Digital Twin snapshot with all 11 biological systems.

**Response (200 OK):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "biological_age": 42.5,
  "chronological_age": 45.0,
  "dunedin_pace": 0.95,
  "longevity_score": 72,
  "healthspan_forecast_years": 35.0,
  "mortality_risk_score": 18.5,
  "systems_status": {
    "cardiovascular": {
      "score": 78,
      "trend": "improving",
      "alerts": []
    },
    "metabolic": {
      "score": 65,
      "trend": "stable",
      "alerts": ["blood_glucose_trending_up"]
    },
    "cognitive": {
      "score": 82,
      "trend": "stable",
      "alerts": []
    },
    "immune": {
      "score": 71,
      "trend": "declining",
      "alerts": ["inflammation_markers_elevated"]
    },
    "hormonal": {"score": 75, "trend": "stable", "alerts": []},
    "neurological": {"score": 80, "trend": "improving", "alerts": []},
    "renal": {"score": 88, "trend": "stable", "alerts": []},
    "hepatic": {"score": 85, "trend": "stable", "alerts": []},
    "bone": {"score": 72, "trend": "declining", "alerts": []},
    "muscular": {"score": 70, "trend": "stable", "alerts": []},
    "sleep_circadian": {"score": 68, "trend": "improving", "alerts": []}
  },
  "last_updated": "2026-03-27T10:30:00Z"
}
```

---

### Rebuild Digital Twin

**POST** `/twin/rebuild`

Force immediate recalculation of Digital Twin (normally done during agent pipeline).

**Request Body:** (empty)

**Response (202 Accepted):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440100",
  "status": "processing",
  "message": "Digital Twin rebuild queued"
}
```

---

### Get Twin Systems Status

**GET** `/twin/systems`

Retrieve status of all 11 biological systems.

**Response (200 OK):**
```json
{
  "systems": {
    "cardiovascular": {"score": 78, "status": "good"},
    "metabolic": {"score": 65, "status": "needs_improvement"},
    ...
  }
}
```

---

### Get Twin History

**GET** `/twin/history`

Retrieve historical Digital Twin snapshots.

**Query Parameters:**
- `start_date` (optional, ISO 8601)
- `end_date` (optional, ISO 8601)
- `skip` (default 0)
- `limit` (default 100)

**Response (200 OK):**
```json
{
  "history": [
    {
      "timestamp": "2026-03-27T10:30:00Z",
      "biological_age": 42.5,
      "longevity_score": 72
    },
    {
      "timestamp": "2026-02-27T10:30:00Z",
      "biological_age": 42.8,
      "longevity_score": 71
    }
  ],
  "total": 12
}
```

---

### Get Twin Score

**GET** `/twin/score`

Alias for getting longevity score from twin. See Score router `/score` endpoint.

---

## Agents Router (`/api/v1/agents`)

### Trigger Agent Pipeline

**POST** `/agents/run`

Initiate full 6-tier agent orchestration.

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "trigger_type": "new_data",
  "trigger_data": {
    "biomarker_ids": ["id1", "id2"],
    "reason": "New blood test results"
  }
}
```

**Response (202 Accepted):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440200",
  "status": "queued",
  "trigger_type": "new_data",
  "message": "Agent pipeline has been queued for execution"
}
```

**Trigger Types:**
- `new_data`: Triggered by biomarker upload
- `daily`: Scheduled daily analysis
- `user_query`: User-initiated question
- `alert`: Anomaly threshold breached

---

### List Agent Sessions

**GET** `/agents/sessions`

Retrieve paginated list of agent execution sessions.

**Query Parameters:**
- `skip` (default 0)
- `limit` (default 50)
- `status_filter` (optional): "running" | "completed" | "failed"

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440200",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "trigger_type": "new_data",
      "status": "completed",
      "started_at": "2026-03-27T10:30:00Z",
      "completed_at": "2026-03-27T10:45:30Z",
      "total_tokens": 8500,
      "total_cost_usd": 0.85
    }
  ],
  "total": 15
}
```

---

### Get Session Details

**GET** `/agents/sessions/{session_id}`

Retrieve full details of a specific agent session.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440200",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "trigger_type": "new_data",
  "status": "completed",
  "duration_seconds": 930,
  "total_tokens": 8500,
  "total_cost_usd": 0.85,
  "decisions_count": 13,
  "protocol_generated": true,
  "contracts_generated": 30
}
```

---

### Get Agent Decisions

**GET** `/agents/decisions`

Retrieve decisions made by all agents in a session.

**Query Parameters:**
- `session_id` (required): Filter by session
- `agent_id` (optional): Filter by agent
- `skip` (default 0)
- `limit` (default 50)

**Response (200 OK):**
```json
{
  "decisions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440300",
      "session_id": "550e8400-e29b-41d4-a716-446655440200",
      "agent_id": "cardiologist",
      "agent_name": "Cardiologist",
      "confidence": 92,
      "was_vetoed": false,
      "output_summary": "ApoB suboptimal, recommend statin therapy review",
      "created_at": "2026-03-27T10:32:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440301",
      "session_id": "550e8400-e29b-41d4-a716-446655440200",
      "agent_id": "sleep_specialist",
      "agent_name": "Sleep Specialist",
      "confidence": 85,
      "was_vetoed": false,
      "output_summary": "Sleep duration adequate, optimize sleep timing",
      "created_at": "2026-03-27T10:35:00Z"
    }
  ],
  "total": 13
}
```

---

### Get Agent Status

**GET** `/agents/status`

Real-time status of running agents or last execution summary.

**Response (200 OK):**
```json
{
  "current_session": {
    "id": "550e8400-e29b-41d4-a716-446655440200",
    "status": "running",
    "current_tier": 2,
    "current_agent": "endocrinologist",
    "progress_percent": 35,
    "estimated_remaining_seconds": 450
  }
}
```

---

## Contracts Router (`/api/v1/contracts`)

### Get Today's Contracts

**GET** `/contracts/today`

Retrieve daily health contracts for today.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440400",
  "date": "2026-03-27",
  "contracts": [
    {
      "id": "contract_1",
      "time": "07:00",
      "action": "exercise_30min_running",
      "description": "Zone 2 running (easy pace)",
      "priority": 1,
      "points": 5,
      "is_binding": true,
      "completed": false
    },
    {
      "id": "contract_2",
      "time": "08:00",
      "action": "take_supplements",
      "description": "NAD+, omega-3, magnesium",
      "priority": 2,
      "points": 3,
      "is_binding": false,
      "completed": false
    },
    {
      "id": "contract_3",
      "time": "12:00",
      "action": "eat_lunch",
      "description": "Grilled chicken, quinoa, vegetables",
      "priority": 2,
      "points": 3,
      "is_binding": false,
      "completed": false
    }
  ],
  "completion_rate": 0.0,
  "longevity_delta": null
}
```

---

### Get Contracts for Specific Date

**GET** `/contracts/{target_date}`

Retrieve contracts for a specific date (YYYY-MM-DD).

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440401",
  "date": "2026-03-20",
  "contracts": [...],
  "completion_rate": 0.75,
  "longevity_delta": 0.25
}
```

---

### Mark Contract Complete

**POST** `/contracts/complete`

Mark a contract as completed.

**Request Body:**
```json
{
  "contract_id": "contract_1",
  "date": "2026-03-27",
  "notes": "Completed 32 minutes at zone 2"
}
```

**Response (200 OK):**
```json
{
  "status": "completed",
  "points_awarded": 5,
  "longevity_delta": 0.05
}
```

---

### Skip Contract

**POST** `/contracts/skip`

Mark a contract as skipped (not completed).

**Request Body:**
```json
{
  "contract_id": "contract_2",
  "date": "2026-03-27",
  "reason": "Felt fatigued"
}
```

**Response (200 OK):**
```json
{
  "status": "skipped",
  "points_lost": 0,
  "longevity_delta": 0.0
}
```

---

### Get Contract Streak

**GET** `/contracts/streak`

Retrieve current contract completion streak.

**Response (200 OK):**
```json
{
  "current_streak_days": 14,
  "longest_streak_days": 32,
  "completion_rate_30d": 0.82,
  "completion_rate_90d": 0.78,
  "points_30d": 342,
  "points_90d": 998
}
```

---

### Get Contract History

**GET** `/contracts/history`

Retrieve paginated contract history.

**Query Parameters:**
- `days` (default 90)
- `skip` (default 0)
- `limit` (default 100)

**Response (200 OK):**
```json
{
  "history": [
    {
      "date": "2026-03-27",
      "completion_rate": 0.75,
      "longevity_delta": 0.25,
      "points_earned": 11
    },
    {
      "date": "2026-03-26",
      "completion_rate": 1.0,
      "longevity_delta": 0.35,
      "points_earned": 15
    }
  ],
  "total": 27
}
```

---

### Get Contract Statistics

**GET** `/contracts/stats`

Retrieve aggregated contract statistics.

**Response (200 OK):**
```json
{
  "total_contracts_ever": 892,
  "total_completed": 734,
  "total_skipped": 158,
  "overall_completion_rate": 0.82,
  "average_points_per_day": 11.5,
  "total_longevity_gain_days": 8.3
}
```

---

## Protocols Router (`/api/v1/protocols`)

### Get Active Protocol

**GET** `/protocols/active`

Retrieve the currently active longevity protocol.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440500",
  "version": 3,
  "status": "active",
  "created_at": "2026-02-01T10:30:00Z",
  "valid_from": "2026-02-01",
  "valid_until": "2026-05-01",
  "approved_by": "cmo",
  "nutrition_plan": {
    "macro_targets": {
      "protein_g": 120,
      "fat_g": 80,
      "carbs_g": 200
    },
    "micronutrient_focus": ["magnesium", "vitamin_d3", "omega_3"],
    "meal_plan": {
      "breakfast": "scrambled_eggs_berries_coffee",
      "lunch": "grilled_chicken_quinoa_vegetables",
      "dinner": "salmon_sweet_potato_leafy_greens"
    }
  },
  "supplement_plan": {
    "daily": [
      {"name": "NAD+", "dosage": "500mg", "rationale": "mitochondrial energy"},
      {"name": "Omega-3", "dosage": "2g EPA+DHA", "rationale": "cardiovascular"}
    ]
  },
  "fitness_plan": {
    "cardio": "150 min/week moderate intensity",
    "strength": "3x/week full body",
    "flexibility": "daily 10 min yoga",
    "weekly_schedule": {
      "monday": "30 min running zone 2",
      "wednesday": "30 min cycling zone 3",
      "saturday": "90 min hike zone 2"
    }
  },
  "sleep_protocol": {
    "target_bedtime": "22:30",
    "target_wake_time": "06:30",
    "consistency": "same time every day",
    "sleep_duration_hours": 8.0,
    "recommendations": ["dim_lights_2h_before_bed", "cool_bedroom_65F"]
  },
  "environment": {
    "blue_light_exposure": "minimize after 8 PM",
    "temperature": "maintain 65-68F during sleep",
    "toxin_avoidance": ["plastic_containers", "non_stick_cookware"]
  },
  "medical_actions": [
    {
      "action": "consult_cardiologist",
      "priority": "high",
      "reason": "suboptimal ApoB, review statin therapy"
    }
  ]
}
```

---

### List All Protocols

**GET** `/protocols`

Retrieve paginated list of all user protocols.

**Query Parameters:**
- `skip` (default 0)
- `limit` (default 50)
- `status_filter` (optional): "draft" | "approved" | "active" | "archived"

**Response (200 OK):**
```json
{
  "protocols": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440500",
      "version": 3,
      "status": "active",
      "created_at": "2026-02-01T10:30:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440501",
      "version": 2,
      "status": "archived",
      "created_at": "2025-11-01T10:30:00Z"
    }
  ],
  "total": 8
}
```

---

### Get Protocol History

**GET** `/protocols/history`

Retrieve version history of protocols.

**Response (200 OK):**
```json
{
  "history": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440500",
      "version": 3,
      "status": "active",
      "created_at": "2026-02-01",
      "changes_from_v2": ["increased_protein_target", "added_NAD+_supplement"]
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440502",
      "version": 2,
      "status": "archived",
      "created_at": "2025-12-01"
    }
  ]
}
```

---

### Compare Protocols

**GET** `/protocols/compare`

Compare two protocol versions side-by-side.

**Query Parameters:**
- `version_a` (required): Version number to compare from
- `version_b` (required): Version number to compare to

**Response (200 OK):**
```json
{
  "version_a": 2,
  "version_b": 3,
  "differences": {
    "nutrition_plan": {
      "protein_g": {"old": 100, "new": 120},
      "carbs_g": {"old": 180, "new": 200}
    },
    "supplements": {
      "added": ["NAD+_500mg"],
      "removed": [],
      "modified": []
    }
  }
}
```

---

### Approve Protocol

**POST** `/protocols/{protocol_id}/approve`

Approve a draft or pending protocol to make it active.

**Request Body:**
```json
{
  "notes": "Approved with minor modifications"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440503",
  "status": "active",
  "approved_at": "2026-03-27T10:30:00Z",
  "valid_from": "2026-03-27",
  "valid_until": "2026-06-27"
}
```

---

### Get Protocol Details

**GET** `/protocols/{protocol_id}`

Retrieve full details of a specific protocol version.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440500",
  "version": 3,
  "status": "active",
  ...
}
```

---

## Score Router (`/api/v1/score`)

### Get Longevity Score

**GET** `/score`

Retrieve comprehensive longevity metrics.

**Response (200 OK):**
```json
{
  "longevity_score": 72,
  "biological_age": 42.5,
  "chronological_age": 45.0,
  "age_delta": -2.5,
  "dunedin_pace": 0.95,
  "healthspan_forecast_years": 35.0,
  "mortality_risk_score": 18.5,
  "trend_30d": "improving",
  "projected_lifespan": 92.5
}
```

---

### Get Score Breakdown

**GET** `/score/breakdown`

Detailed breakdown of longevity score components.

**Response (200 OK):**
```json
{
  "overall_score": 72,
  "components": {
    "cardiovascular": {
      "weight": 0.25,
      "score": 78,
      "contribution": 19.5
    },
    "metabolic": {
      "weight": 0.20,
      "score": 65,
      "contribution": 13.0
    },
    "cognitive": {
      "weight": 0.15,
      "score": 82,
      "contribution": 12.3
    },
    ...
  }
}
```

---

### Get Score Forecast

**GET** `/score/forecast`

5-year longevity score projection based on adherence.

**Response (200 OK):**
```json
{
  "scenarios": [
    {
      "name": "Current trajectory (no changes)",
      "score_5yr": 65,
      "biological_age_5yr": 48.2
    },
    {
      "name": "With protocol adherence (90%)",
      "score_5yr": 82,
      "biological_age_5yr": 38.5
    },
    {
      "name": "With perfect adherence (100%)",
      "score_5yr": 88,
      "biological_age_5yr": 35.0
    }
  ]
}
```

---

### Get Score Trends

**GET** `/score/trends`

Historical score trends with analysis.

**Query Parameters:**
- `days` (default 365)
- `granularity` (default "daily"): "daily" | "weekly" | "monthly"

**Response (200 OK):**
```json
{
  "trend": "improving",
  "slope": 0.15,
  "slope_interpretation": "Score improving by 0.15 points per day",
  "data_points": [
    {"date": "2026-03-27", "score": 72},
    {"date": "2026-03-26", "score": 71.9},
    ...
  ],
  "significant_events": [
    {"date": "2026-02-15", "event": "started_protocol", "impact": +4}
  ]
}
```

---

### Get Leaderboard

**GET** `/score/leaderboard`

(Optional) Aggregate statistics across platform if multi-user.

**Response (200 OK):**
```json
{
  "your_rank": 42,
  "your_score": 72,
  "user_count": 1000,
  "percentile": 95,
  "average_score": 65,
  "top_scores": [
    {"rank": 1, "score": 96},
    {"rank": 2, "score": 94},
    ...
  ]
}
```

---

## Inventory Router (`/api/v1/inventory`)

### List Supplements

**GET** `/inventory`

Retrieve all supplements in user's inventory.

**Query Parameters:**
- `skip` (default 0)
- `limit` (default 100)
- `filter_active` (default true): Show only non-expired supplements

**Response (200 OK):**
```json
{
  "supplements": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440600",
      "name": "NAD+",
      "brand": "Tru Niagen",
      "dosage_per_unit": "250mg",
      "units_remaining": 60,
      "expiry_date": "2027-06-30",
      "auto_reorder": true,
      "status": "adequate_stock"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440601",
      "name": "Omega-3",
      "brand": "Nordic Naturals",
      "dosage_per_unit": "1000mg",
      "units_remaining": 12,
      "expiry_date": "2026-09-15",
      "auto_reorder": false,
      "status": "low_stock"
    }
  ],
  "total": 18
}
```

---

### Add Supplement

**POST** `/inventory`

Add a new supplement to inventory.

**Request Body:**
```json
{
  "name": "NAD+",
  "brand": "Tru Niagen",
  "dosage_per_unit": "250mg",
  "units_remaining": 60,
  "expiry_date": "2027-06-30",
  "auto_reorder": true
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440602",
  "name": "NAD+",
  "brand": "Tru Niagen",
  "dosage_per_unit": "250mg",
  "units_remaining": 60,
  "expiry_date": "2027-06-30",
  "auto_reorder": true,
  "created_at": "2026-03-27T10:30:00Z"
}
```

---

### Mark Supplement Consumed

**POST** `/inventory/consume`

Log supplement consumption.

**Request Body:**
```json
{
  "supplement_id": "550e8400-e29b-41d4-a716-446655440600",
  "units_consumed": 1,
  "date": "2026-03-27"
}
```

**Response (200 OK):**
```json
{
  "supplement_id": "550e8400-e29b-41d4-a716-446655440600",
  "units_remaining": 59,
  "status": "adequate_stock"
}
```

---

### Get Reorder List

**GET** `/inventory/reorder`

Get list of supplements needing reorder (low stock or expiring soon).

**Response (200 OK):**
```json
{
  "to_reorder": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440601",
      "name": "Omega-3",
      "reason": "low_stock",
      "units_remaining": 12,
      "recommended_quantity": 90
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440603",
      "name": "Magnesium Glycinate",
      "reason": "expiring_soon",
      "expiry_date": "2026-04-30",
      "days_until_expiry": 34
    }
  ]
}
```

---

### Get Expiry Alerts

**GET** `/inventory/expiry`

Get supplements expiring within 30 days.

**Response (200 OK):**
```json
{
  "expiring_soon": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440603",
      "name": "Magnesium Glycinate",
      "expiry_date": "2026-04-30",
      "days_until_expiry": 34,
      "units_remaining": 45
    }
  ]
}
```

---

### Delete Supplement

**DELETE** `/inventory/{supplement_id}`

Remove a supplement from inventory.

**Response (204 No Content)**

---

### Update Supplement

**PUT** `/inventory/{supplement_id}`

Update supplement details (units, expiry, auto-reorder).

**Request Body:**
```json
{
  "units_remaining": 55,
  "auto_reorder": false
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440600",
  "units_remaining": 55,
  "auto_reorder": false,
  "updated_at": "2026-03-27T10:30:00Z"
}
```

---

## WebSocket Endpoint

Real-time updates for agent pipeline progress and protocol notifications.

**URL**: `ws://localhost:8000/ws/v1/live`

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/v1/live');
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};
```

**Message Examples:**
```json
{
  "event": "pipeline_started",
  "session_id": "550e8400-e29b-41d4-a716-446655440200",
  "timestamp": "2026-03-27T10:30:00Z"
}

{
  "event": "tier_complete",
  "tier": 2,
  "agents_completed": 8,
  "duration_ms": 4500
}

{
  "event": "protocol_approved",
  "protocol_id": "550e8400-e29b-41d4-a716-446655440500",
  "contracts_generated": 30
}
```

---

## Rate Limiting

Default rate limits: **100 requests per minute per user**

Rate limit information in response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1711533060
```

If rate limit exceeded: **429 Too Many Requests**

---

## Pagination

All list endpoints support pagination with `skip` and `limit` parameters.

```bash
# Get 50 biomarkers, skip first 100
curl "http://localhost:8000/api/v1/data/biomarkers?skip=100&limit=50"
```

Response includes pagination metadata:
```json
{
  "items": [...],
  "total": 542,
  "skip": 100,
  "limit": 50
}
```

---

## Swagger/OpenAPI Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
