"""Create a transparent end-by-end tactical review from NWNHT's public DB.

No PDF parsing is performed.  The input is the original, read-only SQLite
database distributed with NWNHT/curling.  The report deliberately separates
facts recorded by the upstream database (call, rating, detected stones) from
our short tactical interpretation.
"""

from __future__ import annotations

import argparse
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HOUSE_RADIUS_M = 1.8288
ROOT = Path(__file__).resolve().parent
DEFAULT_DATABASE = ROOT.parents[1] / "external_research" / "NWNHT_curling" / "curling-main" / "src" / "world_curling_ss.db"


def connect(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise FileNotFoundError(f"Public database not found: {path}")
    connection = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def derive_stone_colour_maps(
    states: dict[tuple[int, int], dict[str, Any]], teams: list[str]
) -> tuple[dict[int, dict[str, str]], dict[int, str]]:
    """Infer each end's stone-colour ownership from observable additions.

    NWNHT stores the player/team correctly, but some pages viewed from the
    opposite end have their *throw colour* label reversed relative to the
    detected stone colour.  Rather than trusting that label, use the fact
    that when a retained stone count increases by exactly one, it must be the
    current thrower's colour.  One established colour determines the other
    because an end has exactly two teams.  Ambiguity remains explicit.
    """
    maps: dict[int, dict[str, str]] = defaultdict(dict)
    evidence: dict[int, str] = {}
    end_numbers = sorted({end for end, _ in states})
    for end_no in end_numbers:
        previous: Counter[str] = Counter()
        conflicts = 0
        for shot in sorted(shot for end, shot in states if end == end_no):
            state = states[(end_no, shot)]
            current = Counter(str(stone["colour"]) for stone in state["stones"])
            increased = [colour for colour in ("red", "yellow") if current[colour] == previous[colour] + 1]
            throw_team = state["throw_team"]
            if len(increased) == 1 and throw_team:
                colour = increased[0]
                old = maps[end_no].get(colour)
                if old is None:
                    maps[end_no][colour] = str(throw_team)
                elif old != throw_team:
                    conflicts += 1
            previous = current
        if len(maps[end_no]) == 1:
            colour, owner = next(iter(maps[end_no].items()))
            other_colour = "yellow" if colour == "red" else "red"
            other_team = next((team for team in teams if team != owner), None)
            if other_team is not None:
                maps[end_no][other_colour] = other_team
        if len(maps[end_no]) == 2 and conflicts == 0:
            evidence[end_no] = "由连续壶面新增壶与投手队伍反推"
        elif len(maps[end_no]) == 2:
            evidence[end_no] = f"由连续壶面反推，但存在 {conflicts} 次冲突"
        else:
            evidence[end_no] = "未能从可见新增壶唯一确定颜色归属"
    return maps, evidence


def stone_summary(stones: list[dict[str, Any]], teams: list[str]) -> tuple[str, str]:
    """Return total on-sheet counts and current scoring side from detected stones."""
    counts = Counter(stone["team"] for stone in stones)
    count_text = ", ".join(f"{team} {counts[team]}" for team in teams)
    in_house = [stone for stone in stones if stone["radius_m"] <= HOUSE_RADIUS_M]
    if not in_house:
        return count_text, "营内无壶"
    in_house.sort(key=lambda stone: stone["radius_m"])
    scoring_team = in_house[0]["team"]
    scoring = 0
    for stone in in_house:
        if stone["team"] != scoring_team:
            break
        scoring += 1
    nearest = in_house[0]
    return count_text, f"{scoring_team} 暂得 {scoring}（最近 {nearest['radius_m']:.2f} m）"


def tactical_tag(call: str | None) -> str:
    """A restrained interpretation of the official call label, not a claim of intent."""
    mapping = {
        "Take-out": "清除/处理对方壶",
        "Double Take-out": "双飞，压低场上壶数",
        "Clearing": "清场，降低复杂度",
        "Guard": "前场守壶，制造掩护",
        "Front": "前场占位/守壶",
        "Draw": "落营或前场落点",
        "Hit and Roll": "撞击后滚到新位置",
        "Raise": "推进己方壶",
        "Promotion Take-out": "借己方壶完成清除",
        "Wick / Soft Peeling": "轻碰/软 peel，调整而非硬清",
    }
    return mapping.get(call or "", "上游未归类的叫球")


def conclusion(
    end_number: int,
    hammer_team: str | None,
    points: dict[str, int],
    call_counts: Counter[str],
    complete: bool,
) -> str:
    if not complete:
        return (
            f"第 {end_number} 局：上游库没有完整的 16 手记录（或最后一手没有投手信息）。"
            "比分栏仍可作为赛果参考，但不能据此判成 blank、偷分或末手战术。"
        )
    scorer = next((team for team, value in points.items() if value > 0), None)
    clears = sum(call_counts[call] for call in ("Take-out", "Double Take-out", "Clearing"))
    guards = sum(call_counts[call] for call in ("Guard", "Front"))
    draws = call_counts["Draw"]
    if scorer is None:
        basis = "本局 blank；后手没有拿分，后手权保留。"
    elif scorer == hammer_team:
        basis = f"{scorer} 有后手并拿到 {points[scorer]} 分。"
    else:
        basis = f"{scorer} 无后手却拿到 {points[scorer]} 分，属于偷分。"
    pattern = f"叫球结构：清除类 {clears} 手、守壶类 {guards} 手、draw {draws} 手。"
    if clears >= 10:
        lesson = "这局明显优先降低壶数；与“后手局面不利时可清场/blank”分支相符。"
    elif guards >= 4 and draws >= 4:
        lesson = "前场结构与营内落点同时出现，属于主动制造多层局面的样本。"
    else:
        lesson = "需要结合逐手壶面判断是哪一次碰撞改变了局势，不能仅从叫球名称下结论。"
    return f"第 {end_number} 局：{basis} {pattern} {lesson}"


def build_report(connection: sqlite3.Connection, match_id: int) -> str:
    match = connection.execute(
        """
        SELECT m.*, ev.name AS event_name, ev.start_date AS event_start_date
        FROM Match m JOIN Event ev ON ev.event_id=m.event_id WHERE m.match_id=?
        """,
        (match_id,),
    ).fetchone()
    if match is None:
        raise ValueError(f"Unknown match_id={match_id}")
    teams = [str(match["team_1"]), str(match["team_2"])]
    rows = connection.execute(
        """
        SELECT e.end_id,e.num AS end_number,e.hammer_colour,e.team_1_final_score,e.team_2_final_score,
               pos.position_id,pos.frame_num,t.colour AS throw_colour,t.type AS called_shot,t.rating,p.name,p.team,
               s.colour AS stone_colour,s.x,s.y,s.size
        FROM End e JOIN Position pos ON pos.end_id=e.end_id
        LEFT JOIN Throw t ON t.end_id=e.end_id AND t.throw_num=pos.frame_num
        LEFT JOIN Player p ON p.player_id=t.player_id
        LEFT JOIN Stone s ON s.position_id=pos.position_id
        WHERE e.match_id=? AND pos.frame_num BETWEEN 1 AND 16
        ORDER BY e.num,pos.frame_num,s.stone_id
        """,
        (match_id,),
    )
    states: dict[tuple[int, int], dict[str, Any]] = {}
    end_meta: dict[int, dict[str, Any]] = {}
    for row in rows:
        end_no, shot = int(row["end_number"]), int(row["frame_num"])
        key = (end_no, shot)
        if key not in states:
            states[key] = {
                "stones": [],
                "throw_team": row["team"], "player": row["name"], "call": row["called_shot"], "rating": row["rating"],
            }
            end_meta[end_no] = {
                "end_id": int(row["end_id"]), "hammer_colour": row["hammer_colour"],
                "score_after": {teams[0]: int(row["team_1_final_score"]), teams[1]: int(row["team_2_final_score"])},
            }
        if row["stone_colour"] is not None:
            colour = str(row["stone_colour"])
            x, y = float(row["x"]), float(row["y"])
            states[key]["stones"].append({"colour": colour, "x_m": x, "y_m": y, "radius_m": (x * x + y * y) ** 0.5})

    maps, map_evidence = derive_stone_colour_maps(states, teams)
    for (end_no, _), state in states.items():
        for stone in state["stones"]:
            colour = str(stone["colour"])
            stone["team"] = maps[end_no].get(colour, f"未知({colour})")

    lines = [
        f"# NWNHT 公开壶谱复盘：{match['team_1']} vs {match['team_2']}",
        "",
        f"- 比赛：{match['event_name']}，{match['start_time']}，match_id={match_id}",
        f"- 最终比分：{match['team_1']} {match['team_1_final_score']} – {match['team_2_final_score']} {match['team_2']}",
        "- 数据：NWNHT/curling 随附 SQLite；壶位为上游自动解析坐标。叫球/评分和壶位是事实记录，最后一列的战术意图是我们的保守归纳。",
        "- 对照原则：[Team Gushue 公开战术树](../../planning_proxy/docs/strategy/05_Team_Gushue公开战术树_证据版.md)。",
        "",
    ]
    previous_score = {team: 0 for team in teams}
    for end_no in sorted(end_meta):
        meta = end_meta[end_no]
        colour_map = maps[end_no]
        present_shots = sorted(shot for end, shot in states if end == end_no)
        complete = present_shots == list(range(1, 17)) and bool(states[(end_no, 16)]["throw_team"])
        hammer_team = states[(end_no, 16)]["throw_team"] if complete else None
        score_after = meta["score_after"]
        points = {team: score_after[team] - previous_score[team] for team in teams}
        calls = Counter(str(states[(end_no, shot)]["call"]) for shot in range(1, 17) if (end_no, shot) in states)
        lines += [
            f"## 第 {end_no} 局",
            "",
            f"- 后手：{hammer_team or '未能由完整末手确认'}；本局得分：{teams[0]} {points[teams[0]]}，{teams[1]} {points[teams[1]]}；累计：{teams[0]} {score_after[teams[0]]}，{teams[1]} {score_after[teams[1]]}。",
            f"- 壶色归属：red→{colour_map.get('red', '未知')}，yellow→{colour_map.get('yellow', '未知')}（{map_evidence[end_no]}）。",
            f"- 逐手覆盖：{len(present_shots)}/16 手" + ("，完整。" if complete else "，不完整；本局不下完整战术结论。"),
            "",
            "| 手 | 出手方 / 投手 | 官方叫球（评分） | 出手后检测壶数 | 营内暂时得分 | 观察到的离散目标 |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for shot in range(1, 17):
            state = states.get((end_no, shot))
            if state is None:
                continue
            total, scoring = stone_summary(state["stones"], teams)
            actor = f"{state['throw_team'] or '未知'} / {state['player'] or '未知'}"
            call = state["call"] or "未记录"
            rating = "-" if state["rating"] is None else str(state["rating"])
            lines.append(f"| {shot} | {actor} | {call}（{rating}） | {total} | {scoring} | {tactical_tag(state['call'])} |")
        lines += ["", conclusion(end_no, hammer_team, points, calls, complete), ""]
        previous_score = score_after
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--match-id", type=int, required=True)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or ROOT / "reviews" / f"match_{args.match_id}.md"
    if output.exists():
        raise SystemExit(f"Refusing to overwrite {output}; choose a new --output or remove it deliberately.")
    with connect(args.database) as connection:
        report = build_report(connection, args.match_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
