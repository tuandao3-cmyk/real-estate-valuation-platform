"""
Structural Tabular Feature Extraction
------------------------------------
Role:
- Extract deterministic, non-decisive structural features
- No valuation logic
- No scoring
- No thresholds

Governance:
- MASTER_SPEC.md compliant
- Read-only input
- Deterministic output
"""

from typing import Dict, Any
from datetime import datetime
import hashlib
import json


def _hash_payload(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def extract_structural_features(property_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structural (physical) features from a normalized property record.

    Input (Read-only):
        property_record: dict
            Expected normalized fields only.
            No raw ingestion, no guessing.

    Output (Feature-only):
        StructuralFeaturePayload (non-decisive)
    """

    features: Dict[str, Any] = {}

    # --- Basic dimensions ---
    features["land_area_sqm"] = property_record.get("land_area_sqm")
    features["gross_floor_area_sqm"] = property_record.get("gross_floor_area_sqm")
    features["num_floors"] = property_record.get("num_floors")
    features["frontage_m"] = property_record.get("frontage_m")
    features["access_road_width_m"] = property_record.get("access_road_width_m")

    # --- Shape & layout (descriptive only) ---
    features["plot_shape"] = property_record.get("plot_shape")
    features["corner_lot_flag"] = property_record.get("corner_lot_flag", False)

    # --- Construction metadata ---
    features["construction_year"] = property_record.get("construction_year")
    features["building_age_years"] = property_record.get("building_age_years")
    features["remaining_quality_ratio"] = property_record.get("remaining_quality_ratio")

    # --- Legal / planning descriptors (non-judgmental) ---
    features["zoning_label"] = property_record.get("zoning_label")
    features["planning_disclosure_flag"] = property_record.get(
        "planning_disclosure_flag", False
    )

    # --- Feature metadata ---
    feature_payload = {
        "feature_group": "STRUCTURAL_TABULAR",
        "feature_version": "v1.0.0",
        "extracted_at_utc": datetime.utcnow().isoformat(),
        "features": features
    }

    feature_payload["feature_hash"] = _hash_payload(feature_payload)

    return feature_payload
