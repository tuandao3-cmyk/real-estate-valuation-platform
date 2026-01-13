# Module: valuation_engine/override/override_request.py
# Part of Advanced AVM System

# valuation_engine/override/override_request.py
# 🚫 DO NOT MODIFY WITHOUT GOVERNANCE APPROVAL
#
# Role: Human Override Request Registrar (Workflow-only, Read-only)
# Risk: NHÓM A – Human Authority / Legal & Audit Control
#
# This module ONLY validates and records an override REQUEST
# made by a human actor. It does NOT approve, evaluate, or
# apply the override.
#
# valuation_dossier.json remains the Single Source of Truth.

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime, timezone


# -----------------------------
# Canonical Data Structures
# -----------------------------

@dataclass(frozen=True)
class OverrideRequest:
    """
    Canonical representation of a human override request.

    This object is a FACT RECORD, not a decision.
    """
    valuation_hash: str
    actor_id: str
    actor_role: str
    override_reason_code: str
    requested_at_utc: str
    comment: Optional[str] = None
    evidence_refs: Optional[Dict[str, str]] = None


# -----------------------------
# Validation Layer (Static)
# -----------------------------

class OverrideRequestValidationError(Exception):
    """Raised when an override request violates governance rules."""
    pass


def validate_override_request(
    *,
    valuation_dossier: Dict[str, Any],
    override_reason_codes: Dict[str, Any],
    actor_id: str,
    actor_role: str,
    override_reason_code: str,
) -> None:
    """
    Perform GOVERNANCE-ONLY validation for an override request.

    ❌ Does NOT approve override
    ❌ Does NOT evaluate business impact
    ❌ Does NOT modify any artifact
    """

    # ---- Single Source of Truth check ----
    if "valuation_hash" not in valuation_dossier:
        raise OverrideRequestValidationError(
            "valuation_dossier missing valuation_hash"
        )

    # ---- Reason code existence ----
    if override_reason_code not in override_reason_codes:
        raise OverrideRequestValidationError(
            f"Unknown override_reason_code: {override_reason_code}"
        )

    # ---- Role authorization check ----
    allowed_roles = override_reason_codes[override_reason_code].get(
        "allowed_roles", []
    )
    if actor_role not in allowed_roles:
        raise OverrideRequestValidationError(
            f"Actor role '{actor_role}' not authorized for reason code '{override_reason_code}'"
        )

    # ---- Explicit prohibition: AI / System ----
    if actor_role.upper() in {"AI", "SYSTEM", "RULE_ENGINE", "LLM"}:
        raise OverrideRequestValidationError(
            "Non-human actors are forbidden from requesting overrides"
        )


# -----------------------------
# Factory Function
# -----------------------------

def create_override_request(
    *,
    valuation_dossier: Dict[str, Any],
    override_reason_codes: Dict[str, Any],
    actor_id: str,
    actor_role: str,
    override_reason_code: str,
    comment: Optional[str] = None,
    evidence_refs: Optional[Dict[str, str]] = None,
) -> OverrideRequest:
    """
    Create a validated OverrideRequest record.

    This function:
    - VALIDATES governance constraints
    - CREATES an immutable request object

    It does NOT:
    - Apply override
    - Change workflow
    - Log approval
    - Decide acceptance
    """

    validate_override_request(
        valuation_dossier=valuation_dossier,
        override_reason_codes=override_reason_codes,
        actor_id=actor_id,
        actor_role=actor_role,
        override_reason_code=override_reason_code,
    )

    return OverrideRequest(
        valuation_hash=valuation_dossier["valuation_hash"],
        actor_id=actor_id,
        actor_role=actor_role,
        override_reason_code=override_reason_code,
        requested_at_utc=datetime.now(timezone.utc).isoformat(),
        comment=comment,
        evidence_refs=evidence_refs,
    )


# -----------------------------
# Governance Guarantees
# -----------------------------
#
# ✔ Read-only access to valuation_dossier
# ✔ Deterministic structure
# ✔ No side effects
# ✔ No decision authority
# ✔ Audit-ready
#
# Any application of override MUST be handled
# downstream by approval_log, maker-checker,
# and valuation_flow enforcement.
#
# 🛑 END OF override_request.py
