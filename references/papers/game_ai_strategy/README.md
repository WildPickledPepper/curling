# Game AI Strategy Papers

This folder collects open-access papers for studying training strategies in
rule-based game AI, especially search, self-play, action abstraction, and digital
curling.

## Reading Order

1. `09_mcts_survey_browne2012.pdf`
   - Topic: MCTS fundamentals, UCT, rollout policy, tree policy, variants.
   - Why read: Gives the vocabulary for search-based game AI.
   - Source: https://repository.essex.ac.uk/4117/1/MCTS-Survey.pdf

2. `05_kr_uct_continuous_action_curling_ijcai2016.pdf`
   - Topic: MCTS in continuous action spaces with execution uncertainty.
   - Why read: Directly relevant to curling-like shot selection.
   - Source: https://www.ijcai.org/Proceedings/16/Papers/104.pdf

3. `08_hammer_shots_curling_ijcai2016.pdf`
   - Topic: Curling hammer-shot action selection.
   - Why read: Direct curling decision-making under shot uncertainty.
   - Source: https://www.ijcai.org/Proceedings/16/Papers/086.pdf

4. `06_deep_rl_continuous_action_simulated_curling_pmlr2018.pdf`
   - Topic: Deep RL in continuous action spaces, simulated curling case study.
   - Why read: Shows how continuous-shot RL is handled in a curling environment.
   - Source: https://proceedings.mlr.press/v80/lee18b/lee18b.pdf

5. `07_digital_curling_nfsp_springer_open_2021.pdf`
   - Topic: NFSP model for a digital curling system.
   - Why read: Closest to competition-style digital curling.
   - Source: https://link.springer.com/content/pdf/10.1007/s40747-021-00345-6.pdf

6. `01_alphazero_self_play_arxiv_1712.01815.pdf`
   - Topic: General self-play reinforcement learning with MCTS.
   - Why read: Canonical recipe for combining policy/value nets and search.
   - Source: https://arxiv.org/pdf/1712.01815.pdf

7. `02_alphago_zero_ucl_accepted_nature24270.pdf`
   - Topic: AlphaGo Zero, self-play plus MCTS.
   - Why read: Deeper system-level reference for the AlphaZero family.
   - Source: https://discovery.ucl.ac.uk/id/eprint/10045895/1/agz_unformatted_nature.pdf

8. `03_nfsp_self_play_arxiv_1603.01121.pdf`
   - Topic: Neural Fictitious Self-Play.
   - Why read: Self-play with best-response and average-policy learning.
   - Source: https://arxiv.org/pdf/1603.01121.pdf

9. `04_elastic_mcts_state_abstraction_arxiv_2205.15126.pdf`
   - Topic: MCTS with state abstraction for strategy games.
   - Why read: Supports the idea of reducing raw game states/actions into useful abstractions.
   - Source: https://arxiv.org/pdf/2205.15126.pdf

## Notes For Our Project

- Do not treat the local mock server as final physics.
- Start by learning high-level tactic selection.
- Use MCTS/KR-UCT ideas when we need continuous shot refinement.
- Use self-play and opponent pools only after the baseline tactic bot is stable.
- Evaluate on the official server before trusting any local-training ranking.
