# Module: listing_intelligence/content_analysis/copy_paste_detector.py
# Part of Advanced AVM System
# listing_intelligence/content_analysis/copy_paste_detector.py

"""
ROLE:
    Copy–Paste Content Redundancy Signal Generator

GOVERNANCE:
    - Rule-based only
    - No ML / No embeddings
    - No cross-user inference
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List
import hashlib
import re


# ---------------------------------------------------------------------
# Public detector API
# ---------------------------------------------------------------------

def detect_copy_paste_content(
    *,
    description: str | None,
    historical_fingerprints: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Detect copy–paste or templated content patterns.

    INPUT (read-only):
        description
        historical_fingerprints (optional, pre-approved store)

    OUTPUT (signal only):
        {
            "status": PASS | UNCERTAIN,
            "severity": LOW | MEDIUM,
            "findings": {...},
            "evidence_refs": [...]
        }
    """

    findings: Dict[str, Any] = {}
    evidence_refs: List[str] = []

    if not description:
        return _signal(
            status="UNCERTAIN",
            severity="LOW",
            findings={"missing_description": True},
            evidence_refs=evidence_refs,
        )

    normalized_text = _normalize_text(description)
    fingerprint = _hash_text(normalized_text)

    # -----------------------------------------------------------------
    # 1. Exact fingerprint reuse
    # -----------------------------------------------------------------
    if historical_fingerprints and fingerprint in historical_fingerprints:
        findings["exact_content_reuse_detected"] = {
            "fingerprint": fingerprint
        }

    # -----------------------------------------------------------------
    # 2. Low lexical diversity (template-like text)
    # -----------------------------------------------------------------
    tokens = normalized_text.split()
    unique_ratio = len(set(tokens)) / max(len(tokens), 1)

    if len(tokens) > 50 and unique_ratio < 0.35:
        findings["low_lexical_diversity"] = {
            "token_count": len(tokens),
            "unique_ratio": round(unique_ratio, 3),
        }

    # -----------------------------------------------------------------
    # 3. Repetitive phrase pattern
    # -----------------------------------------------------------------
    repeated_phrases = _detect_repeated_phrases(normalized_text)
    if repeated_phrases:
        findings["repetitive_phrases"] = repeated_phrases

    # -----------------------------------------------------------------
    # Signal synthesis (NO DECISION)
    # -----------------------------------------------------------------
    if findings:
        severity = "MEDIUM" if len(findings) > 1 else "LOW"
        return _signal(
            status="UNCERTAIN",
            severity=severity,
            findings=findings,
            evidence_refs=evidence_refs,
        )

    return _signal(
        status="PASS",
        severity="LOW",
        findings=findings,
        evidence_refs=evidence_refs,
    )


# ---------------------------------------------------------------------
# Internal helpers (pure, deterministic)
# ---------------------------------------------------------------------

def _normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _detect_repeated_phrases(text: str, window: int = 4) -> List[str]:
    tokens = text.split()
    seen = {}
    repeats = []

    for i in range(len(tokens) - window + 1):
        phrase = " ".join(tokens[i:i + window])
        seen[phrase] = seen.get(phrase, 0) + 1

    for phrase, count in seen.items():
        if count >= 3:
            repeats.append({
                "phrase": phrase,
                "count": count,
            })

    return repeats


def _signal(
    *,
    status: str,
    severity: str,
    findings: Dict[str, Any],
    evidence_refs: List[str],
) -> Dict[str, Any]:
    """
    Standardized signal output.
    """
    return {
        "status": status,
        "severity": severity,
        "findings": findings,
        "evidence_refs": evidence_refs,
    }

