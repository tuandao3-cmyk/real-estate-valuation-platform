"""
SIMILARITY FEATURES MODULE
==========================

Role:
- Generate descriptive similarity signals between a target property
  and comparable properties.

Governance:
- NON-DECISIVE
- READ-ONLY
- NO WEIGHTING
- NO RANKING
- NO PRICE INFERENCE

Compliance:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – ADVANCED AVM

If this module affects pricing or approval logic → SYSTEM VIOLATION
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import math
import hashlib


# -------------------------------------------------------------------
# Data Contracts
# -------------------------------------------------------------------

@dataclass(frozen=True)
class PropertySnapshot:
    """
    Immutable snapshot of property attributes used for similarity signals.

    NOTE:
    - These are descriptive attributes only.
    - Legal truth, valuation truth, and pricing are handled elsewhere.
    """
    property_id: str
    latitude: float
    longitude: float
    land_area_sqm: float | None
    building_area_sqm: float | None
    year_built: int | None
    floor_count: int | None
    asset_type: str
    administrative_area_code: str


@dataclass(frozen=True)
class SimilaritySignal:
    """
    Output signal — descriptive only.
    """
    target_property_id: str
    comparable_property_id: str
    signals: Dict[str, Any]
    signal_hash: str


# -------------------------------------------------------------------
# Utility Functions (Pure / Deterministic)
# -------------------------------------------------------------------

def _haversine_distance_meters(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate great-circle distance between two points.
    Pure math. No interpretation.
    """
    r = 6371000.0  # Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


def _safe_ratio(a: float | None, b: float | None) -> float | None:
    """
    Compute a/b safely.
    """
    if a is None or b is None or b == 0:
        return None
    return a / b


def _hash_signal(payload: Dict[str, Any]) -> str:
    """
    Deterministic signal hash for audit & replay.
    """
    serialized = str(sorted(payload.items())).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


# -------------------------------------------------------------------
# Similarity Feature Generator
# -------------------------------------------------------------------

class SimilarityFeatureGenerator:
    """
    Generate similarity signals between target property and comparables.

    Governance Rules:
    - No thresholds
    - No scores
    - No ranking
    - No selection logic
    """

    @staticmethod
    def generate(
        target: PropertySnapshot,
        comparable: PropertySnapshot,
    ) -> SimilaritySignal:
        """
        Generate descriptive similarity metrics.

        Output is intentionally verbose & raw.
        Interpretation is forbidden at this layer.
        """

        signals: Dict[str, Any] = {}

        # ------------------------------------------------------------
        # Geographic proximity (distance only)
        # ------------------------------------------------------------
        signals["geo_distance_m"] = _haversine_distance_meters(
            target.latitude,
            target.longitude,
            comparable.latitude,
            comparable.longitude,
        )

        # ------------------------------------------------------------
        # Area relationships (ratios only)
        # ------------------------------------------------------------
        signals["land_area_ratio"] = _safe_ratio(
            target.land_area_sqm, comparable.land_area_sqm
        )
        signals["building_area_ratio"] = _safe_ratio(
            target.building_area_sqm, comparable.building_area_sqm
        )

        # ------------------------------------------------------------
        # Temporal relationship
        # ------------------------------------------------------------
        if target.year_built is not None and comparable.year_built is not None:
            signals["year_built_diff"] = (
                target.year_built - comparable.year_built
            )
        else:
            signals["year_built_diff"] = None

        # ------------------------------------------------------------
        # Structural relationship
        # ------------------------------------------------------------
        if target.floor_count is not None and comparable.floor_count is not None:
            signals["floor_count_diff"] = (
                target.floor_count - comparable.floor_count
            )
        else:
            signals["floor_count_diff"] = None

        # ------------------------------------------------------------
        # Categorical consistency (boolean flags only)
        # ------------------------------------------------------------
        signals["same_asset_type"] = (
            target.asset_type == comparable.asset_type
        )

        signals["same_administrative_area"] = (
            target.administrative_area_code
            == comparable.administrative_area_code
        )

        # ------------------------------------------------------------
        # Final signal hash
        # ------------------------------------------------------------
        signal_hash = _hash_signal(signals)

        return SimilaritySignal(
            target_property_id=target.property_id,
            comparable_property_id=comparable.property_id,
            signals=signals,
            signal_hash=signal_hash,
        )


# -------------------------------------------------------------------
# Batch Helper (No Selection Logic)
# -------------------------------------------------------------------

def generate_similarity_matrix(
    target: PropertySnapshot,
    comparables: List[PropertySnapshot],
) -> List[SimilaritySignal]:
    """
    Generate similarity signals for all comparables.

    IMPORTANT:
    - This does NOT choose, rank, or filter comparables.
    - Downstream modules must respect governance boundaries.
    """

    results: List[SimilaritySignal] = []

    for comp in comparables:
        results.append(
            SimilarityFeatureGenerator.generate(target, comp)
        )

    return results
