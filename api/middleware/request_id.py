"""
api/middleware/request_id.py

GOVERNANCE NOTICE
-----------------
This middleware guarantees the presence of a unique request_id
for every incoming HTTP request.

STRICT CONSTRAINTS:
- No business logic
- No mutation of request payload
- No valuation / model dependency
- request_id is immutable once set
"""

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to attach a unique request_id to each request.

    Purpose:
    - Ensure traceability across API, services, audit logs
    - Support replay, debugging, and legal inspection
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """
        Attach request_id to request.state and response headers.

        Priority:
        - Respect existing X-Request-ID if provided
        - Otherwise generate a new UUID4
        """

        incoming_request_id = request.headers.get(REQUEST_ID_HEADER)

        request_id = incoming_request_id or str(uuid.uuid4())

        # Attach to request state for downstream usage
        request.state.request_id = request_id

        response: Response = await call_next(request)

        # Echo request_id back to client for traceability
        response.headers[REQUEST_ID_HEADER] = request_id

        return response
