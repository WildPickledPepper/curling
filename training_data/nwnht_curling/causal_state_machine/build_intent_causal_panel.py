#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build S -> pre-shot intent proxy -> realized effect -> reply -> Y panel."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path
try:
 from .build_causal_state_abstraction import _opponent_reply_effect,state_key
 from .build_causal_estimation_panel import fold_for_match
 from .derive_pre_shot_intent_panel import intent
except ImportError:
 import sys;sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
 from causal_state_machine.build_causal_state_abstraction import _opponent_reply_effect,state_key # type: ignore
 from causal_state_machine.build_causal_estimation_panel import fold_for_match # type: ignore
 from causal_state_machine.derive_pre_shot_intent_panel import intent # type: ignore
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--input',type=Path,default=root/'nwnht_first_player_board_effects_v2.jsonl');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_intent_causal_panel_v1.jsonl');p.add_argument('--manifest',type=Path,default=root/'nwnht_first_player_intent_causal_panel_v1_manifest.json');args=p.parse_args()
 if args.output.exists() or args.manifest.exists():raise SystemExit('Refusing to overwrite existing output')
 n=0;counts=Counter()
 with args.output.open('w',encoding='utf-8') as out:
  for line in args.input.open(encoding='utf-8'):
   r=json.loads(line);k=int(r['own_throw_number']);call=str(r['observed_own_delivery']['called_shot']);i=intent(call);counts[i]+=1;n+=1
   out.write(json.dumps({'panel_key':f"{r['end_id']}:{r['own_global_shot_number']}",'match_id':r['match_id'],'fold':fold_for_match(int(r['match_id'])),'K':k,'runtime_core_state':state_key(k,list(r['s_before_own'])),'runtime_fine_state':state_key(k,list(r['s_before_own']),fine=True),'pre_shot_intent_proxy':i,'upstream_call_for_audit':call,'realized_board_effect':r['observed_own_board_effect']['primary_effect'],'opponent_reply_effect_proxy':_opponent_reply_effect(list(r['u_after_own']),list(r['s_after_opponent_reply'])),'terminal_first_end_margin':r['terminal_end_label']['first_end_margin'],'offline_confounders':{'first_team':r['first_team'],'opponent_team':r['opponent_team'],'event_name':r['offline_context']['event_name']}},ensure_ascii=False,sort_keys=True)+'\n')
 m={'schema':'nwnht_first_player_intent_causal_panel_v1','rows':n,'intent_counts':dict(sorted(counts.items())),'temporal_contract':'pre_shot_intent_proxy uses only upstream_called_shot recorded for the delivery; realized_board_effect and opponent_reply_effect_proxy are explicitly downstream labels.','runtime_contract':'Only K/runtime_core_state/runtime_fine_state may be used at runtime. Intent proxy and all other fields are offline labels.','limits':['Upstream call is an imperfect intent proxy, not a local execution command.','No target-region class is available yet.']}
 args.manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),'manifest':str(args.manifest),'rows':n,'intent_counts':m['intent_counts']},ensure_ascii=False))
if __name__=='__main__':main()
