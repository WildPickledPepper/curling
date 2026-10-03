#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从真实长时接触回退中抽取、交叉验证接触类正样本。"""
from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from planning_proxy.evaluate_vs_teammate_ppo import ProxyMatchPlayer, canonical_board  # noqa: E402
from planning_proxy.first_player_strategy import FirstPlayerPlan  # noqa: E402
from planning_proxy.strict_refine import Candidate, evaluate_one, make_position  # noqa: E402

OUT = ROOT / "planning_proxy" / "solver_benchmark" / "actual_fallback_contact_v1.json"

def sig(states: list[dict[str, Any]]) -> tuple[Any, ...]:
    return tuple((i, round(float(s["x"]), 6), round(float(s["y"]), 6), round(float(s.get("yaw", 0.0)), 6))
                 for i, s in enumerate(states) if bool(s.get("enabled", False)))

def board(states: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"index": i, "owner": "self" if i % 2 == 0 else "opponent", "x": float(s["x"]), "y": float(s["y"]), "yaw": float(s.get("yaw",0.0)), "enabled": True}
            for i,s in enumerate(states) if bool(s.get("enabled",False))]

def main() -> int:
    rows=[]; by_sig: dict[tuple[Any,...], list[tuple[str,dict[str,Any]]]]={}
    for path in sorted((ROOT/"planning_proxy"/"runs").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            try: r=json.loads(line)
            except json.JSONDecodeError: continue
            if r.get("type")!="shot" or r.get("actor")!="proxy": continue
            by_sig.setdefault(sig(r["stateBefore"]),[]).append((path.relative_to(ROOT).as_posix(),r))
            p=(r.get("detail") or {}).get("firstPlayerPlan") or {}
            if ((r.get("detail") or {}).get("mode")=="first_player_safe_fallback_after_mads" and float(r.get("decisionSeconds",0))>=50
                and p.get("opponent_action")=="physical_clear" and len((r.get("detail") or {}).get("physicsSeeds",[]))>=3): rows.append((path.relative_to(ROOT).as_posix(),r))
    seen=set(); samples=[]; env=ProxyMatchPlayer(physics_seeds=3,parent_regions=3,decision_budget_seconds=105)
    for source,fallback in rows:
        key=sig(fallback["stateBefore"])
        if key in seen: continue
        seen.add(key); raw=(fallback["detail"] or {})["firstPlayerPlan"]; plan=FirstPlayerPlan.from_json(raw)
        strict,_=canonical_board(fallback["stateBefore"],proxy_team=0); seeds=[int(x) for x in fallback["detail"]["physicsSeeds"]]
        actions=[]
        for action_source,r in by_sig.get(key,[]):
            x=tuple(float(v) for v in r.get("bestshot",[]))
            if len(x)==3 and x!=(3.0,0.0,0.0) and x not in actions: actions.append(x)
        for x in actions:
            e=evaluate_one(env.environment,Candidate(*x,parent_rank=1),strict,make_position(strict),seeds,plan.shot_index,active_index=plan.shot_index,tactical_plan=plan)
            if e.rule_legal and len(e.tactical_goal_met)==len(seeds) and all(e.tactical_goal_met):
                samples.append({"id":f"实战接触回退_v1_{len(samples):03d}","history_source":source,"original_fallback_seconds":float(fallback["decisionSeconds"]),"board":board(fallback["stateBefore"]),"goal_contract":raw,"required_physics_seeds":seeds,"oracle_witness":{"bestshot":list(x),"strict":e.to_json()}}); break
    OUT.write_text(json.dumps({"schema":"planning_proxy_actual_fallback_contact_v1","scope":"真实长时 physical_clear 回退；同完整壶面历史动作；三种子原合同正向验证","candidate_state_count":len(seen),"sample_count":len(samples),"samples":samples},ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"output":str(OUT),"long_fallback_states":len(seen),"positive_samples":len(samples)},ensure_ascii=False))
if __name__=="__main__": raise SystemExit(main())
