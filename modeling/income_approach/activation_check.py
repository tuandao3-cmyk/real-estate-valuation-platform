"""
Income Approach Activation Check
--------------------------------

GOVERNANCE ROLE:
- Permission gate ONLY
- Determines whether Income Approach is ALLOWED to run
- Does NOT compute income, yield, cap rate, or value
- Does NOT affect approval / rejection / pricing

MASTER SPEC GUARANTEES:
- valuation_dossier.json is Single Source of Truth
- Read-only access
- Deterministic, explainable, audit-ready
"""

from typing import Dict, Any, List, TypedDict


class ActivationResult(TypedDict):
    allowed: bool
    reasons: List[str]
    valuation_hash: str
    policy_version: str


# Governance-locked policy version
POLICY_VERSION = "v1.0.0"


def check_income_approach_activation(
    valuation_dossier: Dict[str, Any]
) -> ActivationResult:
    """
    Check whether Income Approach is permitted to be activated.

    INPUT (Read-only):
    - valuation_dossier.json (SSOT)

    OUTPUT (Workflow-only):
    - ActivationResult

    GOVERNANCE:
    - No inference
    - No fallback
    - No auto-correction
    """

    reasons: List[str] = []

    # --- Mandatory SSOT checks ---
    valuation_hash = valuation_dossier.get("valuation_hash")
    if not valuation_hash:
        return {
            "allowed": False,
            "reasons": ["MISSING_VALUATION_HASH"],
            "valuation_hash": "UNKNOWN",
            "policy_version": POLICY_VERSION,
        }

    property_context = valuation_dossier.get("property_context", {})
    income_context = valuation_dossier.get("income_context", {})
    asset_type = property_context.get("asset_type")

    # --- Asset type eligibility ---
    if asset_type not in {"RENTAL", "COMMERCIAL", "MIXED_USE"}:
        reasons.append("ASSET_TYPE_NOT_INCOME_ELIGIBLE")

    # --- Income data availability ---
    declared_income = income_context.get("declared_income")
    lease_information = income_context.get("lease_information")

    if declared_income is None and lease_information is None:
        reasons.append("NO_DECLARED_INCOME_DATA")

    # --- Governance flags ---
    special_flags = valuation_dossier.get("special_flags", [])

    if "INCOME_DATA_UNVERIFIED" in special_flags:
        reasons.append("INCOME_DATA_UNVERIFIED")

    if "LEGAL_RESTRICTION_ON_RENTAL" in special_flags:
        reasons.append("LEGAL_RESTRICTION_ON_RENTAL")

    # --- Final permission decision ---
    allowed = len(reasons) == 0

    return {
        "allowed": allowed,
        "reasons": reasons,
        "valuation_hash": valuation_hash,
        "policy_version": POLICY_VERSION,
    }
