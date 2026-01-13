# Module: listing_intelligence/verification/address_verifier.py
# Part of Advanced AVM System

# listing_intelligence/verification/address_verifier.py

"""
ROLE:
    Address Verification Signal Generator

GOVERNANCE:
    - Deterministic
    - Rule-based only
    - No data mutation
    - No decision making

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Public verifier API
# ---------------------------------------------------------------------

def verify_address(
    *,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Verify address consistency and completeness.

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

    listing_addr = listing_snapshot.get("address", {})

    # -----------------------------------------------------------------
    # 1. Completeness check
    # -----------------------------------------------------------------
    required_fields = ["street", "ward", "district", "city"]
    missing_fields = [f for f in required_fields if not listing_addr.get(f)]

    if missing_fields:
        findings["missing_fields"] = missing_fields
        return _signal(
            status="FAIL",
            severity="HIGH",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    # -----------------------------------------------------------------
    # 2. Administrative consistency (basic sanity rules)
    # -----------------------------------------------------------------
    admin_warnings = _check_admin_consistency(listing_addr)
    if admin_warnings:
        findings["administrative_warnings"] = admin_warnings

    # -----------------------------------------------------------------
    # 3. Cross-reference with property record (if provided)
    # -----------------------------------------------------------------
    if property_reference:
        ref_addr = property_reference.get("address", {})
        mismatches = _compare_addresses(listing_addr, ref_addr)
        if mismatches:
            findings["reference_mismatches"] = mismatches

    # -----------------------------------------------------------------
    # 4. Ambiguity detection
    # -----------------------------------------------------------------
    ambiguity_flags = _detect_ambiguity(listing_addr)
    if ambiguity_flags:
        findings["ambiguity_flags"] = ambiguity_flags

    # -----------------------------------------------------------------
    # Final signal synthesis (NO DECISION)
    # -----------------------------------------------------------------
    if findings.get("reference_mismatches"):
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    if findings.get("administrative_warnings") or findings.get("ambiguity_flags"):
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

def _check_admin_consistency(address: Dict[str, Any]) -> List[str]:
    """
    Basic administrative sanity checks.
    No external lookup allowed.
    """

    warnings: List[str] = []

    district = address.get("district", "").lower()
    city = address.get("city", "").lower()

    if "hà nội" in city and district in ["thủ đức", "quận 9"]:
        warnings.append("district_not_consistent_with_city")

    if "hồ chí minh" in city and district in ["đống đa", "ba đình"]:
        warnings.append("district_not_consistent_with_city")

    return warnings


def _compare_addresses(
    listing_addr: Dict[str, Any],
    ref_addr: Dict[str, Any],
) -> List[str]:
    """
    Compare listing address with reference property address.
    """

    mismatches: List[str] = []

    for field in ["street", "ward", "district", "city"]:
        if ref_addr.get(field) and listing_addr.get(field):
            if ref_addr[field].strip().lower() != listing_addr[field].strip().lower():
                mismatches.append(f"{field}_mismatch")

    return mismatches


def _detect_ambiguity(address: Dict[str, Any]) -> List[str]:
    """
    Detect vague or ambiguous address descriptions.
    """

    flags: List[str] = []

    street = address.get("street", "").lower()

    vague_terms = ["gần", "khu vực", "xung quanh", "cạnh", "đối diện"]
    if any(term in street for term in vague_terms):
        flags.append("vague_street_description")

    return flags


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
