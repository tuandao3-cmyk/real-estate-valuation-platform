# Module: listing_intelligence/verification/legal_verifier.py
# Part of Advanced AVM System

# listing_intelligence/verification/legal_verifier.py

"""
ROLE:
    Legal Status Verification Signal Generator

GOVERNANCE:
    - Deterministic
    - Rule-based only
    - No external lookup
    - No legal judgment
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Public verifier API
# ---------------------------------------------------------------------

def verify_legal_status(
    *,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Verify declared legal status information.

    INPUT:
        listing_snapshot (read-only)
        property_reference (optional, read-only)

    OUTPUT (signal only):
        {
            "status": PASS | FAIL | UNCERTAIN,
            "severity": LOW | MEDIUM | HIGH,
            "findings": {...},
            "evidence_refs": [...]
        }
    """

    findings: Dict[str, Any] = {}
    evidence_refs: List[str] = []

    legal = listing_snapshot.get("legal_status", {})

    # -----------------------------------------------------------------
    # 1. Legal document declaration
    # -----------------------------------------------------------------
    legal_doc_type = legal.get("document_type")
    if not legal_doc_type:
        findings["missing_legal_document_declaration"] = True
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    # -----------------------------------------------------------------
    # 2. Ownership declaration
    # -----------------------------------------------------------------
    owner_declared = legal.get("owner_declared")
    if not owner_declared:
        findings["missing_owner_declaration"] = True

    # -----------------------------------------------------------------
    # 3. Encumbrance / dispute disclosure
    # -----------------------------------------------------------------
    encumbrances = legal.get("encumbrances", {})
    disclosed_flags = []

    for key in ["mortgage", "dispute", "seizure"]:
        if encumbrances.get(key) is True:
            disclosed_flags.append(key)

    if disclosed_flags:
        findings["declared_encumbrances"] = disclosed_flags

    # -----------------------------------------------------------------
    # 4. Planning / restriction disclosure
    # -----------------------------------------------------------------
    planning = legal.get("planning_status")
    if planning in ["quy_hoach_treo", "han_che_xay_dung"]:
        findings["planning_restriction_declared"] = planning

    # -----------------------------------------------------------------
    # 5. Cross-reference with property record (if available)
    # -----------------------------------------------------------------
    if property_reference:
        ref_legal = property_reference.get("legal_status", {})
        mismatches = _compare_legal_declaration(legal, ref_legal)
        if mismatches:
            findings["reference_mismatches"] = mismatches

    # -----------------------------------------------------------------
    # Signal synthesis (NO DECISION)
    # -----------------------------------------------------------------
    if findings.get("reference_mismatches"):
        return _signal(
            status="UNCERTAIN",
            severity="HIGH",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    if findings.get("declared_encumbrances") or findings.get("planning_restriction_declared"):
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    if findings:
        return _signal(
            status="UNCERTAIN",
            severity="LOW",
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

def _compare_legal_declaration(
    listing_legal: Dict[str, Any],
    ref_legal: Dict[str, Any],
) -> List[str]:
    """
    Compare declared legal fields with reference record.
    """

    mismatches: List[str] = []

    for field in ["document_type", "owner_declared"]:
        if ref_legal.get(field) and listing_legal.get(field):
            if ref_legal[field] != listing_legal[field]:
                mismatches.append(f"{field}_mismatch")

    return mismatches


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
