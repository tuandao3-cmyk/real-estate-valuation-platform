# model/tier_models/tier_regression_low.py

from typing import Dict, Any
from dataclasses import dataclass
import hashlib


class TierRegressionError(Exception):
    """Raised when low-tier regression cannot be safely executed."""
    pass


@dataclass(frozen=True)
class TierLowRegressionResult:
    """
    Descriptive, NON-DECISIONAL output.

    review_effort_score:
        - Bounded [0.0, 1.0]
        - Higher = more human review effort suggested
        - NOT confidence
        - NOT approval signal
        - NOT price-related
    """
    review_effort_score: float
    input_hash: str
    model_version: str


class TierLowRegression:
    """
    Tier Low Regression – GOVERNANCE SAFE

    Role:
    - Produce a bounded, linear descriptive score
    - Support workflow intensity for low-risk tiers

    Forbidden:
    - Price inference
    - Approval / rejection
    - Confidence estimation
    - Learning / adaptation
    """

    MODEL_VERSION = "tier_low_regression_v1.0.0"

    # Static, policy-approved coefficients (NON-OPTIMIZED)
    # These coefficients DO NOT come from outcome fitting.
    COEFFICIENTS = {
        "data_completeness_score": -0.6,     # more complete → less effort
        "legal_disclosure_flag_count": 0.4,  # more flags → more effort
        "image_quality_score": -0.3,         # better images → less effort
        "drift_indicator": 0.5               # drift present → more effort
    }

    INTERCEPT = 0.5

    OUTPUT_MIN = 0.0
    OUTPUT_MAX = 1.0

    REQUIRED_FIELDS = set(COEFFICIENTS.keys())

    def _hash_inputs(self, inputs: Dict[str, Any]) -> str:
        serialized = repr(sorted(inputs.items())).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _validate_inputs(self, signals: Dict[str, Any]) -> None:
        missing = self.REQUIRED_FIELDS - signals.keys()
        if missing:
            raise TierRegressionError(
                f"Missing required signals for tier low regression: {sorted(missing)}"
            )

    def _clip(self, value: float) -> float:
        return max(self.OUTPUT_MIN, min(self.OUTPUT_MAX, value))

    def score(self, signals: Dict[str, Any]) -> TierLowRegressionResult:
        """
        Compute descriptive review effort score.

        signals MUST NOT contain:
        - price
        - confidence
        - approval
        - model outputs from AVM
        """
        self._validate_inputs(signals)

        linear_sum = self.INTERCEPT

        for feature, coef in self.COEFFICIENTS.items():
            linear_sum += coef * float(signals[feature])

        bounded_score = self._clip(linear_sum)

        return TierLowRegressionResult(
            review_effort_score=bounded_score,
            input_hash=self._hash_inputs(signals),
            model_version=self.MODEL_VERSION,
        )
