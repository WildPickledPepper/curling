#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply a conservative multi-seed placebo threshold to bootstrap candidates."""
from __future__ import annotations
import argparse,json
from pathlib import Path
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--bootstrap-gate',type=Path,default=root/'nwnht_first_player_causal_edge_gate_v0.json');p.add_argument('--placebos',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,default=root/'nwnht_first_player_placebo_refutation_gate_v0.json');args=p.parse_args()
 if args.output.exists():raise SystemExit(f'Refusing to overwrite {args.output}')
 gate=json.loads(args.bootstrap_gate.read_text(encoding='utf-8')); runs=[]
 for path in args.placebos:
  r=json.loads(path.read_text(encoding='utf-8')); edges=r['pairwise_advantages'];runs.append({'file':path.name,'seed':r['manifest'].get('seed'),'pairs':len(edges),'positive_normal_lcb':sum(x['normal_95_lcb']>0 for x in edges),'max_normal_lcb':max(x['normal_95_lcb'] for x in edges)})
 threshold=max(x['max_normal_lcb'] for x in runs); survivors=[x for x in gate['candidates'] if x['cluster_bootstrap_lcb']>threshold]
 out={'schema':'nwnht_first_player_placebo_refutation_gate_v0','rule':'Retain only bootstrap candidates whose cluster-bootstrap LCB exceeds the maximum normal-LCB seen across supplied K-stratified placebo runs. This is a conservative screen, not a calibrated p-value.','placebo_runs':runs,'max_placebo_normal_lcb':round(threshold,4),'survivors':[dict(x,gate='NEEDS_FROZEN_POLICY_OPE') for x in survivors],'summary':{'bootstrap_candidates':len(gate['candidates']),'survivors_after_placebo_threshold':len(survivors)}}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),**out['summary'],'max_placebo_normal_lcb':round(threshold,4)},ensure_ascii=False))
if __name__=='__main__':main()
