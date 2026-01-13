"""
api/routers/health_router.py

GOVERNANCE NOTICE
-----------------
This router exposes system health endpoints for infrastructure monitoring.

STRICT CONSTRAINTS:
- No business logic
- No model or data inspection
- No risk or confidence signaling
- Deterministic responses only
"""

from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/live",
    summary="Liveness check",
    description="Confirms that the API process is running.",
)
async def liveness_check() -> dict:
    """
    Liveness probe.

    Purpose:
    - Used by orchestrators (Docker / Kubernetes)
    - Confirms the process is alive

    No dependency checks are performed.
    """
    return {
        "status": "alive",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }


@router.get(
    "/ready",
    summary="Readiness check",
    description="Confirms that the API is ready to receive traffic.",
)
async def readiness_check() -> dict:
    """
    Readiness probe.

    Purpose:
    - Used by load balancers / orchestrators
    - Confirms the service can accept requests

    NOTE:
    This endpoint does NOT validate:
    - Models
    - Data freshness
    - External service integrity
    """
    return {
        "status": "ready",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
