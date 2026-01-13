"""
feature_pipeline/pipelines/feature_build_flow.py

ROLE (MASTER_SPEC COMPLIANT)
---------------------------
Deterministic orchestration layer for feature building.

This module coordinates feature execution, validation,
and snapshot creation WITHOUT performing any computation.

ABSOLUTE PROHIBITIONS
---------------------
- No feature logic
- No validation logic
- No inference
- No fallback
- No mutation of feature output
"""

from __future__ import annotations

from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timezone

from feature_pipeline.pipelines.feature_validation import FeatureValidationResult
from feature_pipeline.pipelines.feature_snapshot import FeatureSnapshot, FeatureSnapshotBuilder


@dataclass(frozen=True)
class FeatureBuildResult:
    """
    Workflow-only result of feature build flow.
    """
    build_id: str
    created_at_utc: str
    feature_names: List[str]
    validation_result: FeatureValidationResult
    snapshot: FeatureSnapshot


class FeatureBuildFlow:
    """
    Deterministic orchestrator for feature pipeline build.
    """

    PIPELINE_NAME = "feature_build_flow"
    PIPELINE_VERSION = "1.0.0"

    @staticmethod
    def run(
        *,
        feature_names: List[str],
        executed_features: Dict[str, Any],
        feature_versions: Dict[str, str],
        schema_versions: Dict[str, str],
        validation_result: FeatureValidationResult,
    ) -> FeatureBuildResult:
        """
        Execute deterministic feature build flow.

        Preconditions
        -------------
        - Feature execution already completed
        - Feature outputs are read-only
        - Validation already performed upstream
        """

        created_at = datetime.now(timezone.utc).isoformat()

        # Governance: hard stop if validation failed
        if not validation_result.is_valid:
            raise RuntimeError(
                "FeatureBuildFlow aborted: feature validation failed. "
                "No snapshot will be created."
            )

        snapshot = FeatureSnapshotBuilder.build(
            feature_set=executed_features,
            feature_versions=feature_versions,
            schema_versions=schema_versions,
        )

        build_id = FeatureBuildFlow._build_id(snapshot.content_hash)

        return FeatureBuildResult(
            build_id=build_id,
            created_at_utc=created_at,
            feature_names=list(feature_names),
            validation_result=validation_result,
            snapshot=snapshot,
        )

    @staticmethod
    def _build_id(content_hash: str) -> str:
        """
        Deterministic build identifier.
        """
        return f"feature_build_{content_hash[:12]}"
