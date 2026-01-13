"""
api/routers/snapshot_router.py

GOVERNANCE NOTICE
-----------------
This router exposes APIs for creating and retrieving valuation snapshots.

STRICT CONSTRAINTS:
- No business logic
- No feature computation
- No valuation decision
- Snapshot is immutable once created
"""

from fastapi import APIRouter, Request, status

from api.schemas.request.feature_snapshot_request import FeatureSnapshotRequest
from api.schemas.common.metadata import Metadata
from api.services.snapshot_service import SnapshotService

router = APIRouter(
    prefix="/snapshots",
    tags=["Snapshots"],
)


@router.post(
    "",
    summary="Create valuation snapshot",
    status_code=status.HTTP_201_CREATED,
)
async def create_snapshot(
    request: Request,
    payload: FeatureSnapshotRequest,
) -> dict:
    """
    Create a valuation snapshot.

    Purpose:
    - Persist immutable input data
    - Enable reproducibility & audit
    - Act as canonical input for downstream valuation

    NOTE:
    This endpoint does NOT:
    - Validate business correctness
    - Compute features
    - Trigger valuation
    """
    request_id = getattr(request.state, "request_id", None)

    service = SnapshotService()
    snapshot = service.create_snapshot(
        feature_payload=payload,
        request_id=request_id,
    )

    return {
        "snapshot_id": snapshot.snapshot_id,
        "metadata": Metadata(
            request_id=request_id,
        ).model_dump(),
    }


@router.get(
    "/{snapshot_id}",
    summary="Get valuation snapshot",
)
async def get_snapshot(
    snapshot_id: str,
    request: Request,
) -> dict:
    """
    Retrieve an existing snapshot.

    Purpose:
    - Audit
    - Replay
    - Inspection by authorized systems

    NOTE:
    Snapshot content is returned AS-IS.
    """
    request_id = getattr(request.state, "request_id", None)

    service = SnapshotService()
    snapshot = service.get_snapshot(
        snapshot_id=snapshot_id,
        request_id=request_id,
    )

    return snapshot.model_dump()
