# model/tier_models/tier_regression_high.py

from typing import Dict, Any
from dataclasses import dataclass
import hashlib


class TierRegressionError(Exception):
    """Raised when high-tier regression cannot be safely executed."""
    pass


@dataclass(frozen=True)
class TierHighRegressionResult:
    """
    Descriptive, NON-DECISIONAL output.

    escalation_intensity_score:
        - Bounded [0.0, 1.0]
        - Higher = stronger escalation / senior review needed
        - NOT confidence
        - NOT approval or rejection
        - NOT valuation-related
    """
    escalation_intensity_score: float
    input_hash: str
    model_version: str


class TierHighRegression:
    """
    Tier High Regression – GOVERNANCE CRITICAL

    Role:
    - Aggregate severe risk & integrity signals
    - Produce escalation-intensity indicator ONLY

    Explicitly forbidden:
    - Price inference
    - Approval / rejection
    - Confidence estimation
    - Any adaptive or learning behavior
    """

    MODEL_VERSION = "tier_high_regression_v1.0.0"

    # Static, governance-approved coefficients
    # Coefficients reflect ESCALATION INTENSITY ONLY.
    COEFFICIENTS = {
        "legal_contradiction_count": 0.8,        # strong legal ambiguity
        "ownership_ambiguity_flag": 0.9,         # ownership uncertainty
        "fraud_signal_severity": 0.7,             # fraud-related signals (descriptive)
        "data_incompleteness_ratio": 0.6,         # missing critical data
        "geo_inconsistency_score": 0.5,           # location mismatch signals
        "market_extreme_volatility": 0.4          # stressed market context
    }

    # High-tier assumes baseline escalation expectation
    INTERCEPT = 0.75

    OUTPUT_MIN = 0.0
    OUTPUT_MAX = 1.0

    REQUIRED_FIELDS = set(COEFFICIENTS.keys())

    def _hash_inputs(self, inputs: Dict[str, Any]) -> str:
        """
        Deterministic input hash for audit, dispute, and reproducibility.
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
                f"Missing required signals for tier high regression: {sorted(missing)}"
            )

    @staticmethod
    def _clip(value: float, min_v: float, max_v: float) -> float:
        return max(min_v, min(max_v, value))

    def score(self, signals: Dict[str, Any]) -> TierHighRegressionResult:
        """
        Compute descriptive escalation intensity score.

        Inputs MUST NOT include:
        - price
        - valuation outputs
        - confidence metrics
        - approval hints
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

        return TierHighRegressionResult(
            escalation_intensity_score=bounded_score,
            input_hash=self._hash_inputs(signals),
            model_version=self.MODEL_VERSION,
        )
