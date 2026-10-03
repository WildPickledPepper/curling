from typing import List, Union

import numpy as np

# from base_library import Stone_R
# import base_library as bl
# from base_library import flag,score,Stone_R,House_R
import base_library as bl
from base_library import Stone_R,flag,shot_num

# 类型别名
Coordinate = List[float]
StateList = List[Coordinate]
StrategyResult = Union[List[Union[int, float]], int]


def clear(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """炸球策略 - 清除聚集的对方壶。

    检测场上是否有3个或以上横坐标接近的壶聚集，计算击打位置以清除这些壶。

    Args:
        state_list: 所有壶的坐标列表，每个元素为[x, y]格式的坐标。
        is_init: 先后手标识，0表示我方先手，1表示后手（此策略不使用）。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果找到可清除的目标，返回[v0, h0, 0]格式的击打参数列表；
        否则返回None表示策略不可行。其中v0为速度，h0为横向偏移量。

    Examples:
        >>> result = clear([[2.5, 6.0], [2.6, 6.5], [2.7, 7.0]])
        >>> print(result)  # [6, 0.142, 0] 或 0
    """
    c=0
    _list=[]
    state_list=sorted(state_list,key=lambda x:x[1],reverse=True)
    state_list=[state_list[i]for i in range(len(state_list))if state_list[i][0]!=0 and state_list[i][1]!=0]
    if len(state_list)<3:
        return None
    for i in range(len(state_list)):
        t=[]
        for j in range(len(state_list)):
            if abs(state_list[i][0]-state_list[j][0])<2*Stone_R :
                t.append(state_list[j])
        if len(t)>=3:
            for k in range(len(t)):
                _list.append(t[k])
            break
    if len(_list)<3:
        return None
    else:
        _list=sorted(_list,key=lambda x:x[1],reverse=True)
        v0 = np.array(_list[2]) - np.array(_list[1])  # 标准向量指向中心
        if v0[0] == 0:
            return None
        angle1 = np.arctan2(abs(v0[1]), abs(v0[0]))
        multiple = 2 * Stone_R / np.sqrt(v0[0] ** 2 + v0[1] ** 2)
        point_x = _list[1][0] - multiple * v0[0]
        point_y = _list[1][1] - multiple * v0[1]
        v = np.array([point_x, point_y]) - np.array(_list[0])
        if v[0] == 0:
            return None
        angle2 = np.arctan2(abs(v[1]), abs(v[0]))
        h_offset = _list[0][0] - 2.375
        if not np.isnan(h_offset):
            return [6, h_offset + 0.017, 0]
        else:
            return None


def middle_in_center(state_list: StateList, is_init: int, shot_num: int = shot_num) -> StrategyResult:
    """中路进营策略 - 将己方壶打入大本营中心。

    分析场上局势，选择合适的己方壶将其打入大本营中心区域得分。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果策略可行，返回[v0, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = middle_in_center([[2.4, 5.0], [2.5, 5.5]], 0)
        >>> print(result)  # [3.5, 0.05, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])
    in_center=False
    for i in range(len(state_list)):
        if bl.DistH(state_list[i])<0.4:
            in_center=True
    target = []
    if in_center==False:
        for i in range(len(state_me)):
            if state_me[i][1]<4.88+0.61:
                continue
            if -3*Stone_R>state_me[i][0]-2.375 or state_me[i][0]-2.375>3*Stone_R:
               continue
            if bl.Roadjudge(state_me[i], [state_me[i][0], 10.61], state_list)and bl.Roadjudge(state_me[i], [state_me[i][0], 4.88], state_list):
                target.append(state_me[i])
    if len(target)!=0:
        d=[]
        for i in range(len(target)):
           d.append(target[i][1]-4.88)
        t=np.argmin(d)
        vt = bl.d_v(target[t][1]-4.88)
        d = bl.v_d(vt)
        v =  np.polyval(bl.an, target[t][1])#修正
        v0 = bl.d_v(d + (27.6 + 4.88 - target[t][1])) + v
        h0=target[t][0]-2.375
        if v0<4:
            h0+=0.024
        return [v0,h0,0]
    else:
        return None   #不可行



def double_hit_init(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """双飞先手策略 - 先手情况下的双飞击打。

    在先手情况下，寻找合适的两个对方壶进行双飞击打。

    Args:
        state_list: 所有壶的坐标列表（内部会自动分离对方壶和己方壶）。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果策略可行，返回[6, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = double_hit_init([[2.5, 6.0], [2.6, 6.5], [2.4, 7.0], [2.5, 7.5]])
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])

    state_list_enemy = [i for i in state_enemy if i[0] != 0 and i[1] != 0]
    out_s = bl.NearestTarget(state_list_enemy)  # 升序
    n = len(out_s)  # 目前场上对手壶的个数
    for i in range(n - 1):
        d = bl.Dist(out_s[0], out_s[i + 1])
        if (out_s[i + 1][1] > out_s[0][1] or (
                out_s[i + 1][1] > 4.88 - 1.22 and bl.DistH(out_s[i]) < 1.83 + 1.8 * Stone_R)) and bl.DistH(
                out_s[0]) < 1.22:
            if d > 2 * np.sqrt(2) * Stone_R:
                D = np.sqrt(d ** 2 - (2 * Stone_R) ** 2)  # 辅瞄壶与最终击打壶的距离
                theta = np.arcsin(2 * Stone_R / d)
                vec1 = [out_s[i + 1][0] - out_s[0][0], out_s[i + 1][1] - out_s[0][1]]
                vec2 = [out_s[i + 1][0] - out_s[0][0], 0]
                vec1_norm = np.linalg.norm(vec1)
                vec2_norm = np.linalg.norm(vec2)
                if vec1_norm < 1e-8 or vec2_norm < 1e-8:
                    continue
                cos_alpha = np.dot(vec1, vec2) / vec1_norm / vec2_norm
                cos_alpha = np.clip(cos_alpha, -1.0, 1.0)
                alpha = np.arccos(cos_alpha)
                angle = theta + alpha
                delta_x = D * np.cos(angle)
                delta_y = D * np.sin(angle)
            else:
                theta = np.arccos(d / 4 / Stone_R)
                vec1 = [out_s[i + 1][0] - out_s[0][0], out_s[i + 1][1] - out_s[0][1]]
                vec2 = [out_s[i + 1][0] - out_s[0][0], 0]
                vec1_norm = np.linalg.norm(vec1)
                vec2_norm = np.linalg.norm(vec2)
                if vec1_norm < 1e-8 or vec2_norm < 1e-8:
                    continue
                cos_alpha = np.dot(vec1, vec2) / vec1_norm / vec2_norm
                cos_alpha = np.clip(cos_alpha, -1.0, 1.0)
                alpha = np.arccos(cos_alpha)
                angle = theta + alpha
                delta_x = 2 * Stone_R * np.cos(angle)
                delta_y = 2 * Stone_R * np.sin(angle)
            if angle < 25 * np.pi / 180 and d > 1.22:
                continue
            if d > 2.6 and angle < 50 * np.pi / 180:
                continue
            if d > 1.22 + 1.83 and 75 * np.pi / 180 > angle >= 50 * np.pi / 180:
                continue
            if vec2[0] != 0 and angle <= 75 * np.pi / 180:
                if vec1[0] > 0 and vec1[1] > 0:  # 所判断的球在中心球右下
                    point = [out_s[0][0] + delta_x, out_s[0][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
                if vec1[0] > 0 and vec1[1] < 0:  # 右上
                    point = [out_s[i + 1][0] - delta_x, out_s[0][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
                if vec1[0] < 0 and vec1[1] > 0:  # 左下
                    point = [out_s[0][0] - delta_x, out_s[0][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
                if vec1[0] < 0 and vec1[1] < 0:  # 左上
                    point = [out_s[i + 1][0] + delta_x, out_s[i + 1][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
    return None  # 双飞策略无法实现
    #双飞策略无法实现


def double_hit_gote(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """双飞后手策略 - 后手情况下的双飞击打。

    在后手情况下，寻找合适的两个对方壶进行双飞击打。

    Args:
        state_list: 所有壶的坐标列表（内部会自动分离对方壶和己方壶）。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果策略可行，返回[6, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = double_hit_gote([[2.5, 6.0], [2.6, 6.5], [2.4, 7.0], [2.5, 7.5]])
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])

    state_list_enemy = [i for i in state_enemy if i[0] != 0 and i[1] != 0]
    out_s = bl.NearestTarget(state_list_enemy)  # 升序
    n = len(out_s)  # 目前场上对手壶的个数
    for i in range(n - 1):
        d = bl.Dist(out_s[0], out_s[i + 1])
        if out_s[i + 1][1] > out_s[0][1] or (
                out_s[i + 1][1] > 4.88 - 1.22 and bl.DistH(out_s[i]) < 1.83 + 1.8 * Stone_R):
            if d > 2 * np.sqrt(2) * Stone_R:
                D = np.sqrt(d ** 2 - (2 * Stone_R) ** 2)  # 辅瞄壶与最终击打壶的距离
                theta = np.arcsin(2 * Stone_R / d)
                vec1 = [out_s[i + 1][0] - out_s[0][0], out_s[i + 1][1] - out_s[0][1]]
                vec2 = [out_s[i + 1][0] - out_s[0][0], 0]
                alpha = np.arctan2(abs(vec1[1]), abs(vec1[0]))
                angle = theta + alpha
                delta_x = D * np.cos(angle)
                delta_y = D * np.sin(angle)
            else:
                theta = np.arccos(d / 4 / Stone_R)
                vec1 = [out_s[i + 1][0] - out_s[0][0], out_s[i + 1][1] - out_s[0][1]]
                vec2 = [out_s[i + 1][0] - out_s[0][0], 0]
                alpha = np.arctan2(abs(vec1[1]), abs(vec1[0]))
                angle = theta + alpha
                delta_x = 2 * Stone_R * np.cos(angle)
                delta_y = 2 * Stone_R * np.sin(angle)
            if angle < 25 * np.pi / 180 and d > 1.22:
                continue
            if d > 2.6 and angle < 50 * np.pi / 180:
                continue
            if d > 1.22 + 1.83 and 75 * np.pi / 180 > angle >= 50 * np.pi / 180:
                continue
            if vec2[0] != 0 and angle <= 75 * np.pi / 180:
                if vec1[0] > 0 and vec1[1] > 0:  # 所判断的球在中心球右下
                    point = [out_s[0][0] + delta_x, out_s[0][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
                if vec1[0] > 0 and vec1[1] < 0:  # 右上
                    point = [out_s[i + 1][0] - delta_x, out_s[0][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
                if vec1[0] < 0 and vec1[1] > 0:  # 左下
                    point = [out_s[0][0] - delta_x, out_s[0][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
                if vec1[0] < 0 and vec1[1] < 0:  # 左上
                    point = [out_s[i + 1][0] + delta_x, out_s[i + 1][1] + delta_y]
                    a = [point[0], 10.61]  # 发球点
                    if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                        h = point[0] - 2.375  # 偏移量
                        if point[0] - out_s[i + 1][0] > 0:
                            x0 = 0.017
                        else:
                            x0 = 0.033
                        return [6, h + x0, 0]
    return None  # 双飞策略无法实现


def double_hit_last(state_list: StateList, is_init: int = flag, shot_num: int = 14) -> StrategyResult:
    """最后一球的双飞策略 - 处理最后一投的双飞击打。

    在最后一投时，寻找合适的两个对方壶进行双飞击打以获取优势。

    Args:
        state_list: 所有壶的坐标列表（内部会自动分离对方壶和己方壶）。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号，默认为14（最后一球）。

    Returns:
        如果策略可行，返回[6, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = double_hit_last([[2.5, 6.0], [2.6, 6.5], [2.4, 7.0], [2.5, 7.5]])
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])

    state_list_enemy = [i for i in state_enemy if i[0] != 0 and i[1] != 0]
    state_list_filtered = [i for i in state_list if i[0] != 0 and i[1] != 0]
    out_s = bl.NearestTarget(state_list_enemy)  # 升序
    if len(out_s) != 0:
        state_list_filtered = [i for i in state_list_filtered if i[0] != 0 and i[1] != 0]
        state_list_filtered = [i for i in state_list_filtered if i != out_s[0]]
        n = len(state_list_filtered)  # 目前场上对手壶的个数
        for i in range(n):
            d = bl.Dist(out_s[0], state_list_filtered[i])
            if (state_list_filtered[i][1] > out_s[0][1] or (state_list_filtered[i][1] > 4.88 - 1.22 and bl.DistH(
                    state_list_filtered[i]) < 1.83 + 1.8 * Stone_R)) and bl.DistH(out_s[0]) < 1.22:
                if d > 2 * np.sqrt(2) * Stone_R:
                    D = np.sqrt(d ** 2 - (2 * Stone_R) ** 2)  # 辅瞄壶与最终击打壶的距离
                    theta = np.arcsin(2 * Stone_R / d)
                    vec1 = [state_list_filtered[i][0] - out_s[0][0], state_list_filtered[i][1] - out_s[0][1]]
                    vec2 = [state_list_filtered[i][0] - out_s[0][0], 0]
                    alpha = np.arctan2(abs(vec1[1]), abs(vec1[0]))
                    angle = theta + alpha
                    delta_x = D * np.cos(angle)
                    delta_y = D * np.sin(angle)
                else:
                    theta = np.arccos(d / 4 / Stone_R)
                    vec1 = [state_list_filtered[i][0] - out_s[0][0], state_list_filtered[i][1] - out_s[0][1]]
                    vec2 = [state_list_filtered[i][0] - out_s[0][0], 0]
                    alpha = np.arctan2(abs(vec1[1]), abs(vec1[0]))
                    angle = theta + alpha
                    delta_x = 2 * Stone_R * np.cos(angle)
                    delta_y = 2 * Stone_R * np.sin(angle)
                if angle < 25 * np.pi / 180 and d > 1.22:
                    continue
                if d > 2.6 and angle < 50 * np.pi / 180:
                    continue
                if d > 1.22 + 1.83 and 75 * np.pi / 180 > angle >= 50 * np.pi / 180:
                    continue
                if vec2[0] != 0 and angle <= 75 * np.pi / 180:
                    if vec1[0] > 0 and vec1[1] > 0:  # 所判断的球在中心球右下
                        point = [out_s[0][0] + delta_x, out_s[0][1] + delta_y]
                        a = [point[0], 10.61]  # 发球点
                        if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                            h = point[0] - 2.375  # 偏移量
                            if point[0] - state_list_filtered[i][0] > 0:
                                x0 = 0.017
                            else:
                                x0 = 0.033
                            return [6, h + x0, 0]
                    if vec1[0] > 0 and vec1[1] < 0:  # 右上
                        point = [state_list_filtered[i][0] - delta_x, out_s[0][1] + delta_y]
                        a = [point[0], 10.61]  # 发球点
                        if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                            h = point[0] - 2.375  # 偏移量
                            if point[0] - state_list_filtered[i][0] > 0:
                                x0 = 0.017
                            else:
                                x0 = 0.033
                            return [6, h + x0, 0]
                    if vec1[0] < 0 and vec1[1] > 0:  # 左下
                        point = [out_s[0][0] - delta_x, out_s[0][1] + delta_y]
                        a = [point[0], 10.61]  # 发球点
                        if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                            h = point[0] - 2.375  # 偏移量
                            if point[0] - state_list_filtered[i][0] > 0:
                                x0 = 0.017
                            else:
                                x0 = 0.033
                            return [6, h + x0, 0]
                    if vec1[0] < 0 and vec1[1] < 0:  # 左上
                        point = [state_list_filtered[i][0] + delta_x, state_list_filtered[i][1] + delta_y]
                        a = [point[0], 10.61]  # 发球点
                        if bl.Roadjudge(point, out_s[0], state_list) and bl.Roadjudge(point, a, state_list):
                            h = point[0] - 2.375  # 偏移量
                            if point[0] - state_list_filtered[i][0] > 0:
                                x0 = 0.017
                            else:
                                x0 = 0.033
                            return [6, h + x0, 0]
    return None  # 双飞策略无法实现


def freeze(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """粘球策略 - 将己方壶紧贴对方壶以获得优势。

    通过精确控制速度和位置，将己方壶紧贴对方壶，使对方难以清除。

    Args:
        state_list: 所有壶的坐标列表（内部会自动分离对方壶和己方壶）。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[v0, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = freeze([[2.5, 6.0], [2.4, 7.0]], 0, 10)
        >>> print(result)  # [2.5, 0.1, 0] 或 0
    """
    state_enemy = []
    state_me = []
    print(shot_num)
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            print(i)
            state_me.append(state_list[2 * i + 1])

    y_up = 4.88
    enemy_s = bl.NearestTarget(state_enemy)
    enemy_s = [i for i in enemy_s if i[0] != 0 and i[1] != 0]
    s = bl.NearestTarget(state_list)
    state_me_sorted = bl.NearestTarget(state_me)
    for i in enemy_s:
        vec1 = [i[0] - 2.375, i[1] - 4.88]
        vec2 = [i[0] - 2.375, 0]
        theta = np.arctan2(abs(vec1[1]), abs(vec1[0]))
        d = bl.DistH(i)
        if theta < 40 * np.pi / 180 and d > 1.22:
            continue
        if bl.Roadjudge(i, [2.375, 4.88], state_list) or (
                bl.Roadjudge(i, state_me_sorted[0], state_list) and bl.DistH(state_me_sorted[0]) < 0.61):
            if bl.Roadjudge(i, [i[0], 10.61], state_list) and bl.Roadjudge(i, [i[0], i[1] - 2.2 * Stone_R],
                                                                           state_me) and i[1] >= y_up and 0.545 < i[
                0] < 4.205:
                if shot_num == 14:
                    if enemy_s[0] == s[0]:
                        if bl.DistH(i) < 1.83:
                            return [bl.y2v(i[1]), i[0] - 2.375, 0]
                    else:
                        return [bl.y2v(i[1]), i[0] - 2.375, 0]
                else:
                    return [bl.y2v(i[1]), i[0] - 2.375, 0]
    return None

def defense(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """防守策略 - 保护己方优势壶或阻碍对方得分。

    根据场上局势，选择放置保护壶或粘球等防守手段。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[v0, h0, 0]格式的击打参数；
        否则返回None表示不需要防守。

    Examples:
        >>> result = defense([[2.4, 5.0], [2.5, 5.5]], 0, 10)
        >>> print(result)  # [2.7, 0.05, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])
    out_s = bl.NearestTarget(state_me)
    enemy_s = bl.NearestTarget(state_enemy)
    out_s = [i for i in out_s if i[0]!=0 and i[1]!=0]
    enemy_s = [i for i in enemy_s if i[0]!=0 and i[1]!=0]
    if len(out_s)!=0 and len(enemy_s)!=0:
        if bl.DistH(out_s[0]) < bl.DistH(enemy_s[0]) and bl.DistH(out_s[0])<1.22:    #中心得分壶为我方壶
            if bl.Roadjudge(out_s[0],[out_s[0][0],10.61],state_list):      #判断路径是否可行，若可行，即没有壶保护可以被直接击打到
                if shot_num != 14:
                    return [2.7,out_s[0][0]-2.375,0]                  #做一个保护壶
                else:
                    return [bl.y2v(out_s[0][1]),out_s[0][0]-2.375,0]
            else:          #若有壶保护
                if bl.Roadjudge(out_s[0],[out_s[0][0],10.61],state_enemy) == False and bl.Roadjudge(out_s[0],[out_s[0][0],10.61],state_me):    #障碍壶是敌方的且没有我方障碍壶
                    point = bl.Roadjudge_state(out_s[0],[out_s[0][0],10.61],state_enemy)    #直接粘一颗壶在对方壶上
                    return [bl.y2v(point[1]),out_s[0][0]-2.375,0]               #粘球
    return None        #不需要防守
def defense_push_in(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """防守对方传击进攻策略 - 阻止对方通过传击得分。

    在敌方球和我方中心壶连线中点放置保护壶，防止对方传击。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果策略可行，返回[v0, h0, 0]格式的击打参数；
        否则返回None表示不需要此防守。

    Examples:
        >>> result = defense_push_in([[2.4, 5.0], [2.5, 5.5]], 0, 10)
        >>> print(result)  # [2.3, 0.05, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])
    out_s = bl.NearestTarget(state_me)
    enemy_s = bl.NearestTarget(state_enemy)
    out_s = [i for i in out_s if i[0]!=0 and i[1]!=0]
    enemy_s = [i for i in enemy_s if i[0]!=0 and i[1]!=0]
    if not out_s or not enemy_s:
        return None
    for i in enemy_s:
        vec1 = [i[0]-out_s[0][0],i[1]-out_s[0][1]]
        vec2 = [i[0]-out_s[0][0],0]
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 < 1e-8 or norm2 < 1e-8:
            continue
        cos_theta = np.dot(vec1, vec2) / norm1 / norm2
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        theta = np.arccos(cos_theta)
        if bl.Roadjudge(i,[i[0],i[1]+2.2*Stone_R],state_me) and i[1]<8:
            if 2*np.pi/9< theta <np.pi/2 and vec1[1] > 0:
                if bl.DistH(out_s[0])<0.61:
                    point = [(i[0]+out_s[0][0])/2,(i[1]+out_s[0][1])/2]           #在敌方球和我方中心壶连线的中点上放一颗保护壶
                    if bl.Roadjudge(i,out_s[0],state_list) and bl.Roadjudge(i,[i[0],10.61],state_list):
                        if bl.Roadjudge(point,[point[0],10.61],state_list) and bl.LocalJudge(point,state_list):
                            return [bl.y2v(point[1])-0.01,point[0]-2.375,0]
                else:
                    point = [(i[0]+2.375)/2,(i[1]+4.88)/2]           #在敌方球和中心连线的中点上放一颗保护壶
                    if bl.Roadjudge(i,[2.375,4.88],state_list) and bl.Roadjudge(i,[i[0],10.61],state_list):
                        if bl.Roadjudge(point,[point[0],10.61],state_list) and bl.LocalJudge(point,state_list):
                            return [bl.y2v(point[1])-0.01,point[0]-2.375,0]
    return None

def _active_stones(state_list: StateList) -> StateList:
    return [stone for stone in state_list if stone[0] != 0 or stone[1] != 0]


def _free_draw_to_point(state_list: StateList, point: Coordinate, velocity: float = None) -> StrategyResult:
    stones = _active_stones(state_list)
    local_ok = True if not stones else bool(bl.LocalJudge(point, stones))
    if local_ok and bl.Roadjudge(point, [point[0], 10.61], stones):
        v0 = velocity if velocity is not None else bl.y2v(point[1])
        return [v0, point[0] - 2.375, 0]
    return None


def _split_stones(state_list: StateList, is_init: int):
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])
    return state_enemy, state_me


def _is_active(stone: Coordinate) -> bool:
    return stone[0] != 0 or stone[1] != 0


def _is_guard(stone: Coordinate) -> bool:
    return _is_active(stone) and 6.71 < stone[1] < 9.74 and 0.545 < stone[0] < 4.205


# The four promoted bypass releases use fixed (v, w) pairs.  These quartic
# fits reproduce their recovered no-contact trajectories on y=4.70..10.80;
# h is a pure horizontal translation.  Keeping the fits here avoids making
# the deployable tactic library depend on the local PhysX package.
_BYPASS_CURVE_COEFFICIENTS = {
    9.0: (-4.3615015504337583e-08, 1.3355878401676497e-05, 0.00038091152483873676, -0.06760984687699306, 3.7031086743170536),
    -9.0: (4.3615015427169256e-08, -1.335587839925585e-05, -0.0003809115248665006, 0.06760984687712897, 0.9980913256827108),
    8.0: (0.0002086431205502171, -0.007083234062023531, 0.08995310995516775, -0.5668030279245925, 4.96023033714188),
    -8.0: (-0.00020864312055021583, 0.007083234062023397, -0.08995310995516496, 0.5668030279245718, -0.25903033714183854),
}
_BYPASS_PATH_CLEARANCE = 2.0 * Stone_R + 0.045
_BYPASS_TARGET_Y_MIN = 4.70
_BYPASS_TARGET_Y_MAX = 5.85
_BYPASS_GUARD_Y_MIN = 6.71
_BYPASS_GUARD_Y_MAX = 9.74
_BYPASS_GUARD_OFFSET_MIN = 0.20
_BYPASS_GUARD_OFFSET_MAX = 1.10


def _calibrated_bypass_x(y_value: float, h0: float, w0: float) -> float:
    coefficients = _BYPASS_CURVE_COEFFICIENTS.get(float(w0))
    if coefficients is None:
        raise ValueError(f"unsupported calibrated bypass rotation: {w0}")
    return float(np.polyval(coefficients, y_value) + h0)


def _bypass_path_is_clear(
    state_list: StateList,
    shot: StrategyResult,
    excluded: List[Coordinate],
    *,
    min_y: float,
) -> bool:
    """Reject extra stones that intersect the calibrated inbound curl lane."""
    if shot is None or shot == 0:
        return False
    _, h0, w0 = shot
    for stone in state_list:
        if not _is_active(stone) or any(stone is ignored for ignored in excluded):
            continue
        if not min_y <= stone[1] <= 10.80:
            continue
        curve_x = _calibrated_bypass_x(stone[1], float(h0), float(w0))
        if abs(stone[0] - curve_x) < _BYPASS_PATH_CLEARANCE:
            return False
    return True


def _bypass_path_blocked(
    state_list: StateList,
    shot: StrategyResult,
    excluded: List[Coordinate],
    *,
    min_y: float,
) -> bool:
    """Return whether an active stone intersects a calibrated inbound lane."""
    return not _bypass_path_is_clear(state_list, shot, excluded, min_y=min_y)


def _bypass_guard_side_margin(guard: Coordinate, shot: StrategyResult, side: int) -> float:
    """Return signed clearance between a named guard and a calibrated curl."""
    if shot is None or shot == 0:
        return -np.inf
    _, h0, w0 = shot
    curve_x = _calibrated_bypass_x(guard[1], float(h0), float(w0))
    return float(side * (curve_x - guard[0]))


def _direct_hit_target(
    state_list: StateList,
    state_me: StateList,
    target: Coordinate,
    velocity: float = 6.0,
) -> StrategyResult:
    if not _is_active(target):
        return None
    if bl.Roadjudge(target, [target[0], 10.61], state_list) and bl.Roadjudge(
        target, [target[0], 3.05], state_me
    ):
        return [velocity, target[0] - 2.375, 0]

    d = Stone_R
    state_list_filtered = [stone for stone in state_list if stone != target]
    for h in np.arange(-d, d, 0.01):
        offset_target = [target[0] + h, target[1]]
        if bl.Roadjudge(offset_target, [offset_target[0], 10.61], state_list_filtered):
            correction = 0.033 if h < 0 else 0.017
            return [velocity, target[0] + h - 2.375 + correction, 0]
    return None


def _hit_nearest_target(
    state_list: StateList,
    is_init: int,
    predicate,
    velocity: float = 6.0,
) -> StrategyResult:
    state_enemy, state_me = _split_stones(state_list, is_init)
    targets = [stone for stone in state_enemy if _is_active(stone) and predicate(stone)]
    targets = sorted(targets, key=lambda stone: bl.DistH(stone))
    for target in targets:
        result = _direct_hit_target(state_list, state_me, target, velocity=velocity)
        if result is not None:
            return result
    return None


def _blocked_house_target_pairs(
    state_list: StateList,
    is_init: int,
    target: Coordinate = None,
):
    """Return target/guard pairs that can require a last-shot bypass."""
    state_enemy, _ = _split_stones(state_list, is_init)
    house_targets = [stone for stone in state_enemy if _is_active(stone) and bl.House(stone)]
    if target is not None:
        house_targets = [stone for stone in house_targets if stone is target or stone == target]
    house_targets.sort(key=bl.DistH)
    guards = [stone for stone in state_list if _is_guard(stone)]
    for target in house_targets:
        for guard in sorted(guards, key=lambda stone: -stone[1]):
            lateral_offset = guard[0] - target[0]
            if (
                guard[1] > target[1]
                and _BYPASS_GUARD_OFFSET_MIN <= abs(lateral_offset) <= _BYPASS_GUARD_OFFSET_MAX
            ):
                yield target, guard


def _blocked_house_target(state_list: StateList, is_init: int):
    """Return the best legacy target/guard pair, if a bypass pair exists."""
    return next(_blocked_house_target_pairs(state_list, is_init), None)


def _around_guard_takeout(
    state_list: StateList,
    is_init: int,
    side: int,
    shot_num: int,
) -> StrategyResult:
    """Use a calibrated late-end curl to take shot rock behind an offset guard.

    The parameters below were verified in the strict local PhysX corpus.  They
    are deliberately not a generic curl solver: a centred guard cannot be
    bypassed and then hit squarely with one monotonic curl.  Returning ``None``
    outside this narrow geometry lets the action mask reject the tactic.
    """
    return _around_guard_takeout_detail(state_list, is_init, side, shot_num)["shot"]


def _around_guard_takeout_detail(
    state_list: StateList,
    is_init: int,
    side: int,
    shot_num: int,
    target: Coordinate = None,
) -> dict:
    """Solve one takeout route and retain its rejection reason for telemetry."""
    detail = {"available": False, "reason": "unknown", "shot": None, "target": None, "guard": None}
    if shot_num < 12:
        detail["reason"] = "early_end"
        return detail
    pairs = list(_blocked_house_target_pairs(state_list, is_init, target))
    if not pairs:
        detail["reason"] = "no_blocked_house_target"
        return detail

    saw_geometry = False
    saw_side = False
    for candidate_target, guard in pairs:
        lateral_offset = guard[0] - candidate_target[0]
        if not (
            _BYPASS_TARGET_Y_MIN <= candidate_target[1] <= _BYPASS_TARGET_Y_MAX
            and _BYPASS_GUARD_Y_MIN <= guard[1] <= _BYPASS_GUARD_Y_MAX
        ):
            continue
        saw_geometry = True
        # A left curl passes a guard that sits right of the target, and vice versa.
        if lateral_offset * side >= 0:
            continue
        saw_side = True
        rotation = -side * 9.0
        # h is a translation term. Aligning the recovered curve at the named
        # target is more accurate than the previous linear approximation.
        h0 = candidate_target[0] - _calibrated_bypass_x(candidate_target[1], 0.0, rotation)
        shot = [6.0, h0, rotation]
        if _bypass_guard_side_margin(guard, shot, side) < _BYPASS_PATH_CLEARANCE:
            continue
        if _bypass_path_blocked(state_list, shot, [candidate_target, guard], min_y=candidate_target[1] - 0.02):
            continue
        detail.update(
            available=True,
            reason="available",
            shot=shot,
            target=candidate_target,
            guard=guard,
        )
        return detail

    if not saw_geometry:
        detail["reason"] = "unsupported_geometry"
    elif not saw_side:
        detail["reason"] = "wrong_curl_side"
    else:
        detail["reason"] = "path_blocked"
    return detail


def bypass_takeout_for_target(
    state_list: StateList,
    is_init: int,
    target: Coordinate,
    side: int,
    shot_num: int,
) -> StrategyResult:
    """Return a target-conditioned, guard-clearing takeout release."""
    return _around_guard_takeout_detail(state_list, is_init, side, shot_num, target=target)["shot"]


def around_guard_takeout_left(
    state_list: StateList,
    is_init: int = flag,
    shot_num: int = shot_num,
) -> StrategyResult:
    return _around_guard_takeout(state_list, is_init, side=-1, shot_num=shot_num)


def around_guard_takeout_right(
    state_list: StateList,
    is_init: int = flag,
    shot_num: int = shot_num,
) -> StrategyResult:
    return _around_guard_takeout(state_list, is_init, side=1, shot_num=shot_num)


def _around_guard_draw(state_list: StateList, side: int, shot_num: int) -> StrategyResult:
    """Use a calibrated late-end curl to draw to button around one offset guard."""
    return _around_guard_draw_detail(state_list, side, shot_num)["shot"]


def _around_guard_draw_detail(state_list: StateList, side: int, shot_num: int) -> dict:
    """Solve one draw route and retain its rejection reason for telemetry."""
    detail = {"available": False, "reason": "no_offset_guard", "shot": None, "target": None, "guard": None}
    if shot_num < 12:
        detail["reason"] = "early_end"
        return detail
    guards = sorted(
        [stone for stone in state_list if _is_guard(stone)],
        key=lambda stone: (abs(stone[0] - 2.375), -stone[1]),
    )
    rotation = -side * 8.0
    # The calibrated free-flight curve ends at the button, rather than at a
    # fixed side offset. This is especially important for a final-stone draw.
    h0 = 2.375 - _calibrated_bypass_x(4.88, 0.0, rotation)
    shot = [3.1, h0, rotation]
    for guard in guards:
        guard_offset = guard[0] - 2.375
        if not _BYPASS_GUARD_Y_MIN <= guard[1] <= _BYPASS_GUARD_Y_MAX or not _BYPASS_GUARD_OFFSET_MIN <= abs(guard_offset) <= _BYPASS_GUARD_OFFSET_MAX:
            continue
        # The shot curls opposite the selected guard's lateral offset.
        if guard_offset * side >= 0:
            continue
        if (
            _bypass_guard_side_margin(guard, shot, side) >= _BYPASS_PATH_CLEARANCE
            and _bypass_path_is_clear(state_list, shot, [guard], min_y=4.70)
        ):
            detail.update(available=True, reason="available", shot=shot, target=[2.375, 4.88], guard=guard)
            return detail
        detail.update(reason="path_blocked", guard=guard)
    return detail


def around_guard_draw_left(
    state_list: StateList,
    is_init: int = flag,
    shot_num: int = shot_num,
) -> StrategyResult:
    return _around_guard_draw(state_list, side=-1, shot_num=shot_num)


def around_guard_draw_right(
    state_list: StateList,
    is_init: int = flag,
    shot_num: int = shot_num,
) -> StrategyResult:
    return _around_guard_draw(state_list, side=1, shot_num=shot_num)


def bypass_action_diagnostics(state_list: StateList, is_init: int, shot_num: int) -> dict:
    """Describe calibrated bypass availability without modifying the board.

    Each action has an ``available`` flag plus a stable rejection reason.  The
    optional target/guard coordinates let collectors tie a selected action to
    a physical contract after the shot settles.
    """
    details = {}
    for suffix, side in (("left", -1), ("right", 1)):
        details[f"around_guard_takeout_{suffix}"] = _around_guard_takeout_detail(
            state_list, is_init, side, shot_num,
        )
        details[f"around_guard_draw_{suffix}"] = _around_guard_draw_detail(
            state_list, side, shot_num,
        )
    return details


def _draw_candidates(state_list: StateList, candidates) -> StrategyResult:
    for point, velocity in candidates:
        result = _free_draw_to_point(state_list, point, velocity)
        if result is not None:
            return result
    return None


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _with_h_bias(result: StrategyResult, bias: float) -> StrategyResult:
    if result is None or result == 0:
        return result
    return [result[0], result[1] + bias, result[2]]


def _freeze_enemy_rank(
    state_list: StateList,
    is_init: int,
    rank: int,
) -> StrategyResult:
    state_enemy, state_me = _split_stones(state_list, is_init)
    targets = [stone for stone in state_enemy if _is_active(stone)]
    targets = sorted(targets, key=lambda stone: bl.DistH(stone))
    if len(targets) <= rank:
        return None
    target = targets[rank]
    if target[1] < 4.88 - 0.35 or not (0.545 < target[0] < 4.205):
        return None
    if bl.Roadjudge(target, [target[0], 10.61], state_list) and bl.Roadjudge(
        target, [target[0], target[1] - 2.2 * Stone_R], state_me
    ):
        return [bl.y2v(target[1]), target[0] - 2.375, 0]

    state_list_filtered = [stone for stone in state_list if stone != target]
    for offset in (-Stone_R, Stone_R, -2 * Stone_R, 2 * Stone_R):
        point = [target[0] + offset, target[1]]
        if 0.545 < point[0] < 4.205 and bl.Roadjudge(point, [point[0], 10.61], state_list_filtered):
            return [bl.y2v(point[1]), point[0] - 2.375, 0]
    return None


def _guard_point_for_stone(stone: Coordinate, distance: float = 1.05) -> Coordinate:
    return [
        _clamp(stone[0], 0.545 + Stone_R, 4.205 - Stone_R),
        _clamp(stone[1] + distance, 6.85, 8.45),
    ]


def _raise_takeout_with_middle(
    state_list: StateList,
    is_init: int,
    middle_owner: str,
) -> StrategyResult:
    state_enemy, state_me = _split_stones(state_list, is_init)
    active = _active_stones(state_list)
    targets = [stone for stone in state_enemy if _is_active(stone) and bl.House(stone)]
    targets = sorted(targets, key=lambda stone: bl.DistH(stone))
    if not targets:
        return None

    if middle_owner == "my":
        middle_pool = state_me
    elif middle_owner == "opp":
        middle_pool = state_enemy
    else:
        middle_pool = active

    for target in targets:
        middles = [
            stone for stone in middle_pool
            if _is_active(stone)
            and stone != target
            and stone[1] > target[1] + 2.2 * Stone_R
            and 0.545 < stone[0] < 4.205
        ]
        middles = sorted(middles, key=lambda stone: abs(stone[0] - target[0]) + 0.25 * abs(stone[1] - target[1]))
        for middle in middles:
            vector = np.array(target) - np.array(middle)
            norm = np.linalg.norm(vector)
            if norm < 1e-8 or vector[1] >= -0.1:
                continue
            angle = np.arctan2(abs(vector[1]), max(abs(vector[0]), 1e-8))
            if angle < np.pi * 35 / 180:
                continue
            contact = np.array(middle) - 2 * Stone_R * vector / norm
            contact_point = [float(contact[0]), float(contact[1])]
            state_without_pair = [
                stone for stone in active
                if stone != middle and stone != target
            ]
            if not (0.545 < contact_point[0] < 4.205):
                continue
            if not bl.Roadjudge(middle, target, state_without_pair):
                continue
            if not bl.Roadjudge(contact_point, [contact_point[0], 10.61], active):
                continue
            correction = 0.033 if vector[0] > 0 else 0.017
            return [6, contact_point[0] - 2.375 + correction, 0]
    return None


def draw_button(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375, 4.88], None),
            ([2.375 - Stone_R, 4.88], None),
            ([2.375 + Stone_R, 4.88], None),
        ],
    )


def draw_top4(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375, 5.49], None),
            ([2.375 - 2 * Stone_R, 5.49], None),
            ([2.375 + 2 * Stone_R, 5.49], None),
        ],
    )


def draw_back4(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375, 4.27], None),
            ([2.375 - 2 * Stone_R, 4.27], None),
            ([2.375 + 2 * Stone_R, 4.27], None),
        ],
    )


