"""Unit tests for entropy and basic analysis."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.analyzers.primary import PrimaryAnalyzer


def test_shannon_entropy_uniform():
    data = bytes(range(256)) * 10
    ent = PrimaryAnalyzer._shannon_entropy(data)
    assert 7.9 < ent <= 8.0


def test_shannon_entropy_constant():
    data = b"\x00" * 1000
    ent = PrimaryAnalyzer._shannon_entropy(data)
    assert ent == 0.0


def test_duplicate_blocks():
    block = b"A" * 4096
    data = block + block + b"B" * 4096
    dups = PrimaryAnalyzer._estimate_duplicate_blocks(data)
    assert dups >= 1
