"""
Image GPS Metadata vs Listing Location Consistency Signal
---------------------------------------------------------

Role:
- Check consistency between image EXIF GPS metadata (if present)
  and declared listing latitude / longitude.

Governance:
- Signal-only
- Non-decisive
- Deterministic
- No fraud conclusion
- No valuation or workflow impact

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
class ImageGPSMetadata:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class GeoImageMatchSignal:
    geo_consistency_score: float  # descriptive, 0.0 – 1.0
    status: str  # PASS / UNCERTAIN
    distance_delta_meters: Optional[float]
    signal_hash: str


# =========================
# Utility Functions
# =========================

def haversine_distance_meters(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Compute haversine distance between two geo points in meters.
    Deterministic, no external dependency.
    """
    r = 6371000  # Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


def compute_signal_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic signal hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# =========================
# Core Signal Generator
# =========================

def generate_geo_image_match_signal(
    image_gps: Optional[ImageGPSMetadata],
    listing_latitude: float,
    listing_longitude: float,
    max_expected_distance_meters: float = 300.0,
) -> GeoImageMatchSignal:
    """
    Generate geo consistency signal between image GPS metadata
    and declared listing coordinates.

    Inputs (Read-only):
    - image_gps: extracted EXIF GPS metadata (optional)
    - listing_latitude / longitude: declared listing location
    - max_expected_distance_meters: static governance tolerance

    Output:
    - GeoImageMatchSignal (signal-only)
    """

    if image_gps is None:
        payload = {
            "image_gps_present": False,
            "listing_latitude": listing_latitude,
            "listing_longitude": listing_longitude,
        }

        return GeoImageMatchSignal(
            geo_consistency_score=0.5,
            status="UNCERTAIN",
            distance_delta_meters=None,
            signal_hash=compute_signal_hash(payload),
        )

    distance = haversine_distance_meters(
        image_gps.latitude,
        image_gps.longitude,
        listing_latitude,
        listing_longitude,
    )

    # Descriptive consistency score (not probabilistic)
    if distance <= max_expected_distance_meters:
        geo_consistency_score = round(
            1.0 - (distance / max_expected_distance_meters), 3
        )
        status = "PASS"
    else:
        geo_consistency_score = round(
            max(0.0, 1.0 - (distance / (max_expected_distance_meters * 3))), 3
        )
        status = "UNCERTAIN"

    payload = {
        "image_latitude": image_gps.latitude,
        "image_longitude": image_gps.longitude,
        "listing_latitude": listing_latitude,
        "listing_longitude": listing_longitude,
        "distance_meters": round(distance, 2),
        "tolerance_meters": max_expected_distance_meters,
        "status": status,
    }

    return GeoImageMatchSignal(
        geo_consistency_score=geo_consistency_score,
        status=status,
        distance_delta_meters=round(distance, 2),
        signal_hash=compute_signal_hash(payload),
    )
