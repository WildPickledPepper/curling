import json
from typing import List, Tuple, Union
Coordinate = List[float]
StateList = List[Coordinate]
import numpy as np
from pathlib import Path
# 初始化参数
Stone_R: float = 0.145              # 壶半径
House_R: float = 1.830              # 大本营半径
flag: int = 0
score: int = 0
shot_num:int=0
# 从文件中加载巨型数组
json_path = Path(__file__).parent/'data'/'data.json'
with open(json_path, 'r') as f:
    loaded_data = json.load(f)
feature = np.array(loaded_data['feature'])
v = np.array(loaded_data["v"])
feature_roll=np.array(loaded_data['feature_roll'])
v_roll=np.array(loaded_data["v_roll"])
feature_roll_pro=np.array(loaded_data['feature_roll_pro'])
h_roll_pro=np.array(loaded_data['h_roll_pro'])
feature_roll_extension=np.array(loaded_data['feature_roll_extension'])
v_roll_extension=np.array(loaded_data["v_roll_extension"])
feature_roll_max=np.array(loaded_data['feature_roll_max'])
h_roll_max=np.array(loaded_data['h_roll_max'])
vy=np.array(loaded_data['vy'])
vh=np.array(loaded_data['vh'])
vy = np.array(vy, dtype=float)
vh = np.array(vh, dtype=float)
# an= np.polyfit(vy, vh, 4)
# 添加数据检查
vy = np.array(vy, dtype=float)
vh = np.array(vh, dtype=float)

# 检查数据有效性
if len(vy) != len(vh):
    raise ValueError("vy and vh must have the same length")
if len(vy) <= 4:
    raise ValueError("Need at least 5 points for degree-4 polynomial")
if np.any(np.isnan(vy)) or np.any(np.isnan(vh)):
    raise ValueError("Input contains NaN values")
if np.all(vy == vy[0]):  # 所有x值相同
    raise ValueError("x values must not all be identical")

an = np.polyfit(vy, vh, 4)
def feature_v(L: float, L_target: float, angle: float) -> np.ndarray:
    """根据位置参数查找最匹配的速度值。

    通过计算输入参数与预存特征数据的欧氏距离，找到最接近的匹配项并返回对应的速度值。

    Args:
        L: 当前位置的L坐标值。
        L_target: 目标位置的L坐标值。
        angle: 角度参数。

    Returns:
        匹配到的速度值数组。

    Examples:
        >>> v_result = feature_v(1.0, 2.0, 0.5)
    """
    d: np.ndarray = feature - np.array([L, L_target, angle])
    mean: np.ndarray = sum(feature) / len(feature)
    d = d / mean
    dis: List[float] = []
    for i in range(len(d)):
        dis.append(sum(d[i] ** 2))
    dis = np.array(dis)
    # print(dis)
    t: int = np.argmin(dis)
    # print('v[t]', t, v[t], dis[t])
    return v[t]


def feature_roll_v(L: float, L_target: float, angle: float) -> np.ndarray:
    """根据位置参数查找打甩状态下的最匹配速度值。

    通过计算输入参数与预存打甩特征数据的欧氏距离，找到最接近的匹配项并返回对应的打甩速度值。

    Args:
        L: 当前位置的L坐标值。
        L_target: 目标位置的L坐标值。
        angle: 角度参数。

    Returns:
        匹配到的打甩速度值数组。

    Examples:
        >>> v_roll_result = feature_roll_v(1.0, 2.0, 0.5)
    """
    d: np.ndarray = feature_roll - np.array([L, L_target, angle])
    mean: np.ndarray = sum(feature_roll) / len(feature_roll)
    d = d / mean
    dis: List[float] = []
    for i in range(len(d)):
        dis.append(sum(d[i] ** 2))
    dis = np.array(dis)
    # print(dis)
    t: int = np.argmin(dis)
    # print('v[t]', t, v_roll[t], dis[t])
    return v_roll[t]


def feature_roll_v_pro(L_target: float) -> np.ndarray:
    """根据目标位置查找相应打甩模式下的速度偏移量。

    通过计算目标位置与预存相应打甩特征数据的绝对差值，找到最接近的匹配项并返回对应的偏移量。

    Args:
        L_target: 目标位置的L坐标值。

    Returns:
        匹配到的打甩偏移量数组。

    Examples:
        >>> h_result = feature_roll_v_pro(2.0)
    """
    # print(feature_roll_pro)
    d: np.ndarray = abs(feature_roll_pro - np.array([L_target]))
    # print(d)
    t: int = np.argmin(d)
    # print('h_list[t]', t, h_roll_pro[t], d[t])
    return h_roll_pro[t]


