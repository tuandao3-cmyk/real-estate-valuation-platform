"""
model_reasoning.py

GOVERNANCE-LOCKED MODEL REASONING MODULE
---------------------------------------

PURPOSE
-------
Provide a structured, non-decisional reasoning artifact that explains
HOW a model output should be read by humans.

This module exists to:
- Support transparency
- Assist appraisers in narrative understanding
- Provide audit-safe reasoning context

THIS MODULE DOES NOT:
- Decide price
- Judge correctness
- Compare models
- Override rules
- Influence approval outcomes

COMPLIANCE
----------
- MASTER_SPEC.md
- IMPLEMENTATION STATUS PART 1
- IMPLEMENTATION STATUS PART 2
"""

from dataclasses import dataclass
from typing import List, Optional


# =========================
# DATA STRUCTURES
# =========================

@dataclass(frozen=True)
class ReasoningStatement:
    """
    Single neutral reasoning statement.

    Governance:
    - Text is DESCRIPTIVE ONLY
    - No prescriptive or evaluative language allowed
    """
    statement: str
    source: str  # e.g. 'model_metadata', 'feature_contribution', 'risk_flag'


@dataclass(frozen=True)
class ModelReasoningResult:
    """
    Immutable container for model reasoning.

    This object:
    - Is explanatory, not analytical
    - Is safe for audit and replay
    - Requires human interpretation
    """
    model_id: str
    model_version: str
    sample_id: str
    reasoning_statements: List[ReasoningStatement]
    limitations: List[str]
    disclaimer: str


# =========================
# CORE BUILDER
# =========================

class ModelReasoningBuilder:
    """
    Builder for structured model reasoning.

    GOVERNANCE NOTES
    ----------------
    - Accepts ONLY pre-written or pre-approved text
    - Does NOT generate insights
    - Does NOT infer causality
    """

    def __init__(
        self,
        model_id: str,
        model_version: str,
    ):
        self.model_id = model_id
        self.model_version = model_version

    def build(
        self,
        sample_id: str,
        reasoning_statements: List[ReasoningStatement],
        limitations: List[str],
        disclaimer: Optional[str] = None,
    ) -> ModelReasoningResult:
        """
        Construct a model reasoning artifact.

        IMPORTANT
        ---------
        - All text must be prepared upstream (LLM or human)
        - This function only STRUCTURES content
        """

        final_disclaimer = disclaimer or (
            "The following reasoning is explanatory only and does not "
            "constitute a valuation conclusion or approval recommendation."
        )

        return ModelReasoningResult(
            model_id=self.model_id,
            model_version=self.model_version,
            sample_id=sample_id,
            reasoning_statements=reasoning_statements,
            limitations=limitations,
            disclaimer=final_disclaimer,
        )


# =========================
# DESCRIPTIVE UTILITIES
# =========================

def extract_reasoning_text(
    reasoning: ModelReasoningResult,
) -> List[str]:
    """
    Extract plain reasoning text for display or reporting.

    GOVERNANCE:
    - No rephrasing
    - No summarization
    - No sentiment analysis
    """
    return [r.statement for r in reasoning.reasoning_statements]


def extract_sources(
    reasoning: ModelReasoningResult,
) -> List[str]:
    """
    Extract unique sources referenced in reasoning.

    NOTE:
    - Informational only
    - NOT a credibility score
    """
    return list(
        {r.source for r in reasoning.reasoning_statements}
    )


# =========================
# GOVERNANCE GUARD
# =========================

__all__ = [
    "ReasoningStatement",
    "ModelReasoningResult",
    "ModelReasoningBuilder",
    "extract_reasoning_text",
    "extract_sources",
]

"""
FINAL GOVERNANCE STATEMENT
-------------------------
This module answers:

"What contextual explanations accompany the model output?"

It NEVER answers:
"Is the model right?"
"Should the price be accepted?"
"What action should be taken?"

Those decisions remain with licensed humans.
"""
