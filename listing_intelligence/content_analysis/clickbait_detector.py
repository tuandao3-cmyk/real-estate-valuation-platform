# Module: listing_intelligence/content_analysis/clickbait_detector.py
# Part of Advanced AVM System

# listing_intelligence/content_analysis/clickbait_detector.py

"""
ROLE:
    Clickbait / Misleading Content Signal Generator

GOVERNANCE:
    - Rule-based only
    - No ML / No NLP inference
    - No behavioral assumption
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List
import re


# ---------------------------------------------------------------------
# Static governance-approved vocabularies
# ---------------------------------------------------------------------

CLICKBAIT_PHRASES = [
    "duy nhất",
    "có một không hai",
    "rẻ nhất",
    "siêu rẻ",
    "không thể bỏ lỡ",
    "cơ hội vàng",
    "giá sốc",
    "bán gấp",
    "cắt lỗ",
    "lãi ngay",
]

ABSOLUTE_CLAIMS = [
    "100%",
    "cam kết",
    "đảm bảo",
    "chắc chắn",
    "vĩnh viễn",
    "mãi mãi",
    "không rủi ro",
]

URGENCY_MARKERS = [
    "hôm nay",
    "ngay",
    "gấp",
    "chỉ còn",
    "cuối cùng",
]


# ---------------------------------------------------------------------
# Public detector API
# ---------------------------------------------------------------------

def detect_clickbait(
    *,
    title: str | None,
    description: str | None,
) -> Dict[str, Any]:
    """
    Detect clickbait or misleading language patterns.

    INPUT (read-only):
        title
        description

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

    title_text = (title or "").lower()
    desc_text = (description or "").lower()

    # -----------------------------------------------------------------
    # 1. Clickbait phrase detection
    # -----------------------------------------------------------------
    clickbait_hits = _match_phrases(title_text, CLICKBAIT_PHRASES)
    if clickbait_hits:
        findings["clickbait_phrases_in_title"] = clickbait_hits

    # -----------------------------------------------------------------
    # 2. Absolute / unverifiable claims
    # -----------------------------------------------------------------
    absolute_hits = _match_phrases(desc_text, ABSOLUTE_CLAIMS)
    if absolute_hits:
        findings["absolute_claims_in_description"] = absolute_hits

    # -----------------------------------------------------------------
    # 3. Urgency pressure language
    # -----------------------------------------------------------------
    urgency_hits = _match_phrases(title_text, URGENCY_MARKERS)
    if urgency_hits:
        findings["urgency_language"] = urgency_hits

    # -----------------------------------------------------------------
    # 4. Title vs description mismatch (very basic heuristic)
    # -----------------------------------------------------------------
    if title_text and desc_text:
        title_keywords = set(_extract_keywords(title_text))
        desc_keywords = set(_extract_keywords(desc_text))

        if title_keywords and not title_keywords.intersection(desc_keywords):
            findings["title_description_mismatch"] = {
                "title_keywords": list(title_keywords),
                "description_keywords": list(desc_keywords),
            }

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

def _match_phrases(text: str, phrases: List[str]) -> List[str]:
    hits = []
    for phrase in phrases:
        if phrase in text:
            hits.append(phrase)
    return hits


def _extract_keywords(text: str) -> List[str]:
    tokens = re.findall(r"\b\w{4,}\b", text)
    return tokens[:10]


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
