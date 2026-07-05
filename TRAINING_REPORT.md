# Search-Distilled Curling Tactic Model Report

## Result

Trained model:

- `model/search_distill_tactic_policy.pt`
- `model/search_distill_tactic_policy_first.pt`
- `model/search_distill_tactic_policy_second.pt`

Evaluation report:

- `log/search_distill_eval.json`
- `log/search_distill_eval_refined.json`
- `log/search_distill_eval_fixed_sideaware.json`
- `log/search_distill_eval_adaptive_sideaware.json`
- `log/search_distill_eval_adaptive_ranked_candidates.json`
- `log/search_distill_eval_dual_models_80.json`
- `STRATEGY_MODE_ANALYSIS.md` with detailed first-player/second-player,
  phase, score-bucket, and sweep-pattern analysis.

Local fast-simulator evaluation, held-out random seeds:

| Policy | Games | Avg score | Win rate | Loss rate |
| --- | ---: | ---: | ---: | ---: |
| Random valid tactic | 2000 | -0.3215 | 45.80% | 54.20% |
| Scripted tactic priority | 2000 | -1.5355 | 34.00% | 66.00% |
| Search-distilled model | 2000 | 1.3720 | 79.35% | 20.65% |
| 4-rollout search oracle | 100 | 1.3100 | 81.00% | 19.00% |

The trained model is close to the shallow search oracle while being much cheaper
to run at match time.

## Current Strongest Local Version

After the paper review, the robot was upgraded from pure tactic selection to
small-budget continuous shot refinement. The newest version uses separate
first-player and second-player models, side-aware search, and adaptive late-shot
budgets:

- The first-player model chooses likely tactics when we are first player.
- The second-player model chooses likely tactics when we are second player.
- Local root search refines `(v0, h0, w0, sweep_distance)`.
- Search now evaluates from the correct first-player/second-player perspective.
- A scripted fallback candidate is always included with the model top-k tactics.
- Candidate truncation now keeps the base shot and closest local perturbations
  before spending remaining slots on exploration. This fixes the earlier issue
  where arbitrary loop order could drop the original tactic shot.
- The last two own shots use a larger `late` search budget.
- If we are second player, the final own shot uses a larger `hammer` budget.
- Search respects no-sweep tactics such as `guard_*`, `occupy`, `take_out`,
  `hit_roll`, `clear`, and `defense`.
- The socket robot sends the chosen `BESTSHOT` first, then sends the planned
  `SWEEP` distance after `MOTIONINFO`.

Current strongest local command:

```powershell
D:\anaconda3\python.exe search_distill_robot.py --key <connect-key> -H <host> -p <port> --first-model-file model/search_distill_tactic_policy_first.pt --second-model-file model/search_distill_tactic_policy_second.pt --shot-search local --search-top-k 3 --search-candidates 24 --search-rollouts 2 --late-search-top-k 4 --late-search-candidates 32 --late-search-rollouts 3 --hammer-search-candidates 48 --hammer-search-rollouts 4
```

Use this conservative fallback if the official server time budget is tight:

```powershell
D:\anaconda3\python.exe search_distill_robot.py --key <connect-key> -H <host> -p <port> --first-model-file model/search_distill_tactic_policy_first.pt --second-model-file model/search_distill_tactic_policy_second.pt --shot-search local --fixed-search --search-top-k 3 --search-candidates 16 --search-rollouts 1
```

Medium local evaluation with continuous refinement:

| Policy | Games | Avg score | Win rate | Loss rate |
| --- | ---: | ---: | ---: | ---: |
| Random valid tactic | 300 | -0.4567 | 42.67% | 57.33% |
| Scripted tactic priority | 300 | -1.4867 | 34.67% | 65.33% |
| Search-distilled model | 300 | 1.2667 | 79.00% | 21.00% |
| 4-rollout search oracle | 50 | 1.2800 | 76.00% | 24.00% |
| Model + continuous refinement | 80 | 2.0375 | 80.00% | 20.00% |

The refined version is the strongest current local candidate. Its sweep rate in
this evaluation was `48.13%`.

Side-aware evaluation after the latest upgrade:

| Policy | Games | Avg score | Win rate | Loss rate |
| --- | ---: | ---: | ---: | ---: |
| Model + fixed continuous refinement, first player | 80 | 1.9750 | 81.25% | 18.75% |
| Model + fixed continuous refinement, second player | 80 | 2.8250 | 90.00% | 10.00% |
| Model + adaptive continuous refinement, first player | 80 | 2.5125 | 92.50% | 7.50% |
| Model + adaptive continuous refinement, second player | 80 | 3.8625 | 98.75% | 1.25% |

The adaptive result is still local-simulator evidence, but it is the strongest
current configuration and now covers both first-player and second-player
perspectives.

Candidate-ranking evaluation after fixing local candidate truncation:

| Policy | Games | Avg score | Win rate | Loss rate |
| --- | ---: | ---: | ---: | ---: |
| Adaptive refinement with loop-order truncation, first player | 80 | 2.5125 | 92.50% | 7.50% |
| Adaptive refinement with loop-order truncation, second player | 80 | 3.8625 | 98.75% | 1.25% |
| Adaptive refinement with ranked candidate truncation, first player | 80 | 2.9375 | 93.75% | 6.25% |
| Adaptive refinement with ranked candidate truncation, second player | 80 | 3.5625 | 95.00% | 5.00% |

