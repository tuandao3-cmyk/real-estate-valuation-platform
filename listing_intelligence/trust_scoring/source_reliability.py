"""
listing_intelligence/trust_scoring/source_reliability.py

GOVERNANCE ROLE
---------------
Produce a descriptive, non-decisive reliability projection
based solely on source-level features.

ABSOLUTE CONSTRAINTS
--------------------
- No approval / rejection
- No hard trust conclusion
- No pricing or valuation impact
- No workflow authority
- Deterministic, explainable mapping only

Reliability here is CONTEXTUAL INFORMATION, not a verdict.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
from datetime import datetime

from listing_intelligence.trust_scoring.source_features import SourceFeatureSet


@dataclass(frozen=True)
class SourceReliabilityProjection:
    """
    Descriptive reliability projection for a listing source.
    """
    listing_id: str
    source_platform: str
    reliability_band: str  # VERY_LOW / LOW / MEDIUM / HIGH (descriptive)
    contributing_factors: Dict[str, Optional[bool]]
    notes: str
    projection_timestamp: str
    projection_version: str = "v1.0-descriptive"


class SourceReliabilityProjector:
    """
    Deterministic, rule-transparent reliability projection.

    IMPORTANT:
    ----------
    - These mappings are NOT thresholds for action.
    - Bands are descriptive only.
    - Any downstream use must apply independent governance.
    """

    ALLOWED_BANDS = {"VERY_LOW", "LOW", "MEDIUM", "HIGH"}

    def project(
        self,
        source_features: SourceFeatureSet,
    ) -> SourceReliabilityProjection:
        """
        Create a descriptive reliability projection.

        Parameters
        ----------
        source_features : SourceFeatureSet
            Immutable source features

        Returns
        -------
        SourceReliabilityProjection
            Non-decisive reliability context
        """

        band = self._derive_band(source_features)
        now_utc = datetime.utcnow().isoformat()

        return SourceReliabilityProjection(
            listing_id=source_features.listing_id,
            source_platform=source_features.source_platform,
            reliability_band=band,
            contributing_factors={
                "verified_identity": source_features.verified_identity,
                "verified_phone": source_features.verified_phone,
                "verified_email": source_features.verified_email,
                "has_transaction_history": source_features.has_transaction_history,
                "poster_type_known": source_features.poster_type != "unknown",
            },
            notes=(
                "Reliability band is descriptive only. "
                "It reflects observable source attributes and "
                "must not be interpreted as approval, rejection, "
                "or fraud determination."
            ),
            projection_timestamp=now_utc,
        )

    def _derive_band(self, source_features: SourceFeatureSet) -> str:
        """
        Deterministic descriptive mapping.

        WARNING:
        --------
        This logic MUST NOT be reused as a rule engine.
        """

        positive_signals = 0

        if source_features.verified_identity:
            positive_signals += 1
        if source_features.verified_phone:
            positive_signals += 1
        if source_features.verified_email:
            positive_signals += 1
        if source_features.has_transaction_history:
            positive_signals += 1
        if source_features.poster_type != "unknown":
            positive_signals += 1

        if positive_signals <= 1:
            return "VERY_LOW"
        if positive_signals == 2:
            return "LOW"
        if positive_signals in {3, 4}:
            return "MEDIUM"
        return "HIGH"


class SourceReliabilitySerializer:
    """
    Serialization helpers for audit & storage layers.
    """

    @staticmethod
    def to_dict(
        projection: SourceReliabilityProjection,
    ) -> Dict:
        return asdict(projection)
