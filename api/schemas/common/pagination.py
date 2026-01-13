"""
api/schemas/common/pagination.py

GOVERNANCE NOTICE
-----------------
This file defines PAGINATION SCHEMA for API responses.

- Transport metadata only
- No business logic
- No inference
- No decision authority

Violation of this contract = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PaginationMeta(BaseModel):
    """
    Pagination metadata for list-based API responses.

    Purpose:
    - Support client-side navigation
    - Provide transparent response context

    Pagination MUST NOT be used for:
    - Approval logic
    - Risk evaluation
    - Model routing
    - Valuation decisions
    """

    page: int = Field(
        ...,
        ge=1,
        description="Current page number (1-indexed).",
        examples=[1],
    )

    page_size: int = Field(
        ...,
        ge=1,
        description="Number of items per page.",
        examples=[20],
    )

    total_items: Optional[int] = Field(
        None,
        ge=0,
        description="Total number of available items, if known.",
        examples=[245],
    )

    total_pages: Optional[int] = Field(
        None,
        ge=0,
        description="Total number of pages, if total_items is known.",
        examples=[13],
    )

    has_next: Optional[bool] = Field(
        None,
        description="Indicates whether a next page exists. Informational only.",
        examples=[True],
    )

    has_previous: Optional[bool] = Field(
        None,
        description="Indicates whether a previous page exists. Informational only.",
        examples=[False],
    )

    model_config = ConfigDict(
        frozen=True,               # Enforce immutability
        extra="forbid",             # Disallow undeclared fields
        validate_assignment=False,  # Prevent runtime mutation
    )
