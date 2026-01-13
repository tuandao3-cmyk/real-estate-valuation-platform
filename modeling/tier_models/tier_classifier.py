# model/tier_models/tier_classifier.py

from typing import Dict, Any, List
from dataclasses import dataclass
import hashlib


class TierClassificationError(Exception):
    """Raised when tier classification cannot be safely performed."""
    pass


@dataclass(frozen=True)
class TierResult:
    """
    Descriptive tier classification output.
    NON-DECISIONAL. NON-NUMERIC.
    """
    tier: str
    reasons: List[str]
    input_hash: str
    classifier_version: str


class TierClassifier:
    """
    Tier Classifier – GOVERNANCE-SAFE MODULE

    Role:
    - Classify valuation dossier into descriptive tiers (A/B/C/D)
    - Support workflow routing & human review intensity

    Forbidden:
    - Price inference
    - Approval / rejection
    - Confidence manipulation
    - Learning / adaptation
    """

    CLASSIFIER_VERSION = "tier_classifier_v1.0.0"

    ALLOWED_TIERS = {"A", "B", "C", "D"}

    def __init__(self, tier_rules: Dict[str, Dict[str, Any]]):
        """
        tier_rules: static, versioned rule configuration
        Example structure:
        {
            "A": {"max_legal_flags": 0, "min_data_completeness": 0.95},
            "B": {"max_legal_flags": 1, "min_data_completeness": 0.85},
            "C": {"max_legal_flags": 2, "min_data_completeness": 0.70},
            "D": {"fallback": True}
        }
        """
        self._validate_rules(tier_rules)
        self.tier_rules = tier_rules

    def _validate_rules(self, tier_rules: Dict[str, Dict[str, Any]]) -> None:
        if not tier_rules:
            raise TierClassificationError("Tier rules must not be empty")

        for tier in tier_rules.keys():
            if tier not in self.ALLOWED_TIERS:
                raise TierClassificationError(f"Invalid tier defined: {tier}")

    def _hash_inputs(self, inputs: Dict[str, Any]) -> str:
        """
        Hash input signals for audit & reproducibility.
        """
        serialized = repr(sorted(inputs.items())).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def classify(self, dossier_signals: Dict[str, Any]) -> TierResult:
        """
        Perform deterministic tier classification.

        dossier_signals MUST NOT contain:
        - price
        - confidence
        - approval status
        """
        required_fields = [
            "data_completeness_score",
            "legal_disclosure_flag_count",
            "image_quality_score",
            "feature_snapshot_hash",
        ]

        for field in required_fields:
            if field not in dossier_signals:
                raise TierClassificationError(
                    f"Missing required signal for tier classification: {field}"
                )

        reasons: List[str] = []

        data_completeness = dossier_signals["data_completeness_score"]
        legal_flags = dossier_signals["legal_disclosure_flag_count"]
        image_quality = dossier_signals["image_quality_score"]

        input_hash = self._hash_inputs(dossier_signals)

        # Tier evaluation – strict order A → D
        for tier in ["A", "B", "C"]:
            rule = self.tier_rules.get(tier)
            if not rule:
                continue

            if legal_flags > rule.get("max_legal_flags", float("inf")):
                continue

            if data_completeness < rule.get("min_data_completeness", 0.0):
                continue

            if image_quality < rule.get("min_image_quality", 0.0):
                continue

            reasons.append(
                f"Meets criteria for Tier {tier}: "
                f"legal_flags={legal_flags}, "
                f"data_completeness={data_completeness}, "
                f"image_quality={image_quality}"
            )

            return TierResult(
                tier=tier,
                reasons=reasons,
                input_hash=input_hash,
                classifier_version=self.CLASSIFIER_VERSION,
            )

        # Fallback Tier D (explicitly non-failing)
        reasons.append(
            "Does not meet Tier A/B/C criteria – assigned Tier D for mandatory human review"
        )

        return TierResult(
            tier="D",
            reasons=reasons,
            input_hash=input_hash,
            classifier_version=self.CLASSIFIER_VERSION,
        )
