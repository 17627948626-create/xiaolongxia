# notify-state-spec.md - 通知状态机规范

> 创建时间:2026-04-02
> 适用范围:xiaolongxia workflow 完工通知/开工通知/卡点通知链路
> 版本:v1.0

---

## 1. 状态机定义

```
pending → attempting → api_ok
                    ↘ api_error → retrying → api_ok
                                          ↘ escalated
```

### 状态枚举值

| 状态值 | 含义 |
|--------|------|
| `pending` | 通知尚未尝试发送 |
| `attempting` | 正在调用 message 工具(写入此状态后立即调用) |
| `api_ok` | message API 返回 `ok:true`(**注意:不代表人类已收悉**) |
| `api_error` | message API 返回错误或异常(含超时、非 ok 响应) |
| `retrying` | 已发生至少一次 api_error,正在等待后重试 |
| `escalated` | 3次尝试全部失败,需人工介入 |
| `manual_notified` | 人工补发完工通知后设置的终态(仅人工处置流程使用) |
| `unknown` | 读取旧记录时该字段缺失,视同此值 |

### 状态转移规则

1. 初始状态默认 `pending`(字段可不写)
2. 开始调用前:写 `notify_status=attempting`,写 `notify_attempted_at`(首次则写,后续不覆盖)
3. 调用成功(`ok:true`):写 `notify_status=api_ok`,写 `notify_last_attempt_at`
4. 调用失败:写 `notify_status=api_error`,写 `notify_last_attempt_at`,计数 +1
5. api_error 后等待 30s,重试:写 `notify_status=retrying`,再变 `attempting`
6. 3次全失败(`notify_attempt_count >= 3`):写 `notify_status=escalated`
7. `escalated → manual_notified`:触发者:人工操作;触发条件:老板已通过任何渠道收到通知(Feishu DM、session 内说明均可);需要更新的字段:`notify_status=manual_notified`,追加 `notify_manual_notified_at`(ISO8601时间戳)

**完整状态图(含终态):**
```
pending → attempting → api_ok(终态)
                    ↘ api_error → retrying → attempting → api_ok(终态)
                                                       ↘ escalated → (人工操作) → manual_notified(终态)
```

`manual_notified` 是明确的人工处置终态,与 `api_ok` 等价,表示通知已送达(人工确认)。

---

## 2. published-logs 新增字段定义

以下字段全部**可选**,向后兼容。旧记录无这些字段时,读取方视同 `notify_status=unknown`。

| 字段名 | 类型 | 枚举值/格式 | 含义 |
|--------|------|-------------|------|
| `notify_status` | string (enum) | 见上方状态枚举 | 当前通知状态 |
| `notify_attempted_at` | string (ISO8601) | 例:`2026-04-02T10:22:00+08:00` | 首次尝试时间(首次写入后不再覆盖) |
| `notify_last_attempt_at` | string (ISO8601) | 例:`2026-04-02T10:22:35+08:00` | 最后一次尝试时间(每次尝试后更新) |
| `notify_attempt_count` | integer | ≥ 0 | 累计尝试次数 |
| `notify_dedupe_key` | string | `{slug}_{YYYYMMDD}` | 幂等键,用于防止同一消息重复发送 |

### 字段示例

```json
{
  "title": "你的仓库,现在有两种读者",
  "status": "published",
  "published_at": "2026-04-02T10:22:00+08:00",
  "note": "延误约2小时",
  "slug": "two-readers-for-your-repo",
  "source_file": "/path/to/article.md",
  "notify_status": "api_ok",
  "notify_attempted_at": "2026-04-02T10:22:05+08:00",
  "notify_last_attempt_at": "2026-04-02T10:22:05+08:00",
  "notify_attempt_count": 1,
  "notify_dedupe_key": "two-readers-for-your-repo_20260402"
}
```

---

## 3. 操作顺序(强制)

```
1. 写 notify_status=attempting(写入 published-logs)
2. 写 notify_attempted_at(首次才写,不覆盖)
3. notify_attempt_count += 1
4. 调用 message 工具
5a. 如果 ok:true → 写 notify_status=api_ok,写 notify_last_attempt_at → 结束
5b. 如果失败 → 写 notify_status=api_error,写 notify_last_attempt_at
6. 等待 30s
7. 如果 notify_attempt_count < 3 → 回到步骤1(写 retrying → attempting)
8. 如果 notify_attempt_count >= 3 → 写 notify_status=escalated → 触发人工处置
```

