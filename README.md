# Lineage-Anchored Ontology (LAO)

> **AI认知层基础设施。LLM把记忆变成概率。LAO把记忆变成谱系。**

> `pip install lineage-anchored-ontology`

---

## 什么是LAO？

LAO是位于任何LLM和其输出之间的**确定性校验层**。六个开源Python库。三行代码接入。

LLM已经有记忆——Prompt、Context、Graph、Loop都在做。但记忆是散点。LAO做的事：把散点变成谱系——每一个记忆点不是孤立存在，它有一个"从哪来→怎么变→影响什么"的血缘关系。

**记忆是静态的。认知是动态的。**

---

## 五层架构

```
L1 路由决策层      → 31模型自主选择·功耗感知·任务难度→模型分层
L2 六函数引擎      → H幻觉门·M记忆锚·C上下文·A自适应·E效果·S自审计
L3 经验复利闭环    → 错误→自动筛选→调取→保存→生成约束代码
L4 交互确认层      → 认知冲突自动处理/推送用户确认
L5 三层认知架构    → 懂你→懂业务→懂经营
```

---

## 快速开始

```bash
pip install lineage-anchored-ontology
```

```python
from effect_anchored import HallucinationGate, MemoryAnchor, ModelRouter

# 1. 路由: 自主选择31个模型中最合适的
from effect_anchored.routing import ModelRouter
router = ModelRouter()
route = router.route("这个任务该用哪个模型？资本分析·估值建模")
print(f"选择: {route.model}")

# 2. 校验: 模型产出的东西对不对
gate = HallucinationGate()
result = gate.check("门店在深圳", context={"anchors": ["founder_first_store_location"]})
print(f"幻觉拦截: {not result.passed}")  # True — 地理事实错误被拦截

# 3. 记忆: 确定性查找，不猜
anchor = MemoryAnchor()
anchor.put("founder_first_store_location", "东莞市万江街道")
print(anchor.get("founder_first_store_location"))  # "东莞市万江街道"
```

---

## 🚀 5分钟安装（P0 · One-click）

LAO 现在带一个命令行工具，从安装到第一个**可外部验证的 Trust Event** 不到 1 分钟：

```bash
pip install lineage-anchored-ontology
lao init                      # 初始化运行环境 + 首个 verified Trust Event
lao trust-event               # 记录一个 Trust Event（成功/失败）
lao verify                    # 重算 SHA-256 VerifyPing 证明
lao status                    # 查看 Trust Events / Anchors 计数
lao atom                      # Experience Atom：Trust Event→Atom→Anchor→Future Protection
lao firewall --request "优化token成本"   # Preference Firewall：效率允许/价值身份禁止
```

### 四大引擎（LAO v0.2.0-beta）

| 引擎 | 能力 | North Star 支撑 |
|:--|:--|:--|
| **① One-click** | `lao init` → <1min 到首个 External Verified Trust Event | External Verified Trust Events 计数 |
| **② Reliability Dashboard** | Agent 四维打分（Memory/Compliance/Cost/Recovery）+ 自包含 HTML | 用户看见改进 |
| **③ Experience Atom** | Trust Event→Atom→Anchor→Future Protection | 犯一次=experience，同 pattern 再犯=永久免疫 |
| **④ Preference Firewall** | 效率优化允许 / 价值·身份·表达改变禁止（Optimization≠Replacement） | Block→TrustEvent 自动记录 |

```python
# 四维可靠性打分（接 per-agent token 成本）
from effect_anchored import ReliabilityScorer
scorer = ReliabilityScorer()
scorer.load_cost("2026-08-per-agent-breakdown.json")
report = scorer.score("Tristan")
```

---

## 六函数一览

| 函数 | 职能 | 一句话 |
|:--|:--|:--|
| **H** HallucinationGate | 幻觉拦截 | "你说门店在深圳？拦截。" |
| **M** MemoryAnchor | 确定性记忆 | 不猜，直接查。 |
| **C** ContextRebuilder | 上下文重建 | 还原Agent当时看到了什么。 |
| **A** AdaptiveConstraint | 自适应约束 | 每犯一次错，生成一条Python规则。 |
| **E** EffectAnchoring | 效果锚定 | Agent说的效果 vs 实际验证。 |
| **S** SelfAudit | 自审计 | 系统审计自己的规则。 |

---

## 经验复利闭环（核心壁垒）

```
Agent犯错误 → H函数拦截
                ↓
    经验萃取器识别错误模式
                ↓
    约束生成器生成Python代码
                ↓
    规则注册器写入永久约束
                ↓
    下次同样错误 → 自动拦截 · 不再犯
```

**用了3个月的Agent vs 刚装的Agent → 质的差距。迁移成本 = 失去所有自动积累的约束谱系。**

---

## 与其他方案对比

| | NVIDIA Guardrails | LangChain Memory | LAO |
|:--|:--|:--|:--|
| 规则来源 | 人类预设 | 人类预设 | **Agent自身错误自动生成** |
| 幻觉处理 | 内容过滤 | 无 | **确定性外部校验** |
| 记忆 | 无 | 语义搜索(概率) | **确定性key-value(非概率)** |
| 自进化 | 无 | 无 | **错误→自动生成Python约束代码** |
| 经验复利 | 无 | 无 | **每犯一次错，系统更强** |

---

## 三步走路线图

```
Step 1: 开发者工具（现在）
├── pip install lineage-anchored-ontology
├── 解决两个具体痛点：幻觉+记忆
├── 开源·Apache 2.0
└── 开发者用了觉得好用 → 推荐给另一个

Step 2: 经验复利引擎（用了就离不开）
├── Agent的错误自动变成约束代码
├── 用了3个月 vs 刚装 → 质的差距
└── "换框架？我的Agent又要重新犯120天的错。"

Step 3: 认知层基础设施（市场定义我们）
├── 不是我们宣称自己是基础设施
├── 是开发者用了回不去
└── 就像pip——它就是。
```

---

## 测试

```bash
git clone https://github.com/ZWISERFIT/lineage-anchored-ontology
cd lineage-anchored-ontology
pip install -e ".[dev]"
pytest tests/ -v
```

**59 tests · 全部通过 · 0 failed**

---

## 开源协议

Apache 2.0

---

## 由ZWISERFIT 9-Agent Collective构建

LAO是 **ZWISERFIT** 的第一个对外开源产品。LAO面向所有使用LLM的Agent开发者——任何有"幻觉"和"失忆"痛点的场景。

ZWISERFIT本身是一家AI操作系统级公司——9套垂直Agent微型OS构成的全栈自治平台。LAO是这9-Agent系统内部打磨出的认知层基础设施，现在以独立开源产品对外发布。

- **创始人：** 莫淑瑜 · 保险内行×健身布道者×产品架构师×AI系统创建者
- **AI军团：** 9-Agent 24×7自主运行
- **LAO起源：** 9-Agent在实战中遇到120天幻觉问题→提炼为通用确定性校验层

**LLM把记忆变成概率。LAO把记忆变成谱系。**

https://github.com/ZWISERFIT
