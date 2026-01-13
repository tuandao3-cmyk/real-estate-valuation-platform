"""
api/services/confidence_service.py

GOVERNANCE NOTICE
-----------------
This service exposes confidence-related information produced by
upstream ensemble components.

STRICT CONSTRAINTS:
- No model inference
- No recalculation of confidence
- No thresholding or interpretation
- No approval / rejection logic

Confidence is descriptive metadata ONLY.
"""

from datetime import datetime
from typing import Dict, Any

from api.schemas.response.confidence_response import ConfidenceResponse
from api.schemas.common.metadata import Metadata


class ConfidenceService:
    """
    Confidence service – descriptive layer only.

    Purpose:
    - Normalize confidence signal output
    - Attach metadata & audit context
    - Guarantee no decision leakage

    This service does NOT:
    - Judge reliability
    - Compare against thresholds
    - Trigger workflow actions
    """

    @staticmethod
    def build_confidence_response(
        confidence_payload: Dict[str, Any],
        metadata: Metadata,
    ) -> ConfidenceResponse:
        """
        Build confidence API response.

        Parameters:
        - confidence_payload:
            Output from ensemble confidence_estimator
            (already computed, read-only)
        - metadata:
            Request / actor / trace metadata

        Returns:
        - ConfidenceResponse (schema-controlled)
        """

        response = ConfidenceResponse(
            confidence=confidence_payload,
            generated_at=datetime.utcnow().isoformat(),
            metadata=metadata,
        )

        return response
