"""Registries for analyzers, codecs and pipelines."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Type
import logging

logger = logging.getLogger(__name__)


class CodecRegistry:
    """Central registry of available codecs / compressors."""

    _codecs: Dict[str, Any] = {}
    _aliases: Dict[str, str] = {}

    @classmethod
    def register(cls, name: str, codec: Any, aliases: Optional[List[str]] = None) -> None:
        cls._codecs[name.lower()] = codec
        if aliases:
            for a in aliases:
                cls._aliases[a.lower()] = name.lower()
        logger.debug("Registered codec: %s", name)

    @classmethod
    def get(cls, name: str) -> Any:
        key = name.lower()
        if key in cls._aliases:
            key = cls._aliases[key]
        if key not in cls._codecs:
            raise KeyError(f"Codec '{name}' not registered")
        return cls._codecs[key]

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._codecs.keys())

    @classmethod
    def has(cls, name: str) -> bool:
        key = name.lower()
        return key in cls._codecs or key in cls._aliases


class AnalyzerRegistry:
    """Registry of file analyzers."""

    _analyzers: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, analyzer: Any) -> None:
        cls._analyzers[name.lower()] = analyzer
        logger.debug("Registered analyzer: %s", name)

    @classmethod
    def get(cls, name: str) -> Any:
        key = name.lower()
        if key not in cls._analyzers:
            raise KeyError(f"Analyzer '{name}' not registered")
        return cls._analyzers[key]

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._analyzers.keys())


class PipelineRegistry:
    """Registry of named pipelines."""

    _pipelines: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, pipeline_factory: Callable) -> None:
        cls._pipelines[name.lower()] = pipeline_factory
        logger.debug("Registered pipeline: %s", name)

    @classmethod
    def get(cls, name: str) -> Any:
        key = name.lower()
        if key not in cls._pipelines:
            raise KeyError(f"Pipeline '{name}' not registered")
        return cls._pipelines[key]

    @classmethod
    def list(cls) -> List[str]:
        return sorted(cls._pipelines.keys())
