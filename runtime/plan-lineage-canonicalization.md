# Lineage / pipeline-state canonicalization 最小方案

## 结论先说

这次 publish 前反复被 `lineage_audit.py` 判 dirty，不是单点 bug，而是 **状态存在双轨 schema**：

- 一轨是 `pipeline-state.md` 和 `lineage_audit.py` 认可的 **顶层 canonical schema**（`children` / `artifact_provenance`）
- 一轨是运行过程中实际还在写的 **旧/旁路 lineage schema**（`lineage.children` / `lineage.artifact_provenance`，而且字段形状、artifact key、step 名都不一样）

结果就是：运行时“看起来有 lineage”，但 publish gate 真正查的是另一套更严格的 canonical 顶层字段，所以直到 publish 前才暴露。

---

## 1. 根因收敛：为什么写入方式和 audit 认的 canonical 结构会分叉

### 根因 A：当前存在“双写但不同 schema”，且旧 schema 仍被上游阶段当成主记录

`pipeline-state.md` 已明确规定 canonical 顶层结构应该是：

- `children.<step>[]`，每条带 `session_key` / `label` / `model` / `status` / `artifacts`
- `artifact_provenance.<artifact>`，每条带 `producer_type` / `producer_step` / `session_key` / `model`

但这次 run 的 `pipeline-state.json` 里仍同时存在旧的嵌套结构：

- `lineage.children.researcher.status`
- `lineage.children.researcher.artifact_paths.{research_json, outline_md, ...}`
- `lineage.artifact_provenance.draft_md / draft_v2_md / draft_v3_md`
- 旧字段名如 `source_mode`, `step`

这说明：**实际执行链路里，仍有人在写 legacy lineage 结构；canonical 顶层字段没有在同一个统一入口被持续维护。**

### 根因 B：audit 是 strict exact-match，旧结构虽然“语义上差不多”，但它不认

`lineage_audit.py` 的关键判断很严格：

1. `child_has_evidence()` 要求 `children[step][].artifacts` 里的 artifact 名称，和 audit 选中的 artifact **字符串完全一致**。
2. `provenance_ok()` 用 `prov.get(artifact)`，要求 `artifact_provenance` 的 key 和 artifact 名称 **完全一致**。
3. `normalize_children()` / `normalize_artifact_provenance()` 只会做很有限的宽读：
   - 会统一 step alias（如 `writer_revision_v3` → `writer`）
   - 会把 `producer` 映射成 `producer_step`
   - **不会**把 `draft_v3_md` 这种 alias key 自动还原成 `draft-v3.md`
   - **不会**把 `artifact_paths` 自动变成 canonical 的 `artifacts[]`
   - **不会**从嵌套 `lineage.*` 自动提升成顶层 canonical 结构

所以旧结构不是“差一点”，而是 audit 根本没把它当同一种数据。

### 根因 C：artifact 命名口径不统一，basename / absolute path / alias key 混用

这次 state 里至少混了三种 artifact 标识法：

1. canonical basename：`research.json` / `outline.md` / `final.md` / `final-layout.md`
2. absolute path：`/root/.../draft-v4.md` / `/root/.../review-v3.json`
3. legacy alias key：`draft_md` / `draft_v2_md` / `draft_v3_md`

`lineage_audit.py` 对 artifact 的判定不是“同指向文件即可”，而是 **key 和 evidence string 要对上**。因此：

- basename 和 absolute path 一旦混写，就很容易在 `children.artifacts` 与 `artifact_provenance` 之间错位
- alias key（如 `draft_v3_md`）即便内部 `path` 对，也不会被 audit 当成 `draft-v3.md`

### 根因 D：canonicalization 发生得太晚，只在 publish gate 前补，不在步骤完成时落盘

`pipeline-state.md` 的口径是：**每次 spawn 前、每次步骤完成后都要更新 state**。

但这次从现象看，真正可过 audit 的 canonical 顶层字段，是在 publish 前人工补进去后才齐。说明当前链路至少有一段是：

- 子 agent 已经产出 artifact
- 但 canonical 顶层 evidence/provenance 没同步落盘
- 上游阶段继续往下跑
- 到 publish gate 才第一次被严格检查

