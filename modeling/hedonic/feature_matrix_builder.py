"""
Hedonic Feature Matrix Builder

🚫 DO NOT VIOLATE MASTER_SPEC.md
🚫 THIS MODULE DOES NOT PERFORM VALUATION
🚫 THIS MODULE DOES NOT CONTAIN BUSINESS RULES

Purpose:
- Build deterministic feature matrix for hedonic models
- Enforce schema, ordering, and reproducibility
- Attach feature_snapshot_hash for audit & lineage
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class FeatureMatrix:
    """
    Immutable container for hedonic feature matrix
    """
    feature_names: List[str]
    matrix: List[List[float]]
    feature_snapshot_hash: str


class FeatureMatrixBuilder:
    """
    Controlled builder for hedonic feature matrices.

    This class:
    - Consumes immutable feature snapshots
    - Produces deterministic feature matrices
    - Does NOT perform normalization or learning
    """

    def __init__(self, expected_schema: List[str]):
        """
        :param expected_schema: Ordered list of required feature names
        """
        self._expected_schema = expected_schema

    def build(
        self,
        feature_snapshot: Dict[str, Dict[str, float]]
    ) -> FeatureMatrix:
        """
        Build feature matrix from snapshot.

        :param feature_snapshot:
            {
              "property_id_1": { "feature_a": x, "feature_b": y, ... },
              "property_id_2": { ... }
            }

        :return: FeatureMatrix
        """

        self._validate_snapshot(feature_snapshot)

        feature_names = list(self._expected_schema)
        matrix: List[List[float]] = []

        for property_id, features in feature_snapshot.items():
            row = []
            for fname in feature_names:
                value = features.get(fname)
                if value is None:
                    raise ValueError(
                        f"Missing required feature '{fname}' "
                        f"for property_id={property_id}"
                    )
                row.append(float(value))
            matrix.append(row)

        snapshot_hash = self._compute_snapshot_hash(
            feature_snapshot,
            feature_names
        )

        return FeatureMatrix(
            feature_names=feature_names,
            matrix=matrix,
            feature_snapshot_hash=snapshot_hash
        )

    def _validate_snapshot(self, snapshot: Dict[str, Dict[str, float]]) -> None:
        """
        Enforce snapshot integrity & schema compliance.
        """
        if not snapshot:
            raise ValueError("Feature snapshot is empty")

        for property_id, features in snapshot.items():
            if not isinstance(features, dict):
                raise TypeError(
                    f"Invalid feature format for property_id={property_id}"
                )

            missing = set(self._expected_schema) - set(features.keys())
            if missing:
                raise ValueError(
                    f"Feature snapshot missing required features "
                    f"{missing} for property_id={property_id}"
                )

    @staticmethod
    def _compute_snapshot_hash(
        snapshot: Dict[str, Dict[str, float]],
        feature_order: List[str]
    ) -> str:
        """
        Compute deterministic hash for reproducibility & audit.

        Hash covers:
        - property ordering
        - feature ordering
        - feature values
        """

        canonical_payload = {
            "feature_order": feature_order,
            "properties": []
        }

        for property_id in sorted(snapshot.keys()):
            ordered_features = {
                fname: snapshot[property_id][fname]
                for fname in feature_order
            }
            canonical_payload["properties"].append({
                "property_id": property_id,
                "features": ordered_features
            })

        payload_bytes = json.dumps(
            canonical_payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

        return hashlib.sha256(payload_bytes).hexdigest()
