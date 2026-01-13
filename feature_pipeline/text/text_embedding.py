"""
feature_pipeline/text/text_embedding.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Deterministic Text Embedding Generator (Feature Layer).

This module converts cleaned text into a fixed-length numeric
vector using hashing-based embedding.

ABSOLUTE PROHIBITIONS
---------------------
- No semantic inference
- No sentiment analysis
- No intent detection
- No desirability / quality inference
- No valuation logic
- No scoring or ranking

Embedding output is a DESCRIPTIVE REPRESENTATION ONLY.

GOVERNANCE GUARANTEES
--------------------
- Deterministic
- Stateless
- No training
- No external model calls
- Fully reproducible
"""

from __future__ import annotations

import hashlib
from typing import List, Dict


class TextEmbeddingError(Exception):
    """Raised when text embedding generation fails."""


class HashingTextEmbedder:
    """
    Deterministic hashing-based text embedder.

    Design rationale:
    -----------------
    - No ML model
    - No training data
    - No semantic understanding
    - Suitable for governance-heavy systems
    """

    def __init__(self, dimension: int = 128):
        """
        Parameters
        ----------
        dimension : int
            Fixed embedding vector size.

        Governance:
        -----------
        - Must be explicitly configured
        - Changing dimension requires version bump
        """
        if dimension <= 0:
            raise TextEmbeddingError("dimension must be > 0")

        self.dimension = dimension

    def _tokenize(self, text: str) -> List[str]:
        """
        Very simple whitespace tokenization.

        Governance:
        -----------
        - No linguistic inference
        - No stemming
        - No synonym expansion
        """
        return [t for t in text.lower().split() if t]

    def _hash_token(self, token: str) -> int:
        """
        Hash token deterministically using SHA-256.
        """
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return int(digest, 16)

    def embed(self, text: str) -> List[int]:
        """
        Generate text embedding vector.

        Parameters
        ----------
        text : str
            Pre-cleaned text input.

        Returns
        -------
        List[int]
            Fixed-length embedding vector.
        """
        if text is None:
            raise TextEmbeddingError("Input text must not be None")

        if not isinstance(text, str):
            raise TextEmbeddingError(
                f"Input text must be str, got {type(text).__name__}"
            )

        vector = [0] * self.dimension
        tokens = self._tokenize(text)

        for token in tokens:
            idx = self._hash_token(token) % self.dimension
            vector[idx] += 1

        return vector


def generate_text_embedding(
    text: str,
    dimension: int = 128,
) -> Dict[str, object]:
    """
    Functional wrapper for text embedding generation.

    SAFE FOR
    --------
    - Feature pipelines
    - Similarity indexing
    - Descriptive analytics
    - Audit replay

    NOT ALLOWED FOR
    ---------------
    - Decision making
    - Trust scoring
    - Valuation logic
    - Approval routing

    Returns
    -------
    Dict[str, object]
        {
            "embedding": List[int],
            "dimension": int,
            "method": "hashing",
        }
    """
    embedder = HashingTextEmbedder(dimension=dimension)
    embedding = embedder.embed(text)

    return {
        "embedding": embedding,
        "dimension": dimension,
        "method": "hashing",
    }
