# Module: listing_intelligence/trust_scoring/trust_model.py
# Part of Advanced AVM System
"""
Trust Model Projection (Non-Decisive)
------------------------------------

Role:
- Project a descriptive trust score from TrustFeatureSet
- Serve as an interpretable signal for downstream systems
- No decision, no gating, no workflow control

Governance:
- Static model
- Deterministic computation
- Non-authoritative
- Outside valuation & approval logic

Compliant with:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – TRUST SCORING
"""

from dataclasses import dataclass
from typing import Dict, Any
import hashlib
import json


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class TrustScoreProjection:
    trust_score: float              # descriptive only (0.0 – 1.0)
    contributing_features: Dict[str, float]
    model_id: str
    model_version: str
    projection_hash: str


# =========================
# Static Model Parameters
# =========================

MODEL_ID = "trust_model_static_linear"
MODEL_VERSION = "v1.0.0-GOVERNANCE_LOCKED"

# Governance-approved static weights
STATIC_WEIGHTS: Dict[str, float] = {
    "verification_review_ratio": -0.35,
    "content_high_severity_count": -0.25,
    "content_medium_severity_count": -0.10,
    "avg_ai_image_probability": -0.20,
    "max_ai_image_probability": -0.30,
}


# =========================
# Utility Functions
# =========================

def compute_projection_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for audit & lineage.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def clamp(value: float, min_v: float = 0.0, max_v: float = 1.0) -> float:
    return max(min_v, min(value, max_v))


# =========================
# Core Trust Model
# =========================

def project_trust_score(
    trust_features: Dict[str, Any]
) -> TrustScoreProjection:
    """
    Generate descriptive trust score projection.

    Input (Read-only):
    - trust_features: TrustFeatureSet.features

    Output:
    - TrustScoreProjection (non-decisive)
    """

    base_score = 1.0
    contributions: Dict[str, float] = {}

    for feature, weight in STATIC_WEIGHTS.items():
        value = trust_features.get(feature)

        # Ignore missing or non-numeric features
        if value is None or not isinstance(value, (int, float)):
            continue

        contribution = round(weight * float(value), 4)
        contributions[feature] = contribution
        base_score += contribution

    trust_score = round(clamp(base_score), 4)

    payload = {
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "trust_score": trust_score,
        "contributing_features": contributions,
    }

    return TrustScoreProjection(
        trust_score=trust_score,
        contributing_features=contributions,
        model_id=MODEL_ID,
        model_version=MODEL_VERSION,
        projection_hash=compute_projection_hash(payload),
    )

