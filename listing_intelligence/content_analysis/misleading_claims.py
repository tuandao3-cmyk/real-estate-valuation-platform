# Module: listing_intelligence/content_analysis/misleading_claims.py
# Part of Advanced AVM System

# listing_intelligence/content_analysis/misleading_claims.py

"""
ROLE:
    Misleading Declarative Claims Signal Generator

GOVERNANCE:
    - Rule-based only
    - No ML / No LLM
    - No factual verification
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List
import re


# ---------------------------------------------------------------------
# Governance-approved declarative claim patterns
# ---------------------------------------------------------------------

DECLARATIVE_PATTERNS = {
    "legal_claims": [
        "sổ đỏ",
        "sổ hồng",
        "pháp lý đầy đủ",
        "đã hoàn công",
        "đã ra sổ",
    ],
    "planning_claims": [
        "không quy hoạch",
        "ổn định lâu dài",
        "không tranh chấp",
    ],
    "ownership_claims": [
        "chính chủ",
        "chủ đứng bán",
        "không qua trung gian",
    ],
    "usage_claims": [
        "ở ngay",
        "kinh doanh tốt",
        "cho thuê tốt",
    ],
}

ABSOLUTE_MODIFIERS = [
    "100%",
    "hoàn toàn",
    "chắc chắn",
    "đảm bảo",
    "vĩnh viễn",
]


# ---------------------------------------------------------------------
# Public detector API
# ---------------------------------------------------------------------

def detect_misleading_claims(
    *,
    description: str | None,
    declared_facts: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Detect potentially misleading declarative claims
    that exceed declared or supported facts.

    INPUT (read-only):
        description
        declared_facts (optional structured disclosures)

    OUTPUT (signal only):
        {
            "status": PASS | UNCERTAIN,
            "severity": LOW | MEDIUM,
            "findings": {...},
            "evidence_refs": [...]
        }
    """

    findings: Dict[str, Any] = {}
    evidence_refs: List[str] = []

    if not description:
        return _signal(
            status="PASS",
            severity="LOW",
            findings={},
            evidence_refs=evidence_refs,
        )

    text = description.lower()

    # -----------------------------------------------------------------
    # 1. Detect declarative claims by category
    # -----------------------------------------------------------------
    for category, patterns in DECLARATIVE_PATTERNS.items():
        hits = _match_patterns(text, patterns)
        if hits:
            findings[f"{category}_claims_detected"] = hits

    # -----------------------------------------------------------------
    # 2. Absolute modifier amplification
    # -----------------------------------------------------------------
    abs_hits = _match_patterns(text, ABSOLUTE_MODIFIERS)
    if abs_hits:
        findings["absolute_modifiers_used"] = abs_hits

    # -----------------------------------------------------------------
    # 3. Claim vs declared facts mismatch (shallow check)
    # -----------------------------------------------------------------
    if declared_facts:
        if "legal_status" in declared_facts:
            if declared_facts.get("legal_status") in ["unknown", "partial"]:
                if "legal_claims_detected" in findings:
                    findings["legal_claims_without_full_disclosure"] = True

        if "ownership_type" in declared_facts:
            if declared_facts.get("ownership_type") != "single_owner":
                if "ownership_claims_detected" in findings:
                    findings["ownership_claims_conflict"] = True

    # -----------------------------------------------------------------
    # Signal synthesis (NO DECISION)
    # -----------------------------------------------------------------
    if findings:
        severity = "MEDIUM" if (
            "absolute_modifiers_used" in findings
            or len(findings) > 1
        ) else "LOW"

        return _signal(
            status="UNCERTAIN",
            severity=severity,
            findings=findings,
            evidence_refs=evidence_refs,
        )

    return _signal(
        status="PASS",
        severity="LOW",
        findings=findings,
        evidence_refs=evidence_refs,
    )


# ---------------------------------------------------------------------
# Internal helpers (pure, deterministic)
# ---------------------------------------------------------------------

def _match_patterns(text: str, patterns: List[str]) -> List[str]:
    hits = []
    for p in patterns:
        if p in text:
            hits.append(p)
    return hits


def _signal(
    *,
    status: str,
    severity: str,
    findings: Dict[str, Any],
    evidence_refs: List[str],
) -> Dict[str, Any]:
    """
    Standardized signal output.
    """
    return {
        "status": status,
        "severity": severity,
        "findings": findings,
        "evidence_refs": evidence_refs,
    }
