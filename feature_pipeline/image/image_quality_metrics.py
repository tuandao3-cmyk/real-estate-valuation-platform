"""
feature_pipeline/image/image_quality_metrics.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Image Quality Metrics Generator (Feature Layer).

This module extracts LOW-LEVEL, TECHNICAL image quality metrics
for descriptive and audit purposes only.

ABSOLUTE PROHIBITIONS
---------------------
- No aesthetic judgment
- No property quality inference
- No fraud conclusion
- No trust / risk scoring
- No valuation logic
- No workflow influence

Metrics are DESCRIPTIVE SIGNALS ONLY.

GOVERNANCE GUARANTEES
--------------------
- Deterministic
- No ML / No AI inference
- No training
- Stateless
- Reproducible
- Audit-friendly
"""

from __future__ import annotations

from typing import Dict, Any

import math

try:
    from PIL import Image, ImageStat
except ImportError as exc:
    raise ImportError(
        "Pillow is required for image_quality_metrics"
    ) from exc


class ImageQualityError(Exception):
    """Raised when image quality metric extraction fails."""


class ImageQualityMetricsExtractor:
    """
    Deterministic image quality metrics extractor.

    Metrics Scope
    -------------
    - Image dimensions
    - Aspect ratio
    - Brightness (mean pixel intensity)
    - Contrast (pixel intensity std deviation)
    - Sharpness proxy (Laplacian variance approximation)

    IMPORTANT
    ---------
    Metrics are purely technical.
    No interpretation or judgment is performed.
    """

    def __init__(self) -> None:
        pass

    def _validate_image(self, image: Image.Image) -> None:
        if image is None:
            raise ImageQualityError("Image must not be None")

        if not isinstance(image, Image.Image):
            raise ImageQualityError(
                f"Expected PIL.Image.Image, got {type(image).__name__}"
            )

    def _compute_brightness(self, image: Image.Image) -> float:
        """
        Compute mean brightness using grayscale conversion.
        """
        gray = image.convert("L")
        stat = ImageStat.Stat(gray)
        return float(stat.mean[0])

    def _compute_contrast(self, image: Image.Image) -> float:
        """
        Compute contrast as standard deviation of grayscale pixel values.
        """
        gray = image.convert("L")
        stat = ImageStat.Stat(gray)
        return float(stat.stddev[0])

    def _compute_sharpness_proxy(self, image: Image.Image) -> float:
        """
        Compute a simple sharpness proxy.

        Governance note:
        ----------------
        This is NOT a perceptual quality score.
        It is a mathematical edge-variation proxy only.
        """
        gray = image.convert("L")
        pixels = list(gray.getdata())

        if len(pixels) < 2:
            return 0.0

        diffs = [
            abs(pixels[i] - pixels[i - 1])
            for i in range(1, len(pixels))
        ]

        mean_diff = sum(diffs) / len(diffs)
        variance = sum(
            (d - mean_diff) ** 2 for d in diffs
        ) / len(diffs)

        return math.sqrt(variance)

    def extract(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract image quality metrics.

        Parameters
        ----------
        image : PIL.Image.Image
            Loaded image object.

        Returns
        -------
        Dict[str, Any]
            Descriptive image quality metrics.
        """
        self._validate_image(image)

        width, height = image.size
        aspect_ratio = width / height if height > 0 else None

        metrics = {
            "width": width,
            "height": height,
            "aspect_ratio": aspect_ratio,
            "brightness_mean": self._compute_brightness(image),
            "contrast_stddev": self._compute_contrast(image),
            "sharpness_proxy": self._compute_sharpness_proxy(image),
        }

        return metrics


def extract_image_quality_metrics(
    image: Image.Image,
) -> Dict[str, Any]:
    """
    Functional wrapper for image quality metric extraction.

    SAFE FOR
    --------
    - Feature pipeline
    - Image diagnostics
    - Audit replay

    NOT ALLOWED FOR
    ---------------
    - Trust scoring
    - Fraud decision
    - Valuation adjustment
    - Approval routing

    Returns
    -------
    Dict[str, Any]
        Image quality metrics (descriptive only).
    """
    extractor = ImageQualityMetricsExtractor()
    return extractor.extract(image)
