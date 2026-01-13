# Module: listing_intelligence/verification/occupancy_verifier.py
# Part of Advanced AVM System

# listing_intelligence/verification/occupancy_verifier.py

"""
ROLE:
    Occupancy / Usage Disclosure Verification Signal Generator

GOVERNANCE:
    - Deterministic
    - Rule-based only
    - No legal judgment
    - No external verification
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Public verifier API
# ---------------------------------------------------------------------

def verify_occupancy(
    *,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Verify declared occupancy / usage information.

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

    occupancy = listing_snapshot.get("occupancy", {})

    # -----------------------------------------------------------------
    # 1. Occupancy declaration presence
    # -----------------------------------------------------------------
    occupancy_status = occupancy.get("status")
    if not occupancy_status:
        findings["missing_occupancy_status"] = True
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    occupancy_status = occupancy_status.lower()

    # -----------------------------------------------------------------
    # 2. Internal consistency checks
    # -----------------------------------------------------------------
    occupant_type = occupancy.get("occupant_type")

    if occupancy_status == "vacant" and occupant_type:
        findings["vacant_with_occupant_declared"] = {
            "occupant_type": occupant_type
        }

    if occupancy_status == "occupied" and not occupant_type:
        findings["occupied_without_occupant_type"] = True

    # Utility usage sanity (if declared)
    utilities_active = occupancy.get("utilities_active")
    if occupancy_status == "vacant" and utilities_active is True:
        findings["vacant_with_active_utilities"] = True

    # -----------------------------------------------------------------
    # 3. Occupancy vs asset type sanity
    # -----------------------------------------------------------------
    asset_type = listing_snapshot.get("asset_type")
    incompatibilities = _check_occupancy_asset_compatibility(
        occupancy_status=occupancy_status,
        asset_type=asset_type,
    )
    if incompatibilities:
        findings["occupancy_asset_incompatibility"] = incompatibilities

    # -----------------------------------------------------------------
    # 4. Cross-reference with property record (if available)
    # -----------------------------------------------------------------
    if property_reference:
        ref_occupancy = property_reference.get("occupancy", {})
        mismatches = _compare_occupancy(occupancy, ref_occupancy)
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

def _check_occupancy_asset_compatibility(
    *,
    occupancy_status: str,
    asset_type: str | None,
) -> List[str]:
    """
    Check basic logical compatibility between occupancy declaration
    and asset type. This is NOT a legal judgment.
    """

    issues: List[str] = []

    if not asset_type:
        return issues

    asset_type = asset_type.lower()

    if asset_type in ["dat_trong", "dat_nong_nghiep"] and occupancy_status == "occupied":
        issues.append("occupied_declared_on_non_residential_land")

    return issues


def _compare_occupancy(
    listing_occupancy: Dict[str, Any],
    ref_occupancy: Dict[str, Any],
) -> List[str]:
    """
    Compare occupancy declaration with reference record.
    """

    mismatches: List[str] = []

    for field in ["status", "occupant_type"]:
        if ref_occupancy.get(field) and listing_occupancy.get(field):
            if ref_occupancy[field] != listing_occupancy[field]:
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
