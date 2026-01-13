# model/income_approach/income_model.py
# GOVERNANCE LOCKED – INCOME APPROACH CALCULATION ONLY
# AI ASSISTS – HUMAN DECIDES

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


class IncomeApproachViolation(Exception):
    """Raised when income approach governance rules are violated."""
    pass


@dataclass(frozen=True)
class IncomeInputs:
    """
    All inputs MUST be pre-approved and validated upstream.
    This model does NOT validate market correctness.
    """
    net_operating_income: float  # NOI
    cap_rate: float              # selected by HUMAN, from reference table
    activation_token: str        # must be issued by activation_check
    assumptions_version: str
    cap_rate_table_version: str


@dataclass
class IncomeOutput:
    """
    Output is INTERMEDIATE valuation signal.
    Not final value. Not approved value.
    """
    indicated_value: float
    calculation_timestamp: str
    inputs_snapshot: Dict[str, Any]
    limitations: str
    governance_flags: Dict[str, bool]


class IncomeModel:
    """
    Income Approach Model – Mechanical Calculator

    ROLE:
    - Convert approved NOI & Cap Rate into an indicated value
    - Preserve full auditability
    - Enforce role separation

    NON-ROLE:
    - Market judgment
    - Cap rate selection
    - Risk adjustment
    - Approval / rejection
    """

    MODEL_NAME = "IncomeApproachModel"
    MODEL_VERSION = "v1.0.0"
    GOVERNANCE_ROLE = "INCOME_CALCULATION_ONLY"

    def __init__(self):
        self._activated = False

    def activate(self, activation_token: str):
        """
        Activation must be granted externally.
        This model cannot self-activate.
        """
        if not activation_token or not activation_token.startswith("INCOME_OK_"):
            raise IncomeApproachViolation(
                "Income approach activation token invalid or missing."
            )
        self._activated = True

    def compute(self, inputs: IncomeInputs) -> IncomeOutput:
        """
        Perform income capitalization calculation.

        Formula:
            Indicated Value = NOI / Cap Rate

        Governance:
        - No adjustment
        - No smoothing
        - No fallback
        """

        if not self._activated:
            raise IncomeApproachViolation(
                "Income model used without explicit activation."
            )

        if inputs.cap_rate <= 0:
            raise IncomeApproachViolation(
                "Cap rate must be positive and human-approved."
            )

        indicated_value = inputs.net_operating_income / inputs.cap_rate

        return IncomeOutput(
            indicated_value=indicated_value,
            calculation_timestamp=datetime.utcnow().isoformat(),
            inputs_snapshot={
                "net_operating_income": inputs.net_operating_income,
                "cap_rate": inputs.cap_rate,
                "assumptions_version": inputs.assumptions_version,
                "cap_rate_table_version": inputs.cap_rate_table_version,
                "model_version": self.MODEL_VERSION,
            },
            limitations=(
                "This value is an indicative result from the Income Approach "
                "based solely on provided NOI and cap rate assumptions. "
                "It does not represent market value, final valuation, "
                "or approval for any financial decision."
            ),
            governance_flags={
                "human_cap_rate_selected": True,
                "activation_required": True,
                "auto_decision_prohibited": True,
                "final_value_prohibited": True,
            },
        )


# === USAGE NOTE (NON-EXECUTABLE) =====================================
#
# activation_token must come from:
#   model/income_approach/activation_check.py
#
# Result must be written into:
#   valuation_dossier.json
#
# Any direct consumption of this output as FINAL VALUE
# is a SYSTEM VIOLATION.
#
# ====================================================================
