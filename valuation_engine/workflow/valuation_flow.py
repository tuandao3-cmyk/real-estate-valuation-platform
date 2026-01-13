"""
valuation_engine/workflow/valuation_flow.py

Tuân thủ tuyệt đối MASTER_SPEC.md & IMPLEMENTATION STATUS
Role: Valuation Workflow Orchestrator (Workflow-only, Deterministic)

NGUYÊN TẮC BẤT BIẾN
- valuation_dossier.json là Single Source of Truth
- READ-ONLY với mọi input
- KHÔNG tính giá
- KHÔNG áp rule kinh doanh
- KHÔNG sinh decision tín dụng / định giá
- KHÔNG ML / LLM
- KHÔNG ghi file / mutate state
- Chỉ điều phối luồng (routing + gating)

File này KHÔNG:
- Override con người
- Thay thế appraisal
- Tạo hay sửa bất kỳ artifact nào
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

# Import workflow gates (pure, deterministic)
from valuation_engine.workflow.approval_required import evaluate_approval_requirement
from valuation_engine.workflow.maker_checker_enforcer import enforce_maker_checker
from valuation_engine.workflow.escalation_policy import evaluate_escalation
from valuation_engine.workflow.rejection_gate import evaluate_rejection  # giả định đã tồn tại


# =========================
# Canonical flow outcomes
# =========================

FLOW_BLOCKED = "FLOW_BLOCKED"
FLOW_ESCALATED = "FLOW_ESCALATED"
FLOW_HUMAN_APPROVAL_REQUIRED = "FLOW_HUMAN_APPROVAL_REQUIRED"
FLOW_READY_FOR_REPORTING = "FLOW_READY_FOR_REPORTING"


# =========================
# Output schema (workflow-only)
# =========================

@dataclass(frozen=True)
class ValuationFlowResult:
    flow_status: str
    reasons: Tuple[str, ...]
    valuation_hash: str
    trace_id: Optional[str]
    policy_versions: Tuple[str, ...]


# =========================
# Core Orchestration Logic
# =========================

def run_valuation_flow(
    *,
    valuation_dossier: Dict[str, Any],
    decision_result: Optional[Dict[str, Any]] = None,
    approval_log: Optional[Dict[str, Any]] = None,
    trace_id: Optional[str] = None,
) -> ValuationFlowResult:
    """
    Điều phối toàn bộ valuation workflow theo đúng thứ tự pháp lý.

    Thứ tự BẮT BUỘC (không được thay đổi):
    1. Hard Rejection Gate
    2. Approval Requirement Routing
    3. Escalation Policy
    4. Maker–Checker Enforcement (nếu có approval_log)
    """

    policy_versions = []

    # -------------------------------------------------
    # 1. HARD REJECTION GATE (fail-fast, legal-grade)
    # -------------------------------------------------
    rejection = evaluate_rejection(
        valuation_dossier=valuation_dossier,
        decision_result=decision_result,
        approval_log=approval_log,
    )
    policy_versions.append(rejection.policy_version)

    if rejection.rejected:
        return ValuationFlowResult(
            flow_status=FLOW_BLOCKED,
            reasons=(rejection.rejection_code,),
            valuation_hash=rejection.valuation_hash,
            trace_id=trace_id,
            policy_versions=tuple(policy_versions),
        )

    # -------------------------------------------------
    # 2. APPROVAL REQUIREMENT ROUTER
    # -------------------------------------------------
    approval_req = evaluate_approval_requirement(
        valuation_dossier=valuation_dossier
    )
    policy_versions.append(approval_req.policy_version)

    if approval_req.requirement == "WORKFLOW_BLOCKED":
        return ValuationFlowResult(
            flow_status=FLOW_BLOCKED,
            reasons=tuple(approval_req.reasons),
            valuation_hash=approval_req.valuation_hash,
            trace_id=trace_id,
            policy_versions=tuple(policy_versions),
        )

    if approval_req.requirement == "HUMAN_APPROVAL_REQUIRED":
        return ValuationFlowResult(
            flow_status=FLOW_HUMAN_APPROVAL_REQUIRED,
            reasons=tuple(approval_req.reasons),
            valuation_hash=approval_req.valuation_hash,
            trace_id=trace_id,
            policy_versions=tuple(policy_versions),
        )

    # -------------------------------------------------
    # 3. ESCALATION POLICY
    # -------------------------------------------------
    escalation = evaluate_escalation(
        valuation_dossier=valuation_dossier,
        decision_result=decision_result,
        approval_log=approval_log,
    )
    policy_versions.append(escalation.policy_version)

    if escalation.escalation_required:
        return ValuationFlowResult(
            flow_status=FLOW_ESCALATED,
            reasons=tuple(escalation.reasons),
            valuation_hash=escalation.valuation_hash,
            trace_id=trace_id,
            policy_versions=tuple(policy_versions),
        )

    # -------------------------------------------------
    # 4. MAKER–CHECKER ENFORCEMENT (nếu đã có approval)
    # -------------------------------------------------
    if approval_log is not None:
        enforcement = enforce_maker_checker(
            valuation_dossier=valuation_dossier,
            approval_log=approval_log,
        )
        policy_versions.append(enforcement.policy_version)

        if enforcement.result != "ENFORCED_OK":
            return ValuationFlowResult(
                flow_status=FLOW_BLOCKED,
                reasons=tuple(enforcement.reasons),
                valuation_hash=enforcement.valuation_hash,
                trace_id=trace_id,
                policy_versions=tuple(policy_versions),
            )

    # -------------------------------------------------
    # FLOW PASSED – READY FOR REPORTING / EXPORT
    # -------------------------------------------------
    return ValuationFlowResult(
        flow_status=FLOW_READY_FOR_REPORTING,
        reasons=tuple(),
        valuation_hash=valuation_dossier.get("valuation_hash", "UNKNOWN"),
        trace_id=trace_id,
        policy_versions=tuple(policy_versions),
    )
