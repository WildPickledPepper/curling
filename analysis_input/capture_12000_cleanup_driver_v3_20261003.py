"""Capture with a read-only tag-string sample on the collision root only."""
from pathlib import Path
import capture_12011_first_solver as capture
capture.PROBE=Path(__file__).resolve().parent/'case12000_cleanup_observer_v3_20261003.js'
capture.STREAM_MODE=True
capture.main()
