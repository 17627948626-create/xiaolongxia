# XIAOLONGXIA_WRITER_LITE.md

## 定位

这不是第二套写作流程，也不是 `wechat-article-forge` 的替身。

它只做两件事：
1. **写前轻适配**：把主 agent 已定下的题，压成一张最小作战卡 `writer-lite-brief.json`
2. **写后红灯预检**：在 Writer 初稿完成、Reviewer 介入前，做一次只抓 hard fail 的 `writer-lite-check.json`

硬边界：
- 不改 `wechat-article-forge` 本体
- 不新增中间编排层
- 不新增第二 reviewer / 第二 writer / 第二 Humanizer
- lite 只是 **caller-side adapter + preflight gate**
- lite **不打分**、**不替代 reviewer**、**不做最终通过判断**

---

## 本虾写作原型（只保留 4 型）

> 这些原型只能当“判别式 / 约束”，不能当固定模板、开头配方或句式清单。

### 1) 热点解读型
适用判别：
- 最近 48 小时内有明确热点入口，读者已经在搜、在聊、在转
- 文章任务不是复述新闻，而是解释“这事为什么值得今天看”
- 必须能给出一个可复述的判断，而不是信息搬运

不适用时：
- 只有热度，没有判断
- 写完像热点汇总或资讯摘抄

### 2) 事故复盘型
适用判别：
- 有翻车、争议、故障、误判、演示失手等事件
- 文章核心是借事故暴露底层问题：流程脆点、产品幻觉、行业误解、系统约束
- 复盘必须能落到“为什么会这样”和“后面会怎样”

不适用时：
- 只是吃瓜，没有结构性结论
- 只批评表面，没有抽出机制

### 3) 爆产品体验型
适用判别：
- 有单一爆产品 / 爆 demo / 爆更新做入口
- 可以从真实体验、公开演示、可观察行为中提炼判断
- 重点是“它真正改变了什么 / 没改变什么”，不是功能列表

不适用时：
- 文章主体变成产品说明书
- 只写新鲜感，不写使用后果和边界

### 4) 方法论型（慎用）
适用判别：
- 不是凭空抽象输出，必须挂在明确案例、重复性误解或刚发生的触发点上
- 必须能解释一个读者现在就会遇到的问题
- 只有在入口仍然够强时，才适合晚 8 点主发

不适用时：
- 没有 why-now，只是作者想讲道理
- 纯观点空转，脱离具体事件和读者感知

---

## 明确“不借”的 khazix 元素

本虾 lite 只借“约束意识”，**不借**以下具体壳子：
- 不借口癖、招牌话头、习惯性自我称呼
- 不借标点禁令式写法纪律（不搞“一刀切禁用某标点/某句式”）
- 不借默认长文长度设定（不预设越长越像正稿）
- 不借“无小标题执念”（能不能分节服从内容，不做形式崇拜）
- 不借过强个人叙事外壳（不能让“我”压过事件、判断和读者获得）

---

## AI 边界角色矩阵

| 角色 | 能做什么 | 不能做什么 |
|---|---|---|
| 主 agent | 选题拍板；读取本文件；生成并批准 `writer-lite-brief.json`；在 Writer 初稿后运行 lite preflight；决定阻塞还是 advisory；决定是否接受 Researcher 的证据型纠偏 | 不能把 brief 批准权下放给下游角色 |
| Researcher | 围绕已定题补证、校验、提证据型纠偏建议；若主入口证据失效，可建议修正 brief | 不能自行改 brief；不能偷换选题；不能把建议直接写成批准结果 |
| Writer | 在已锁定的 `hot_hook` / `thesis` / `ai_punchline` 内，写出**最有作者感、最能被复述**的一版初稿；主动保住 **1 个可转述判断、1 个截图级段落、1 个具体情绪场景** | 不能改 brief；不能自行换 prototype / thesis / 结构主轴；不能把“三保住”误当成新增 blocker 清单 |
| Reviewer | 依据 reviewer rubric 做主审；是 primary adjudicator；默认保持对长上游上下文的独立性，必要时只看最小必要 brief 摘要做一致性核对 | 不能直接改 brief；不能把 lite check 或 brief 当自己的评分标准；不能要求完整 prototype / outline |
| Humanizer | 清理 AI 味、节奏、机械腔，保留本虾声音 | 不能扩权改 brief；不能重写成另一种人格；不能借机改题；**不能补逻辑、不能补事实、不能改 thesis** |
| Layout | 做公众号排版与格式收口 | 不能改 brief；不能改文风主轴；不能借排版名义改 thesis |

