#!/usr/bin/env python
"""Fallback runner if packaging/import issues occur.
Usage:
  python run_video_analyzer.py --video path/to/video.mp4 --interval 2
"""
import sys
import os
from pathlib import Path

# Ensure src on sys.path
ROOT = Path(__file__).parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from video_analyzer.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
