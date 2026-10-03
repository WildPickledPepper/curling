#!/usr/bin/env python3
"""画 Unity 控制器的有效场地与规划器的策略废球区。"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Rectangle

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from planning_proxy.competition_rules import HOUSE_R, HOUSE_X, HOUSE_Y, STONE_R
from planning_proxy.first_player_strategy import (
    BACK_HOUSE_DEAD_Y,
    EDGE_DEAD_LEFT,
    EDGE_DEAD_RIGHT,
)


OUTPUT = Path(__file__).resolve().parents[1] / "runs" / "unity_rink_and_tactical_dead_zones.png"
FONT = Path(r"C:\Windows\Fonts\msyh.ttc")

# Unity UpdateState 保留 body_x/body_y 的严格范围，换成 protocol/规划坐标。
UNITY_LEFT, UNITY_RIGHT = -2.23 + HOUSE_X, 2.23 + HOUSE_X
UNITY_BACK, UNITY_FRONT = -2.015 + HOUSE_Y, 5.645 + HOUSE_Y


def label(ax: plt.Axes, x: float, y: float, text: str, *, color: str = "#162a3a", size: float = 10) -> None:
    ax.text(x, y, text, ha="center", va="center", color=color, fontsize=size,
            fontproperties=FontProperties(fname=str(FONT)) if FONT.exists() else None)


def main() -> int:
    fig, ax = plt.subplots(figsize=(10, 12), constrained_layout=True)
    font = FontProperties(fname=str(FONT)) if FONT.exists() else None

    # 控制器外侧是 Unity UpdateState 会清槽并 SetActive(false) 的物理出场区。
    ax.set_facecolor("#eceff1")
    ax.add_patch(Rectangle((UNITY_LEFT, UNITY_BACK), UNITY_RIGHT - UNITY_LEFT, UNITY_FRONT - UNITY_BACK,
                           facecolor="#edf8fb", edgecolor="#1d4d63", linewidth=2.0, zorder=1))

    # 策略层仍有效的区域：排除两侧废球带，排除完全越过后沿的壶。
    ax.add_patch(Rectangle((EDGE_DEAD_LEFT[1], BACK_HOUSE_DEAD_Y),
                           EDGE_DEAD_RIGHT[0] - EDGE_DEAD_LEFT[1], UNITY_FRONT - BACK_HOUSE_DEAD_Y,
                           facecolor="#dff3dd", edgecolor="none", alpha=0.85, zorder=2))
    ax.add_patch(Rectangle((EDGE_DEAD_LEFT[0], UNITY_BACK), EDGE_DEAD_LEFT[1] - EDGE_DEAD_LEFT[0],
                           UNITY_FRONT - UNITY_BACK, facecolor="#ffd7d2", edgecolor="#c75246", hatch="///", alpha=0.75, zorder=3))
    ax.add_patch(Rectangle((EDGE_DEAD_RIGHT[0], UNITY_BACK), EDGE_DEAD_RIGHT[1] - EDGE_DEAD_RIGHT[0],
                           UNITY_FRONT - UNITY_BACK, facecolor="#ffd7d2", edgecolor="#c75246", hatch="///", alpha=0.75, zorder=3))
    ax.add_patch(Rectangle((UNITY_LEFT, UNITY_BACK), UNITY_RIGHT - UNITY_LEFT, BACK_HOUSE_DEAD_Y - UNITY_BACK,
                           facecolor="#ffd7d2", edgecolor="#c75246", hatch="///", alpha=0.75, zorder=3))

    # 大本营及中线。
    for radius, color, alpha in ((HOUSE_R, "#5a86b8", 0.13), (1.22, "#ffffff", 0.85), (0.61, "#df5b59", 0.25)):
        ax.add_patch(Circle((HOUSE_X, HOUSE_Y), radius, facecolor=color, edgecolor="#315d8e", linewidth=1.1, alpha=alpha, zorder=4))
    ax.axvline(HOUSE_X, color="#4c6575", linestyle="--", linewidth=1.0, zorder=5)
    ax.axhline(HOUSE_Y, color="#4c6575", linestyle="--", linewidth=1.0, zorder=5)
    ax.axhline(BACK_HOUSE_DEAD_Y, color="#c75246", linestyle="--", linewidth=1.5, zorder=6)

    # 标出一颗壶的尺度，避免把中心边界误解成壶沿边界。
    ax.add_patch(Circle((4.00, 9.65), STONE_R, facecolor="#2672b8", edgecolor="#123d66", zorder=7))
    label(ax, 3.65, 9.65, "壶半径 0.145 m", size=9)

    label(ax, HOUSE_X, 10.14, "Unity 控制器有效保留区\n（超出该框：物理出场 / disabled）", size=12)
    label(ax, HOUSE_X, 8.75, "策略非废球区\n（仍可能是守壶、障碍或得分威胁）", color="#216b31", size=11)
    label(ax, (EDGE_DEAD_LEFT[0] + EDGE_DEAD_LEFT[1]) / 2, 7.3, "左侧\n废球带", color="#9e362e", size=9)
    label(ax, (EDGE_DEAD_RIGHT[0] + EDGE_DEAD_RIGHT[1]) / 2, 7.3, "右侧\n废球带", color="#9e362e", size=9)
    label(ax, HOUSE_X, 2.72, "大本营后方废球区\n（壶心 ≤ %.3f m，完全不可能计分）" % BACK_HOUSE_DEAD_Y, color="#9e362e", size=10)
    label(ax, HOUSE_X, HOUSE_Y + 0.05, "大本营圆心\n(2.375, 4.880)", size=9)

    ax.annotate("后沿废球线", xy=(UNITY_RIGHT, BACK_HOUSE_DEAD_Y), xytext=(4.95, 3.18),
                arrowprops={"arrowstyle": "->", "color": "#c75246"}, color="#9e362e", fontproperties=font, fontsize=10)
    ax.set_xlim(-0.25, 5.65)
    ax.set_ylim(2.25, 11.05)
    ax.set_aspect("equal")
    ax.set_xlabel("协议 x / m（左右）", fontproperties=font)
    ax.set_ylabel("协议 y / m（前后；投壶从上向下）", fontproperties=font)
    ax.set_title("Unity 球场与规划器的策略废球定义", fontsize=17, weight="bold", fontproperties=font)
    ax.grid(alpha=0.2)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=200, bbox_inches="tight")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
