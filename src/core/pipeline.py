"""Pipeline engine – sequences of compression stages."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import logging
import time
import tempfile
import shutil

from .types import AnalysisResult, CompressionStats, CompressionMode

logger = logging.getLogger(__name__)


class PipelineStage(ABC):
    """Abstract base for a single compression / transform stage."""

    name: str = "base"
    supports_lossless: bool = True
    supports_lossy: bool = False
    requires_gpu: bool = False

    @abstractmethod
    def apply(
        self,
        data: bytes,
        context: Dict[str, Any],
        analysis: Optional[AnalysisResult] = None,
    ) -> bytes:
        """Transform input bytes → output bytes."""
        ...

    def can_apply(self, analysis: AnalysisResult, mode: CompressionMode) -> bool:
        return True

    def estimate_gain(self, analysis: AnalysisResult) -> float:
        """Rough expected size reduction factor (0–1). Higher is better."""
        return 0.1


@dataclass
class PipelineResult:
    data: bytes
    stages_applied: List[str]
    stats: Optional[CompressionStats] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None


class Pipeline:
    """Ordered sequence of PipelineStage instances."""

    def __init__(
        self,
        name: str,
        stages: List[PipelineStage],
        mode: CompressionMode = CompressionMode.BALANCED,
    ):
        self.name = name
        self.stages = stages
        self.mode = mode

    def run(
        self,
        data: bytes,
        analysis: Optional[AnalysisResult] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> PipelineResult:
        context = context or {}
        applied: List[str] = []
        current = data
        start = time.perf_counter()

        try:
            for stage in self.stages:
                if analysis and not stage.can_apply(analysis, self.mode):
                    logger.debug("Skipping stage %s (not applicable)", stage.name)
                    continue
                logger.debug("Applying stage: %s", stage.name)
                current = stage.apply(current, context, analysis)
                applied.append(stage.name)
                if len(current) > len(data) * 1.5 and len(applied) < 3:
                    logger.warning("Stage %s expanded data significantly; continuing", stage.name)

            elapsed = time.perf_counter() - start
            stats = CompressionStats.compute(
                original_size=len(data),
                compressed_size=len(current),
                time_sec=elapsed,
                algorithm=self.name,
                stages=applied,
                mode=self.mode.value,
            )
            return PipelineResult(
                data=current,
                stages_applied=applied,
                stats=stats,
                success=True,
            )
        except Exception as e:
            logger.exception("Pipeline %s failed", self.name)
            return PipelineResult(
                data=data,
                stages_applied=applied,
                success=False,
                error=str(e),
            )

    def __repr__(self) -> str:
        return f"Pipeline(name={self.name!r}, stages={[s.name for s in self.stages]})"
