#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conservatively gate bootstrap candidates; does not approve strategy edges."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
 root=Path(__file__).resolve().parent/'artifacts'; p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--bootstrap',type=Path,default=root/'nwnht_first_player_dr_cluster_bootstrap_v0.json');p.add_argument('--homogeneity',type=Path,default=root/'nwnht_first_player_state_homogeneity_screen_v0.json');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_causal_edge_gate_v0.json');args=p.parse_args()
 if args.output.exists(): raise SystemExit(f'Refusing to overwrite {args.output}')
 b=json.loads(args.bootstrap.read_text(encoding='utf-8'));h=json.loads(args.homogeneity.read_text(encoding='utf-8'))
 blocked={(x['core_state'],x['observed_own_effect']) for x in h['diagnostics'] if x['abstraction_status']=='STABLE_HETEROGENEITY_SPLIT'}
 edges=[]
 for x in b['advantages']:
  if not x['cluster_bootstrap_positive']: continue
  issues=[]
  if (x['state_id'],x['better_candidate']) in blocked: issues.append('better_candidate_has_stable_fine_state_heterogeneity')
  if (x['state_id'],x['comparison_action']) in blocked: issues.append('comparison_action_has_stable_fine_state_heterogeneity')
  lcb=float(x['cluster_bootstrap_lcb'])
  edges.append({**x,'unobserved_differential_bias_to_zero_end_margin':round(lcb,4),'sensitivity_at_0_10_end_margin_bias':round(lcb-0.10,4),'heterogeneity_issues':issues,'gate':'REJECT_OR_SPLIT' if issues else 'NEEDS_REFUTATION_AND_OPE'})
 out={'schema':'nwnht_first_player_causal_edge_gate_v0','purpose':'Conservative post-bootstrap gate; no edge is strategy-approved.','sensitivity_interpretation':'If an omitted factor can create a treatment-specific differential end-margin bias at least equal to unobserved_differential_bias_to_zero_end_margin, the bootstrap lower bound can be driven to zero. This is a transparent bias-threshold analysis, not identification of the omitted factor.','summary':{'bootstrap_positive_candidates':len(edges),'blocked_by_known_fine_state_heterogeneity':sum(bool(x['heterogeneity_issues']) for x in edges),'candidates_with_bias_threshold_over_0_10':sum(x['unobserved_differential_bias_to_zero_end_margin']>0.10 for x in edges)},'candidates':edges,'remaining_required_gates':['multiple-seed/permutation refutations','match-cluster bootstrap with nuisance-model refit','unobserved-confounding domain justification','frozen-policy holdout OPE','local-rule and PhysX reachability']}
 args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),**out['summary']},ensure_ascii=False))
if __name__=='__main__':main()
