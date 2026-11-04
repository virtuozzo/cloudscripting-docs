#!/usr/bin/env python3
"""Stable entry point for isolated Hugo release artifacts."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.migration.release_build import main

if __name__ == '__main__':
    raise SystemExit(main())
