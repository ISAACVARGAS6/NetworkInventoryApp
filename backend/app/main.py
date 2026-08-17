from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes_scan import router as scan_router
from app.api.routes_devices import router as devices_router
from app.api.routes_inventory import router as inventory_router

from app.core.database import Base
from app.core.database import engine
from app.core.database import SessionLocal

import app.models


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Network Inventory API",
    description=(
        "REST API for network discovery, "
        "device inventory and service analysis."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    scan_router,
    prefix="/api",
)

app.include_router(
    devices_router,
    prefix="/api",
)

app.include_router(
    inventory_router,
    prefix="/api",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    """Return basic API information."""

    return {
        "application": "Network Inventory API",
        "version": "1.0.0",
        "status": "online",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    """Check that the API and its persistence layer are available."""

    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        return {
            "status": "unhealthy",
            "database": "unavailable",
        }

    return {
        "status": "healthy",
        "database": "available",
    }