### Writer 创作目标（不是 blocker）

Writer 的任务不是先替 Reviewer 把所有优化题都提前做完，而是在已锁定方向内把稿子写活。

因此，Writer 首稿默认要尽量保住三样东西：
- **1 个可转述判断**：读者看完能直接复述的一句话结论
- **1 个截图级段落**：值得被单独截出来传播的一段
- **1 个具体情绪场景**：不是抽象态度，而是读者能感到 tension 的真实场景

这“三保住”是**创作目标**，用于保护锋芒和作者感；**不是** lite / review 新增的一套 blocker checklist。

---

## outline / brief 分轨（硬规则）

这轮以后，`outline` 和 `writer-lite-brief` 必须彻底分轨，不能再互相污染。

### `outline` 是什么

`outline` = **prose-safe 正文蓝图**。

它只允许出现：
- 可直接展开成正文的小节标题
- 每节的内容要点 / 证据点 / 推进关系
- 对读者可见的正常 prose 级表述

它**不允许**出现：
- 任何 planning labels / placeholders / note-to-writer
- 任何后台调度语、创作纪律语、流程提醒语
- 例如：`[截图级段落位置]` / `[具体情绪场景位置]` / `[可转述判断位置]`
- 例如：`结尾别升太大` / `不要写成...` / `最后一节只做两件事`

一句话：`outline` 是给正文展开用的，不是给 Writer 看的后台便签。

### `writer-lite-brief` 是什么

`writer-lite-brief` = **创作边界 / 目标 / 禁区 / 节奏提醒 / 不要写成什么**。

它负责锁：
- 方向边界
- 核心判断
- 必保住的东西
- 明确不能踩的坑

它不负责给出段落施工图，不替 Writer 设计正文展开方式。

---

## 最小结构化事实侧车（给 Writer / lite preflight 消费）

为了防止“事实口径越界”，但又不把 Writer 压成保守改写器，research 侧至少要允许挂一个**最小结构化高风险事实载体**（可放在 `research.json.fact_records` 或等价字段）。

核心原则不是“禁止判断”，而是：

> **禁止无标识写强。**

也就是：
- **源事实**：可直接陈述
- **归纳 / 推断**：允许写，但必须显式是判断，不能伪装成 source 原话
- **作者观点**：允许更强表达，但不能借 source 背书

最小字段至少覆盖：
- `kind: "api_snapshot"` → **必须带 `observed_at`**
- `quote_mode: "paraphrase_only" | "verbatim"`
- `kind: "readme_claim"` + `attribution_required`
- `file_size_bytes` + `unit`
- 可选：`needle` / `claim`，供 lite preflight 做机械匹配

---

## `writer-lite-brief.json` 最小结构

这个文件只服务于“把题压清楚”，不是长 prompt。

### brief 锁定边界（硬规则）

- `writer-lite-brief` **只能锁方向，不能锁成文方案**
- 锁的是**角度边界**，不是段落设计
- 锁的是**核心判断**，不是修辞路线
- Writer 对**结构展开、节奏安排、具体表达**仍有主导权
- `must_keep` / `must_avoid` 默认都应极短，建议**各不超过 3 条**；超过这个长度，说明 brief 已开始替 Writer 写稿

必填字段：
- `draft_version`
- `updated_at`
- `change_reason`
- `prototype`
- `hot_hook`
- `thesis`
- `ai_punchline`
- `must_keep`
- `must_avoid`

