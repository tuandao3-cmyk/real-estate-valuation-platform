"""
api/schemas/response/error_response.py

GOVERNANCE NOTICE
-----------------
This file defines the canonical API error response schema.

- Error responses are descriptive, not prescriptive
- Errors do NOT imply valuation rejection or approval
- No business or valuation logic is allowed

Violation of this contract = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ErrorResponse(BaseModel):
    """
    Standardized API error response.

    Purpose:
    - Provide structured, audit-friendly error information
    - Enable deterministic client handling
    - Preserve legal defensibility

    This schema MUST NOT:
    - Trigger workflow decisions
    - Encode approval / rejection semantics
    - Leak internal system logic
    """

    error_code: str = Field(
        ...,
        description=(
            "Stable, standardized error identifier. "
            "Used for client handling and audit reference."
        ),
        examples=["VALIDATION_ERROR", "SCHEMA_MISMATCH", "POLICY_VIOLATION"],
    )

    error_message: str = Field(
        ...,
        description=(
            "Human-readable description of the error. "
            "Must be neutral, factual, and non-prescriptive."
        ),
        examples=["Request payload does not match required schema."],
    )

    error_context: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Optional contextual metadata to assist debugging. "
            "Must not contain sensitive data, valuation logic, "
            "or internal decision signals."
        ),
        examples=[{"field": "valuation_hash", "issue": "missing"}],
    )

    trace_id: Optional[str] = Field(
        None,
        description=(
            "Optional trace identifier linking the error to a workflow "
            "or audit trace record."
        ),
        examples=["trace_2026_01_12_abcd1234"],
    )

    model_config = ConfigDict(
        frozen=True,               # Immutable once created
        extra="forbid",             # Disallow undeclared fields
        validate_assignment=False,  # Prevent runtime mutation
    )
