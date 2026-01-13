"""
deduplicate.py

GOVERNANCE STATUS:
- Role: Deterministic Duplicate Detector (SIGNAL ONLY)
- Spec: MASTER_SPEC.md (Role Separation + Data Immutability)
- Decision Power: NONE
- Learning: FORBIDDEN

Purpose:
- Detect potential duplicate records
- Produce duplicate groups & flags
- NEVER merge, drop, or overwrite raw data
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import hashlib


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class DuplicateSignal:
    record_id: str
    duplicate_group_id: str
    match_keys: Tuple[str, ...]
    confidence: float          # deterministic score (rule-based)
    signal_hash: str           # audit / reproducibility


# =========================
# Core Public API
# =========================

def detect_duplicates(
    records: List[Dict[str, Any]],
    key_fields: List[str]
) -> List[DuplicateSignal]:
    """
    Detect duplicates using strict key matching.

    Rules:
    - Only exact match on provided key_fields
    - No fuzzy logic
    - No partial inference
    - Missing key => record excluded from grouping

    Output:
    - DuplicateSignal list
    """

    index: Dict[str, List[Dict[str, Any]]] = {}

    for record in records:
        key = _build_dedup_key(record, key_fields)
        if key is None:
            continue

        index.setdefault(key, []).append(record)

    signals: List[DuplicateSignal] = []

    for dedup_key, group in index.items():
        if len(group) < 2:
            continue

        group_id = _hash_value(dedup_key)

        for record in group:
            signals.append(
                _build_signal(
                    record_id=str(record.get("id")),
                    group_id=group_id,
                    match_keys=tuple(key_fields),
                    group_size=len(group)
                )
            )

    return signals


# =========================
# Helpers (Deterministic)
# =========================

def _build_dedup_key(
    record: Dict[str, Any],
    key_fields: List[str]
) -> str | None:
    """
    Build a strict deduplication key.

    If any key field is missing or null => return None
    """
    values = []

    for field in key_fields:
        value = record.get(field)
        if value is None:
            return None
        values.append(str(value).strip().lower())

    raw_key = "|".join(values)
    return _hash_value(raw_key)


def _build_signal(
    record_id: str,
    group_id: str,
    match_keys: Tuple[str, ...],
    group_size: int
) -> DuplicateSignal:
    """
    Deterministic duplicate signal builder.
    """

    confidence = _confidence_by_group_size(group_size)

    signal_hash = _hash_value(
        f"{record_id}|{group_id}|{match_keys}|{confidence}"
    )

    return DuplicateSignal(
        record_id=record_id,
        duplicate_group_id=group_id,
        match_keys=match_keys,
        confidence=confidence,
        signal_hash=signal_hash
    )


def _confidence_by_group_size(group_size: int) -> float:
    """
    Rule-based confidence.
    NOT statistical accuracy.
    """
    if group_size >= 5:
        return 0.9
    if group_size >= 3:
        return 0.7
    return 0.5


def _hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# =========================
# Compliance Guardrails
# =========================

__all__ = [
    "DuplicateSignal",
    "detect_duplicates",
]
