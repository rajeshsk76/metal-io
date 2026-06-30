#!/usr/bin/env python3
"""Entry point for the metal.io project."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from metal_io.cli import main

if __name__ == "__main__":
    raise SystemExit(main())