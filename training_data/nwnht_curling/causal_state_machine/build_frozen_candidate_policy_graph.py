#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Freeze refutation-screened edges with opponent-reply diagnostics for OPE."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--gate',type=Path,default=root/'nwnht_first_player_placebo_refutation_gate_v0.json');p.add_argument('--abstraction',type=Path,default=root/'nwnht_first_player_causal_state_abstraction_v1.json');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_frozen_candidate_policy_graph_v1.json');args=p.parse_args()
 if args.output.exists():raise SystemExit(f'Refusing to overwrite {args.output}')
 gate=json.loads(args.gate.read_text(encoding='utf-8')); abstraction=json.loads(args.abstraction.read_text(encoding='utf-8'))
 lookup={(x['from_state'],x['observed_own_effect']):x for x in abstraction['state_action_diagnostics']}
 grouped={}
 for candidate in gate.get('survivors', gate.get('candidates', [])):
  evidence=lookup.get((candidate['state_id'],candidate['better_candidate']))
  if evidence is None: raise ValueError(f"Missing state-action diagnostic: {candidate['state_id']} / {candidate['better_candidate']}")
  grouped.setdefault(candidate['state_id'],[]).append({'state_id':candidate['state_id'],'recommended_observed_effect_proxy':candidate['better_candidate'],'comparison_effect':candidate['comparison_action'],'evidence':{k:candidate[k] for k in ('raw_support_better_candidate','raw_support_comparison','dr_advantage_end_margin','cluster_bootstrap_lcb','cluster_bootstrap_ucb','unobserved_differential_bias_to_zero_end_margin','heterogeneity_issues')},'own_post_shot_topology_distribution':evidence['own_post_shot_topology_distribution'],'opponent_reply_distribution':evidence['opponent_reply_distribution'],'next_state_distribution':evidence['next_state_distribution']})
 nodes=[]
 for state, candidates in sorted(grouped.items()):
  if len(candidates)==1:
   nodes.append({**candidates[0],'fallback':'SEARCH_REQUIRED','status':'FROZEN_FOR_OPE_ONLY'})
  else:
   nodes.append({'state_id':state,'candidate_effects':candidates,'fallback':'SEARCH_REQUIRED','status':'AMBIGUOUS_CANDIDATE_SET_NO_RECOMMENDATION','reason':'Each candidate only beat its own comparator; no pairwise supported advantage selects between candidates.'})
 out={'schema':'nwnht_first_player_frozen_candidate_policy_graph_v1','purpose':'Fixed candidate graph for predeployment OPE. It is not a deployable policy and contains no target region or PhysX command.','runtime_contract':'Only an exact state_id with exactly one unambiguous candidate may expose its effect; every other state and every failed physical/rule check must return SEARCH_REQUIRED.','state_node_count':len(nodes),'unambiguous_effect_node_count':sum(x['status']=='FROZEN_FOR_OPE_ONLY' for x in nodes),'nodes':nodes,'prohibitions':['Do not replace effect proxy with a called-shot label.','Do not execute without local-rule and strict PhysX reachability checks.','Do not treat opponent-reply frequencies as worst-case guarantees.'],'required_before_deployment':['end-level frozen-policy OPE on held-out matches','full nuisance-model-refit bootstrap','domain-grounded unobserved-confounding sensitivity analysis','learned target-region and local PhysX verification']}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),'state_node_count':len(nodes),'unambiguous_effect_node_count':out['unambiguous_effect_node_count']},ensure_ascii=False))
if __name__=='__main__':main()
