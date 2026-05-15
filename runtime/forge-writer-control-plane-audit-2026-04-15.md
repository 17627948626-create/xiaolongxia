# forge-writer-control-plane-audit-2026-04-15

## 1. VERDICT: PASS

现行控制面 / 活规则源已经基本收口一致：Writer / Revise 的正式执行口径已统一为 **spawn 子 agent，默认直接继承父级/主会话模型执行**；`writer_model` 已统一成 **可选 override**；我在本轮检查对象里没有发现任何仍可把当前运行重新拉回 `kimi-cli` / `deepseek-cli` / `deepseek/deepseek-chat` API writer executor 的**正式入口**。

## 2. BLOCKING_FINDINGS

- 无。

## 3. NON_BLOCKING_FINDINGS

1. **历史旧口径仍保留在长期记忆里，但已被明确作废，不构成当前正式入口。**
   - Path: `/root/.openclaw/workspace-xiaolongxia/MEMORY.md:34`
   - Quote: `Writer 默认链为 kimi-cli，API fallback 为 deepseek/deepseek-chat... 但该 Writer 口径已在 2026-04-15 被老板暂停，不能再视作当前有效默认配置。`
   - Why not blocking: 这条是历史记录，而且同一段下一行 `/root/.openclaw/workspace-xiaolongxia/MEMORY.md:35` 已用更高时效的新记录明确覆盖；它没有把旧 backend 保留成现行规则，只是保留了演化轨迹。

2. **当日记忆对 `writer_model` 的“留空=继承父级主模型”没有逐字展开，但默认继承口径已经被同批现行规则源补齐。**
   - Path: `/root/.openclaw/workspace-xiaolongxia/memory/2026-04-15.md:14`
   - Quote: `` `writer_model` 仅作可选覆盖 ``
   - Why not blocking: 该句前文已经写了“今后默认由 Writer 子 agent 直接继承主模型执行”，而且 `AGENTS.md:213`、`SKILL.md:137`、`data-layout.md:91` 都把空值继承语义说死了，所以这里不构成控制面歧义。

## 4. CHECKED_RULE_SOURCES

1. `/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/config.json:13`
   - Evidence: `"writer_model": ""`
   - Meaning: 默认不强制覆写 Writer 模型；为空值形态与“继承父级主模型”口径一致。

2. `/root/.openclaw/workspace-xiaolongxia/AGENTS.md:211-217`
   - Evidence:
     - `旧 Writer backend 全部退出当前产品面`
     - `spawn Writer 子 agent，直接继承主模型执行`
     - `` `writer_model` ... 可选覆盖；... 留空，则 Writer / Revise 默认继承主会话模型 ``
     - `Writer 默认继承主模型`
   - Meaning: workspace 主规则已明确切断旧 backend，并把 Writer / Revise 统一到子 agent + inherited model。

3. `/root/.openclaw/workspace-xiaolongxia/USER.md:7`
   - Evidence: `Writer / Revise 直接由子 agent 继承主模型执行。writer_model 仅作为可选覆盖字段；留空时默认继承主会话模型。`
   - Meaning: 用户偏好层与工作流控制面一致，没有要求显式指定 writer_model，也没有保留旧 CLI/API 写稿入口。

4. `/root/.openclaw/workspace-xiaolongxia/MEMORY.md:34-35`
   - Evidence:
     - line 34 明确保留旧口径为历史记录，并注明 `不能再视作当前有效默认配置`
     - line 35 明确当前正确口径：旧 backend 退出，Writer / Revise 保留子 agent 壳并直接继承主模型
   - Meaning: 记忆层没有把旧 backend 伪装成现行规则；反而显式标记了“旧→新”的切换。

5. `/root/.openclaw/workspace-xiaolongxia/memory/2026-04-15.md:14-15`
   - Evidence:
     - `不再走 kimi-cli、deepseek-cli、deepseek/deepseek-chat API 这些旧执行器`
     - `今后默认由 Writer 子 agent 直接继承主模型执行`
     - `已同步清理现行控制面与 forge 技能规则源`
   - Meaning: 当日变更日志与现行规则源一致。

6. `/root/.openclaw/skills/wechat-article-forge/SKILL.md:137-140`
   - Evidence:
     - `writer_model ... optional override only`
     - `If writer_model is empty / omitted ... inherit the parent/main session model`
     - `The active forge flow has no CLI writer path and no separate API writer executor path`
     - `Writer / Revise are ordinary subagent steps`
   - Meaning: 技能主规范已把旧 CLI/API writer executor 明确判死，并把空值继承语义写成执行合同。

