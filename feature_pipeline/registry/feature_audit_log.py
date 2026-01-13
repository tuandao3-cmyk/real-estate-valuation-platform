# ============================================================
# FEATURE AUDIT LOG
# File: feature_pipeline/registry/feature_audit_log.py
#
# Governance Level:
#   NHÓM A – Audit / Legal Evidence
#
# Role:
#   Immutable, append-only audit trail for feature lifecycle events
#
# MASTER_SPEC COMPLIANCE:
# - No feature mutation
# - No valuation logic
# - No decision authority
# ============================================================

from dataclasses import dataclass
from typing import List
import hashlib
import json
from datetime import datetime, timezone


class FeatureAuditViolation(Exception):
    """Raised when audit log governance is violated."""
    pass


@dataclass(frozen=True)
class FeatureAuditEvent:
    """
    Immutable audit event for feature governance.

    Governance:
    - Append-only
    - Read-only
    - Hashable
    """
    event_type: str                 # REGISTER_VERSION / DEPRECATE / OWNER_ASSIGN
    feature_id: str
    feature_version: str
    actor_id: str
    actor_role: str
    event_timestamp_utc: str
    event_comment: str | None = None


class FeatureAuditLog:
    """
    Append-only audit log for feature registry actions.

    ❌ Does NOT:
    - Modify feature definitions
    - Approve feature usage
    - Influence valuation

    ✅ Does:
    - Persist immutable audit events
    - Generate deterministic audit hashes
    """

    def __init__(self) -> None:
        self._events: List[FeatureAuditEvent] = []

    def append_event(self, event: FeatureAuditEvent) -> str:
        """
        Append a new audit event.

        Governance rules:
        - Events are immutable
        - No deletion
        - No overwrite
        """

        if not isinstance(event, FeatureAuditEvent):
            raise FeatureAuditViolation("Invalid audit event type")

        self._events.append(event)
        return self._generate_event_hash(event)

    def list_events(self) -> List[FeatureAuditEvent]:
        """
        Read-only snapshot of audit events.
        """
        return list(self._events)

    def _generate_event_hash(self, event: FeatureAuditEvent) -> str:
        """
        Deterministic SHA-256 hash for legal-grade audit evidence.
        """

        payload = {
            "event_type": event.event_type,
            "feature_id": event.feature_id,
            "feature_version": event.feature_version,
            "actor_id": event.actor_id,
            "actor_role": event.actor_role,
            "event_timestamp_utc": event.event_timestamp_utc,
            "event_comment": event.event_comment,
        }

        canonical_json = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )

        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


# ============================================================
# HELPER (OPTIONAL – GOVERNANCE SAFE)
# ============================================================

def utc_now_iso() -> str:
    """
    Generate UTC timestamp in ISO-8601 format.
    Deterministic format, no locale dependency.
    """
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# GOVERNANCE NOTE
#
# - FeatureAuditLog is evidence, not control logic
# - No audit event can alter system behavior
# - valuation_dossier.json remains SSOT
#
# END OF FILE
# ============================================================
