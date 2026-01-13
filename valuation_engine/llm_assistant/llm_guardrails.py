# valuation_engine/llm_assistant/llm_guardrails.py

"""
LLM GUARDRAILS – LEGAL & GOVERNANCE ENFORCEMENT LAYER
====================================================

Classification:
    NHÓM A – LEGAL / AUDIT / GOVERNANCE CRITICAL

Role:
    Hard guardrails enforcing absolute boundaries for LLM usage.

This module exists to PREVENT, not to correct.

----------------------------------------------------
CORE PRINCIPLES (NON-NEGOTIABLE)
----------------------------------------------------
- valuation_dossier.json is the Single Source of Truth
- LLM is a CLERK, not a decision-maker
- LLM output MUST NOT influence numeric decisions
- Any violation => SYSTEM VIOLATION

This module:
- DOES NOT call LLM
- DOES NOT modify data
- DOES NOT compute values
- DOES NOT make decisions
- DOES NOT interact with workflow logic

It ONLY:
- Validates inputs to LLM
- Validates outputs from LLM
- Enforces hard blocks on forbidden content
"""

from __future__ import annotations

import re
from typing import Dict, List, Any


# ---------------------------------------------------------------------
# GOVERNANCE CONSTANTS (LOCKED)
# ---------------------------------------------------------------------

FORBIDDEN_NUMERIC_PATTERNS = [
    r"\b\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+)?\s*(vnđ|vnd|đ|usd|\$|tỷ|triệu|million|billion)\b",
    r"\b\d+\s*(vnđ|vnd|đ|usd|\$)\b",
    r"\b\d+(\.\d+)?\s*(tỷ|triệu|million|billion)\b",
]

FORBIDDEN_DECISION_KEYWORDS = [
    "approve",
    "reject",
    "khuyến nghị",
    "đề xuất",
    "nên cho vay",
    "nên đầu tư",
    "chấp thuận",
    "từ chối",
]

FORBIDDEN_ROLE_ACTIONS = [
    "override",
    "adjust price",
    "điều chỉnh giá",
    "thay đổi kết quả",
    "quyết định",
]


# ---------------------------------------------------------------------
# EXCEPTIONS (LEGAL-GRADE)
# ---------------------------------------------------------------------

class LLMGuardrailViolation(Exception):
    """
    Raised when LLM input or output violates MASTER_SPEC boundaries.
    Any occurrence MUST be treated as SYSTEM VIOLATION.
    """
    pass


# ---------------------------------------------------------------------
# INPUT GUARDRAILS
# ---------------------------------------------------------------------

def validate_llm_input(input_payload: Dict[str, Any]) -> None:
    """
    Validate that LLM input strictly complies with MASTER_SPEC.

    Allowed:
    - Read-only references
    - Structured, non-decisional context
    - Explanation-only intent

    Forbidden:
    - Any numeric decision intent
    - Any instruction to predict, adjust, or decide
    """

    if not isinstance(input_payload, dict):
        raise LLMGuardrailViolation("LLM input must be a structured dictionary.")

    forbidden_fields = {
        "price",
        "final_price",
        "confidence_score",
        "risk_band",
        "decision",
        "approval",
    }

    for key in input_payload.keys():
        if key.lower() in forbidden_fields:
            raise LLMGuardrailViolation(
                f"Forbidden field in LLM input: {key}"
            )


# ---------------------------------------------------------------------
# OUTPUT GUARDRAILS
# ---------------------------------------------------------------------

def validate_llm_output(text: str) -> None:
    """
    Validate LLM output text to ensure:
    - No numeric values
    - No decision language
    - No implicit approval / rejection
    """

    if not isinstance(text, str):
        raise LLMGuardrailViolation("LLM output must be text.")

    _check_forbidden_numeric(text)
    _check_forbidden_decision_language(text)
    _check_forbidden_role_actions(text)


def _check_forbidden_numeric(text: str) -> None:
    """
    Block ANY numeric financial expression.
    """
    for pattern in FORBIDDEN_NUMERIC_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            raise LLMGuardrailViolation(
                "LLM output contains numeric or monetary information "
                "which is strictly forbidden."
            )


def _check_forbidden_decision_language(text: str) -> None:
    """
    Block language implying approval, rejection, or recommendation.
    """
    lowered = text.lower()
    for keyword in FORBIDDEN_DECISION_KEYWORDS:
        if keyword in lowered:
            raise LLMGuardrailViolation(
                f"LLM output contains forbidden decision language: '{keyword}'"
            )


def _check_forbidden_role_actions(text: str) -> None:
    """
    Block language implying override or system authority.
    """
    lowered = text.lower()
    for keyword in FORBIDDEN_ROLE_ACTIONS:
        if keyword in lowered:
            raise LLMGuardrailViolation(
                f"LLM output contains forbidden role action: '{keyword}'"
            )


# ---------------------------------------------------------------------
# PUBLIC CONTRACT
# ---------------------------------------------------------------------

def enforce_llm_guardrails(
    *,
    input_payload: Dict[str, Any],
    llm_output_text: str,
) -> None:
    """
    Canonical enforcement entrypoint.

    This function MUST be called immediately:
    - Before LLM invocation (input validation)
    - After LLM response (output validation)

    Side effects:
    - NONE

    Returns:
    - None if compliant

    Raises:
    - LLMGuardrailViolation if ANY violation is detected
    """

    validate_llm_input(input_payload)
    validate_llm_output(llm_output_text)


# ---------------------------------------------------------------------
# AUDIT ASSERTION (OPTIONAL, FACT-ONLY)
# ---------------------------------------------------------------------

def llm_compliance_assertion() -> Dict[str, Any]:
    """
    Returns a static compliance assertion for audit trace usage.

    This function:
    - Does NOT evaluate runtime behavior
    - Does NOT inspect outputs
    - Merely declares enforced constraints
    """

    return {
        "llm_numeric_influence": False,
        "llm_decision_authority": False,
        "llm_override_capability": False,
        "guardrails_enforced": True,
        "spec_reference": "MASTER_SPEC.md §1.2, §3, §11",
    }
