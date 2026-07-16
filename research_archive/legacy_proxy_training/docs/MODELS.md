# Model files

## Current local default

- `search_distill_tactic_policy_first.pt`
  - First-player model.
  - Copied from the original `search_distill_tactic_policy.pt`.
  - The original training loop only sampled first-player turns, so this is a
    first-player model even though its checkpoint metadata predates the
    explicit `player` field.

- `search_distill_tactic_policy_second.pt`
  - Second-player model.
  - Trained with `train_search_distill.py --player second`.
  - Checkpoint metadata includes `player=second`.

The robot loads both files by default and chooses by current side:

```powershell
D:\anaconda3\python.exe search_distill_robot.py --key <connect-key> -H <host> -p <port> --shot-search local --search-top-k 3 --search-candidates 24 --search-rollouts 2 --late-search-top-k 4 --late-search-candidates 32 --late-search-rollouts 3 --hammer-search-candidates 48 --hammer-search-rollouts 4
```

`search_distill_tactic_policy.pt` is kept as a backward-compatible alias for
the original first-player model.
