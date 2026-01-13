"""
feature_pipeline/image/floor_count_estimator.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Floor Count Estimation Proxy (Image Feature Layer).

This module estimates a RELATIVE floor-count proxy
from image geometry only.

ABSOLUTE PROHIBITIONS
---------------------
- No real-world floor count claim
- No legal / cadastral inference
- No valuation logic
- No asset classification
- No ML / LLM usage
- No autonomous detection

IMPORTANT
---------
Output is a TECHNICAL IMAGE-BASED PROXY ONLY.
"""

from __future__ import annotations

from typing import Dict, Any, Optional

try:
    from PIL import Image
except ImportError as exc:
    raise ImportError(
        "Pillow is required for floor_count_estimator"
    ) from exc


class FloorCountEstimationError(Exception):
    """Raised when floor count estimation fails."""


class FloorCountEstimator:
    """
    Deterministic floor count proxy estimator.

    Estimation Logic (Governance-safe)
    ----------------------------------
    - Uses facade height in pixels
    - Divides by assumed average floor height (pixels)
    - No semantic understanding
    - No object detection
    """

    def __init__(
        self,
        assumed_floor_height_px: int = 80,
    ) -> None:
        """
        Parameters
        ----------
        assumed_floor_height_px : int
            Technical heuristic ONLY.
            Does NOT represent real-world floor height.
        """
        if assumed_floor_height_px <= 0:
            raise ValueError(
                "assumed_floor_height_px must be positive"
            )

        self.assumed_floor_height_px = assumed_floor_height_px

    def _validate_image(self, image: Image.Image) -> None:
        if image is None:
            raise FloorCountEstimationError("Image must not be None")

        if not isinstance(image, Image.Image):
            raise FloorCountEstimationError(
                f"Expected PIL.Image.Image, got {type(image).__name__}"
            )

    def estimate(
        self,
        image: Image.Image,
        facade_bbox: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        """
        Estimate floor count proxy.

        Parameters
        ----------
        image : PIL.Image.Image
            Input image.
        facade_bbox : Optional[Dict[str, int]]
            Optional pre-validated bounding box:
            {
                "y_min": int,
                "y_max": int
            }

            NOTE:
            -----
            Bounding box must come from an upstream,
            governance-approved signal source.
            This module does NOT detect floors or facades.

        Returns
        -------
        Dict[str, Any]
            {
                "floor_count_proxy": float | None,
                "facade_height_px": int | None,
                "assumed_floor_height_px": int,
                "method": str,
                "disclaimer": str
            }
        """
        self._validate_image(image)

        _, image_height = image.size

        if image_height <= 0:
            raise FloorCountEstimationError(
                "Invalid image height"
            )

        if facade_bbox is None:
            return {
                "floor_count_proxy": None,
                "facade_height_px": None,
                "assumed_floor_height_px": self.assumed_floor_height_px,
                "method": "no_bbox_provided",
                "disclaimer": (
                    "Floor count could not be estimated because "
                    "no facade bounding box was provided. "
                    "This module does not perform detection."
                ),
            }

        for key in ("y_min", "y_max"):
            if key not in facade_bbox:
                raise FloorCountEstimationError(
                    f"Missing bbox field: {key}"
                )

        y_min = max(0, int(facade_bbox["y_min"]))
        y_max = min(image_height, int(facade_bbox["y_max"]))

        if y_max <= y_min:
            raise FloorCountEstimationError(
                "Invalid facade bounding box coordinates"
            )

        facade_height_px = y_max - y_min
        floor_count_proxy = (
            facade_height_px / self.assumed_floor_height_px
        )

        return {
            "floor_count_proxy": floor_count_proxy,
            "facade_height_px": facade_height_px,
            "assumed_floor_height_px": self.assumed_floor_height_px,
            "method": "pixel_height_ratio",
            "disclaimer": (
                "Floor count is an image-based proxy only. "
                "It does NOT represent actual number of floors, "
                "legal construction levels, or valuation relevance."
            ),
        }


def estimate_floor_count(
    image: Image.Image,
    facade_bbox: Optional[Dict[str, int]] = None,
    assumed_floor_height_px: int = 80,
) -> Dict[str, Any]:
    """
    Functional wrapper for floor count proxy estimation.

    SAFE FOR
    --------
    - Image feature pipelines
    - Descriptive analytics
    - Audit replay

    NOT ALLOWED FOR
    ---------------
    - Valuation
    - Regulatory inference
    - Asset approval
    """
    estimator = FloorCountEstimator(
        assumed_floor_height_px=assumed_floor_height_px
    )
    return estimator.estimate(image, facade_bbox)
