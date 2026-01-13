"""
Temporal / Time-Based Tabular Feature Extraction
-----------------------------------------------
Role:
- Extract time & freshness related features
- No trend inference
- No forecasting
- No valuation logic

Governance:
- MASTER_SPEC.md compliant
- Deterministic & replayable
"""

from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import json


def _hash_payload(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _safe_year_diff(current_year: int, past_year: Optional[int]) -> Optional[int]:
    if past_year is None:
        return None
    return max(current_year - past_year, 0)


def extract_time_features(
    property_record: Dict[str, Any],
    reference_time_utc: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extract time-related tabular features.

    Input (Read-only):
        property_record: dict
            Normalized property record.
        reference_time_utc: ISO timestamp (optional)
            If not provided, uses current UTC time.

    Output:
        TimeFeaturePayload (non-decisive)
    """

    now = (
        datetime.fromisoformat(reference_time_utc)
        if reference_time_utc
        else datetime.utcnow()
    )

    current_year = now.year

    features: Dict[str, Any] = {}

    # --- Construction & asset age ---
    features["construction_year"] = property_record.get("construction_year")
    features["asset_age_years"] = _safe_year_diff(
        current_year,
        property_record.get("construction_year")
    )

    # --- Renovation / upgrade disclosure ---
    features["last_renovation_year"] = property_record.get("last_renovation_year")
    features["years_since_renovation"] = _safe_year_diff(
        current_year,
        property_record.get("last_renovation_year")
    )

    # --- Listing & transaction timestamps ---
    features["listing_created_at"] = property_record.get("listing_created_at")
    features["last_transaction_year"] = property_record.get("last_transaction_year")
    features["years_since_last_transaction"] = _safe_year_diff(
        current_year,
        property_record.get("last_transaction_year")
    )

    # --- Data freshness indicators (descriptive only) ---
    features["data_snapshot_year"] = property_record.get("data_snapshot_year")
    features["years_since_data_snapshot"] = _safe_year_diff(
        current_year,
        property_record.get("data_snapshot_year")
    )

    # --- Feature metadata ---
    feature_payload = {
        "feature_group": "TIME_TABULAR",
        "feature_version": "v1.0.0",
        "reference_time_utc": now.isoformat(),
        "extracted_at_utc": datetime.utcnow().isoformat(),
        "features": features
    }

    feature_payload["feature_hash"] = _hash_payload(feature_payload)

    return feature_payload
