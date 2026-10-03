#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cluster-bootstrap DR pairwise advantages without refitting nuisance models."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

def main() -> None:
    root=Path(__file__).resolve().parent/'artifacts'; p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--screen',type=Path,required=True);p.add_argument('--influence',type=Path,required=True);p.add_argument('--output',type=Path,default=root/'nwnht_first_player_dr_cluster_bootstrap_v0.json');p.add_argument('--replicates',type=int,default=200);p.add_argument('--seed',type=int,default=20260717);args=p.parse_args()
    if args.output.exists(): raise SystemExit(f'Refusing to overwrite {args.output}')
    screen=json.loads(args.screen.read_text(encoding='utf-8')); data=np.load(args.influence,allow_pickle=False)
    match=data['match_id']; states=data['core_state']; pseudo=data['pseudo']; actions=[str(x) for x in data['actions']]; action_index={a:i for i,a in enumerate(actions)}
    unique, inverse=np.unique(match,return_inverse=True); rng=np.random.default_rng(args.seed); weights=np.vstack([np.bincount(rng.choice(len(unique),size=len(unique),replace=True),minlength=len(unique)) for _ in range(args.replicates)])
    output=[]
    for edge in screen['pairwise_advantages']:
        rows=np.flatnonzero(states==edge['state_id']); left=action_index[edge['better_candidate']]; right=action_index[edge['comparison_action']]; diff=pseudo[rows,left]-pseudo[rows,right]
        if not np.isfinite(diff).all(): continue
        group=inverse[rows]; sums=np.bincount(group,weights=diff,minlength=len(unique)); counts=np.bincount(group,minlength=len(unique)); samples=(weights@sums)/(weights@counts)
        output.append({**edge,'cluster_bootstrap_replicates':args.replicates,'cluster_bootstrap_lcb':round(float(np.quantile(samples,.025)),4),'cluster_bootstrap_ucb':round(float(np.quantile(samples,.975)),4),'cluster_bootstrap_positive':bool(np.quantile(samples,.025)>0),'status':'BOOTSTRAP_SCREENING_ONLY'})
    result={'schema':'nwnht_first_player_dr_cluster_bootstrap_v0','method':'Resample match_id clusters of fixed cross-fitted DR pseudo-outcomes; nuisance models are not refit.','limits':['This is not a full refit bootstrap and does not address unobserved confounding.','Passing bootstrap does not approve a policy edge.'],'summary':{'input_pairwise_cells':len(screen['pairwise_advantages']),'bootstrapped_cells':len(output),'positive_cluster_bootstrap_lcb':sum(x['cluster_bootstrap_positive'] for x in output)},'advantages':output}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),**result['summary']},ensure_ascii=False))
if __name__=='__main__': main()