于是 dirty lineage 不在“产生偏差的那个阶段”暴露，而是滞后到发布前才炸。

---

## 2. 最小修复方案

## 方案目标

不大改 orchestrator 结构，不追求一次性清掉所有历史字段；只做一层 **统一 canonical 写入口**，让所有后续阶段都能稳定写出 audit 认可的顶层字段。

### 是否要新增 helper / script

**建议新增，且应该新增。**

最小可实施做法：新增一个专门的 canonical 写 helper，例如：

- `scripts/sync_lineage_canonical.py`

职责只做两件事：

1. 接收当前 step、session metadata、产物列表
2. 统一回写 `pipeline-state.json` 顶层：
   - `children`
   - `artifact_provenance`
   - `schema_version`
   - `updated_at`

它不负责业务决策，不负责 audit，只负责“把 lineage 证据按唯一 canonical 口径写对”。

为什么要单独 helper：

- 现在分叉的本质就是“多处各写各的”
- 如果继续靠 orchestrator 各阶段内联拼 JSON，很容易再次漂移
- helper 很小，但能把写法收口成一个入口

### 写入时机放在哪些阶段

最小必要写入时机有两个层级：

#### Must-have 时机 1：每个子阶段完成后，立刻写 canonical evidence

至少覆盖：

- researcher 完成后
- writer / 每一轮 revise 完成后
- reviewer 完成后
- humanizer 完成后
- layout 完成后

每次该阶段 artifact 一落盘，就立刻调用 helper，把该阶段的：

- `session_key`
- `label`
- `model`
- `status=done`
- `artifacts`
- 每个 artifact 对应 provenance

同步到顶层 canonical 字段。

这是最关键的一刀：**让 dirty lineage 在产生时就可见，而不是留到 publish 前才发现。**

#### Must-have 时机 2：publish 前继续保留 `lineage_audit.py --write-state`

publish 前 audit 还要保留，但角色从“补救”降成“最终验收 + lazy migration 兜底”。

也就是说：

- 平时靠 helper 持续写对
- publish 前 audit 只做最后 fail-closed 检查
- 不再指望 audit 成为第一次 canonicalization 的地方

### 统一哪几个字段 / 键格式

最小必须统一 4 类：

#### 1) canonical evidence 只认顶层，不再让 `lineage.*` 承担发布权威

发布控制面唯一权威：

- 顶层 `children`
- 顶层 `artifact_provenance`

`lineage.*` 可暂时保留给兼容或调试，但必须降级为：

- 非权威
- 可选镜像
- 不能作为 publish gate 的前提

#### 2) step 名统一成 canonical step

统一只写：

- `researcher`
- `writer`
- `reviewer`
- `humanizer`
- `layout`

不要把这些直接写进 canonical 字段：

- `writer_revision_v2`
- `writer_revision_v3`
- `factfix`
- `rewrite`
- `rework`

这些可以体现在 label 或 artifact 文件名里，但 **canonical `producer_step` 和 `children` bucket 必须只写主 step 名**。

#### 3) artifact key 统一成“draft dir 相对文件名（basename）”

建议 canonical 一律写：

- `research.json`
- `outline.md`
- `draft-v4.md`
- `review-v3.json`
- `final.md`
- `final-layout.md`

不要在 canonical 顶层混写：

- absolute path
- `draft_v3_md` 这种 alias key
- `artifact_paths.{draft_md: /abs/path}` 这种结构

原因：

- `lineage_audit.py` 本身示例和主口径就是文件名
- basename 最稳定、最容易 exact-match
- 同一个 draft_dir 内不存在跨目录歧义

如果业务上还需要 absolute path，可另存为辅助字段，比如 `artifact_paths`，但 **canonical 发布证据只认 basename**。

#### 4) provenance 字段统一成 audit 认可的 4 元组

每个 canonical provenance 至少只保留：

- `producer_type: "child"`
- `producer_step: <canonical step>`
- `session_key`
- `model`

旧字段如：

- `source_mode: child_session`
- `step: writer_revision_v3`
- `path: /root/...`

