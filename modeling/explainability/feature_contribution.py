"""
feature_contribution.py

GOVERNANCE-LOCKED EXPLAINABILITY MODULE
--------------------------------------

PURPOSE
-------
Compute descriptive feature contribution for regression-style models
in a strictly NON-DECISIONAL, NON-VALUTIVE manner.

This module exists solely to:
- Support human interpretability
- Provide audit evidence
- Enable forensic / replay analysis

ABSOLUTE PROHIBITIONS
---------------------
- NO price conclusion
- NO feature importance ranking for selection
- NO model comparison verdict
- NO approval / rejection logic
- NO runtime valuation usage

All outputs are DESCRIPTIVE, READ-ONLY, and HUMAN-INTERPRETED.

COMPLIANT WITH:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS PART 1
- IMPLEMENTATION STATUS PART 2
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np


# =========================
# DATA STRUCTURES
# =========================

@dataclass(frozen=True)
class FeatureContribution:
    """
    Immutable container for per-feature contribution.

    NOTE:
    - contribution_value is NUMERIC ONLY
    - meaning MUST be interpreted by humans
    """
    feature_name: str
    contribution_value: float
    baseline_value: float
    feature_value: float


@dataclass(frozen=True)
class ContributionResult:
    """
    Aggregated explainability output.

    This object is:
    - Read-only
    - Non-decisive
    - Audit-safe
    """
    model_id: str
    model_version: str
    sample_id: str
    method: str
    contributions: List[FeatureContribution]
    residual: Optional[float]


# =========================
# CORE EXPLAINABILITY LOGIC
# =========================

class FeatureContributionCalculator:
    """
    Calculator for feature contribution.

    GOVERNANCE NOTES
    ----------------
    - Accepts ONLY trained model parameters (read-only)
    - Does NOT fit, adjust, or optimize anything
    - No auto-normalization beyond explicit input
    """

    def __init__(
        self,
        model_id: str,
        model_version: str,
        coefficients: Dict[str, float],
        intercept: float,
        baseline: Dict[str, float],
    ):
        """
        Parameters
        ----------
        coefficients:
            Frozen regression coefficients (post-training).
        intercept:
            Model intercept (read-only).
        baseline:
            Reference baseline per feature (e.g. training mean).
        """
        self.model_id = model_id
        self.model_version = model_version
        self.coefficients = coefficients
        self.intercept = intercept
        self.baseline = baseline

    def compute(
        self,
        sample_id: str,
        feature_values: Dict[str, float],
        actual_value: Optional[float] = None,
    ) -> ContributionResult:
        """
        Compute per-feature contribution for a single sample.

        IMPORTANT:
        - actual_value is OPTIONAL
        - residual is reported ONLY if actual_value is provided
        - No judgement is made on residual size
        """

        contributions: List[FeatureContribution] = []
        predicted_value = self.intercept

        for feature, coef in self.coefficients.items():
            value = feature_values.get(feature)
            base = self.baseline.get(feature)

            # Explicit null handling – no silent inference
            if value is None or base is None:
                continue

            delta = value - base
            contribution = coef * delta

            predicted_value += contribution

            contributions.append(
                FeatureContribution(
                    feature_name=feature,
                    contribution_value=float(contribution),
                    baseline_value=float(base),
                    feature_value=float(value),
                )
            )

        residual: Optional[float] = None
        if actual_value is not None:
            residual = float(actual_value - predicted_value)

        return ContributionResult(
            model_id=self.model_id,
            model_version=self.model_version,
            sample_id=sample_id,
            method="linear_contribution",
            contributions=contributions,
            residual=residual,
        )


# =========================
# UTILITY (DESCRIPTIVE ONLY)
# =========================

def summarize_contributions(
    result: ContributionResult,
) -> Dict[str, float]:
    """
    Produce a flat, numeric-only summary.

    OUTPUT
    ------
    Dict[str, float]:
        feature_name -> contribution_value

    GOVERNANCE:
    - No ranking
    - No thresholding
    - No interpretation
    """
    return {
        c.feature_name: c.contribution_value
        for c in result.contributions
    }


def total_absolute_contribution(
    result: ContributionResult,
) -> float:
    """
    Numeric magnitude indicator.

    NOTE:
    - Descriptive statistic only
    - NOT a confidence score
    - NOT a quality measure
    """
    return float(
        np.sum([abs(c.contribution_value) for c in result.contributions])
    )


# =========================
# GOVERNANCE GUARD
# =========================

__all__ = [
    "FeatureContribution",
    "ContributionResult",
    "FeatureContributionCalculator",
    "summarize_contributions",
    "total_absolute_contribution",
]

"""
FINAL GOVERNANCE STATEMENT
-------------------------
This module explains WHAT influenced the model output numerically.
It NEVER explains WHAT SHOULD BE DONE.

Interpretation belongs to humans.
Responsibility belongs to humans.
"""
