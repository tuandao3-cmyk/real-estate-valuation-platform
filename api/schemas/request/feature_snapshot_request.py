"""
api/schemas/request/feature_snapshot_request.py

GOVERNANCE NOTICE
-----------------
This file defines the REQUEST SCHEMA for creating a feature snapshot.

- Request declaration only
- No feature engineering
- No validation beyond type / presence
- No decision authority

Violation of this contract = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class FeatureSnapshotRequest(BaseModel):
    """
    Request schema for feature snapshot creation.

    Purpose:
    - Declare valuation intent
    - Provide raw, pre-feature-engineering inputs
    - Anchor audit trail before feature pipeline execution

    This request MUST NOT:
    - Contain engineered features
    - Contain inferred or derived values
    - Influence valuation or approval logic
    """

    valuation_id: str = Field(
        ...,
        description="Unique identifier of the valuation session this snapshot belongs to.",
        examples=["valuation_2026_01_12_001"],
    )

    property_id: str = Field(
        ...,
        description="Unique identifier of the property under valuation.",
        examples=["property_hcm_abc123"],
    )

    raw_inputs: Dict[str, Any] = Field(
        ...,
        description=(
            "Raw input payload as received from upstream systems or user submission. "
            "Must represent unprocessed data only."
        ),
        examples=[
            {
                "address": "123 Nguyen Trai, District 1, HCMC",
                "land_area": 85,
                "building_area": 240,
                "num_floors": 4,
                "images": ["img_001.jpg", "img_002.jpg"],
            }
        ],
    )

    source_system: str = Field(
        ...,
        description="Originating system or channel providing the raw inputs.",
        examples=["internal_los", "manual_appraiser_entry"],
    )

    requester_id: Optional[str] = Field(
        None,
        description="Identifier of the human or system requesting snapshot creation.",
        examples=["user_789"],
    )

    request_notes: Optional[str] = Field(
        None,
        description=(
            "Optional technical notes about the request. "
            "MUST NOT contain valuation judgment, approval intent, or recommendations."
        ),
        max_length=500,
    )

    model_config = ConfigDict(
        frozen=True,               # Request object must be immutable once created
        extra="forbid",             # Disallow undeclared fields
        validate_assignment=False,  # Prevent runtime mutation
    )
