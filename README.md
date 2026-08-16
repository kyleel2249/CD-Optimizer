# CD Optimizer

**The World's Most Advanced AI-Powered File Compression Platform**

CD Optimizer is a production-grade, modular compression engine that automatically selects and orchestrates the optimal compression strategy for every file — lossless, visually lossless, configurable lossy, neural, semantic, predictive, and hybrid AI pipelines.

It aims to approach theoretical entropy limits while respecting quality constraints, continuously learning from compression outcomes, and benchmarking against state-of-the-art codecs.

## Vision

For every file, search for the smallest mathematically achievable representation while respecting the selected quality constraints. Learn continuously from prior compressions, benchmark against state-of-the-art codecs, and automatically adopt the best-performing strategy for each file type.

## Key Capabilities

- **Lossless** – Bit-perfect restoration with cryptographic checksum verification
- **Visually Lossless / Smart Lossy** – Human-eye-identical quality
- **Configurable Lossy** – 99% → 50% quality or custom
- **Neural Compression** – Autoencoders, VAEs, Transformers, learned codecs
- **Semantic & Predictive** – Context-aware, language-aware, structure-aware
- **Adaptive Multi-Stage Pipelines** – Preprocessing → Deduplication → Entropy coding → Neural stages
- **Automatic File-Type Intelligence** – Images, Video, Audio, Documents, Code, Archives, 3D, CAD, Databases, AI Models, and everything else
- **Modes**: Ultra (max ratio), Balanced, Fast, Lossless, Custom
- **Hardware Acceleration**: CUDA, OpenCL, Metal, DirectML, TensorRT, Vulkan Compute, AVX/AVX2/AVX-512, multi-threading
- **Batch Processing**, REST API, CLI, modern GUI
- **Security**: Encrypted archives, password protection, SHA-256 integrity, recovery records
- **Analytics**: Size savings, energy/CO₂ estimates, AI confidence, algorithm used

## Supported Formats (and more)

| Category     | Formats                                      |
|--------------|----------------------------------------------|
| Images       | PNG, JPEG, JPG, WEBP, AVIF, HEIF, GIF, BMP, TIFF, RAW, SVG, PSD |
| Video        | MP4, MOV, AVI, MKV, WEBM, MPEG, FLV, WMV, HEVC, AV1 |
| Audio        | MP3, WAV, FLAC, AAC, OGG, M4A, AIFF          |
| Documents    | PDF, DOCX, DOC, PPT, PPTX, XLS, XLSX, TXT, CSV, EPUB, HTML, XML, JSON |
| Source Code  | Python, JS/TS, Java, Go, Rust, C/C++, PHP, Ruby, Swift, Kotlin |
| Archives     | ZIP, RAR, 7Z, TAR, GZIP, BZ2                 |
| 3D / CAD     | OBJ, FBX, GLTF, USD, STL, DWG, DXF           |
| Databases    | SQLite, MySQL/PostgreSQL dumps               |
| AI Models    | ONNX, TensorFlow, PyTorch, GGUF, Safetensors |
| Everything else | Accepted and routed to best generic pipeline |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                         │
│  GUI (Next.js)  ·  CLI  ·  REST API  ·  Batch / Cloud       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                   Orchestrator / AI Controller              │
│  File Analysis → Pipeline Search → Quality Validation →     │
│  Continuous Learning & Model Updates                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Analyzers   │   │   Pipelines   │   │    Codecs     │
│ Entropy,      │   │ Image/Video/  │   │ zstd, Brotli, │
│ Redundancy,   │   │ Audio/PDF/    │   │ LZMA, FFmpeg, │
│ Semantic,     │   │ Code/Generic  │   │ Neural, etc.  │
│ Metadata      │   │ + Neural      │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Quality Metrics & Security Layer               │
│  PSNR / SSIM / LPIPS / Audio / OCR / Checksums / Encryption │
└─────────────────────────────────────────────────────────────┘
```

See `docs/architecture/` for detailed design documents.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Rust (optional, for high-performance components)
- FFmpeg, libwebp, libavif, etc. (system packages)
- CUDA toolkit (optional, for GPU acceleration)

### Installation

```bash
# Clone
git clone https://github.com/kyleel2249/CD-Optimizer.git
cd CD-Optimizer

# Python backend + core
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend && npm install && cd ..

# Optional: build Rust components
# cargo build --release
```

### CLI Usage

```bash
# Compress a single file (auto mode)
python -m cli.cd_optimizer compress input.png -o output.cdopt

# Lossless
python -m cli.cd_optimizer compress input.pdf --mode lossless

# Ultra mode (max ratio)
python -m cli.cd_optimizer compress video.mp4 --mode ultra --quality 95

# Batch
python -m cli.cd_optimizer batch ./folder --recursive --mode balanced

# Decompress
python -m cli.cd_optimizer decompress output.cdopt -o restored.png
```

### REST API

```bash
uvicorn backend.api.main:app --reload --port 8000
```

Endpoints: `/compress`, `/decompress`, `/analyze`, `/batch`, `/health`, `/metrics`

### Docker

```bash
docker compose up --build
```

## Project Structure

```
CD-Optimizer/
├── src/                    # Core compression engine
│   ├── core/               # Orchestrator, pipeline engine, registry
│   ├── analyzers/          # Entropy, semantic, visual, audio analyzers
│   ├── pipelines/          # File-type specific pipelines
│   ├── neural/             # Neural codecs, autoencoders, entropy models
│   ├── codecs/             # Wrappers for classical + hybrid codecs
│   ├── quality/            # Metrics (PSNR, SSIM, LPIPS, …)
│   ├── security/           # Encryption, integrity, recovery
│   └── utils/              # Helpers, hardware detection, etc.
├── backend/                # FastAPI REST service
├── frontend/               # Next.js + Tailwind modern UI
├── cli/                    # Command-line interface
├── docs/                   # Architecture, API, algorithms
├── tests/                  # Unit, integration, benchmarks
├── models/                 # Trained / exported neural models
├── configs/                # Default pipelines, quality profiles
├── docker/                 # Dockerfiles & compose
└── scripts/                # Training, benchmarking, release scripts
```

## Modes

| Mode       | Priority              | Description                                      |
|------------|-----------------------|--------------------------------------------------|
| **Lossless** | Correctness         | Bit-perfect, SHA-256 verified                    |
| **Fast**     | Speed               | Minimal stages, hardware accelerated             |
| **Balanced** | Ratio + Quality + Speed | Default intelligent choice                    |
| **Ultra**    | Maximum ratio       | Multi-attempt AI search + neural + ensemble      |
| **Custom**   | User-defined        | Advanced mode – full control over stages         |

## Development Roadmap

1. **Foundation** (current) – Modular architecture, classical codecs, analysis, CLI/API skeleton, docs
2. **Intelligent Pipelines** – Full file-type routers, multi-stage search, quality validation
3. **Neural Core** – Learned image/video codecs, entropy models, continuous learning loop
4. **Hardware & Scale** – Full GPU paths, distributed batch, energy metrics
5. **Production Hardening** – Security, recovery, cloud connectors, GUI polish, extensive benchmarks

## Contributing

We welcome contributions in compression research, neural codecs, systems engineering, and UI/UX. Please see `docs/CONTRIBUTING.md` (coming soon) and open issues/PRs.

## License

Apache-2.0 (or as specified in LICENSE)

## Acknowledgments

Built on the shoulders of giants: zstd, Brotli, LZMA, FFmpeg, libwebp, libavif, PyTorch, ONNX Runtime, and the broader compression & ML research community.

---

**CD Optimizer** – Compress closer to the mathematical limit.
