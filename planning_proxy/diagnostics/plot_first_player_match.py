#!/usr/bin/env python3
"""把本地评测 JSONL 画成逐手壶面图，用于复盘 fallback 与双飞。"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Rectangle


HOUSE_X, HOUSE_Y = 2.375, 4.88
HOUSE_R, INNER_R, BUTTON_R, STONE_R = 1.83, 1.22, 0.61, 0.145
WINDOWS_CJK_FONT = Path(r"C:\Windows\Fonts\msyh.ttc")


def read_shots(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    return [row for row in rows if row.get("type") == "shot"]


def draw_house(ax: plt.Axes) -> None:
    ax.add_patch(Rectangle((HOUSE_X - HOUSE_R, HOUSE_Y - HOUSE_R), 2 * HOUSE_R, 2 * HOUSE_R,
                           facecolor="#f9fbff", edgecolor="none", zorder=0))
    for radius, color, alpha in ((HOUSE_R, "#3d72b4", 0.10), (INNER_R, "#ffffff", 0.80), (BUTTON_R, "#d84444", 0.20)):
        ax.add_patch(Circle((HOUSE_X, HOUSE_Y), radius, facecolor=color, edgecolor="#294c74", lw=0.8, alpha=alpha, zorder=1))
    ax.axvline(HOUSE_X, color="#697784", lw=0.7, ls="--", zorder=1)
    ax.axhline(HOUSE_Y, color="#697784", lw=0.7, ls="--", zorder=1)


def draw_stones(ax: plt.Axes, states: list[dict]) -> None:
    for state in states:
        if not state.get("enabled", False):
            continue
        index = int(state["index"])
        ours = index % 2 == 0
        color = "#2672b8" if ours else "#c94747"
        edge = "#113c66" if ours else "#712020"
        ax.add_patch(Circle((float(state["x"]), float(state["y"])), STONE_R, facecolor=color, edgecolor=edge, lw=1.0, zorder=4))
        ax.text(float(state["x"]), float(state["y"]), str(index), color="white", ha="center", va="center", fontsize=6, weight="bold", zorder=5)


def draw_targets(ax: plt.Axes, detail: dict, actor: str) -> None:
    if actor != "proxy":
        return
    plan = detail.get("firstPlayerPlan") or detail.get("fallbackFromPlan")
    if not isinstance(plan, dict):
        return
    for point in plan.get("target_points", []):
        if not isinstance(point, list) or len(point) != 2:
            continue
        ax.add_patch(Circle((float(point[0]), float(point[1])), 0.30, fill=False, edgecolor="#3a9b49", lw=1.0, ls=":", zorder=3))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    shots = read_shots(args.input)
    chinese_font = FontProperties(fname=str(WINDOWS_CJK_FONT)) if WINDOWS_CJK_FONT.exists() else None
    columns = 4
    rows = math.ceil(len(shots) / columns)
    figure, axes = plt.subplots(rows, columns, figsize=(13, 3.5 * rows), constrained_layout=True)
    axes_list = list(axes.flat) if hasattr(axes, "flat") else [axes]

    for ax, shot in zip(axes_list, shots):
        draw_house(ax)
        draw_targets(ax, shot.get("detail", {}), shot.get("actor", ""))
        draw_stones(ax, shot["stateAfter"])
        detail = shot.get("detail", {})
        mode = detail.get("mode", detail.get("tactic", ""))
        fallback = "fallback" in str(mode)
        title_color = "#c77700" if fallback else "#182b3a"
        ax.set_title(f"#{shot['shot']:02d} {shot['actor']}  score {shot['temporaryScoreFirst']:+d}\n{mode}", fontsize=8, color=title_color)
        ax.set_xlim(0.3, 4.5)
        ax.set_ylim(3.0, 9.1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("#eaf4f7")
        for spine in ax.spines.values():
            spine.set_color("#d39b25" if fallback else "#aebbc4")
            spine.set_linewidth(1.6 if fallback else 0.7)

    for ax in axes_list[len(shots):]:
        ax.axis("off")
    figure.suptitle(
        "PPO 对局复盘：蓝 = 我方先手，红 = PPO；绿虚线 = 我方声明落点区；橙框 = fallback",
        fontsize=13,
        weight="bold",
        fontproperties=chinese_font,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180, bbox_inches="tight")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
