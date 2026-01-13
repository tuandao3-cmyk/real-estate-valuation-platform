"""
api/routers/admin_router.py

GOVERNANCE NOTICE
-----------------
Administrative router for audit, compliance, and system visibility.

STRICT CONSTRAINTS:
- Read-only
- No execution control
- No valuation logic
- No model activation
"""

from fastapi import APIRouter, Request, status

from api.schemas.common.metadata import Metadata
from api.schemas.common.pagination import Pagination
from api.services.audit_service import AuditService
from api.services.report_service import ReportService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get(
    "/system/status",
    summary="Get system governance status",
    status_code=status.HTTP_200_OK,
)
async def get_system_status(request: Request) -> dict:
    """
    Retrieve high-level system governance status.

    Purpose:
    - Operational visibility
    - Audit readiness check
    - Compliance monitoring

    NOTE:
    Status is descriptive only, not a health approval.
    """
    request_id = getattr(request.state, "request_id", None)

    audit_service = AuditService()
    status_info = audit_service.get_system_status(
        request_id=request_id,
    )

    return {
        "status": status_info.model_dump(),
        "metadata": Metadata(
            request_id=request_id,
        ).model_dump(),
    }


@router.get(
    "/audit/logs",
    summary="List audit logs",
    status_code=status.HTTP_200_OK,
)
async def list_audit_logs(
    request: Request,
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """
    List audit log entries.

    Purpose:
    - Regulatory inspection
    - Dispute resolution
    - Historical traceability

    NOTE:
    Logs are append-only and immutable.
    """
    request_id = getattr(request.state, "request_id", None)

    audit_service = AuditService()
    logs, total = audit_service.list_audit_logs(
        page=page,
        page_size=page_size,
        request_id=request_id,
    )

    return {
        "items": [log.model_dump() for log in logs],
        "pagination": Pagination(
            page=page,
            page_size=page_size,
            total_items=total,
        ).model_dump(),
        "metadata": Metadata(
            request_id=request_id,
        ).model_dump(),
    }


@router.get(
    "/reports",
    summary="List all reports (admin view)",
    status_code=status.HTTP_200_OK,
)
async def list_all_reports(
    request: Request,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """
    Admin-level report discovery endpoint.

    Purpose:
    - Oversight
    - Audit preparation
    - Workflow supervision

    NOTE:
    This endpoint does NOT modify or regenerate reports.
    """
    request_id = getattr(request.state, "request_id", None)

    report_service = ReportService()
    reports, total = report_service.list_reports(
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
