#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a pre-shot intent-proxy panel; board effect remains an outcome, not treatment."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

def intent(call:str)->str:
 m={'DRAW':'DRAW_TO_HOUSE','FREEZE':'FREEZE','GUARD':'GUARD','FRONT':'GUARD','TAKEOUT':'HIT_OR_REMOVE','DOUBLE_TAKEOUT':'HIT_OR_REMOVE','CLEARING':'HIT_OR_REMOVE','PROMOTION_TAKEOUT':'RAISE_OR_PROMOTE','RAISE':'RAISE_OR_PROMOTE','HIT_AND_ROLL':'HIT_AND_ROLL','WICK_OR_SOFT_PEEL':'HIT_OR_REMOVE','THROUGH':'THROUGH'}
 return m.get(call,'UNCLASSIFIED_INTENT')
def main():
 root=Path(__file__).resolve().parent/'artifacts';p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--input',type=Path,default=root/'nwnht_first_player_board_effects_v2.jsonl');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_pre_shot_intent_panel_v0.jsonl');p.add_argument('--manifest',type=Path,default=root/'nwnht_first_player_pre_shot_intent_panel_v0_manifest.json');args=p.parse_args()
 if args.output.exists() or args.manifest.exists():raise SystemExit('Refusing to overwrite existing output')
 counts=Counter();n=0
 with args.output.open('w',encoding='utf-8') as out:
  for line in args.input.open(encoding='utf-8'):
   r=json.loads(line);raw=str(r['observed_own_delivery']['called_shot']);i=intent(raw);counts[i]+=1;n+=1
   out.write(json.dumps({'panel_key':f"{r['end_id']}:{r['own_global_shot_number']}",'match_id':r['match_id'],'K':r['own_throw_number'],'runtime_board_before':r['s_before_own'],'offline_confounders':{'first_team':r['first_team'],'opponent_team':r['opponent_team'],'event_name':r['offline_context']['event_name']},'pre_shot_intent_proxy':i,'upstream_call_for_audit':raw,'realized_board_effect':r['observed_own_board_effect']['primary_effect'],'opponent_reply_board_effect_proxy':None,'terminal_first_end_margin':r['terminal_end_label']['first_end_margin']},ensure_ascii=False,sort_keys=True)+'\n')
 manifest={'schema':'nwnht_first_player_pre_shot_intent_panel_v0','rows':n,'intent_counts':dict(sorted(counts.items())),'treatment_definition':'pre_shot_intent_proxy is recorded before its realized board effect, but it is an upstream called-shot proxy rather than a local PhysX command.','causal_role':'Use intent as treatment candidate; use realized_board_effect as mediator/outcome. Do not reverse these roles.','limits':['Intent labels may be noisy or incomplete.','No target region has yet been inferred.','No runtime policy may use upstream call labels.']}
 args.manifest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),'manifest':str(args.manifest),'rows':n,'intent_counts':manifest['intent_counts']},ensure_ascii=False))
if __name__=='__main__':main()
