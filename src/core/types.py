"""Core type definitions for CD Optimizer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import hashlib
import time


class FileType(Enum):
    """Detected file categories used for pipeline routing."""

    IMAGE = auto()
    VIDEO = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    PDF = auto()
    CODE = auto()
    ARCHIVE = auto()
    MODEL_3D = auto()
    CAD = auto()
    DATABASE = auto()
    AI_MODEL = auto()
    TEXT = auto()
    BINARY = auto()
    UNKNOWN = auto()


class CompressionMode(Enum):
    LOSSLESS = "lossless"
    FAST = "fast"
    BALANCED = "balanced"
    ULTRA = "ultra"
    CUSTOM = "custom"


@dataclass
class QualityProfile:
    """User-selectable quality target."""

    name: str = "balanced"
    # 1.0 = perfect / lossless, 0.0 = maximum loss
    target_quality: float = 1.0
    preserve_edges: bool = True
    preserve_text: bool = True
    preserve_faces: bool = True
    preserve_transparency: bool = True
    max_psnr_drop_db: Optional[float] = None
    max_ssim_drop: Optional[float] = None
    custom_params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_percentage(cls, pct: int) -> "QualityProfile":
        """Create profile from 50–100 style percentage."""
        q = max(0.0, min(1.0, pct / 100.0))
        return cls(
            name=f"{pct}%",
            target_quality=q,
            preserve_edges=pct >= 80,
            preserve_text=pct >= 90,
            preserve_faces=pct >= 85,
        )


@dataclass
class AnalysisResult:
    """Result of pre-compression analysis."""

    file_path: Path
    file_type: FileType
    mime_type: str
    size_bytes: int
    entropy: float
    redundancy_estimate: float
    has_transparency: bool = False
    width: Optional[int] = None
    height: Optional[int] = None
    channels: Optional[int] = None
    duration_sec: Optional[float] = None
    sample_rate: Optional[int] = None
    language: Optional[str] = None
    encoding: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    duplicate_blocks: int = 0
    noise_estimate: float = 0.0
    color_distribution: Dict[str, float] = field(default_factory=dict)
    recommended_pipelines: List[str] = field(default_factory=list)
    ai_confidence: float = 0.0
    analysis_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": str(self.file_path),
            "file_type": self.file_type.name,
            "mime_type": self.mime_type,
            "size_bytes": self.size_bytes,
            "entropy": self.entropy,
            "redundancy_estimate": self.redundancy_estimate,
            "has_transparency": self.has_transparency,
            "width": self.width,
            "height": self.height,
            "channels": self.channels,
            "duration_sec": self.duration_sec,
            "sample_rate": self.sample_rate,
            "language": self.language,
            "encoding": self.encoding,
            "metadata": self.metadata,
            "duplicate_blocks": self.duplicate_blocks,
            "noise_estimate": self.noise_estimate,
            "color_distribution": self.color_distribution,
            "recommended_pipelines": self.recommended_pipelines,
            "ai_confidence": self.ai_confidence,
            "analysis_time_ms": self.analysis_time_ms,
        }


@dataclass
class CompressionStats:
    """Statistics produced by a compression run."""

    original_size: int
    compressed_size: int
    ratio: float
    percent_saved: float
    time_sec: float
    algorithm: str
    pipeline_stages: List[str]
    mode: str
    quality_score: Optional[float] = None
    psnr: Optional[float] = None
    ssim: Optional[float] = None
    lpips: Optional[float] = None
    checksum_original: str = ""
    checksum_restored: str = ""
    lossless: bool = False
    ai_confidence: float = 0.0
    cpu_percent: float = 0.0
    memory_peak_mb: float = 0.0
    gpu_used: bool = False
    energy_estimate_j: Optional[float] = None
    co2_saved_g: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def compute(
        cls,
        original_size: int,
        compressed_size: int,
        time_sec: float,
        algorithm: str,
        stages: List[str],
        mode: str,
        **kwargs: Any,
    ) -> "CompressionStats":
        ratio = original_size / compressed_size if compressed_size > 0 else 0.0
        percent = (1.0 - compressed_size / original_size) * 100.0 if original_size > 0 else 0.0
        return cls(
            original_size=original_size,
            compressed_size=compressed_size,
            ratio=ratio,
            percent_saved=percent,
            time_sec=time_sec,
            algorithm=algorithm,
            pipeline_stages=stages,
            mode=mode,
            **kwargs,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_size": self.original_size,
            "compressed_size": self.compressed_size,
            "ratio": round(self.ratio, 4),
            "percent_saved": round(self.percent_saved, 2),
            "time_sec": round(self.time_sec, 3),
            "algorithm": self.algorithm,
            "pipeline_stages": self.pipeline_stages,
            "mode": self.mode,
            "quality_score": self.quality_score,
            "psnr": self.psnr,
            "ssim": self.ssim,
            "lpips": self.lpips,
            "checksum_original": self.checksum_original,
            "checksum_restored": self.checksum_restored,
            "lossless": self.lossless,
            "ai_confidence": self.ai_confidence,
            "cpu_percent": self.cpu_percent,
            "memory_peak_mb": self.memory_peak_mb,
            "gpu_used": self.gpu_used,
            "energy_estimate_j": self.energy_estimate_j,
            "co2_saved_g": self.co2_saved_g,
            "extra": self.extra,
        }


def sha256_file(path: Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
