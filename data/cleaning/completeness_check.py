"""
completeness_check.py

GOVERNANCE STATUS:
- Role: Data Completeness Signal Generator (NON-INTELLIGENT)
- Spec: MASTER_SPEC.md (Role Separation, Data Immutability)
- Decision Power: NONE
- Auto-fix / Inference: FORBIDDEN

Purpose:
- Check presence of mandatory fields
- Produce completeness signals ONLY
- NEVER modify or enrich data
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import hashlib


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class CompletenessSignal:
    record_id: str
    missing_fields: List[str]
    completeness_ratio: float     # purely arithmetic
    severity: str                 # low / medium / high
    signal_hash: str              # audit & reproducibility


# =========================
# Public API
# =========================

def check_completeness(
    records: List[Dict[str, Any]],
    required_fields: List[str]
) -> List[CompletenessSignal]:
    """
    Rule-based completeness check.

    Rules:
    - Field is missing if key absent OR value is None OR empty string
    - No inference
    - No auto-correction
    """

    signals: List[CompletenessSignal] = []

    total_required = len(required_fields)
    if total_required == 0:
        return signals

    for record in records:
        record_id = str(record.get("id"))

        missing = [
            field for field in required_fields
            if _is_missing(record.get(field))
        ]

        if not missing:
            continue

        ratio = (total_required - len(missing)) / total_required
        severity = _severity_by_ratio(ratio)

        signals.append(
            _build_signal(
                record_id=record_id,
                missing_fields=missing,
                ratio=ratio,
                severity=severity
            )
        )

    return signals


# =========================
# Helpers (Deterministic)
# =========================

def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _severity_by_ratio(ratio: float) -> str:
    """
    Deterministic severity classification.
    """
    if ratio < 0.5:
        return "high"
    if ratio < 0.8:
        return "medium"
    return "low"


def _build_signal(
    record_id: str,
    missing_fields: List[str],
    ratio: float,
    severity: str
) -> CompletenessSignal:
    raw = f"{record_id}|{missing_fields}|{ratio}|{severity}"
    signal_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    return CompletenessSignal(
        record_id=record_id,
        missing_fields=missing_fields,
        completeness_ratio=ratio,
        severity=severity,
        signal_hash=signal_hash
    )


# =========================
# Compliance Guardrails
# =========================

__all__ = [
    "CompletenessSignal",
    "check_completeness",
]
