"""
feature_pipeline/drift/psi_calculator.py

ROLE (MASTER_SPEC COMPLIANT)
---------------------------
Population Stability Index (PSI) calculator.

This module computes descriptive distribution drift metrics
between a reference (baseline) distribution and a current one.

ABSOLUTE PROHIBITIONS
---------------------
- No thresholds
- No alerts
- No decisions
- No retraining trigger
- No workflow impact
"""

from __future__ import annotations

import math
from typing import List, Dict, Any


class PSICalculationError(Exception):
    """Raised when PSI calculation inputs are invalid."""


class PSICalculator:
    """
    Deterministic PSI calculator.

    PSI Formula
    -----------
    PSI = Σ (actual_i - expected_i) * ln(actual_i / expected_i)

    Notes
    -----
    - Output is descriptive only
    - Interpretation is external to this module
    """

    @staticmethod
    def calculate(
        *,
        expected_distribution: List[float],
        actual_distribution: List[float],
        epsilon: float = 1e-6,
    ) -> float:
        """
        Compute Population Stability Index (PSI).

        Parameters
        ----------
        expected_distribution : List[float]
            Baseline distribution (e.g. training reference).
        actual_distribution : List[float]
            Current distribution (e.g. production snapshot).
        epsilon : float
            Small constant to avoid division-by-zero.

        Returns
        -------
        float
            PSI value (non-negative, descriptive).

        Preconditions
        -------------
        - Distributions must be same length
        - Values must be >= 0
        - Sum does NOT have to be 1.0 (will be normalized)
        """

        PSICalculator._validate_inputs(
            expected_distribution=expected_distribution,
            actual_distribution=actual_distribution,
        )

        expected = PSICalculator._normalize(expected_distribution)
        actual = PSICalculator._normalize(actual_distribution)

        psi_value = 0.0

        for exp_i, act_i in zip(expected, actual):
            exp_i = max(exp_i, epsilon)
            act_i = max(act_i, epsilon)

            psi_value += (act_i - exp_i) * math.log(act_i / exp_i)

        return psi_value

    @staticmethod
    def calculate_with_breakdown(
        *,
        expected_distribution: List[float],
        actual_distribution: List[float],
        epsilon: float = 1e-6,
    ) -> Dict[str, Any]:
        """
        Compute PSI with per-bin breakdown.

        Returns
        -------
        Dict with:
        - psi_value
        - bins: list of per-bin contributions
        """

        PSICalculator._validate_inputs(
            expected_distribution=expected_distribution,
            actual_distribution=actual_distribution,
        )

        expected = PSICalculator._normalize(expected_distribution)
        actual = PSICalculator._normalize(actual_distribution)

        bins = []
        total_psi = 0.0

        for idx, (exp_i, act_i) in enumerate(zip(expected, actual)):
            exp_i = max(exp_i, epsilon)
            act_i = max(act_i, epsilon)

            contribution = (act_i - exp_i) * math.log(act_i / exp_i)
            total_psi += contribution

            bins.append(
                {
                    "bin_index": idx,
                    "expected_ratio": exp_i,
                    "actual_ratio": act_i,
                    "psi_contribution": contribution,
                }
            )

        return {
            "psi_value": total_psi,
            "bin_contributions": bins,
            "governance_note": (
                "PSI values are descriptive drift metrics only. "
                "No thresholds or decisions are applied in this module."
            ),
        }

    @staticmethod
    def _normalize(values: List[float]) -> List[float]:
        """
        Normalize list of non-negative values into ratios.
        """
        total = sum(values)
        if total <= 0:
            raise PSICalculationError(
                "Distribution sum must be greater than zero."
            )
        return [v / total for v in values]

    @staticmethod
    def _validate_inputs(
        *,
        expected_distribution: List[float],
        actual_distribution: List[float],
    ) -> None:
        """
        Validate PSI input distributions.
        """
        if not expected_distribution or not actual_distribution:
            raise PSICalculationError(
                "Distributions must not be empty."
            )

        if len(expected_distribution) != len(actual_distribution):
            raise PSICalculationError(
                "Expected and actual distributions must have equal length."
            )

        for v in expected_distribution + actual_distribution:
            if v < 0:
                raise PSICalculationError(
                    "Distribution values must be non-negative."
                )
