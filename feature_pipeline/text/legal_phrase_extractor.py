"""
feature_pipeline/text/legal_phrase_extractor.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Text-level Legal Phrase Extraction ONLY.

This module belongs to the TEXT FEATURE PIPELINE.
It performs deterministic extraction of predefined
legal-related phrases from textual descriptions.

ABSOLUTE PROHIBITIONS
---------------------
- No legal judgment
- No compliance decision
- No risk scoring
- No classification (clean / risky / illegal)
- No downstream triggering

This module answers ONLY:
"Which predefined legal phrases appear in this text?"

OUTPUT
------
Pure extraction results:
- phrase surface form
- character positions
- phrase category

Governance & Audit
------------------
- Deterministic
- Rule-based
- No ML / No LLM
- Fully auditable
"""

from __future__ import annotations

import re
from typing import Dict, List, Pattern, Any


class LegalPhraseExtractionError(Exception):
    """Raised when legal phrase extraction fails."""


class LegalPhraseExtractor:
    """
    Deterministic legal phrase extractor (TEXT LAYER).

    IMPORTANT:
    ----------
    - Phrase list MUST be externally provided
    - No phrase expansion
    - No semantic interpretation
    """

    def __init__(self, phrase_patterns: Dict[str, List[str]]):
        """
        Parameters
        ----------
        phrase_patterns : Dict[str, List[str]]
            Mapping from phrase category to literal phrases.

            Example:
            {
                "ownership": [
                    "sổ đỏ",
                    "giấy chứng nhận quyền sử dụng đất"
                ],
                "dispute": [
                    "tranh chấp",
                    "khiếu kiện"
                ]
            }
        """
        if not phrase_patterns:
            raise LegalPhraseExtractionError(
                "phrase_patterns must not be empty"
            )

        self.phrase_patterns = phrase_patterns
        self._compiled_patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, Pattern[str]]:
        """
        Compile literal phrases into regex patterns.

        Governance Rules
        ----------------
        - Escape all phrases
        - Word-boundary matching
        - Case-insensitive only
        """
        compiled: Dict[str, Pattern[str]] = {}

        for category, phrases in self.phrase_patterns.items():
            if not phrases:
                continue

            escaped = [re.escape(p) for p in phrases]
            pattern_str = r"\b(" + "|".join(escaped) + r")\b"

            compiled[category] = re.compile(
                pattern_str,
                flags=re.IGNORECASE | re.UNICODE
            )

        return compiled

    def extract(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract legal phrases from text.

        Parameters
        ----------
        text : str
            Raw input text.

        Returns
        -------
        Dict[str, List[Dict[str, Any]]]
            {
                category: [
                    {
                        "phrase": str,
                        "start": int,
                        "end": int
                    }
                ]
            }
        """
        if text is None:
            raise LegalPhraseExtractionError("Input text must not be None")

        if not isinstance(text, str):
            raise LegalPhraseExtractionError(
                f"Input text must be str, got {type(text).__name__}"
            )

        results: Dict[str, List[Dict[str, Any]]] = {}

        for category, pattern in self._compiled_patterns.items():
            matches: List[Dict[str, Any]] = []

            for match in pattern.finditer(text):
                matches.append(
                    {
                        "phrase": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )

            if matches:
                results[category] = matches

        return results


def extract_legal_phrases(
    text: str,
    phrase_patterns: Dict[str, List[str]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Functional wrapper for pipeline usage.

    Governance Note
    ---------------
    SAFE for text feature pipelines.
    No semantic meaning is inferred.

    Parameters
    ----------
    text : str
        Raw input text.
    phrase_patterns : Dict[str, List[str]]
        Predefined phrase catalog.

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        Extracted phrases grouped by category.
    """
    extractor = LegalPhraseExtractor(phrase_patterns)
    return extractor.extract(text)
