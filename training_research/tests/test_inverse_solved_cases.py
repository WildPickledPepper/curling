"""Observed solution mining must not fabricate a double or seed certificate."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from training_research.build_inverse_solved_cases import main, observed_pairs
from training_research.inverse_dataset.sampling import validate_scene


class SolvedCaseTests(unittest.TestCase):
    def setUp(self):
        self.scene=validate_scene({"scene_id":"test-double","family":"double_hit","active_index":5,
            "stones":[{"index":0,"x":2.2,"y":4.88},{"index":2,"x":2.55,"y":4.88}]})
        self.record={"scene_key":self.scene["scene_key"],"requested_scene":self.scene,"shot":[6.,0.,0.],
            "active_index":5,"physics_seed":1,"record_id":"test:0","status":"complete","rule_violations":[],
            "before":[{"index":i,"enabled":i in (0,2),"x":2.2 if i==0 else 2.55,"y":4.88} for i in range(16)],
            "physical_final":[{"index":i,"enabled":False,"x":0.,"y":0.} for i in range(16)],
            "prediction":{"settled":True,"firstContactTargets":[0]},"collision_events":[{"stones":[0,2]}]}

    def test_double_requires_actual_pair_and_target_first_contact(self):
        self.assertEqual(observed_pairs(self.record),[(0,2)])
        missing=copy.deepcopy(self.record); missing["collision_events"]=[]
        self.assertEqual(observed_pairs(missing),[])
        wrong=copy.deepcopy(self.record); wrong["prediction"]["firstContactTargets"]=[4]
        self.assertEqual(observed_pairs(wrong),[])

    def test_duplicate_seeds_do_not_create_known_solution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            for name,seeds in (("unique",(1,2,3)),("duplicates",(1,1,1))):
                runs=root/name; shard=runs/"inverse_manual_boards_20261004"/"shards"; shard.mkdir(parents=True)
                rows=[{**self.record,"physics_seed":seed,"record_id":"test:"+str(i)} for i,seed in enumerate(seeds)]
                (shard/"000000.raw.jsonl").write_text("\n".join(json.dumps(r) for r in rows)+"\n",encoding="utf-8")
                output=runs/"catalog"
                main(["--runs",str(runs),"--output",str(output),"--min-observed-seeds","3"])
                scenes=json.loads((output/"scenes.json").read_text(encoding="utf-8"))
                self.assertEqual(len(scenes),1 if name=="unique" else 0)
                self.assertTrue(all("candidate_shots" not in s and "references" not in s for s in scenes))

    def test_search_certificates_require_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            search=root/"inverse_search"; search.mkdir()
            selection={"tactic":"double_hit","first_contact_any":[0,2],"require_single_first_contact":True,
                "required_collision_pairs":[[0,2]],"goal":{"stones":{
                    "0":{"type":"OUT_OF_HOUSE","required":True},
                    "2":{"type":"OUT_OF_HOUSE","required":True}}}}
            evidence=search/"evidence.json"
            evidence.write_text(json.dumps({"scene":self.scene,"goal":selection,"rows":[{
                "first_three_seed_success_shot":self.record["shot"],
                "calls":[{**self.record,"physics_seed":seed} for seed in (1,2,3)]}]}),encoding="utf-8")
            (search/"report.json").write_text(json.dumps({"rows":[{"success":True,"evidence":str(evidence)}]}),encoding="utf-8")
            for include in (False,True):
                output=root/("mixed" if include else "forward_only")
                argv=["--runs",str(root),"--output",str(output)]
                main(argv+(["--include-search-certificates"] if include else []))
                manifest=json.loads((output/"manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["cases"],int(include))
                self.assertEqual(manifest["include_search_certificates"],include)


if __name__=="__main__":
    unittest.main()
