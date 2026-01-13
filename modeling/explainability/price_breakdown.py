"""
price_breakdown.py

GOVERNANCE-LOCKED PRICE DECOMPOSITION MODULE
--------------------------------------------

PURPOSE
-------
Provide a transparent, numeric-only decomposition of a model-generated
price estimate into traceable components.

This module exists to:
- Improve auditability
- Support human explanation
- Enable forensic review of valuation mechanics

THIS MODULE DOES NOT:
- Decide price
- Adjust valuation
- Apply rules
- Assess acceptability
- Rank components
- Judge reasonableness

COMPLIANCE
----------
- MASTER_SPEC.md
- IMPLEMENTATION STATUS PART 1
- IMPLEMENTATION STATUS PART 2
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


# =========================
# DATA STRUCTURES
# =========================

@dataclass(frozen=True)
class PriceComponent:
    """
    Single numeric component contributing to a price.

    Governance:
    - value is descriptive only
    - label is neutral (no semantic judgement)
    """
    component_name: str
    value: float
    source: str


@dataclass(frozen=True)
class PriceBreakdownResult:
    """
    Immutable price breakdown artifact.

    This object:
    - Is NOT a valuation conclusion
    - Cannot be modified post-creation
    - Is suitable for audit & replay
    """
    model_id: str
    model_version: str
    sample_id: str
    base_price: float
    components: List[PriceComponent]
    final_price: float
    notes: Optional[str]


# =========================
# CORE LOGIC
# =========================

class PriceBreakdownBuilder:
    """
    Builder for price breakdown.

    GOVERNANCE NOTES
    ----------------
    - Accepts ONLY pre-computed numeric inputs
    - No inference, no optimization
    - Caller is responsible for correctness of inputs
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
        base_price: float,
        components: Dict[str, float],
        component_sources: Dict[str, str],
        notes: Optional[str] = None,
    ) -> PriceBreakdownResult:
        """
        Construct a price breakdown artifact.

        Parameters
        ----------
        base_price:
            Raw model output before decomposition.
        components:
            Dict of component_name -> numeric delta.
        component_sources:
            Dict of component_name -> provenance identifier
            (e.g. 'core_model', 'risk_adjustment', 'ensemble_weighting')

        IMPORTANT
        ---------
        - base_price is NOT validated here
        - components are NOT checked for correctness
        - No semantic meaning is inferred
        """

        price_components: List[PriceComponent] = []
        total_adjustment = 0.0

        for name, value in components.items():
            source = component_sources.get(name, "unknown")
            numeric_value = float(value)

            total_adjustment += numeric_value

            price_components.append(
                PriceComponent(
                    component_name=name,
                    value=numeric_value,
                    source=source,
                )
            )

        final_price = float(base_price + total_adjustment)

        return PriceBreakdownResult(
            model_id=self.model_id,
            model_version=self.model_version,
            sample_id=sample_id,
            base_price=float(base_price),
            components=price_components,
            final_price=final_price,
            notes=notes,
        )


# =========================
# DESCRIPTIVE UTILITIES
# =========================

def flatten_breakdown(
    breakdown: PriceBreakdownResult,
) -> Dict[str, float]:
    """
    Flatten breakdown into a simple numeric map.

    OUTPUT
    ------
    Dict[str, float]:
        component_name -> value

    GOVERNANCE:
    - No aggregation logic
    - No ranking
    - No filtering
    """
    return {
        c.component_name: c.value
        for c in breakdown.components
    }


def total_adjustment_amount(
    breakdown: PriceBreakdownResult,
) -> float:
    """
    Compute total adjustment magnitude.

    NOTE:
    - Pure arithmetic
    - NOT a confidence indicator
    - NOT a risk signal
    """
    return float(
        sum(c.value for c in breakdown.components)
    )


# =========================
# GOVERNANCE GUARD
# =========================

__all__ = [
    "PriceComponent",
    "PriceBreakdownResult",
    "PriceBreakdownBuilder",
    "flatten_breakdown",
    "total_adjustment_amount",
]

"""
FINAL GOVERNANCE STATEMENT
-------------------------
This module answers ONE question only:

"How did the number get formed mathematically?"

It NEVER answers:
"Is the number correct?"
"Should the number be accepted?"
"What should the appraiser do?"

Those decisions belong to humans.
"""