**严禁跳过步骤1**（不写 attempting 直接调用），否则失败时无法区分“未尝试”与“尝试中崩溃”。

---

## 3.1 中断恢复规则

若读取 published-logs 发现 `notify_status` 为 `attempting`、`api_error` 或 `retrying`，说明上次通知流程中途中断。

**恢复逻辑**：

1. 检查 `notify_last_attempt_at`，若距现在超过 5 分钟，视为中断态，进入恢复
2. 恢复时：根据 `notify_attempt_count` 判断剩余重试次数（最大3次总计）：
   - 若 `count < 3`：直接从 `retrying` 状态继续重试，无需重置计数器
   - 若 `count >= 3`：直接设 `notify_status=escalated`，进入人工处置路径
3. `attempting` 超时阈値：5分钟内无后续状态更新，视为进程崩溃，触发恢复流程

**注意**：`notify_last_attempt_at` 未超过5分钟（心跳中），不触发恢复，等待当前流程自然结束。

---

## 4. 幂等规则

若 published-logs 中已存在满足以下条件的记录,则**跳过本次发送**:

- `notify_status in ("api_ok", "manual_notified")`
- `notify_dedupe_key == "{当前slug}_{今日YYYYMMDD}"`

适用场景:重复触发、agent 重启后重跑、复盘 cron 误触发同一轮通知。

⚠️ **语义边界**:当前方案提供「at-least-once + best-effort 去重」,不保证严格 exactly-once。
存在一个崩溃窗口:message 已发出但 agent 在写 `api_ok` 之前崩溃,重启后会再次发送。
这是已知可接受的风险,后续如需严格 exactly-once,需引入持久化 outbound request id。

---

## 5. 重试规则

- **最大尝试次数**:3次(初次 + 2次重试)
- **重试间隔**:30秒
- **状态流转**:`api_error → retrying → attempting → api_ok / api_error`
- **3次全败终态**:`escalated`
- **escalated 处置**:触发人工处置流程(见 `notify-runbook.md`),**必须**用 message 工具通知老板当前卡点

### escalated 后的 fallback 规则

当 `notify_status=escalated` 时,message 工具本身可能就是失败的原因。fallback 优先级:

1. **优先**:重试用 message 工具发 Feishu DM(最多1次额外尝试)
2. **次优**:在当前 session 内直接 reply 说明卡点(即使不是 Feishu DM)
3. **保底**:下次 cron 触发时,step 7 的日志检查会发现 escalated 状态,补发通知

无论通过哪种方式通知到老板,均可将 notify_status 更新为 `manual_notified`。

---

## 6. 重要语义说明

### `api_ok` ≠ 人类已收悉

`api_ok` 仅表示:**message 工具调用返回了 `ok:true`**。

它不保证:
- Feishu 服务器已送达
- 老板已阅读或注意到消息
- 消息显示在正确的会话里

因此,`api_ok` 只是必要条件,不是充分条件。如需确认人类收悉,需等老板明确回复。

### `ok:true` 的风险来源

历史记录显示,以下情况曾出现 `ok:true` 但老板未收到:
- `target` 格式不正确(group vs user 混用)
- `channel` 参数传错
- Feishu 插件路由异常
- 图片走 `/tmp/` 路径(媒体发送失败但 text 部分 ok)

---

## 7. 事实源与审计镜像

| 存储位置 | 角色 |
|----------|------|
| `published-logs/xiaolongxia-youhuashuo.jsonl` | **通知状态的唯一事实源(Source of Truth)** |
| `memory/YYYY-MM-DD.md` | 审计镜像(human-readable,非机读权威源) |

两者冲突时,以 published-logs 为准。

memory 文件中的通知状态描述属于"日志摘要",不具备事务语义。

---

## 8. 关联文档

- `published-logs-format-spec.md`:字段格式与兼容性规范
- `notify-runbook.md`:escalated 状态的人工处置手册
- `proposed-agents-md-changes.md`:AGENTS.md 建议变更(待老板批准)
