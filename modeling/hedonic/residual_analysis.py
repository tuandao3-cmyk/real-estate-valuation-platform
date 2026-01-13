"""
Hedonic Model Residual Analysis (Governance & Diagnostics Only)

🚫 NOT PART OF VALUATION DECISION FLOW
🚫 DOES NOT UPDATE MODEL
🚫 DOES NOT AFFECT PRICING

Purpose:
- Quantify model residual behavior for audit & model risk management
- Provide descriptive diagnostics ONLY
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import math
import statistics
import hashlib
import json


# ---------------------------------------------------------------------
# Data Contracts
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ResidualInput:
    """
    Immutable input for residual analysis.
    """
    model_id: str
    model_version: str
    feature_snapshot_hash: str
    predictions: Dict[str, float]        # property_id -> predicted price
    actuals: Dict[str, float]             # property_id -> observed price
    evaluation_context: Optional[Dict]    # metadata only (e.g. dataset name)


@dataclass(frozen=True)
class ResidualMetrics:
    """
    Descriptive residual statistics.
    """
    count: int
    mean_error: float
    mean_absolute_error: float
    root_mean_squared_error: float
    median_absolute_error: float
    max_positive_error: float
    max_negative_error: float


@dataclass(frozen=True)
class ResidualReport:
    """
    Final residual analysis artifact.
    """
    model_id: str
    model_version: str
    feature_snapshot_hash: str
    residual_metrics: ResidualMetrics
    residual_distribution: Dict[str, int]
    limitations: List[str]
    audit_hash: str


# ---------------------------------------------------------------------
# Residual Analyzer
# ---------------------------------------------------------------------

class HedonicResidualAnalyzer:
    """
    Pure diagnostic component for hedonic model residuals.

    This class:
    - Performs numeric error analysis
    - Produces no decisions
    - Is safe for audit / MRM
    """

    def analyze(self, residual_input: ResidualInput) -> ResidualReport:
        self._validate_input(residual_input)

        errors = self._compute_errors(
            residual_input.predictions,
            residual_input.actuals
        )

        metrics = self._compute_metrics(errors)
        distribution = self._residual_buckets(errors)

        audit_hash = self._audit_hash(
            residual_input,
            metrics,
            distribution
        )

        return ResidualReport(
            model_id=residual_input.model_id,
            model_version=residual_input.model_version,
            feature_snapshot_hash=residual_input.feature_snapshot_hash,
            residual_metrics=metrics,
            residual_distribution=distribution,
            limitations=self._limitations(),
            audit_hash=audit_hash
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_input(residual_input: ResidualInput) -> None:
        if not residual_input.predictions:
            raise ValueError("No predictions provided for residual analysis")

        if not residual_input.actuals:
            raise ValueError("No actual values provided for residual analysis")

    @staticmethod
    def _compute_errors(
        predictions: Dict[str, float],
        actuals: Dict[str, float]
    ) -> List[float]:
        errors = []

        for pid, pred in predictions.items():
            if pid not in actuals:
                continue  # missing ground truth is allowed

            errors.append(pred - actuals[pid])

        if not errors:
            raise ValueError("No overlapping prediction/actual pairs")

        return errors

    @staticmethod
    def _compute_metrics(errors: List[float]) -> ResidualMetrics:
        abs_errors = [abs(e) for e in errors]

        mse = sum(e ** 2 for e in errors) / len(errors)
        rmse = math.sqrt(mse)

        return ResidualMetrics(
            count=len(errors),
            mean_error=sum(errors) / len(errors),
            mean_absolute_error=sum(abs_errors) / len(abs_errors),
            root_mean_squared_error=rmse,
            median_absolute_error=statistics.median(abs_errors),
            max_positive_error=max(errors),
            max_negative_error=min(errors)
        )

    @staticmethod
    def _residual_buckets(errors: List[float]) -> Dict[str, int]:
        """
        Bucket residuals into coarse descriptive ranges.
        No threshold meaning. No quality judgement.
        """
        buckets = {
            "< -30%": 0,
            "-30% to -10%": 0,
            "-10% to +10%": 0,
            "+10% to +30%": 0,
            "> +30%": 0
        }

        for e in errors:
            if e < -0.30:
                buckets["< -30%"] += 1
            elif -0.30 <= e < -0.10:
                buckets["-30% to -10%"] += 1
            elif -0.10 <= e <= 0.10:
                buckets["-10% to +10%"] += 1
            elif 0.10 < e <= 0.30:
                buckets["+10% to +30%"] += 1
            else:
                buckets["> +30%"] += 1

        return buckets

    @staticmethod
    def _audit_hash(
        residual_input: ResidualInput,
        metrics: ResidualMetrics,
        distribution: Dict[str, int]
    ) -> str:
        payload = {
            "model_id": residual_input.model_id,
            "model_version": residual_input.model_version,
            "feature_snapshot_hash": residual_input.feature_snapshot_hash,
            "metrics": metrics.__dict__,
            "distribution": distribution
        }

        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def _limitations() -> List[str]:
        return [
            "Residual analysis is descriptive and retrospective only.",
            "Metrics do not imply model approval or rejection.",
            "Results depend on the quality and representativeness of observed data.",
            "Residuals must not be used directly in valuation decisions.",
            "Analysis does not account for unobserved property attributes."
        ]
