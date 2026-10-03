#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Document why an effect-proxy candidate graph failed its held-out OPE."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

def tv(a:Counter,b:Counter):
 ta,tb=sum(a.values()),sum(b.values());return 0.0 if not ta or not tb else .5*sum(abs(a[k]/ta-b[k]/tb) for k in set(a)|set(b))
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--graph',type=Path,required=True);p.add_argument('--panel',type=Path,default=root/'nwnht_first_player_causal_estimation_panel_v0.jsonl');p.add_argument('--holdout-fold',type=int,default=4);p.add_argument('--ope',type=Path,default=root/'nwnht_first_player_holdout_frozen_policy_ipw_v0.json');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_effect_proxy_failure_diagnosis_v0.json');args=p.parse_args()
 if args.output.exists():raise SystemExit(f'Refusing to overwrite {args.output}')
 graph=json.loads(args.graph.read_text(encoding='utf-8'));policy={x['state_id']:x['recommended_observed_effect_proxy'] for x in graph['nodes'] if x['status']=='FROZEN_FOR_OPE_ONLY'}; rows=[json.loads(x) for x in args.panel.open(encoding='utf-8')];diag=[]
 for state,target in policy.items():
  dev=[r for r in rows if r['runtime_core_state']==state and r['fold']!=args.holdout_fold];hold=[r for r in rows if r['runtime_core_state']==state and r['fold']==args.holdout_fold];da=Counter(r['observed_own_effect'] for r in dev);ha=Counter(r['observed_own_effect'] for r in hold)
  diag.append({'state_id':state,'target_effect_proxy':target,'development_rows':len(dev),'holdout_rows':len(hold),'development_target_support':da[target],'holdout_target_support':ha[target],'development_action_distribution':dict(da),'holdout_action_distribution':dict(ha),'action_distribution_tv':round(tv(da,ha),4)})
 ope=json.loads(args.ope.read_text(encoding='utf-8'));out={'schema':'nwnht_first_player_effect_proxy_failure_diagnosis_v0','heldout_ope':ope['value'],'state_diagnostics':diag,'conclusions':['The held-out OPE lower bound is non-positive, so no effect-proxy policy edge is supported for deployment.','Coverage and raw target support persist in holdout; failure cannot be dismissed as a missing-state artifact alone.','The treatment is a post-shot achieved board effect. A planner chooses an intended target/mechanism, not the realized effect, so effect-proxy estimates are not by themselves executable policy prescriptions.'],'next_required_redefinition':'Define pre-shot tactical intent/target-region classes, then separately model P(achieved effect | state, intent, PhysX-feasible region).'}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),'states':len(diag),'ope_lcb':ope['value']['cluster_bootstrap_lcb']},ensure_ascii=False))
if __name__=='__main__':main()
