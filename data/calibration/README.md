# Calibration Data

Raw observations collected from the official-compatible curling server.

- `no_sweep_200.jsonl`: 200 free-running shots with middle-state telemetry;
  190 retained final positions and 10 out-of-play censored outcomes.
- `sweep_200.jsonl`: 200 shots covering sweep distances from 0 to 12 metres.

The JSONL files are local training data and are excluded from Git by default.
They are inputs for the fitted configurations under `config/`.
