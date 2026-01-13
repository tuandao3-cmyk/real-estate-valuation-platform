"""
Hedonic AVM Core Model (Inference Only)

🚫 DO NOT VIOLATE MASTER_SPEC.md
🚫 THIS MODEL DOES NOT DECIDE FINAL VALUE
🚫 THIS MODEL DOES NOT APPLY BUSINESS RULES

Role:
- Produce hedonic price estimates as one signal among many
- Fully reproducible, auditable, immutable
"""

from dataclasses import dataclass
from typing import List, Dict
import json
import hashlib
import math


@dataclass(frozen=True)
class HedonicModelArtifact:
    """
    Immutable representation of a trained hedonic model.
    """
    model_id: str
    model_version: str
    feature_order: List[str]
    coefficients: List[float]
    intercept: float
    training_metadata_hash: str


@dataclass(frozen=True)
class HedonicPrediction:
    """
    Output of hedonic model inference.
    This is NOT a valuation conclusion.
    """
    model_id: str
    model_version: str
    feature_snapshot_hash: str
    raw_estimates: Dict[str, float]
    dispersion_metric: float
    limitations: List[str]


class HedonicModel:
    """
    Deterministic hedonic regression model (linear form).

    This class:
    - Loads immutable artifacts
    - Applies pure mathematical inference
    - Emits no decisions
    """

    def __init__(self, artifact: HedonicModelArtifact):
        self._artifact = artifact
        self._validate_artifact()

    def predict(
        self,
        feature_matrix: "FeatureMatrix",
        property_ids: List[str]
    ) -> HedonicPrediction:
        """
        Run hedonic inference.

        :param feature_matrix: FeatureMatrix from feature_matrix_builder
        :param property_ids: Ordered list matching feature_matrix rows
        :return: HedonicPrediction
        """

        self._validate_feature_matrix(feature_matrix)

        if len(property_ids) != len(feature_matrix.matrix):
            raise ValueError(
                "property_ids length does not match feature matrix rows"
            )

        estimates: Dict[str, float] = {}

        for idx, row in enumerate(feature_matrix.matrix):
            value = self._artifact.intercept
            for coef, x in zip(self._artifact.coefficients, row):
                value += coef * x

            estimates[property_ids[idx]] = float(value)

        dispersion = self._compute_dispersion(list(estimates.values()))

        return HedonicPrediction(
            model_id=self._artifact.model_id,
            model_version=self._artifact.model_version,
            feature_snapshot_hash=feature_matrix.feature_snapshot_hash,
            raw_estimates=estimates,
            dispersion_metric=dispersion,
            limitations=self._limitations()
        )

    # ------------------------------------------------------------------
    # Internal validation & utilities
    # ------------------------------------------------------------------

    def _validate_artifact(self) -> None:
        if len(self._artifact.coefficients) != len(self._artifact.feature_order):
            raise ValueError(
                "Coefficient count does not match feature order"
            )

    def _validate_feature_matrix(self, feature_matrix: "FeatureMatrix") -> None:
        if feature_matrix.feature_names != self._artifact.feature_order:
            raise ValueError(
                "Feature order mismatch between model artifact "
                "and feature matrix"
            )

    @staticmethod
    def _compute_dispersion(values: List[float]) -> float:
        """
        Compute simple dispersion metric (coefficient of variation).
        """
        if not values:
            return 0.0

        mean = sum(values) / len(values)
        if mean == 0:
            return 0.0

        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std_dev = math.sqrt(variance)

        return std_dev / abs(mean)

    @staticmethod
    def _limitations() -> List[str]:
        """
        Mandatory legal & methodological limitations.
        """
        return [
            "Hedonic model output is an estimate, not a final valuation.",
            "Model assumes linear relationships between features and price.",
            "Outputs must be reviewed in conjunction with other AVM models.",
            "Model does not account for undocumented property conditions.",
            "Results are subject to data quality and feature coverage limits."
        ]


# ----------------------------------------------------------------------
# Artifact loader (controlled, deterministic)
# ----------------------------------------------------------------------

def load_hedonic_artifact(path: str) -> HedonicModelArtifact:
    """
    Load hedonic model artifact from immutable JSON file.

    The artifact file MUST be registered in model_registry.yaml.
    """

    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    required_fields = [
        "model_id",
        "model_version",
        "feature_order",
        "coefficients",
        "intercept",
        "training_metadata"
    ]

    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Missing required artifact field: {field}")

    metadata_bytes = json.dumps(
        payload["training_metadata"],
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    training_metadata_hash = hashlib.sha256(metadata_bytes).hexdigest()

    return HedonicModelArtifact(
        model_id=payload["model_id"],
        model_version=payload["model_version"],
        feature_order=payload["feature_order"],
        coefficients=payload["coefficients"],
        intercept=float(payload["intercept"]),
        training_metadata_hash=training_metadata_hash
    )
