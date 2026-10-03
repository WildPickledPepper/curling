# Stage S U6 Flat Deployment

This archive contains a root-only submission package for the Deep Sets U6
checkpoint. Extract every file into the course-platform root directory, then
run `python main.py`. The package requires only Python, PyTorch and NumPy.

`main.py` loads `latest.pt` and enables both frozen Stage S rules:

- P1 final-shot `peel_guard` defensive guard.
- P2 final-shot blocked-button `around_guard_draw_left` guard.

Override the connection without editing files when needed:

```bash
python main.py -k YOUR_CONNECTKEY -H YOUR_HOST -p 7788 --name zzy_stage_s_u6
```

The same values can be supplied through `CONNECTKEY`, `CURLING_HOST`,
`CURLING_PORT`, `CURLING_AI_NAME`, and `PPO_CHECKPOINT`. Do not replace this
package with the repository's legacy `main.py` or `ppo_robot.py`: they use the
old ActorCritic architecture and cannot load this Deep Sets checkpoint.
