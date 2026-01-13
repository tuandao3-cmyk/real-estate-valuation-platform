# Module: listing_intelligence/workflows/verify_flow.py
# Part of Advanced AVM System

# listing_intelligence/workflows/verify_flow.py

"""
ROLE:
    Deterministic Listing Verification Orchestrator

GOVERNANCE:
    - READ-ONLY inputs
    - SIGNAL-ONLY outputs
    - NO scoring
    - NO acceptance / rejection
    - NO dossier mutation

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List

# --- Verifier imports (each verifier is independent & deterministic) ---
from listing_intelligence.verification.address_verifier import verify_address
from listing_intelligence.verification.legal_verifier import verify_legal_status
from listing_intelligence.verification.zoning_verifier import verify_zoning
from listing_intelligence.verification.occupancy_verifier import verify_occupancy
from listing_intelligence.verification.ownership_consistency import verify_ownership_consistency


# ---------------------------------------------------------------------
# Output contract
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class VerificationSignal:
    verifier_name: str
    status: str                 # PASS / FAIL / UNCERTAIN
    findings: Dict[str, Any]
    severity: str               # LOW / MEDIUM / HIGH
    evidence_refs: List[str]
    generated_at_utc: str


@dataclass(frozen=True)
class VerificationResult:
    listing_id: str
    signals: List[VerificationSignal]
    verification_timestamp_utc: str

    # Governance markers
    decision_made: bool = False
    price_influenced: bool = False
    workflow_blocked: bool = False


# ---------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------

def run_listing_verification(
    *,
    listing_id: str,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
) -> VerificationResult:
    """
    Execute listing verification flow.

    INPUT:
        - listing_snapshot: immutable ingest snapshot
        - property_reference: optional reference record

    OUTPUT:
        VerificationResult (signals only)

    NOTE:
        This function MUST remain deterministic.
    """

    signals: List[VerificationSignal] = []
    now = datetime.utcnow().isoformat()

    # --- Address Verification ---
    addr_result = verify_address(
        listing_snapshot=listing_snapshot,
        property_reference=property_reference,
    )
    signals.append(_wrap_signal("address_verifier", addr_result, now))

    # --- Legal Status Verification ---
    legal_result = verify_legal_status(
        listing_snapshot=listing_snapshot,
        property_reference=property_reference,
    )
    signals.append(_wrap_signal("legal_verifier", legal_result, now))

    # --- Zoning Verification ---
    zoning_result = verify_zoning(
        listing_snapshot=listing_snapshot,
        property_reference=property_reference,
    )
    signals.append(_wrap_signal("zoning_verifier", zoning_result, now))

    # --- Occupancy Verification ---
    occupancy_result = verify_occupancy(
        listing_snapshot=listing_snapshot
    )
    signals.append(_wrap_signal("occupancy_verifier", occupancy_result, now))

    # --- Ownership Consistency Verification ---
    ownership_result = verify_ownership_consistency(
        listing_snapshot=listing_snapshot,
        property_reference=property_reference,
    )
    signals.append(_wrap_signal("ownership_consistency", ownership_result, now))

    return VerificationResult(
        listing_id=listing_id,
        signals=signals,
        verification_timestamp_utc=now,
    )


# ---------------------------------------------------------------------
# Internal helper (NOT exported)
# ---------------------------------------------------------------------

def _wrap_signal(
    verifier_name: str,
    raw_result: Dict[str, Any],
    timestamp: str,
) -> VerificationSignal:
    """
    Normalize verifier output into a governance-compliant signal.
    """

    return VerificationSignal(
        verifier_name=verifier_name,
        status=raw_result["status"],                 # PASS / FAIL / UNCERTAIN
        findings=raw_result.get("findings", {}),
        severity=raw_result.get("severity", "LOW"),
        evidence_refs=raw_result.get("evidence_refs", []),
        generated_at_utc=timestamp,
    )
