# model/ensemble/outlier_suppressor.py

from typing import List, Dict, Any
from dataclasses import dataclass
import hashlib
import statistics


class OutlierSuppressorError(Exception):
    """Raised when outlier suppression cannot be safely executed."""
    pass


@dataclass(frozen=True)
class SuppressedOutput:
    """
    Descriptive, NON-DECISIONAL output.

    suppressed_values:
        - List of numeric model outputs after suppression
        - Original count preserved
        - No value invented or deleted

    suppression_metadata:
        - Descriptive explanation only
    """
    suppressed_values: List[float]
    suppression_metadata: Dict[str, Any]
    input_hash: str
    model_version: str


class OutlierSuppressor:
    """
    Outlier Suppressor – GOVERNANCE SAFE

    Role:
    - Reduce influence of extreme model outputs
    - Preserve dispersion & transparency

    Forbidden:
    - Removing models
    - Replacing with synthetic values
    - Market-based adjustment
    - Learning or adaptive behavior
    """

    MODEL_VERSION = "outlier_suppressor_v1.0.0"

    # Governance-approved static parameters
    IQR_MULTIPLIER = 1.5

    def _hash_inputs(self, values: List[float]) -> str:
        serialized = repr(values).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _validate_inputs(self, values: List[float]) -> None:
        if not isinstance(values, list):
            raise OutlierSuppressorError("Input must be a list of numeric values")

        if len(values) < 3:
            raise OutlierSuppressorError(
                "Outlier suppression requires at least 3 model outputs"
            )

        for v in values:
            if not isinstance(v, (int, float)):
                raise OutlierSuppressorError("All model outputs must be numeric")

    def suppress(self, model_outputs: List[float]) -> SuppressedOutput:
        """
        Apply IQR-based outlier suppression.

        Method:
        - Compute Q1, Q3
        - Define lower / upper bounds
        - Clamp extreme values to bounds (NOT removal)

        This preserves:
        - Count of models
        - Transparency
        - Dispersion visibility
        """
        self._validate_inputs(model_outputs)

        sorted_vals = sorted(model_outputs)

        q1 = statistics.quantiles(sorted_vals, n=4)[0]
        q3 = statistics.quantiles(sorted_vals, n=4)[2]
        iqr = q3 - q1

        lower_bound = q1 - self.IQR_MULTIPLIER * iqr
        upper_bound = q3 + self.IQR_MULTIPLIER * iqr

        suppressed = []
        suppressed_count = 0

        for v in model_outputs:
            if v < lower_bound:
                suppressed.append(lower_bound)
                suppressed_count += 1
            elif v > upper_bound:
                suppressed.append(upper_bound)
                suppressed_count += 1
            else:
                suppressed.append(v)

        metadata = {
            "method": "IQR_CLAMPING",
            "iqr_multiplier": self.IQR_MULTIPLIER,
            "q1": q1,
            "q3": q3,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "suppressed_value_count": suppressed_count,
            "original_value_count": len(model_outputs),
            "note": (
                "Outliers were clamped, not removed. "
                "This process does not imply correctness or incorrectness of any model."
            )
        }

        return SuppressedOutput(
            suppressed_values=suppressed,
            suppression_metadata=metadata,
            input_hash=self._hash_inputs(model_outputs),
            model_version=self.MODEL_VERSION
        )
