"""Budget and certification checks for the new inverse search entry."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from training_research.inverse_dataset.selection import failure_reason
from training_research.inverse_initials import solve,BudgetedDoubleSolver


class InitialSearchTests(unittest.TestCase):
    def setUp(self):
        self.selection = {"tactic":"double_hit","goal":{"stones":{"0":{"type":"OUT_OF_PLAY"},"2":{"type":"OUT_OF_PLAY"}}},
                          "first_contact_any":[0,2],"require_single_first_contact":True,"required_collision_pairs":[[0,2]]}
        self.scene = {"selection":self.selection}
        self.proposal = {"shot":[6.,.1,0.],"source":"test","family":(0,"straight")}

    def record(self, *, pair=True):
        record = {"status":"complete","rule_violations":[],"physical_final":[{"index":i,"enabled":False,"x":0.,"y":0.} for i in range(16)],
                  "prediction":{"settled":True,"firstContactTargets":[0]},"collision_events":[{"stones":[0,2]}] if pair else []}
        record["task_failure"] = failure_reason(record,self.selection)
        return record

    def run_search(self, evaluate, **options):
        with patch("training_research.inverse_initials.quick_initials",return_value=[self.proposal]), \
             patch("training_research.inverse_initials.geometric_initials",return_value=([],0)):
            return solve(self.scene,evaluate=evaluate,elapsed=options.pop("elapsed",lambda:0.),
                         budget_seconds=options.pop("budget_seconds",5.),**options)

    def test_accepts_only_complete_three_seed_certificate(self):
        seen=[]
        attempts, diagnostics=self.run_search(lambda shot,seed,phase: seen.append(seed) or self.record())
        self.assertEqual(seen,[0,1,2])
        self.assertIn("bestshot",attempts[0])
        self.assertTrue(diagnostics["initial_three_seed_success"])

    def test_single_seed_success_does_not_claim_three_seed_robustness(self):
        seen=[]
        attempts,diagnostics=self.run_search(lambda shot,seed,phase:seen.append(seed) or self.record(),required_seed_successes=1)
        self.assertEqual(seen,[0])
        self.assertIn("bestshot",attempts[0])
        self.assertTrue(diagnostics["initial_success"])
        self.assertFalse(diagnostics["initial_three_seed_success"])

    def test_public_entry_defaults_to_one_seed_and_allows_explicit_three(self):
        scene={"scene_id":"test","active_index":5,"stones":[{"index":0,"x":2.2,"y":4.8},{"index":2,"x":2.55,"y":4.8}],
               "selection":self.selection}
        calls=[]
        record=self.record()
        env=SimpleNamespace(scene=SimpleNamespace(_dataset_collision_events=record["collision_events"]))
        def play(shot):
            calls.append(shot)
            return {**record["prediction"],"states":record["physical_final"]}
        env.play=play
        solver=BudgetedDoubleSolver(environment=env)
        with patch("training_research.inverse_dataset.cli.reset_environment",return_value=record["physical_final"]), \
             patch("training_research.inverse_initials.quick_initials",return_value=[self.proposal]):
            result=solver.solve(scene)
            self.assertTrue(result["success"])
            self.assertEqual(len(calls),1)
            self.assertEqual(result["required_seed_successes"],1)
            calls.clear()
            result=solver.solve(scene,required_seed_successes=3)
            self.assertEqual(len(calls),3)
            self.assertTrue(result["diagnostics"]["initial_three_seed_success"])

    def test_partial_certificate_at_call_budget_is_not_a_solution(self):
        seen=[]
        attempts,diagnostics=self.run_search(lambda shot,seed,phase: seen.append(seed) or self.record(),max_calls=2)
        self.assertEqual(seen,[0,1])
        self.assertNotIn("bestshot",attempts[0])
        self.assertEqual(diagnostics["search_physics_calls"],2)

    def test_terminal_goal_without_target_collision_is_rejected(self):
        attempts,diagnostics=self.run_search(lambda *args:self.record(pair=False),max_calls=3)
        self.assertNotIn("bestshot",attempts[0])
        self.assertEqual(diagnostics["search_physics_calls"],3)

    def test_expired_deadline_does_not_start_simulation(self):
        seen=[]
        attempts,diagnostics=self.run_search(lambda *args:seen.append(args) or self.record(),elapsed=lambda:5.)
        self.assertEqual(seen,[])
        self.assertNotIn("bestshot",attempts[0])
        self.assertEqual(diagnostics["search_physics_calls"],0)

    def test_ten_second_deadline_during_verification_rejects_partial_solution(self):
        elapsed=[8.]
        seen=[]
        def evaluate(shot,seed,phase):
            seen.append(seed)
            elapsed[0]=10.01
            return self.record()
        attempts,diagnostics=self.run_search(evaluate,budget_seconds=10.,elapsed=lambda:elapsed[0])
        self.assertEqual(seen,[0])
        self.assertNotIn("bestshot",attempts[0])
        self.assertEqual(diagnostics["search_physics_calls"],1)

    def test_invalid_search_limits_fail_before_simulation(self):
        for name in ("max_calls","conservative_rounds","local_rounds"):
            for value in (0,-1,1.5,True):
                with self.subTest(name=name,value=value),self.assertRaises(ValueError):
                    self.run_search(lambda *args:self.fail("unexpected simulation"),**{name:value})

    def test_distinct_speeds_in_one_family_keep_both_search_entrances(self):
        proposals=[{"shot":[v,0.,9.],"source":"contact_geometry","proxy_valid":True,"family":(0,0,9)} for v in (5.3,5.)]
        def evaluate(shot,*args):
            record=self.record()
            if not (shot[0]<5.05 and shot[1]>.05):
                record["physical_final"][0].update(enabled=True,x=2.375,y=4.88)
            record["task_failure"]=failure_reason(record,self.selection)
            return record
        for profile in ("baseline","fast_poll"):
            with self.subTest(profile=profile), \
                 patch("training_research.inverse_initials.quick_initials",return_value=[]), \
                 patch("training_research.inverse_initials.geometric_initials",return_value=(proposals,2)):
                attempts,diagnostics=solve(self.scene,evaluate=evaluate,elapsed=lambda:0.,budget_seconds=5.,refinement_profile=profile)
            self.assertLess(attempts[0]["bestshot"][0],5.05)
            self.assertTrue(diagnostics["refinement_three_seed_success"])

    def test_fast_poll_reserves_calls_for_additional_geometry(self):
        proposals=[{"shot":[5.,h,0.],"source":"contact_geometry","proxy_valid":True,"family":(0,0,0)} for h in (0.,.2)]
        proposals.append({"shot":[5.,-.2,9.],"source":"contact_geometry","proxy_valid":False,"family":(0,1,9)})
        seen=[]
        def evaluate(shot,seed,phase):
            seen.append((tuple(shot),seed,phase))
            return self.record(pair=shot[1]<-.15 and shot[2]==9.)
        with patch("training_research.inverse_initials.quick_initials",return_value=[]), \
             patch("training_research.inverse_initials.geometric_initials",return_value=(proposals,3)):
            attempts,diagnostics=solve(self.scene,evaluate=evaluate,elapsed=lambda:0.,budget_seconds=10.,refinement_profile="fast_poll")
        self.assertEqual(attempts[0]["bestshot"],[5.,-.2,9.])
        index=next(i for i,item in enumerate(seen) if item[0]==(5.,-.2,9.))
        self.assertLessEqual(index,diagnostics["conservative_call_limit"])

    def test_axis_initial_polish_still_requires_three_seed_certificate(self):
        proposals=[{"shot":[5.3,0.,5.],"source":"contact_geometry","proxy_valid":True,"family":(0,0,5)}]
        seen=[]
        def evaluate(shot,seed,phase):
            seen.append((tuple(shot),seed,phase))
            record=self.record()
            if not (abs(shot[0]-5.18)<1e-6 and shot[1]==0.):
                record["physical_final"][0].update(enabled=True,x=2.375,y=4.88)
            record["task_failure"]=failure_reason(record,self.selection)
            return record
        with patch("training_research.inverse_initials.quick_initials",return_value=[]), \
             patch("training_research.inverse_initials.geometric_initials",return_value=(proposals,1)):
            attempts,diagnostics=solve(self.scene,evaluate=evaluate,elapsed=lambda:0.,budget_seconds=10.,initial_polish=True)
        self.assertEqual(attempts[0]["bestshot"],[5.18,0.,5.])
        self.assertEqual([r[1] for r in seen[-3:]],[0,1,2])
        self.assertTrue(all(r[2]=="initial_polish" for r in seen[-3:]))
        self.assertTrue(diagnostics["refinement_three_seed_success"])


if __name__=="__main__":
    unittest.main()
