# Unity Calibration Plan

Goal: make FastCurlingEnv match the Unity standalone simulator closely enough
for self-play training and tactical search.

## Current State

- Unity standalone server is running through local_arena.py.
- unity_sampling_supervisor.py is running and will keep trying to attach two samplers.
- unity_ui_watcher.py is running and will click the visible Unity page when the desktop is unlocked and the page is visible.
- Power sleep/hibernate timers were disabled for AC power.

Current background logs:

- log/unity_sampling/supervisor_v2.out.log
- log/unity_sampling/sampler1.out.log
- log/unity_sampling/sampler2.out.log
- log/unity_sampling/ui_watcher.out.log

## Data Layers

### 1. Free Landing

Inputs: v0, h0, w0, sweep.

Target: final resting (x, y) and intermediate MOTIONINFO.

Use only samples with collision_free=true.

Fitting:

- first pass: ridge polynomial regression in tools/calibration/fit_unity_samples.py;
- later pass: compare against paper ODE hybrid model.

### 2. Sweep

Sweep is included as a feature in the Unity landing model.

Feature set:

    1, v, h, w, sweep, |w|, tanh(w), v^2, h^2, w^2, sweep^2,
    v*h, v*w, h*w, v*sweep, h*sweep, w*sweep

This replaces the previous fixed y -= sweep * 0.045 heuristic when
config/unity_physics_calibration.json exists.

### 3. High-Speed Takeout Envelope

The current sampling plan includes fast no-collision shots with:

- v0 = 4.0 .. 6.0
- h0 = -1.2 .. 1.2
- w0 = -1.57, 0, 1.57

These are necessary before trusting takeout trajectory search.

### 4. Collision / Rotation

This is not solved by landing regression. Required next dataset:

- one stationary target stone;
- incoming speed 4.0 .. 6.0;
- impact offset around [-2R, 2R];
- curl rotation w0;
- record shooter final position and target final position;
- repeat for guards/button/top-four positions.

Only after this dataset exists should apply_simple_collision be replaced by a fitted collision model.

## Commands

Fit available Unity JSONL samples:

    D:\anaconda3\python.exe tools\calibration\fit_unity_samples.py data\calibration\unity_v2_samples_Player1.jsonl data\calibration\unity_v2_samples_Player2.jsonl --output config\unity_physics_calibration.json --eval-output config\unity_physics_evaluation.json

Check background sampling:

    Get-Content log\unity_sampling\supervisor_v2.out.log -Tail 40
    Get-Content log\unity_sampling\ui_watcher.out.log -Tail 40
    Get-ChildItem data\calibration\unity*.jsonl
