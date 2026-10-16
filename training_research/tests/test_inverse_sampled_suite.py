import copy
import unittest
from unittest.mock import patch
import numpy as np

from training_research.build_inverse_sampled_suite import observed_task
from training_research.inverse_dataset.sampling import validate_scene
from training_research.inverse_dataset.selection import failure_reason
from training_research.inverse_goal_search import solve,proposals


class SampledSuiteTests(unittest.TestCase):
    def setUp(self):
        self.scene=validate_scene({"active_index":5,"stones":[{"index":0,"x":2.2,"y":4.8},{"index":2,"x":2.5,"y":4.8}]})
        self.record={"status":"complete","rule_violations":[],"requested_scene":self.scene,"active_index":5,
            "before":[{"index":i,"enabled":i in (0,2),"x":2.2 if i==0 else 2.5,"y":4.8} for i in range(16)],
            "physical_final":[{"index":i,"enabled":i==5,"x":2.375,"y":4.88} for i in range(16)],
            "prediction":{"settled":True,"contact":True,"firstContactTargets":[0]},"collision_events":[{"stones":[0,2]}]}

    def test_one_observation_is_enough_and_terminal_is_from_actual_result(self):
        task,priority=observed_task(self.record)
        self.assertEqual(task["tactic"],"double_hit")
        self.assertEqual(priority,0)
        self.assertIsNone(failure_reason(self.record,task))
        self.assertEqual(task["goal"]["stones"]["5"]["x"],2.375)
        self.assertEqual(task["goal"]["stones"]["5"]["radius"],.15)

    def test_non_double_and_illegal_results_are_not_promoted_to_double(self):
        r=copy.deepcopy(self.record); r["collision_events"]=[]
        self.assertNotEqual(observed_task(r)[0]["tactic"],"double_hit")
        r["rule_violations"]=["protected_guard"]
        self.assertIsNone(observed_task(r))

    def test_general_solver_acceptance_and_call_cap(self):
        selection={"tactic":"achieved_goal","goal":{"stones":{"5":{"type":"IN_REGION","x":2.375,"y":4.88,"radius":.15}}}}
        record={**self.record,"task_failure":None}
        for required,cap,success in ((1,1,True),(3,2,False),(3,3,True)):
            seen=[]
            with patch("training_research.inverse_goal_search.proposals",return_value=[(0.,(3.,0.,0.),("draw",0))]):
                result,diag=solve({"selection":selection},evaluate=lambda shot,seed,phase:seen.append(seed) or record,
                    elapsed=lambda:0.,budget_seconds=10.,max_calls=cap,required_seed_successes=required)
            self.assertEqual("bestshot" in result[0],success)
            self.assertLessEqual(len(seen),cap)

    def test_shooter_removal_without_any_contact_anchor_gets_proposals(self):
        scene=copy.deepcopy(self.scene)
        scene["selection"]={"tactic":"achieved_goal","goal":{"stones":{
            "0":{"type":"IN_REGION","x":2.2,"y":4.8,"radius":.15},
            "2":{"type":"IN_REGION","x":2.5,"y":4.8,"radius":.15},
            "5":{"type":"OUT_OF_PLAY"}}}}
        generated=proposals(scene,lambda:0.,10.)
        self.assertTrue(generated)
        self.assertTrue(all(.2<=s[0]<=6. and abs(s[1])<=2.23 and abs(s[2])<=15.7 for _,s,_ in generated))

    def test_no_contact_goal_with_background_removal_uses_placement_initials(self):
        scene=copy.deepcopy(self.scene)
        scene["selection"]={"tactic":"default_draw","require_no_contact":True,"goal":{"stones":{
            "0":{"type":"OUT_OF_PLAY"},"2":{"type":"OUT_OF_PLAY"},
            "5":{"type":"IN_REGION","x":2.375,"y":4.88,"radius":.15}}}}
        def path(v,w):
            return np.array([[2.375,15.,0.,-v],[2.375,20.-5*v,0.,0.]])
        with patch("training_research.inverse_goal_search.path_array",side_effect=path), \
             patch("training_research.inverse_goal_search.clearance",return_value=10.):
            generated=proposals(scene,lambda:0.,10.)
        self.assertTrue(generated)
        self.assertTrue(all(family[0]=="draw" for _,_,family in generated))


if __name__=="__main__": unittest.main()