可选字段：
- `why_fit`（一句话）
- `downstream_boundary`（一句话）

最小示意：

```json
{
  "draft_version": "draft-v1",
  "updated_at": "2026-04-07T11:30:00+08:00",
  "change_reason": "topic locked; generate lite brief before research",
  "prototype": "事故复盘型",
  "hot_hook": "一句话说明最近这件热点为什么会把人拉进来",
  "thesis": "一句话讲清本虾真正判断",
  "ai_punchline": "一句话说明 AI 视角补刀点",
  "must_keep": ["必须保住的判断或段落任务"],
  "must_avoid": ["明确不能写成什么"],
  "why_fit": "一句话说明为什么这个 prototype 合适",
  "downstream_boundary": "一句话说明下游只能执行、不能偷换方向"
}
```

---

## lite preflight（红灯预检）规则

### 定位
- 这是 **preflight gate**，不是 reviewer rubric
- 只抓 **有限、可枚举、可机械判定** 的红灯
- 不打分
- 不输出风格建议
- 不做第二 reviewer
- 默认只在 **Writer 首稿进 review 前** 跑一次
- 最多只允许 **一次 pre-review 打回**，不得无限返修

### 允许检查的机械红灯（有限集合）
只检查下面这些，不能再膨胀：

1. **脚手架 / placeholder 残留**
   - 如 `[截图级段落位置]` / `note-to-writer` / `不要写成...`
2. **动态数字缺时点**
   - 尤其是 `api_snapshot` / stars / forks / 下载量 / 用户数 等动态数
   - 没有 `observed_at` 或正文未写出时点时，直接红灯
3. **假直引 / 假 verbatim**
   - `paraphrase_only` 的材料被写成带引号原话
   - 正文出现直引，但 research 里没有对应 `verbatim` 支撑
4. **README / 自我描述被写成已验证实证**
   - `readme_claim` 且 `attribution_required=true` 的内容，如果正文没标明是 README / 项目自述 / 仓库说明，就红灯
5. **bytes / size 被写成人类字数**
   - 如 `16790 bytes` 被写成 `1.6 万字`

除此之外，lite 不该拦截。比如：
- “这段还不够炸”
- “传播性还能更强”
- “节奏还能更顺”
- “像不像爆文”

这些都不属于 lite。

### hard block / advisory 语义
- 默认 `check_mode = blocking`
- 命中上述机械红灯时，记为 `hard_block`
- 当主 agent 认定进入时间紧张窗口时，lite 自动降级为 `advisory`
- 降级后仍要记录风险，但**不再阻塞** review / publish

### 重跑条件
只有修改触及以下任一范围时，才必须重跑 lite preflight：
- 标题
- 开头 300 字
- `thesis`
- 结构主轴

如果只是补证据、修个别句子、调排版、去 AI 味，不强制重跑。

### 与 Reviewer 的关系（硬规则）
- `lite check = preflight gate`
- `reviewer rubric = primary adjudicator`
- 最终通过/否决只看 `weighted_total`
- severe issues 并进评分，不再单列 blocker gate
- lite 不做最终通过/否决
- lite 不替代 reviewer

### 重复严重问题收敛规则（新增硬规则）

当同一类 **severe issue** 在连续两轮 review 中仍明显压分时，主 agent 不得再把 reviewer 原话原封不动丢给 Writer 做“继续优化”。必须先把它压成**原子改稿合同**，再允许进入下一轮 Writer。

原子改稿合同至少要包含：
- `issue_id`（同一问题的稳定名字）
- `why_still_failing`（一句话说明为何上一轮没清掉）
- `rewrite_budget`（这轮只准改哪几处，不准扩散）
- `must_replace`（必须改掉的具体句子 / 句式 / 段落起手）
- `max_keep`（最多允许保留几处同类表达）
- `preserve`（必须保住的判断/段落，防止越改越空）

