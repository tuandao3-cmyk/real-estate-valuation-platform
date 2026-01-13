"""
api/middleware/error_handler.py

GOVERNANCE NOTICE
-----------------
This middleware standardizes error handling for API requests.

STRICT CONSTRAINTS:
- No business logic
- No retry / bypass
- No interpretation or severity judgment
- No mutation of request data
- Preserve error transparency for auditability
"""

from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.schemas.response.error_response import ErrorResponse


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global API error handling middleware.

    Purpose:
    - Catch unhandled exceptions
    - Normalize error response schema
    - Preserve request_id for traceability

    This middleware does NOT decide how the system should react.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        try:
            response = await call_next(request)
            return response

        except Exception as exc:  # noqa: BLE001
            request_id = getattr(request.state, "request_id", None)

            error_payload = ErrorResponse(
                error_code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred.",
                request_id=request_id,
            )

            return JSONResponse(
                status_code=500,
                content=error_payload.model_dump(),
            )
