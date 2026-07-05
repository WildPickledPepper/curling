from AIRobot import AIRobot
import strategy_library as sl

class TacticsRobot(AIRobot):
    def __init__(self, key, name, host, port):
        super().__init__(key, name, host, port)

    def get_bestshot(self):
        if self.shot_num == 0:
            self.strategy_path = [0] * 9  # 重置策略路径
            self.strategy_path[0] = 0 if self.player_is_init else 1
            self.strategy_phase = "steal" if self.player_is_init else "normal"
        
        # 根据阵营分发到对应策略
        if self.player_is_init:
            # 先手策略
            shot_msg = self.Strategy_init()
        else:
            # 后手策略
            shot_msg = self.Strategy_gote()
        
        return shot_msg

    def get_state_list(self):
        state_list = []
        for n in range(8):
            init_x, init_y = float(self.position[n*4]), float(self.position[n*4+1])
            gote_x, gote_y = float(self.position[n*4+2]), float(self.position[n*4+3])
            state_list.append([init_x, init_y])
            state_list.append([gote_x, gote_y])
        return state_list

    def execute_tactic(self, tactic_func, tactic_name, state_list, is_init, shot_num):
        print(f"调用战术: {tactic_name}")
        result = tactic_func(state_list, is_init, shot_num)
        if result is not None and result != 0:
            v0, h0, w0 = result
            return f"BESTSHOT {v0} {h0} {w0}"
        return None

    def default_shot(self):
        return "BESTSHOT 3.0 0 0"

    def get_my_shot_index(self):
        if self.player_is_init:
            return (self.shot_num // 2) + 1
        else:
            return ((self.shot_num - 1) // 2) + 1


    def Strategy_init(self):
        """先手专属策略：基于策略树的动态决策，主打开局占位、稳健铺垫、中盘守势保分"""
        shot_idx = self.get_my_shot_index()
        is_init = 0 if self.player_is_init else 1
        state_list = self.get_state_list()

        def select_strategy():
            if shot_idx == 1:
                result = self.execute_tactic(sl.occupy, "occupy", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 2:
                result = self.execute_tactic(sl.occupy, "occupy", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 3:
                result = "BESTSHOT 3.0 0.5 0"
                return result if result else self.default_shot()
            elif shot_idx == 4:
                result = self.execute_tactic(sl.hit_roll, "hit_roll", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 5:
                result = "BESTSHOT 2.8 0.7 0"
                return result if result else self.default_shot()
            elif shot_idx == 6:
                result = self.execute_tactic(sl.push_in, "push_in", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 7:
                result = self.execute_tactic(sl.defense_push_in, "defense_push_in", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 8:
                result = self.execute_tactic(sl.push_in_14, "push_in_14", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
        return select_strategy()

    def Strategy_gote(self):
        """后手专属策略：主打后发制人、中盘传击清壶、末轮反击翻盘"""
        shot_idx = self.get_my_shot_index()
        is_init = 0 if self.player_is_init else 1
        state_list = self.get_state_list()

        def select_strategy():
            if shot_idx == 1:
                result = self.execute_tactic(sl.occupy, "occupy", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 2:
                result = "BESTSHOT 2.8 -0.5 0"
                return result if result else self.default_shot()
            elif shot_idx == 3:
                result = self.execute_tactic(sl.hit_roll, "hit_roll", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 4:
                result = self.execute_tactic(sl.double_hit_gote, "double_hit_gote", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 5:
                result = self.execute_tactic(sl.defense, "defense", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 6:
                result = "BESTSHOT 2.8 1.0 0"
                return result if result else self.default_shot()
            elif shot_idx == 7:
                result = self.execute_tactic(sl.push_in, "push_in", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
            elif shot_idx == 8:
                result = self.execute_tactic(sl.push_in_14, "push_in_14", state_list, is_init, self.shot_num)
                return result if result else self.default_shot()
        return select_strategy()

if __name__ == "__main__":
    key = "lidandan_b73e5f80-45a4-4b0d-9fbc-d76e4e6579a2"
    myrobot = TacticsRobot(key, name="TacticsAI", host="curling-server-7788.jupyterhub.svc.cluster.local", port=7788)
    myrobot.recv_forever()