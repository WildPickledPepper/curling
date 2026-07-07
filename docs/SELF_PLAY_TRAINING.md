# Self-Play Training Notes

## Objective

The current training target is not just higher local score.  A candidate model
must also show explainable tactical behavior:

- first-player and second-player policies remain separate;
- enemy shot rock or enemy button occupancy should trigger offensive options;
- takeout-family actions are measured explicitly;
- candidates are promoted only after symmetric head-to-head evaluation.

## Current Training Loop

`self_play_trainer.py` wraps the existing search-distillation trainer:

1. train a first-player candidate against a mixed opponent pool;
2. train a second-player candidate against the same champion pool;
3. evaluate candidate pair against current champion pair with side swapping;
4. compute score, win rate, and takeout-family offense rate;
5. optionally promote the candidate by copying it onto the champion model paths.

Generated candidates and run logs are ignored by Git:

- `model/self_play/`
- `model/backups/`
- `log/self_play_runs/`

## Smoke Command

This verifies the loop only.  It should not be used to replace the default
models.

```powershell
D:\anaconda3\python.exe self_play_trainer.py --cycles 1 --games 20 --rollouts 1 --epochs 2 --batch-size 128 --eval-games 30 --search-eval-games 10 --head-to-head-games 5 --trace-games 1
```

Latest smoke evidence:

- candidate vs champion symmetric average score: `0.3`;
- candidate win rate: `0.7`;
- candidate takeout-family rate: `0.3375`;
- champion takeout-family rate in the same match: `0.25`;
- no promotion was performed.

The sample is intentionally too small for strength claims, but it proves the
automation works.

## Longer CPU Run

Use this for unattended CPU training:

```powershell
D:\anaconda3\python.exe self_play_trainer.py --cycles 3 --games 250 --rollouts 4 --epochs 10 --batch-size 256 --eval-games 250 --search-eval-games 80 --head-to-head-games 30 --opponent-policy balanced-mix
```

Add `--promote` only when you are comfortable letting the script overwrite:

- `model/search_distill_tactic_policy_first.pt`
- `model/search_distill_tactic_policy_second.pt`

The default promotion gate is:

- symmetric candidate average score >= `0.05`;
- candidate win rate >= `0.50`;
- candidate takeout-family rate >= `0.08`;
- candidate takeout-family rate is not more than `0.02` below champion.

## Offensive Behavior Checks

Fixed tactical probes:

```powershell
D:\anaconda3\python.exe tools/analysis/probe_offense_scenarios.py --rollouts 1 --candidates 16 --report-file log/offense_probe_path_collision.json
```

Latest useful probe:

- first-player `enemy_button`: selected `take_out`;
- explanation: `enemy_shot=0.00m;enemy_button;intent=remove_or_roll`;
- target stone after shot: out of play.

Fast-simulator self-play after path-collision fix:

```powershell
D:\anaconda3\python.exe evaluate_head_to_head.py --blue-policy dual_refined --red-policy dual_refined --games 20 --trace-games 1 --report-file log/head_to_head_dual_self_path_collision_20.json
```

Observed action-family rates:

- first-player/blue takeout-family rate: `0.10625`;
- second-player/red takeout-family rate: `0.35625`.

This is the first clear evidence that the robot is no longer only pushing to
center in the fast simulator.

## Important Implementation Fix

The fast simulator previously detected collisions only near the final landing
point.  High-speed takeout shots often pass through the target and stop beyond
it, so they were incorrectly treated as misses.  `fast_curling_env.py` now
checks high-speed collisions along the shot path.  The regression test is:

```powershell
D:\anaconda3\python.exe -m unittest discover -s tests -p "test_*.py" -v
```
