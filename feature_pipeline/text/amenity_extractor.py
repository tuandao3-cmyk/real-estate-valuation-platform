"""
feature_pipeline/text/amenity_extractor.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Text-level Amenity Extraction ONLY.

This module performs deterministic extraction of
declared amenities from free-form listing text.

ABSOLUTE PROHIBITIONS
---------------------
- No desirability inference
- No quality assessment
- No valuation implication
- No scoring / weighting
- No ranking
- No market relevance interpretation

This module ONLY answers:
"Which predefined amenities are explicitly mentioned?"

GOVERNANCE GUARANTEES
--------------------
- Deterministic
- Rule-based
- No ML / No LLM
- Auditable
- Feature-only
"""

from __future__ import annotations

import re
from typing import Dict, List, Pattern, Any


class AmenityExtractionError(Exception):
    """Raised when amenity extraction fails."""


class AmenityExtractor:
    """
    Deterministic amenity extractor (TEXT FEATURE LAYER).

    IMPORTANT:
    ----------
    - Amenity list MUST be explicitly provided
    - No synonym expansion unless explicitly declared
    - No semantic guessing
    """

    def __init__(self, amenity_catalog: Dict[str, List[str]]):
        """
        Parameters
        ----------
        amenity_catalog : Dict[str, List[str]]
            Mapping from amenity category to literal amenity phrases.

            Example:
            {
                "parking": ["bãi đỗ xe", "chỗ để xe"],
                "security": ["bảo vệ 24/7", "camera an ninh"],
                "utilities": ["thang máy", "máy phát điện"]
            }
        """
        if not amenity_catalog:
            raise AmenityExtractionError(
                "amenity_catalog must not be empty"
            )

        self.amenity_catalog = amenity_catalog
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, Pattern[str]]:
        """
        Compile amenity phrases into regex patterns.

        Governance Rules
        ----------------
        - Literal matching only
        - Escaped phrases
        - Word-boundary matching
        - Case-insensitive
        """
        compiled: Dict[str, Pattern[str]] = {}

        for category, phrases in self.amenity_catalog.items():
            if not phrases:
                continue

            escaped_phrases = [re.escape(p) for p in phrases]
            pattern_str = r"\b(" + "|".join(escaped_phrases) + r")\b"

            compiled[category] = re.compile(
                pattern_str,
                flags=re.IGNORECASE | re.UNICODE
            )

        return compiled

    def extract(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract amenities from text.

        Parameters
        ----------
        text : str
            Listing description or title.

        Returns
        -------
        Dict[str, List[Dict[str, Any]]]
            {
                category: [
                    {
                        "amenity": str,
                        "start": int,
                        "end": int
                    }
                ]
            }
        """
        if text is None:
            raise AmenityExtractionError("Input text must not be None")

        if not isinstance(text, str):
            raise AmenityExtractionError(
                f"Input text must be str, got {type(text).__name__}"
            )

        results: Dict[str, List[Dict[str, Any]]] = {}

        for category, pattern in self._compiled_patterns.items():
            matches: List[Dict[str, Any]] = []

            for match in pattern.finditer(text):
                matches.append(
                    {
                        "amenity": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )

            if matches:
                results[category] = matches

        return results


def extract_amenities(
    text: str,
    amenity_catalog: Dict[str, List[str]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Functional wrapper for amenity extraction.

    SAFE FOR:
    ---------
    - Feature pipelines
    - Audit replay
    - Offline processing

    NOT ALLOWED FOR:
    ----------------
    - Scoring
    - Ranking
    - Decision making

    Parameters
    ----------
    text : str
        Raw listing text.
    amenity_catalog : Dict[str, List[str]]
        Explicit amenity phrase catalog.

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        Extracted amenities grouped by category.
    """
    extractor = AmenityExtractor(amenity_catalog)
    return extractor.extract(text)
