# Curling AI Workspace

Digital curling course workspace plus a local search-distilled competition
robot.

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

- `TRAINING_REPORT.md`
- `STRATEGY_MODE_ANALYSIS.md`
- `model/MODELS.md`
- `log/search_distill_eval_dual_models_80.json`

## Training

First-player model:

```powershell
D:\anaconda3\python.exe train_search_distill.py --player first --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_first.pt --report-file log/search_distill_report_first.json
```

Second-player model:

```powershell
D:\anaconda3\python.exe train_search_distill.py --player second --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_second.pt --report-file log/search_distill_report_second.json
```

Evaluate the dual-model robot locally:

```powershell
D:\anaconda3\python.exe evaluate_search_distill.py --games 1 --search-games 1 --refined-games 80 --adaptive-refined --first-model-file model/search_distill_tactic_policy_first.pt --second-model-file model/search_distill_tactic_policy_second.pt --refined-top-k 3 --refined-candidates 24 --refined-rollouts 2 --late-refined-top-k 4 --late-refined-candidates 32 --late-refined-rollouts 3 --hammer-refined-candidates 48 --hammer-refined-rollouts 4 --trace-games 3 --report-file log/search_distill_eval_dual_models_80.json
```

Socket smoke tests for the default robot:

```powershell
# Player1 / first-player path
D:\anaconda3\python.exe local_curling_server.py --host 127.0.0.1 --port 7792 --key local-test:0 --rounds 1 --connect-name Player1
D:\anaconda3\python.exe search_distill_robot.py --key local-test:0 -H 127.0.0.1 -p 7792 --shot-search local

# Player2 / second-player path
D:\anaconda3\python.exe local_curling_server.py --host 127.0.0.1 --port 7793 --key local-test:0 --rounds 1 --connect-name Player2
D:\anaconda3\python.exe search_distill_robot.py --key local-test:0 -H 127.0.0.1 -p 7793 --shot-search local
```

The Player2 smoke should show `玩家2，首局后手` and a final-shot
`budget=hammer` line in the robot log.

## Important Caveat

The strongest evidence here is from the local mock physics. The official server
is still authoritative. When it is available, run calibration shots and short
official smoke tests before trusting local search parameters.