7. `/root/.openclaw/skills/wechat-article-forge/SKILL.md:428`
   - Evidence: `if empty, Orchestrator should omit sessions_spawn.model and let Writer inherit the parent/main session model`
   - Meaning: 配置表与正文规则一致，没有出现“字段表”和“正文规则”打架。

8. `/root/.openclaw/skills/wechat-article-forge/references/agent-config.md:31,45`
   - Evidence:
     - `默认继承主会话模型；writer_model 仅作可选覆盖`
     - `spawn Writer 子代理；默认直接继承主会话模型；只有在 config.json.writer_model 显式非空时才覆盖`
   - Meaning: 角色配置与实际编排说明完全对齐。

9. `/root/.openclaw/skills/wechat-article-forge/references/data-layout.md:69,91`
   - Evidence:
     - `"writer_model": ""`
     - `只作为 Writer 子代理... 可选覆盖字段；若为空，则 Writer 默认继承父级/主会话模型`
   - Meaning: 数据布局层没有遗留“必须显式指定 writer_model 才能写稿”的暗门。

## 5. ADVERSARIAL_ATTEMPTS

我刻意从以下角度试图把现行运行“拉回旧路”，但都失败了：

1. **找旧 backend 的正式入口词。**
   - 方法：grep `kimi-cli` / `deepseek-cli` / `deepseek/deepseek-chat` / `deepseek-chat` / `backend` / `writer executor`。
   - 结果：在现行规则源里，这些词只出现在两类位置：
     1) 明确宣布退出当前产品面的禁用条款；
     2) 历史记忆条目，且同时注明“已暂停/不能视作当前有效默认配置”。
   - 失败原因：没有任何一处把它们写成现行可走路径。

2. **找“Writer 需要显式指定 writer_model 才能工作”的文案漏洞。**
   - 方法：核对 `config.json`、`SKILL.md`、`agent-config.md`、`data-layout.md`。
   - 结果：所有正式口径都统一为：`writer_model` 是 optional override；空值时省略 `sessions_spawn.model`，Writer 直接继承父级/主会话模型。
   - 失败原因：没有任何一处写成 mandatory field、fail-closed-on-empty、或“老板指定后才能写”。

3. **找 Writer / Revise 分叉：首稿继承主模型，但改稿偷偷回旧执行器。**
   - 方法：重点检查 `SKILL.md:137-140`、`AGENTS.md:213`、`data-layout.md:91`。
   - 结果：这些规则都把 Step 2 + Step 4 一起收口，明确写成 Writer / Revise 共用同一语义：子 agent 执行，默认继承主模型，`writer_model` 只作可选覆盖。
   - 失败原因：没有发现“首稿一套、改稿一套”的残留分叉。

4. **找“虽然说禁用旧 backend，但 parent/orchestrator 还能自己代写正文”的回流入口。**
   - 方法：检查 `SKILL.md` 的执行路径条款。
   - 结果：`SKILL.md:138` 明确写着：`Do not move正文 generation back to the parent orchestrator.`
   - 失败原因：控制面不仅禁了 CLI/API writer executor，还禁了把正文生成挪回父级会话。

5. **找配置表与说明文档互相打架。**
   - 方法：对照 `config.json` 空值、`SKILL.md` 字段表、`agent-config.md`、`data-layout.md`。
   - 结果：配置值、字段解释、流程说明三层一致，没有出现一个地方说“默认继承”，另一个地方说“暂无默认 backend / 必须指定 writer_model / 走某个 CLI/API writer path”。
   - 失败原因：当前控制面已经完成同口径收束。

## 6. FINAL_JUDGMENT

本轮审计结论为 **PASS**。

原因不是“看起来差不多”，而是我按最容易复发的几条回流路径逐一试图撬开：
- 旧 CLI 路径回流；
- 旧 API executor 回流；
- Step 2 / Step 4 语义分叉；
- `writer_model` 从 optional 被文案偷偷改回 mandatory；
- 父级 orchestrator 偷偷代写正文；
- 字段表、技能说明、workspace 规则三方打架。

这几条我都没撬开。当前正式控制面已经把 Writer / Revise 收口为：**spawn 子 agent，默认继承父级主模型执行；`writer_model` 仅在显式非空时才覆盖 Writer；旧 `kimi-cli` / `deepseek-cli` / `deepseek/deepseek-chat` writer backend 不再是现行正式入口。**
