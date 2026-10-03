"""Replace only the autonomous shot driver, preserving unrelated edits."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'local_simulator/examples/train_policy_tree_selfplay.py'
s=p.read_text(encoding='utf8')
start=s.index('    def _run_without_target(',s.index('class StrictCurlingEnd:'))
end=s.index('\n\ndef closest_enemy_shot',start)
s=s[:start]+'''    def _run_without_target(
        self, active_index: int, shot: Sequence[float],
        noises: Optional[Sequence[float]], *, friction_seed: Optional[int] = None,
    ) -> dict[str, Any]:
        """Compatibility entry, using the same scheduled driver as play()."""
        from local_simulator.unity_prediction import UnityPredictionClock, UnityPredictionDriver

        self.scene.start_bestshot(active_index, shot, yaw=0.0)
        driver = UnityPredictionDriver(
            self.scene, active_index, seed=0 if friction_seed is None else friction_seed,
            noises=noises, motion_stepper=self.motion_stepper,
            clock=UnityPredictionClock(fixed_dt=self.scene.dt,
                                      time_scale=self.prediction_time_scale),
        )
        return driver.run(frame_elapsed=self.prediction_frame_elapsed)

    def play(self, shot: Sequence[float]) -> dict[str, Any]:
        if self.shot_number >= STONE_COUNT:
            raise RuntimeError("本局 16 手已结束")
        # Per-shot seed is the local prediction policy; Unity's unknown global
        # RNG state is not inferred from an endpoint. Only eligible FixedUpdate
        # calls advance this generator, with Update between clock batches.
        replay = self._run_without_target(
            self.shot_number, shot, None,
            friction_seed=self.seed + self.shot_number * 7919,
        )
        if not replay['settled']:
            raise RuntimeError('Unity controller did not finish within the prediction step budget')
        cleared = self.scene.clear_out_of_play_stones()
        self.shot_number += 1
        return {**replay, 'cleared': cleared, 'states': self.states()}
''' + s[end:]
s=s.replace('def __init__(self, *, seed: int, training_fast: bool = True) -> None:',
'''def __init__(self, *, seed: int, training_fast: bool = True,
                 prediction_frame_elapsed: float = 0.33,
                 prediction_time_scale: float = 96.) -> None:''',1)
s=s.replace('        self.shot_number = 0\n        # This only skips',
'''        self.shot_number = 0
        self.prediction_frame_elapsed = float(prediction_frame_elapsed)
        self.prediction_time_scale = float(prediction_time_scale)
        # This only skips''',1)
p.write_text(s,encoding='utf8')
