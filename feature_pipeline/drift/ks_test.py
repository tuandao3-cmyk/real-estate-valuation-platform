"""
feature_pipeline/drift/ks_test.py

ROLE (MASTER_SPEC COMPLIANT)
---------------------------
Kolmogorov–Smirnov (KS) test for feature distribution drift.

This module computes descriptive statistical distance between
two continuous distributions.

ABSOLUTE PROHIBITIONS
---------------------
- No thresholds
- No decisions
- No alerts
- No retraining triggers
- No workflow impact
"""

from __future__ import annotations

import math
from typing import List, Dict, Any


class KSTestError(Exception):
    """Raised when KS test inputs are invalid."""


class KSTest:
    """
    Deterministic Kolmogorov–Smirnov test implementation.

    Notes
    -----
    - Intended for continuous numeric features
    - Output is descriptive only
    - Interpretation is strictly external
    """

    @staticmethod
    def calculate(
        *,
        baseline: List[float],
        current: List[float],
    ) -> Dict[str, float]:
        """
        Compute KS statistic and approximate p-value.

        Parameters
        ----------
        baseline : List[float]
            Reference distribution (e.g. training / approved baseline).
        current : List[float]
            Current distribution (e.g. production snapshot).

        Returns
        -------
        Dict with:
        - ks_statistic
        - p_value (asymptotic approximation)

        Preconditions
        -------------
        - Inputs must be non-empty
        - Inputs must be numeric
        """

        KSTest._validate_inputs(baseline, current)

        baseline_sorted = sorted(baseline)
        current_sorted = sorted(current)

        n1 = len(baseline_sorted)
        n2 = len(current_sorted)

        i = j = 0
        cdf1 = cdf2 = 0.0
        ks_stat = 0.0

        while i < n1 and j < n2:
            if baseline_sorted[i] <= current_sorted[j]:
                i += 1
                cdf1 = i / n1
            else:
                j += 1
                cdf2 = j / n2

            ks_stat = max(ks_stat, abs(cdf1 - cdf2))

        # Catch remaining tail
        while i < n1:
            i += 1
            cdf1 = i / n1
            ks_stat = max(ks_stat, abs(cdf1 - cdf2))

        while j < n2:
            j += 1
            cdf2 = j / n2
            ks_stat = max(ks_stat, abs(cdf1 - cdf2))

        p_value = KSTest._approximate_p_value(ks_stat, n1, n2)

        return {
            "ks_statistic": ks_stat,
            "p_value": p_value,
            "governance_note": (
                "KS statistic and p-value are descriptive statistical outputs only. "
                "No thresholds or decisions are applied in this module."
            ),
        }

    @staticmethod
    def _approximate_p_value(d: float, n1: int, n2: int) -> float:
        """
        Asymptotic approximation of KS test p-value.

        Reference
        ---------
        Kolmogorov distribution approximation.
        """
        if n1 <= 0 or n2 <= 0:
            return 1.0

        en = math.sqrt((n1 * n2) / (n1 + n2))
        lambda_val = (en + 0.12 + 0.11 / en) * d

        # Kolmogorov asymptotic formula
        p = 2.0 * sum(
            (-1) ** (k - 1) * math.exp(-2 * (k ** 2) * (lambda_val ** 2))
            for k in range(1, 100)
        )

        return max(min(p, 1.0), 0.0)

    @staticmethod
    def _validate_inputs(baseline: List[float], current: List[float]) -> None:
        """
        Validate KS test input arrays.
        """
        if not baseline or not current:
            raise KSTestError("Input distributions must not be empty.")

        for v in baseline + current:
            if not isinstance(v, (int, float)):
                raise KSTestError(
                    "KS test requires numeric input values only."
                )
