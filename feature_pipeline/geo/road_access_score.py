"""
Road Access Score
-----------------
Role:
- Generate descriptive road accessibility signal
- Purely structural & contextual
- No valuation or approval authority

Governance:
- MASTER_SPEC.md compliant
- Non-decisive
- Deterministic & auditable
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


def compute_road_access_score(
    road_access_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compute a descriptive road access score.

    Input (Read-only):
        road_access_info:
            road_width_m (optional)
            road_type (optional)  # e.g. alley, residential, main_road
            access_distance_m (optional)  # distance from property to road
            vehicle_access (optional)  # boolean or descriptive string
            source (optional)

    Output:
        RoadAccessSignal (descriptive only)
    """

    road_width: Optional[float] = road_access_info.get("road_width_m")
    access_distance: Optional[float] = road_access_info.get("access_distance_m")
    road_type: Optional[str] = road_access_info.get("road_type")
    vehicle_access = road_access_info.get("vehicle_access")

    score_components: Dict[str, Optional[float]] = {
        "width_component": None,
        "distance_component": None,
        "vehicle_access_component": None
    }

    # Width contribution (pure normalization, no desirability judgment)
    if road_width is not None:
        score_components["width_component"] = min(max(road_width / 10.0, 0.0), 1.0)

    # Distance contribution (closer ≠ better, just normalized inverse distance)
    if access_distance is not None and access_distance >= 0:
        score_components["distance_component"] = max(
            0.0,
            1.0 - min(access_distance / 200.0, 1.0)
        )

    # Vehicle access normalization
    if isinstance(vehicle_access, bool):
        score_components["vehicle_access_component"] = 1.0 if vehicle_access else 0.0

    valid_components = [
        v for v in score_components.values() if v is not None
    ]

    descriptive_score: Optional[float] = None
    if valid_components:
        descriptive_score = round(sum(valid_components) / len(valid_components), 4)

    payload: Dict[str, Any] = {
        "feature_group": "GEO_ROAD_ACCESS",
        "feature_version": "v1.0.0",
        "computed_at_utc": datetime.utcnow().isoformat(),
        "road_access_input": {
            "road_width_m": road_width,
            "access_distance_m": access_distance,
            "road_type": road_type,
            "vehicle_access": vehicle_access,
            "source": road_access_info.get("source")
        },
        "components": score_components,
        "road_access_score": descriptive_score,
        "notes": (
            "Road access score is a normalized descriptive signal only. "
            "It does not imply value, desirability, liquidity, or approval suitability."
        )
    }

    payload["signal_hash"] = _hash_payload(payload)

    return payload
