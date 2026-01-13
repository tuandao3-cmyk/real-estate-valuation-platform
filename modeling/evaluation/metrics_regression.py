"""
model/evaluation/metrics_regression.py

GOVERNANCE ROLE
---------------
Offline regression metric calculator for model evaluation & audit.

STRICT BOUNDARIES
-----------------
- Numeric computation ONLY
- No thresholds
- No interpretation
- No decision
- No workflow influence

COMPLIANCE
----------
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & 2
"""

from __future__ import annotations

from typing import Dict
import numpy as np


class RegressionMetrics:
    """
    Pure numeric regression metrics.

    This class MUST NOT:
    - classify model quality
    - emit PASS / FAIL
    - recommend deployment
    - generate confidence scores
    """

    @staticmethod
    def _validate_inputs(y_true: np.ndarray, y_pred: np.ndarray) -> None:
        if not isinstance(y_true, np.ndarray) or not isinstance(y_pred, np.ndarray):
            raise TypeError("Inputs must be numpy arrays")

        if y_true.shape != y_pred.shape:
            raise ValueError("y_true and y_pred must have the same shape")

        if y_true.ndim != 1:
            raise ValueError("Inputs must be 1-dimensional arrays")

        if len(y_true) == 0:
            raise ValueError("Input arrays must not be empty")

    @staticmethod
    def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Mean Absolute Error
        """
        RegressionMetrics._validate_inputs(y_true, y_pred)
        return float(np.mean(np.abs(y_true - y_pred)))

    @staticmethod
    def mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Mean Squared Error
        """
        RegressionMetrics._validate_inputs(y_true, y_pred)
        return float(np.mean((y_true - y_pred) ** 2))

    @staticmethod
    def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Root Mean Squared Error
        """
        RegressionMetrics._validate_inputs(y_true, y_pred)
        return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

    @staticmethod
    def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Mean Absolute Percentage Error (MAPE)

        NOTE:
        - Pure numeric metric
        - No acceptability judgment
        """
        RegressionMetrics._validate_inputs(y_true, y_pred)

        if np.any(y_true == 0):
            raise ValueError("MAPE is undefined when y_true contains zero")

        return float(np.mean(np.abs((y_true - y_pred) / y_true)))

    @staticmethod
    def r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        R-squared (Coefficient of Determination)

        NOTE:
        - Descriptive statistic only
        - Does NOT imply model suitability
        """
        RegressionMetrics._validate_inputs(y_true, y_pred)

        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

        if ss_tot == 0:
            raise ValueError("R2 is undefined when variance of y_true is zero")

        return float(1 - ss_res / ss_tot)

    @staticmethod
    def evaluate(
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> Dict[str, float]:
        """
        Compute a bundle of regression metrics.

        GOVERNANCE:
        - Output is descriptive
        - Caller MUST NOT interpret or threshold internally
        """
        RegressionMetrics._validate_inputs(y_true, y_pred)

        return {
            "mae": RegressionMetrics.mae(y_true, y_pred),
            "mse": RegressionMetrics.mse(y_true, y_pred),
            "rmse": RegressionMetrics.rmse(y_true, y_pred),
            "mape": RegressionMetrics.mape(y_true, y_pred),
            "r2": RegressionMetrics.r2(y_true, y_pred),
        }
