"""
feature_pipeline/image/facade_width_estimator.py

ROLE (MASTER_SPEC COMPLIANT)
----------------------------
Facade Width Estimation Proxy (Image Feature Layer).

This module estimates a RELATIVE facade width proxy
from a single image using basic geometric signals.

ABSOLUTE PROHIBITIONS
---------------------
- No real-world dimension claim
- No legal / cadastral inference
- No valuation or desirability logic
- No asset classification
- No ML / LLM usage
- No workflow authority

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
        "Pillow is required for facade_width_estimator"
    ) from exc


class FacadeWidthEstimationError(Exception):
    """Raised when facade width estimation fails."""


class FacadeWidthEstimator:
    """
    Deterministic facade width proxy estimator.

    Estimation Logic (Governance-safe)
    ----------------------------------
    - Use image width as reference
    - Estimate facade bounding span ratio
    - No semantic detection
    - No object recognition
    """

    def __init__(self) -> None:
        pass

    def _validate_image(self, image: Image.Image) -> None:
        if image is None:
            raise FacadeWidthEstimationError("Image must not be None")

        if not isinstance(image, Image.Image):
            raise FacadeWidthEstimationError(
                f"Expected PIL.Image.Image, got {type(image).__name__}"
            )

    def estimate(
        self,
        image: Image.Image,
        facade_bbox: Optional[Dict[str, int]] = None,
    ) -> Dict[str, Any]:
        """
        Estimate facade width proxy.

        Parameters
        ----------
        image : PIL.Image.Image
            Input image.
        facade_bbox : Optional[Dict[str, int]]
            Optional pre-validated bounding box:
            {
                "x_min": int,
                "x_max": int
            }

            NOTE:
            -----
            BBox must come from an upstream, governance-approved
            signal generator (if any). This module does NOT detect
            facades by itself.

        Returns
        -------
        Dict[str, Any]
            {
                "facade_width_ratio": float,
                "image_width_px": int,
                "facade_width_px": int | None,
                "method": str,
                "disclaimer": str
            }
        """
        self._validate_image(image)

        image_width, _ = image.size

        if image_width <= 0:
            raise FacadeWidthEstimationError(
                "Invalid image width"
            )

        if facade_bbox is None:
            # Fallback: no facade localization available
            return {
                "facade_width_ratio": None,
                "image_width_px": image_width,
                "facade_width_px": None,
                "method": "no_bbox_provided",
                "disclaimer": (
                    "Facade width could not be estimated because "
                    "no facade bounding box was provided. "
                    "This module does not perform detection."
                ),
            }

        for key in ("x_min", "x_max"):
            if key not in facade_bbox:
                raise FacadeWidthEstimationError(
                    f"Missing bbox field: {key}"
                )

        x_min = max(0, int(facade_bbox["x_min"]))
        x_max = min(image_width, int(facade_bbox["x_max"]))

        if x_max <= x_min:
            raise FacadeWidthEstimationError(
                "Invalid facade bounding box coordinates"
            )

        facade_width_px = x_max - x_min
        facade_width_ratio = facade_width_px / image_width

        return {
            "facade_width_ratio": facade_width_ratio,
            "image_width_px": image_width,
            "facade_width_px": facade_width_px,
            "method": "bbox_ratio_estimation",
            "disclaimer": (
                "Facade width is an image-based relative proxy only. "
                "It does NOT represent real-world dimensions, "
                "legal frontage, or valuation relevance."
            ),
        }


def estimate_facade_width(
    image: Image.Image,
    facade_bbox: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """
    Functional wrapper for facade width proxy estimation.

    SAFE FOR
    --------
    - Image feature pipelines
    - Human descriptive review
    - Audit replay

    NOT ALLOWED FOR
    ---------------
    - Valuation
    - Asset sizing claims
    - Approval or risk routing
    """
    estimator = FacadeWidthEstimator()
    return estimator.estimate(image, facade_bbox)
