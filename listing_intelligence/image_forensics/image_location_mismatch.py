"""
Image Location Mismatch Signal Generator
----------------------------------------

Role:
- Detect potential mismatch between image geolocation metadata (EXIF)
  and declared / normalized property location.

Governance:
- Signal-only
- Non-decisive
- Deterministic
- No valuation impact
- No fraud conclusion

Compliant with:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import hashlib
import json
import math


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class ImageGeoMetadata:
    latitude: Optional[float]
    longitude: Optional[float]
    source: str  # EXIF / AI_DERIVED / UNKNOWN


@dataclass(frozen=True)
class ReferenceLocation:
    latitude: float
    longitude: float
    reference_type: str  # DECLARED_ADDRESS / GEOCODED_ADDRESS


@dataclass(frozen=True)
class ImageLocationMismatchSignal:
    mismatch_status: str  # PASS / UNCERTAIN / MISMATCH / NO_GEO_DATA
    distance_km: Optional[float]
    threshold_km: float
    image_geo_source: str
    findings: Dict[str, Any]
    signal_hash: str


# =========================
# Utility Functions
# =========================

def haversine_distance_km(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate great-circle distance between two points on Earth.
    Deterministic and library-free.
    """
    R = 6371.0  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def compute_signal_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic signal hash for lineage & audit.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# =========================
# Core Signal Generator
# =========================

def generate_image_location_mismatch_signal(
    image_geo: ImageGeoMetadata,
    reference_location: ReferenceLocation,
    mismatch_threshold_km: float = 5.0,
) -> ImageLocationMismatchSignal:
    """
    Generate image location mismatch signal.

    Inputs:
    - image_geo: extracted image geolocation metadata (if any)
    - reference_location: declared or normalized property location
    - mismatch_threshold_km: static governance threshold

    Output:
    - ImageLocationMismatchSignal (signal-only)
    """

    findings: Dict[str, Any] = {
        "reference_type": reference_location.reference_type,
        "image_geo_available": image_geo.latitude is not None
        and image_geo.longitude is not None,
    }

    if image_geo.latitude is None or image_geo.longitude is None:
        payload = {
            "status": "NO_GEO_DATA",
            "findings": findings,
        }
        return ImageLocationMismatchSignal(
            mismatch_status="NO_GEO_DATA",
            distance_km=None,
            threshold_km=mismatch_threshold_km,
            image_geo_source=image_geo.source,
            findings=findings,
            signal_hash=compute_signal_hash(payload),
        )

    distance_km = haversine_distance_km(
        image_geo.latitude,
        image_geo.longitude,
        reference_location.latitude,
        reference_location.longitude,
    )

    if distance_km <= mismatch_threshold_km:
        status = "PASS"
    elif distance_km <= mismatch_threshold_km * 3:
        status = "UNCERTAIN"
    else:
        status = "MISMATCH"

    findings.update(
        {
            "distance_km": round(distance_km, 3),
            "threshold_km": mismatch_threshold_km,
            "image_geo_source": image_geo.source,
        }
    )

    payload = {
        "status": status,
        "distance_km": distance_km,
        "threshold_km": mismatch_threshold_km,
        "image_geo_source": image_geo.source,
        "reference_location": {
            "lat": reference_location.latitude,
            "lon": reference_location.longitude,
        },
    }

    return ImageLocationMismatchSignal(
        mismatch_status=status,
        distance_km=round(distance_km, 3),
        threshold_km=mismatch_threshold_km,
        image_geo_source=image_geo.source,
        findings=findings,
        signal_hash=compute_signal_hash(payload),
    )
