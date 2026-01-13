# Module: listing_intelligence/trust_scoring/trust_features.py
# Part of Advanced AVM System
"""
Trust Feature Extraction (Listing Intelligence)
-----------------------------------------------

Role:
- Extract descriptive, low-level trust-related features
  from listing verification & content signals.
- Provide normalized, explainable feature values.

Governance:
- Feature-only (non-decisive)
- No trust score computation
- No thresholds / classification
- No workflow or valuation impact

Compliant with:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import hashlib
import json


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class TrustFeatureSet:
    """
    Canonical container for trust-related features.
    Values are descriptive & normalized.
    """
    features: Dict[str, Any]
    signal_sources: List[str]
    feature_hash: str


# =========================
# Utility Functions
# =========================

def compute_feature_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for feature lineage & audit.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# =========================
# Core Feature Extractor
# =========================

def extract_trust_features(
    verification_signals: List[Dict[str, Any]],
    content_signals: List[Dict[str, Any]],
    image_forensics_signals: List[Dict[str, Any]],
) -> TrustFeatureSet:
    """
    Extract descriptive trust-related features from upstream signals.

    Inputs (Read-only):
    - verification_signals: outputs from listing_intelligence.verification.*
    - content_signals: outputs from listing_intelligence.content_analysis.*
    - image_forensics_signals: outputs from listing_intelligence.image_forensics.*

    Output:
    - TrustFeatureSet (feature-only, non-decisive)
    """

    features: Dict[str, Any] = {}
    signal_sources: List[str] = []

    # -------------------------
    # Verification Consistency
    # -------------------------
    verification_review_flags = [
        s for s in verification_signals
        if s.get("status") in ("UNCERTAIN", "REVIEW_REQUIRED")
    ]

    features["verification_review_count"] = len(verification_review_flags)
    features["verification_signal_count"] = len(verification_signals)

    if verification_signals:
        features["verification_review_ratio"] = round(
            len(verification_review_flags) / len(verification_signals), 4
        )
    else:
        features["verification_review_ratio"] = 0.0

    signal_sources.append("verification")

    # -------------------------
    # Content Integrity Signals
    # -------------------------
    content_severity_levels = [
        s.get("severity", "LOW") for s in content_signals
    ]

    features["content_signal_count"] = len(content_signals)
    features["content_high_severity_count"] = content_severity_levels.count("HIGH")
    features["content_medium_severity_count"] = content_severity_levels.count("MEDIUM")

    signal_sources.append("content_analysis")

    # -------------------------
    # Image Forensics Awareness
    # -------------------------
    ai_image_probs = [
        s.get("ai_image_probability")
        for s in image_forensics_signals
        if s.get("ai_image_probability") is not None
    ]

    if ai_image_probs:
        features["avg_ai_image_probability"] = round(
            sum(ai_image_probs) / len(ai_image_probs), 4
        )
        features["max_ai_image_probability"] = round(
            max(ai_image_probs), 4
        )
    else:
        features["avg_ai_image_probability"] = None
        features["max_ai_image_probability"] = None

    features["image_signal_count"] = len(image_forensics_signals)

    signal_sources.append("image_forensics")

    # -------------------------
    # Finalize Feature Set
    # -------------------------
    payload = {
        "features": features,
        "signal_sources": sorted(set(signal_sources)),
    }

    return TrustFeatureSet(
        features=features,
        signal_sources=sorted(set(signal_sources)),
        feature_hash=compute_feature_hash(payload),
    )

