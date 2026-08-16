# Architecture Overview

## Goals

- Approach theoretical entropy limits under quality constraints
- Fully automatic pipeline selection
- Continuous learning from compression outcomes
- Modular, extensible, production-ready
- Cross-platform (Windows, macOS, Linux)
- CLI + REST API + modern GUI

## High-Level Components

1. **Analyzers**  
   Detect file type, compute entropy, redundancy, semantic features, visual/audio statistics.

2. **Pipeline Engine**  
   Composable stages (preprocessing, classical codecs, neural codecs, entropy coding, packaging).

3. **Orchestrator (AI Controller)**  
   Selects candidate pipelines, runs multi-attempt search (Ultra mode), ranks by size/quality/speed, validates results.

4. **Quality Validation**  
   PSNR, SSIM, LPIPS, audio similarity, OCR accuracy, cryptographic checksums.

5. **Security Layer**  
   AES-256-GCM + Argon2id password protection, integrity records.

6. **Interfaces**  
   - CLI (`cli/cd_optimizer.py`)
   - REST API (FastAPI)
   - GUI (Next.js – planned full implementation)
   - Batch / folder / drive processing

## Data Flow

```
Input File
    │
    ▼
Primary Analyzer (+ specialized analyzers)
    │
    ▼
Pipeline Selector (mode + quality + analysis → ranked list)
    │
    ▼
Multi-attempt Execution (Fast: 1, Balanced: 3, Ultra: many)
    │
    ▼
Quality / Integrity Gate
    │
    ▼
Optional Encryption + Container Packaging
    │
    ▼
Output + Stats + Learning Feedback
```

## Extensibility

- New codecs register via `CodecRegistry`
- New analyzers via `AnalyzerRegistry`
- New pipelines via `build_pipelines_for` or dedicated factories
- Neural models live under `models/` and are loaded by stages in `src/neural/`

## Future Extensions

- Full container format with self-describing header
- Learned neural image / video codecs (Torch / ONNX)
- Continuous learning loop storing successful (file features → pipeline) pairs
- Distributed batch workers
- Cloud storage connectors
- GPU acceleration paths for every major stage
