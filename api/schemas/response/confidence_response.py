"""
api/schemas/response/confidence_response.py

GOVERNANCE NOTICE
-----------------
This file defines the canonical confidence response schema.

IMPORTANT:
- Confidence is a RISK & CONSISTENCY SIGNAL, NOT a decision
- Confidence does NOT represent accuracy or approval likelihood
- This schema contains NO valuation logic

Any violation constitutes a SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, conint, confloat


class ConfidenceResponse(BaseModel):
    """
    Confidence signal returned by the valuation system.

    Purpose:
    - Communicate data & model agreement quality
    - Act as a governance gate for human review
    - Support audit and explainability

    This schema MUST NOT:
    - Recommend approval or rejection
    - Adjust valuation values
    - Encode decision logic
    """

    confidence_score: confloat(ge=0.0, le=1.0) = Field(
        ...,
        description=(
            "Normalized confidence score in range [0.0, 1.0]. "
            "Represents model agreement and data quality only."
        ),
        examples=[0.72],
    )

    confidence_level: conint(ge=1, le=5) = Field(
        ...,
        description=(
            "Discrete confidence tier (1–5). "
            "Used for workflow gating, NOT decision making."
        ),
        examples=[3],
    )

    dispersion_index: Optional[confloat(ge=0.0)] = Field(
        None,
        description=(
            "Optional dispersion indicator across model outputs. "
            "Higher values indicate lower agreement."
        ),
        examples=[0.18],
    )

    data_quality_score: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None,
        description=(
            "Optional normalized score reflecting input data completeness "
            "and reliability."
        ),
        examples=[0.81],
    )

    requires_human_review: bool = Field(
        ...,
        description=(
            "Governance flag indicating whether human review is REQUIRED. "
            "This is a control signal, NOT an approval or rejection."
        ),
        examples=[True],
    )

    confidence_version: str = Field(
        ...,
        description=(
            "Version identifier of the confidence computation logic. "
            "Used for audit traceability and reproducibility."
        ),
        examples=["confidence_v1.0.0"],
    )

    model_config = ConfigDict(
        frozen=True,               # Immutable after creation
        extra="forbid",             # Strict schema enforcement
        validate_assignment=False,  # Prevent runtime mutation
    )
