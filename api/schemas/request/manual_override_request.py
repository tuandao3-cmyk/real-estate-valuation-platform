"""
api/schemas/request/manual_override_request.py

GOVERNANCE NOTICE
-----------------
This file defines the REQUEST schema for a HUMAN-INITIATED manual override.

- Override request ≠ override approval
- No valuation logic
- No decision authority
- Human accountability is mandatory

Violation of this contract = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict


class ManualOverrideRequest(BaseModel):
    """
    Request schema for registering a manual override request.

    Purpose:
    - Record explicit human intent to override
    - Anchor legal accountability
    - Trigger downstream governance workflow

    This schema MUST NOT:
    - Execute override
    - Change valuation outcome
    - Bypass maker-checker or approval flow
    """

    override_request_id: str = Field(
        ...,
        description="Globally unique identifier for this override request.",
        examples=["override_req_2026_01_12_0001"],
    )

    valuation_hash: str = Field(
        ...,
        description=(
            "Hash reference of the valuation_dossier to which this override "
            "request applies. Immutable legal anchor."
        ),
        examples=["a94f1c2e7c8b9d..."],
    )

    actor_id: str = Field(
        ...,
        description="Identifier of the human requesting the override.",
        examples=["appraiser_007"],
    )

    actor_role: Literal[
        "appraiser",
        "senior_appraiser",
        "credit_officer",
        "risk_officer",
        "compliance_officer",
        "other",
    ] = Field(
        ...,
        description="Declared role of the human requesting the override.",
        examples=["senior_appraiser"],
    )

    override_scope: Literal[
        "valuation_output",
        "confidence_projection",
        "workflow_routing",
        "documentation_only",
    ] = Field(
        ...,
        description=(
            "Declared scope of the override request. "
            "Used for governance routing only."
        ),
        examples=["valuation_output"],
    )

    override_reason_code: str = Field(
        ...,
        description=(
            "Standardized override reason code. "
            "Must exist in override_reason_codes.yaml."
        ),
        examples=["MARKET_ANOMALY_OBSERVED"],
    )

    override_explanation: str = Field(
        ...,
        description=(
            "Free-text explanation provided by the human. "
            "Must justify the override request in neutral, factual language."
        ),
        min_length=20,
        max_length=2000,
    )

    evidence_references: Optional[List[str]] = Field(
        None,
        description=(
            "Optional references to supporting evidence "
            "(documents, photos, reports, external IDs). "
            "No binary data allowed."
        ),
        examples=[["doc_legal_123", "photo_set_456"]],
    )

    request_channel: Optional[str] = Field(
        None,
        description="Channel through which the override request is submitted.",
        examples=["internal_appraiser_ui"],
    )

    model_config = ConfigDict(
        frozen=True,               # Immutable once created
        extra="forbid",             # Disallow undeclared fields
        validate_assignment=False,  # Prevent runtime mutation
    )
