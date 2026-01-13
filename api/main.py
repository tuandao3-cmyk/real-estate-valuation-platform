"""
api/main.py

SYSTEM ENTRYPOINT – GOVERNANCE LOCKED
------------------------------------
This file bootstraps the API application.

STRICT CONSTRAINTS:
- No business logic
- No valuation logic
- No decision making
- Router & middleware wiring only
"""

from fastapi import FastAPI

from api.middleware.request_id import RequestIDMiddleware
from api.middleware.error_handler import ErrorHandlerMiddleware
from api.middleware.auth import AuthMiddleware
from api.middleware.trust_guard import TrustGuardMiddleware
from api.middleware.rate_limit import RateLimitMiddleware

from api.routers.health_router import router as health_router
from api.routers.snapshot_router import router as snapshot_router
from api.routers.valuation_router import router as valuation_router
from api.routers.report_router import router as report_router
from api.routers.admin_router import router as admin_router


def create_app() -> FastAPI:
    """
    Application factory.

    Purpose:
    - Deterministic app construction
    - Testability
    - Governance isolation

    NOTE:
    This function MUST remain side-effect free.
    """
    app = FastAPI(
        title="Advanced AVM API",
        description=(
            "AI-assisted real estate valuation platform API. "
            "This system assists valuation professionals; "
            "humans remain fully accountable."
        ),
        version="1.0.0",
    )

    # ------------------------------------------------------------------
    # Middleware (ORDER MATTERS – DO NOT REARRANGE WITHOUT GOVERNANCE)
    # ------------------------------------------------------------------

    # 1. Request identity & traceability
    app.add_middleware(RequestIDMiddleware)

    # 2. Authentication / authorization
    app.add_middleware(AuthMiddleware)

    # 3. Trust & fraud pre-screening (non-decisive)
    app.add_middleware(TrustGuardMiddleware)

    # 4. Rate limiting (operational safety)
    app.add_middleware(RateLimitMiddleware)

    # 5. Unified error handling (last in chain)
    app.add_middleware(ErrorHandlerMiddleware)

    # ------------------------------------------------------------------
    # Routers (READ-ONLY / WORKFLOW-SAFE)
    # ------------------------------------------------------------------

    app.include_router(health_router)
    app.include_router(snapshot_router)
    app.include_router(valuation_router)
    app.include_router(report_router)
    app.include_router(admin_router)

    return app


# ASGI entrypoint
app = create_app()
