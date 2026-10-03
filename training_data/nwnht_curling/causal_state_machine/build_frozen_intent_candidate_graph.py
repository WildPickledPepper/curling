#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Freeze intent-proxy candidates with observed downstream distributions."""
from __future__ import annotations
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--gate',type=Path,required=True);p.add_argument('--panel',type=Path,default=root/'nwnht_first_player_intent_causal_panel_v1.jsonl');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_intent_frozen_graph_v0.json');args=p.parse_args()
 if args.output.exists():raise SystemExit(f'Refusing to overwrite {args.output}')
 gate=json.loads(args.gate.read_text(encoding='utf-8'));targets={(x['state_id'],x['better_candidate']):x for x in gate['survivors']};stats=defaultdict(lambda:{'effect':Counter(),'reply':Counter(),'n':0})
 for line in args.panel.open(encoding='utf-8'):
  r=json.loads(line);key=(r['runtime_core_state'],r['pre_shot_intent_proxy'])
  if key in targets:stats[key]['effect'][r['realized_board_effect']]+=1;stats[key]['reply'][r['opponent_reply_effect_proxy']]+=1;stats[key]['n']+=1
 nodes=[]
 for key,c in targets.items():
  s=stats[key];n=s['n'];nodes.append({'state_id':key[0],'recommended_pre_shot_intent_proxy':key[1],'comparison_intent_proxy':c['comparison_action'],'evidence':{k:c[k] for k in ('raw_support_better_candidate','raw_support_comparison','dr_advantage_end_margin','cluster_bootstrap_lcb','unobserved_differential_bias_to_zero_end_margin')},'observed_realized_effect_distribution':{k:round(v/n,6) for k,v in sorted(s['effect'].items())},'observed_opponent_reply_distribution':{k:round(v/n,6) for k,v in sorted(s['reply'].items())},'fallback':'SEARCH_REQUIRED','status':'FROZEN_INTENT_PROXY_FOR_HELDOUT_OPE_ONLY'})
 out={'schema':'nwnht_first_player_intent_frozen_graph_v0','purpose':'Frozen pre-shot intent-proxy graph. Downstream distributions are observed diagnostics, not guarantees.','nodes':nodes,'required_before_deployment':['held-out OPE','replace upstream intent proxy with learned target-region classes','local-rule and PhysX reachability','manual audit of call-label mapping'],'status':'NOT_DEPLOYABLE'}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),'nodes':len(nodes)},ensure_ascii=False))
if __name__=='__main__':main()
