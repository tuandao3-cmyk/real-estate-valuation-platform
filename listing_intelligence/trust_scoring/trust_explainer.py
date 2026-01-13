# Module: listing_intelligence/trust_scoring/trust_explainer.py
# Part of Advanced AVM System
"""
Trust Explainer (Human-Readable, Non-Decisive)
----------------------------------------------

Role:
- Generate descriptive explanation for trust-related artifacts
- Help human reviewers understand signals & projections
- No judgment, no recommendation, no workflow impact

Governance:
- Explanation-only
- Deterministic text assembly
- No inference or decision logic
- Safe for audit & regulator review

Compliant with:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – TRUST SCORING
"""

from dataclasses import dataclass
from typing import Dict, Any, List
import hashlib
import json


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class TrustExplanation:
    summary: str
    feature_highlights: List[str]
    score_context: str
    calibration_context: str
    limitations: List[str]
    explanation_hash: str


# =========================
# Utility
# =========================

def compute_explanation_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic hash for audit & reproducibility.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# =========================
# Core Explainer
# =========================

def explain_trust_projection(
    trust_features: Dict[str, Any],
    trust_score: float,
    calibrated_band: str,
    model_id: str,
    model_version: str,
    calibration_version: str,
) -> TrustExplanation:
    """
    Generate human-readable explanation for trust artifacts.

    Inputs (Read-only):
    - trust_features: descriptive feature set
    - trust_score: raw trust score projection (0.0 – 1.0)
    - calibrated_band: descriptive band (VERY_LOW / LOW / MEDIUM / HIGH)
    - model_id, model_version: metadata only
    - calibration_version: metadata only

    Output:
    - TrustExplanation (explanation-only)
    """

    # -------------------------
    # Summary
    # -------------------------
    summary = (
        "The trust indicators for this listing are derived from "
        "verification consistency checks, content integrity signals, "
        "and image forensics awareness. "
        "All indicators are descriptive and non-decisive."
    )

    # -------------------------
    # Feature Highlights
    # -------------------------
    highlights: List[str] = []

    if trust_features.get("verification_review_count", 0) > 0:
        highlights.append(
            f"{trust_features.get('verification_review_count')} verification signal(s) "
            "require human review or clarification."
        )

    if trust_features.get("content_high_severity_count", 0) > 0:
        highlights.append(
            f"{trust_features.get('content_high_severity_count')} content signal(s) "
            "were flagged with high descriptive severity."
        )

    if trust_features.get("max_ai_image_probability") is not None:
        highlights.append(
            "Some images show a measurable probability of being "
            "synthetic or AI-generated based on static detection models."
        )

    if not highlights:
        highlights.append(
            "No notable trust-related irregularities were highlighted "
            "by the descriptive signals."
        )

    # -------------------------
    # Score Context
    # -------------------------
    score_context = (
        f"The trust score projection is {round(trust_score, 4)} on a normalized scale "
        f"from 0.0 to 1.0. This value is produced by a static, governance-locked model "
        f"({model_id}, {model_version}) and is provided for reference only."
    )

    # -------------------------
    # Calibration Context
    # -------------------------
    calibration_context = (
        f"For readability, the score is mapped to the descriptive band "
        f"'{calibrated_band}' using calibration version {calibration_version}. "
        "This band does not represent approval, rejection, or trustworthiness."
    )

    # -------------------------
    # Limitations
    # -------------------------
    limitations = [
        "Trust indicators do not confirm or deny fraud.",
        "Trust score projections are not approval or rejection criteria.",
        "Human judgment is required to interpret all trust-related information.",
        "All trust artifacts are independent from valuation and pricing logic.",
    ]

    payload = {
        "summary": summary,
        "feature_highlights": highlights,
        "score_context": score_context,
        "calibration_context": calibration_context,
        "limitations": limitations,
    }

    return TrustExplanation(
        summary=summary,
        feature_highlights=highlights,
        score_context=score_context,
        calibration_context=calibration_context,
        limitations=limitations,
        explanation_hash=compute_explanation_hash(payload),
    )

