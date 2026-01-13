"""
api/schemas/request/valuation_request.py

GOVERNANCE NOTICE
-----------------
This file defines the REQUEST SCHEMA for initiating a valuation.

- Declaration of intent only
- No valuation logic
- No inference
- No approval or decision authority

Violation of this contract = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class ValuationRequest(BaseModel):
    """
    Request schema for initiating a valuation process.

    Purpose:
    - Declare valuation intent
    - Define scope and purpose
    - Anchor audit trail before any model execution

    This request MUST NOT:
    - Contain price expectations
    - Influence valuation outcomes
    - Bypass rule or human review
    """

    valuation_id: str = Field(
        ...,
        description="Globally unique identifier for this valuation run.",
        examples=["valuation_2026_01_12_0001"],
    )

    property_id: str = Field(
        ...,
        description="Unique identifier of the property to be valued.",
        examples=["property_hcm_abc123"],
    )

    valuation_purpose: Literal[
        "credit_assessment",
        "internal_review",
        "risk_monitoring",
        "collateral_reference",
        "other",
    ] = Field(
        ...,
        description=(
            "Declared purpose of the valuation. "
            "Used for governance, routing permission, and audit context only."
        ),
        examples=["credit_assessment"],
    )

    requested_by: str = Field(
        ...,
        description="Identifier of the requesting human role or system.",
        examples=["credit_officer_001"],
    )

    request_channel: Optional[str] = Field(
        None,
        description="Channel through which the valuation request is initiated.",
        examples=["los_system", "manual_appraiser_ui"],
    )

    jurisdiction: Optional[str] = Field(
        None,
        description=(
            "Legal or regulatory jurisdiction applicable to this valuation. "
            "Used for policy enforcement only."
        ),
        examples=["VN"],
    )

    valuation_notes: Optional[str] = Field(
        None,
        description=(
            "Optional contextual notes for the valuation request. "
            "MUST NOT include target price, approval intent, or decision hints."
        ),
        max_length=500,
    )

    model_config = ConfigDict(
        frozen=True,               # Enforce immutability
        extra="forbid",             # Disallow undeclared fields
        validate_assignment=False,  # Prevent runtime mutation
    )
