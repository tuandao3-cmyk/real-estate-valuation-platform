# ============================================================
# FEATURE VERSIONING REGISTRY
# File: feature_pipeline/registry/feature_versioning.py
#
# Governance Level:
#   NHÓM A – Audit / Feature Immutability
#
# Role:
#   Deterministic feature version tracking and validation
#
# MASTER_SPEC COMPLIANCE:
# - No feature mutation
# - No business logic
# - No valuation impact
# ============================================================

from dataclasses import dataclass
from typing import Dict
import hashlib
import json


class FeatureVersioningViolation(Exception):
    """Raised when feature versioning governance is violated."""
    pass


@dataclass(frozen=True)
class FeatureVersion:
    """
    Immutable representation of a feature version.

    Governance:
    - Read-only
    - Hashable
    - Audit-safe
    """
    feature_id: str
    version: str
    schema_version: str
    owner_role: str
    description: str
    created_at_utc: str


class FeatureVersionRegistry:
    """
    Registry responsible for feature version tracking.

    ❌ Does NOT:
    - Create features
    - Modify features
    - Decide feature usage

    ✅ Does:
    - Register immutable versions
    - Produce deterministic version hash
    - Validate version consistency
    """

    def __init__(self) -> None:
        self._registry: Dict[str, FeatureVersion] = {}

    def register_feature_version(self, feature: FeatureVersion) -> str:
        """
        Register a new feature version.

        Governance rules:
        - Feature ID + version must be unique
        - Re-registration is forbidden
        """

        registry_key = f"{feature.feature_id}:{feature.version}"

        if registry_key in self._registry:
            raise FeatureVersioningViolation(
                f"Feature version already registered: {registry_key}"
            )

        self._registry[registry_key] = feature
        return self._generate_version_hash(feature)

    def get_feature_version(self, feature_id: str, version: str) -> FeatureVersion:
        registry_key = f"{feature_id}:{version}"

        if registry_key not in self._registry:
            raise FeatureVersioningViolation(
                f"Feature version not found: {registry_key}"
            )

        return self._registry[registry_key]

    def _generate_version_hash(self, feature: FeatureVersion) -> str:
        """
        Deterministic SHA-256 hash for audit & reproducibility.
        """

        payload = {
            "feature_id": feature.feature_id,
            "version": feature.version,
            "schema_version": feature.schema_version,
            "owner_role": feature.owner_role,
            "description": feature.description,
            "created_at_utc": feature.created_at_utc,
        }

        canonical_json = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )

        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    def list_registered_versions(self) -> Dict[str, FeatureVersion]:
        """
        Read-only snapshot of registered feature versions.
        """
        return dict(self._registry)


# ============================================================
# GOVERNANCE NOTE
#
# - FeatureVersionRegistry is NOT a source of truth for valuation
# - valuation_dossier.json OVERRIDES ALL
# - This registry exists purely for traceability & audit
#
# END OF FILE
# ============================================================