如果主 agent 没先把重复 severe issue 压成这种合同，就不应继续放 Writer 下一轮。

### 表达层严重问题的 fail-closed 规则（新增硬规则）

像“模板味过重”“高频固定句式”“作者感被同一骨架压住”这类**表达层 severe issue**，一旦被 Reviewer 在 `critical_issues` 中明确指出，或连续两轮显著拉低 `Voice` / `Completion Power`，就不能再按普通 upgrade suggestion 处理。

具体执行：
- 同类表达层 severe issue **第一次出现**：允许正常改一轮
- **第二次仍未清**：必须进入“原子改稿合同”模式
- **第三次仍未清**：默认停止自动改稿，转主 agent / 老板人工判断，不再继续靠 Writer 同构迭代硬磨

目的不是减少严格度，而是防止“同一个严重问题连提三次，但改稿指令始终不够可执行”的空转。
- lite 不输出风格建议池
- Reviewer 默认保持对长上游上下文的独立性；只有确实需要做一致性核对时，才允许传**最小必要 brief 摘要**，且该摘要不是评分标准，更不能传完整 prototype / outline

---

## Humanizer 边界（单列写死）

Humanizer 不是救火队，只负责清理表达层问题：
- 可以清理 AI 味、机械腔、节奏僵硬、重复句式
- **不能补逻辑**
- **不能补事实**
- **不能改 thesis**

如果稿子需要补的是逻辑、事实、核心判断成立性，必须回退上游（Writer / Research / Review 前链路）处理，**不允许在 Humanizer 环节就地硬修**。

---

## `writer-lite-check.json` 最小结构

必填字段：
- `draft_version`
- `updated_at`
- `change_reason`
- `check_mode`（`blocking` 或 `advisory`）
- `hard_fail`
- `hard_fail_reasons`

建议附带：
- `checks[]`（有限机械检查结果）
- `preflight_scope = mechanical_red_lights_only`
- `max_pre_review_bounces = 1`
- `generated_at`
- `generator`（至少标明脚本名/路径）
- `input_fingerprints`（至少要有 `draft_sha256`，最好同时带 `brief_sha256` / `research_sha256`）
- `artifact_contract = script_generated_only`
- `blocking_enforced`（明确这次是 blocking 还是 advisory 降级）

最小示意：

```json
{
  "draft_version": "draft-v1",
  "generated_at": "2026-04-07T12:10:00Z",
  "updated_at": "2026-04-07T12:10:00Z",
  "change_reason": "writer first draft completed; run lite preflight before review",
  "check_mode": "blocking",
  "hard_fail": false,
  "hard_fail_reasons": [],
  "checks": [],
  "preflight_scope": "mechanical_red_lights_only",
  "artifact_contract": "script_generated_only",
  "blocking_enforced": false,
  "generator": {
    "name": "writer_lite_preflight.py"
  },
  "input_fingerprints": {
    "draft_sha256": "..."
  },
  "max_pre_review_bounces": 1
}
```

---

## 运行时 durable sidecar 规则

- `writer-lite-brief.json` 与 `writer-lite-check.json` 必须绑定到**具体 draft version**
- 两个文件里至少都要有：`draft_version` / `updated_at` / `change_reason`
- `writer-lite-check.json` **必须由脚本原样生成**；不能手工补一个 JSON、也不能拿旧 sidecar 冒充“这版已经跑过 preflight”
- durable 证据至少要能回答两件事：**是谁生成的**（generator / script）和**针对哪份输入生成的**（`draft_sha256`，以及可选的 brief/research 指纹）
- 一旦 draft version 变化，旧 `writer-lite-check.json` 视为**过期**，不能拿旧检查结果覆盖新稿
- 不要求每次微调都落盘；建议只在以下时点写 durable 文件：
  1. 首稿进 review 前
  2. 被打回重写时
  3. 最终过稿时
- durable sidecar 只记录“这版稿子的方向约束”和“这版稿子是否命中红灯”，不承载第二套评分体系
