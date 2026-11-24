"""Compatibility entry point for the canonical course-welcome renderer."""
from pathlib import Path
import runpy
import sys

if __name__ == '__main__':
    source = Path(__file__).resolve().parents[1] / 'amc-introduction'
    sys.path.insert(0, str(source))
    runpy.run_path(str(source / 'render.py'), run_name='__main__')
