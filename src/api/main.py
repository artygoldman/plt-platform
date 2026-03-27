"""FastAPI application for Personal Longevity Team Platform."""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, WebSocketDisconnect, WebSocketException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket

from src.api.routers import agents, contracts, data, inventory, protocols, score, twin, users
from src.db.base import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events.

    Creates database tables on startup.
    """
    # Startup
    await init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down")


# Initialize FastAPI app
app = FastAPI(
    title="Personal Longevity Team API",
    version="0.1.0",
    description="API for the Personal Longevity Team platform",
    lifespan=lifespan,
)

# Add CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Status, version, and timestamp
    """
    return {
        "status": "ok",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


# WebSocket endpoint placeholder
@app.websocket("/ws/v1/live")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates.

    TODO: Implement real-time streaming in Phase 4.

    Args:
        websocket: WebSocket connection
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except WebSocketException as e:
        print(f"WebSocket error: {e}")


# Include routers with /api/v1 prefix
app.include_router(users.router, prefix="/api/v1")
app.include_router(data.router, prefix="/api/v1")
app.include_router(twin.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(contracts.router, prefix="/api/v1")
app.include_router(protocols.router, prefix="/api/v1")
app.include_router(score.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
