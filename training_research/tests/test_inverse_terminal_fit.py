import copy
import unittest
from unittest.mock import patch
import numpy as np

from training_research.inverse_contact_atlas import atlas_initials
from training_research.inverse_goal_search import clip, loss
from training_research.inverse_terminal_refine import fit, residual
from training_research.inverse_dataset.selection import failure_reason


class TerminalFitTests(unittest.TestCase):
    def test_coupled_fit_reaches_actual_goal_within_trial_allowance(self):
        selection={"goal":{"stones":{"0":{"type":"IN_REGION","x":2.2,"y":4.8,"radius":.04},
                                      "5":{"type":"IN_REGION","x":2.375,"y":4.88,"radius":.04}}}}
        calls=[]
        def trial(shot,phase):
            shot=clip(shot);v,h,w=shot;dv=v-3.
            states=[{"index":i,"enabled":i in (0,5),"x":0.,"y":0.} for i in range(16)]
            states[0].update(x=2.2+dv+.6*h+.1*w,y=4.8+3*h+.3*w)
            states[5].update(x=2.375+.2*dv-h+.15*w,y=4.88+dv-.5*w)
            record={"status":"complete","physical_final":states,"prediction":{"settled":True,"contact":False},
                    "collision_events":[],"rule_violations":[]}
            record["task_failure"]=failure_reason(record,selection)
            calls.append(record)
            return {"shot":shot,"loss":loss(record,selection),"record":record,"success":record["task_failure"] is None,"phase":phase}
        start=trial((3.2,.04,.8),"initial");calls.clear()
        current,success=fit(start,trial,selection,allowance=24)
        self.assertTrue(success)
        self.assertIsNone(failure_reason(success["record"],selection))
        self.assertLessEqual(len(calls),24)
        from training_research.micro_terminal_refine import fit as micro_fit
        start=trial((3.05,.01,.2),"initial");calls.clear()
        current,success=micro_fit(start,trial,selection,allowance=24)
        self.assertTrue(success)
        self.assertIsNone(failure_reason(success["record"],selection))
        self.assertLessEqual(len(calls),24)

    def test_required_collision_is_still_penalised_when_positions_are_met(self):
        states=[{"index":i,"enabled":True,"x":2.375,"y":4.88} for i in range(16)]
        record={"status":"complete","physical_final":states,"prediction":{"settled":True,"contact":True,"firstContactTargets":[0]},"collision_events":[],"rule_violations":[]}
        selection={"goal":{"stones":{"5":{"type":"IN_REGION","x":2.375,"y":4.88,"radius":.15}}},"required_collision_pairs":[[0,2]]}
        self.assertEqual(failure_reason(record,selection),"missing_collision_pair")
        self.assertGreater(float(residual(record,selection)@residual(record,selection)),0.)

    def test_atlas_excludes_current_board_before_nearest_neighbour_selection(self):
        scene={"scene_key":"current","active_index":5,"stones":[{"index":0,"x":2.2,"y":4.8}],
            "selection":{"first_contact_any":[0],"goal":{"stones":{
                "0":{"type":"IN_REGION","x":2.2,"y":4.8,"radius":.15},
                "5":{"type":"IN_REGION","x":2.2,"y":4.8,"radius":.15}}}}}
        atlas={"scene_key":np.array(["current","different"]),"record_id":np.array(["excluded-answer","other-board"]),
            "shot":np.array([[3.,0.,0.],[3.,.1,0.]]),"first_y":np.array([4.8,4.8]),
            "target_live":np.ones(2,dtype=bool),"active_live":np.ones(2,dtype=bool),"target_house":np.ones(2,dtype=bool),
            "target_delta":np.array([[0.,0.],[.1,.1]]),"active_delta":np.zeros((2,2)),
            "nearby":np.full((2,6),5.),"stones":np.ones(2),"launch_relative_x":np.array([-2.2,-2.1])}
        before=copy.deepcopy(scene)
        with patch("training_research.inverse_contact_atlas.load_atlas",return_value=atlas), \
             patch("training_research.inverse_initials.path_array",return_value=np.zeros((2,4))), \
             patch("training_research.inverse_initials.interpolate",return_value=(np.array([2.375,4.8,0.,-1.]),1)):
            shots,sources=atlas_initials(scene,lambda:0.,1.,clip)
        self.assertEqual(shots,[(3.,.1,0.)])
        self.assertEqual([s["record_id"] for s in sources],["other-board"])
        self.assertEqual(scene,before)



if __name__=="__main__":unittest.main()
