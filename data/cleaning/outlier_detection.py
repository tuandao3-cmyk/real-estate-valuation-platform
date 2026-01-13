# Module: data/cleaning/outlier_detection.py
# Part of Advanced AVM System

"""
outlier_detection.py

GOVERNANCE STATUS:
- Role: Rule-Based Outlier Signal Generator (NON-INTELLIGENT)
- Spec: MASTER_SPEC.md (Role Separation, Data Immutability)
- Decision Power: NONE
- Learning / Adaptation: FORBIDDEN

Purpose:
- Detect extreme or suspicious numeric values
- Produce OUTLIER SIGNALS ONLY
- NEVER modify, drop, or correct data
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import hashlib
import statistics


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class OutlierSignal:
    record_id: str
    field_name: str
    value: float
    rule_applied: str
    severity: str              # low / medium / high
    signal_hash: str           # audit & reproducibility


# =========================
# Public API
# =========================

def detect_outliers(
    records: List[Dict[str, Any]],
    field_name: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    iqr_multiplier: float = 1.5
) -> List[OutlierSignal]:
    """
    Rule-based outlier detection.

    Rules:
    - Hard bounds (min / max) if provided
    - IQR-based rule (deterministic)
    - No automatic threshold tuning
    """

    values = _collect_numeric_values(records, field_name)
    signals: List[OutlierSignal] = []

    if not values:
        return signals

    q1, q3 = _quartiles(values)
    iqr = q3 - q1
    lower_iqr = q1 - iqr_multiplier * iqr
    upper_iqr = q3 + iqr_multiplier * iqr

    for record in records:
        record_id = str(record.get("id"))
        value = record.get(field_name)

        if not _is_number(value):
            continue

        value = float(value)

        # Rule 1: Hard bounds
        if min_value is not None and value < min_value:
            signals.append(
                _build_signal(
                    record_id,
                    field_name,
                    value,
                    rule="below_min_threshold",
                    severity="high"
                )
            )
            continue

        if max_value is not None and value > max_value:
            signals.append(
                _build_signal(
                    record_id,
                    field_name,
                    value,
                    rule="above_max_threshold",
                    severity="high"
                )
            )
            continue

        # Rule 2: IQR rule
        if value < lower_iqr or value > upper_iqr:
            signals.append(
                _build_signal(
                    record_id,
                    field_name,
                    value,
                    rule="iqr_outlier",
                    severity=_severity_by_distance(value, q1, q3, iqr)
                )
            )

    return signals


# =========================
# Helpers (Deterministic)
# =========================

def _collect_numeric_values(
    records: List[Dict[str, Any]],
    field_name: str
) -> List[float]:
    values: List[float] = []
    for record in records:
        value = record.get(field_name)
        if _is_number(value):
            values.append(float(value))
    return values


def _quartiles(values: List[float]) -> tuple[float, float]:
    """
    Deterministic quartile calculation.
    """
    sorted_vals = sorted(values)
    q1 = statistics.quantiles(sorted_vals, n=4)[0]
    q3 = statistics.quantiles(sorted_vals, n=4)[2]
    return q1, q3


def _severity_by_distance(
    value: float,
    q1: float,
    q3: float,
    iqr: float
) -> str:
    """
    Rule-based severity classification.
    """
    if iqr == 0:
        return "medium"

    if value < q1 - 3 * iqr or value > q3 + 3 * iqr:
        return "high"

    return "medium"


def _build_signal(
    record_id: str,
    field_name: str,
    value: float,
    rule: str,
    severity: str
) -> OutlierSignal:
    raw = f"{record_id}|{field_name}|{value}|{rule}|{severity}"
    signal_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    return OutlierSignal(
        record_id=record_id,
        field_name=field_name,
        value=value,
        rule_applied=rule,
        severity=severity,
        signal_hash=signal_hash
    )


def _is_number(value: Any) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


# =========================
# Compliance Guardrails
# =========================

__all__ = [
    "OutlierSignal",
    "detect_outliers",
]
