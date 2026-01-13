"""
MODEL VERSIONING – ADVANCED AVM
File: modeling/registry/model_versioning.py

LEGAL & GOVERNANCE STATUS
-------------------------
This module enforces model reproducibility and auditability.

A model run is considered VALID if and only if:
- model_version is explicitly declared
- feature_snapshot_hash is present and immutable
- backward compatibility rules are satisfied

MASTER_SPEC COMPLIANCE
---------------------
- No implicit versioning
- No dynamic feature binding
- No silent backward breaking
- valuation_dossier.json is the single source of truth

This module DOES NOT:
- Train models
- Run inference
- Select models
- Modify features
"""

from dataclasses import dataclass
from typing import List, Optional
import hashlib


# ============================================================
# EXCEPTIONS (AUDIT-GRADE)
# ============================================================

class ModelVersioningError(Exception):
    """Base exception for model versioning violations."""


class MissingVersionError(ModelVersioningError):
    pass


class MissingFeatureSnapshotError(ModelVersioningError):
    pass


class BackwardIncompatibilityError(ModelVersioningError):
    pass


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass(frozen=True)
class FeatureSnapshot:
    """
    Represents an immutable snapshot of feature definitions
    used at model inference time.
    """
    feature_set_id: str
    feature_list: List[str]
    schema_version: str

    def compute_hash(self) -> str:
        """
        Computes a deterministic hash for the feature snapshot.
        """
        payload = (
            self.feature_set_id
            + self.schema_version
            + "|".join(sorted(self.feature_list))
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ModelVersionInfo:
    """
    Immutable model version declaration.
    """
    model_id: str
    model_version: str
    feature_snapshot_hash: str
    backward_compatible_versions: List[str]


# ============================================================
# VERSIONING ENFORCER
# ============================================================

class ModelVersioningGuard:
    """
    Enforces reproducibility constraints for model execution.

    This guard must be called BEFORE any model inference.
    """

    @staticmethod
    def validate(
        declared_version: Optional[ModelVersionInfo],
        runtime_feature_snapshot: Optional[FeatureSnapshot],
        previous_model_version: Optional[str] = None,
    ) -> None:
        """
        Validates that a model execution is reproducible and compliant.

        Raises:
            MissingVersionError
            MissingFeatureSnapshotError
            BackwardIncompatibilityError
        """

        # ----------------------------------------------------
        # 1. MODEL VERSION MUST EXIST
        # ----------------------------------------------------
        if declared_version is None:
            raise MissingVersionError(
                "Model execution blocked: model_version is not declared."
            )

        if not declared_version.model_version:
            raise MissingVersionError(
                "Model execution blocked: model_version is empty."
            )

        # ----------------------------------------------------
        # 2. FEATURE SNAPSHOT MUST EXIST & MATCH
        # ----------------------------------------------------
        if runtime_feature_snapshot is None:
            raise MissingFeatureSnapshotError(
                "Model execution blocked: feature snapshot is missing."
            )

        computed_hash = runtime_feature_snapshot.compute_hash()

        if computed_hash != declared_version.feature_snapshot_hash:
            raise MissingFeatureSnapshotError(
                "Feature snapshot hash mismatch. "
                "Reproducibility cannot be guaranteed."
            )

        # ----------------------------------------------------
        # 3. BACKWARD COMPATIBILITY CHECK
        # ----------------------------------------------------
        if previous_model_version:
            if previous_model_version not in declared_version.backward_compatible_versions:
                raise BackwardIncompatibilityError(
                    f"Model version '{declared_version.model_version}' "
                    f"is NOT backward compatible with previous version "
                    f"'{previous_model_version}'."
                )

        # ----------------------------------------------------
        # PASSED ALL CHECKS
        # ----------------------------------------------------
        return


# ============================================================
# AUDIT NOTE (NON-NEGOTIABLE)
# ============================================================
"""
If this guard is bypassed or removed:

- Model outputs become NON-REPRODUCIBLE
- Valuation results become NON-AUDITABLE
- System becomes NON-COMPLIANT with MASTER_SPEC

Any valuation generated without passing ModelVersioningGuard
is INVALID by definition.
"""
