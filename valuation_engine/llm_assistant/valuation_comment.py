"""
valuation_engine/llm_assistant/valuation_comment.py

ROLE:
    LLM-Assisted Valuation Commentary Generator (Clerical Only)

GOVERNANCE CLASSIFICATION:
    NHÓM A – Legal / Audit Boundary

AUTHORITATIVE SPEC:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – valuation_comment.py

CORE PRINCIPLES (ENFORCED):
    - valuation_dossier.json is Single Source of Truth
    - Read-only inputs
    - No computation
    - No inference
    - No decision-making
    - LLM = clerical writer only
"""

from typing import Dict, Any

from valuation_engine.llm_assistant.llm_guardrails import (
    enforce_llm_guardrails,
    LLMGuardrailViolation,
)

# Explicit allowlist of sections that LLM may describe
_ALLOWED_SECTIONS = {
    "property_context",
    "valuation_overview",
    "data_sources_summary",
    "methodology_description",
    "risk_and_confidence_description",
    "system_limitations",
}


class ValuationCommentaryError(Exception):
    """Raised when valuation commentary generation violates governance rules."""


def generate_valuation_commentary(
    *,
    valuation_context: Dict[str, Any],
    llm_client,
) -> Dict[str, str]:
    """
    Generate descriptive valuation commentary using LLM assistance.

    GOVERNANCE NOTES:
        - This function is clerical-only.
        - It does NOT calculate, infer, or decide.
        - All inputs are treated as read-only facts.
        - All outputs are descriptive text only.

    Parameters
    ----------
    valuation_context : dict
        Pre-validated, governance-approved context extracted upstream.
        MUST NOT contain:
            - prices
            - thresholds
            - approval states
            - rule logic
            - free-text human decisions

    llm_client :
        Pre-approved LLM client instance.
        Must NOT be invoked outside guardrails.

    Returns
    -------
    Dict[str, str]
        Mapping of section_name -> descriptive commentary text.

    Raises
    ------
    ValuationCommentaryError
        If any governance or guardrail violation occurs.
    """

    if not isinstance(valuation_context, dict):
        raise ValuationCommentaryError("valuation_context must be a dict")

    commentary: Dict[str, str] = {}

    for section_name, section_payload in valuation_context.items():
        # Enforce strict section allowlist
        if section_name not in _ALLOWED_SECTIONS:
            raise ValuationCommentaryError(
                f"Section '{section_name}' is not permitted for LLM commentary"
            )

        # Prepare strictly descriptive prompt
        prompt = _build_descriptive_prompt(
            section_name=section_name,
            section_payload=section_payload,
        )

        # Invoke LLM (no retry, no fallback)
        raw_output = llm_client.generate_text(prompt)

        # Enforce guardrails (FAIL-HARD)
        try:
            safe_output = enforce_llm_guardrails(
                text=raw_output,
                section_name=section_name,
            )
        except LLMGuardrailViolation as exc:
            raise ValuationCommentaryError(
                f"LLM output violated guardrails in section '{section_name}'"
            ) from exc

        commentary[section_name] = safe_output

    return commentary


def _build_descriptive_prompt(*, section_name: str, section_payload: Any) -> str:
    """
    Build a strictly descriptive prompt for LLM.

    HARD CONSTRAINTS:
        - No questions
        - No instructions to evaluate
        - No approval language
        - No numeric reasoning
        - No suggestions or recommendations
    """

    return (
        "You are assisting with drafting descriptive valuation commentary.\n\n"
        "STRICT RULES:\n"
        "- Describe facts only.\n"
        "- Do NOT infer, evaluate, or judge.\n"
        "- Do NOT recommend any decision.\n"
        "- Do NOT introduce numbers, thresholds, or conclusions.\n"
        "- Use neutral, professional language.\n\n"
        f"SECTION: {section_name}\n"
        "FACTS (READ-ONLY):\n"
        f"{section_payload}\n\n"
        "TASK:\n"
        "Rewrite the above facts into a clear, neutral, human-readable description.\n"
    )
