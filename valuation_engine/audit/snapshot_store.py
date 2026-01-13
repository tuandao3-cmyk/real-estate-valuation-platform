# Module: valuation_engine/audit/snapshot_store.py
# Part of Advanced AVM System

# valuation_engine/audit/snapshot_store.py

"""
IMMUTABLE SNAPSHOT STORE
========================

LEGAL ROLE
----------
This module is responsible for creating and storing immutable valuation snapshots
for audit, forensic, and legal purposes.

It preserves evidence of:
- What data existed
- At what time
- Under which policy versions
- With which cryptographic hashes

STRICT CONSTRAINTS (MASTER_SPEC ENFORCED)
-----------------------------------------
- NO data modification
- NO inference
- NO valuation logic
- NO model invocation
- NO automatic triggering
- READ-ONLY inputs
- WRITE-ONCE outputs

Any deviation invalidates audit defensibility.
"""

from __future__ import annotations

import json
import hashlib
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


# =========================================================
# Snapshot Reason (SYSTEM-DEFINED ONLY)
# =========================================================

class SnapshotReason:
    FINAL_VALUATION = "FINAL_VALUATION"
    CREDIT_REVIEW = "CREDIT_REVIEW"
    AUDIT_REQUEST = "AUDIT_REQUEST"
    LEGAL_HOLD = "LEGAL_HOLD"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"


# =========================================================
# Core Data Structures
# =========================================================

@dataclass(frozen=True)
class ArtifactRef:
    artifact_name: str
    content_hash: str
    required_flag: bool


@dataclass(frozen=True)
class ValuationSnapshot:
    snapshot_id: str
    created_at_utc: str
    snapshot_reason: str
    valuation_hash: str
    trace_id: str
    artifact_refs: List[ArtifactRef]
    policy_versions: Dict[str, str]
    immutable: bool = True
    legal_hold_capable: bool = True


# =========================================================
# Snapshot Store
# =========================================================

class SnapshotStore:
    """
    SnapshotStore is a write-once evidence repository.

    It does NOT:
    - Decide when to snapshot
    - Inspect valuation correctness
    - Validate business logic

    It ONLY:
    - Hash
    - Freeze
    - Persist
    """

    def __init__(self, storage_dir: str):
        self._base_path = Path(storage_dir)
        self._base_path.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def create_snapshot(
        self,
        *,
        valuation_dossier_path: Path,
        valuation_trace_path: Path,
        trace_id: str,
        snapshot_reason: str,
        policy_versions: Dict[str, str],
        optional_artifacts: Optional[Dict[str, Path]] = None,
    ) -> ValuationSnapshot:
        """
        Explicit snapshot creation.

        REQUIRED:
        - Completed valuation dossier
        - Completed valuation trace
        - Explicit reason
        """

        self._validate_reason(snapshot_reason)

        dossier_hash = self._hash_file(valuation_dossier_path)
        trace_hash = self._hash_file(valuation_trace_path)

        artifact_refs: List[ArtifactRef] = [
            ArtifactRef(
                artifact_name="valuation_dossier",
                content_hash=dossier_hash,
                required_flag=True,
            ),
            ArtifactRef(
                artifact_name="valuation_trace",
                content_hash=trace_hash,
                required_flag=True,
            ),
        ]

        if optional_artifacts:
            for name, path in optional_artifacts.items():
                artifact_refs.append(
                    ArtifactRef(
                        artifact_name=name,
                        content_hash=self._hash_file(path),
                        required_flag=False,
                    )
                )

        snapshot = ValuationSnapshot(
            snapshot_id=str(uuid.uuid4()),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            snapshot_reason=snapshot_reason,
            valuation_hash=dossier_hash,
            trace_id=trace_id,
            artifact_refs=artifact_refs,
            policy_versions=dict(policy_versions),
        )

        self._persist_snapshot(snapshot)

        return snapshot

    # -----------------------------------------------------
    # Internal Mechanics (NON-BUSINESS)
    # -----------------------------------------------------

    def _persist_snapshot(self, snapshot: ValuationSnapshot) -> None:
        """
        Persist snapshot as immutable JSON.
        Write-once. No overwrite.
        """

        snapshot_path = self._base_path / f"{snapshot.snapshot_id}.json"

        if snapshot_path.exists():
            raise RuntimeError("Snapshot overwrite attempt detected")

        with snapshot_path.open("w", encoding="utf-8") as f:
            json.dump(
                self._serialize(snapshot),
                f,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )

    @staticmethod
    def _hash_file(path: Path) -> str:
        """
        Cryptographic hash for tamper detection.
        """ 
        sha256 = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def _serialize(snapshot: ValuationSnapshot) -> Dict:
        """
        Convert dataclass to JSON-safe dict.
        """
        data = asdict(snapshot)
        data["artifact_refs"] = [
            asdict(ref) for ref in snapshot.artifact_refs
        ]
        return data

    @staticmethod
    def _validate_reason(reason: str) -> None:
        allowed = {
            SnapshotReason.FINAL_VALUATION,
            SnapshotReason.CREDIT_REVIEW,
            SnapshotReason.AUDIT_REQUEST,
            SnapshotReason.LEGAL_HOLD,
            SnapshotReason.MANUAL_OVERRIDE,
        }
        if reason not in allowed:
            raise ValueError(f"Invalid snapshot reason: {reason}")


# =========================================================
# END OF FILE
# =========================================================
