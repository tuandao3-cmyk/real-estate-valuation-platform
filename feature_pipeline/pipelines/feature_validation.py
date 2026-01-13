"""
feature_pipeline/pipelines/feature_validation.py

ROLE (MASTER_SPEC COMPLIANT)
---------------------------
Feature Validation Pipeline.

This module validates feature outputs BEFORE they are consumed
by downstream components (models, rules, risk, ensemble).

ABSOLUTE PROHIBITIONS
---------------------
- No feature generation
- No feature transformation
- No ML / LLM
- No valuation logic
- No decision making

This is a GOVERNANCE & QUALITY GATE ONLY.
"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Optional


class FeatureValidationError(Exception):
    """Raised when a feature fails validation."""


class FeatureValidator:
    """
    Deterministic feature validator.

    Validation Dimensions
    ---------------------
    - Schema presence
    - Type safety
    - NaN / Inf protection
    - Range sanity (optional)
    - Metadata completeness
    """

    def __init__(
        self,
        required_fields: Optional[List[str]] = None,
        numeric_ranges: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> None:
        """
        Parameters
        ----------
        required_fields : Optional[List[str]]
            List of mandatory feature fields.

        numeric_ranges : Optional[Dict[str, Dict[str, float]]]
            Optional numeric constraints:
            {
                "feature_name": {
                    "min": float,
                    "max": float
                }
            }
        """
        self.required_fields = required_fields or []
        self.numeric_ranges = numeric_ranges or {}

    def _validate_required_fields(
        self,
        feature: Dict[str, Any],
    ) -> None:
        for field in self.required_fields:
            if field not in feature:
                raise FeatureValidationError(
                    f"Missing required field: {field}"
                )

    def _validate_numeric_value(
        self,
        name: str,
        value: Any,
    ) -> None:
        if not isinstance(value, (int, float)):
            raise FeatureValidationError(
                f"Feature '{name}' must be numeric, "
                f"got {type(value).__name__}"
            )

        if math.isnan(value) or math.isinf(value):
            raise FeatureValidationError(
                f"Feature '{name}' contains NaN or Inf"
            )

    def _validate_numeric_ranges(
        self,
        feature: Dict[str, Any],
    ) -> None:
        for name, constraints in self.numeric_ranges.items():
            if name not in feature:
                continue

            value = feature[name]
            self._validate_numeric_value(name, value)

            min_v = constraints.get("min")
            max_v = constraints.get("max")

            if min_v is not None and value < min_v:
                raise FeatureValidationError(
                    f"Feature '{name}' below minimum: {value} < {min_v}"
                )

            if max_v is not None and value > max_v:
                raise FeatureValidationError(
                    f"Feature '{name}' above maximum: {value} > {max_v}"
                )

    def _validate_metadata(
        self,
        feature: Dict[str, Any],
    ) -> None:
        """
        Metadata is mandatory for auditability.

        Expected (minimum):
        - method
        - disclaimer
        """
        for meta_key in ("method", "disclaimer"):
            if meta_key not in feature:
                raise FeatureValidationError(
                    f"Missing metadata field: {meta_key}"
                )

            if not isinstance(feature[meta_key], str):
                raise FeatureValidationError(
                    f"Metadata field '{meta_key}' must be string"
                )

    def validate(
        self,
        feature: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate a single feature dictionary.

        Parameters
        ----------
        feature : Dict[str, Any]
            Feature output from feature_pipeline.

        Returns
        -------
        Dict[str, Any]
            The SAME feature dict if valid.

        Raises
        ------
        FeatureValidationError
            If any validation rule is violated.
        """
        if not isinstance(feature, dict):
            raise FeatureValidationError(
                f"Feature must be dict, got {type(feature).__name__}"
            )

        self._validate_required_fields(feature)
        self._validate_numeric_ranges(feature)
        self._validate_metadata(feature)

        return feature


def validate_features(
    features: Dict[str, Dict[str, Any]],
    required_fields: Optional[List[str]] = None,
    numeric_ranges: Optional[Dict[str, Dict[str, float]]] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Batch validation for multiple features.

    SAFE FOR
    --------
    - Feature pipeline orchestration
    - Audit replay
    - Governance enforcement

    NOT ALLOWED FOR
    ---------------
    - Feature inference
    - Aggregation
    - Model input reshaping
    """
    validator = FeatureValidator(
        required_fields=required_fields,
        numeric_ranges=numeric_ranges,
    )

    validated: Dict[str, Dict[str, Any]] = {}

    for feature_name, feature_data in features.items():
        try:
            validated[feature_name] = validator.validate(feature_data)
        except FeatureValidationError as exc:
            raise FeatureValidationError(
                f"Feature '{feature_name}' failed validation: {exc}"
            ) from exc

    return validated
