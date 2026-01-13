"""
approval_required.py

ROLE (STRICT):
- Workflow routing ONLY
- Determine whether human approval is REQUIRED
- Non-computational, deterministic, audit-safe

ABSOLUTE CONSTRAINTS:
- Read-only access to valuation_dossier.json
- Must NOT compute confidence, risk, or price
- Must NOT modify or persist any artifact
- Must NOT invoke ML / LLM
- valuation_dossier.json is the single source of truth

MASTER_SPEC COMPLIANCE:
- Confidence is a gate, not a metric
- Risk band controls workflow routing
- Humans remain accountable
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List


# =========================
# ENUMS & DATA CONTRACTS
# =========================

class ApprovalRequirement(Enum):
    """
    Canonical workflow routing outcomes.
    """
    AUTO_ALLOWED = "AUTO_ALLOWED"          # Allowed to proceed, still logged elsewhere
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    WORKFLOW_BLOCKED = "WORKFLOW_BLOCKED"  # Structural / integrity issue


@dataclass(frozen=True)
class ApprovalDecision:
    """
    Output of this module.
    This is NOT a valuation decision.
    """
    requirement: ApprovalRequirement
    reasons: List[str]              # Canonical reason codes
    valuation_hash: str             # For audit trace
    policy_version: str             # confidence/risk policy version


# =========================
# CORE FUNCTION
# =========================

def determine_approval_requirement(
    valuation_dossier: Dict[str, Any],
    confidence_policy: Dict[str, Any],
    risk_policy: Dict[str, Any],
) -> ApprovalDecision:
    """
    Determine whether human approval is mandatory.

    INPUTS (READ-ONLY):
    - valuation_dossier.json (mandatory, canonical)
    - confidence_threshold.yaml (static policy)
    - risk_band_rules.yaml (static policy)

    OUTPUT:
    - ApprovalDecision (workflow routing only)

    FAILURE MODE:
    - Any missing / malformed critical field => HUMAN_APPROVAL_REQUIRED
    """

    reasons: List[str] = []

    # -------------------------
    # 1. HARD VALIDATION
    # -------------------------
    if not valuation_dossier:
        return ApprovalDecision(
            requirement=ApprovalRequirement.WORKFLOW_BLOCKED,
            reasons=["MISSING_VALUATION_DOSSIER"],
            valuation_hash="UNKNOWN",
            policy_version=_policy_version(confidence_policy, risk_policy),
        )

    valuation_hash = valuation_dossier.get("valuation_hash")
    if not valuation_hash:
        return ApprovalDecision(
            requirement=ApprovalRequirement.WORKFLOW_BLOCKED,
            reasons=["MISSING_VALUATION_HASH"],
            valuation_hash="UNKNOWN",
            policy_version=_policy_version(confidence_policy, risk_policy),
        )

    # -------------------------
    # 2. READ CONFIDENCE (NO COMPUTATION)
    # -------------------------
    confidence_score = valuation_dossier.get("confidence_score")
    if confidence_score is None:
        reasons.append("CONFIDENCE_MISSING")
    else:
        min_auto_conf = confidence_policy.get("min_confidence_for_auto")
        if min_auto_conf is None:
            reasons.append("CONFIDENCE_POLICY_INVALID")
        elif confidence_score < min_auto_conf:
            reasons.append("LOW_CONFIDENCE")

    # -------------------------
    # 3. READ RISK BAND (NO COMPUTATION)
    # -------------------------
    risk_band = valuation_dossier.get("risk_band")
    if not risk_band:
        reasons.append("RISK_BAND_MISSING")
    else:
        blocked_bands = risk_policy.get("require_human_approval", [])
        if risk_band in blocked_bands:
            reasons.append(f"RISK_BAND_{risk_band}")

    # -------------------------
    # 4. FINAL ROUTING LOGIC
    # -------------------------
    if reasons:
        return ApprovalDecision(
            requirement=ApprovalRequirement.HUMAN_APPROVAL_REQUIRED,
            reasons=sorted(set(reasons)),
            valuation_hash=valuation_hash,
            policy_version=_policy_version(confidence_policy, risk_policy),
        )

    return ApprovalDecision(
        requirement=ApprovalRequirement.AUTO_ALLOWED,
        reasons=["AUTO_CRITERIA_SATISFIED"],
        valuation_hash=valuation_hash,
        policy_version=_policy_version(confidence_policy, risk_policy),
    )


# =========================
# INTERNAL UTILITIES
# =========================

def _policy_version(confidence_policy: Dict[str, Any], risk_policy: Dict[str, Any]) -> str:
    """
    Combine policy versions for audit trace.
    """
    return (
        f"confidence={confidence_policy.get('version', 'UNKNOWN')};"
        f"risk={risk_policy.get('version', 'UNKNOWN')}"
    )
