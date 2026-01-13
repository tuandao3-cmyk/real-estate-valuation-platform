"""
AI-Generated Image Probability Signal
------------------------------------

Role:
- Provide descriptive awareness signal indicating the likelihood
  that an image is AI-generated or synthetic.

Governance Principles:
- Signal-only
- Non-decisive
- Deterministic wrapper
- No fraud or intent conclusion
- No valuation, approval, or workflow impact

Compliant with:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from dataclasses import dataclass
from typing import Dict, Any
import hashlib
import json


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class AIGeneratedImageSignal:
    ai_image_probability: float  # descriptive, 0.0 – 1.0
    confidence_level: str        # LOW / MEDIUM / HIGH
    signal_hash: str


# =========================
# Utility Functions
# =========================

def compute_signal_hash(payload: Dict[str, Any]) -> str:
    """
    Compute deterministic SHA-256 hash for signal lineage & audit.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def map_confidence_level(probability: float) -> str:
    """
    Map probability to descriptive confidence level.
    Deterministic, governance-defined.
    """
    if probability < 0.3:
        return "LOW"
    if probability < 0.7:
        return "MEDIUM"
    return "HIGH"


# =========================
# Core Signal Generator
# =========================

def generate_ai_generated_image_signal(
    model_output_probability: float,
    model_identifier: str,
    model_version: str,
) -> AIGeneratedImageSignal:
    """
    Generate AI-generated image awareness signal.

    Inputs (Read-only):
    - model_output_probability: probability score from a fixed,
      pre-trained external detection model (0.0 – 1.0)
    - model_identifier: static model name (for audit metadata)
    - model_version: static version string

    Output:
    - AIGeneratedImageSignal (signal-only)
    """

    # Clamp for defensive determinism (no inference)
    probability = min(max(model_output_probability, 0.0), 1.0)

    confidence_level = map_confidence_level(probability)

    payload = {
        "model_identifier": model_identifier,
        "model_version": model_version,
        "ai_image_probability": round(probability, 4),
        "confidence_level": confidence_level,
    }

    return AIGeneratedImageSignal(
        ai_image_probability=round(probability, 4),
        confidence_level=confidence_level,
        signal_hash=compute_signal_hash(payload),
    )