The ranked-candidate version improves the two-sided average score from `3.1875`
to `3.2500` while guaranteeing the base tactic shot remains in the local search
set. A more exploratory `55%` core-candidate variant was also tested in
`log/search_distill_eval_adaptive_balanced_candidates.json`; it underperformed
and was not kept.

Independent first/second model evaluation:

| Policy | Games | Avg score | Win rate | Loss rate |
| --- | ---: | ---: | ---: | ---: |
| Shared first-player model, first player | 80 | 2.9375 | 93.75% | 6.25% |
| Shared first-player model, second player | 80 | 3.5625 | 95.00% | 5.00% |
| First model + second model, first player | 80 | 2.9375 | 93.75% | 6.25% |
| First model + second model, second player | 80 | 3.7375 | 97.50% | 2.50% |

The independent second-player model improves the two-sided average score from
`3.2500` to `3.3375` in the same local evaluation setup. This confirms the
course and NFSP-paper warning that first-player and second-player positions
should not be treated as one shared policy.

Socket smoke test with adaptive search:

- Logs: `log/adaptive_socket_robot.out.log`, `log/adaptive_socket_server.out.log`
- Ranked-candidate smoke logs: `log/ranked_socket_robot.out.log`,
  `log/ranked_socket_server.out.log`
- Robot/server exit code: `0`
- Robot/server stderr: empty
- Observed `normal` search on early shots and `late` search on the final two
  own shots.

## Why This Strategy

The initial linear Q-learning tactic selector did not improve enough:

- 500 socket-trained episodes
- Total avg score: `+0.052`
- Recent 100 avg score: `-0.01`
- It was slow because every episode launched a socket server process.

The literature points to a better path for digital curling and similar games:

- MCTS/UCT for sequential decisions.
- Kernel-regression or continuous-action search for curling-style shot spaces.
- Search/self-play results distilled into a neural policy/value model.
- Action/state abstraction to make the problem tractable.

Relevant local papers:

- `references/papers/game_ai_strategy/05_kr_uct_continuous_action_curling_ijcai2016.pdf`
- `references/papers/game_ai_strategy/06_deep_rl_continuous_action_simulated_curling_pmlr2018.pdf`
- `references/papers/game_ai_strategy/07_digital_curling_nfsp_springer_open_2021.pdf`
- `references/papers/game_ai_strategy/08_hammer_shots_curling_ijcai2016.pdf`
- `references/papers/game_ai_strategy/01_alphazero_self_play_arxiv_1712.01815.pdf`

## Implemented Training Method

Files added:

- `fast_curling_env.py`
  - In-process version of the local mock server physics.
  - Removes socket/process overhead.

- `train_search_distill.py`
  - Generates expert decisions with root Monte Carlo search.
  - Keeps full tactic-library candidates at the root.
  - Uses cheap rollout actions inside simulations for speed.
  - Distills expert policy/value targets into a PyTorch network.

- `search_distill_robot.py`
  - Socket-compatible robot that loads first-player and second-player models.
  - Supports local continuous shot refinement and planned sweeping.

- `continuous_shot_search.py`
  - Small-budget continuous refinement around tactic candidates.
  - Evaluates local `(v0, h0, w0, sweep_distance)` variants with rollout
    simulations.
  - Supports both first-player and second-player scoring perspectives.
  - Ranks oversized candidate sets by distance from the base shot, preserving
    core local perturbations plus a smaller exploratory tail.

- `evaluate_search_distill.py`
  - Independent evaluation script.
  - Reports refined continuous search metrics and saves replay traces.
  - Reports first-player and second-player refined-search metrics separately.

Training command used:

```powershell
D:\anaconda3\python.exe train_search_distill.py --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 3000 --model-file model/search_distill_tactic_policy.pt --report-file log/search_distill_report.json
```

Second-player model training command used:

```powershell
D:\anaconda3\python.exe train_search_distill.py --player second --games 1500 --rollouts 8 --epochs 30 --batch-size 512 --eval-games 1000 --model-file model/search_distill_tactic_policy_second.pt --report-file log/search_distill_report_second.json
```

The long built-in evaluation was stopped after the model had been saved, then a
separate controlled evaluation was run:

```powershell
D:\anaconda3\python.exe evaluate_search_distill.py --games 2000 --search-games 100 --model-file model/search_distill_tactic_policy.pt --report-file log/search_distill_eval.json
```

## Speed

Previous socket-loop training:

- 500 episodes took roughly 13 minutes.
- Result quality was weak.

Search-distillation data generation:

- 1500 expert games / 12000 own-turn samples generated in about 168 seconds.
- Training 30 epochs completed immediately after.
- Full evaluation took longer because it deliberately ran thousands of games with
  full tactic legality checks.

## Caveat

This result is strong on the local mock physics. The official server is still
the authority for final competition quality. The model is therefore a strong
local candidate, not proof of official-server strength.

The continuous refinement layer depends even more strongly on local physics than
the pure tactic model. When the official server is available, first run shot
calibration and short official smoke tests before trusting the refined search
parameters.
