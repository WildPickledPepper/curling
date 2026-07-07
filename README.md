# Curling AI Workspace

Digital curling course workspace plus a local search-distilled competition
robot.

## Official Standalone Arena

The downloaded standalone server is now the authoritative local physics and
match environment. Start the server, open its Unity UI, and connect both of our
robots with one command:

```powershell
D:\anaconda3\python.exe local_arena.py start --robots --show-msg
```

In the opened page, select the two-player/infinite-round mode and start the
match. Runtime status and shutdown:

```powershell
D:\anaconda3\python.exe local_arena.py status
D:\anaconda3\python.exe local_arena.py stop
```

The standalone binary directory is intentionally excluded from Git. The
in-process `fast_curling_env.py` remains a high-speed training surrogate; it
must be calibrated and evaluated against the standalone arena. The legacy
`archive/legacy/mock_curling_server.py` is only a lightweight socket smoke-test
double.

## Project Layout

- Root: current robot, training, evaluation, search, and fast simulator code.
- `docs/`: reports and strategy notes.
- `tools/calibration/`: official-server sampling and physics fitting tools.
- `tools/eval/` and `tools/analysis/`: older evaluation and analysis utilities.
- `archive/legacy/`: obsolete DQN/mock-server experiments kept for reference.
- `notebooks/` and `images/`: original course notebooks and assets.

## Current Strongest Local Robot

Use separate first-player and second-player models. The side difference is large
enough that the robot should not use one shared policy for both. These
side-specific model files are the default paths in `search_distill_robot.py`.

```powershell
D:\anaconda3\python.exe search_distill_robot.py --key <connect-key> -H <host> -p <port> --shot-search local --search-top-k 3 --search-candidates 24 --search-rollouts 2 --late-search-top-k 4 --late-search-candidates 32 --late-search-rollouts 3 --hammer-search-candidates 48 --hammer-search-rollouts 4
```

Conservative fallback if the official server time budget is tight:

```powershell
D:\anaconda3\python.exe search_distill_robot.py --key <connect-key> -H <host> -p <port> --shot-search local --fixed-search --search-top-k 3 --search-candidates 16 --search-rollouts 1
```

## Evidence

Local fast-simulator refined-search evaluation:

| Configuration | First avg | First win | Second avg | Second win | Mean avg |
| --- | ---: | ---: | ---: | ---: | ---: |
| Shared first-player model for both sides | 2.9375 | 93.75% | 3.5625 | 95.00% | 3.2500 |
| Separate first/second models | 2.9375 | 93.75% | 3.7375 | 97.50% | 3.3375 |

Main reports:

- `docs/CURRENT_MODEL_STRATEGY.md`
- `docs/TRAINING_REPORT.md`
- `docs/SELF_PLAY_TRAINING.md`
- `docs/STRATEGY_MODE_ANALYSIS.md`
- `model/MODELS.md`
- `log/search_distill_eval_dual_models_80.json`
- `log/head_to_head_dual_vs_shared_symmetric_20.json`
- `log/head_to_head_dual_vs_scripted_symmetric_20.json`

## Official Physics Calibration

Before trusting local continuous search on the official server, collect
official-server shot samples and calibrate the local simulator. See
`docs/OFFICIAL_PHYSICS_SAMPLING.md`.

The experimental paper-inspired ODE simulator is kept separate from the
competition default. Keep evaluation and deployment fitting separate:

