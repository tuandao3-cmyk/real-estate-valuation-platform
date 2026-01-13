"""
api/middleware/auth.py

GOVERNANCE NOTICE
-----------------
This middleware performs request authentication ONLY.

STRICT CONSTRAINTS:
- Authentication ≠ authorization
- No role interpretation
- No permission decision
- No workflow routing
- No silent fallback

If authentication fails, the request is rejected immediately.
"""

from typing import Callable, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.schemas.response.error_response import ErrorResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware.

    Responsibilities:
    - Extract authentication token
    - Perform token validation (structural / cryptographic)
    - Attach authenticated principal metadata to request.state

    NOT RESPONSIBLE FOR:
    - Role-based authorization
    - Approval logic
    - Risk evaluation
    """

    def __init__(
        self,
        app,
        token_header: str = "Authorization",
        token_prefix: str = "Bearer",
    ) -> None:
        super().__init__(app)
        self._token_header = token_header
        self._token_prefix = token_prefix

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        auth_header = request.headers.get(self._token_header)

        if not auth_header:
            return self._unauthorized_response(
                message="Missing authentication header.",
                request=request,
            )

        token = self._extract_token(auth_header)
        if not token:
            return self._unauthorized_response(
                message="Invalid authentication header format.",
                request=request,
            )

        principal = self._validate_token(token)
        if principal is None:
            return self._unauthorized_response(
                message="Invalid or expired authentication token.",
                request=request,
            )

        # Attach authenticated principal to request state
        request.state.principal = principal

        return await call_next(request)

    def _extract_token(self, header_value: str) -> Optional[str]:
        """
        Extract raw token from Authorization header.

        Expected format:
            Authorization: Bearer <token>
        """
        parts = header_value.split()
        if len(parts) != 2:
            return None

        prefix, token = parts
        if prefix != self._token_prefix:
            return None

        return token.strip()

    def _validate_token(self, token: str) -> Optional[dict]:
        """
        Validate authentication token.

        IMPORTANT:
        - This method MUST remain deterministic.
        - No external inference.
        - No role or permission resolution.

        Placeholder implementation:
        Replace with cryptographic validation (JWT, HMAC, mTLS, etc.)
        """
        # --- GOVERNANCE PLACEHOLDER ---
        # Example: token must be non-empty and non-whitespace
        if not token or not token.strip():
            return None

        # Minimal authenticated principal metadata
        return {
            "auth_type": "bearer",
            "token_hash": hash(token),
        }

    def _unauthorized_response(
        self,
        message: str,
        request: Request,
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)

        error = ErrorResponse(
            error_code="UNAUTHORIZED",
            message=message,
            request_id=request_id,
        )

        return JSONResponse(
            status_code=401,
            content=error.model_dump(),
        )
