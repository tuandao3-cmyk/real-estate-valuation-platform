# Module: listing_intelligence/verification/ownership_consistency.py
# Part of Advanced AVM System
# listing_intelligence/verification/ownership_consistency.py

"""
ROLE:
    Ownership Disclosure Consistency Verification Signal Generator

GOVERNANCE:
    - Deterministic
    - Rule-based only
    - No legal ownership judgment
    - No external registry lookup
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Public verifier API
# ---------------------------------------------------------------------

def verify_ownership_consistency(
    *,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Verify ownership declaration consistency.

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

    ownership = listing_snapshot.get("ownership", {})

    # -----------------------------------------------------------------
    # 1. Ownership declaration presence
    # -----------------------------------------------------------------
    ownership_type = ownership.get("ownership_type")
    owners = ownership.get("owners")

    if not ownership_type:
        findings["missing_ownership_type"] = True
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    # Normalize
    ownership_type = ownership_type.lower()
    owners = owners or []

    # -----------------------------------------------------------------
    # 2. Internal consistency checks
    # -----------------------------------------------------------------
    if ownership_type == "sole" and len(owners) > 1:
        findings["sole_ownership_with_multiple_owners"] = {
            "declared_owner_count": len(owners)
        }

    if ownership_type in ["joint", "co_ownership"] and len(owners) < 2:
        findings["joint_ownership_with_insufficient_owners"] = {
            "declared_owner_count": len(owners)
        }

    if ownership_type and not owners:
        findings["ownership_declared_without_owner_list"] = True

    # -----------------------------------------------------------------
    # 3. Listing role vs ownership sanity
    # -----------------------------------------------------------------
    lister_role = listing_snapshot.get("lister_role")

    if lister_role == "broker" and ownership.get("authority_scope") == "full":
        findings["broker_declared_full_ownership_authority"] = True

    # -----------------------------------------------------------------
    # 4. Cross-reference with property record (if available)
    # -----------------------------------------------------------------
    if property_reference:
        ref_ownership = property_reference.get("ownership", {})
        mismatches = _compare_ownership(ownership, ref_ownership)
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

    if findings:
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
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

def _compare_ownership(
    listing_ownership: Dict[str, Any],
    ref_ownership: Dict[str, Any],
) -> List[str]:
    """
    Compare ownership declaration with reference record.
    """

    mismatches: List[str] = []

    for field in ["ownership_type"]:
        if ref_ownership.get(field) and listing_ownership.get(field):
            if ref_ownership[field] != listing_ownership[field]:
                mismatches.append(f"{field}_mismatch")

    ref_owner_count = len(ref_ownership.get("owners", []))
    listing_owner_count = len(listing_ownership.get("owners", []))

    if ref_owner_count and listing_owner_count:
        if ref_owner_count != listing_owner_count:
            mismatches.append("owner_count_mismatch")

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

