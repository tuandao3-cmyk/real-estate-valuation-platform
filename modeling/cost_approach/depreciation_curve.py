# model/cost_approach/depreciation_curve.py
# ==========================================================
# GOVERNANCE CLASS: NHÓM A – COST APPROACH (DEPRECIATION)
# ROLE: Descriptive Depreciation Curve Generator
# AUTHORITY: NON-DECISIVE / HUMAN-VALIDATED
# ==========================================================
#
# IMPORTANT:
# - This module provides depreciation curves for COST APPROACH ONLY
# - Output is a descriptive depreciation factor (0.0 – 1.0)
# - NO valuation, NO price adjustment, NO market inference
#
# MASTER_SPEC ENFORCEMENT:
# - Deterministic
# - No learning
# - No auto-calibration
# - No override logic
# ==========================================================

from dataclasses import dataclass
from typing import Literal, Dict
import hashlib
import json


DepreciationType = Literal[
    "physical",
    "functional",
    "external"
]


CurveType = Literal[
    "straight_line",
    "age_life",
    "accelerated"
]


@dataclass(frozen=True)
class DepreciationInput:
    """
    Input contract for depreciation calculation.

    NOTE:
    - age_years must come from validated feature pipeline
    - economic_life_years must be human-approved reference
    """
    depreciation_type: DepreciationType
    curve_type: CurveType
    age_years: float
    economic_life_years: float


class DepreciationCurveEngine:
    """
    Static, deterministic depreciation curve engine.

    GOVERNANCE GUARANTEES:
    - Read-only logic
    - No side effects
    - No adaptive behavior
    - No valuation authority
    """

    @staticmethod
    def compute(input_data: DepreciationInput) -> Dict[str, float]:
        """
        Compute descriptive depreciation factor.

        Returns:
            {
                "depreciation_factor": float,   # 0.0 – 1.0
                "remaining_ratio": float        # 0.0 – 1.0
            }

        INTERPRETATION:
        - depreciation_factor: proportion of cost depreciated
        - remaining_ratio: proportion of cost remaining
        """

        DepreciationCurveEngine._validate_input(input_data)

        if input_data.curve_type == "straight_line":
            factor = DepreciationCurveEngine._straight_line(
                input_data.age_years,
                input_data.economic_life_years
            )

        elif input_data.curve_type == "age_life":
            factor = DepreciationCurveEngine._age_life(
                input_data.age_years,
                input_data.economic_life_years
            )

        elif input_data.curve_type == "accelerated":
            factor = DepreciationCurveEngine._accelerated(
                input_data.age_years,
                input_data.economic_life_years
            )

        else:
            raise ValueError("Unsupported depreciation curve type")

        remaining = max(0.0, 1.0 - factor)

        return {
            "depreciation_factor": round(factor, 6),
            "remaining_ratio": round(remaining, 6)
        }

    # --------------------------------------------------
    # Curve implementations (DESCRIPTIVE ONLY)
    # --------------------------------------------------

    @staticmethod
    def _straight_line(age: float, life: float) -> float:
        """
        Straight-line depreciation.

        Logic:
        depreciation = age / life
        """
        return min(max(age / life, 0.0), 1.0)

    @staticmethod
    def _age_life(age: float, life: float) -> float:
        """
        Age-life method (common in appraisal practice).

        Identical numeric form to straight-line,
        but semantically tied to economic life concept.
        """
        return min(max(age / life, 0.0), 1.0)

    @staticmethod
    def _accelerated(age: float, life: float) -> float:
        """
        Accelerated depreciation curve.

        GOVERNANCE NOTE:
        - Fixed exponent
        - No calibration
        - No outcome-based tuning
        """
        exponent = 1.5
        ratio = min(max(age / life, 0.0), 1.0)
        return min(ratio ** exponent, 1.0)

    # --------------------------------------------------
    # Validation & Audit Support
    # --------------------------------------------------

    @staticmethod
    def _validate_input(input_data: DepreciationInput) -> None:
        """
        Hard validation – fail fast.
        """
        if input_data.age_years < 0:
            raise ValueError("age_years must be non-negative")

        if input_data.economic_life_years <= 0:
            raise ValueError("economic_life_years must be > 0")

        if input_data.age_years > input_data.economic_life_years * 2:
            # Governance guardrail: unrealistic input
            raise ValueError("age_years exceeds reasonable economic life range")

    @staticmethod
    def compute_audit_hash(input_data: DepreciationInput) -> str:
        """
        Generate deterministic hash for audit & replay.
        """
        payload = {
            "depreciation_type": input_data.depreciation_type,
            "curve_type": input_data.curve_type,
            "age_years": input_data.age_years,
            "economic_life_years": input_data.economic_life_years
        }

        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