def feature_roll_v_max(L_target: float) -> np.ndarray:
    """根据目标位置查找最大打甩模式下的速度偏移量。

    通过计算目标位置与预存最大打甩特征数据的绝对差值，找到最接近的匹配项并返回对应的偏移量。

    Args:
        L_target: 目标位置的L坐标值。

    Returns:
        匹配到的最大打甩偏移量数组。

    Examples:
        >>> h_max_result = feature_roll_v_max(2.0)
    """
    # print(feature_roll_max)
    d: np.ndarray = abs(feature_roll_max - np.array([L_target]))
    # print(d)
    t: int = np.argmin(d)
    # print('h_list_max[t]', t, h_roll_max[t], d[t])
    return h_roll_max[t]


def feature_roll_v_extension(L: float, L_target: float) -> np.ndarray:
    """根据扩展位置参数查找打甩状态下的最匹配速度值。

    通过计算输入参数与预存扩展打甩特征数据的欧氏距离，找到最接近的匹配项并返回对应的扩展打甩速度值。

    Args:
        L: 当前位置的L坐标值。
        L_target: 目标位置的L坐标值。

    Returns:
        匹配到的扩展打甩速度值数组。

    Examples:
        >>> v_ext_result = feature_roll_v_extension(1.0, 2.0)
    """
    d: np.ndarray = feature_roll_extension - np.array([L, L_target])
    mean: np.ndarray = sum(feature_roll_extension) / len(feature_roll_extension)
    d = d / mean
    dis: List[float] = []
    for i in range(len(d)):
        dis.append(sum(d[i] ** 2))
    dis = np.array(dis)
    # print(dis)
    t: int = np.argmin(dis)
    # print('v_roll_extension[t]', t, v_roll_extension[t], dis[t])
    return v_roll_extension[t]

# ... existing code ...


def get_dist(x: float, y: float) -> float:
    """计算某一冰壶距离营垒圆心的距离。

    根据给定的坐标点，计算该点到大本营中心点(2.375, 4.88)的欧氏距离。

    Args:
        x: 冰壶的x坐标值。
        y: 冰壶的y坐标值。

    Returns:
        冰壶到营垒圆心的距离值。

    Examples:
        >>> distance = get_dist(2.0, 5.0)
    """
    House_x: float = 2.375
    House_y: float = 4.88
    return np.sqrt((x - House_x) ** 2 + (y - House_y) ** 2)


def y2v(y: float) -> float:
    """根据纵坐标计算速度值。

    使用线性公式将指定位置的纵坐标转换为对应的速度值。

    Args:
        y: 指定位置的纵坐标值。

    Returns:
        计算得到的速度值。

    Examples:
        >>> velocity = y2v(3.5)
    """
    v0: float = float(3.613 - 0.12234 * y - 0.03)
    return v0


def polv2(a: float, b: float, c: float, x: float) -> float:
    """计算二次多项式的值。

    根据给定的系数a、b、c和自变量x，计算二次多项式 ax² + bx + c 的值。

    Args:
        a: 二次项系数。
        b: 一次项系数。
        c: 常数项系数。
        x: 自变量值。

    Returns:
        二次多项式的计算结果。

    Examples:
        >>> result = polv2(1.0, 2.0, 3.0, 4.0)
    """
    return a * x ** 2 + b * x + c


def y2_v(y: float) -> float:
    """根据纵坐标计算速度值（使用预定义的二次多项式系数）。

    使用固定的二次多项式系数将纵坐标转换为速度值。

    Args:
        y: 纵坐标值。

    Returns:
        计算得到的速度值。

    Examples:
        >>> velocity = y2_v(3.5)
    """
    a: float = 0.0015
    b: float = -0.1303
    c: float = 3.5939
    return polv2(a, b, c, y)


def delta_y2v_small(delta_y: float) -> float:
    """计算小范围位移差对应的速度值。

    使用特定的二次多项式系数计算小范围位移差对应的速度值。

    Args:
        delta_y: 小范围的位移差值。

    Returns:
        计算得到的速度值。

    Examples:
        >>> velocity = delta_y2v_small(0.5)
    """
    a: float = 0.0197
    b: float = 0.3085
    c: float = -0.0029
    return polv2(a, b, c, delta_y)


