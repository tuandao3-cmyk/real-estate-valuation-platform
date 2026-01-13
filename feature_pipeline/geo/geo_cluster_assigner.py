"""
Geo Cluster Assigner
-------------------
Role:
- Assign static geospatial clusters based on coordinates
- Pure spatial grouping, no market or valuation semantics

Governance:
- MASTER_SPEC.md compliant
- No learning
- No inference
"""

from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import json
import math


def _hash_payload(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _grid_cluster_id(
    latitude: float,
    longitude: float,
    grid_size_deg: float
) -> str:
    """
    Assign a grid-based cluster ID.

    NOTE:
    - Grid-based, not data-driven
    - Deterministic & static
    """
    lat_bucket = math.floor(latitude / grid_size_deg)
    lon_bucket = math.floor(longitude / grid_size_deg)

    return f"GRID_{lat_bucket}_{lon_bucket}"


def assign_geo_cluster(
    geo_signal: Dict[str, Any],
    cluster_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Assign a static geospatial cluster.

    Input (Read-only):
        geo_signal:
            latitude
            longitude
            geo_confidence (optional)
            geo_source (optional)

        cluster_config:
            grid_size_deg (float, static & governance-approved)
            cluster_scheme_id (string)

    Output:
        GeoClusterSignal (descriptive only)
    """

    latitude: Optional[float] = geo_signal.get("latitude")
    longitude: Optional[float] = geo_signal.get("longitude")

    grid_size: float = cluster_config.get("grid_size_deg", 0.01)
    scheme_id: str = cluster_config.get("cluster_scheme_id", "GRID_V1")

    cluster_id: Optional[str] = None

    if latitude is not None and longitude is not None:
        cluster_id = _grid_cluster_id(latitude, longitude, grid_size)

    payload: Dict[str, Any] = {
        "feature_group": "GEO_CLUSTER",
        "feature_version": "v1.0.0",
        "assigned_at_utc": datetime.utcnow().isoformat(),
        "cluster_scheme_id": scheme_id,
        "grid_size_deg": grid_size,
        "input_geo": {
            "latitude": latitude,
            "longitude": longitude,
            "geo_confidence": geo_signal.get("geo_confidence"),
            "geo_source": geo_signal.get("geo_source")
        },
        "cluster_id": cluster_id,
        "notes": (
            "Geospatial cluster is a static spatial grouping only. "
            "It does not represent market zones, price areas, or desirability."
        )
    }

    payload["cluster_hash"] = _hash_payload(payload)

    return payload
