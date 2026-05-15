# HEARTBEAT.md

# 每次心跳检查（保持简短）

- 今天晚 8 点的文章发了吗？（仅晚 8 点一轮，早 8 点 cron 已于 2026-04-04 删除）
- 上次发布有没有异常未处理？
- OpenClaw 有没有新版本？（有的话去看 changelog）

## 晚间窗口重点检查

如果当前时间在 **19:50–21:10**，优先读取：

- `/root/.openclaw/workspace-xiaolongxia/runtime/evening-run.lock.json`

### 运行锁判断规则（按顺序）

> 当前世界观：**主 agent 直接承担整条编排流程**。运行锁反映的是主流程推进状态，不再假设存在独立的中间编排层。

1. **锁不存在**：20:00 cron 尚未触发或已完成清理，正常。
2. **`state=done`，或 `phase` 已是 `published` / `done` 且 `waiting_for=null`**：本轮已完成，不接管，只做结果确认。若旧锁里残留 `safe_check_qr_path` / `relay_status` / `progress_source=orchestrator` 等历史字段，**以 `state` / `phase` / `waiting_for` 为准**，不要误判成仍在等待扫码。
3. **`phase=awaiting_human` / `blocked`，或 `required_user_action` 存在且 `waiting_for` 是 `boss_scan` / `boss_confirm`**：在等老板操作，不重复催，不接管。
4. **`state=running`，且 `now - last_progress_at <= expected_silence_ttl_minutes`**：正常运行中，不接管。
5. **`state=running`，且超出 `expected_silence_ttl_minutes` 但未超 `max_run_minutes`**：疑似静默，只汇报当前状态，不直接接管。
6. **`state=error`，或 `state=running` 且同时超过 `expected_silence_ttl_minutes` 与 `max_run_minutes`**：判定卡住，主动汇报并接管。

> **兼容说明**：旧格式运行锁里可能仍有 `orchestrator_session`、`progress_source=orchestrator`、`relay_*`、历史二维码路径等字段；这些现在都只是兼容残留。**心跳判断只认 `state` / `phase` / `current_step` / `waiting_for` / `required_user_action` / `last_progress_at`。**

> **注意**：锁文件里没有 `expected_silence_ttl_minutes` 或 `max_run_minutes` 字段时（旧格式兼容），用默认值：静默阈值 25 分钟，总运行上限 60 分钟。

## 任务追踪模式（有正在进行的任务时）

如果 `/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/drafts/` 下有未完成的草稿目录（有 pipeline-state.json 但无 publish.md，或 publish.md 存在但 published-logs 最新记录 status 不是 published），则：

1. `ls -lt <draft_dir>` 看最新文件和时间
2. 结合 `evening-run.lock.json` 判断当前阶段（**以 `state` / `phase` / `current_step` 为主，不看旧的 orchestrator 命名字段**）
3. 报告：**进行中任务｜显式状态（state/phase/current_step）｜waiting_for｜最新文件｜距上次推进多久**
4. 如果已明确在等老板扫码/确认，不重复催；只在状态变化时再汇报
5. 如果没有等待老板，且判定卡住（按上方规则 6），主动汇报：**疑似卡住，需要人工干预**

如果一切正常且没有文章需要发，回复 HEARTBEAT_OK。
