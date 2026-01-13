"""
feature_pipeline/pipelines/feature_snapshot.py

ROLE (MASTER_SPEC COMPLIANT)
---------------------------
Immutable snapshot creator for feature pipeline outputs.

This module packages validated feature outputs into a
deterministic, audit-ready snapshot artifact.

ABSOLUTE PROHIBITIONS
---------------------
- No feature computation
- No validation
- No mutation
- No inference
- No retry / fallback
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List


class FeatureSnapshot:
    """
    Immutable container for feature pipeline outputs.

    Snapshot Guarantees
    -------------------
    - Deterministic serialization
    - Hash-addressable
    - Audit-ready
    - Replay-safe
    """

    def __init__(
        self,
        *,
        snapshot_id: str,
        created_at_utc: str,
        feature_set: Dict[str, Any],
        feature_versions: Dict[str, str],
        schema_versions: Dict[str, str],
        pipeline_version: str,
        content_hash: str,
    ) -> None:
        self.snapshot_id = snapshot_id
        self.created_at_utc = created_at_utc
        self.feature_set = feature_set
        self.feature_versions = feature_versions
        self.schema_versions = schema_versions
        self.pipeline_version = pipeline_version
        self.content_hash = content_hash

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize snapshot to dictionary.
        """
        return {
            "snapshot_id": self.snapshot_id,
            "created_at_utc": self.created_at_utc,
            "pipeline_version": self.pipeline_version,
            "content_hash": self.content_hash,
            "feature_versions": self.feature_versions,
            "schema_versions": self.schema_versions,
            "feature_set": self.feature_set,
            "governance_disclaimer": (
                "This snapshot is an immutable evidence artifact. "
                "No inference, validation, or transformation was "
                "performed during snapshot creation."
            ),
        }


class FeatureSnapshotBuilder:
    """
    Deterministic builder for FeatureSnapshot.
    """

    PIPELINE_VERSION = "1.0.0"

    @staticmethod
    def build(
        *,
        feature_set: Dict[str, Any],
        feature_versions: Dict[str, str],
        schema_versions: Dict[str, str],
    ) -> FeatureSnapshot:
        """
        Build an immutable snapshot from validated feature outputs.

        Preconditions
        -------------
        - feature_set MUST be validated upstream
        - versions MUST be explicit
        """
        created_at = datetime.now(timezone.utc).isoformat()

        canonical_payload = FeatureSnapshotBuilder._canonical_payload(
            feature_set=feature_set,
            feature_versions=feature_versions,
            schema_versions=schema_versions,
            pipeline_version=FeatureSnapshotBuilder.PIPELINE_VERSION,
        )

        content_hash = FeatureSnapshotBuilder._hash_payload(canonical_payload)

        snapshot_id = f"feature_snapshot_{content_hash[:16]}"

        return FeatureSnapshot(
            snapshot_id=snapshot_id,
            created_at_utc=created_at,
            feature_set=feature_set,
            feature_versions=feature_versions,
            schema_versions=schema_versions,
            pipeline_version=FeatureSnapshotBuilder.PIPELINE_VERSION,
            content_hash=content_hash,
        )

    @staticmethod
    def _canonical_payload(
        *,
        feature_set: Dict[str, Any],
        feature_versions: Dict[str, str],
        schema_versions: Dict[str, str],
        pipeline_version: str,
    ) -> Dict[str, Any]:
        """
        Create canonical payload for hashing.
        """
        return {
            "pipeline_version": pipeline_version,
            "feature_versions": dict(sorted(feature_versions.items())),
            "schema_versions": dict(sorted(schema_versions.items())),
            "feature_set": FeatureSnapshotBuilder._sort_nested(feature_set),
        }

    @staticmethod
    def _hash_payload(payload: Dict[str, Any]) -> str:
        """
        Compute SHA-256 hash of canonical payload.
        """
        encoded = json.dumps(
            payload,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def _sort_nested(obj: Any) -> Any:
        """
        Recursively sort nested structures to guarantee determinism.
        """
        if isinstance(obj, dict):
            return {k: FeatureSnapshotBuilder._sort_nested(obj[k]) for k in sorted(obj)}
        if isinstance(obj, list):
            return [FeatureSnapshotBuilder._sort_nested(v) for v in obj]
        return obj
