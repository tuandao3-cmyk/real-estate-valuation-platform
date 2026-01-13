# Module: valuation_engine/audit/valuation_trace.py
# Part of Advanced AVM System

"""
valuation_engine/audit/valuation_trace.py

LEGAL ROLE
----------
Audit Trace Orchestrator for Valuation Workflow

This module provides a deterministic, read-only audit trace
for the valuation workflow, strictly compliant with MASTER_SPEC.md.

NON-NEGOTIABLE CONSTRAINTS
-------------------------
- NO valuation logic
- NO ML / NO LLM
- NO rule computation
- NO decision making
- NO artifact mutation
- NO side effects

This file ONLY:
- References existing artifacts
- Records workflow steps
- Captures hashes & policy versions
- Ensures reproducibility & auditability

If conflict arises:
valuation_dossier.json OVERRIDES ALL
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional


# =========================
# DATA STRUCTURES (IMMUTABLE)
# =========================

@dataclass(frozen=True)
class TraceArtifactRef:
    """
    Immutable reference to an existing artifact.
    """
    name: str
    hash: str
    required: bool


@dataclass(frozen=True)
class TraceStep:
    """
    One deterministic step in the valuation workflow.
    """
    step_name: str
    component: str
    status: str  # EXECUTED / SKIPPED / BLOCKED
    timestamp_utc: str
    references: List[TraceArtifactRef]


@dataclass(frozen=True)
class ValuationTraceRecord:
    """
    Canonical audit trace record.

    This record:
    - Is NOT a decision
    - Is NOT a valuation result
    - Is NOT a legal conclusion
    """
    trace_id: str
    valuation_hash: str
    created_at_utc: str
    reproducible: bool
    steps: List[TraceStep]
    policy_versions: Dict[str, str]


# =========================
# ORCHESTRATOR (READ-ONLY)
# =========================

class ValuationTraceBuilder:
    """
    Deterministic builder for valuation audit trace.

    This class:
    - Does NOT validate logic
    - Does NOT evaluate rules
    - Does NOT infer outcomes

    It ONLY records what already happened in the workflow.
    """

    def __init__(
        self,
        trace_id: str,
        valuation_hash: str,
        policy_versions: Dict[str, str],
    ):
        self._trace_id = trace_id
        self._valuation_hash = valuation_hash
        self._policy_versions = policy_versions
        self._steps: List[TraceStep] = []

    def record_step(
        self,
        *,
        step_name: str,
        component: str,
        status: str,
        artifact_refs: List[TraceArtifactRef],
    ) -> None:
        """
        Record a workflow step.

        STRICT RULES:
        - status must reflect upstream workflow result
        - artifact_refs must already exist
        """
        step = TraceStep(
            step_name=step_name,
            component=component,
            status=status,
            timestamp_utc=datetime.utcnow().isoformat() + "Z",
            references=artifact_refs,
        )
        self._steps.append(step)

    def build(self) -> ValuationTraceRecord:
        """
        Finalize immutable audit trace record.

        This does NOT:
        - Persist to storage
        - Trigger workflow
        - Influence decisions
        """
        return ValuationTraceRecord(
            trace_id=self._trace_id,
            valuation_hash=self._valuation_hash,
            created_at_utc=datetime.utcnow().isoformat() + "Z",
            reproducible=True,
            steps=list(self._steps),
            policy_versions=dict(self._policy_versions),
        )


# =========================
# PUBLIC INTERFACE
# =========================

def generate_valuation_trace(
    *,
    trace_id: str,
    valuation_hash: str,
    policy_versions: Dict[str, str],
    executed_steps: List[Dict],
) -> ValuationTraceRecord:
    """
    Generate a valuation audit trace.

    Parameters
    ----------
    trace_id : str
        External audit trace identifier
    valuation_hash : str
        Hash of valuation_dossier.json (mandatory)
    policy_versions : Dict[str, str]
        Versions of governance policies applied
    executed_steps : List[Dict]
        Pre-determined workflow execution results
        (provided by valuation_flow.py)

    IMPORTANT
    ---------
    - This function TRUSTS upstream workflow results
    - It does NOT re-evaluate anything
    - It ONLY records facts
    """

    builder = ValuationTraceBuilder(
        trace_id=trace_id,
        valuation_hash=valuation_hash,
        policy_versions=policy_versions,
    )

    for step in executed_steps:
        builder.record_step(
            step_name=step["step_name"],
            component=step["component"],
            status=step["status"],
            artifact_refs=[
                TraceArtifactRef(
                    name=ref["name"],
                    hash=ref["hash"],
                    required=ref["required"],
                )
                for ref in step.get("artifact_refs", [])
            ],
        )

    return builder.build()


# =========================
# EXPORT (READ-ONLY)
# =========================

def serialize_trace(trace: ValuationTraceRecord) -> Dict:
    """
    Serialize valuation trace for storage or audit export.

    NOTE:
    - Serialization ONLY
    - No transformation
    """
    return asdict(trace)
