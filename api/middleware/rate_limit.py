"""
api/middleware/rate_limit.py

GOVERNANCE NOTICE
-----------------
This middleware enforces a simple, deterministic rate limit.

STRICT CONSTRAINTS:
- Infrastructure protection only
- No behavioral inference
- No trust or risk adjustment
- No business logic
"""

import time
from typing import Callable, Dict, Tuple

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.schemas.response.error_response import ErrorResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware.

    Characteristics:
    - Fixed window
    - Deterministic behavior
    - Per-client isolation
    - Non-persistent (process-local)

    NOT responsible for:
    - Abuse classification
    - Penalty escalation
    - Account suspension
    """

    def __init__(
        self,
        app,
        max_requests: int = 100,
        window_seconds: int = 60,
    ) -> None:
        super().__init__(app)
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._requests: Dict[str, Tuple[int, float]] = {}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        client_key = self._get_client_key(request)
        now = time.time()

        count, window_start = self._requests.get(client_key, (0, now))

        if now - window_start >= self._window_seconds:
            # Reset window
            count = 0
            window_start = now

        count += 1
        self._requests[client_key] = (count, window_start)

        if count > self._max_requests:
            return self._rate_limited_response(request)

        return await call_next(request)

    def _get_client_key(self, request: Request) -> str:
        """
        Resolve a technical client identifier.

        Priority:
        1. X-Client-Id header (if provided)
        2. Client IP address

        NOTE:
        Identifier is used ONLY for rate limiting.
        """
        client_id = request.headers.get("X-Client-Id")
        if client_id:
            return client_id

        if request.client:
            return request.client.host

        return "unknown"

    def _rate_limited_response(self, request: Request) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)

        error = ErrorResponse(
            error_code="RATE_LIMIT_EXCEEDED",
            message="Too many requests in a short period.",
            request_id=request_id,
        )

        return JSONResponse(
            status_code=429,
            content=error.model_dump(),
        )
