"""Use the existing capture orchestrator with bounded streaming event batches."""
import capture_12011_first_solver as capture
capture.STREAM_MODE=True
capture.main()
