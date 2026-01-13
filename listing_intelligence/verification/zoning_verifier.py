# Module: listing_intelligence/verification/zoning_verifier.py
# Part of Advanced AVM System

# listing_intelligence/verification/zoning_verifier.py

"""
ROLE:
    Zoning / Land-Use Declaration Verification Signal Generator

GOVERNANCE:
    - Deterministic
    - Rule-based only
    - No external zoning lookup
    - No legal or planning judgment
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Public verifier API
# ---------------------------------------------------------------------

def verify_zoning(
    *,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Verify declared zoning / land-use information.

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

    zoning = listing_snapshot.get("zoning", {})

    # -----------------------------------------------------------------
    # 1. Zoning declaration presence
    # -----------------------------------------------------------------
    land_use_type = zoning.get("land_use_type")
    if not land_use_type:
        findings["missing_land_use_declaration"] = True
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    # -----------------------------------------------------------------
    # 2. Basic land-use sanity vs asset type
    # -----------------------------------------------------------------
    asset_type = listing_snapshot.get("asset_type")

    incompatibilities = _check_land_use_compatibility(
        land_use_type=land_use_type,
        asset_type=asset_type,
    )
    if incompatibilities:
        findings["land_use_incompatibility"] = incompatibilities

    # -----------------------------------------------------------------
    # 3. Restriction / planning disclosure
    # -----------------------------------------------------------------
    restrictions = zoning.get("restrictions", {})
    disclosed_restrictions = []

    for key in ["lo_gioi", "hanh_lang_bao_ve", "quy_hoach_treo"]:
        if restrictions.get(key) is True:
            disclosed_restrictions.append(key)

    if disclosed_restrictions:
        findings["declared_restrictions"] = disclosed_restrictions

    # -----------------------------------------------------------------
    # 4. Cross-reference with property record (if available)
    # -----------------------------------------------------------------
    if property_reference:
        ref_zoning = property_reference.get("zoning", {})
        mismatches = _compare_zoning(zoning, ref_zoning)
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

    if findings.get("land_use_incompatibility") or findings.get("declared_restrictions"):
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

def _check_land_use_compatibility(
    *,
    land_use_type: str,
    asset_type: str | None,
) -> List[str]:
    """
    Check basic logical compatibility between land-use declaration
    and asset type. This is NOT a legal judgment.
    """

    issues: List[str] = []

    if not asset_type:
        return issues

    land_use_type = land_use_type.lower()
    asset_type = asset_type.lower()

    if land_use_type == "dat_nong_nghiep" and asset_type in ["nha_o", "can_ho"]:
        issues.append("residential_asset_on_agricultural_land")

    if land_use_type == "dat_o" and asset_type in ["nha_xuong", "cong_trinh_cong_nghiep"]:
        issues.append("industrial_asset_on_residential_land")

    return issues


def _compare_zoning(
    listing_zoning: Dict[str, Any],
    ref_zoning: Dict[str, Any],
) -> List[str]:
    """
    Compare zoning declaration with reference record.
    """

    mismatches: List[str] = []

    for field in ["land_use_type"]:
        if ref_zoning.get(field) and listing_zoning.get(field):
            if ref_zoning[field] != listing_zoning[field]:
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
