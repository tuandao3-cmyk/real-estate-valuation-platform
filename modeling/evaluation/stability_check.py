"""
model/evaluation/stability_check.py

GOVERNANCE ROLE
---------------
Offline model stability analysis (descriptive, numeric only).

PURPOSE
-------
Measure stability of regression model outputs across
different datasets / time slices without interpretation.

STRICT BOUNDARIES
-----------------
- Offline execution ONLY
- No thresholds
- No PASS / FAIL
- No governance decision
- No registry interaction
"""

from __future__ import annotations

from typing import Dict, Any
import numpy as np


class StabilityCheck:
    """
    StabilityCheck computes numeric stability indicators
    between two sets of model predictions.

    This class MUST NOT:
    - decide model acceptability
    - emit alerts
    - apply thresholds
    - influence runtime valuation
    """

    @staticmethod
    def _validate_inputs(
        y_pred_reference: np.ndarray,
        y_pred_candidate: np.ndarray,
    ) -> None:
        if not isinstance(y_pred_reference, np.ndarray):
            raise TypeError("y_pred_reference must be a numpy array")

        if not isinstance(y_pred_candidate, np.ndarray):
            raise TypeError("y_pred_candidate must be a numpy array")

        if y_pred_reference.shape != y_pred_candidate.shape:
            raise ValueError("Prediction arrays must have the same shape")

        if y_pred_reference.size == 0:
            raise ValueError("Prediction arrays must not be empty")

    @staticmethod
    def check(
        y_pred_reference: np.ndarray,
        y_pred_candidate: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Compute descriptive stability metrics.

        Parameters
        ----------
        y_pred_reference : np.ndarray
            Baseline / historical prediction outputs
        y_pred_candidate : np.ndarray
            New prediction outputs to compare

        Returns
        -------
        Dict[str, Any]
            Numeric stability indicators ONLY
        """
        StabilityCheck._validate_inputs(
            y_pred_reference=y_pred_reference,
            y_pred_candidate=y_pred_candidate,
        )

        diff = y_pred_candidate - y_pred_reference

        # --- Pure numeric descriptors ---
        mean_reference = float(np.mean(y_pred_reference))
        mean_candidate = float(np.mean(y_pred_candidate))

        std_reference = float(np.std(y_pred_reference))
        std_candidate = float(np.std(y_pred_candidate))

        mean_shift = float(np.mean(diff))
        std_shift = float(np.std(diff))

        abs_shift_mean = float(np.mean(np.abs(diff)))
        max_abs_shift = float(np.max(np.abs(diff)))

        # --- Relative change (guarded against zero division) ---
        relative_mean_change = (
            mean_shift / mean_reference if mean_reference != 0 else None
        )

        return {
            "n_samples": int(y_pred_reference.size),
            "reference_distribution": {
                "mean": mean_reference,
                "std": std_reference,
            },
            "candidate_distribution": {
                "mean": mean_candidate,
                "std": std_candidate,
            },
            "shift_metrics": {
                "mean_shift": mean_shift,
                "std_shift": std_shift,
                "mean_absolute_shift": abs_shift_mean,
                "max_absolute_shift": max_abs_shift,
                "relative_mean_change": relative_mean_change,
            },
        }
