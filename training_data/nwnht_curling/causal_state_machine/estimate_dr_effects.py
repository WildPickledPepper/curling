#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grouped-cross-fit multi-action doubly robust screening from the causal panel.

This estimates observational backdoor-adjusted end-margin values under the
explicit sequential-ignorability assumption.  It is not a released policy.
"""
from __future__ import annotations
import argparse, json, warnings
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.exceptions import ConvergenceWarning

ACTION = "observed_own_effect"
Y = "terminal_first_end_margin"
FEATURES = ["K", "runtime_core_state", "runtime_fine_state", "first_team", "opponent_team", "event_name"]
MIN_SUPPORT = 100
PROPENSITY_FLOOR = 0.02

def load_panel(path: Path) -> pd.DataFrame:
    rows=[]
    for line in path.open(encoding='utf-8'):
        r=json.loads(line); z=r.pop('offline_confounders')
        r.update(z); rows.append(r)
    return pd.DataFrame(rows)

def permute_actions_within_k(frame: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Placebo: retain K-specific treatment prevalence but break row pairing."""
    result=frame.copy(); rng=np.random.default_rng(seed)
    for _, indices in result.groupby('K').groups.items():
        indices=np.asarray(list(indices),dtype=int)
        result.loc[indices,ACTION]=rng.permutation(result.loc[indices,ACTION].to_numpy())
    return result

def pipeline_logistic() -> Pipeline:
    return Pipeline([('onehot', ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), FEATURES)])),
                     ('model', LogisticRegression(max_iter=1000, tol=1e-3, C=0.5, solver='lbfgs', multi_class='multinomial', n_jobs=1, random_state=20260717))])

def pipeline_ridge() -> Pipeline:
    return Pipeline([('onehot', ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), FEATURES)])),
                     ('model', Ridge(alpha=20.0, solver='lsqr'))])

def estimate(frame: pd.DataFrame) -> tuple[list[dict], list[dict], dict, np.ndarray, list[str]]:
    actions=sorted(frame[ACTION].unique()); n=len(frame)
    pseudo=np.full((n,len(actions)), np.nan); propensity=np.full((n,len(actions)), np.nan)
    index={a:i for i,a in enumerate(actions)}
    for fold in sorted(frame.fold.unique()):
        test=np.flatnonzero(frame.fold.to_numpy()==fold); train=np.flatnonzero(frame.fold.to_numpy()!=fold)
        train_df, test_df=frame.iloc[train], frame.iloc[test]
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', ConvergenceWarning)
            prop=pipeline_logistic().fit(train_df, train_df[ACTION])
        if any(issubclass(item.category, ConvergenceWarning) for item in caught):
            raise RuntimeError(f"Propensity model did not converge in fold {fold}; refusing to emit DR estimates.")
        probs=prop.predict_proba(test_df)
        for j,a in enumerate(prop.named_steps['model'].classes_): propensity[test,index[a]]=probs[:,j]
        for a in actions:
            ai=index[a]; subset=train_df[train_df[ACTION]==a]
            if len(subset)<30: continue
            model=pipeline_ridge().fit(subset, subset[Y])
            m=model.predict(test_df)
            pseudo[test,ai]=m
            observed=(test_df[ACTION].to_numpy()==a)
            e=np.maximum(propensity[test,ai], PROPENSITY_FLOOR)
            pseudo[test,ai]+=observed*(test_df[Y].to_numpy()-m)/e
    results=[]; advantages=[]
    for state, ids in frame.groupby('runtime_core_state').groups.items():
        ids=np.asarray(list(ids),dtype=int); counts=Counter(frame.iloc[ids][ACTION])
        if len(ids)<MIN_SUPPORT: continue
        for a, count in sorted(counts.items()):
            if count<MIN_SUPPORT: continue
            values=pseudo[ids,index[a]]; values=values[np.isfinite(values)]
            if len(values)<MIN_SUPPORT: continue
            se=float(values.std(ddof=1)/np.sqrt(len(values)))
            results.append({'state_id':state,'action':a,'raw_action_support':count,'dr_value_end_margin':round(float(values.mean()),4),'normal_95_lcb':round(float(values.mean()-1.96*se),4),'normal_95_ucb':round(float(values.mean()+1.96*se),4),'mean_clipped_propensity':round(float(np.nanmean(np.maximum(propensity[ids,index[a]],PROPENSITY_FLOOR))),4),'low_propensity_fraction':round(float(np.nanmean(propensity[ids,index[a]]<PROPENSITY_FLOOR)),4),'status':'ESTIMATED_NOT_POLICY_APPROVED'})
        supported=sorted(a for a,count in counts.items() if count>=MIN_SUPPORT)
        for pos, left in enumerate(supported):
            for right in supported[pos + 1:]:
                diff=pseudo[ids,index[left]] - pseudo[ids,index[right]]
                diff=diff[np.isfinite(diff)]
                if len(diff)<MIN_SUPPORT: continue
                se=float(diff.std(ddof=1)/np.sqrt(len(diff)))
                advantages.append({'state_id':state,'better_candidate':left,'comparison_action':right,'raw_support_better_candidate':counts[left],'raw_support_comparison':counts[right],'dr_advantage_end_margin':round(float(diff.mean()),4),'normal_95_lcb':round(float(diff.mean()-1.96*se),4),'normal_95_ucb':round(float(diff.mean()+1.96*se),4),'status':'SCREENING_ONLY_NO_BOOTSTRAP_OR_REFUTATION'})
    manifest={'schema':'nwnht_first_player_dr_screen_v1','assumption':'Conditional exchangeability given runtime topology plus offline team/opponent/event categories; untestable and potentially false.','method':'5-fold match-grouped cross-fitted AIPW; multinomial propensity and action-specific ridge outcome models.','limits':['Board-effect treatment is a post-shot achievement proxy, not randomized intention.','Normal IID intervals are only a screening interval; no bootstrap/refutation/sensitivity test has yet passed.','No result is a policy recommendation.'],'rows':n,'actions':actions,'estimated_state_action_cells':len(results),'pairwise_advantage_cells':len(advantages),'propensity_floor':PROPENSITY_FLOOR}
    return results, advantages, manifest, pseudo, actions

