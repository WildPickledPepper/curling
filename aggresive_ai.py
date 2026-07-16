# -*- coding: utf-8 -*-
"""
数字冰壶 AI 选手 —— 激进进攻策略
=================================
基于 Socket 通讯框架 + strategy_library 战术库（16个战术）。

通讯框架：完整处理 CONNECTKEY → ISREADY → SETSTATE → POSITION → GO → SCORE → GAMEOVER。

策略核心：get_bestshot() 直接调用 strategy_library，按攻击性从高到低级联尝试。
  攻击性分级:
    ★★★  double_hit_last / push_in_14 / double_hit / clear     (全力猛攻)
    ★★   take_out / hit_roll / push_in / double_push_in         (积极清壶)
    ★    middle_in_center / occupy / double_push_in_center       (占中得分)
    ✗    freeze / defense / defense_push_in / disarm_defend      (防守类—不使用)

  三个阶段:
    末期(第7-8壶) → double_hit_last → push_in_14 → clear → take_out → hit_roll
    中期(第4-6壶) → 后手偏双击清场, 先手偏打定+打甩
    早期(第1-3壶) → 优先清除对手得分壶, 其次占中布局

使用方式:
    python my_robot.py -k <key> -host 127.0.0.1 -p <port>
"""

import socket
import time
import math
import sys
import os
import argparse

# ── 导入战术库 ────────────────────────────────────────────────────────
_TACTICSLIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"DCCourse", "tacticslib")
if os.path.isdir(_TACTICSLIB_DIR) and _TACTICSLIB_DIR not in sys.path:
    sys.path.insert(0, _TACTICSLIB_DIR)

try:
    import strategy_library as sl
    _HAS_TACTICSLIB = True
except ImportError:
    _HAS_TACTICSLIB = False
    print("[警告] 未找到战术库，将使用内置简化策略", flush=True)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                    第 1 部分: 通讯框架 (保留)                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

# 默认连接参数（本地服务器会通过命令行覆盖）
key  = "tewisfdlws_c38b4172-fcc9-4081-b6b2-ff5c60b37b91"
host = 'curling-server-7788.jupyterhub.svc.cluster.local'
port = 7788

parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', help='host', default=host, required=False)
parser.add_argument('-p', '--port', help='tcp server port', default=str(port), required=False)
parser.add_argument('-k', '--key',  help='CONNECTKEY', default="", required=False)
args, _ = parser.parse_known_args()


