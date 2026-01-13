"""
COMPARABLE AFFINITY (PER-DIMENSION) MODULE
=========================================

Role:
- Generate PER-DIMENSION affinity signals between target property
  and comparable properties.
- These affinities are DESCRIPTIVE ONLY.

Strict Governance:
- NO composite weight
- NO normalization to sum=1
- NO ranking / selection
- NO price interaction
- NO approval logic

If this module is used to affect pricing, approval, or ranking
→ SYSTEM VIOLATION (MASTER_SPEC.md).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import math
import hashlib


# -------------------------------------------------------------------
# Data Contracts (Read-only, Descriptive)
# -------------------------------------------------------------------

@dataclass(frozen=True)
class AffinitySignal:
    """
    Per-dimension affinity signals.

    NOTE:
    - Each field is independent.
    - There is NO combined score by design.
    """
    target_property_id: str
    comparable_property_id: str
    affinities: Dict[str, Optional[float]]
    affinity_hash: str


# -------------------------------------------------------------------
# Deterministic Kernel Helpers (Bounded, Interpretable)
# -------------------------------------------------------------------

def _bounded_inverse_distance(value: Optional[float], scale: float) -> Optional[float]:
    """
    Convert a distance-like value into a bounded affinity (0, 1].

    affinity = 1 / (1 + value / scale)

    Governance:
    - Pure math
    - No threshold
    - No interpretation
    """
    if value is None or scale <= 0:
        return None
    return 1.0 / (1.0 + (value / scale))


def _bounded_ratio_affinity(ratio: Optional[float]) -> Optional[float]:
    """
    Convert ratio closeness to bounded affinity.

    affinity = exp(-|1 - ratio|)

    Governance:
    - Symmetric
    - Bounded (0, 1]
    - No weighting
    """
    if ratio is None:
        return None
    return math.exp(-abs(1.0 - ratio))


def _bounded_difference_affinity(diff: Optional[float], scale: float) -> Optional[float]:
    """
    Convert absolute difference to bounded affinity.

    affinity = exp(-|diff| / scale)
    """
    if diff is None or scale <= 0:
        return None
    return math.exp(-abs(diff) / scale)


def _hash_affinity(payload: Dict[str, Any]) -> str:
    """
    Deterministic hash for audit & replay.
    """
    serialized = str(sorted(payload.items())).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


# -------------------------------------------------------------------
# Affinity Generator (NO COMPOSITE LOGIC)
# -------------------------------------------------------------------

class ComparableAffinityGenerator:
    """
    Generate per-dimension affinity signals.

    Governance Guarantees:
    - Each dimension stands alone
    - No aggregation
    - Downstream combination is FORBIDDEN here
    """

    @staticmethod
    def generate(
        *,
        target_property_id: str,
        comparable_property_id: str,
        geo_distance_m: Optional[float],
        land_area_ratio: Optional[float],
        building_area_ratio: Optional[float],
        year_built_diff: Optional[int],
        floor_count_diff: Optional[int],
        same_asset_type: bool,
        same_administrative_area: bool,
    ) -> AffinitySignal:
        """
        Produce bounded, interpretable affinity signals.

        All scales are FIXED & GOVERNANCE-APPROVED.
        """

        affinities: Dict[str, Optional[float]] = {}

        # ------------------------------------------------------------
        # Geographic affinity (distance-based)
        # ------------------------------------------------------------
        affinities["geo_affinity"] = _bounded_inverse_distance(
            geo_distance_m,
            scale=1000.0  # 1km descriptive scale (NOT a rule)
        )

        # ------------------------------------------------------------
        # Size affinities
        # ------------------------------------------------------------
        affinities["land_area_affinity"] = _bounded_ratio_affinity(
            land_area_ratio
        )
        affinities["building_area_affinity"] = _bounded_ratio_affinity(
            building_area_ratio
        )

        # ------------------------------------------------------------
        # Temporal / structural affinities
        # ------------------------------------------------------------
        affinities["year_built_affinity"] = _bounded_difference_affinity(
            year_built_diff,
            scale=10.0  # years (descriptive only)
        )

        affinities["floor_count_affinity"] = _bounded_difference_affinity(
            floor_count_diff,
            scale=3.0
        )

        # ------------------------------------------------------------
        # Categorical consistency (binary, NOT numeric weight)
        # ------------------------------------------------------------
        affinities["asset_type_match"] = 1.0 if same_asset_type else 0.0
        affinities["administrative_area_match"] = (
            1.0 if same_administrative_area else 0.0
        )

        affinity_hash = _hash_affinity(affinities)

        return AffinitySignal(
            target_property_id=target_property_id,
            comparable_property_id=comparable_property_id,
            affinities=affinities,
            affinity_hash=affinity_hash,
        )


# -------------------------------------------------------------------
# Batch Helper (STRICTLY NO SELECTION)
# -------------------------------------------------------------------

def generate_affinity_set(
    inputs: List[Dict[str, Any]]
) -> List[AffinitySignal]:
    """
    Generate affinity signals for a batch of comparables.

    IMPORTANT:
    - Input must already be prepared (no inference here).
    - This function does NOT filter, sort, or rank.
    """

    results: List[AffinitySignal] = []

    for item in inputs:
        results.append(
            ComparableAffinityGenerator.generate(**item)
        )

    return results
