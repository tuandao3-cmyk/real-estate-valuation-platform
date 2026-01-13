# Module: data/lineage/data_provenance.py
# Part of Advanced AVM System

"""
data_provenance.py

GOVERNANCE STATUS:
- Role: Canonical Data Provenance Registry (FACT-ONLY)
- Spec Authority: MASTER_SPEC.md
- Risk Classification: NHÓM A – Legal / Audit Critical
- Decision Power: NONE
- Intelligence Level: ZERO

Purpose:
- Record and expose explicit data provenance facts
- Provide immutable evidence of data origin & transformation chain
- Support audit, reproducibility, and legal defensibility

IMPORTANT:
- Provenance is DECLARED, never inferred
- This module does NOT discover, guess, or derive provenance
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import hashlib


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class ProvenanceRecord:
    """
    Single provenance fact for one artifact.
    """
    artifact_name: str
    artifact_hash: str
    source_type: str              # raw_input / external_feed / manual_entry / derived
    source_refs: List[str]        # explicit references only
    transformation_step: str      # descriptive label, no logic
    recorded_at_utc: str
    governance_level: str         # NHÓM A / B / C
    immutable: bool = True


@dataclass(frozen=True)
class ProvenanceEntry:
    """
    Canonical, auditable provenance entry.
    """
    record: ProvenanceRecord
    provenance_hash: str          # deterministic, audit-grade


# =========================
# Provenance Registry
# =========================

class DataProvenanceRegistry:
    """
    Append-only provenance registry.

    RULES (ABSOLUTE):
    - No mutation
    - No inference
    - No enrichment
    """

    def __init__(self) -> None:
        self._entries: Dict[str, ProvenanceEntry] = {}

    # -------------------------
    # Public API
    # -------------------------

    def register_provenance(
        self,
        *,
        artifact_name: str,
        artifact_hash: str,
        source_type: str,
        source_refs: List[str],
        transformation_step: str,
        governance_level: str
    ) -> ProvenanceEntry:
        """
        Register a provenance fact.

        Preconditions:
        - All sources must be explicitly provided
        - transformation_step is descriptive only
        """

        if artifact_name in self._entries:
            raise ValueError(
                f"Provenance for artifact '{artifact_name}' already exists. "
                "Provenance records are immutable."
            )

        recorded_at = datetime.utcnow().isoformat()

        record = ProvenanceRecord(
            artifact_name=artifact_name,
            artifact_hash=artifact_hash,
            source_type=source_type,
            source_refs=source_refs,
            transformation_step=transformation_step,
            recorded_at_utc=recorded_at,
            governance_level=governance_level,
        )

        provenance_hash = _hash_provenance(record)

        entry = ProvenanceEntry(
            record=record,
            provenance_hash=provenance_hash
        )

        self._entries[artifact_name] = entry
        return entry

    def get_provenance(self, artifact_name: str) -> Optional[ProvenanceEntry]:
        """
        Read-only provenance lookup.
        """
        return self._entries.get(artifact_name)

    def list_artifacts(self) -> List[str]:
        """
        List artifacts with registered provenance.
        """
        return sorted(self._entries.keys())


# =========================
# Deterministic Hashing
# =========================

def _hash_provenance(record: ProvenanceRecord) -> str:
    """
    Produce deterministic provenance hash for audit & replay.
    """
    payload = (
        f"{record.artifact_name}|"
        f"{record.artifact_hash}|"
        f"{record.source_type}|"
        f"{record.source_refs}|"
        f"{record.transformation_step}|"
        f"{record.recorded_at_utc}|"
        f"{record.governance_level}|"
        f"{record.immutable}"
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# =========================
# Compliance Guardrails
# =========================

__all__ = [
    "ProvenanceRecord",
    "ProvenanceEntry",
    "DataProvenanceRegistry",
]
