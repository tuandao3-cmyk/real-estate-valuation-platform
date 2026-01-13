"""
api/schemas/common/metadata.py

GOVERNANCE NOTICE
-----------------
This file defines COMMON METADATA SCHEMA used across the system.

- Schema only
- No business logic
- No inference
- No decision authority

Violation of this contract = SYSTEM VIOLATION (MASTER_SPEC.md)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ArtifactMetadata(BaseModel):
    """
    Canonical metadata attached to every system artifact.

    Purpose:
    - Audit traceability
    - Reproducibility
    - Legal defensibility

    This metadata MUST NOT influence valuation, approval, or confidence.
    """

    artifact_id: str = Field(
        ...,
        description="Globally unique identifier of the artifact (UUID or hash-based ID).",
        examples=["feature_snapshot_2026_01_12_abcd1234"],
    )

    artifact_type: str = Field(
        ...,
        description="Logical type of artifact (feature_snapshot, model_output, ensemble_output, report, etc.).",
        examples=["model_output"],
    )

    created_at: datetime = Field(
        ...,
        description="UTC timestamp when the artifact was created.",
    )

    created_by: str = Field(
        ...,
        description="System component or service name that produced this artifact.",
        examples=["hedonic_model_v1"],
    )

    model_id: Optional[str] = Field(
        None,
        description="Model identifier if artifact is model-related. Must exist in model_registry.",
        examples=["hedonic_v1"],
    )

    model_version: Optional[str] = Field(
        None,
        description="Exact model version used to generate this artifact.",
        examples=["1.0.3"],
    )

    feature_snapshot_hash: Optional[str] = Field(
        None,
        description="Hash of the feature snapshot used. Required for any model or ensemble output.",
        examples=["sha256:9f2c..."],
    )

    schema_version: str = Field(
        ...,
        description="Schema version of the artifact payload.",
        examples=["1.0"],
    )

    source_commit: Optional[str] = Field(
        None,
        description="Source control commit hash of the producing codebase.",
        examples=["a9c3f2d"],
    )

    notes: Optional[str] = Field(
        None,
        description="Free-text technical notes. MUST NOT contain decisions, approvals, or recommendations.",
        max_length=500,
    )

    model_config = ConfigDict(
        frozen=True,               # Enforce immutability
        extra="forbid",             # No undeclared fields
        validate_assignment=False,  # Prevent runtime mutation
    )
