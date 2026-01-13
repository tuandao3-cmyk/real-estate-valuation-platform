"""
api/routers/report_router.py

GOVERNANCE NOTICE
-----------------
This router exposes reporting and audit-oriented read APIs.

STRICT CONSTRAINTS:
- Reporting only
- Read-only access
- No valuation logic
- No decision authority
"""

from fastapi import APIRouter, Request, status

from api.schemas.common.metadata import Metadata
from api.schemas.common.pagination import Pagination
from api.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/valuation/{valuation_id}",
    summary="Get valuation report",
    status_code=status.HTTP_200_OK,
)
async def get_valuation_report(
    valuation_id: str,
    request: Request,
) -> dict:
    """
    Retrieve valuation report artifact.

    Purpose:
    - Human review
    - Audit inspection
    - Regulatory evidence

    NOTE:
    Returned report is immutable and non-decisive.
    """
    request_id = getattr(request.state, "request_id", None)

    service = ReportService()
    report = service.get_valuation_report(
        valuation_id=valuation_id,
        request_id=request_id,
    )

    return {
        "report": report.model_dump(),
        "metadata": Metadata(
            request_id=request_id,
        ).model_dump(),
    }


@router.get(
    "",
    summary="List available reports",
    status_code=status.HTTP_200_OK,
)
async def list_reports(
    request: Request,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """
    List existing reports.

    Purpose:
    - Discovery
    - Review workflow
    - Audit navigation

    NOTE:
    No filtering by performance or outcome.
    """
    request_id = getattr(request.state, "request_id", None)

    service = ReportService()
    reports, total = service.list_reports(
        page=page,
        page_size=page_size,
        request_id=request_id,
    )

    return {
        "items": [r.model_dump() for r in reports],
        "pagination": Pagination(
            page=page,
            page_size=page_size,
            total_items=total,
        ).model_dump(),
        "metadata": Metadata(
            request_id=request_id,
        ).model_dump(),
    }
