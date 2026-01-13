"""
api/middleware/trust_guard.py

GOVERNANCE NOTICE
-----------------
This middleware enforces trust-based workflow gating ONLY.

STRICT CONSTRAINTS:
- Trust signal MUST come from valuation_dossier (SSOT)
- No trust computation
- No fraud judgment
- No valuation or approval decision
- Deterministic, policy-driven behavior only
"""

from typing import Callable, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.schemas.response.error_response import ErrorResponse


class TrustGuardMiddleware(BaseHTTPMiddleware):
    """
    Trust-based workflow gate.

    Responsibilities:
    - Read trust signal from request.state (SSOT-derived)
    - Apply static trust policy
    - Block request if trust is below allowed threshold

    NOT RESPONSIBLE FOR:
    - Trust score calculation
    - Risk band assignment
    - Approval or escalation routing
    """

    def __init__(
        self,
        app,
        minimum_trust_band: str = "LOW",
    ) -> None:
        super().__init__(app)
        self._minimum_trust_band = minimum_trust_band
        self._band_order = ["VERY_LOW", "LOW", "MEDIUM", "HIGH"]

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Enforce trust gating before request reaches service layer.
        """
        trust_context = self._extract_trust_context(request)

        if trust_context is None:
            return self._blocked_response(
                message="Missing trust context.",
                request=request,
            )

        trust_band = trust_context.get("trust_band")
        if trust_band is None:
            return self._blocked_response(
                message="Trust band not provided.",
                request=request,
            )

        if not self._is_trust_allowed(trust_band):
            return self._blocked_response(
                message=f"Trust level '{trust_band}' below minimum requirement.",
                request=request,
            )

        return await call_next(request)

    def _extract_trust_context(self, request: Request) -> Optional[dict]:
        """
        Extract trust context attached earlier in the pipeline.

        Expected source:
        - valuation_dossier.json
        - listing_intelligence trust projection

        NOTE:
        This middleware DOES NOT fetch files or compute trust.
        """
        return getattr(request.state, "trust_context", None)

    def _is_trust_allowed(self, trust_band: str) -> bool:
        """
        Compare trust band against static minimum threshold.

        Deterministic ordering:
        VERY_LOW < LOW < MEDIUM < HIGH
        """
        try:
            current_index = self._band_order.index(trust_band)
            minimum_index = self._band_order.index(self._minimum_trust_band)
        except ValueError:
            # Unknown trust band → fail fast
            return False

        return current_index >= minimum_index

    def _blocked_response(
        self,
        message: str,
        request: Request,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)

        error = ErrorResponse(
            error_code="TRUST_GUARD_BLOCKED",
            message=message,
            request_id=request_id,
        )

        return JSONResponse(
            status_code=403,
            content=error.model_dump(),
        )
