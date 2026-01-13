"""
api/services/snapshot_service.py

GOVERNANCE NOTICE
-----------------
This service is responsible for creating and retrieving immutable
feature / input snapshots for valuation workflows.

STRICT CONSTRAINTS:
- No valuation logic
- No model inference
- No rule evaluation
- No mutation after snapshot creation

Violation = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

import uuid
import hashlib
import json
from datetime import datetime
from typing import Dict, Any

from api.schemas.request.feature_snapshot_request import FeatureSnapshotRequest
from api.schemas.common.metadata import Metadata


class SnapshotService:
    """
    Snapshot orchestration service.

    Purpose:
    - Create immutable snapshots of input & feature data
    - Guarantee reproducibility and audit traceability
    - Act as a legal boundary before any valuation logic

    This service does NOT:
    - Validate business meaning
    - Enrich features
    - Perform transformations
    """

    @staticmethod
    def create_snapshot(
        request: FeatureSnapshotRequest,
        metadata: Metadata,
    ) -> Dict[str, Any]:
        """
        Create an immutable snapshot from request payload.

        Parameters:
        - request: FeatureSnapshotRequest (validated schema)
        - metadata: Metadata (request / actor / source info)

        Returns:
        - snapshot dictionary (immutable by contract)

        Snapshot MUST be persisted by caller.
        """

        snapshot_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        snapshot_payload = {
            "snapshot_id": snapshot_id,
            "created_at": created_at,
            "metadata": metadata.model_dump(),
            "feature_payload": request.model_dump(),
        }

        snapshot_hash = SnapshotService._compute_hash(snapshot_payload)

        snapshot_payload["snapshot_hash"] = snapshot_hash

        return snapshot_payload

    @staticmethod
    def _compute_hash(payload: Dict[str, Any]) -> str:
        """
        Compute deterministic hash for snapshot integrity.

        Purpose:
        - Ensure immutability
        - Enable audit replay
        - Detect tampering

        Hash algorithm is deterministic and content-based.
        """

        canonical_json = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
