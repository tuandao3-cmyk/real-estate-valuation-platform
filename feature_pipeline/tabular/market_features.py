"""
Market Context Tabular Feature Extraction
----------------------------------------
Role:
- Extract descriptive market context features
- No price prediction
- No trend inference
- No valuation logic

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
    Deterministic SHA-256 hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def extract_market_features(property_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract market-related tabular features.

    Input (Read-only):
        property_record: dict
            Normalized, validated upstream.
            No enrichment or inference here.

    Output:
        MarketFeaturePayload (non-decisive)
    """

    features: Dict[str, Any] = {}

    # --- Supply-side context (descriptive) ---
    features["nearby_listing_count"] = property_record.get("nearby_listing_count")
    features["nearby_project_count"] = property_record.get("nearby_project_count")
    features["new_supply_flag"] = property_record.get("new_supply_flag", False)

    # --- Transaction activity (historical, descriptive only) ---
    features["recent_transaction_count"] = property_record.get(
        "recent_transaction_count"
    )
    features["transaction_observation_window_months"] = property_record.get(
        "transaction_observation_window_months"
    )

    # --- Liquidity proxy (non-judgmental) ---
    features["avg_days_on_market"] = property_record.get("avg_days_on_market")
    features["listing_turnover_rate"] = property_record.get("listing_turnover_rate")

    # --- Market segmentation labels ---
    features["market_segment_label"] = property_record.get("market_segment_label")
    features["locality_market_code"] = property_record.get("locality_market_code")

    # --- Feature metadata ---
    feature_payload = {
        "feature_group": "MARKET_TABULAR",
        "feature_version": "v1.0.0",
        "extracted_at_utc": datetime.utcnow().isoformat(),
        "features": features
    }

    feature_payload["feature_hash"] = _hash_payload(feature_payload)

    return feature_payload
