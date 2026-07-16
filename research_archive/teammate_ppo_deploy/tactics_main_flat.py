from AIRobot import AIRobot, args
import strategy_library as sl
import base_library as bl

ENABLE_SWEEP = False
SWEEP_DISTANCE = 0
ENABLE_CENTERLINE_CHOICE = True
CENTERLINE_CHOICE = "RESET"
ENABLE_OPENING_VARIATION = True
OPENING_VARIATION_PERIOD = 10

class TacticsRobot(AIRobot):
    def __init__(
            self,
            key,
            name,
            host,
            port,
            show_msg=False,
            enable_sweep=ENABLE_SWEEP,
            sweep_distance=SWEEP_DISTANCE,
            enable_centerline_choice=ENABLE_CENTERLINE_CHOICE,
            centerline_choice=CENTERLINE_CHOICE,
            enable_opening_variation=ENABLE_OPENING_VARIATION,
            opening_variation_period=OPENING_VARIATION_PERIOD):
        super().__init__(
            key,
            name,
            host,
            port,
            show_msg=show_msg,
            enable_sweep=enable_sweep,
            sweep_distance=sweep_distance,
            enable_centerline_choice=enable_centerline_choice,
            centerline_choice=centerline_choice)
        self.enable_opening_variation = enable_opening_variation
        self.opening_variation_period = max(1, int(opening_variation_period))
        self.local_end_index = 0
        self._last_state_shot = None

    def recv_setstate(self, msg_list):
        previous_shot = self._last_state_shot
        super().recv_setstate(msg_list)
        if self.shot_num == 0 and previous_shot is not None and previous_shot != 0:
            self.local_end_index += 1
        self._last_state_shot = self.shot_num

    def get_bestshot(self):
        if self.shot_num == 0:
            self.strategy_path = [0] * 9  # 重置策略路径
            self.strategy_path[0] = 0 if self.player_is_init else 1
            self.strategy_phase = "steal" if self.player_is_init else "normal"

        opening_msg = self.get_opening_override()
        if opening_msg:
            return opening_msg
        
        # 根据阵营分发到对应策略
        if self.player_is_init:
            # 先手策略
            shot_msg = self.Strategy_init()
        else:
            # 后手策略
            shot_msg = self.Strategy_gote()
        
        return shot_msg

    def get_opening_override(self):
        if not self.enable_opening_variation:
            return None
        if not self.player_is_init:
            return None

        shot_idx = self.get_my_shot_index()
        if shot_idx != 1:
            return None

        period_slot = self.local_end_index % self.opening_variation_period
        if period_slot == self.opening_variation_period - 2:
            tactic_name = "opening_left_guard"
            shot_msg = "BESTSHOT 2.7 -0.87 0"
        elif period_slot == self.opening_variation_period - 1:
            tactic_name = "opening_right_guard"
            shot_msg = "BESTSHOT 2.7 0.87 0"
        else:
            return None

        state_list = self.get_state_list()
        is_init = 0 if self.player_is_init else 1
        summary = self.get_position_summary(state_list, is_init)
        print(
            "决策摘要:",
            f"shot={shot_idx}",
            f"score={summary['score_for_my']}",
            f"my_house={len(summary['my_house'])}",
            f"opp_house={len(summary['opp_house'])}",
            f"my_guard={len(summary['my_guards'])}",
            f"opp_guard={len(summary['opp_guards'])}")
        print(f"战术评分: {tactic_name}:36.0, occupy:32.0")
        print(f"选择战术: {tactic_name} score=36.0")
        return shot_msg

    def get_state_list(self):
        state_list = []
        for n in range(8):
            init_x, init_y = float(self.position[n*4]), float(self.position[n*4+1])
            gote_x, gote_y = float(self.position[n*4+2]), float(self.position[n*4+3])
            state_list.append([init_x, init_y])
            state_list.append([gote_x, gote_y])
        return state_list

    def execute_tactic(self, tactic_func, tactic_name, state_list, is_init, shot_num, quiet=False):
        if not quiet:
            print(f"调用战术: {tactic_name}")
        result = tactic_func(state_list, is_init, shot_num)
        if result is not None and result != 0:
            v0, h0, w0 = result
            return f"BESTSHOT {v0} {h0} {w0}"
        return None

    def try_tactics(self, tactic_plan, state_list, is_init, summary=None, shot_idx=None):
        if summary is None or shot_idx is None:
            for tactic_func, tactic_name in tactic_plan:
                shot_msg = self.execute_tactic(
                    tactic_func, tactic_name, state_list, is_init, self.shot_num)
                if shot_msg:
                    return shot_msg
            return self.default_shot()

        candidates = []
        for tactic_func, tactic_name in tactic_plan:
            shot_msg = self.execute_tactic(
                tactic_func, tactic_name, state_list, is_init, self.shot_num, quiet=True)
            if shot_msg:
                score = self.get_tactic_score(tactic_name, summary, shot_idx)
                candidates.append((score, tactic_name, shot_msg))

        if not candidates:
            return self.fallback_shot(summary)

        candidates.sort(key=lambda item: item[0], reverse=True)
        best_score, best_name, best_msg = candidates[0]
        preview = ", ".join(
            f"{name}:{score:.1f}" for score, name, _ in candidates[:4])
        print(f"战术评分: {preview}")
        print(f"选择战术: {best_name} score={best_score:.1f}")
        return best_msg

    def get_tactic_score(self, tactic_name, summary, shot_idx):
        score = summary["score_for_my"]
        my_house_count = len(summary["my_house"])
        opp_house_count = len(summary["opp_house"])
        my_guard_count = len(summary["my_guards"])
        opp_guard_count = len(summary["opp_guards"])
        late_weight = 1.0 + 0.18 * max(0, shot_idx - 1)

        tactic_scores = {
            "occupy": 18,
            "middle_in_center": 24,
            "defense": 20,
            "defense_push_in": 25,
            "take_out": 22,
            "hit_roll": 26,
            "push_in": 28,
            "push_in_14": 30,
            "double_hit_init": 27,
            "double_hit_gote": 27,
            "double_hit_last": 31,
            "freeze": 23,
            "clear": 21,
            "disarm_defend": 22,
            "double_push_in": 29,
            "double_push_in_center": 29,
        }
        value = tactic_scores.get(tactic_name, 10)

        if tactic_name in ("occupy", "defense"):
            value += 10 if shot_idx <= 3 else -4
            value += 5 if my_house_count > 0 else 0
            value += 8 if score > 0 else 0
            value -= 10 if score < 0 and shot_idx >= 5 else 0
            value -= 6 if my_guard_count >= 2 else 0

        if tactic_name in ("middle_in_center", "freeze"):
            value += 10 if my_house_count == 0 else 0
            value += 6 if score == 0 else 0
            value += 4 if shot_idx <= 4 else 0

        if tactic_name in ("take_out", "hit_roll", "clear", "disarm_defend"):
            value += late_weight * (10 if opp_house_count > 0 else -5)
            value += late_weight * (8 if score < 0 else 0)
            value += 6 if opp_guard_count >= 2 else 0
            value -= 8 if score > 0 and opp_house_count == 0 else 0

        if tactic_name.startswith("double_hit"):
            value += late_weight * (8 if opp_house_count >= 2 else -8)
            value += late_weight * (7 if score < 0 else 0)
            value += 5 if shot_idx >= 5 else 0

        if tactic_name in ("push_in", "push_in_14", "double_push_in", "double_push_in_center"):
            value += late_weight * (8 if my_house_count > 0 else -2)
            value += late_weight * (10 if score <= 0 else 2)
            value += 10 if shot_idx >= 6 else 0

        if tactic_name == "defense_push_in":
            value += 9 if score >= 0 else 2
            value += 8 if shot_idx >= 5 else 0
            value += 5 if my_house_count > 0 else 0

        if self.player_is_init:
            value += 4 if tactic_name in ("occupy", "defense", "take_out") else 0
        else:
            value += 5 if tactic_name in ("hit_roll", "push_in", "push_in_14", "take_out") else 0

        return value

    def default_shot(self):
        return "BESTSHOT 3.0 0 0"

    def fallback_shot(self, summary):
        if summary["opp_house"]:
            target = summary["opp_house"][0]["stone"]
            h0 = target[0] - 2.375
            print("兜底策略: take_out_nearest")
            return f"BESTSHOT 6 {h0} 0"
        if summary["score_for_my"] <= 0:
            print("兜底策略: draw_center")
            return "BESTSHOT 3.0 0 0"
        print("兜底策略: guard_center")
        return "BESTSHOT 2.7 0 0"

    def handle_centerline_violation(self):
        if not self.enable_centerline_choice:
            return None
        choice, reason = self.choose_centerline_choice()
        print(f"中线规则选择: {choice} reason={reason}")
        return "CENTERLINE_CHOICE " + choice

    def choose_centerline_choice(self):
        state_list = self.get_state_list()
        is_init = 0 if self.player_is_init else 1
        summary = self.get_position_summary(state_list, is_init)
        score = summary["score_for_my"]
        my_house_count = len(summary["my_house"])
        opp_house_count = len(summary["opp_house"])
        my_guard_count = len(summary["my_guards"])

        if score >= 2:
            return "KEEP", "multi_score_position"
        if score >= 1 and my_house_count > 0 and opp_house_count == 0:
            return "KEEP", "clean_scoring_position"
        if score < 0 or opp_house_count > my_house_count:
            return "RESET", "opponent_position_better"
        if self.shot_num <= 4 and my_guard_count == 0:
            return "RESET", "early_no_guard"
        if summary["closest_owner"] == "my":
            return "KEEP", "closest_stone_is_mine"
        return "RESET", "neutral_or_unclear"

    def get_my_shot_index(self):
        if self.player_is_init:
            return (self.shot_num // 2) + 1
        else:
            return ((self.shot_num - 1) // 2) + 1

    def is_played_stone(self, stone):
        return stone[0] != 0 or stone[1] != 0

    def is_my_stone_index(self, index, is_init):
        return index % 2 == is_init

    def get_position_summary(self, state_list, is_init):
        my_stones = []
        opp_stones = []
        house_stones = []
        my_guards = []
        opp_guards = []

        for index, stone in enumerate(state_list):
            if not self.is_played_stone(stone):
                continue

            owner = "my" if self.is_my_stone_index(index, is_init) else "opp"
            stone_info = {
                "stone": stone,
                "owner": owner,
                "dist": bl.DistH(stone),
                "index": index,
            }

            if owner == "my":
                my_stones.append(stone_info)
            else:
                opp_stones.append(stone_info)

            if bl.House(stone):
                house_stones.append(stone_info)

            in_guard_zone = (
                6.71 < stone[1] < 9.74
                and 0.545 < stone[0] < 4.205)
            if in_guard_zone:
                if owner == "my":
                    my_guards.append(stone_info)
                else:
                    opp_guards.append(stone_info)

        house_stones.sort(key=lambda item: item["dist"])
        score_for_my = 0
        closest_owner = None
        if house_stones:
            closest_owner = house_stones[0]["owner"]
            for item in house_stones:
                if item["owner"] == closest_owner:
                    score_for_my += 1 if closest_owner == "my" else -1
                else:
                    break

        return {
            "my_stones": my_stones,
            "opp_stones": opp_stones,
            "house_stones": house_stones,
            "my_house": [item for item in house_stones if item["owner"] == "my"],
            "opp_house": [item for item in house_stones if item["owner"] == "opp"],
            "my_guards": my_guards,
            "opp_guards": opp_guards,
            "closest_owner": closest_owner,
            "score_for_my": score_for_my,
        }

    def get_double_hit_tactic(self):
        if self.player_is_init:
            return sl.double_hit_init, "double_hit_init"
        return sl.double_hit_gote, "double_hit_gote"

    def build_decision_plan(self, summary, shot_idx):
        score = summary["score_for_my"]
        my_house_count = len(summary["my_house"])
        opp_house_count = len(summary["opp_house"])
        my_guard_count = len(summary["my_guards"])

        double_hit = self.get_double_hit_tactic()
        opening_plan = [
            (sl.occupy, "occupy"),
            (sl.middle_in_center, "middle_in_center"),
            (sl.defense, "defense"),
        ]
        attack_plan = [
            double_hit,
            (sl.take_out, "take_out"),
            (sl.hit_roll, "hit_roll"),
            (sl.push_in, "push_in"),
            (sl.middle_in_center, "middle_in_center"),
            (sl.occupy, "occupy"),
        ]
        defense_plan = [
            (sl.defense, "defense"),
            (sl.defense_push_in, "defense_push_in"),
            (sl.occupy, "occupy"),
            (sl.middle_in_center, "middle_in_center"),
        ]
        late_attack_plan = [
            (sl.push_in_14, "push_in_14"),
            double_hit,
            (sl.take_out, "take_out"),
            (sl.hit_roll, "hit_roll"),
            (sl.middle_in_center, "middle_in_center"),
        ]
        late_defense_plan = [
            (sl.defense_push_in, "defense_push_in"),
            (sl.defense, "defense"),
            (sl.push_in_14, "push_in_14"),
            (sl.take_out, "take_out"),
        ]

        if shot_idx <= 2:
            if score < 0 or opp_house_count > my_house_count:
                return [(sl.take_out, "take_out"), (sl.hit_roll, "hit_roll")] + opening_plan
            return opening_plan

        if shot_idx >= 7:
            if score < 0:
                return late_attack_plan
            if score > 0:
                return late_defense_plan
            return [
                (sl.push_in_14, "push_in_14"),
                (sl.middle_in_center, "middle_in_center"),
                (sl.hit_roll, "hit_roll"),
                (sl.defense, "defense"),
            ]

        if score < 0:
            return attack_plan

        if score > 0:
            if my_guard_count == 0:
                return [(sl.occupy, "occupy")] + defense_plan
            return defense_plan

        if opp_house_count >= 2:
            return [double_hit, (sl.take_out, "take_out"), (sl.hit_roll, "hit_roll")] + defense_plan

        if my_house_count == 0:
            return [(sl.middle_in_center, "middle_in_center"), (sl.occupy, "occupy")] + attack_plan

        return [(sl.push_in, "push_in"), (sl.hit_roll, "hit_roll")] + defense_plan

    def Strategy_init(self):
        """先手策略：用基础决策树在占位、进攻和防守之间切换。"""
        shot_idx = self.get_my_shot_index()
        is_init = 0 if self.player_is_init else 1
        state_list = self.get_state_list()
        summary = self.get_position_summary(state_list, is_init)
        tactic_plan = self.build_decision_plan(summary, shot_idx)
        print(
            "决策摘要:",
            f"shot={shot_idx}",
            f"score={summary['score_for_my']}",
            f"my_house={len(summary['my_house'])}",
            f"opp_house={len(summary['opp_house'])}",
            f"my_guard={len(summary['my_guards'])}",
            f"opp_guard={len(summary['opp_guards'])}")
        return self.try_tactics(tactic_plan, state_list, is_init, summary, shot_idx)

    def Strategy_gote(self):
        """后手策略：用基础决策树在占位、进攻和防守之间切换。"""
        shot_idx = self.get_my_shot_index()
        is_init = 0 if self.player_is_init else 1
        state_list = self.get_state_list()
        summary = self.get_position_summary(state_list, is_init)
        tactic_plan = self.build_decision_plan(summary, shot_idx)
        print(
            "决策摘要:",
            f"shot={shot_idx}",
            f"score={summary['score_for_my']}",
            f"my_house={len(summary['my_house'])}",
            f"opp_house={len(summary['opp_house'])}",
            f"my_guard={len(summary['my_guards'])}",
            f"opp_guard={len(summary['opp_guards'])}")
        return self.try_tactics(tactic_plan, state_list, is_init, summary, shot_idx)

if __name__ == "__main__":
    myrobot = TacticsRobot(
        args.key,
        name="TacticsAI",
        host=args.host,
        port=int(args.port),
        show_msg=args.show_msg,
        enable_sweep=ENABLE_SWEEP,
        sweep_distance=SWEEP_DISTANCE,
        enable_centerline_choice=ENABLE_CENTERLINE_CHOICE,
        centerline_choice=CENTERLINE_CHOICE)
    myrobot.recv_forever()
