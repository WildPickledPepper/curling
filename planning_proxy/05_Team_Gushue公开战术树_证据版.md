# Team Gushue 公开战术树（证据版）

## 先说明这份文档的边界

这不是宣称拿到了 Brad Gushue 队的私有战术手册。公开资料里没有任何顶尖队伍发布“遇到每一种局面该投哪一颗壶”的完整内部策略树。

本文件只做两件事：

1. 记录公开比赛报道、队长访谈中**直接可核验**的 Team Gushue 布局和决策；
2. 将这些已经发生过的决策，整理成不含连续出手参数的“公开行为树”。

每个节点都标出证据。没有被公开材料直接支持的推论，绝不写成“Gushue 队就是这么规定的”。我们自己的路径求解器只能执行树给出的**离散目标区域**，不能反过来给 Team Gushue 编造私有战术。

## 为什么选 Team Gushue

Team Gushue 是可以找到较多公开战术复盘的顶尖队伍。其公开表述有一个非常清楚的总原则：

> 前半局主动争取领先；拿到领先后，在后半局通过控制局面守住领先。

这是 Brad Gushue 在 2022 泛大陆锦标赛公开说出的思路：他们前半场更激进地让壶到位、争取领先，随后再控制比赛；该场面对多颗加拿大守壶时，日本被迫尝试长距离 runback 和 raise。[Curling Canada 赛后报道](https://www.curling.ca/blog/2022/11/05/final-destination/)

这和“每颗壶都无脑清掉”不同：前半局愿意制造复杂度；领先后才主动降低复杂度。

## 从公开比赛中抽出的布局原则

### 原则一：前半局要把壶放进正确位置，而不是只追求清场

Gushue 的公开表述是：冰面会逐渐变难，因此早期把关键壶放到位、争取领先很重要；有了领先再控制后半局。[Curling Canada，2022](https://www.curling.ca/blog/2022/11/05/final-destination/)

已观察到的布局结果：加拿大在前方有多颗守壶，己方得分壶在四英尺和按钮附近、且处于掩护后；对手因此不得不选择长距离 raise/runback。[同上](https://www.curling.ca/blog/2022/11/05/final-destination/)

**离散含义：**

```text
前半局、尚未领先
    不要把“敌壶数量=0”当唯一目标
    优先建立：前方掩护 + 营内可得分壶 + 后续可继续加壶的通道
```

这里的“掩护”不是说一颗中线守壶能绝对保护后方壶；它是让对方的有效反击变成长 runback、raise、绕壶或穿窄门。我们的 PhysX 已证明单中线守壶不足以保证后方壶不被旋进清掉，因此该节点必须把对方的旋进反击也交给严格验证。

### 原则二：对方双中线守壶时，不把己方壶堆进同一条中线

2018 年 Team Mouat 对 Team Drummond 的冠军赛复盘记录了一个很具体的高水平应对：对方摆出两颗中线守壶后，Mouat 先把前两颗壶 draw 到两翼；随后通过清中路、hit-and-roll、angle promote 把局面转回可得分的形状。[苏格兰冰壶协会比赛复盘](https://www.scottishcurling.org/scottish-curling-championships-2018-mens-final-match-report/)

这不是 Team Gushue 的私有做法，但它是顶尖队伍面对双中线压力时的公开真实范例，纳入树中作为“中线堵死时的标准分支”。

**离散含义：**

```text
中线有两颗有效守壶，直进中路被堵
    → 先在左/右翼建立可得分壶，不再追加同线中线壶
    → 之后找清中、hit-and-roll 或角度 promote 的机会
```

### 原则三：领先后，把对方逼到长距离、高难度反击，而非硬保所有己方壶

2022 年 Gushue 队在前方布有多颗守壶、营内有三颗得分壶时，对方只能尝试长距离 runback/raise，最终失败，加拿大偷到三分。[Curling Canada，2022](https://www.curling.ca/blog/2022/11/05/final-destination/)

这条证据支持的不是“守壶不可突破”，而是：

```text
领先 / 想偷分
    → 保留会让对方必须做长距离 raise、runback、窄门 draw 的前方结构
    → 不必执着每颗己方壶永远在场
    → 只要对方最容易的得分路线被抬高，就达到了防守目的
```

### 原则四：对手把壶藏在掩护后，不只用一类清壶

2026 奥运会加拿大—英国男队金牌赛复盘中，双方在中线守壶附近交换 soft-weight hit；当营内两颗壶“焊”在按钮附近时，另一方被迫尝试 double takeout。比赛也出现了 hit-and-roll、穿 port 的 draw、raise 等不同处理，而不是只用高速直线打定。[Grand Slam of Curling 比赛复盘](https://www.thegrandslamofcurling.com/news/canada-great-britain-mens-curling-gold-medal-game-recap)

**离散含义：**

```text
对方壶被掩护
    若有直接清壶路线：打定 / 双飞
    若直接路线被守壶遮挡：soft hit-and-roll、raise、穿门 draw、或先清守壶
    不把“直线打不到”误判成“这颗壶安全”
```

这和我们刚做出的中线守壶反证一致：后方壶是否安全，要看对方是否存在可用绕行和碰撞链，而不是只看正面直线是否被挡。

### 原则五：局面不利或需要保留后手时，主动清空并 blank

2024 世界男子锦标赛决赛的公开复盘中，瑞典通过 runback 和 peel 清理守壶区，阻止 Gushue 建立激进局；Gushue 自己也曾用 hit-and-roll out 尝试 blank。该场面说明“清空、不给对方继续堆壶、保留后手”是顶尖队伍的真实分支，而不是保守失误。[Curling Canada 赛后刊物，第 28 页](https://www.curling.ca/wp-content/uploads/2025/06/EE24_Final_Updated1125-1.pdf)

**离散含义：**

```text
我方后手，且当前最多只能拿 1 分、但强行进攻会给对方偷分机会
    → 清守壶 / 清营内关键壶
    → 让本局成为 blank 或低复杂度单分局
```

## 公开行为树

下面的树只使用上述公开证据能支撑的决策顺序。它不是任何一支队伍的私有完整 playbook；每条叶子只是“布局目标”，连续参数仍由本项目求解器搜索。

```text
开始一局
│
├─ 我方有最后一壶（后手）？
│  │
│  ├─ 是
│  │  ├─ 当前可争取两分以上？
│  │  │  ├─ 是 → 用边翼/角落和营内壶展开；保留通往四英尺的最后一路
│  │  │  └─ 否 → 清守壶、降低壶数；若强攻会被偷分，目标改为 blank 或稳拿一分
│  │  │
│  │  └─ 对方用中线壶把中路堵死？
│  │     ├─ 是 → 优先向两翼 draw；等待 hit-and-roll、清中或 promote 机会
│  │     └─ 否 → 继续在一侧形成“守壶 + 营内壶”的得分通道
│  │
│  └─ 否（我方先手）
│     ├─ 前半局、需要制造偷分压力？
│     │  ├─ 是 → 中线守壶可作为中路压力来源；营内壶必须严格测试对方旋进绕行
│     │  └─ 否 / 已领先 → 把局面压向中路，减少对方左右展开；优先限制其两分机会
│     │
│     └─ 对方已有有效营内壶？
│        ├─ 有直接路线 → takeout / double / hit-and-roll，清掉最近威胁
│        └─ 被守壶遮挡 → 比较 raise、soft hit-and-roll、穿门 draw、先清守壶；
│                         不能默认后方壶安全
│
└─ 任意时刻：当前候选布局是否让对方最容易的反击变成高概率得分？
   ├─ 是 → 拒绝该布局，改选另一侧 / 清场 / blank 分支
   └─ 否 → 交给路径求解器搜索具体落点，并用严格 PhysX 多摩擦序列复核
```

## 如何接入我们的系统

这份树在本项目中只输出离散意图，不输出 `v/h/w`：

| 树的叶子 | 给路径求解器的目标 |
| --- | --- |
| 两翼展开 | 左翼或右翼的营内目标区；另一侧留给下一颗壶。 |
| 中线压力 | 中线守壶区，但不把它视作后方壶的绝对掩护。 |
| 清中 / 清守壶 | 指定要处理的壶和允许的滚位区。 |
| hit-and-roll | 指定敌方目标壶 + 己方出手壶的滚位区。 |
| raise / promote | 指定被撞己方壶、目标区和允许牺牲数。 |
| blank | 严格 PhysX 下搜索双方营内无有效得分壶、我方不留下对方两分机会的清场结果。 |

每个叶子都必须经过：

```text
离散布局目标 → 粗代理筛连续路线 → 严格 PhysX 多摩擦序列复核 → 对手反击搜索
```

## 不能从公开资料假装知道的事

以下内容没有公开、逐局可复用的 Team Gushue 完整资料，因此不写死：

- 他们每一种比分、每一局、每一颗壶的固定坐标；
- 他们对某条旋进或 raise 的内部成功率阈值；
- 他们如何针对某一具体对手调整树；
- 他们的扫冰判断和临场冰况修正；
- 他们的私有赛前准备、视频数据库和通信规则。

这些必须由我们的 PhysX 验证、比赛限制和后续对局数据补齐，不能假称来自 Team Gushue。

## 资料索引

1. [Team Gushue 2022：早期激进建立领先，随后控制比赛](https://www.curling.ca/blog/2022/11/05/final-destination/)
2. [Team Mouat 2018：双中线守壶下两翼 draw、清中、hit-and-roll、promote 的完整比赛复盘](https://www.scottishcurling.org/scottish-curling-championships-2018-mens-final-match-report/)
3. [2026 加拿大—英国金牌赛：中线守壶附近的 soft hit、raise、double、port draw](https://www.thegrandslamofcurling.com/news/canada-great-britain-mens-curling-gold-medal-game-recap)
4. [2024 世界赛决赛：runback/peel 阻止对方建立激进局，及 blank 分支](https://www.curling.ca/wp-content/uploads/2025/06/EE24_Final_Updated1125-1.pdf)
