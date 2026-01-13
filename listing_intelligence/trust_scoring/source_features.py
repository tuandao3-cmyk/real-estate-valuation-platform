"""
listing_intelligence/trust_scoring/source_features.py

GOVERNANCE ROLE
---------------
Extract and normalize source-related signals for listing trust analysis.

ABSOLUTE RULES
--------------
- No trust score computation
- No pass / fail classification
- No pricing logic
- No rule override
- Descriptive signals only

These features represent SOURCE CHARACTERISTICS,
not conclusions about trustworthiness.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Optional
from datetime import datetime


@dataclass(frozen=True)
class SourceFeatureSet:
    """
    Normalized source-level signals for a property listing.
    """
    listing_id: str
    source_platform: str
    poster_type: str  # e.g. 'owner', 'agent', 'unknown'
    account_age_days: Optional[int]
    total_listings_by_poster: Optional[int]
    verified_identity: Optional[bool]
    verified_phone: Optional[bool]
    verified_email: Optional[bool]
    has_transaction_history: Optional[bool]
    first_seen_timestamp: str
    extraction_timestamp: str


class SourceFeatureExtractor:
    """
    Extracts source-related features from raw listing metadata.

    This class performs NO interpretation.
    """

    def __init__(self, source_platform: str) -> None:
        self._source_platform = source_platform

    def extract(
        self,
        listing_id: str,
        raw_metadata: Dict,
    ) -> SourceFeatureSet:
        """
        Extract source features from raw metadata.

        Parameters
        ----------
        listing_id : str
            Unique listing identifier
        raw_metadata : Dict
            Raw metadata from listing ingestion layer

        Returns
        -------
        SourceFeatureSet
            Immutable, descriptive source feature object
        """

        now_utc = datetime.utcnow().isoformat()

        return SourceFeatureSet(
            listing_id=listing_id,
            source_platform=self._source_platform,
            poster_type=self._extract_poster_type(raw_metadata),
            account_age_days=raw_metadata.get("account_age_days"),
            total_listings_by_poster=raw_metadata.get("total_listings_by_poster"),
            verified_identity=raw_metadata.get("verified_identity"),
            verified_phone=raw_metadata.get("verified_phone"),
            verified_email=raw_metadata.get("verified_email"),
            has_transaction_history=raw_metadata.get("has_transaction_history"),
            first_seen_timestamp=raw_metadata.get(
                "first_seen_timestamp", now_utc
            ),
            extraction_timestamp=now_utc,
        )

    @staticmethod
    def _extract_poster_type(raw_metadata: Dict) -> str:
        """
        Normalize poster type into a controlled vocabulary.
        """
        poster_type = raw_metadata.get("poster_type")

        if poster_type in {"owner", "agent", "developer"}:
            return poster_type

        return "unknown"


class SourceFeatureSerializer:
    """
    Serialization helpers for SourceFeatureSet.
    """

    @staticmethod
    def to_dict(feature_set: SourceFeatureSet) -> Dict:
        """
        Convert SourceFeatureSet to plain dictionary.
        """
        return asdict(feature_set)
