# Official Physics Sampling

Use this workflow to collect official-server throw data before calibrating the
local simulator. The goal is not to win; it is to record controlled
`BESTSHOT -> MOTIONINFO -> POSITION` samples.

## Recommended Dual-Player Collector

`dual_calibration_collector.py` opens two socket connections from one process,
so the server assigns them to `Player1` and `Player2`. It uses conservative
defaults around the known stable center draw region:

- `v0`: `2.75` to `3.25`
- `h0`: `-0.45` to `0.45`
- `w0`: `-1.5` to `1.5`

For clean no-collision single-stone samples, use debug reset mode. Pass the
plain key; the script automatically appends `:0` when `--use-reset` is enabled.

```bash
python dual_calibration_collector.py \
  --key "$CONNECT_KEY" \
  -H "$HOST" \
  -p "$PORT" \
  --use-reset \
  --output-file "log/server_calibration/dual_calibration_samples.jsonl" \
  --show-msg
```

Short test:

```bash
python dual_calibration_collector.py \
  --key "$CONNECT_KEY" \
  -H "$HOST" \
  -p "$PORT" \
  --use-reset \
  --random-samples 20 \
  --show-msg
```

If stones still go out of play, narrow the range further:

```bash
python dual_calibration_collector.py \
  --key "$CONNECT_KEY" \
  -H "$HOST" \
  -p "$PORT" \
  --use-reset \
  --random-samples 20 \
  --v-min 2.85 --v-max 3.10 \
  --h-min -0.25 --h-max 0.25 \
  --w-min -0.8 --w-max 0.8 \
  --show-msg
```

The old broad random range (`v0` up to `4.5`, `h0` up to `1.0`, `w0` up to
`4.0`) is too aggressive for first-pass official physics calibration and will
often throw stones out of play.

## Server Setup

Use a normal two-player room, preferably with infinite rounds enabled. Do not
append `:1` to the key unless you intentionally want to challenge a boss AI.

Start two sampler processes with the same connect key. The server will assign
the first connection to `Player1` and the second connection to `Player2`.

Terminal 1:

```bash
python official_physics_sampler.py \
  --key "$CONNECT_KEY" \
  -H "$HOST" \
  -p "$PORT" \
  --name SamplerA \
  --output "log/official_physics_samples_{player}.jsonl" \
  --show-msg
```

Terminal 2:

```bash
python official_physics_sampler.py \
  --key "$CONNECT_KEY" \
  -H "$HOST" \
  -p "$PORT" \
  --name SamplerB \
  --output "log/official_physics_samples_{player}.jsonl" \
  --show-msg
```

Expected outputs:

- `log/official_physics_samples_Player1.jsonl`
- `log/official_physics_samples_Player2.jsonl`

On Linux, combine them after the run:

```bash
cat log/official_physics_samples_Player1.jsonl \
    log/official_physics_samples_Player2.jsonl \
  > log/official_physics_samples_combined.jsonl
```

## What The Sampler Does

The default schedule spreads one end across a 4x4 grid:

- 4 velocity levels
- 4 lateral offsets
- one shared rotation/sweep setting per end

Across ends, it changes rotation and sweep. This uses infinite-round mode to
collect many repeated controlled samples while keeping stones separated within
each end.

Each JSONL record includes:

- `before_position`
- `shot`: `v0`, `h0`, `w0`, `sweep`, `label`
- `motioninfo`
- `after_position`
- `final_xy`
- `existing_stone_max_move`
- `collision_free`

For the first calibration pass, filter to:

```text
collision_free == true
```

Those samples are the cleanest approximation of single-stone official physics.

## Useful Short Test

Limit each process to a few own shots:

```bash
python official_physics_sampler.py \
  --key "$CONNECT_KEY" \
  -H "$HOST" \
  -p "$PORT" \
  --max-samples 8 \
  --output "log/official_physics_samples_{player}.jsonl" \
  --show-msg
```

Once that works, remove `--max-samples`.