def main():
    global ACTION
    root=Path(__file__).resolve().parent/'artifacts'; p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=root/'nwnht_first_player_causal_estimation_panel_v0.jsonl');p.add_argument('--output',type=Path,default=root/'nwnht_first_player_dr_screen_v1.json');p.add_argument('--influence-output',type=Path,default=None);p.add_argument('--include-folds',default=None,help='Comma-separated preassigned match folds for development-only estimation.');p.add_argument('--treatment-column',default=ACTION);p.add_argument('--permute-actions-within-k',action='store_true');p.add_argument('--seed',type=int,default=20260717); args=p.parse_args()
    if args.output.exists() or (args.influence_output is not None and args.influence_output.exists()): raise SystemExit('Refusing to overwrite existing output')
    ACTION=args.treatment_column
    frame=load_panel(args.input)
    if ACTION not in frame.columns: raise SystemExit(f'Missing treatment column: {ACTION}')
    included_folds=None if args.include_folds is None else tuple(sorted({int(value) for value in args.include_folds.split(',') if value.strip()}))
    if included_folds is not None:
        frame=frame[frame['fold'].isin(included_folds)].reset_index(drop=True)
        if len(frame)==0: raise SystemExit('No rows selected by --include-folds')
    if args.permute_actions_within_k: frame=permute_actions_within_k(frame,args.seed)
    results,advantages,manifest,pseudo,actions=estimate(frame); manifest['placebo_action_permutation_within_K']=bool(args.permute_actions_within_k); manifest['seed']=args.seed
    manifest['included_folds']=included_folds;manifest['treatment_column']=ACTION
    args.output.write_text(json.dumps({'manifest':manifest,'estimates':results,'pairwise_advantages':advantages},ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'output':str(args.output),**manifest},ensure_ascii=False))
    if args.influence_output is not None:
        np.savez_compressed(args.influence_output, match_id=frame['match_id'].to_numpy(dtype=np.int64), core_state=frame['runtime_core_state'].to_numpy(dtype=str), pseudo=pseudo.astype(np.float32), actions=np.asarray(actions,dtype=str))
if __name__=='__main__': main()
