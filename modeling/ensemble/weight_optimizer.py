# model/ensemble/weight_optimizer.py

from typing import List, Dict, Any
from dataclasses import dataclass
import hashlib
import statistics


class WeightOptimizerError(Exception):
    """Raised when weight assignment violates governance constraints."""
    pass


@dataclass(frozen=True)
class WeightOptimizationResult:
    """
    NON-DECISIONAL, DESCRIPTIVE OUTPUT

    weights:
        - Static weights per model output
        - Sum to 1.0
        - No model removed

    metadata:
        - Explanation of weight logic
        - Statistical descriptors only
    """
    weights: List[float]
    metadata: Dict[str, Any]
    input_hash: str
    model_version: str


class WeightOptimizer:
    """
    Weight Optimizer – GOVERNANCE SAFE

    Role:
    - Assign static weights based on dispersion stability
    - Improve ensemble robustness WITHOUT learning

    Forbidden:
    - Outcome-based optimization
    - Adaptive tuning
    - Price adjustment
    - Model exclusion
    """

    MODEL_VERSION = "weight_optimizer_v1.0.0"

    # Governance-approved static parameters
    MIN_WEIGHT = 0.10
    MAX_WEIGHT = 0.40

    def _hash_inputs(self, values: List[float]) -> str:
        serialized = repr(values).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _validate_inputs(self, values: List[float]) -> None:
        if not isinstance(values, list):
            raise WeightOptimizerError("Model outputs must be a list")

        if len(values) < 2:
            raise WeightOptimizerError(
                "At least two model outputs are required for weighting"
            )

        for v in values:
            if not isinstance(v, (int, float)):
                raise WeightOptimizerError("All model outputs must be numeric")

    def assign_weights(self, model_outputs: List[float]) -> WeightOptimizationResult:
        """
        Assign deterministic weights based on distance to median.

        Logic (STATIC, NON-LEARNING):
        - Median used as neutral anchor (not truth)
        - Models closer to median receive higher weight
        - Bounds enforced to prevent dominance or exclusion

        This does NOT imply correctness of any model.
        """
        self._validate_inputs(model_outputs)

        median_value = statistics.median(model_outputs)

        distances = [
            abs(v - median_value) for v in model_outputs
        ]

        # Avoid division by zero in perfectly identical outputs
        max_distance = max(distances) if max(distances) > 0 else 1.0

        raw_scores = [
            1.0 - (d / max_distance) for d in distances
        ]

        # Enforce static bounds
        bounded_scores = [
            min(max(score, self.MIN_WEIGHT), self.MAX_WEIGHT)
            for score in raw_scores
        ]

        total = sum(bounded_scores)
        if total <= 0:
            raise WeightOptimizerError("Invalid weight normalization state")

        normalized_weights = [
            score / total for score in bounded_scores
        ]

        metadata = {
            "method": "MEDIAN_DISTANCE_WEIGHTING",
            "median_reference": median_value,
            "min_weight": self.MIN_WEIGHT,
            "max_weight": self.MAX_WEIGHT,
            "distance_metric": "ABSOLUTE_DIFFERENCE",
            "note": (
                "Weights reflect statistical proximity, not model quality, "
                "accuracy, or correctness. No learning or outcome feedback involved."
            )
        }

        return WeightOptimizationResult(
            weights=normalized_weights,
            metadata=metadata,
            input_hash=self._hash_inputs(model_outputs),
            model_version=self.MODEL_VERSION
        )
