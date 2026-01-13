# model/ensemble/confidence_estimator.py

from typing import List, Dict, Any
from dataclasses import dataclass
import math
import hashlib


class ConfidenceEstimationError(Exception):
    """Raised when confidence estimation violates governance rules."""
    pass


@dataclass(frozen=True)
class ConfidenceResult:
    """
    NON-DECISIONAL CONFIDENCE OUTPUT

    confidence_score:
        - Bounded [0, 1]
        - Measures agreement + data quality ONLY

    components:
        - Agreement metrics
        - Data quality indicators

    metadata:
        - Explicit disclaimer
        - Method description

    IMPORTANT:
    - Confidence does NOT imply accuracy
    - Confidence does NOT approve valuation
    """
    confidence_score: float
    components: Dict[str, Any]
    metadata: Dict[str, Any]
    input_hash: str
    model_version: str


class ConfidenceEstimator:
    """
    Confidence Estimator – GOVERNANCE CRITICAL

    Role:
    - Quantify agreement and data completeness
    - Provide gating signal for human workflow

    Absolute Prohibitions:
    - No price adjustment
    - No approval / rejection decision
    - No learning / calibration
    - No outcome-based tuning
    """

    MODEL_VERSION = "confidence_estimator_v1.0.0"

    def _hash_inputs(self, prices: List[float], data_quality_flags: Dict[str, bool]) -> str:
        serialized = repr((prices, data_quality_flags)).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _validate_prices(self, prices: List[float]) -> None:
        if not isinstance(prices, list) or len(prices) < 2:
            raise ConfidenceEstimationError(
                "At least two price signals are required to assess agreement"
            )

        for p in prices:
            if not isinstance(p, (int, float)) or p <= 0:
                raise ConfidenceEstimationError(
                    "All price signals must be positive numeric values"
                )

    def _validate_quality_flags(self, flags: Dict[str, bool]) -> None:
        if not isinstance(flags, dict):
            raise ConfidenceEstimationError("Data quality flags must be a dictionary")

        for k, v in flags.items():
            if not isinstance(v, bool):
                raise ConfidenceEstimationError(
                    f"Data quality flag '{k}' must be boolean"
                )

    def _agreement_score(self, prices: List[float]) -> float:
        """
        Agreement proxy based on coefficient of variation (CV).

        Logic:
        - Lower dispersion → higher agreement
        - Purely statistical, no interpretation
        """
        mean_price = sum(prices) / len(prices)
        variance = sum((p - mean_price) ** 2 for p in prices) / len(prices)
        std_dev = math.sqrt(variance)

        if mean_price == 0:
            return 0.0

        cv = std_dev / mean_price

        # Deterministic bounding:
        # CV >= 1.0 → agreement = 0
        # CV <= 0.0 → agreement = 1
        agreement = max(0.0, min(1.0, 1.0 - cv))
        return agreement

    def _data_quality_score(self, flags: Dict[str, bool]) -> float:
        """
        Data quality score = proportion of passed checks.

        No weighting.
        No inference.
        """
        if not flags:
            return 0.0

        passed = sum(1 for v in flags.values() if v)
        return passed / len(flags)

    def estimate(
        self,
        price_signals: List[float],
        data_quality_flags: Dict[str, bool]
    ) -> ConfidenceResult:
        """
        Produce a bounded confidence score for workflow gating.

        Interpretation:
        - Low score → requires human review
        - High score → still requires human accountability
        """
        self._validate_prices(price_signals)
        self._validate_quality_flags(data_quality_flags)

        agreement = self._agreement_score(price_signals)
        data_quality = self._data_quality_score(data_quality_flags)

        # Simple mechanical combination (non-optimized, non-learned)
        confidence_score = (agreement + data_quality) / 2.0

        confidence_score = max(0.0, min(1.0, confidence_score))

        components = {
            "agreement_score": agreement,
            "data_quality_score": data_quality,
            "price_signal_count": len(price_signals),
            "data_quality_flag_count": len(data_quality_flags)
        }

        metadata = {
            "method": "AGREEMENT_PLUS_DATA_QUALITY",
            "disclaimer": (
                "Confidence score reflects model agreement and input data quality only. "
                "It does NOT measure accuracy, does NOT approve valuation, "
                "and must NOT be used as a pricing or decision factor."
            )
        }

        return ConfidenceResult(
            confidence_score=confidence_score,
            components=components,
            metadata=metadata,
            input_hash=self._hash_inputs(price_signals, data_quality_flags),
            model_version=self.MODEL_VERSION
        )