```powershell
# Honest 151/39 train/validation report
D:\anaconda3\python.exe tools/calibration/fit_paper_physics.py data/calibration/no_sweep_200.jsonl --dt 0.0125 --output config/paper_physics_evaluation.json

# Deployment refit: all 200 middle states and all 190 observable landings
D:\anaconda3\python.exe tools/calibration/fit_paper_physics.py data/calibration/no_sweep_200.jsonl --dt 0.0125 --fit-all --initial-config config/paper_physics_evaluation.json --output config/paper_physics_calibration.json

D:\anaconda3\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

See `docs/CURLING_PHYSICS_MODEL_ANALYSIS.md` for the equations, limitations and
validation comparison. The fitted configuration is
`config/paper_physics_calibration.json`; the held-out evidence remains in
`config/paper_physics_evaluation.json`.

## Training

First-player model:

```powershell
D:\anaconda3\python.exe train_search_distill.py --player first --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_first.pt --report-file log/search_distill_report_first.json
```

Second-player model:

```powershell
D:\anaconda3\python.exe train_search_distill.py --player second --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_second.pt --report-file log/search_distill_report_second.json
```

Opponent-pool training is now available. The default remains `random`, matching
the original local mock opponent. `balanced-mix` keeps half of the original
random-opponent distribution and mixes in model, scripted, and rollout
opponents; this is the safer next experiment than replacing the whole data
distribution with hard opponents:

```powershell
D:\anaconda3\python.exe train_search_distill.py --player first --opponent-policy balanced-mix --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_first_balanced.pt --report-file log/search_distill_report_first_balanced.json
D:\anaconda3\python.exe train_search_distill.py --player second --opponent-policy balanced-mix --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_second_balanced.pt --report-file log/search_distill_report_second_balanced.json
```

`model-mix` is the harder pool: it gives more weight to the opponent side's
available side-specific model plus scripted and rollout opponents. For example,
when training the second-player model, both pools can load
`search_distill_tactic_policy_first.pt` as the first-player opponent.

Evaluate the dual-model robot locally:

```powershell
D:\anaconda3\python.exe tools/eval/evaluate_search_distill.py --games 1 --search-games 1 --refined-games 80 --adaptive-refined --first-model-file model/search_distill_tactic_policy_first.pt --second-model-file model/search_distill_tactic_policy_second.pt --refined-top-k 3 --refined-candidates 24 --refined-rollouts 2 --late-refined-top-k 4 --late-refined-candidates 32 --late-refined-rollouts 3 --hammer-refined-candidates 48 --hammer-refined-rollouts 4 --trace-games 3 --report-file log/search_distill_eval_dual_models_80.json
```

Run symmetric head-to-head checks. These swap sides so hammer advantage does not
dominate the conclusion:

```powershell
D:\anaconda3\python.exe evaluate_head_to_head.py --blue-policy dual_refined --red-policy shared_refined --swap-sides --games 20 --report-file log/head_to_head_dual_vs_shared_symmetric_20.json
D:\anaconda3\python.exe evaluate_head_to_head.py --blue-policy dual_refined --red-policy scripted --swap-sides --games 20 --report-file log/head_to_head_dual_vs_scripted_symmetric_20.json
```

Run iterative self-play candidate training:

```powershell
D:\anaconda3\python.exe self_play_trainer.py --cycles 3 --games 250 --rollouts 4 --epochs 10 --batch-size 256 --eval-games 250 --search-eval-games 80 --head-to-head-games 30 --opponent-policy balanced-mix
```

Use `--promote` only when the promotion gate should overwrite the current
first/second champion models. See `docs/SELF_PLAY_TRAINING.md` for the gate and
offensive-action checks.

Current symmetric low-budget head-to-head results:

| Policy A | Policy B | Games per side assignment | A avg score | A win rate |
| --- | --- | ---: | ---: | ---: |
| dual_refined | shared_refined | 20 | 0.25 | 50.00% |
| dual_refined | scripted | 20 | 7.05 | 97.50% |

Socket smoke tests for the default robot:

```powershell
# Player1 / first-player path
D:\anaconda3\python.exe archive/legacy/mock_curling_server.py --host 127.0.0.1 --port 7792 --key local-test:0 --rounds 1 --connect-name Player1
D:\anaconda3\python.exe search_distill_robot.py --key local-test:0 -H 127.0.0.1 -p 7792 --shot-search local

# Player2 / second-player path
D:\anaconda3\python.exe archive/legacy/mock_curling_server.py --host 127.0.0.1 --port 7793 --key local-test:0 --rounds 1 --connect-name Player2
D:\anaconda3\python.exe search_distill_robot.py --key local-test:0 -H 127.0.0.1 -p 7793 --shot-search local
```

The Player2 smoke should show `玩家2，首局后手` and a final-shot
`budget=hammer` line in the robot log.

## Important Caveat

The strongest evidence here is from the local mock physics. The official server
is still authoritative. When it is available, run calibration shots and short
official smoke tests before trusting local search parameters.
