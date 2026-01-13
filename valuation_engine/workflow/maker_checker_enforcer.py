"""
maker_checker_enforcer.py

ROLE (STRICT):
- Enforce maker–checker separation
- Validate human authority in approval workflow
- Append-only verification (read-only on artifacts)

ABSOLUTE CONSTRAINTS:
- MUST NOT create valuation decisions
- MUST NOT modify valuation_dossier or decision_result
- MUST NOT compute price / confidence / risk
- MUST NOT invoke ML / LLM
- MUST NOT auto-approve anything

LEGAL POSITION:
- This module enforces HUMAN accountability
- Absence or violation = NON-COMPLIANT WORKFLOW

MASTER_SPEC.md OVERRIDES ALL
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List, Optional


# =========================
# ENUMS & DATA CONTRACTS
# =========================

class EnforcementResult(Enum):
    """
    Canonical enforcement outcomes.
    """
    ENFORCED_OK = "ENFORCED_OK"
    ENFORCEMENT_FAILED = "ENFORCEMENT_FAILED"


@dataclass(frozen=True)
class EnforcementDecision:
    """
    Output of maker-checker enforcement.
    This is NOT a business decision.
    """
    result: EnforcementResult
    reasons: List[str]
    valuation_hash: str
    approval_hash: Optional[str]


# =========================
# CORE FUNCTION
# =========================

def enforce_maker_checker(
    valuation_dossier: Dict[str, Any],
    approval_log: Dict[str, Any],
) -> EnforcementDecision:
    """
    Enforce maker–checker separation and human authority.

    INPUTS (READ-ONLY):
    - valuation_dossier.json (mandatory)
    - approval_log.json (mandatory, append-only)

    OUTPUT:
    - EnforcementDecision (workflow gate)

    FAILURE MODE:
    - Any violation => ENFORCEMENT_FAILED
    """

    reasons: List[str] = []

    # -------------------------
    # 1. HARD VALIDATION
    # -------------------------
    if not valuation_dossier:
        return _fail(
            ["MISSING_VALUATION_DOSSIER"],
            valuation_hash="UNKNOWN",
            approval_hash=None,
        )

    valuation_hash = valuation_dossier.get("valuation_hash")
    if not valuation_hash:
        return _fail(
            ["MISSING_VALUATION_HASH"],
            valuation_hash="UNKNOWN",
            approval_hash=None,
        )

    if not approval_log:
        return _fail(
            ["MISSING_APPROVAL_LOG"],
            valuation_hash=valuation_hash,
            approval_hash=None,
        )

    approval_hash = approval_log.get("approval_hash")
    if not approval_hash:
        reasons.append("MISSING_APPROVAL_HASH")

    # -------------------------
    # 2. HUMAN SIGNATURE CHECK
    # -------------------------
    maker = approval_log.get("maker")
    checker = approval_log.get("checker")

    if not maker:
        reasons.append("MISSING_MAKER")
    if not checker:
        reasons.append("MISSING_CHECKER")

    if maker and checker and maker == checker:
        reasons.append("MAKER_CHECKER_SAME_PERSON")

    # -------------------------
    # 3. ROLE VALIDATION
    # -------------------------
    if maker and not _is_human_actor(maker):
        reasons.append("MAKER_NOT_HUMAN")

    if checker and not _is_human_actor(checker):
        reasons.append("CHECKER_NOT_HUMAN")

    # -------------------------
    # 4. DECISION ATTESTATION
    # -------------------------
    decision = approval_log.get("decision")
    if decision not in {"APPROVED", "REJECTED"}:
        reasons.append("INVALID_OR_MISSING_DECISION")

    timestamp = approval_log.get("timestamp")
    if not timestamp:
        reasons.append("MISSING_APPROVAL_TIMESTAMP")

    # -------------------------
    # 5. FINAL ENFORCEMENT
    # -------------------------
    if reasons:
        return _fail(
            reasons=reasons,
            valuation_hash=valuation_hash,
            approval_hash=approval_hash,
        )

    return EnforcementDecision(
        result=EnforcementResult.ENFORCED_OK,
        reasons=["MAKER_CHECKER_ENFORCED"],
        valuation_hash=valuation_hash,
        approval_hash=approval_hash,
    )


# =========================
# INTERNAL UTILITIES
# =========================

def _is_human_actor(actor: Dict[str, Any]) -> bool:
    """
    Validate that the actor is a human authority.
    System / AI / Rule engines are forbidden.
    """
    return (
        actor.get("type") == "HUMAN"
        and actor.get("id") is not None
        and actor.get("role") in {"APPRAISER", "CREDIT_OFFICER", "MANAGER"}
    )


def _fail(
    reasons: List[str],
    valuation_hash: str,
    approval_hash: Optional[str],
) -> EnforcementDecision:
    """
    Canonical failure constructor.
    """
    return EnforcementDecision(
        result=EnforcementResult.ENFORCEMENT_FAILED,
        reasons=sorted(set(reasons)),
        valuation_hash=valuation_hash,
        approval_hash=approval_hash,
    )
