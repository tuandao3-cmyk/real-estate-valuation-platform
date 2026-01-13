"""
Legal & Planning Tabular Feature Extraction
-------------------------------------------
Role:
- Extract descriptive legal / planning features
- No legal judgment
- No valuation logic
- No risk decision

Governance:
- MASTER_SPEC.md compliant
- Deterministic & replayable
"""

from typing import Dict, Any
from datetime import datetime
import hashlib
import json


def _hash_payload(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for lineage & audit.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def extract_legal_features(property_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract legal & planning related tabular features from a normalized property record.

    Input (Read-only):
        property_record: dict
            Must be normalized & validated upstream.
            No inference, no enrichment.

    Output (Feature-only):
        LegalFeaturePayload (non-decisive)
    """

    features: Dict[str, Any] = {}

    # --- Ownership & documentation (descriptive only) ---
    features["ownership_type"] = property_record.get("ownership_type")
    features["num_declared_owners"] = property_record.get("num_declared_owners")
    features["ownership_disclosure_flag"] = property_record.get(
        "ownership_disclosure_flag", False
    )

    # --- Legal documents ---
    features["has_land_use_right_certificate"] = property_record.get(
        "has_land_use_right_certificate"
    )
    features["certificate_type"] = property_record.get("certificate_type")
    features["certificate_issue_year"] = property_record.get("certificate_issue_year")

    # --- Planning & zoning disclosure ---
    features["declared_zoning_label"] = property_record.get("declared_zoning_label")
    features["planning_disclosure_flag"] = property_record.get(
        "planning_disclosure_flag", False
    )
    features["planning_notes_present"] = property_record.get(
        "planning_notes_present", False
    )

    # --- Restrictions & encumbrances (declared only) ---
    features["declared_mortgage_flag"] = property_record.get(
        "declared_mortgage_flag", False
    )
    features["declared_dispute_flag"] = property_record.get(
        "declared_dispute_flag", False
    )
    features["usage_restriction_flag"] = property_record.get(
        "usage_restriction_flag", False
    )

    # --- Feature metadata ---
    feature_payload = {
        "feature_group": "LEGAL_TABULAR",
        "feature_version": "v1.0.0",
        "extracted_at_utc": datetime.utcnow().isoformat(),
        "features": features
    }

    feature_payload["feature_hash"] = _hash_payload(feature_payload)

    return feature_payload
