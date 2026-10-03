#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Held-out match-level self-normalized IPW screen for a frozen partial policy."""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
try:
 from . import estimate_dr_effects as est
except ImportError:
 import sys
 sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
 import causal_state_machine.estimate_dr_effects as est # type: ignore
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--graph',type=Path,required=True);p.add_argument('--panel',type=Path,default=root/'nwnht_first_player_causal_estimation_panel_v0.jsonl');p.add_argument('--treatment-column',default='observed_own_effect');p.add_argument('--holdout-fold',type=int,default=4);p.add_argument('--output',type=Path,default=root/'nwnht_first_player_holdout_frozen_policy_ipw_v0.json');p.add_argument('--replicates',type=int,default=200);p.add_argument('--seed',type=int,default=20260717);args=p.parse_args()
 if args.output.exists():raise SystemExit(f'Refusing to overwrite {args.output}')
 graph=json.loads(args.graph.read_text(encoding='utf-8'));rec_key='recommended_pre_shot_intent_proxy' if args.treatment_column=='pre_shot_intent_proxy' else 'recommended_observed_effect_proxy';policy={x['state_id']:x[rec_key] for x in graph['nodes'] if rec_key in x};est.ACTION=args.treatment_column
 frame=est.load_panel(args.panel);dev=frame[frame.fold!=args.holdout_fold];test=frame[frame.fold==args.holdout_fold].copy();model=est.pipeline_logistic().fit(dev,dev[est.ACTION]);classes=list(model.named_steps['model'].classes_);probs=model.predict_proba(test);prob={a:probs[:,classes.index(a)] for a in classes};test['_target']=test.runtime_core_state.map(policy);test['_ratio']=1.0;test['_matched']=True
 for idx,row in test[test._target.notna()].iterrows():
  target=row['_target'];e=max(float(prob[target][test.index.get_loc(idx)]),.02)
  if row[est.ACTION]!=target:test.at[idx,'_matched']=False
  else:test.at[idx,'_ratio']=1.0/e
 end_rows=[]
 for (match,end),group in test.groupby(['match_id',test.panel_key.str.split(':').str[0]]):
  triggered=group[group._target.notna()]; matched=bool(triggered._matched.all()); w=float(triggered._ratio.prod()) if len(triggered) and matched else (0.0 if len(triggered) else 1.0); y=float(group.terminal_first_end_margin.iloc[0]);end_rows.append((int(match),y,w,len(triggered)))
 arr=np.asarray(end_rows,dtype=float);match=arr[:,0].astype(int);y=arr[:,1];w=arr[:,2];base=float(y.mean());value=float((w*y).sum()/w.sum()) if w.sum()>0 else float('nan');unique,inverse=np.unique(match,return_inverse=True);rng=np.random.default_rng(args.seed);boots=[]
 for _ in range(args.replicates):
  take=rng.choice(len(unique),len(unique),replace=True); mult=np.bincount(take,minlength=len(unique)); ww=mult[inverse]*w; boots.append(float((ww*y).sum()/ww.sum()) if ww.sum()>0 else float('nan'))
 boots=np.asarray([x for x in boots if np.isfinite(x)]);out={'schema':'nwnht_first_player_holdout_frozen_policy_ipw_v0','scope':'Heldout-fold end-level IPW for a frozen partial policy; all non-triggered decisions follow behavior policy.','coverage':{'holdout_fold':args.holdout_fold,'ends':len(y),'triggered_ends':int((arr[:,3]>0).sum()),'matched_triggered_ends':int(((arr[:,3]>0)&(w>0)).sum()),'effective_sample_size':round(float(w.sum()**2/(w*w).sum()),2),'max_weight':round(float(w.max()),4),'policy':policy},'value':{'historical_end_margin':round(base,4),'ipw_policy_end_margin':round(value,4),'estimated_advantage':round(value-base,4),'cluster_bootstrap_lcb':round(float(np.quantile(boots,.025)-base),4),'cluster_bootstrap_ucb':round(float(np.quantile(boots,.975)-base),4)},'limits':['IPW can be unstable under limited overlap; ESS and max_weight must be inspected.','Effect labels are post-shot achievement proxies.','No PhysX/local-rule feasibility or full causal sensitivity analysis is included.'],'status':'HELDOUT_IPW_SCREENING_ONLY'}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),**out['coverage'],**out['value']},ensure_ascii=False))
if __name__=='__main__':main()
