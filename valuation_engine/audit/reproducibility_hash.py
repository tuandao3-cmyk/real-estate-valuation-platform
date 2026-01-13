"""
reproducibility_hash.py

NHÓM A – AUDIT / LEGAL INTEGRITY
Role: Deterministic Reproducibility Hash Generator (Read-only)

Purpose
-------
Generate a canonical, reproducible hash representing
the exact state of valuation-relevant artifacts at a point in time.

This hash is used for:
- Audit traceability
- Snapshot integrity
- Court defensibility
- Replay verification

IMPORTANT
---------
- This module DOES NOT make decisions
- DOES NOT compute prices or metrics
- DOES NOT apply rules
- DOES NOT mutate or persist data
- DOES NOT call ML / LLM
- Read-only, pure function behavior

MASTER_SPEC.md OVERRIDES ALL
"""

from __future__ import annotations

import json
import hashlib
from typing import Any, Dict, Iterable, Tuple


# ----------------------------
# Canonical JSON Serialization
# ----------------------------

def _canonicalize_json(data: Any) -> str:
    """
    Convert JSON-compatible data into a canonical string representation.

    Rules:
    - Sorted keys
    - No whitespace
    - Stable ordering
    - UTF-8 encoding
    - No float rounding or transformation

    This ensures:
    same logical content => same byte sequence => same hash
    """
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


# ----------------------------
# Hash Primitives
# ----------------------------

def _sha256_hex(payload: str) -> str:
    """
    Compute SHA-256 hash (hex encoded) of a UTF-8 string.
    """
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ----------------------------
# Public API
# ----------------------------

def generate_reproducibility_hash(
    *,
    valuation_dossier: Dict[str, Any],
    referenced_artifacts: Iterable[Tuple[str, Dict[str, Any]]],
    policy_versions: Dict[str, str],
) -> str:
    """
    Generate a deterministic reproducibility hash.

    Parameters
    ----------
    valuation_dossier : dict (REQUIRED)
        Canonical valuation dossier (Single Source of Truth).

    referenced_artifacts : Iterable[(artifact_name, artifact_content)]
        Other read-only artifacts that were referenced in the workflow
        (e.g. decision_result, approval_log, valuation_trace).

        Order does NOT matter.

    policy_versions : dict
        Governance-approved policy versions applied during workflow.

    Returns
    -------
    reproducibility_hash : str
        Hex-encoded SHA-256 hash.

    Governance Guarantees
    ---------------------
    - Read-only
    - Deterministic
    - Replayable
    - Audit-ready
    - No side effects

    Compliance
    ----------
    - valuation_dossier.json is mandatory
    - valuation_dossier OVERRIDES ALL on conflict
    """

    if valuation_dossier is None:
        raise ValueError("valuation_dossier is mandatory for reproducibility hash")

    # Canonical payload structure (STRICT ORDER)
    canonical_payload = {
        "valuation_dossier": valuation_dossier,
        "referenced_artifacts": {
            name: content
            for name, content in sorted(referenced_artifacts, key=lambda x: x[0])
        },
        "policy_versions": dict(sorted(policy_versions.items())),
    }

    canonical_string = _canonicalize_json(canonical_payload)
    return _sha256_hex(canonical_string)


# ----------------------------
# Validation Helpers (Audit-only)
# ----------------------------

def verify_reproducibility_hash(
    *,
    expected_hash: str,
    valuation_dossier: Dict[str, Any],
    referenced_artifacts: Iterable[Tuple[str, Dict[str, Any]]],
    policy_versions: Dict[str, str],
) -> bool:
    """
    Verify whether a given reproducibility hash matches
    the recomputed hash from the provided artifacts.

    This function:
    - DOES NOT log
    - DOES NOT throw on mismatch
    - Pure verification only

    Returns
    -------
    bool
        True if hashes match, False otherwise.
    """
    computed = generate_reproducibility_hash(
        valuation_dossier=valuation_dossier,
        referenced_artifacts=referenced_artifacts,
        policy_versions=policy_versions,
    )
    return computed == expected_hash
