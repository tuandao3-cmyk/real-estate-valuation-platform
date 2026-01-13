"""
api/routers/valuation_router.py

GOVERNANCE NOTICE
-----------------
This router exposes valuation execution APIs.

STRICT CONSTRAINTS:
- No pricing logic
- No rule enforcement
- No confidence calculation
- No decision making
"""

from fastapi import APIRouter, Request, status

from api.schemas.request.valuation_request import ValuationRequest
from api.schemas.common.metadata import Metadata
from api.services.valuation_service import ValuationService

router = APIRouter(
    prefix="/valuations",
    tags=["Valuations"],
)


@router.post(
    "",
    summary="Run valuation based on snapshot",
    status_code=status.HTTP_201_CREATED,
)
async def run_valuation(
    request: Request,
    payload: ValuationRequest,
) -> dict:
    """
    Execute valuation flow.

    Purpose:
    - Consume immutable snapshot
    - Run controlled valuation pipeline
    - Produce valuation result for review

    NOTE:
    This endpoint does NOT:
    - Decide acceptance
    - Adjust price
    - Apply human override
    """
    request_id = getattr(request.state, "request_id", None)

    service = ValuationService()
    valuation_result = service.run_valuation(
        valuation_request=payload,
        request_id=request_id,
    )

    return {
        "valuation_id": valuation_result.valuation_id,
        "result": valuation_result.model_dump(),
        "metadata": Metadata(
            request_id=request_id,
        ).model_dump(),
    }


@router.get(
    "/{valuation_id}",
    summary="Get valuation result",
)
async def get_valuation(
    valuation_id: str,
    request: Request,
) -> dict:
    """
    Retrieve valuation result.

    Purpose:
    - Review
    - Audit
    - Reporting

    NOTE:
    Returned data is immutable and AS-IS.
    """
    request_id = getattr(request.state, "request_id", None)

    service = ValuationService()
    valuation_result = service.get_valuation(
        valuation_id=valuation_id,
        request_id=request_id,
    )

    return valuation_result.model_dump()
