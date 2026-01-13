# Module: data/cleaning/normalize_address.py
# Part of Advanced AVM System

"""
File: data/cleaning/normalize_address.py

Risk Classification: NHÓM A – DATA STANDARDIZATION / AUDIT SUPPORT
Change Policy: GOVERNANCE-LOCKED

ROLE DEFINITION
----------------
This module provides deterministic, non-inferential normalization of address
strings for consistency and comparability across the system.

It performs PURE TEXT STANDARDIZATION ONLY.

It DOES NOT:
- Validate address correctness
- Infer missing address components
- Geocode or enrich location data
- Decide jurisdiction, zoning, or asset validity
- Modify valuation logic or outcomes

Normalized outputs are SUPPORTING DATA ONLY and must be stored
as separate fields or artifacts. Raw input addresses are NEVER overwritten.

valuation_dossier.json remains the Single Source of Truth.
"""

from typing import Dict
import re


# Canonical abbreviation map (static, governance-approved)
_ABBREVIATIONS = {
    r"\bđường\b": "Đ.",
    r"\bphường\b": "P.",
    r"\bxã\b": "X.",
    r"\bquận\b": "Q.",
    r"\bhuyện\b": "H.",
    r"\btỉnh\b": "T.",
    r"\bthành phố\b": "TP."
}


def normalize_address(address: str) -> Dict[str, str]:
    """
    Normalize an address string into a standardized textual form.

    INPUT
    -----
    address : str
        Raw address string as provided by source systems or humans.

    OUTPUT
    ------
    Dict[str, str]
        {
            "original": <original input string>,
            "normalized": <normalized string>
        }

    GUARANTEES
    ----------
    - Deterministic: same input => same output
    - Non-destructive: original value is preserved
    - No enrichment or inference
    - No external service calls
    """

    if not isinstance(address, str):
        raise TypeError("Address must be a string")

    original = address

    # Basic whitespace normalization
    normalized = address.strip()
    normalized = re.sub(r"\s+", " ", normalized)

    # Lowercase for deterministic replacement
    working = normalized.lower()

    # Apply canonical abbreviations
    for pattern, replacement in _ABBREVIATIONS.items():
        working = re.sub(pattern, replacement.lower(), working)

    # Restore capitalization style (simple title-case, not semantic)
    normalized = working.title()

    return {
        "original": original,
        "normalized": normalized
    }


__all__ = ["normalize_address"]
