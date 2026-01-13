"""
model/evaluation/backtest_runner.py

GOVERNANCE ROLE
---------------
Offline backtesting orchestrator for regression models.

STRICT BOUNDARIES
-----------------
- Offline execution ONLY
- Deterministic orchestration
- No interpretation
- No thresholds
- No approval / activation logic

COMPLIANCE
----------
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – PART 1 & 2
"""

from __future__ import annotations

from typing import Dict, Any, Callable
import numpy as np

from model.evaluation.metrics_regression import RegressionMetrics


class BacktestRunner:
    """
    Backtest orchestration engine.

    This class:
    - Executes model inference on historical data
    - Computes regression metrics
    - Returns descriptive results ONLY

    This class MUST NOT:
    - judge model quality
    - decide deployment
    - modify models
    - influence valuation workflow
    """

    def __init__(
        self,
        model_id: str,
        model_version: str,
        inference_fn: Callable[[np.ndarray], np.ndarray],
    ) -> None:
        """
        Parameters
        ----------
        model_id : str
            Immutable model identifier (registry-aligned)
        model_version : str
            Version string tied to artifact hash
        inference_fn : Callable
            Deterministic inference function (read-only model)
        """
        if not callable(inference_fn):
            raise TypeError("inference_fn must be callable")

        self.model_id = model_id
        self.model_version = model_version
        self.inference_fn = inference_fn

    @staticmethod
    def _validate_inputs(
        X: np.ndarray,
        y_true: np.ndarray,
    ) -> None:
        if not isinstance(X, np.ndarray) or not isinstance(y_true, np.ndarray):
            raise TypeError("X and y_true must be numpy arrays")

        if X.shape[0] != y_true.shape[0]:
            raise ValueError("X and y_true must have the same number of rows")

        if X.shape[0] == 0:
            raise ValueError("Backtest dataset must not be empty")

    def run(
        self,
        X: np.ndarray,
        y_true: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Execute backtest.

        GOVERNANCE:
        - No PASS / FAIL
        - No thresholding
        - No comparison logic
        - Output is descriptive and auditable
        """
        self._validate_inputs(X, y_true)

        # --- Inference (read-only, deterministic) ---
        y_pred = self.inference_fn(X)

        if not isinstance(y_pred, np.ndarray):
            raise TypeError("Inference output must be a numpy array")

        if y_pred.shape != y_true.shape:
            raise ValueError("y_pred shape must match y_true shape")

        # --- Metric computation (numeric only) ---
        metrics = RegressionMetrics.evaluate(
            y_true=y_true,
            y_pred=y_pred,
        )

        # --- Assemble audit-safe result ---
        return {
            "model_id": self.model_id,
            "model_version": self.model_version,
            "n_samples": int(len(y_true)),
            "metrics": metrics,
        }
