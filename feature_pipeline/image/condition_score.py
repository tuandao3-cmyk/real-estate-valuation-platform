# Module: feature_pipeline/image/condition_score.py
# Part of Advanced AVM System

"""
feature_pipeline/image/condition_score.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Image Technical Condition Proxy (Feature Layer).

This module computes a DESCRIPTIVE, NON-DECISIVE
condition proxy from low-level image quality metrics.

ABSOLUTE PROHIBITIONS
---------------------
- No aesthetic judgment
- No property condition inference
- No valuation implication
- No trust / risk scoring
- No workflow control
- No ML / LLM usage

IMPORTANT
---------
"condition_score" is a TECHNICAL AGGREGATE ONLY.
It does NOT represent real asset condition.
"""

from __future__ import annotations

from typing import Dict, Any


class ConditionScoreError(Exception):
    """Raised when condition score computation fails."""


class ImageConditionScorer:
    """
    Deterministic image condition proxy calculator.

    Inputs
    ------
    Pre-computed image quality metrics ONLY:
    - brightness_mean
    - contrast_stddev
    - sharpness_proxy
    - width
    - height

    Governance
    ----------
    - Static formula
    - No learning
    - No adaptive thresholds
    - Purely descriptive
    """

    def __init__(
        self,
        brightness_range: tuple[float, float] = (0.0, 255.0),
        contrast_range: tuple[float, float] = (0.0, 128.0),
        sharpness_range: tuple[float, float] = (0.0, 128.0),
    ) -> None:
        self.brightness_range = brightness_range
        self.contrast_range = contrast_range
        self.sharpness_range = sharpness_range

    @staticmethod
    def _normalize(
        value: float,
        min_val: float,
        max_val: float,
    ) -> float:
        """
        Normalize value into [0, 1].

        Governance:
        -----------
        - Hard clamp
        - Deterministic
        """
        if max_val <= min_val:
            return 0.0

        v = max(min(value, max_val), min_val)
        return (v - min_val) / (max_val - min_val)

    def compute(
        self,
        image_quality_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compute descriptive condition proxy.

        Parameters
        ----------
        image_quality_metrics : Dict[str, Any]
            Output from image_quality_metrics.py

        Returns
        -------
        Dict[str, Any]
            {
                "condition_score": float (0.0 – 1.0),
                "components": {
                    "brightness_norm": float,
                    "contrast_norm": float,
                    "sharpness_norm": float
                },
                "method": "static_normalized_aggregate",
                "disclaimer": str
            }
        """
        required_fields = [
            "brightness_mean",
            "contrast_stddev",
            "sharpness_proxy",
        ]

        for field in required_fields:
            if field not in image_quality_metrics:
                raise ConditionScoreError(
                    f"Missing required metric: {field}"
                )

        brightness_norm = self._normalize(
            image_quality_metrics["brightness_mean"],
            *self.brightness_range,
        )

        contrast_norm = self._normalize(
            image_quality_metrics["contrast_stddev"],
            *self.contrast_range,
        )

        sharpness_norm = self._normalize(
            image_quality_metrics["sharpness_proxy"],
            *self.sharpness_range,
        )

        # Static, equal-weight aggregate
        condition_score = (
            brightness_norm +
            contrast_norm +
            sharpness_norm
        ) / 3.0

        return {
            "condition_score": condition_score,
            "components": {
                "brightness_norm": brightness_norm,
                "contrast_norm": contrast_norm,
                "sharpness_norm": sharpness_norm,
            },
            "method": "static_normalized_aggregate",
            "disclaimer": (
                "This is a technical image-quality proxy only. "
                "It does NOT represent physical asset condition, "
                "value, desirability, or risk."
            ),
        }


def compute_image_condition_score(
    image_quality_metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Functional wrapper for image condition proxy computation.

    SAFE FOR
    --------
    - Feature pipelines
    - Human review support
    - Audit replay

    NOT ALLOWED FOR
    ---------------
    - Valuation
    - Trust / risk decision
    - Approval routing
    - Automated conclusions
    """
    scorer = ImageConditionScorer()
    return scorer.compute(image_quality_metrics)
