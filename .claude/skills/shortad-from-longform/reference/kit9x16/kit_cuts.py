#!/usr/bin/env python3
"""Moved 2026-09-24 (VQC-C): the pose-matched cut is `_shared/cut/piccuts.py`, the only copy, shared by every
video skill. This shim keeps `kit_cuts.py decide|calibrate ...` working; build_kit.py calls the shared tool directly."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "_shared", "cut"))
from piccuts import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
