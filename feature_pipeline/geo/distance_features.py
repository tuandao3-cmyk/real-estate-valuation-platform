"""
Distance Features
-----------------
Role:
- Generate descriptive distance-based geospatial features
- Pure geometry, no valuation semantics

Governance:
- MASTER_SPEC.md compliant
- Non-decisive
- Deterministic
"""

from typing import Dict, Any, Optional
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import hashlib
import json


EARTH_RADIUS_KM = 6371.0


def _hash_payload(payload: Dict[str, Any]) -> str:
    """
    Create deterministic SHA-256 hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _haversine_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate Haversine distance in kilometers.
    """
    lat1_r, lon1_r = radians(lat1), radians(lon1)
    lat2_r, lon2_r = radians(lat2), radians(lon2)

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = sin(dlat / 2) ** 2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def compute_distance_features(
    subject_location: Dict[str, Any],
    reference_points: Dict[str, Dict[str, float]]
) -> Dict[str, Any]:
    """
    Compute distance features from subject location to reference points.

    Input (Read-only):
        subject_location:
            latitude
            longitude
            geo_confidence (optional)
            geo_source (optional)

        reference_points:
            {
                "city_center": {"latitude": ..., "longitude": ...},
                "district_center": {...},
                "landmark_x": {...}
            }

    Output:
        DistanceFeatureSignal (descriptive only)
    """

    latitude: Optional[float] = subject_location.get("latitude")
    longitude: Optional[float] = subject_location.get("longitude")

    distances: Dict[str, Optional[float]] = {}

    if latitude is not None and longitude is not None:
        for ref_name, ref in reference_points.items():
            ref_lat = ref.get("latitude")
            ref_lon = ref.get("longitude")

            if ref_lat is None or ref_lon is None:
                distances[ref_name] = None
                continue

            distances[ref_name] = round(
                _haversine_km(latitude, longitude, ref_lat, ref_lon),
                4
            )
    else:
        for ref_name in reference_points.keys():
            distances[ref_name] = None

    payload: Dict[str, Any] = {
        "feature_group": "GEO_DISTANCE",
        "feature_version": "v1.0.0",
        "computed_at_utc": datetime.utcnow().isoformat(),
        "subject_location": {
            "latitude": latitude,
            "longitude": longitude,
            "geo_confidence": subject_location.get("geo_confidence"),
            "geo_source": subject_location.get("geo_source")
        },
        "distance_km": distances,
        "notes": (
            "Distances are geometric only. "
            "No assumptions about accessibility, value, or desirability."
        )
    }

    payload["distance_hash"] = _hash_payload(payload)

    return payload
