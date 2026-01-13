# listing_intelligence/content_analysis/price_anomaly_detector.py

"""
ROLE:
    Price Disclosure Anomaly Signal Generator

GOVERNANCE:
    - Deterministic
    - Rule-based only
    - No market prediction
    - No valuation logic
    - No pricing recommendation
    - Signal-only output

COMPLIANCE:
    MASTER_SPEC.md
    IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from typing import Dict, Any, List


# ---------------------------------------------------------------------
# Public detector API
# ---------------------------------------------------------------------

def detect_price_anomalies(
    *,
    listing_snapshot: Dict[str, Any],
    property_reference: Dict[str, Any] | None = None,
    static_bounds: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Detect logical anomalies in declared listing price.

    INPUT (read-only):
        listing_snapshot
        property_reference (optional)
        static_bounds (optional, deterministic config)

    OUTPUT (signal only):
        {
            "status": PASS | FAIL | UNCERTAIN,
            "severity": LOW | MEDIUM | HIGH,
            "findings": {...},
            "evidence_refs": [...]
        }
    """

    findings: Dict[str, Any] = {}
    evidence_refs: List[str] = []

    price = listing_snapshot.get("price", {})

    total_price = price.get("total_price")
    price_per_sqm = price.get("price_per_sqm")
    currency = price.get("currency")
    area_sqm = listing_snapshot.get("area_sqm")

    # -----------------------------------------------------------------
    # 1. Price presence & basic validity
    # -----------------------------------------------------------------
    if total_price is None:
        findings["missing_total_price"] = True
        return _signal(
            status="UNCERTAIN",
            severity="MEDIUM",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    if not _is_positive_number(total_price):
        findings["invalid_total_price"] = total_price
        return _signal(
            status="FAIL",
            severity="HIGH",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    if currency is None:
        findings["missing_currency"] = True

    # -----------------------------------------------------------------
    # 2. Area vs price sanity
    # -----------------------------------------------------------------
    if area_sqm is not None:
        if area_sqm <= 0 and total_price > 0:
            findings["price_with_zero_or_negative_area"] = {
                "area_sqm": area_sqm,
                "total_price": total_price,
            }

        if price_per_sqm and area_sqm > 0:
            implied_total = price_per_sqm * area_sqm
            deviation_ratio = abs(implied_total - total_price) / total_price

            if deviation_ratio > 0.2:
                findings["price_per_sqm_inconsistent"] = {
                    "declared_total": total_price,
                    "implied_total": implied_total,
                    "deviation_ratio": round(deviation_ratio, 3),
                }

    # -----------------------------------------------------------------
    # 3. Static heuristic bounds (non-market)
    # -----------------------------------------------------------------
    bounds = static_bounds or {}

    min_price = bounds.get("min_total_price")
    max_price = bounds.get("max_total_price")

    if min_price is not None and total_price < min_price:
        findings["below_static_min_price"] = {
            "total_price": total_price,
            "min_price": min_price,
        }

    if max_price is not None and total_price > max_price:
        findings["above_static_max_price"] = {
            "total_price": total_price,
            "max_price": max_price,
        }

    # -----------------------------------------------------------------
    # 4. Reference comparison (if available)
    # -----------------------------------------------------------------
    if property_reference:
        ref_price = property_reference.get("price", {}).get("total_price")
        if _is_positive_number(ref_price):
            ratio = total_price / ref_price
            if ratio < 0.5 or ratio > 2.0:
                findings["large_deviation_from_reference"] = {
                    "reference_price": ref_price,
                    "current_price": total_price,
                    "ratio": round(ratio, 2),
                }

    # -----------------------------------------------------------------
    # Signal synthesis (NO DECISION)
    # -----------------------------------------------------------------
    if any(k.startswith("invalid") for k in findings):
        return _signal(
            status="FAIL",
            severity="HIGH",
            findings=findings,
            evidence_refs=evidence_refs,
        )

    if findings:
        severity = "HIGH" if "large_deviation_from_reference" in findings else "MEDIUM"
        return _signal(
            status="UNCERTAIN",
            severity=severity,
            findings=findings,
            evidence_refs=evidence_refs,
        )

    return _signal(
        status="PASS",
        severity="LOW",
        findings=findings,
        evidence_refs=evidence_refs,
    )


# ---------------------------------------------------------------------
# Internal helpers (pure, deterministic)
# ---------------------------------------------------------------------

def _is_positive_number(value: Any) -> bool:
    try:
        return isinstance(value, (int, float)) and value > 0
    except Exception:
        return False


def _signal(
    *,
    status: str,
    severity: str,
    findings: Dict[str, Any],
    evidence_refs: List[str],
) -> Dict[str, Any]:
    """
    Standardized signal output.
    """
    return {
        "status": status,
        "severity": severity,
        "findings": findings,
        "evidence_refs": evidence_refs,
    }
