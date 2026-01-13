# model/tier_models/tier_regression_mid.py

from typing import Dict, Any
from dataclasses import dataclass
import hashlib


class TierRegressionError(Exception):
    """Raised when mid-tier regression cannot be safely executed."""
    pass


@dataclass(frozen=True)
class TierMidRegressionResult:
    """
    Descriptive, NON-DECISIONAL output.

    review_intensity_score:
        - Bounded [0.0, 1.0]
        - Higher = more intensive human review suggested
        - NOT confidence
        - NOT approval signal
        - NOT valuation-related
    """
    review_intensity_score: float
    input_hash: str
    model_version: str


class TierMidRegression:
    """
    Tier Mid Regression – GOVERNANCE SAFE

    Role:
    - Aggregate descriptive risk & integrity signals
    - Produce a bounded review-intensity indicator

    Explicitly forbidden:
    - Price inference
    - Approval / rejection
    - Confidence estimation
    - Learning or adaptive behavior
    """

    MODEL_VERSION = "tier_mid_regression_v1.0.0"

    # Static, governance-approved coefficients
    # Coefficients reflect REVIEW INTENSITY ONLY, not risk or value.
    COEFFICIENTS = {
        "data_completeness_score": -0.4,        # better data → less review
        "legal_disclosure_flag_count": 0.6,     # legal ambiguity → more review
        "content_consistency_issues": 0.5,      # mismatch signals → more review
        "image_condition_indicator": 0.4,       # uncertain condition → more review
        "market_context_volatility": 0.3        # volatile context → caution
    }

    INTERCEPT = 0.6

    OUTPUT_MIN = 0.0
    OUTPUT_MAX = 1.0

    REQUIRED_FIELDS = set(COEFFICIENTS.keys())

    def _hash_inputs(self, inputs: Dict[str, Any]) -> str:
        """
        Deterministic hash for audit & reproducibility.
        """
        serialized = repr(sorted(inputs.items())).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _validate_inputs(self, signals: Dict[str, Any]) -> None:
        """
        Fail-fast validation.
        """
        missing = self.REQUIRED_FIELDS - signals.keys()
        if missing:
            raise TierRegressionError(
                f"Missing required signals for tier mid regression: {sorted(missing)}"
            )

    @staticmethod
    def _clip(value: float, min_v: float, max_v: float) -> float:
        return max(min_v, min(max_v, value))

    def score(self, signals: Dict[str, Any]) -> TierMidRegressionResult:
        """
        Compute descriptive review intensity score.

        Signals MUST NOT include:
        - price
        - valuation outputs
        - confidence
        - approval indicators
        """
        self._validate_inputs(signals)

        linear_sum = self.INTERCEPT

        for feature, coef in self.COEFFICIENTS.items():
            linear_sum += coef * float(signals[feature])

        bounded_score = self._clip(
            linear_sum,
            self.OUTPUT_MIN,
            self.OUTPUT_MAX
        )

        return TierMidRegressionResult(
            review_intensity_score=bounded_score,
            input_hash=self._hash_inputs(signals),
            model_version=self.MODEL_VERSION,
        )
