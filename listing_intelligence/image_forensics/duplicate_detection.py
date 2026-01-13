"""
Duplicate / Reused Image Detection Signal
-----------------------------------------

Role:
- Detect potential duplicate or reused images across listings
  using image fingerprint / perceptual hash similarity.

Governance:
- Signal-only
- Non-decisive
- Deterministic
- No fraud conclusion
- No valuation impact

Compliant with:
- MASTER_SPEC.md
- IMPLEMENTATION STATUS – LISTING INTELLIGENCE
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import hashlib
import json


# =========================
# Data Structures
# =========================

@dataclass(frozen=True)
class ImageFingerprint:
    image_id: str
    fingerprint: str  # perceptual hash or stable fingerprint


@dataclass(frozen=True)
class DuplicateImageSignal:
    duplicate_probability: float  # descriptive, 0.0 – 1.0
    duplicate_group_id: str
    similarity_score: float
    compared_images: List[str]
    signal_hash: str


# =========================
# Utility Functions
# =========================

def compute_similarity(fp_a: str, fp_b: str) -> float:
    """
    Compute similarity between two image fingerprints.

    Assumption:
    - Fingerprints are equal-length strings.
    - Similarity = normalized character match ratio.

    Deterministic & model-free.
    """
    if len(fp_a) != len(fp_b) or not fp_a:
        return 0.0

    matches = sum(1 for a, b in zip(fp_a, fp_b) if a == b)
    return matches / len(fp_a)


def compute_signal_hash(payload: Dict[str, Any]) -> str:
    """
    Deterministic signal hash for lineage & audit.
    """
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# =========================
# Core Signal Generator
# =========================

def generate_duplicate_image_signal(
    target_image: ImageFingerprint,
    reference_images: List[ImageFingerprint],
    similarity_threshold: float = 0.9,
) -> DuplicateImageSignal:
    """
    Generate duplicate image detection signal.

    Inputs:
    - target_image: fingerprint of the current listing image
    - reference_images: fingerprints from other listings
    - similarity_threshold: static governance threshold

    Output:
    - DuplicateImageSignal (signal-only)
    """

    highest_similarity = 0.0
    matched_images: List[str] = []

    for ref in reference_images:
        similarity = compute_similarity(
            target_image.fingerprint, ref.fingerprint
        )
        if similarity >= similarity_threshold:
            matched_images.append(ref.image_id)
            highest_similarity = max(highest_similarity, similarity)

    if not matched_images:
        duplicate_probability = 0.0
        similarity_score = 0.0
    else:
        duplicate_probability = round(highest_similarity, 3)
        similarity_score = round(highest_similarity, 3)

    duplicate_group_id_source = {
        "target_image_id": target_image.image_id,
        "matched_images": sorted(matched_images),
    }
    duplicate_group_id = hashlib.sha256(
        json.dumps(duplicate_group_id_source, sort_keys=True)
        .encode("utf-8")
    ).hexdigest()

    payload = {
        "target_image_id": target_image.image_id,
        "matched_images": matched_images,
        "similarity_score": similarity_score,
        "threshold": similarity_threshold,
    }

    return DuplicateImageSignal(
        duplicate_probability=duplicate_probability,
        duplicate_group_id=duplicate_group_id,
        similarity_score=similarity_score,
        compared_images=matched_images,
        signal_hash=compute_signal_hash(payload),
    )
