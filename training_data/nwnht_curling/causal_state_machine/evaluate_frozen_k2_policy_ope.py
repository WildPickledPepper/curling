#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Evaluate the frozen K2-only candidate policy using cross-fitted DR pseudo-outcomes."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np

def read_panel(path:Path):
 rows=[json.loads(line) for line in path.open(encoding='utf-8')]
 return rows
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--graph',type=Path,default=root/'nwnht_first_player_frozen_candidate_policy_graph_v1.json');p.add_argument('--panel',type=Path,default=root/'nwnht_first_player_causal_estimation_panel_v0.jsonl');p.add_argument('--influence',type=Path,default=root/'nwnht_first_player_dr_influence_v0.npz');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_frozen_k2_policy_ope_v0.json');p.add_argument('--replicates',type=int,default=200);p.add_argument('--seed',type=int,default=20260717);args=p.parse_args()
 if args.output.exists():raise SystemExit(f'Refusing to overwrite {args.output}')
 graph=json.loads(args.graph.read_text(encoding='utf-8')); policy={x['state_id']:x['recommended_observed_effect_proxy'] for x in graph['nodes'] if x['status']=='FROZEN_FOR_OPE_ONLY'}
 rows=read_panel(args.panel);data=np.load(args.influence,allow_pickle=False); actions=[str(x) for x in data['actions']]; ai={x:i for i,x in enumerate(actions)}
 if len(rows)!=len(data['match_id']) or any(int(r['match_id'])!=int(m) or r['runtime_core_state']!=s for r,m,s in zip(rows,data['match_id'],data['core_state'])):raise ValueError('Panel/influence alignment failed')
 # Exactly one K2 row per accepted end.  Uncovered ends retain observed continuation.
 selected=[]; all_end={}
 for i,r in enumerate(rows):
  if r['K']==2:
   all_end[int(r['match_id']),r['panel_key'].split(':')[0]]=i
   action=policy.get(r['runtime_core_state'])
   if action is not None:selected.append(i)
 base=np.array([rows[i]['terminal_first_end_margin'] for i in all_end.values()],dtype=float); policy_values=base.copy(); ordered=list(all_end.values()); pos={i:j for j,i in enumerate(ordered)}
 for i in selected:policy_values[pos[i]]=data['pseudo'][i,ai[policy[rows[i]['runtime_core_state']]]]
 diff=policy_values-base; matches=np.array([rows[i]['match_id'] for i in ordered]); unique,inverse=np.unique(matches,return_inverse=True);rng=np.random.default_rng(args.seed);weights=np.vstack([np.bincount(rng.choice(len(unique),len(unique),replace=True),minlength=len(unique)) for _ in range(args.replicates)]);sums=np.bincount(inverse,weights=diff,minlength=len(unique));counts=np.bincount(inverse,minlength=len(unique));boot=(weights@sums)/(weights@counts)
 out={'schema':'nwnht_first_player_frozen_k2_policy_ope_v0','policy_scope':'Only K2 exact matches to two frozen candidate states; all other decisions use observed historical continuation.','method':'End-level average of cross-fitted DR pseudo-outcome at covered K2 decision, observed terminal end margin otherwise; match-cluster bootstrap without nuisance-model refit.','coverage':{'ends':len(ordered),'covered_k2_ends':len(selected),'coverage_fraction':round(len(selected)/len(ordered),6),'candidate_effects':policy},'value':{'historical_end_margin':round(float(base.mean()),4),'frozen_partial_policy_end_margin':round(float(policy_values.mean()),4),'estimated_advantage':round(float(diff.mean()),4),'cluster_bootstrap_lcb':round(float(np.quantile(boot,.025)),4),'cluster_bootstrap_ucb':round(float(np.quantile(boot,.975)),4)},'limits':['Effect proxy is post-shot board achievement, not a directly executable shot intent.','This is a K2-only partial policy; it does not validate a full eight-shot strategy.','Bootstrap does not refit nuisance models.','No local-rule or PhysX reachability is included.'],'status':'OPE_SCREENING_ONLY_NOT_DEPLOYMENT_APPROVAL'}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),**out['coverage'],**out['value']},ensure_ascii=False))
if __name__=='__main__':main()
