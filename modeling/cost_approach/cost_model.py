# model/cost_approach/cost_model.py
# ==========================================================
# GOVERNANCE CLASS: NHÓM A – COST APPROACH (REFERENCE MODEL)
# ROLE: Cost-Based Value Reference Generator
# AUTHORITY: NON-DECISIVE / HUMAN-VALIDATED
# ==========================================================
#
# IMPORTANT:
# - This module implements COST APPROACH as a descriptive reference
# - Output is NOT a final valuation
# - Must be combined via ensemble + rule + human review
#
# MASTER_SPEC ENFORCEMENT:
# - Deterministic
# - No learning
# - No auto-adjustment
# - No rule override
# ==========================================================

from dataclasses import dataclass
from typing import Dict
import hashlib
import json

from model.cost_approach.depreciation_curve import (
    DepreciationInput,
    DepreciationCurveEngine
)


@dataclass(frozen=True)
class CostModelInput:
    """
    Input contract for Cost Approach.

    All numeric inputs must come from:
    - feature_snapshot
    - human-approved reference tables
    """

    replacement_cost_new: float
    depreciation_input: DepreciationInput
    land_value_reference: float


@dataclass(frozen=True)
class CostModelOutput:
    """
    Descriptive output of Cost Approach.

    NOTE:
    - This is NOT a final valuation
    - This output MUST NOT be used standalone
    """

    replacement_cost_new: float
    depreciation_factor: float
    depreciated_structure_cost: float
    land_value_reference: float
    total_cost_reference: float
    audit_hash: str


class CostApproachModel:
    """
    Static Cost Approach Model.

    GOVERNANCE GUARANTEES:
    - Read-only computation
    - No inference beyond arithmetic
    - No authority to decide value
    """

    @staticmethod
    def run(input_data: CostModelInput) -> CostModelOutput:
        """
        Execute cost approach calculation.

        Formula (descriptive):
            Depreciated Structure Cost =
                Replacement Cost New * (1 - Depreciation Factor)

            Total Cost Reference =
                Depreciated Structure Cost + Land Value Reference
        """

        CostApproachModel._validate_input(input_data)

        depreciation_result = DepreciationCurveEngine.compute(
            input_data.depreciation_input
        )

        depreciation_factor = depreciation_result["depreciation_factor"]

        depreciated_structure_cost = (
            input_data.replacement_cost_new * (1.0 - depreciation_factor)
        )

        total_cost_reference = (
            depreciated_structure_cost + input_data.land_value_reference
        )

        audit_hash = CostApproachModel._compute_audit_hash(
            input_data=input_data,
            depreciation_result=depreciation_result,
            depreciated_structure_cost=depreciated_structure_cost,
            total_cost_reference=total_cost_reference
        )

        return CostModelOutput(
            replacement_cost_new=round(input_data.replacement_cost_new, 2),
            depreciation_factor=round(depreciation_factor, 6),
            depreciated_structure_cost=round(depreciated_structure_cost, 2),
            land_value_reference=round(input_data.land_value_reference, 2),
            total_cost_reference=round(total_cost_reference, 2),
            audit_hash=audit_hash
        )

    # --------------------------------------------------
    # Validation & Governance Guardrails
    # --------------------------------------------------

    @staticmethod
    def _validate_input(input_data: CostModelInput) -> None:
        """
        Hard validation – fail fast.

        Governance rule:
        - Cost approach must not run on invalid or speculative data
        """

        if input_data.replacement_cost_new <= 0:
            raise ValueError("replacement_cost_new must be > 0")

        if input_data.land_value_reference < 0:
            raise ValueError("land_value_reference must be >= 0")

    # --------------------------------------------------
    # Audit & Reproducibility
    # --------------------------------------------------

    @staticmethod
    def _compute_audit_hash(
        input_data: CostModelInput,
        depreciation_result: Dict[str, float],
        depreciated_structure_cost: float,
        total_cost_reference: float
    ) -> str:
        """
        Generate deterministic audit hash for replay & dispute.

        Hash includes:
        - All inputs
        - Depreciation output
        - Final arithmetic result
        """

        payload = {
            "replacement_cost_new": input_data.replacement_cost_new,
            "depreciation_input": {
                "depreciation_type": input_data.depreciation_input.depreciation_type,
                "curve_type": input_data.depreciation_input.curve_type,
                "age_years": input_data.depreciation_input.age_years,
                "economic_life_years": input_data.depreciation_input.economic_life_years
            },
            "depreciation_result": depreciation_result,
            "depreciated_structure_cost": depreciated_structure_cost,
            "land_value_reference": input_data.land_value_reference,
            "total_cost_reference": total_cost_reference
        }

        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
