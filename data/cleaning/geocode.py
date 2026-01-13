# Module: data/cleaning/geocode.py
# Part of Advanced AVM System
"""
geocode.py

GOVERNANCE STATUS:
- Role: Deterministic Geocode Mapper (NON-INTELLIGENT)
- Spec: MASTER_SPEC.md (Data Immutability + Role Separation)
- Decision Power: NONE
- External Calls: FORBIDDEN

Purpose:
- Map normalized address -> coordinates
- ONLY via internal reference tables
- NEVER infer, guess, or "fix" addresses
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import hashlib
import json
import os

# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class GeocodeResult:
    latitude: Optional[float]
    longitude: Optional[float]
    source: str               # e.g. "internal_reference"
    confidence: float         # deterministic, NOT ML confidence
    resolution: str           # city / district / ward / street / exact
    geocode_hash: str         # for audit & reproducibility


# =========================
# Internal Reference Loader
# =========================

class InternalGeocodeTable:
    """
    Loads pre-approved internal geocode reference tables.

    Governance:
    - Read-only
    - Versioned
    - No runtime modification
    """

    def __init__(self, table_path: str):
        if not os.path.exists(table_path):
            raise FileNotFoundError(f"Geocode table not found: {table_path}")

        with open(table_path, "r", encoding="utf-8") as f:
            self._table: Dict[str, Dict[str, Any]] = json.load(f)

    def lookup(self, normalized_address: str) -> Optional[Dict[str, Any]]:
        return self._table.get(normalized_address)


# =========================
# Core Geocode Function
# =========================

def geocode_address(
    normalized_address: str,
    geocode_table: InternalGeocodeTable
) -> GeocodeResult:
    """
    Deterministic geocoding using internal reference only.

    Rules:
    - If address not found → return NULL coordinates
    - NEVER fallback to guessing
    - NEVER call external services
    """

    record = geocode_table.lookup(normalized_address)

    if record is None:
        return _null_geocode(normalized_address)

    return _build_result(
        normalized_address=normalized_address,
        latitude=record.get("lat"),
        longitude=record.get("lon"),
        resolution=record.get("resolution", "unknown"),
        confidence=record.get("confidence", 0.5),
        source="internal_reference"
    )


# =========================
# Helpers (Audit-Safe)
# =========================

def _build_result(
    normalized_address: str,
    latitude: float,
    longitude: float,
    resolution: str,
    confidence: float,
    source: str
) -> GeocodeResult:
    geocode_hash = _hash_payload(
        normalized_address,
        latitude,
        longitude,
        resolution,
        confidence,
        source
    )

    return GeocodeResult(
        latitude=latitude,
        longitude=longitude,
        source=source,
        confidence=float(confidence),
        resolution=resolution,
        geocode_hash=geocode_hash
    )


def _null_geocode(normalized_address: str) -> GeocodeResult:
    """
    Explicit null result.
    Missing geocode is NOT an error.
    It is a signal for downstream confidence & escalation.
    """
    return GeocodeResult(
        latitude=None,
        longitude=None,
        source="not_found",
        confidence=0.0,
        resolution="none",
        geocode_hash=_hash_payload(normalized_address, None, None, "none", 0.0, "not_found")
    )


def _hash_payload(*values: Any) -> str:
    """
    Deterministic hash for audit & reproducibility.
    """
    raw = "|".join("" if v is None else str(v) for v in values)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# =========================
# Compliance Guardrails
# =========================

__all__ = [
    "GeocodeResult",
    "InternalGeocodeTable",
    "geocode_address",
]

