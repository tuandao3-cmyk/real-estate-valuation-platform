# Module: valuation_engine/workflow/escalation_policy.py
# Part of Advanced AVM System

"""
valuation_engine/workflow/escalation_policy.py

Tuân thủ MASTER_SPEC.md & IMPLEMENTATION STATUS
Role: Escalation Routing Policy (Workflow-only, Non-computational)

- READ-ONLY
- DETERMINISTIC
- NO SIDE EFFECTS
- NO ML / LLM
- NO FILE IO
- NO MUTATION
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# =========================
# Canonical enums / codes
# =========================

ESCALATION_LEVEL_SENIOR_APPRAISER = "SENIOR_APPRAISER"
ESCALATION_LEVEL_CREDIT_COMMITTEE = "CREDIT_COMMITTEE"
ESCALATION_LEVEL_RISK_COMMITTEE = "RISK_COMMITTEE"

REASON_LOW_CONFIDENCE = "LOW_CONFIDENCE"
REASON_MEDIUM_HIGH_RISK = "MEDIUM_HIGH_RISK"
REASON_SPECIAL_FLAG = "SPECIAL_FLAG"
REASON_MISSING_INFORMATION = "MISSING_INFORMATION"
REASON_GOVERNANCE_FAILSAFE = "GOVERNANCE_FAILSAFE"


# =========================
# Output schema (workflow-only)
# =========================

@dataclass(frozen=True)
class EscalationDecision:
    escalation_required: bool
    escalation_level: Optional[str]
    reasons: Tuple[str, ...]
    valuation_hash: str
    policy_version: str


# =========================
# Helpers (pure, read-only)
# =========================

def _get_required_fields(dossier: Dict[str, Any]) -> List[str]:
    """Fields that MUST exist for safe routing (no computation)."""
    return [
        "valuation_hash",
        "risk_band",
        "confidence_score",
    ]


def _missing_fields(dossier: Dict[str, Any]) -> List[str]:
    required = _get_required_fields(dossier)
    return [f for f in required if f not in dossier]


def _has_special_flags(dossier: Dict[str, Any]) -> bool:
    flags = dossier.get("special_flags")
    return isinstance(flags, (list, tuple)) and len(flags) > 0


def _is_low_confidence(dossier: Dict[str, Any]) -> bool:
    """
    NON-COMPUTATIONAL:
    confidence_score is read-only and already evaluated upstream.
    Here we only check canonical banding by value presence.
    """
    # Expected upstream normalization:
    # confidence_score in {"LOW","MEDIUM","HIGH"} or numeric already mapped.
    return dossier.get("confidence_score") == "LOW"


def _is_medium_or_high_risk(dossier: Dict[str, Any]) -> bool:
    return dossier.get("risk_band") in ("MEDIUM", "HIGH")


def _determine_level(reasons: List[str]) -> str:
    """
    Deterministic escalation level mapping.
    Fail-safe: highest governance level wins.
    """
    if REASON_SPECIAL_FLAG in reasons or REASON_GOVERNANCE_FAILSAFE in reasons:
        return ESCALATION_LEVEL_RISK_COMMITTEE
    if REASON_MEDIUM_HIGH_RISK in reasons:
        return ESCALATION_LEVEL_CREDIT_COMMITTEE
    return ESCALATION_LEVEL_SENIOR_APPRAISER


# =========================
# Core API (pure function)
# =========================

def evaluate_escalation(
    valuation_dossier: Dict[str, Any],
    decision_result: Optional[Dict[str, Any]] = None,
    approval_log: Optional[Dict[str, Any]] = None,
    *,
    policy_version: str = "escalation_policy@1.0.0",
) -> EscalationDecision:
    """
    Evaluate escalation routing WITHOUT computing risk/confidence.

    Inputs:
      - valuation_dossier (MANDATORY, read-only)
      - decision_result (OPTIONAL, read-only)
      - approval_log (OPTIONAL, read-only)

    Output:
      - EscalationDecision (workflow-only)
    """

    # ---- Mandatory source of truth ----
    if not isinstance(valuation_dossier, dict):
        # Governance fail-safe: escalate highest
        return EscalationDecision(
            escalation_required=True,
            escalation_level=ESCALATION_LEVEL_RISK_COMMITTEE,
            reasons=(REASON_GOVERNANCE_FAILSAFE,),
            valuation_hash="UNKNOWN",
            policy_version=policy_version,
        )

    valuation_hash = valuation_dossier.get("valuation_hash", "UNKNOWN")

    reasons: List[str] = []

    # ---- Missing info => mandatory escalation (fail-safe) ----
    missing = _missing_fields(valuation_dossier)
    if missing:
        reasons.append(REASON_MISSING_INFORMATION)

    # ---- Routing by read-only signals (no computation) ----
    if _is_low_confidence(valuation_dossier):
        reasons.append(REASON_LOW_CONFIDENCE)

    if _is_medium_or_high_risk(valuation_dossier):
        reasons.append(REASON_MEDIUM_HIGH_RISK)

    if _has_special_flags(valuation_dossier):
        reasons.append(REASON_SPECIAL_FLAG)

    # ---- Final decision ----
    if reasons:
        level = _determine_level(reasons)
        return EscalationDecision(
            escalation_required=True,
            escalation_level=level,
            reasons=tuple(dict.fromkeys(reasons)),  # stable de-dup
            valuation_hash=valuation_hash,
            policy_version=policy_version,
        )

    # ---- No escalation required ----
    return EscalationDecision(
        escalation_required=False,
        escalation_level=None,
        reasons=tuple(),
        valuation_hash=valuation_hash,
        policy_version=policy_version,
    )