可以作为兼容附加信息保留在别处，但不应再承担 publish audit 所需的主语义。

---

## 3. 如何避免再次到 publish 前才人工补救

### 核心原则：把 lineage canonicalization 从“发布前补作业”改成“每一步交付即记账”

最小落地方式：

1. **每个子 agent 完成回收结果后，先调用 canonical helper，再推进下一步**
2. **在 step 边界加一个轻量自检**：不是完整 audit，只检查当前 step 的 canonical evidence 是否已写进顶层
3. **publish 前保留完整 audit fail-closed**，但它只应该抓到真正异常，而不是常态性补漏

### 建议增加一个轻量“早爆”检查点

不一定要新大脚本，可以是 helper 自带返回值或一个极小校验：

- 当前 step 的 `children[step]` 是否已有 `session_key + artifacts`
- 当前 step 的每个 artifact 是否已有 `artifact_provenance[artifact]`
- `producer_step` 是否等于该 step

如果这里不过，流程就在当下停住并报 `repairing lineage state`，而不是继续流到 publish。

### 对旧 run / 兼容 run 的最低兜底

`lineage_audit.py --write-state` 继续保留 lazy migration 能力，但定位明确为：

- 兼容旧 run
- 对历史遗留字段做最后一次宽读 + 回写 canonical
- 不是新 run 的常规主路径

否则团队会继续默认“反正 publish 前 audit 会帮我补”。这正是今晚会卡住的根因之一。

---

## 4. must-fix / can-wait

## Must-fix（本轮就该做）

### 1. 统一 canonical 写入口

新增一个专门 helper/script，所有阶段完成后都走它写：

- 顶层 `children`
- 顶层 `artifact_provenance`

这是第一优先级，不做这一条，后面都只是继续手补。

### 2. 统一 artifact key 格式为 draft-dir 相对文件名

canonical 顶层不要再混 absolute path / alias key / basename。

只要 key 不统一，`child_has_evidence()` 和 `prov.get(artifact)` 这种 exact-match 迟早再炸。

### 3. 把 canonical 写入前移到每个 step completion

researcher / writer / reviewer / humanizer / layout 每次完成就写，不准等 publish 前。

否则 dirty lineage 还是会在最贵的时点才暴露。

### 4. 明确顶层 canonical 才是 publish authority

把 `lineage.*` 降级为兼容/调试镜像，别再让人误以为“里面有 lineage 就算完成”。

---

## Can-wait（可以后补，不影响先止血）

### 1. 是否彻底删除 legacy `lineage.*`

短期不必立刻删。先做到：

- 新写入只以顶层 canonical 为权威
- legacy 结构不再参与发布判断

等跑稳后再考虑完全移除。

### 2. 是否让 audit 自动从所有 legacy 形态做更强迁移

可以做，但不是当前最小方案重点。

因为更强的宽读迁移只会继续容忍脏输入；当前更需要的是 **上游写对**。

### 3. 是否补全历史 draft-v1/v2/v3 全量 provenance 回填

对已完成 run，除非要做历史追溯或复盘，不必优先处理。先保证今后的 active run 不再分叉。

### 4. 是否把 research gate / outline gate 等辅助产物也纳入发布级 lineage

这属于扩面，不是今晚问题的最小止血点。当前只需保证 publish 主链 body artifacts：

- `research.json` / `outline.md`
- 当前 `draft-vN.md`
- 当前 `review-vN.json`
- `final.md`
- `final-layout.md`

---

## 建议的最小执行口径

一句话版：

> 新增一个“canonical lineage 写入 helper”，在每个子阶段完成后立刻把顶层 `children` / `artifact_provenance` 按 canonical step + basename artifact 写对；publish 前 audit 只做最终验收，不再承担第一次补 canonical 的职责。

---

## 给主控的落地顺序建议

1. 先定义 canonical helper 的唯一输入/输出契约
2. 把 researcher / writer / reviewer / humanizer / layout 完成后的 state 写入改成统一调这个 helper
3. 把 canonical artifact key 收口成 basename
4. 保留 publish 前 `lineage_audit.py --write-state` 做最后兜底
5. 后续再考虑清理 legacy `lineage.*`
