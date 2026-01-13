"""
feature_pipeline/drift/feature_drift_report.py

GOVERNANCE ROLE
---------------
Pure reporting layer for feature drift metrics.

ABSOLUTE RULES
--------------
- No metric calculation
- No threshold comparison
- No drift classification
- No alerts
- No automated decisions
- Human interpretation only

This module aggregates numeric drift statistics
into a structured, audit-friendly report.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass(frozen=True)
class FeatureDriftMetric:
    """
    Container for numeric drift metrics of a single feature.
    """
    feature_name: str
    metric_type: str  # e.g. 'PSI', 'KS_STATISTIC'
    value: float
    reference_window: str
    comparison_window: str
    calculation_timestamp: str


@dataclass(frozen=True)
class FeatureDriftRecord:
    """
    Aggregated drift record per feature.
    """
    feature_name: str
    metrics: List[FeatureDriftMetric]


@dataclass(frozen=True)
class FeatureDriftReport:
    """
    Top-level drift report object.

    This object is DESCRIPTIVE ONLY.
    """
    report_id: str
    generated_at: str
    data_snapshot_id: str
    model_version: Optional[str]
    features: List[FeatureDriftRecord]
    notes: Optional[str] = None


class FeatureDriftReportBuilder:
    """
    Builder class to assemble a drift report from
    pre-computed numeric drift metrics.
    """

    def __init__(
        self,
        data_snapshot_id: str,
        model_version: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        self._data_snapshot_id = data_snapshot_id
        self._model_version = model_version
        self._notes = notes
        self._records: Dict[str, List[FeatureDriftMetric]] = {}

    def add_metric(
        self,
        feature_name: str,
        metric_type: str,
        value: float,
        reference_window: str,
        comparison_window: str,
        calculation_timestamp: Optional[str] = None,
    ) -> None:
        """
        Add a numeric drift metric for a feature.

        IMPORTANT:
        - Assumes metric already computed elsewhere
        - No validation or interpretation is performed
        """
        metric = FeatureDriftMetric(
            feature_name=feature_name,
            metric_type=metric_type,
            value=value,
            reference_window=reference_window,
            comparison_window=comparison_window,
            calculation_timestamp=calculation_timestamp
            or datetime.utcnow().isoformat(),
        )

        self._records.setdefault(feature_name, []).append(metric)

    def build(self) -> FeatureDriftReport:
        """
        Build the final FeatureDriftReport object.
        """
        feature_records = [
            FeatureDriftRecord(feature_name=fn, metrics=metrics)
            for fn, metrics in self._records.items()
        ]

        return FeatureDriftReport(
            report_id=self._generate_report_id(),
            generated_at=datetime.utcnow().isoformat(),
            data_snapshot_id=self._data_snapshot_id,
            model_version=self._model_version,
            features=feature_records,
            notes=self._notes,
        )

    @staticmethod
    def _generate_report_id() -> str:
        """
        Generate a deterministic, audit-friendly report ID.
        """
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"feature-drift-report-{ts}"


class FeatureDriftReportSerializer:
    """
    Serialization utilities for FeatureDriftReport.
    """

    @staticmethod
    def to_dict(report: FeatureDriftReport) -> Dict:
        """
        Convert report to a plain dictionary.
        """
        return asdict(report)

    @staticmethod
    def to_json(report: FeatureDriftReport, pretty: bool = True) -> str:
        """
        Serialize report to JSON.

        NOTE:
        - Output is read-only
        - No downstream logic should consume this as decision input
        """
        if pretty:
            return json.dumps(asdict(report), indent=2, ensure_ascii=False)
        return json.dumps(asdict(report), ensure_ascii=False)