class AggressiveRobot:
    """激进进攻 AI 选手 —— Socket 通讯 + 战术库策略。"""

    def __init__(self, key: str, name: str, host: str, port: int, show_msg: bool = True):
        # ── Socket 连接 ──────────────────────────────────────────
        self.ai_sock = socket.socket()
        self.ai_sock.connect((host, port))
        print(f"已建立socket连接 {host}:{port}", flush=True)

        self.show_msg = show_msg
        self.send_msg("CONNECTKEY:" + key)

        # ── 状态变量 ─────────────────────────────────────────────
        self.name = name
        self.position = [0.0] * 32       # 16 个壶的 (x,y) 坐标
        self.motioninfo = [0.0] * 5       # 运动状态
        self.round_num = 0
        self.shot_num = 0
        self.round_total = 4
        self.player_is_init = True        # True=先手(蓝), False=后手(红)
        self.score = 0

    # ── Socket 收发（保留原通讯逻辑） ──────────────────────────────

    def send_msg(self, msg: str):
        if self.show_msg:
            print("  >>>> " + msg, flush=True)
        self.ai_sock.send(msg.strip().encode())

    def recv_msg(self):
        """逐字节接收直到 \\0 终结符，返回 (消息码, 参数列表)。"""
        buffer = bytearray()
        while True:
            data = self.ai_sock.recv(1)
            if not data or data == b'\0':
                break
            buffer.extend(data)
        msg_str = buffer.decode().strip()
        if self.show_msg:
            print("<<<< " + msg_str, flush=True)

        msg_list = msg_str.split(" ")
        msg_code = msg_list[0]
        msg_list.pop(0)
        return msg_code, msg_list

    # ── 场地工具函数 ──────────────────────────────────────────────

    @staticmethod
    def get_dist(x: float, y: float) -> float:
        return math.sqrt((x - 2.375) ** 2 + (y - 4.88) ** 2)

    @staticmethod
    def is_in_house(dist: float) -> bool:
        return dist < (1.830 + 0.145)

    def recv_setstate(self, msg_list: list):
        self.shot_num    = int(msg_list[0])
        self.round_num   = int(msg_list[1])
        self.round_total = int(msg_list[2])
        self.next_shot   = int(msg_list[3])

    @property
    def my_shot_idx(self) -> int:
        """我方在当前局中的第几壶 (1-8)。"""
        if self.player_is_init:
            return (self.shot_num // 2) + 1
        else:
            return ((self.shot_num - 1) // 2) + 1

    # ── 构建战术库所需参数 ────────────────────────────────────────

    def build_state_list(self) -> list:
        """从 self.position 构建战术库需要的 16 个 [x,y] 坐标列表。

        顺序: [先手0, 后手0, 先手1, 后手1, ...]
        战术库用 is_init 来区分己方/对方。
        """
        result = []
        for i in range(8):
            x1 = float(self.position[i * 4])
            y1 = float(self.position[i * 4 + 1])
            x2 = float(self.position[i * 4 + 2])
            y2 = float(self.position[i * 4 + 3])
            result.append([x1, y1])
            result.append([x2, y2])
        return result

    def get_is_init(self) -> int:
        """0 = 我方先手(蓝), 1 = 我方后手(红)。"""
        return 0 if self.player_is_init else 1

    # ╔════════════════════════════════════════════════════════════╗
    # ║          第 2 部分: ★ 激进进攻策略 ★                       ║
    # ║                                                          ║
    # ║  16 个战术按攻击性从高到低分级:                              ║
    # ║  ★★★  double_hit_last > push_in_14 > double_hit > clear  ║
    # ║  ★★   take_out > hit_roll > push_in > double_push_in     ║
    # ║  ★     middle_in_center > occupy > double_push_in_center  ║
    # ║  ✗     freeze / defense / defense_push_in / disarm_defend║
    # ║        (防守类战术 — 激进策略不主动使用)                     ║
    # ╚════════════════════════════════════════════════════════════╝

    def get_bestshot(self) -> str:
        """激进策略主决策 —— 按攻击性从高到低依次尝试战术库函数。

        三个阶段:
          末期 (我方第7-8壶) → 全力猛攻，一壶清两敌
          中期 (我方第4-6壶) → 积极清壶，为末段铺路
          早期 (我方第1-3壶) → 清除威胁 + 占中布局

        每个阶段都区分先手(init)和后手(gote):
          后手有最后一壶优势 → 更激进地清场，为最后一壶留出中路
          先手没有最后优势 → 更积极地占中偷分，同时清对手得分壶
        """
        if self.show_msg:
            print(f"============第{self.round_num+1}局第{self.shot_num+1}壶"
                  f" (我方第{self.my_shot_idx}壶)============", flush=True)

        if not _HAS_TACTICSLIB:
            return self._fallback_shot()

        s_list  = self.build_state_list()
        is_init = self.get_is_init()
        shot_n  = self.shot_num
        idx     = self.my_shot_idx
        is_gote = (is_init == 1)   # True=后手, False=先手

        def try_tactic(fn, name: str) -> str | None:
            result = fn(s_list, is_init, shot_n)
            if result is not None and result != 0:
                v0, h0 = float(result[0]), float(result[1])
                print(f"  [战术] {name} → v0={v0:.3f} h0={h0:.3f}", flush=True)
                return f"BESTSHOT {v0:.3f} {h0:.3f} 0.000"
            return None

        # ═══════════════════════════════════════════════════════
        # 阶段 A: 末期 (我方第8壶 = shot 14/15) — 拼命模式
        #   优先双击(double_hit_last)一箭双雕；
        #   不行就传击(push_in_14)借力打力；
        #   再不行炸球(clear)暴力清场。
        # ═══════════════════════════════════════════════════════
        if idx == 8:
            for fn, name in [
                (sl.double_hit_last,      "双击(末壶)"),   # ★★★ 专为最后一壶设计
                (sl.push_in_14,           "传击(14杆)"),   # ★★★ 最后一壶借力传击
                (sl.double_hit_gote,      "双击(后手)"),   # ★★★ 标准双击
                (sl.double_hit_init,      "双击(先手)"),
                (sl.double_push_in,       "双传进营"),     # ★★ 两段接力传击
                (sl.clear,                "炸球"),         # ★★★ 暴力清场
                (sl.take_out,             "打定"),         # ★★ 精确移除
                (sl.hit_roll,             "打甩"),         # ★★ 打了还站位
                (sl.push_in,              "传击"),         # ★★ 单段传击
            ]:
                msg = try_tactic(fn, name)
                if msg is not None:
                    return msg

        # ═══════════════════════════════════════════════════════
        # 阶段 B: 中期 (我方第6-7壶) — 积极清壶
        #   后手方: 尤其要清空中路，为最后一壶留出得分空间
        #   先手方: 清除对手得分壶，尝试偷分
        # ═══════════════════════════════════════════════════════
        if idx >= 6:
            # 后手方的中期优先级: 双击 > 打甩 > 传击 > 炸球
            # 先手方的中期优先级: 打定 > 双击 > 打甩 > 传击
            if is_gote:
                mid_order = [
                    (sl.double_hit_gote,      "双击(后手)"),
                    (sl.double_hit_init,      "双击(先手)"),
                    (sl.hit_roll,             "打甩"),
                    (sl.take_out,             "打定"),
                    (sl.push_in,              "传击"),
                    (sl.double_push_in,       "双传进营"),
                    (sl.clear,                "炸球"),
                    (sl.middle_in_center,     "中路进营"),
                ]
            else:
                mid_order = [
                    (sl.take_out,             "打定"),
                    (sl.hit_roll,             "打甩"),
                    (sl.double_hit_init,      "双击(先手)"),
                    (sl.double_hit_gote,      "双击(后手)"),
                    (sl.push_in,              "传击"),
                    (sl.clear,                "炸球"),
                    (sl.double_push_in,       "双传进营"),
                    (sl.middle_in_center,     "中路进营"),
                ]
            for fn, name in mid_order:
                msg = try_tactic(fn, name)
                if msg is not None:
                    return msg

        # ═══════════════════════════════════════════════════════
        # 阶段 C: 早期 (我方第1-3壶) — 清除威胁 + 占中
        #   优先: 如果对手有壶在营内 → 立刻清除
        #   其次: 占中布局，为后续进攻铺路
        # ═══════════════════════════════════════════════════════

        # C1: 对手壶在营内 → 立即清除
        house_stones = self._get_house_stones()
        opp_in_house = [s for s in house_stones if not s[3]]
        if opp_in_house:
            for fn, name in [
                (sl.take_out,             "打定"),
                (sl.hit_roll,             "打甩"),
                (sl.double_hit_gote,      "双击(后手)"),
                (sl.double_hit_init,      "双击(先手)"),
                (sl.push_in,              "传击"),
                (sl.double_push_in,       "双传进营"),
            ]:
                msg = try_tactic(fn, name)
                if msg is not None:
                    return msg

        # C2: 营内清洁 → 占中布局
        # 后手方偏好 middle_in_center(直接得分), 先手方偏好 occupy(综合占位)
        if is_gote:
            for fn, name in [
                (sl.middle_in_center,     "中路进营"),
                (sl.occupy,               "占位"),
                (sl.double_push_in_center,"双传进营中心"),
            ]:
                msg = try_tactic(fn, name)
                if msg is not None:
                    return msg
        else:
            for fn, name in [
                (sl.occupy,               "占位"),
                (sl.middle_in_center,     "中路进营"),
                (sl.double_push_in_center,"双传进营中心"),
            ]:
                msg = try_tactic(fn, name)
                if msg is not None:
                    return msg

        # C3: 最后再扫一轮 — 清除 + 得分
        for fn, name in [
            (sl.take_out,             "打定"),
            (sl.hit_roll,             "打甩"),
            (sl.middle_in_center,     "中路进营"),
            (sl.occupy,               "占位"),
        ]:
            msg = try_tactic(fn, name)
            if msg is not None:
                return msg

        # ═══════════════════════════════════════════════════════
        # 兜底
        # ═══════════════════════════════════════════════════════
        print("  [战术] 兜底 → draw to center", flush=True)
        return "BESTSHOT 3.0 0 0"

    # ── 辅助 ─────────────────────────────────────────────────────

    def _get_house_stones(self) -> list:
        """返回大本营内的壶列表 [(dist, x, y, is_own), ...]"""
        result = []
        for n in range(8):
            stone_is_init = True
            x1 = float(self.position[n * 4])
            y1 = float(self.position[n * 4 + 1])
            x2 = float(self.position[n * 4 + 2])
            y2 = float(self.position[n * 4 + 3])
            for (x, y) in [(x1, y1), (x2, y2)]:
                if abs(x) > 0.0001 or abs(y) > 0.0001:
                    dist = self.get_dist(x, y)
                    if self.is_in_house(dist):
                        is_own = (self.player_is_init == stone_is_init)
                        result.append((dist, x, y, is_own))
                stone_is_init = False
        return result

    def _fallback_shot(self) -> str:
        """战术库不可用时的简化激进策略。"""
        house = self._get_house_stones()
        if not house:
            return "BESTSHOT 3.0 0 0"

        house.sort(key=lambda s: s[0])
        _, x, y, is_own = house[0]

        if not is_own:
            # 对手最近 → 高速击打
            v0 = 3.613 - 0.12234 * y + 1.0
            h0  = x - 2.375
        elif self.my_shot_idx >= 7:
            # 我方最近 & 最后两壶 → 击打对手次近壶
            opp = [s for s in house if not s[3]]
            if opp:
                opp.sort(key=lambda s: s[0])
                _, ox, oy, _ = opp[0]
                v0 = 3.613 - 0.12234 * oy + 1.0
                h0  = ox - 2.375
            else:
                v0, h0 = 3.0, 0.0
        else:
            # 我方最近且不是末段 → 继续加壶得分
            v0, h0 = 3.0, 0.0

        v0 = max(0.0, min(6.0, v0))
        h0  = max(-2.23, min(2.23, h0))
        return f"BESTSHOT {v0:.3f} {h0:.3f} 0.000"

    # ╔════════════════════════════════════════════════════════════╗
    # ║              第 3 部分: 主消息循环 (保留)                   ║
    # ╚════════════════════════════════════════════════════════════╝

    def recv_forever(self):
        """主循环：接收消息 → 分发处理 → 直到比赛结束。"""
        retNullTime = 0
        self.on_line = True
        time0 = time.time()

        while self.on_line:
            msg_code, msg_list = self.recv_msg()

            # ── 空消息计数（服务器断连检测） ───────────────────
            if msg_code == "":
                retNullTime += 1
            if retNullTime == 5:
                break

            # ── 消息分发 ─────────────────────────────────────
            if msg_code == "CONNECTNAME":
                self.player_is_init = (msg_list[0] == "Player1")
                role = "先手(蓝)" if self.player_is_init else "后手(红)"
                print(f"玩家身份: {role}", flush=True)

            elif msg_code == "ISREADY":
                self.send_msg("READYOK")
                time.sleep(0.5)
                self.send_msg("NAME " + self.name)
                print(f"{self.name} 准备完毕！", flush=True)

            elif msg_code == "NEWGAME":
                time0 = time.time()

            elif msg_code == "SETSTATE":
                self.recv_setstate(msg_list)

            elif msg_code == "POSITION":
                for n in range(32):
                    self.position[n] = float(msg_list[n])

            elif msg_code == "GO":
                shot_msg = self.get_bestshot()       # ★ 调用激进策略
                self.send_msg(shot_msg)

            elif msg_code == "MOTIONINFO":
                for n in range(5):
                    self.motioninfo[n] = float(msg_list[n])

            elif msg_code == "CENTERLINE_VIOLATION":
                self.send_msg("CENTERLINE_CHOICE RESET")

            elif msg_code == "SCORE":
                time1 = time.time()
                self.score = int(msg_list[0])
                elapsed = time1 - time0
                time0 = time1
                if self.score > 0:
                    print(f"[得分] 我方 +{self.score}  (耗时{elapsed:.1f}s)", flush=True)
                    if self.round_total != -1:
                        self.player_is_init = True
                elif self.score < 0:
                    print(f"[得分] 对方 +{-self.score}  (耗时{elapsed:.1f}s)", flush=True)
                    if self.round_total != -1:
                        self.player_is_init = False
                else:
                    print(f"[得分] 平局  (耗时{elapsed:.1f}s)", flush=True)
                    if self.round_total != -1:
                        self.player_is_init = not self.player_is_init

            elif msg_code == "GAMEOVER":
                result_map = {"WIN": "胜利!", "LOSE": "失败", "DRAW": "平局"}
                print(f"[比赛结束] {result_map.get(msg_list[0], msg_list[0])}", flush=True)

        # ── 关闭连接 ─────────────────────────────────────────
        self.ai_sock.close()
        print("已关闭socket连接", flush=True)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                      第 4 部分: 命令行入口                           ║
# ╚══════════════════════════════════════════════════════════════════════╝

if __name__ == '__main__':
    # 命令行 key 优先，否则用默认值
    connect_key = args.key if args.key else key
    robot = AggressiveRobot(
        key=connect_key,
        name="AggressiveAI",
        host=args.host,
        port=int(args.port),
    )
    robot.recv_forever()

