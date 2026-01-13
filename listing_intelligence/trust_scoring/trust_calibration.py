# Module: listing_intelligence/trust_scoring/trust_calibration.py
# Part of Advanced AVM System
"""
Trust Score Calibration (Descriptive Banding Only)
--------------------------------------------------

Role:
- Calibrate descriptive trust score into interpretive bands
- Improve human readability and consistency
- No decision, no gating, no approval logic

Governance:
- Static calibration
- No learning
- No outcome feedback
- Non-decisive
- Reversible & explainable

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
class TrustCalibrationResult:
    raw_trust_score: float
    calibrated_band: str           # VERY_LOW / LOW / MEDIUM / HIGH
    calibration_version: str
    calibration_hash: str


# =========================
# Static Calibration Config
# =========================

CALIBRATION_VERSION = "v1.0.0-GOVERNANCE_LOCKED"

# Governance-approved descriptive bands
CALIBRATION_BANDS = [
    ("VERY_LOW", 0.0, 0.25),
    ("LOW", 0.25, 0.5),
    ("MEDIUM", 0.5, 0.75),
    ("HIGH", 0.75, 1.01),
]


# =========================
# Utility Functions
# =========================

def compute_calibration_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash for audit & reproducibility.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# =========================
# Core Calibration Logic
# =========================

def calibrate_trust_score(
    trust_score: float
) -> TrustCalibrationResult:
    """
    Calibrate descriptive trust score into interpretive band.

    Input (Read-only):
    - trust_score: float (0.0 – 1.0), from trust_model projection

    Output:
    - TrustCalibrationResult (descriptive only)
    """

    # Defensive clamp (no inference)
    score = min(max(trust_score, 0.0), 1.0)

    calibrated_band = "UNKNOWN"
    for band, lower, upper in CALIBRATION_BANDS:
        if lower <= score < upper:
            calibrated_band = band
            break

    payload = {
        "raw_trust_score": round(score, 4),
        "calibrated_band": calibrated_band,
        "calibration_version": CALIBRATION_VERSION,
    }

    return TrustCalibrationResult(
        raw_trust_score=round(score, 4),
        calibrated_band=calibrated_band,
        calibration_version=CALIBRATION_VERSION,
        calibration_hash=compute_calibration_hash(payload),
    )