def center_guard(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375, 7.35], 2.7),
            ([2.375 - Stone_R, 7.35], 2.7),
            ([2.375 + Stone_R, 7.35], 2.7),
            ([2.375, 8.00], None),
        ],
    )


def center_guard_high(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375, 8.15], 2.7),
            ([2.375 - Stone_R, 8.15], 2.7),
            ([2.375 + Stone_R, 8.15], 2.7),
            ([2.375, 8.45], None),
        ],
    )


def center_guard_low(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375, 6.95], 2.7),
            ([2.375 - Stone_R, 6.95], 2.7),
            ([2.375 + Stone_R, 6.95], 2.7),
            ([2.375, 7.15], None),
        ],
    )


def corner_guard_left(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375 - 0.85, 7.35], 2.7),
            ([2.375 - 0.65, 7.35], 2.7),
            ([2.375 - 1.05, 7.55], None),
        ],
    )


def corner_guard_left_high(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375 - 0.95, 8.10], 2.7),
            ([2.375 - 0.75, 8.10], 2.7),
            ([2.375 - 1.10, 8.35], None),
        ],
    )


def corner_guard_right(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375 + 0.85, 7.35], 2.7),
            ([2.375 + 0.65, 7.35], 2.7),
            ([2.375 + 1.05, 7.55], None),
        ],
    )


