"""
Administrative Mapper
---------------------
Role:
- Deterministic mapping from geo signals to administrative labels
- Reference-only, non-legal, non-decisive

Governance:
- MASTER_SPEC.md compliant
- No inference
- No overwrite
"""

from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import json


def _hash_payload(payload: Dict[str, Any]) -> str:
    """
    Create deterministic SHA-256 hash for lineage & audit.
    """
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def map_administrative_units(
    geo_signal: Dict[str, Any],
    admin_reference: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Map geographic signal to administrative units.

    Input (Read-only):
        geo_signal:
            latitude
            longitude
            geo_confidence (optional)
            geo_source (optional)

        admin_reference:
            Pre-approved static lookup table
            (e.g. geohash → admin codes)

    Output:
        AdministrativeMappingSignal (descriptive only)
    """

    latitude: Optional[float] = geo_signal.get("latitude")
    longitude: Optional[float] = geo_signal.get("longitude")

    admin_mapping: Dict[str, Any] = {
        "country_code": None,
        "province_code": None,
        "district_code": None,
        "ward_code": None,
        "admin_source": None
    }

    if latitude is not None and longitude is not None:
        key = f"{round(latitude, 4)}_{round(longitude, 4)}"
        mapped = admin_reference.get(key)

        if mapped:
            admin_mapping.update({
                "country_code": mapped.get("country_code"),
                "province_code": mapped.get("province_code"),
                "district_code": mapped.get("district_code"),
                "ward_code": mapped.get("ward_code"),
                "admin_source": mapped.get("source")
            })

    payload: Dict[str, Any] = {
        "feature_group": "GEO_ADMIN_MAPPING",
        "feature_version": "v1.0.0",
        "mapped_at_utc": datetime.utcnow().isoformat(),
        "input_geo": {
            "latitude": latitude,
            "longitude": longitude,
            "geo_confidence": geo_signal.get("geo_confidence"),
            "geo_source": geo_signal.get("geo_source")
        },
        "administrative_units": admin_mapping
    }

    payload["mapping_hash"] = _hash_payload(payload)

    return payload