def delta_y2v_sixty(delta_y: float) -> float:
    """计算中等范围位移差对应的速度值。

    使用特定的二次多项式系数计算中等范围位移差对应的速度值。

    Args:
        delta_y: 中等范围的位移差值。

    Returns:
        计算得到的速度值。

    Examples:
        >>> velocity = delta_y2v_sixty(1.5)
    """
    a: float = -0.0475
    b: float = 0.7254
    c: float = -0.2233
    return polv2(a, b, c, delta_y)


def delta_y2v_big(delta_d: float) -> float:
    """计算大范围位移差对应的速度值。

    使用特定的二次多项式系数计算大范围位移差对应的速度值。

    Args:
        delta_d: 大范围的位移差值。

    Returns:
        计算得到的速度值。

    Examples:
        >>> velocity = delta_y2v_big(2.5)
    """
    a: float = -0.0753
    b: float = 0.8398
    c: float = -0.2392
    return polv2(a, b, c, delta_d)


A2: List[float] = [-1.0888625519567436, 15.146724507096334, -8.041637987791214]
B2: List[float] = [0.0014974607605535584, 0.033340081194708056, 0.9394168343117365]
# v-----d v是自变量
A: List[float] = [-1.0876685188763353, 15.134698717429497, -7.955352540931309]
# d----v
B: List[float] = [0.0015457293681138328, 0.030732336127025094, 0.9676122749334959]
A1: List[float] = [-1.1251964014815767, 15.354326724465768, -8.276326115926471]
B1: List[float] = [0.0015454469138129897, 0.030630985013025233, 0.9705507493067392]
C: List[float] = [8.991341073452121, 0.6797309032757026]


def d_v(d: float) -> float:
    """根据距离值计算速度值。

    使用B2系数的二次多项式将距离值转换为速度值。

    Args:
        d: 距离值。

    Returns:
        计算得到的速度值。

    Examples:
        >>> velocity = d_v(5.0)
    """
    return B2[0] * d ** 2 + B2[1] * d + B2[2]


def v_d1(v: float) -> float:
    """根据速度值计算距离值（线性关系）。

    使用C系数的线性公式将速度值转换为距离值。

    Args:
        v: 速度值。

    Returns:
        计算得到的距离值。

    Examples:
        >>> distance = v_d1(3.0)
    """
    return C[0] * v + C[1]


def v_d(v: float) -> float:
    """根据速度值计算距离值。

    使用A2系数的二次多项式将速度值转换为距离值。

    Args:
        v: 速度值。

    Returns:
        计算得到的距离值。

    Examples:
        >>> distance = v_d(3.0)
    """
    return A2[0] * v ** 2 + A2[1] * v + A2[2]


def Dist(c1: Tuple[float, float], c2: Tuple[float, float]) -> float:
    """计算两个冰壶之间的距离。

    根据两个冰壶的坐标，计算它们之间的欧氏距离。

    Args:
        c1: 第一个冰壶的坐标元组 (x, y)。
        c2: 第二个冰壶的坐标元组 (x, y)。

    Returns:
        两个冰壶之间的距离值。

    Examples:
        >>> distance = Dist((1.0, 2.0), (3.0, 4.0))
    """
    return np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def DistH(c: Tuple[float, float]) -> float:
    """计算冰壶与大本营中心的距离。

    根据冰壶坐标，计算该冰壶到大本营中心点(2.375, 4.88)的距离。

    Args:
        c: 冰壶的坐标元组 (x, y)。

    Returns:
        冰壶到大本营中心的距离值。

    Examples:
        >>> distance = DistH((2.0, 5.0))
    """
    return np.sqrt((c[0] - 2.375) ** 2 + (c[1] - 4.88) ** 2)


def House(c: Tuple[float, float]) -> bool:
    """判断冰壶是否在大本营内。

    检查给定坐标的冰壶是否位于大本营的有效范围内（考虑壶半径）。

    Args:
        c: 冰壶的坐标元组 (x, y)。

    Returns:
        如果冰壶在大本营内返回True，否则返回False。

    Examples:
        >>> is_in_house = House((2.0, 5.0))
    """
    if DistH(c) < np.sqrt((House_R + Stone_R) ** 2):
        return True
    else:
        return False


