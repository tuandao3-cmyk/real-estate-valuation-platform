"""
api/services/audit_service.py

GOVERNANCE NOTICE
-----------------
This service records and assembles audit evidence.

STRICT CONSTRAINTS:
- No inference
- No decision
- No approval / rejection
- No runtime control logic
- No mutation of valuation artifacts

This service exists solely for auditability and legal traceability.
"""

from datetime import datetime
from typing import Dict, Any, Optional


class AuditService:
    """
    Audit evidence service (API layer).

    Purpose:
    - Record immutable audit events
    - Assemble audit evidence payloads
    - Preserve legal traceability for regulators, auditors, and courts

    This service is NOT part of valuation decision flow.
    """

    @staticmethod
    def record_event(
        event_type: str,
        reference_id: str,
        payload: Dict[str, Any],
        actor_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create an audit event record.

        Parameters:
        - event_type:
            Type of audit event (e.g. SNAPSHOT_CREATED, VALUATION_REQUESTED)
        - reference_id:
            ID of the related entity (snapshot_id, request_id, valuation_id)
        - payload:
            Read-only evidence payload
        - actor_id:
            Optional human actor identifier

        Returns:
        - Audit event dictionary (append-only, non-decisive)
        """

        audit_event: Dict[str, Any] = {
            "event_type": event_type,
            "reference_id": reference_id,
            "actor_id": actor_id,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload,
        }

        return audit_event

    @staticmethod
    def assemble_audit_bundle(
        *,
        snapshot_audit: Optional[Dict[str, Any]] = None,
        valuation_audit: Optional[Dict[str, Any]] = None,
        confidence_audit: Optional[Dict[str, Any]] = None,
        override_audit: Optional[Dict[str, Any]] = None,
        report_audit: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Assemble audit evidence bundle.

        Parameters:
        - snapshot_audit:
            Audit evidence related to feature snapshot
        - valuation_audit:
            Valuation execution trace
        - confidence_audit:
            Confidence generation trace
        - override_audit:
            Manual override evidence (if any)
        - report_audit:
            Report generation trace

        Returns:
        - Consolidated audit bundle (read-only)
        """

        audit_bundle: Dict[str, Any] = {
            "assembled_at": datetime.utcnow().isoformat(),
            "snapshot": snapshot_audit,
            "valuation": valuation_audit,
            "confidence": confidence_audit,
            "override": override_audit,
            "report": report_audit,
        }

        return audit_bundle
