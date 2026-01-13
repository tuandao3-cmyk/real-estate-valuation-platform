"""
COMPARABLE CONTEXT MODEL
=======================

Role:
- Package similarity + affinity signals into a canonical,
  non-decisive comparable context artifact.

Governance:
- READ-ONLY
- DESCRIPTIVE ONLY
- NO SELECTION
- NO RANKING
- NO SCORING
- NO PRICE INTERACTION

Compliance:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – ADVANCED AVM

Any attempt to derive price, ranking, or decision
from this module → SYSTEM VIOLATION
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import hashlib
import json


# -------------------------------------------------------------------
# Data Contracts
# -------------------------------------------------------------------

@dataclass(frozen=True)
class ComparableContext:
    """
    Canonical comparable context for ONE comparable property.

    This object is:
    - Deterministic
    - Immutable
    - Audit-friendly
    """
    target_property_id: str
    comparable_property_id: str
    similarity_signals: Dict[str, Any]
    affinity_signals: Dict[str, Any]
    context_hash: str


@dataclass(frozen=True)
class ComparableContextSet:
    """
    Collection wrapper for multiple comparable contexts.

    NOTE:
    - Order is preserved as input order
    - Order has NO semantic meaning
    """
    target_property_id: str
    comparables: List[ComparableContext]
    set_hash: str


# -------------------------------------------------------------------
# Hashing Utilities (Deterministic)
# -------------------------------------------------------------------

def _stable_hash(payload: Dict[str, Any]) -> str:
    """
    Produce a stable SHA-256 hash for audit & reproducibility.

    Governance:
    - Key-sorted
    - JSON-serialized
    - No randomness
    """
    serialized = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


# -------------------------------------------------------------------
# Comparable Context Builder
# -------------------------------------------------------------------

class ComparableContextBuilder:
    """
    Build ComparableContext objects from upstream signals.

    Upstream Assumptions:
    - similarity_signals are produced by similarity_features.py
    - affinity_signals are produced by comp_weighting.py

    This class performs:
    - Structural validation
    - Deterministic packaging
    """

    @staticmethod
    def build(
        *,
        target_property_id: str,
        comparable_property_id: str,
        similarity_signals: Dict[str, Any],
        affinity_signals: Dict[str, Any],
    ) -> ComparableContext:
        """
        Build a single comparable context.

        Forbidden:
        - Any transformation of meaning
        - Any aggregation
        - Any filtering
        """

        payload = {
            "target_property_id": target_property_id,
            "comparable_property_id": comparable_property_id,
            "similarity_signals": similarity_signals,
            "affinity_signals": affinity_signals,
        }

        context_hash = _stable_hash(payload)

        return ComparableContext(
            target_property_id=target_property_id,
            comparable_property_id=comparable_property_id,
            similarity_signals=similarity_signals,
            affinity_signals=affinity_signals,
            context_hash=context_hash,
        )


# -------------------------------------------------------------------
# Context Set Builder (NO SEMANTIC ORDER)
# -------------------------------------------------------------------

def build_comparable_context_set(
    *,
    target_property_id: str,
    comparable_payloads: List[Dict[str, Any]],
) -> ComparableContextSet:
    """
    Build a ComparableContextSet for a target property.

    comparable_payloads item schema:
    {
        "comparable_property_id": str,
        "similarity_signals": Dict,
        "affinity_signals": Dict
    }

    Governance Guarantees:
    - No sorting
    - No ranking
    - No pruning
    """

    contexts: List[ComparableContext] = []

    for item in comparable_payloads:
        contexts.append(
            ComparableContextBuilder.build(
                target_property_id=target_property_id,
                comparable_property_id=item["comparable_property_id"],
                similarity_signals=item["similarity_signals"],
                affinity_signals=item["affinity_signals"],
            )
        )

    set_payload = {
        "target_property_id": target_property_id,
        "context_hashes": [c.context_hash for c in contexts],
    }

    set_hash = _stable_hash(set_payload)

    return ComparableContextSet(
        target_property_id=target_property_id,
        comparables=contexts,
        set_hash=set_hash,
    )
