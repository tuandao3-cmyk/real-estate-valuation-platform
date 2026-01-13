"""
api/schemas/response/valuation_response.py

GOVERNANCE NOTICE
-----------------
This file defines the canonical valuation response schema.

IMPORTANT LEGAL NOTICE:
- This response does NOT represent an approved value
- This response does NOT replace human appraisal
- This response contains NO decision logic

Any deviation constitutes a SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, confloat

from api.schemas.response.confidence_response import ConfidenceResponse


class ValuationResponse(BaseModel):
    """
    Canonical valuation output schema.

    Purpose:
    - Expose AVM-derived valuation results
    - Preserve transparency & uncertainty
    - Enable downstream rule checks and human review

    This schema MUST NOT:
    - Decide approval or rejection
    - Hide dispersion or risk
    - Encode policy logic
    """

    valuation_amount: confloat(gt=0.0) = Field(
        ...,
        description=(
            "Primary valuation figure produced by ensemble aggregation. "
            "This is NOT a final or approved value."
        ),
        examples=[3_450_000_000.0],
    )

    currency: str = Field(
        ...,
        description="ISO currency code of the valuation amount.",
        examples=["VND"],
        min_length=3,
        max_length=3,
    )

    valuation_range_min: Optional[confloat(gt=0.0)] = Field(
        None,
        description=(
            "Optional lower bound of the valuation range, "
            "reflecting model dispersion and risk adjustment."
        ),
        examples=[3_100_000_000.0],
    )

    valuation_range_max: Optional[confloat(gt=0.0)] = Field(
        None,
        description=(
            "Optional upper bound of the valuation range, "
            "reflecting model dispersion and risk adjustment."
        ),
        examples=[3_800_000_000.0],
    )

    valuation_basis: str = Field(
        ...,
        description=(
            "Textual description of the valuation basis "
            "(e.g. market value, lending value). "
            "Must align with valuation policy."
        ),
        examples=["Market Value – Income & Comparable Approach"],
    )

    confidence: ConfidenceResponse = Field(
        ...,
        description=(
            "Confidence signal associated with this valuation. "
            "Used strictly for governance gating."
        ),
    )

    valuation_metadata: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Optional metadata describing valuation context "
            "(e.g. model set, valuation date, scenario tag). "
            "Must not contain decisions or sensitive logic."
        ),
        examples=[{"valuation_date": "2026-01-12", "model_set": "ensemble_v2"}],
    )

    valuation_version: str = Field(
        ...,
        description=(
            "Version identifier of the valuation computation pipeline. "
            "Ensures reproducibility and audit traceability."
        ),
        examples=["valuation_v2.3.1"],
    )

    model_config = ConfigDict(
        frozen=True,               # Immutable, audit-safe
        extra="forbid",             # Strict schema enforcement
        validate_assignment=False,  # Prevent runtime mutation
    )
