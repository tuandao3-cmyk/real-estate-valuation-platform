# valuation_engine/audit/decision_explainer.py

"""
DECISION EXPLAINER MODULE
========================

GOVERNANCE CLASSIFICATION:
- Group: A (Audit / Explanation / Legal Readability)
- Authority Level: ZERO decision authority
- Side Effects: NONE
- Mutability: READ-ONLY

PURPOSE:
--------
This module generates a structured, human-readable explanation of
an already-determined valuation outcome.

It does NOT:
- compute prices
- adjust confidence
- approve or reject decisions
- infer missing data
- override rules or human authority

All explanations are strictly derived from immutable artifacts.
"""

from typing import Dict, Any, List


class DecisionExplainer:
    """
    DecisionExplainer is a PURE EXPLANATION LAYER.

    It translates factual system artifacts into a structured explanation
    suitable for:
    - Valuation reports
    - Credit committee review
    - Audit inspection
    - Court / dispute context

    NO inference. NO interpretation. NO decision logic.
    """

    def __init__(
        self,
        valuation_dossier: Dict[str, Any],
        decision_result: Dict[str, Any],
        approval_log: Dict[str, Any],
        valuation_trace: Dict[str, Any],
    ):
        self._valuation_dossier = valuation_dossier
        self._decision_result = decision_result
        self._approval_log = approval_log
        self._valuation_trace = valuation_trace

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def generate_explanation(self) -> Dict[str, Any]:
        """
        Generate a structured explanation object.

        Returns:
            Dict[str, Any]: Explanation payload (non-numeric, non-decisional)
        """

        return {
            "property_context": self._explain_property_context(),
            "valuation_summary": self._explain_valuation_summary(),
            "risk_and_confidence": self._explain_risk_and_confidence(),
            "rule_application": self._explain_rule_application(),
            "human_authority": self._explain_human_authority(),
            "limitations": self._explain_limitations(),
        }

    # ------------------------------------------------------------------
    # EXPLANATION SECTIONS (FACTUAL ONLY)
    # ------------------------------------------------------------------

    def _explain_property_context(self) -> Dict[str, Any]:
        return {
            "property_id": self._valuation_dossier.get("property_id"),
            "property_type": self._valuation_dossier.get("property_type"),
            "location": self._valuation_dossier.get("location"),
            "data_snapshot_id": self._valuation_dossier.get("snapshot_id"),
        }

    def _explain_valuation_summary(self) -> Dict[str, Any]:
        return {
            "valuation_methodology": self._decision_result.get(
                "valuation_methodology"
            ),
            "price_band": self._decision_result.get("price_band"),
            "final_status": self._decision_result.get("final_status"),
            "valuation_timestamp": self._decision_result.get(
                "valuation_timestamp"
            ),
        }

    def _explain_risk_and_confidence(self) -> Dict[str, Any]:
        return {
            "confidence_score": self._decision_result.get("confidence_score"),
            "confidence_interpretation": (
                "Confidence reflects model agreement and data quality. "
                "It is used as a routing signal, not a guarantee of accuracy."
            ),
            "risk_flags": self._decision_result.get("risk_flags", []),
        }

    def _explain_rule_application(self) -> Dict[str, Any]:
        return {
            "applied_rules": self._decision_result.get("applied_rules", []),
            "rule_engine_note": (
                "Rules enforce policy constraints and approval routing. "
                "They do not learn, optimize, or predict outcomes."
            ),
        }

    def _explain_human_authority(self) -> Dict[str, Any]:
        return {
            "approval_required": self._decision_result.get(
                "approval_required"
            ),
            "approved_by": self._approval_log.get("approved_by"),
            "approval_role": self._approval_log.get("role"),
            "approval_timestamp": self._approval_log.get("timestamp"),
            "authority_statement": (
                "Final responsibility lies with the licensed appraiser "
                "or authorized credit officer. AI systems do not approve "
                "or reject valuations."
            ),
        }

    def _explain_limitations(self) -> List[str]:
        return [
            "The system relies on available data at the time of valuation.",
            "Model outputs are subject to uncertainty and dispersion.",
            "AI components assist analysis but do not replace human judgment.",
            "Re-running the valuation with the same snapshot reproduces results.",
        ]


# ----------------------------------------------------------------------
# GOVERNANCE ASSERTIONS (DOCUMENTATION-LEVEL)
# ----------------------------------------------------------------------
#
# - This module must never be extended with:
#   * numeric computation
#   * decision thresholds
#   * model calls
#   * LLM prompt execution
#
# - Any violation invalidates audit compliance.
#
# MASTER_SPEC.md OVERRIDES ALL.
#
