"""Compression modes and quality profiles."""

from __future__ import annotations

from enum import Enum
from typing import Dict, Any

from .types import QualityProfile


class CompressionMode(str, Enum):
    LOSSLESS = "lossless"
    FAST = "fast"
    BALANCED = "balanced"
    ULTRA = "ultra"
    CUSTOM = "custom"


# Default quality profiles
QUALITY_PROFILES: Dict[str, QualityProfile] = {
    "perfect": QualityProfile(name="perfect", target_quality=1.0),
    "99": QualityProfile.from_percentage(99),
    "98": QualityProfile.from_percentage(98),
    "95": QualityProfile.from_percentage(95),
    "90": QualityProfile.from_percentage(90),
    "80": QualityProfile.from_percentage(80),
    "70": QualityProfile.from_percentage(70),
    "50": QualityProfile.from_percentage(50),
}


MODE_DEFAULTS: Dict[CompressionMode, Dict[str, Any]] = {
    CompressionMode.LOSSLESS: {
        "max_stages": 8,
        "allow_lossy": False,
        "allow_neural": False,
        "search_attempts": 1,
        "timeout_sec": 300,
        "prefer_speed": False,
    },
    CompressionMode.FAST: {
        "max_stages": 3,
        "allow_lossy": True,
        "allow_neural": False,
        "search_attempts": 1,
        "timeout_sec": 30,
        "prefer_speed": True,
    },
    CompressionMode.BALANCED: {
        "max_stages": 6,
        "allow_lossy": True,
        "allow_neural": True,
        "search_attempts": 3,
        "timeout_sec": 120,
        "prefer_speed": False,
    },
    CompressionMode.ULTRA: {
        "max_stages": 12,
        "allow_lossy": True,
        "allow_neural": True,
        "search_attempts": 12,
        "timeout_sec": 3600,
        "prefer_speed": False,
        "ensemble": True,
    },
    CompressionMode.CUSTOM: {
        "max_stages": 20,
        "allow_lossy": True,
        "allow_neural": True,
        "search_attempts": 5,
        "timeout_sec": 600,
        "prefer_speed": False,
    },
}
