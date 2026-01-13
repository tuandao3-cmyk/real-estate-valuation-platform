"""
feature_pipeline/text/text_cleaning.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Text Cleaning & Normalization ONLY.

This module is part of the Feature Engineering layer.
It performs deterministic, reversible-safe text preprocessing
to standardize raw textual inputs (e.g. descriptions, notes, comments).

ABSOLUTE PROHIBITIONS
---------------------
- No inference
- No scoring
- No sentiment analysis
- No classification
- No value judgment
- No feature importance
- No domain interpretation

OUTPUT
------
Purely normalized text, suitable for downstream feature extraction.

Audit & Governance
------------------
- Deterministic
- Stateless
- No side effects
- No external calls
"""

from __future__ import annotations

import re
import unicodedata
from typing import Optional


class TextCleaningError(Exception):
    """Raised when text cleaning fails due to invalid input."""


class TextCleaner:
    """
    Deterministic text cleaner.

    This class MUST NOT:
    - Infer meaning
    - Extract intent
    - Decide relevance
    """

    def __init__(
        self,
        lowercase: bool = True,
        normalize_unicode: bool = True,
        remove_extra_whitespace: bool = True,
        strip_control_chars: bool = True,
        max_length: Optional[int] = None,
    ):
        self.lowercase = lowercase
        self.normalize_unicode = normalize_unicode
        self.remove_extra_whitespace = remove_extra_whitespace
        self.strip_control_chars = strip_control_chars
        self.max_length = max_length

    def clean(self, text: str) -> str:
        """
        Clean and normalize raw text.

        Parameters
        ----------
        text : str
            Raw input text.

        Returns
        -------
        str
            Cleaned text.

        Raises
        ------
        TextCleaningError
            If input is invalid.
        """
        if text is None:
            raise TextCleaningError("Input text must not be None")

        if not isinstance(text, str):
            raise TextCleaningError(
                f"Input text must be str, got {type(text).__name__}"
            )

        cleaned = text

        if self.normalize_unicode:
            cleaned = self._normalize_unicode(cleaned)

        if self.strip_control_chars:
            cleaned = self._remove_control_characters(cleaned)

        if self.lowercase:
            cleaned = cleaned.lower()

        if self.remove_extra_whitespace:
            cleaned = self._normalize_whitespace(cleaned)

        if self.max_length is not None:
            cleaned = cleaned[: self.max_length]

        return cleaned

    @staticmethod
    def _normalize_unicode(text: str) -> str:
        """
        Normalize unicode text to NFKC form.
        """
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def _remove_control_characters(text: str) -> str:
        """
        Remove non-printable control characters.
        """
        return "".join(
            ch for ch in text
            if unicodedata.category(ch)[0] != "C"
        )

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """
        Collapse multiple whitespace characters into a single space.
        """
        text = re.sub(r"\s+", " ", text)
        return text.strip()


def clean_text(
    text: str,
    *,
    lowercase: bool = True,
    normalize_unicode: bool = True,
    remove_extra_whitespace: bool = True,
    strip_control_chars: bool = True,
    max_length: Optional[int] = None,
) -> str:
    """
    Functional wrapper for text cleaning.

    This function exists to support pipeline-style usage
    without class instantiation.

    Governance Note
    ---------------
    This function is SAFE for feature pipelines.
    It performs NO semantic interpretation.

    Parameters
    ----------
    text : str
        Raw input text.

    Returns
    -------
    str
        Cleaned text.
    """
    cleaner = TextCleaner(
        lowercase=lowercase,
        normalize_unicode=normalize_unicode,
        remove_extra_whitespace=remove_extra_whitespace,
        strip_control_chars=strip_control_chars,
        max_length=max_length,
    )
    return cleaner.clean(text)
