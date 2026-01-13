"""
api/services/valuation_service.py

GOVERNANCE NOTICE
-----------------
This service orchestrates the valuation workflow at API level.

STRICT CONSTRAINTS:
- No valuation logic
- No model execution
- No rule enforcement
- No approval or rejection
- No interpretation of outputs

This file is an orchestration boundary only.
"""

from datetime import datetime
from typing import Dict, Any

from api.schemas.request.valuation_request import ValuationRequest
from api.schemas.response.valuation_response import ValuationResponse
from api.schemas.common.metadata import Metadata


class ValuationService:
    """
    Valuation orchestration service (API layer).

    Purpose:
    - Bind valuation request with existing valuation artifacts
    - Attach metadata & audit context
    - Expose valuation output in a schema-controlled form

    This service assumes:
    - Snapshot already exists
    - Models already executed upstream
    - Outputs are read-only
    """

    @staticmethod
    def build_valuation_response(
        request: ValuationRequest,
        valuation_payload: Dict[str, Any],
        metadata: Metadata,
    ) -> ValuationResponse:
        """
        Build valuation API response.

        Parameters:
        - request:
            Original valuation request (schema-validated)
        - valuation_payload:
            Read-only valuation output produced by valuation engine / ensemble
        - metadata:
            Request / actor / trace metadata

        Returns:
        - ValuationResponse (non-decisive, audit-safe)
        """

        response = ValuationResponse(
            valuation=valuation_payload,
            valuation_request_id=request.request_id,
            generated_at=datetime.utcnow().isoformat(),
            metadata=metadata,
        )

        return response
