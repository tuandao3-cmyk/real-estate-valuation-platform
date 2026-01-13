"""
feature_pipeline/pipelines/feature_error_handler.py

ROLE (MASTER_SPEC COMPLIANT)
---------------------------
Feature Pipeline Error Handling & Normalization.

This module standardizes errors raised during feature extraction
and validation for auditability and governance control.

ABSOLUTE PROHIBITIONS
---------------------
- No error masking
- No silent fallback
- No feature regeneration
- No ML / LLM
- No valuation logic
"""

from __future__ import annotations

import traceback
from typing import Dict, Any, Optional, Type


class FeaturePipelineError(Exception):
    """
    Base exception for all feature pipeline errors.
    """

    error_code: str = "FEATURE_PIPELINE_ERROR"

    def __init__(
        self,
        message: str,
        *,
        stage: Optional[str] = None,
        feature_name: Optional[str] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.feature_name = feature_name
        self.original_exception = original_exception


class FeatureExtractionError(FeaturePipelineError):
    error_code = "FEATURE_EXTRACTION_ERROR"


class FeatureValidationError(FeaturePipelineError):
    error_code = "FEATURE_VALIDATION_ERROR"


class FeatureSchemaError(FeaturePipelineError):
    error_code = "FEATURE_SCHEMA_ERROR"


class FeatureErrorHandler:
    """
    Deterministic error handler for feature pipeline.

    Responsibilities
    ----------------
    - Normalize exception structure
    - Attach governance metadata
    - Preserve original stack trace
    - Prepare error for logging / audit storage
    """

    def normalize(
        self,
        exc: Exception,
        *,
        stage: str,
        feature_name: Optional[str] = None,
        error_type: Optional[Type[FeaturePipelineError]] = None,
    ) -> FeaturePipelineError:
        """
        Normalize any exception into a FeaturePipelineError.

        Parameters
        ----------
        exc : Exception
            Original exception.
        stage : str
            Pipeline stage name (e.g. 'extraction', 'validation').
        feature_name : Optional[str]
            Feature identifier.
        error_type : Optional[Type[FeaturePipelineError]]
            Specific error subclass.

        Returns
        -------
        FeaturePipelineError
        """
        error_cls = error_type or FeaturePipelineError

        return error_cls(
            message=str(exc),
            stage=stage,
            feature_name=feature_name,
            original_exception=exc,
        )

    def to_error_record(
        self,
        error: FeaturePipelineError,
    ) -> Dict[str, Any]:
        """
        Convert normalized error into structured record
        suitable for logging or audit storage.

        Returns
        -------
        Dict[str, Any]
        """
        record: Dict[str, Any] = {
            "error_code": error.error_code,
            "message": str(error),
            "stage": error.stage,
            "feature_name": error.feature_name,
            "exception_type": type(error.original_exception).__name__
            if error.original_exception
            else type(error).__name__,
            "traceback": self._format_traceback(error.original_exception),
            "disclaimer": (
                "This error record is generated for audit and governance. "
                "No automatic correction or inference has been applied."
            ),
        }

        return record

    @staticmethod
    def _format_traceback(
        exc: Optional[Exception],
    ) -> Optional[str]:
        if exc is None:
            return None
        return "".join(
            traceback.format_exception(
                type(exc), exc, exc.__traceback__
            )
        )


def handle_feature_error(
    exc: Exception,
    *,
    stage: str,
    feature_name: Optional[str] = None,
    error_type: Optional[Type[FeaturePipelineError]] = None,
) -> Dict[str, Any]:
    """
    Functional helper to normalize and serialize feature pipeline errors.

    SAFE FOR
    --------
    - Pipeline orchestration
    - Centralized logging
    - Audit trail generation

    NOT ALLOWED FOR
    ---------------
    - Suppressing failures
    - Retrying logic
    - Feature mutation
    """
    handler = FeatureErrorHandler()
    normalized = handler.normalize(
        exc,
        stage=stage,
        feature_name=feature_name,
        error_type=error_type,
    )
    return handler.to_error_record(normalized)
