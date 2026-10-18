"""Compatibility entry point for the latest user-directed depth correction."""
from pathlib import Path
from runpy import run_path

if __name__ == '__main__':
    run_path(str(Path(__file__).with_name('apply_sit_depth_feedback.py')),run_name='__main__')