def NearestTarget(state_list: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """按距离大本营中心的远近对冰壶坐标进行排序。

    计算列表中所有冰壶到大本营中心的距离，并按升序排列返回坐标列表。

    Args:
        state_list: 冰壶坐标列表，每个元素为(x, y)元组。

    Returns:
        按距离升序排列的冰壶坐标列表。如果输入为空则返回空列表。

    Examples:
        >>> sorted_stones = NearestTarget([(1.0, 2.0), (3.0, 4.0), (2.0, 5.0)])
    """
    d: List[List[Union[float, int]]] = []
    out_s: List[Tuple[float, float]] = []
    i: int = 0
    if not state_list:
        return []
    for c in state_list:
        d.append([DistH(c), i])
        i += 1
    d = sorted(d)            # 升序
    for j in d:
        out_s.append(state_list[j[1]])
    return out_s


def LocalJudge(target: Tuple[float, float], state_list: List[Tuple[float, float]]) -> Union[bool, List]:
    """判断目标落点是否可行（面向结果）。

    检查目标位置是否与现有冰壶发生碰撞（距离小于两倍壶半径）。

    Args:
        target: 目标落点坐标元组 (x, y)。
        state_list: 所有冰壶坐标列表，每个元素为(x, y)元组。

    Returns:
        如果落点可行返回True，如果与现有冰壶冲突返回False，如果state_list为空返回空列表。

    Examples:
        >>> is_valid = LocalJudge((2.0, 5.0), [(1.0, 2.0), (3.0, 4.0)])
    """
    if not state_list:
        return []
    for i in state_list:
        if (i[0] - target[0]) ** 2 + (i[1] - target[1]) ** 2 < (Stone_R * 2) ** 2:
            return False
    return True




def Roadjudge(s: Tuple[float, float], c: Tuple[float, float], state_list: List[Tuple[float, float]]) -> bool:
    """判断路径是否可行。

    检查从起点s到终点c的路径是否会与其他冰壶发生碰撞。对于非竖直路径使用角度判断，
    对于竖直路径使用边界框判断。注意：距离过长时精度可能出现问题。

    Args:
        s: 起点坐标元组 (x, y)。
        c: 终点坐标元组 (x, y)。
        state_list: 给定壶的坐标列表，每个元素为(x, y)元组。

    Returns:
        如果路径可行返回True，如果存在障碍返回False。

    Examples:
        >>> is_path_valid = Roadjudge((1.0, 2.0), (3.0, 4.0), [(2.0, 3.0)])
    """
    angle: List = []
    s_else: List[Tuple[float, float]] = [i for i in state_list if i != s]
    s_else = [i for i in s_else if i != c]
    for i in s_else:
        if s[0] != c[0]:      # 非竖直(因为竖直路径一般都比较长，不能用角度计算，需要单独讨论)
            d: float = Dist(s, c)           # 两壶壶心距离
            vec1: List[float] = [i[0] - s[0], i[1] - s[1]]    # 第三者与两壶的向量
            vec2: List[float] = [i[0] - c[0], i[1] - c[1]]
            cos_theta: float = np.dot(vec1, vec2) / np.linalg.norm(vec1) / np.linalg.norm(vec2)
            angle = np.arccos(cos_theta)     # 第三者与两壶的夹角
            angle_max: float = 2 * np.arctan(d / 4 / Stone_R)   # 大于这个最大值第三者就会与路径相交
            if angle > angle_max:
                return False
        else:
            if s[1] < c[1]:
                if s[1] <= i[1] <= c[1]:
                    if s[0] - 2 * Stone_R <= i[0] <= s[0] + 2 * Stone_R:
                        return False
            else:
                if c[1] <= i[1] <= s[1]:
                    if s[0] - 2 * Stone_R <= i[0] <= s[0] + 2 * Stone_R:
                        return False
    return True


def Roadjudge_state(s: Tuple[float, float], c: Tuple[float, float], state_list: List[Tuple[float, float]]) -> Union[Tuple[float, float], int]:
    """返回障碍冰壶的坐标。

    检查从起点s到终点c的路径，如果存在障碍则返回第一个障碍冰壶的坐标，否则返回0。

    Args:
        s: 起点坐标元组 (x, y)。
        c: 终点坐标元组 (x, y)。
        state_list: 给定壶的坐标列表，每个元素为(x, y)元组。

    Returns:
        如果存在障碍返回障碍冰壶的坐标元组 (x, y)，否则返回0。

    Examples:
        >>> obstacle = Roadjudge_state((1.0, 2.0), (3.0, 4.0), [(2.0, 3.0)])
    """
    angle: List = []
    s_else: List[Tuple[float, float]] = [i for i in state_list if i != s]
    s_else = [i for i in s_else if i != c]
    a: Union[Tuple[float, float], int] = 0
    for i in s_else:
        if s[0] != c[0]:      # 非竖直(因为竖直路径一般都比较长，不能用角度计算，需要单独讨论)
            d: float = Dist(s, c)           # 两壶壶心距离
            vec1: List[float] = [i[0] - s[0], i[1] - s[1]]    # 第三者与两壶的向量
            vec2: List[float] = [i[0] - c[0], i[1] - c[1]]
            cos_theta: float = np.dot(vec1, vec2) / np.linalg.norm(vec1) / np.linalg.norm(vec2)
            angle = np.arccos(cos_theta)     # 第三者与两壶的夹角
            angle_max: float = 2 * np.arctan(d / 4 / Stone_R)   # 大于这个最大值第三者就会与路径相交
            if angle > angle_max:
                a = i
        else:
            if s[1] < c[1]:
                if s[1] <= i[1] <= c[1]:
                    if s[0] - 2 * Stone_R <= i[0] <= s[0] + 2 * Stone_R:
                        a = i
            else:
                if c[1] <= i[1] <= s[1]:
                    if s[0] - 2 * Stone_R <= i[0] <= s[0] + 2 * Stone_R:
                        a = i
        if a != 0:
            return a
    return 0


def judge_occupy_situation(state_list: List[Tuple[float, float]]) -> List[List[Union[int, bool, List]]]:
    """判断占位区域内的情况以及壶是否为对方的。

    检查左、中、右三个占位区域是否有冰壶，并判断这些冰壶是否属于对方且路径是否畅通。

    Args:
        state_list: 所有冰壶坐标列表，每个元素为(x, y)元组。

    Returns:
        包含三个区域情况的列表 [left, middle, right]，每个区域的格式为：
        [壶的数量, 是否存在对方壶, 需要击打的对方壶坐标]。

    Examples:
        >>> situation = judge_occupy_situation([(1.0, 7.0), (2.5, 8.0)])
    """
    left_x_left: float = 0.545
    left_x_right: float = 2.375 - 3 * Stone_R
    middle_x_left: float = 2.375 - 3 * Stone_R
    middle_x_right: float = 2.375 + 3 * Stone_R
    right_x_left: float = 2.375 + 3 * Stone_R
    right_x_right: float = 4.205
    y_up: float = 6.71
    y_low: float = 9.74
    left: List[Union[int, bool, List]] = [0, False, []]     # 己方为False,对方为True(此处只是初始化为False)
    middle: List[Union[int, bool, List]] = [0, False, []]
    right: List[Union[int, bool, List]] = [0, False, []]
    n: int = 0
    for i in state_list:
        if (i[0] - Stone_R) > left_x_left and (i[0] + Stone_R) < left_x_right and (i[1] - Stone_R) > y_up and (i[1] + Stone_R) < y_low:
            if flag == 0:                 # 本局我方先手
                if n % 2 == 1:            # 该球是对方球
                    left[1] = True
                    if Roadjudge(i, [i[0], 10.61], state_list):
                        left[2] = i
            else:                       # 本局我方后手
                if n % 2 == 0:
                    left[1] = True
                    if Roadjudge(i, [i[0], 10.61], state_list):
                        left[2] = i
            left[0] += 1        # 左边区有球
        if (i[0] - Stone_R) > middle_x_left and (i[0] + Stone_R) < middle_x_right and (i[1] - Stone_R) > y_up and (i[1] + Stone_R) < y_low:
            if flag == 0:                 # 本局我方先手
                if n % 2 == 1:            # 该球是对方球
                    middle[1] = True
                    if Roadjudge(i, [i[0], 10.61], state_list):
                        middle[2] = i
            else:                       # 本局我方后手
                if n % 2 == 0:
                    middle[1] = True
                    if Roadjudge(i, [i[0], 10.61], state_list):
                        middle[2] = i
            # print('state_list', state_list)
            middle[0] += 1        # 中区有球
        if (i[0] - Stone_R) > right_x_left and (i[0] + Stone_R) < right_x_right and (i[1] - Stone_R) > y_up and (i[1] + Stone_R) < y_low:
            if flag == 0:                 # 本局我方先手
                if n % 2 == 1:            # 该球是对方球
                    right[1] = True
                    if Roadjudge(i, [i[0], 10.61], state_list):
                        right[2] = i
            else:                       # 本局我方后手
                if n % 2 == 0:
                    right[1] = True
                    if Roadjudge(i, [i[0], 10.61], state_list):
                        right[2] = i
            right[0] += 1        # 右边区有球
        n += 1
    situation: List[List[Union[int, bool, List]]] = [left, middle, right]
    return situation


def judge_center_situation(state_list: List[Tuple[float, float]]) -> List[Union[int, bool, List]]:
    """判断中心区域是否有壶以及壶是否为对方的。

    检查以大本营中心为圆心、半径为3倍壶半径的区域内是否有冰壶，并判断是否属于对方。

    Args:
        state_list: 所有冰壶坐标列表，每个元素为(x, y)元组。

    Returns:
        包含中心区域情况的列表 [壶的数量, 是否存在对方壶, 需要击打的对方中心壶坐标列表]。

    Examples:
        >>> center_info = judge_center_situation([(2.3, 4.9), (2.5, 5.0)])
    """
    n: int = 0
    c: List[Union[int, bool, List]] = [0, False, []]                   # 是否有壶，是否存在对方壶，需要击打的对方中心壶坐标
    for i in state_list:
        d: float = DistH(i)
        if d <= 3 * Stone_R:
            if flag == 0:                 # 本局我方先手
                if n % 2 == 1:            # 区域内存在对方球
                    c[1] = True
                    c[2].append(i)
            else:                       # 本局我方后手
                if n % 2 == 0:
                    c[1] = True
                    c[2].append(i)
            c[0] += 1
        n += 1
    return c


def double_hit_vertical(s: Coordinate, c: Coordinate, state_list: StateList, is_init: int = flag, shot_num: int = shot_num) -> Union[Coordinate, int]:
    """垂直双飞策略 - 处理两壶接近竖直情况的双飞。

    当两个目标壶的横坐标接近时，计算垂直双飞的击打点。

    Args:
        s: 第一碰撞球的坐标[x, y]。
        c: 第二碰撞球的坐标[x, y]。
        state_list: 所有壶的坐标列表。
        is_init: 先后手标识，0表示我方先手，1表示后手（此策略不使用）。
        shot_num: 当前投球序号（此策略不使用）。

    Returns:
        如果策略可行，返回击打点坐标[point_x, point_y]；
        否则返回0表示不可行。

    Examples:
        >>> result = double_hit_vertical([2.4, 6.0], [2.45, 6.5], [[2.4, 6.0], [2.45, 6.5]])
        >>> print(result)  # [2.4, 6.29] 或 0
    """
    t = np.pi/4
    if np.abs(c[0]-s[0])<=1/2*Stone_R:
        if c[0] - s[0] < 0:      #第二碰撞球在第一碰撞球左侧
            if Roadjudge(s,c,state_list):
                point1 = [s[0],s[1]+2*Stone_R]
            else:
                return 0
        else:
            if Roadjudge(s,c,state_list):
                point1 = [s[0],s[1]+2*Stone_R]
            else:
                return 0
        if Roadjudge(point1,[point1[0],10.61],state_list):
            return point1
        else:
            return 0
    else:
        if c[0] - s[0] < 0:      #第二碰撞球在第一碰撞球左侧
            point2 = [c[0]-2*np.cos(t)*Stone_R,c[1]+2*np.sin(t)*Stone_R]     #二球辅瞄点
            if Roadjudge(s,point2,state_list):
                d = Dist(point2,s)
                D = 2*Stone_R + d
                k = D/d
                delta_x = np.abs(point2[0]-s[0])*(k-1)
                delta_y = np.abs(point2[1]-s[1])*(k-1)
                point1 = [s[0]+delta_x,s[1]+delta_y]
                if Roadjudge(point1,[point1[0],10.61],state_list):
                    return point1
                else:
                    return 0
            else:
                return 0
        else:
            point2 = [c[0]-2*np.cos(t)*Stone_R,c[1]+2*np.sin(t)*Stone_R]     #二球辅瞄点
            if Roadjudge(s,point2,state_list):
                d = Dist(point2,s)
                D = 2*Stone_R + d
                k = D/d
                delta_x = np.abs(point2[0]-s[0])*(k-1)
                delta_y = np.abs(point2[1]-s[1])*(k-1)
                point1 = [s[0]-delta_x,s[1]+delta_y]
                if Roadjudge(point1,[point1[0],10.61],state_list):
                    return point1
                else:
                    return 0
            else:
                return 0