def corner_guard_right_high(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375 + 0.95, 8.10], 2.7),
            ([2.375 + 0.75, 8.10], 2.7),
            ([2.375 + 1.10, 8.35], None),
        ],
    )


def come_around_left(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375 - 0.55, 5.35], None),
            ([2.375 - 0.75, 5.20], None),
            ([2.375 - 0.45, 4.88], None),
        ],
    )


def come_around_right(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _draw_candidates(
        state_list,
        [
            ([2.375 + 0.55, 5.35], None),
            ([2.375 + 0.75, 5.20], None),
            ([2.375 + 0.45, 4.88], None),
        ],
    )


def take_out_house(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _hit_nearest_target(state_list, is_init, lambda stone: bl.House(stone), velocity=6.0)


def take_out_guard(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _hit_nearest_target(state_list, is_init, _is_guard, velocity=6.0)


def hit_and_stay(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _hit_nearest_target(state_list, is_init, lambda stone: bl.House(stone), velocity=5.7)


def peel_guard(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _hit_nearest_target(state_list, is_init, _is_guard, velocity=8.0)


def hit_roll_left(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _with_h_bias(hit_roll(state_list, is_init, shot_num), -0.08)


def hit_roll_right(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _with_h_bias(hit_roll(state_list, is_init, shot_num), 0.08)


def freeze_no1(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _freeze_enemy_rank(state_list, is_init, 0)


def freeze_no2(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _freeze_enemy_rank(state_list, is_init, 1)


def guard_my_shot(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    _, state_me = _split_stones(state_list, is_init)
    my_house = [stone for stone in state_me if _is_active(stone) and bl.House(stone)]
    my_house = sorted(my_house, key=lambda stone: bl.DistH(stone))
    if not my_house:
        return center_guard(state_list, is_init, shot_num)
    guard_point = _guard_point_for_stone(my_house[0])
    return _draw_candidates(
        state_list,
        [
            (guard_point, 2.7),
            ([guard_point[0] - Stone_R, guard_point[1]], 2.7),
            ([guard_point[0] + Stone_R, guard_point[1]], 2.7),
        ],
    )


def tap_back(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    _, state_me = _split_stones(state_list, is_init)
    active = _active_stones(state_list)
    targets = [
        stone for stone in state_me
        if _is_active(stone)
        and 4.88 + 0.25 < stone[1] < 8.4
        and 0.545 < stone[0] < 4.205
    ]
    targets = sorted(targets, key=lambda stone: abs(stone[0] - 2.375) + 0.2 * bl.DistH(stone))
    for target in targets:
        state_without_target = [stone for stone in active if stone != target]
        if not bl.Roadjudge(target, [2.375, 4.88], state_without_target):
            continue
        if not bl.Roadjudge(target, [target[0], 10.61], active):
            continue
        velocity = _clamp(bl.y2v(target[1]) + 0.9, 3.8, 5.4)
        return [velocity, target[0] - 2.375, 0]
    return middle_in_center(state_list, is_init, shot_num)


def raise_takeout(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _raise_takeout_with_middle(state_list, is_init, "my")


def runback_takeout(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    return _raise_takeout_with_middle(state_list, is_init, "opp")


def _fallback_occupy(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """Conservative occupy fallback used when the detailed rule tree has no shot."""
    candidates = [
        ([2.375, 6.90], 2.7),
        ([2.375 - 6 * Stone_R, 6.90], 2.7),
        ([2.375 + 6 * Stone_R, 6.90], 2.7),
        ([2.81, 6.19], None),
        ([1.94, 6.19], None),
        ([2.375, 6.19], None),
        ([2.375 - 3 * Stone_R, 6.55], None),
        ([2.375 + 3 * Stone_R, 6.55], None),
    ]
    for point, velocity in candidates:
        result = _free_draw_to_point(state_list, point, velocity)
        if result is not None:
            return result
    return None


def _occupy_rule(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """占位策略 - 在关键位置放置壶以控制局面。

    根据场上左、中、右三个区域的壶分布情况，选择合适的占位点。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[v0, h0, 0]格式的击打参数；
        否则返回None表示策略不适用。

    Examples:
        >>> result = occupy([[2.4, 5.0], [2.5, 5.5]], 0, 10)
        >>> print(result)  # [2.7, 0, 0] 或 0
    """
    situation = bl.judge_occupy_situation(state_list)
    left = situation[0]
    middle = situation[1]
    right = situation[2]
    center_situation = bl.judge_center_situation(state_list)
    if middle[0] == 0:               #中空
        return [2.7,0,0]          #占中，-0.1是偏移量误差修正
    else:                            #中区有球
        if middle[1] == True:        #并且中区的球是对手的
            if center_situation[0] != 0:         #检测大本营中心是否有壶，如果有
                if center_situation[1] == False:   #并且中心壶为己方的
                    if left[0]!=0 or right[0]!=0:  #检测左区和右区是否有壶，如果二者任意一个有壶
                        if left[0] == 0:                    #左空
                            return [2.7,0-6*Stone_R,0]   #占左
                        elif right[0] == 0:                 #右空
                            return [2.7,0+6*Stone_R,0]   #占右
                        else:                               #两边都满
                            return None                #此时占位策略不适用
                    else:       #左区和右区都没壶
                        return [2.7,0-6*Stone_R,0]      #占左(占左占右都可，这里选占左)
                else:                    #中心壶为对手壶，垂直双飞
                    if len(middle[2])!=0 and shot_num > 3:
                        for i in range(len(center_situation[2])):          #哪个能打打哪个
                            point = bl.double_hit_vertical(middle[2],center_situation[2][i],state_list)
                            if point != 0:
                                return [6,point[0]-2.375,0]
                            else:       #都打不了
                                return None    #这个策略不适用
                    if shot_num == 3:
                        if left[0] == 0:                    #左空
                            return [2.7,0-6*Stone_R,0]   #占左
                        elif right[0] == 0:                 #右空
                            return [2.7,0+6*Stone_R,0]   #占右
                        else:                               #两边都满
                            return None                #此时占位策略不适用
                    return None
            else:    #大本营中心没壶
                if left[0]!=0 or right[0]!=0:            #检测左区和右区是否有壶，如果二者任意一个有壶
                    if left[1]==True or right[1]==True:  #并且壶是对手的
                        return None        #策略不适用
                    else:          #如果左区或右区有壶是己方的
                        if left[0] == 0:                    #左空
                            return [2.7,0-6*Stone_R,0]   #占左
                        elif right[0] == 0:                 #右空
                            return [2.7,0+6*Stone_R,0]   #占右
                        else:
                            return None         #此时策略不合理
                else:
                    if left[0] == 0:                    #左空
                        return [2.7,0-6*Stone_R,0]   #占左
                    elif right[0] == 0:                 #右空
                        return [2.7,0+6*Stone_R,0]   #占右
                    else:
                        return None         #此时策略不合理
        else:          #中区球是己方的
            if center_situation[0] != 0:         #检测大本营中心是否有壶，如果有
                if center_situation[1] == False:   #并且中心壶为己方的
                    if left[0]!=0 or right[0]!=0:  #检测左区和右区是否有壶，如果二者任意一个有壶
                        if left[1]==True or right[1]==True:  #并且壶是对手的
                            if right[1] == True and right[2] != []:    #只要右边有壶是对手的，粘住对方防守球
                                if bl.Roadjudge(right[2],[right[2][0],10.61],state_list):
                                    v0 = bl.y2v(right[2][1])
                                    h0 = right[2][0]-2.375
                                    return [v0,h0,0]
                                else:                   #粘住左边防守球
                                    if left[1] == True and left[2] != []:
                                        if bl.Roadjudge(left[2],[left[2][0],10.61],state_list):
                                            v0 = bl.y2v(left[2][1])
                                            h0 = left[2][0]-2.375
                                            return [v0,h0,0]
                                        else:
                                            return None
                                    else:
                                        return None
                            else:                   #粘住左边防守球
                                if left[2] != []:
                                    if bl.Roadjudge(left[2],[left[2][0],10.61],state_list):
                                        v0 = bl.y2v(left[2][1])
                                        h0 = left[2][0]-2.375
                                        return [v0,h0,0]
                                    else:
                                        return None
                                else:
                                    return None
                        else:
                            if left[0] == 0:
                                return [2.7,0-6*Stone_R,0]   #占左
                            elif right[0] == 0:                 #右空
                                return [2.7,0+6*Stone_R,0]   #占右
                            else:             #两边都有自己的壶,帖中防守
                                point1 = [2.81,6.19]
                                point2 = [1.94,6.19]
                                if bl.Roadjudge(point1,[point1[0],10.61],state_list) and bl.LocalJudge(point1,state_list) and bl.LocalJudge(point1,state_list):
                                    v0 = bl.y2v(6.19)
                                    h0 = point1[0]-2.375
                                    return [v0,h0,0]
                                elif bl.Roadjudge(point2,[point2[0],10.61],state_list) and bl.LocalJudge(point2,state_list) and bl.LocalJudge(point2,state_list):
                                    v0 = bl.y2v(6.19)
                                    h0 = point2[0]-2.375
                                    return [v0,h0,0]
                                else:
                                    return None    #策略不合理
                    else:    #左右都没壶
                        return [2.7,0-6*Stone_R,0]   #占左
                else:      #中心壶为对手的
                    if left[0]!=0 or right[0]!=0:  #检测左区和右区是否有壶，如果二者任意一个有壶
                        if left[1]==True or right[1]==True:  #并且壶是对手的
                            return None       #此时策略不合理
                        else:
                            if left[0] == 0:
                                return [2.7,0-6*Stone_R,0]   #占左
                            elif right[0] == 0:                 #右空
                                return [2.7,0+6*Stone_R,0]   #占右
                            else:           #贴中防守
                                point1 = [2.81,6.19]
                                point2 = [1.94,6.19]
                                if bl.Roadjudge(point1,[point1[0],10.61],state_list) and bl.LocalJudge(point1,state_list):
                                    v0 = bl.y2v(6.19)
                                    h0 = point1[0]-2.375
                                    return [v0,h0,0]
                                elif bl.Roadjudge(point2,[point2[0],10.61],state_list) and bl.LocalJudge(point2,state_list):
                                    v0 = bl.y2v(6.19)
                                    h0 = point2[0]-2.375
                                    return [v0,h0,0]
                                else:
                                    return None    #策略不合理
                    else:    #左右都没壶
                        return [2.7,0-6*Stone_R,0]   #占左
            else:   #中心没壶
                if left[0]!=0 or right[0]!=0:  #检测左区和右区是否有壶，如果二者任意一个有壶
                    if left[0] == 0:
                        return [2.7,0-6*Stone_R,0]   #占左
                    elif right[0] == 0:                 #右空
                        return [2.7,0+6*Stone_R,0]   #占右
                    else:
                        return None         #此时策略不合理
                else:
                    return [2.7,0-6*Stone_R,0]   #占左
    return None


def occupy(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    result = _occupy_rule(state_list, is_init, shot_num)
    if result is not None and result != 0:
        return result
    return _fallback_occupy(state_list, is_init, shot_num)

def take_out(state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> StrategyResult:
    """打定策略 - 直接击打并清除对方壶。

    选择合适的目标壶进行击打，将其从大本营中清除。

    Args:
        state_list: 所有壶的坐标列表（内部会自动分离对方壶和己方壶）。
        is_init: 先后手标识，0表示我方先手，1表示后手。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果策略可行，返回[6, h0, 0]格式的击打参数；
        否则返回None表示策略不合理。

    Examples:
        >>> result = take_out([[2.5, 6.0], [2.4, 7.0]], 0, 10)
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])

    house_targets = [stone for stone in state_enemy if _is_active(stone) and bl.House(stone)]
    if not house_targets:
        return None
    out_s = bl.NearestTarget(house_targets)  # 按距中心距离升序排序
    if bl.Roadjudge(out_s[0], [out_s[0][0], 10.61], state_list) and out_s[0][0] != 0 and bl.Roadjudge(out_s[0],
                                                                                                      [out_s[0][0],
                                                                                                       3.05], state_me):
        if out_s[0][1] < 6.1:
            if bl.House(out_s[0]):
                return [6, out_s[0][0] - 2.375, 0]
        else:
            return [6, out_s[0][0] - 2.375, 0]
    else:
        if bl.Roadjudge(out_s[0], [out_s[0][0], 10.61], state_list) == False and out_s[0][0] != 0 and bl.Roadjudge(
                out_s[0], [out_s[0][0], 3.05], state_me):
            d = 2 * Stone_R / 2
            h_range = [x for x in np.arange(-d, d, 0.01)]
            state_list_filtered = [i for i in state_list if i != out_s[0]]
            for h in h_range:
                if bl.Roadjudge([out_s[0][0] + h, out_s[0][1]], [out_s[0][0] + h, 10.61], state_list_filtered):
                    if h < 0:
                        if out_s[0][1] < 6.1:
                            if bl.House(out_s[0]):
                                return [6, out_s[0][0] + h - 2.375 + 0.033, 0]
                        else:
                            return [6, out_s[0][0] + h - 2.375 + 0.033, 0]
                    else:
                        if out_s[0][1] < 6.1:
                            if bl.House(out_s[0]):
                                return [6, out_s[0][0] + h - 2.375 + 0.017, 0]
                        else:
                            return [6, out_s[0][0] + h - 2.375 + 0.017, 0]
    return None  # 此时策略不合理



def hit_roll(
    state_list: StateList,
    is_init: int,
    shot_num: int,
    target_stone=None,
) -> StrategyResult:
    """打甩策略 。

    根据目标壶距离中心的远近，选择middle、low、max或extension区域的击打策略，不同区域有不同的击打特征（由无限调试采样得来）。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[v0, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = hit_roll([[2.5, 6.0], [2.6, 6.5]], 0, 10)
        >>> print(result)  # [10, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    d_enemy = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            d_enemy.append(bl.DistH(state_list[2 * i + 1]))
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            d_enemy.append(bl.DistH(state_list[2 * i]))
            state_me.append(state_list[2 * i + 1])
    target_midddle = []
    hit_middle = []
    target_low = []
    hit_low = []
    dert_low = []
    point_low = []
    angle_low = []
    target_max = []
    hit_max = []
    target_extension = []
    hit_extension = []
    for i in range(len(state_enemy)):
        if target_stone is not None and state_enemy[i] is not target_stone:
            continue
        if bl.Roadjudge(state_enemy[i], [state_enemy[i][0], 10.61], state_list) == False or bl.Roadjudge(state_enemy[i],
                                                                                                   [state_enemy[i][0],
                                                                                                    3.05],
                                                                                                   state_list) == False:
            continue
        if state_enemy[i][0] == 0 and state_enemy[i][1] == 0:
            continue
        if abs(state_enemy[i][0] - 2.375) < 1:
            if shot_num == 14:
                if bl.House(state_enemy[i]) == False:
                    continue
            else:
                if bl.House(state_enemy[i]) == False and (state_enemy[i][1] < 4.88 or state_enemy[i][1] > 8.16):
                    continue
            ht = bl.feature_roll_v_pro(state_enemy[i][0])
            if state_enemy[i][0] - 2.375 > 0:
                h0 = -ht + state_enemy[i][0] - 2.375 + 0.033
                point_x = -ht + state_enemy[i][0]
            else:
                h0 = ht + state_enemy[i][0] - 2.375 + 0.017
                point_x = ht + state_enemy[i][0]
            point_y = state_enemy[i][1]
            state_list_t = [state_list[l] for l in range(len(state_list)) if
                            state_list[l][0] != state_enemy[i][0] and state_list[l][1] != state_enemy[i][1]]
            if bl.Roadjudge([point_x, point_y], [point_x, 10.61], state_list_t) and bl.Roadjudge(state_enemy[i],
                                                                                           [state_enemy[i][0], 0],
                                                                                           state_me):
                target_midddle.append(state_enemy[i])
                hit_middle.append(h0)
        elif 1 <= abs(state_enemy[i][0] - 2.375) < 1.5:
            if shot_num == 14:
                if bl.House(state_enemy[i]) == False:
                    continue
            else:
                if bl.House(state_enemy[i]) == False and (state_enemy[i][1] < 4.88 - 0.45 or state_enemy[i][1] > 8.16):
                    continue
            if state_enemy[i][1] > 6.71 - Stone_R:
                final = [2.375, state_enemy[i][1] - abs(2.375 - state_enemy[i][0])]
                vector = np.array(final) - np.array(state_enemy[i])
                D = bl.Dist(state_enemy[i], final)
                d = np.sqrt(D ** 2 - 4 * Stone_R ** 2)
                angle1 = np.arctan2(abs(vector[1]), abs(vector[0]))
                theta = np.arcsin(2 * Stone_R / D)
                angle = angle1 + theta
                if vector[0] > 0:
                    point_x = 2.375 - d * np.cos(angle)
                    point_y = final[1] + d * np.sin(angle)
                else:
                    point_x = 2.375 + d * np.cos(angle)
                    point_y = final[1] + d * np.sin(angle)
                state_list_t = [state_list[l] for l in range(len(state_list)) if
                                state_list[l][0] != state_enemy[i][0] and state_list[l][1] != state_enemy[i][1]]
                if bl.Roadjudge([point_x, point_y], [point_x, 10.61], state_list) and bl.Roadjudge([point_x, point_y], final,
                                                                                             state_list_t):
                    target_low.append(state_enemy[i])
                    if vector[0] > 0:
                        hit_low.append(point_x - 2.375 + 0.033)
                    else:
                        hit_low.append(point_x - 2.375 + 0.017)
                    dert_low.append(d)
                    angle_low.append(angle)
                    point_low.append([point_x, point_y])
            else:
                ht = bl.feature_roll_v_max(state_enemy[i][0])
                if state_enemy[i][0] - 2.375 > 0:
                    h0 = -ht + state_enemy[i][0] - 2.375 + 0.033
                    point_x = -ht + state_enemy[i][0]
                else:
                    h0 = ht + state_enemy[i][0] - 2.375 + 0.017
                    point_x = ht + state_enemy[i][0]
                point_y = state_enemy[i][1]
                state_list_t = [state_list[l] for l in range(len(state_list)) if
                                state_list[l][0] != state_enemy[i][0] and state_list[l][1] != state_enemy[i][1]]
                if bl.Roadjudge([point_x, point_y], [point_x, 10.61], state_list_t) and bl.Roadjudge(state_enemy[i],
                                                                                               [state_enemy[i][0], 0],
                                                                                               state_me):
                    target_max.append(state_enemy[i])
                    hit_max.append(h0)
        elif 1.5 <= abs(state_enemy[i][0] - 2.375) <= 2:
            if shot_num == 14:
                if bl.House(state_enemy[i]) == False:
                    continue
            else:
                if bl.House(state_enemy[i]) == False and (state_enemy[i][1] < 4.88 - 1.5 or state_enemy[i][1] > 8.16):
                    continue
            if state_enemy[i][0] - 2.375 > 0:
                h0 = state_enemy[i][0] - 2.375 + 0.033 - 0.12
            else:
                h0 = state_enemy[i][0] - 2.375 + 0.017 + 0.12
            if bl.Roadjudge(state_enemy[i], [state_enemy[i][0], 10.61], state_list):
                hit_extension.append(h0)
                target_extension.append(state_enemy[i])
    if len(hit_middle) != 0:
        dis = []
        for i in range(len(target_midddle)):
            dis.append(bl.DistH(target_midddle[i]))
        t = np.argmin(dis)
        return [10, hit_middle[t], 0]
    elif len(hit_max) != 0:
        dis = []
        for i in range(len(target_max)):
            dis.append(bl.DistH(target_max[i]))
        t = np.argmin(dis)
        return [10, hit_max[t], 0]
    elif len(hit_low) != 0:
        dis = []
        for i in range(len(target_low)):
            dis.append(bl.DistH(point_low[i]))
        t = np.argmin(dis)
        angle = angle_low[t] * 180 / np.pi
        L = 27.6 + 4.88 - target_low[t][1]
        L_target = abs(point_low[t][0] - 2.375)
        v0 = bl.feature_roll_v(L, L_target, angle)
        h0 = hit_low[t]
        return [v0, h0, 0]
    elif len(hit_extension) != 0:
        dis = []
        for i in range(len(target_extension)):
            dis.append(bl.DistH(target_extension[i]))
        t = np.argmin(dis)
        L = 27.6 + 4.88 - target_extension[t][1]
        L_target = abs(target_extension[t][0] - 2.375)
        v0 = bl.feature_roll_v_extension(L, L_target)
        h0 = hit_extension[t]
        return [v0, h0, 0]
    else:
        return None


def disarm_defend(state_list: StateList, is_init: int, shout_num: int) -> StrategyResult:
    """分壶防守策略 - 在对方壶两侧放置防守壶。

    分析对方壶的分布，在其左右两侧合适位置放置己方壶进行防守。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示先手，1表示后手。
        shout_num: 当前投球序号。

    Returns:
        如果策略可行，返回[4, h0, 0]格式的击打参数；
        否则返回None表示不可行。

    Examples:
        >>> result = disarm_defend([[2.5, 6.0], [2.6, 6.5]], 0, 10)
        >>> print(result)  # [4, 0.35, 0] 或 0
    """
    state_enemy = []
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_me.append(state_list[2 * i + 1])
    state_enemy = [i for i in state_enemy if i[0] != 0 and i[1] != 0]
    state_me = [i for i in state_me if i[0] != 0 and i[1] != 0]
    state_list = [i for i in state_list if i[0] != 0 and i[1] != 0]
    avail_right = []
    avail_left = []
    for i in range(len(state_enemy)):
        if abs(state_enemy[i][0] - 2.375) > 3 * Stone_R:
            continue
        if (bl.Roadjudge(state_enemy[i], [state_enemy[i][0], state_enemy[i][1] + 2.2 * Stone_R], state_me) and
            state_enemy[i][1] < 8) == False:
            continue
        avail = True
        if state_enemy[i][0] - 2.375 <= 0 and state_enemy[i][1] > 4.88:
            for j in range(len(state_list)):
                if 0 < state_list[j][0] - state_enemy[i][0] < 4 * Stone_R and state_list[j][1] > state_enemy[i][
                    1]:  # 右侧不可行判断
                    avail = False
                if 4.88 + 1.83 < state_enemy[i][1] < 4.88 + 1.83 + 0.7 and shout_num <= 4:
                    avail = False
            if avail == True:
                avail_right.append(state_enemy[i])
        avail = True
        if state_enemy[i][0] - 2.375 > 0 and state_enemy[i][1] > 4.88 + 0.9:
            for j in range(len(state_list)):
                if -4 * Stone_R < state_list[j][0] - state_enemy[i][0] < 0 and state_list[j][1] > state_enemy[i][1]:
                    avail = False
                if 4.88 + 1.83 < state_enemy[i][1] < 4.88 + 1.83 + 0.7 and shout_num <= 4:
                    avail = False
            if avail == True:
                avail_left.append(state_enemy[i])
    if len(avail_left) != 0 and len(avail_right) != 0:
        temp1 = sorted(avail_left, key=lambda x: abs(x[1] - 4.88 - 1.22) + abs(x[0] - 2.375), reverse=True)
        temp2 = sorted(avail_right, key=lambda x: abs(x[1] - 4.88 - 1.22) + abs(x[0] - 2.275), reverse=True)
        temp = sorted([temp1[-1], temp2[-1]], key=lambda x: abs(x[1] - 4.88 - 1.22) + abs(x[0] - 2.375), reverse=True)
        if temp[-1][0] == temp2[-1][0]:  # 右侧可行
            h = temp[-1][0] - 2.375 + 2 * Stone_R - 0.05 + 0.017
        else:
            h = temp[-1][0] - 2.375 - 2 * Stone_R + 0.05 + 0.033
        return [4, h, 0]
    elif len(avail_left) == 0 and len(avail_right) != 0:
        temp = sorted(avail_right, key=lambda x: x[1])
        h = temp[-1][0] - 2.375 + 2 * Stone_R - 0.05 + 0.017
        return [4, h, 0]
    elif len(avail_left) != 0 and len(avail_right) == 0:
        temp = sorted(avail_left, key=lambda x: x[1])
        h = temp[-1][0] - 2.375 - 2 * Stone_R + 0.05 + 0.033
        return [4, h, 0]
    else:
        return None


def double_push_in_center(state_list: StateList, is_init: int, shot_num: int) -> StrategyResult:
    """双传进营中心策略 - 通过两次传递将壶打入中心。

    利用两个中间壶作为传递点，最终将壶打入大本营中心区域。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[vt, x, 0]格式的击打参数；
        否则返回None表示策略不可用。

    Examples:
        >>> result = double_push_in_center([[2.5, 6.0], [2.6, 6.5]], 0, 10)
        >>> print(result)  # [3.5, 0.05, 0] 或 0
    """
    state_me = []
    if is_init == 0:
        for i in range(8):
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_me.append(state_list[2 * i + 1])
    dis1 = []
    dis2 = []
    hit = []
    middle1 = []
    middle2 = []
    angle = []
    for i in range(len(state_me)):
        if state_me[i][1] <= 4.88:  # 需要我方大于对面
            continue
        v0 = np.array([2.375, 4.88]) - np.array(state_me[i])  # 标准向量指向中心
        angle1 = np.arctan2(abs(v0[1]), abs(v0[0]))
        if angle1 < 30 / 180 * np.pi:
            continue
        multiple = 2 * Stone_R / np.sqrt(v0[0] ** 2 + v0[1] ** 2)
        point_x = state_me[i][0] - multiple * v0[0]
        point_y = state_me[i][1] - multiple * v0[1]
        if bl.Roadjudge(state_me[i], [2.375, 4.88], state_list):  # 路径1无障碍
            for j in range(len(state_list)):
                if state_list[j][0] == state_me[i][0] and state_list[j][1] == state_me[i][1]:
                    continue
                if state_list[j][1] <= state_me[i][1]:  # 下方球必需低上方球
                    continue
                if bl.Roadjudge(state_list[j], [point_x, point_y], state_list):  # 道路检测可行state_me[i],与中心点
                    v = np.array([point_x, point_y]) - np.array(state_list[j])
                    angle2 = np.arctan2(abs(v[1]), abs(v[0]))
                    if v[0] * v0[0] < 0:
                        continue
                    if angle2 > 70 / 180 * np.pi:
                        continue
                    if angle2 < angle1:
                        continue
                    multiple1 = 2 * Stone_R / np.sqrt(v[0] ** 2 + v[1] ** 2)
                    point_x1 = state_list[j][0] - multiple1 * v[0]
                    point_y1 = state_list[j][1] - multiple1 * v[1]  # 得出最终击球点
                    if bl.Roadjudge([point_x1, point_y1], [point_x1, 10.61], state_list):
                        angle.append([angle1, angle2])
                        middle1.append(state_me[i])
                        middle2.append(state_list[j])
                        dis1.append(bl.Dist([2.375, 4.88], state_me[i]))
                        dis2.append(bl.Dist(state_list[j], [point_x, point_y]))
                        if v[0] > 0:  # 打左边
                            hit.append(point_x1 - 2.375 + 0.033)
                        else:
                            hit.append(point_x1 - 2.375 + 0.017)
    dis = []
    for i in range(len(dis1)):
        dis.append(dis1[i] + dis2[i])
    if len(hit) != 0:
        t = np.argmin(dis)
        x = hit[t]
        vt = bl.y2_v(middle2[t][1])
        derta_y1 = abs(4.88 - middle1[t][1])
        derta_x1 = abs(2.375 - middle1[t][0])
        derta_d1 = np.sqrt(derta_x1 ** 2 + derta_y1 ** 2)
        derta_y2 = abs(middle1[t][1] - middle2[t][1])
        derta_x2 = abs(middle1[t][0] - middle2[t][0])
        derta_d2 = np.sqrt(derta_x2 ** 2 + derta_y2 ** 2)
        if angle[t][0] > np.pi / 180 * 75:
            vt += bl.delta_y2v_small(derta_d1)
        else:
            vt += bl.delta_y2v_big(derta_d1)
        if angle[t][1] > np.pi / 180 * 75:
            vt += bl.delta_y2v_small(derta_d2)
        else:
            vt += bl.delta_y2v_big(derta_d2)
        vt = vt - 0.5
        if vt < 4:
            x -= 0.024
        return [vt, x, 0]
    else:
        return None  # 测略不可用


def double_push_in(state_list: StateList, is_init: int, shot_num: int) -> StrategyResult:
    """双传进营策略 - 通过两次传递击打对方壶。

    利用中间壶作为传递点，最终击打目标壶。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[6, x, 0]格式的击打参数；
        否则返回None表示测量不可用。

    Examples:
        >>> result = double_push_in([[2.5, 6.0], [2.6, 6.5]], 0, 10)
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    d_enemy = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            d_enemy.append(bl.DistH(state_list[2 * i + 1]))
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            d_enemy.append(bl.DistH(state_list[2 * i]))
            state_me.append(state_list[2 * i + 1])
    index = np.argmin(d_enemy)
    if shot_num == 14 or shot_num == 15:
        t = state_enemy[index]
        state_enemy = []
        for i in range(len(d_enemy)):
            if d_enemy[i] < Stone_R * 1.7:  # 1.7半径内
                state_enemy.append(t)
    dis1 = []
    dis2 = []
    hit = []
    hit_target = []
    for k in range(len(state_enemy)):
        if state_enemy[k][1] == 0 and state_enemy[k][0] == 0:
            continue
        if state_enemy[k][1] < 4.88 - 0.61:
            continue
        for i in range(len(state_me)):
            if state_me[i][1] <= state_enemy[k][1]:  # 需要我方大于对面
                continue
            v0 = np.array(state_enemy[k]) - np.array(state_me[i])  # 标准向量指向中心
            angle1 = np.arctan2(abs(v0[1]), abs(v0[0]))
            if angle1 < 30 / 180 * np.pi:
                continue
            multiple = 2 * Stone_R / np.sqrt(v0[0] ** 2 + v0[1] ** 2)
            point_x = state_me[i][0] - multiple * v0[0]
            point_y = state_me[i][1] - multiple * v0[1]
            if v0[0] > 0:
                point_x += 0.033
            else:
                point_x += 0.017
            if bl.Roadjudge(state_me[i], state_enemy[k], state_list):  # 路径1无障碍
                for j in range(len(state_list)):
                    if state_list[j][0] == state_me[i][0] and state_list[j][1] == state_me[i][1]:
                        continue
                    if state_list[j][0] == state_enemy[k][0] and state_list[j][1] == state_enemy[k][1]:
                        continue
                    if state_list[j][1] <= state_me[i][1]:  # 下方球必需低上方球
                        continue
                    if bl.Roadjudge(state_list[j], [point_x, point_y], state_list):  # 道路检测可行state_me[i],与中心点
                        v = np.array([point_x, point_y]) - np.array(state_list[j])
                        angle2 = np.arctan2(abs(v[1]), abs(v[0]))
                        if v[0] * v0[0] < 0:
                            continue
                        if angle2 > 70 / 180 * np.pi:
                            continue
                        if angle2 < angle1:
                            continue
                        angle2 = np.arctan2(abs(v[1]), abs(v[0]))
                        if v[0] * v0[0] < 0:
                            continue
                        if angle2 > 80 / 180 * np.pi:
                            continue
                        multiple1 = 2 * Stone_R / np.sqrt(v[0] ** 2 + v[1] ** 2)
                        point_x1 = state_list[j][0] - multiple1 * v[0]
                        point_y1 = state_list[j][1] - multiple1 * v[1]  # 得出最终击球点
                        if bl.Roadjudge([point_x1, point_y1], [point_x1, 10.61], state_list):
                            dis1.append(bl.Dist(state_enemy[k], state_me[i]))
                            dis2.append(bl.Dist(state_list[j], [point_x, point_y]))
                            hit_target.append(state_enemy[k])
                            if v[0] > 0:  # 打左边
                                hit.append(point_x1 - 2.375 + 0.033)
                            else:
                                hit.append(point_x1 - 2.375 + 0.017)
    dis = []
    for i in range(len(dis1)):
        dis.append(dis1[i] + dis2[i])
    if len(hit) != 0:
        t = np.argmin(dis)
        x = hit[t]
        return [6, x, 0]
    else:
        return None  # 测量不可用


def push_in(state_list: StateList, is_init: int, shot_num: int) -> StrategyResult:
    """传击策略 - 通过中间壶传递力量击打目标。

    利用己方壶作为中介，传递力量击打对方目标壶。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[v0, h0, 0]或[6, h, 0]格式的击打参数；
        否则返回None表示传击不可取。

    Examples:
        >>> result = push_in([[2.5, 6.0], [2.6, 6.5]], 0, 10)
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_list_enemy = []
    state_me = []
    d_enemy = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            state_list_enemy.append(state_list[2 * i])
            d_enemy.append(bl.DistH(state_list[2 * i + 1]))
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            state_list_enemy.append(state_list[2 * i])
            d_enemy.append(bl.DistH(state_list[2 * i]))
            state_me.append(state_list[2 * i + 1])
    index = np.argmin(d_enemy)  # 距离最近的
    if shot_num == 14 or shot_num == 15:
        dis = []
        for i in range(len(state_enemy)):
            if bl.House(state_enemy[i]):
                dis.append(bl.DistH(state_enemy[i]))
        val = False
        if len(dis) >= 2:
            dis = sorted(dis)
            for j in range(len(state_me)):
                if dis[0] < bl.DistH(state_me[j]) < dis[1]:
                    val = True
        t = state_enemy[index]
        if len(dis) == 1:
            if bl.Roadjudge(t, [t[0], 10.61], state_list):
                return [6, t[0] - 2.375, 0]
            else:
                val = True
        state_enemy = []
        if val == True:
            state_enemy.append(t)
    hit_target = []
    hit_list = []
    angle_list = []
    middle_list = []
    state_me = bl.NearestTarget(state_me)
    for i in range(len(state_enemy)):
        if state_enemy[i][1] == 0 and state_enemy[i][0] == 0:
            continue
        if state_enemy[i][0] > 4.205 or state_enemy[i][0] < 0.545:
            continue
        if (shot_num == 14 or shot_num == 15) and state_enemy[i][1] > 6.71:
            continue
        if bl.House(state_enemy[i]) == False and state_enemy[i][1] < 4.88:
            continue
        for j in range(len(state_me)):
            vector = np.array(state_enemy[i]) - np.array(state_me[j])  # 方向指向目标点
            vector_norm = np.linalg.norm(vector)
            if vector_norm < 1e-8:
                continue
            enemy_x = state_enemy[i][0] + 0.61 * vector[0] / vector_norm
            enemy_y = state_enemy[i][1] + 0.61 * vector[1] / vector_norm
            theta0 = np.arctan2(np.abs(vector[1]), np.abs(vector[0]))
            avail = True
            for k in range(len(state_list)):
                if state_list[k][0] != state_me[j][0] and state_list[k][1] != state_me[j][1]:  # 排除自己
                    if abs(state_me[j][0] - state_list[k][0]) < Stone_R / 5 and bl.Dist(state_list[k], state_me[
                        j]) < 2 * 2 * Stone_R:  # 两球横坐标相距1/5个半径
                        avail = False
            if avail == False:
                continue
            if bl.DistH(state_enemy[i]) > 0.61:
                if bl.Dist(state_enemy[i], state_me[j]) < 2 * 2 * Stone_R:
                    continue
            if theta0 < np.pi * 35 / 180:  # 小于35度不打
                continue
            if state_me[j][0] == 0 and state_me[j][1] == 0:
                continue
            if state_me[j][0] > 4.205 or state_me[j][0] < 0.545:
                continue
            if state_me[j][1] <= state_enemy[i][1]:
                continue
            state_list_t = [state_list[l] for l in range(len(state_list))
                            if state_list[l][0] != state_enemy[i][0] and state_list[l][1] != state_enemy[i][1]]
            if bl.Roadjudge(state_me[j], [enemy_x, enemy_y], state_list_t):
                mutiple = 2 * Stone_R / np.sqrt(vector[0] ** 2 + vector[1] ** 2)
                point_x = state_me[j][0] - mutiple * vector[0]
                point_y = state_me[j][1] - mutiple * vector[1]
                if bl.Roadjudge([point_x, point_y], [point_x, 10.61], state_list):
                    hit_target.append(state_enemy[i])
                    middle_list.append(state_me[j])
                    if vector[0] > 0:  # 左边
                        hit_list.append(point_x - 2.375 + 0.033)
                    else:
                        hit_list.append(point_x - 2.375 + 0.017)
                    angle_list.append(theta0)

    if shot_num != 14 and shot_num != 15:  # 非最后一球
        if len(hit_target) != 0 and len(hit_list) != 0:
            dis2 = []
            for i in range(len(hit_target)):
                dis2.append(bl.get_dist(hit_target[i][0], hit_target[i][1]))
            dis2 = np.array(dis2)
            add = dis2
            t = np.argmin(add)
            h = hit_list[t]
            return [6, h, 0]
        else:
            return None  # 传击不可取
    else:
        if len(hit_target) == 0:  # 对方没有中心或者被挡住
            state_enemy = []
            state_enemy.append([2.375, 4.88])
            hit_target = []
            hit_list = []
            angle_list = []
            middle_list = []
            for j in range(len(state_me)):
                vector = np.array(state_enemy[0]) - np.array(state_me[j])  # 方向指向目标点
                theta0 = np.arctan2(np.abs(vector[1]), np.abs(vector[0]))
                if theta0 < np.pi * 40 / 180:  # 小于40度不打
                    continue
                if state_me[j][0] == 0 and state_me[j][1] == 0:
                    continue
                if state_me[j][0] > 4.205 or state_me[j][0] < 0.545:
                    continue
                if state_me[j][1] <= state_enemy[0][1]:
                    continue
                freeze_judge = False  # 检测周边是否有粘球
                for k in range(len(state_list_enemy)):
                    if bl.Dist(state_list_enemy[k], state_me[j]) < 2.2 * Stone_R:
                        freeze_judge = True
                if freeze_judge:
                    continue
                if bl.Roadjudge(state_me[j], state_enemy[0], state_list):
                    mutiple = 2 * Stone_R / np.sqrt(vector[0] ** 2 + vector[1] ** 2)
                    point_x = state_me[j][0] - mutiple * vector[0]
                    point_y = state_me[j][1] - mutiple * vector[1]
                    if bl.Roadjudge([point_x, point_y], [point_x, 10.61], state_list):
                        hit_target.append(state_enemy[0])
                        middle_list.append(state_me[j])
                        if vector[0] > 0:  # 左边
                            hit_list.append(point_x - 2.375 + 0.033)
                        else:
                            hit_list.append(point_x - 2.375 + 0.017)
                        angle_list.append(theta0)
            if len(hit_target) == 0:
                return None
            else:
                dis2 = []
                for i in range(len(hit_target)):
                    dis2.append(bl.get_dist(hit_target[i][0], hit_target[i][1]))
                dis2 = np.array(dis2)
                add = dis2
                t = np.argmin(add)
                h = hit_list[t]
                angle = angle_list[t] * 180 / np.pi
                me = middle_list[t]
                vector = np.array([2.375, 4.88]) - np.array(me)
                v0 = bl.feature_v(27.6 + 4.88 - me[1], bl.DistH(me), angle)
                h0 = hit_list[t]
                return [v0, h0, 0]
        else:
            dis2 = []
            for i in range(len(hit_target)):
                dis2.append(bl.get_dist(hit_target[i][0], hit_target[i][1]))
            dis2 = np.array(dis2)
            add = dis2
            t = np.argmin(add)
            h = hit_list[t]
            return [6, h, 0]
    return None


def push_in_14(state_list: StateList, is_init: int, shot_num: int) -> StrategyResult:
    """第14杆传击策略 - 针对第14杆的特殊传击策略。

    在第14或15杆时，采用更激进的传击策略以争取胜利。

    Args:
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示先手，1表示后手。
        shot_num: 当前投球序号。

    Returns:
        如果策略可行，返回[6, h, 0]格式的击打参数；
        否则返回None表示传击不可取。

    Examples:
        >>> result = push_in_14([[2.5, 6.0], [2.6, 6.5]], 0, 14)
        >>> print(result)  # [6, 0.125, 0] 或 0
    """
    state_enemy = []
    state_me = []
    d_enemy = []
    if is_init == 0:
        for i in range(8):
            state_enemy.append(state_list[2 * i + 1])
            d_enemy.append(bl.DistH(state_list[2 * i + 1]))
            state_me.append(state_list[2 * i])
    else:
        for i in range(8):
            state_enemy.append(state_list[2 * i])
            d_enemy.append(bl.DistH(state_list[2 * i]))
            state_me.append(state_list[2 * i + 1])
    index = np.argmin(d_enemy)  # 距离最近的
    if shot_num == 14 or shot_num == 15:
        dis = []
        for i in range(len(state_enemy)):
            if state_enemy[i][0] != 0 and state_enemy[i][1] != 0:
                dis.append(bl.DistH(state_enemy[i]))
        val = False
        if len(dis) >= 2:
            dis = sorted(dis)
            for j in range(len(state_me)):
                if dis[0] < bl.DistH(state_me[j]) < dis[1]:
                    val = True
        t = state_enemy[index]
        if len(dis) == 1:
            if bl.Roadjudge(t, [t[0], 10.61], state_list):
                return [6, t[0] - 2.375, 0]
            else:
                val = True
        state_enemy = []
        if val == True:
            state_enemy.append(t)
    hit_target = []
    hit_list = []
    angle_list = []
    middle_list = []
    state_me = bl.NearestTarget(state_me)
    for i in range(len(state_enemy)):
        if state_enemy[i][1] == 0 and state_enemy[i][0] == 0:
            continue
        if bl.House(state_enemy[i]) == False:
            if bl.House(state_me[0]):
                continue
        if bl.House(state_enemy[i]) == False and state_enemy[i][1] < 4.88:
            continue
        if state_enemy[i][0] > 4.205 or state_enemy[i][0] < 0.545:
            continue
        if (shot_num == 14 or shot_num == 15) and state_enemy[i][1] > 6.71:
            continue
        for j in range(len(state_me)):
            if state_me[j][0] == 0 and state_me[j][1] == 0:
                continue
            vector = np.array(state_enemy[i]) - np.array(state_me[j])  # 方向指向目标点
            vector_norm = np.linalg.norm(vector)
            if vector_norm <= 1e-12:
                continue
            enemy_x = state_enemy[i][0] + 0.61 * vector[0] / vector_norm
            enemy_y = state_enemy[i][1] + 0.61 * vector[1] / vector_norm
            theta0 = np.arctan2(np.abs(vector[1]), np.abs(vector[0]))
            if bl.DistH(state_enemy[i]) > 0.61:
                if bl.Dist(state_enemy[i], state_me[j]) < 2 * 2 * Stone_R:
                    continue
            if bl.Dist(state_enemy[i], state_me[j]) > 1.83 * 2:
                continue
            if theta0 < np.pi * 35 / 180:  # 小于35度不打
                continue
            if state_me[j][0] > 4.205 or state_me[j][0] < 0.545:
                continue
            if state_me[j][1] <= state_enemy[i][1]:
                continue
            state_list_t = [state_list[l] for l in range(len(state_list))
                            if state_list[l][0] != state_enemy[i][0] and state_list[l][1] != state_enemy[i][1]]
            if bl.Roadjudge(state_me[j], [enemy_x, enemy_y], state_list_t):
                mutiple = 2 * Stone_R / vector_norm
                point_x = state_me[j][0] - mutiple * vector[0]
                point_y = state_me[j][1] - mutiple * vector[1]
                if bl.Roadjudge([point_x, point_y], [point_x, 10.61], state_list):
                    hit_target.append(state_enemy[i])
                    middle_list.append(state_me[j])
                    if vector[0] > 0:  # 左边
                        hit_list.append(point_x - 2.375 + 0.033)
                    else:
                        hit_list.append(point_x - 2.375 + 0.017)
                    angle_list.append(theta0)
    if shot_num != 14 and shot_num != 15:  # 非最后一球
        if len(hit_target) != 0 and len(hit_list) != 0:
            dis2 = []
            for i in range(len(hit_target)):
                dis2.append(bl.get_dist(hit_target[i][0], hit_target[i][1]))
            dis2 = np.array(dis2)
            add = dis2
            t = np.argmin(add)
            h = hit_list[t]
            return [6, h, 0]
        else:
            return None  # 传击不可取
    else:
        if len(hit_target) == 0:  # 对方没有中心或者被挡住
            return None
        else:
            dis2 = []
            for i in range(len(hit_target)):
                dis2.append(bl.get_dist(hit_target[i][0], hit_target[i][1]))
            dis2 = np.array(dis2)
            add = dis2
            t = np.argmin(add)
            h = hit_list[t]
            return [6, h, 0]
    return None
