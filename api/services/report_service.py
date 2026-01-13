"""
api/services/report_service.py

GOVERNANCE NOTICE
-----------------
This service assembles valuation-related artifacts into a report payload.

STRICT CONSTRAINTS:
- No valuation logic
- No inference
- No interpretation
- No approval / rejection hint
- No modification of underlying artifacts

This service is a read-only report assembler.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from api.schemas.common.metadata import Metadata


class ReportService:
    """
    Report assembly service (API layer).

    Purpose:
    - Aggregate immutable valuation artifacts
    - Produce a structured, audit-ready report payload
    - Preserve neutrality and non-decisive positioning

    This service assumes:
    - All inputs are precomputed, immutable artifacts
    - No artifact is modified or interpreted here
    """

    @staticmethod
    def build_report(
        valuation_payload: Dict[str, Any],
        confidence_payload: Optional[Dict[str, Any]],
        explainability_payload: Optional[Dict[str, Any]],
        metadata: Metadata,
    ) -> Dict[str, Any]:
        """
        Assemble valuation report payload.

        Parameters:
        - valuation_payload:
            Read-only valuation result (ensemble output)
        - confidence_payload:
            Optional confidence artifact (descriptive only)
        - explainability_payload:
            Optional explainability artifact (narrative / breakdown)
        - metadata:
            Request, actor, and trace metadata

        Returns:
        - Report payload dictionary (non-decisive, audit-safe)
        """

        report: Dict[str, Any] = {
            "report_generated_at": datetime.utcnow().isoformat(),
            "valuation": valuation_payload,
            "confidence": confidence_payload,
            "explainability": explainability_payload,
            "metadata": metadata,
        }

        return report
