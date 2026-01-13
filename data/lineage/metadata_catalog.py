# Module: data/lineage/metadata_catalog.py
# Part of Advanced AVM System

"""
metadata_catalog.py

GOVERNANCE STATUS:
- Role: Canonical Metadata & Lineage Registry (FACT-ONLY)
- Spec Authority: MASTER_SPEC.md
- Decision Power: NONE
- Intelligence Level: ZERO

Purpose:
- Register and expose immutable metadata about data artifacts
- Provide explicit lineage references (declared, not inferred)
- Support audit, reproducibility, and legal traceability

IMPORTANT:
- This module NEVER infers lineage
- Lineage must be explicitly declared upstream
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import hashlib


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class ArtifactMetadata:
    artifact_name: str
    artifact_type: str            # raw / cleaned / feature / signal / audit
    version: str
    content_hash: str
    created_at_utc: str
    source_artifacts: List[str]   # explicit lineage
    owner_component: str
    governance_level: str         # NHÓM A / B / C
    immutable: bool = True


@dataclass(frozen=True)
class MetadataRecord:
    artifact_metadata: ArtifactMetadata
    metadata_hash: str            # reproducibility & audit


# =========================
# Metadata Catalog
# =========================

class MetadataCatalog:
    """
    Canonical in-memory metadata registry.

    RULES:
    - Append-only
    - No mutation
    - No inference
    """

    def __init__(self) -> None:
        self._records: Dict[str, MetadataRecord] = {}

    # -------------------------
    # Public API
    # -------------------------

    def register_artifact(
        self,
        *,
        artifact_name: str,
        artifact_type: str,
        version: str,
        content_hash: str,
        source_artifacts: List[str],
        owner_component: str,
        governance_level: str
    ) -> MetadataRecord:
        """
        Register artifact metadata as a FACT.

        Preconditions:
        - All lineage must be explicitly provided
        - No auto-discovery
        """

        if artifact_name in self._records:
            raise ValueError(
                f"Artifact '{artifact_name}' already registered. "
                "Metadata is immutable."
            )

        created_at = datetime.utcnow().isoformat()

        metadata = ArtifactMetadata(
            artifact_name=artifact_name,
            artifact_type=artifact_type,
            version=version,
            content_hash=content_hash,
            created_at_utc=created_at,
            source_artifacts=source_artifacts,
            owner_component=owner_component,
            governance_level=governance_level,
        )

        metadata_hash = _hash_metadata(metadata)

        record = MetadataRecord(
            artifact_metadata=metadata,
            metadata_hash=metadata_hash
        )

        self._records[artifact_name] = record
        return record

    def get_metadata(self, artifact_name: str) -> Optional[MetadataRecord]:
        """
        Read-only metadata lookup.
        """
        return self._records.get(artifact_name)

    def list_artifacts(self) -> List[str]:
        """
        List registered artifact names.
        """
        return sorted(self._records.keys())

    def lineage_of(self, artifact_name: str) -> List[str]:
        """
        Return explicitly declared lineage.
        NEVER inferred.
        """
        record = self.get_metadata(artifact_name)
        if not record:
            return []
        return list(record.artifact_metadata.source_artifacts)


# =========================
# Deterministic Hashing
# =========================

def _hash_metadata(metadata: ArtifactMetadata) -> str:
    """
    Produce deterministic hash for audit & reproducibility.
    """
    payload = (
        f"{metadata.artifact_name}|"
        f"{metadata.artifact_type}|"
        f"{metadata.version}|"
        f"{metadata.content_hash}|"
        f"{metadata.created_at_utc}|"
        f"{metadata.source_artifacts}|"
        f"{metadata.owner_component}|"
        f"{metadata.governance_level}|"
        f"{metadata.immutable}"
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# =========================
# Compliance Guardrails
# =========================

__all__ = [
    "ArtifactMetadata",
    "MetadataRecord",
    "MetadataCatalog",
]
