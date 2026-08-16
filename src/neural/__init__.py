"""Neural compression modules (autoencoders, learned codecs, entropy models).

This package will host:
- Image autoencoders / VAEs
- Learned image codecs (Torch / ONNX)
- Video temporal models
- Neural entropy models
- Diffusion-based compressors (research)

Currently provides a registration stub so the orchestrator can discover future stages.
"""

from src.core.registry import CodecRegistry
import logging

logger = logging.getLogger(__name__)


def register_neural_codecs() -> None:
    """Register any available neural codecs (no-op until models are trained/exported)."""
    logger.info("Neural codec registry ready (no models loaded yet)")
