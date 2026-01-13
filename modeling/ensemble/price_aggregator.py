# model/ensemble/price_aggregator.py

from typing import List, Dict, Any
from dataclasses import dataclass
import hashlib


class PriceAggregationError(Exception):
    """Raised when aggregation violates governance constraints."""
    pass


@dataclass(frozen=True)
class PriceAggregationResult:
    """
    NON-DECISIONAL OUTPUT

    aggregated_price:
        - Weighted arithmetic aggregation
        - Indicative signal only

    components:
        - Raw model outputs (unchanged)
        - Corresponding weights

    metadata:
        - Method description
        - Explicit non-decision disclaimer
    """
    aggregated_price: float
    components: List[Dict[str, float]]
    metadata: Dict[str, Any]
    input_hash: str
    model_version: str


class PriceAggregator:
    """
    Price Aggregator – GOVERNANCE CRITICAL

    Role:
    - Aggregate multiple price signals mechanically
    - Preserve traceability and transparency

    Absolute Prohibitions:
    - No filtering / suppression
    - No correction
    - No normalization by market
    - No confidence generation
    - No approval suggestion
    """

    MODEL_VERSION = "price_aggregator_v1.0.0"

    def _hash_inputs(self, prices: List[float], weights: List[float]) -> str:
        serialized = repr((prices, weights)).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _validate_inputs(self, prices: List[float], weights: List[float]) -> None:
        if not isinstance(prices, list) or not isinstance(weights, list):
            raise PriceAggregationError("Prices and weights must be lists")

        if len(prices) == 0:
            raise PriceAggregationError("No price signals provided")

        if len(prices) != len(weights):
            raise PriceAggregationError("Prices and weights length mismatch")

        for p in prices:
            if not isinstance(p, (int, float)):
                raise PriceAggregationError("All prices must be numeric")
            if p <= 0:
                raise PriceAggregationError("Prices must be positive numbers")

        for w in weights:
            if not isinstance(w, (int, float)):
                raise PriceAggregationError("All weights must be numeric")
            if w < 0:
                raise PriceAggregationError("Weights must be non-negative")

        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 1e-6:
            raise PriceAggregationError(
                "Weights must sum to exactly 1.0"
            )

    def aggregate(
        self,
        prices: List[float],
        weights: List[float],
        source_labels: List[str] = None
    ) -> PriceAggregationResult:
        """
        Deterministic weighted aggregation.

        Interpretation rules:
        - Result is NOT market value
        - Result is NOT final price
        - Result requires human judgment
        """
        self._validate_inputs(prices, weights)

        aggregated_price = sum(
            p * w for p, w in zip(prices, weights)
        )

        components = []
        for idx, (p, w) in enumerate(zip(prices, weights)):
            label = (
                source_labels[idx]
                if source_labels and idx < len(source_labels)
                else f"model_{idx}"
            )
            components.append({
                "source": label,
                "price": p,
                "weight": w
            })

        metadata = {
            "aggregation_method": "WEIGHTED_ARITHMETIC_MEAN",
            "price_count": len(prices),
            "disclaimer": (
                "Aggregated price is an indicative ensemble signal only. "
                "It does not represent market value, approval, or valuation decision. "
                "Final responsibility remains with human appraiser."
            )
        }

        return PriceAggregationResult(
            aggregated_price=aggregated_price,
            components=components,
            metadata=metadata,
            input_hash=self._hash_inputs(prices, weights),
            model_version=self.MODEL_VERSION
        )
