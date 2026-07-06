# Official Physics Sampling

Use this workflow to collect official-server throw data before calibrating the
local simulator. The goal is not to win; it is to record controlled
`BESTSHOT -> MOTIONINFO -> POSITION` samples.

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
