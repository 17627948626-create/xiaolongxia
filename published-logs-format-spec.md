# published-logs-format-spec.md — published-logs 格式规范

> 创建时间：2026-04-02  
> 版本：v1.1（新增通知状态字段）  
> 关联文档：`notify-state-spec.md`、`notify-runbook.md`

---

## 当前有效日志路径

```
/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl
```

**注意**：旧日志 `published-log.jsonl` 已归档至 `archive/`，不可使用。上述路径是唯一权威路径。

---

## 文件格式

- 格式：JSONL（JSON Lines），每行一个 JSON 对象，UTF-8 编码
- 每行末尾有换行符 `\n`
- 不使用 JSON Array 或嵌套结构

---

## 字段定义

### 现有字段（不变）

| 字段名 | 类型 | 必填 | 含义 |
|--------|------|------|------|
| `title` | string | 是 | 文章标题 |
| `status` | string | 是 | 发布状态：`published` / `failed` / `draft` |
| `published_at` | string (ISO8601) | 是 | 发布时间，格式：`2026-04-02T10:22:00+08:00` |
| `note` | string | 否 | 备注（人类可读，自由文本） |
| `slug` | string | 是 | 文章唯一标识符（ASCII，用于幂等去重） |
| `source_file` | string | 否 | 原始 markdown 文件路径 |

### 新增可选字段（v1.1，向后兼容）

| 字段名 | 类型 | 枚举值/格式 | 含义 |
|--------|------|-------------|------|
| `notify_status` | string (enum) | `pending` / `attempting` / `api_ok` / `api_error` / `retrying` / `escalated` / `manual_notified` / `unknown` | 完工通知当前状态 |
| `notify_attempted_at` | string (ISO8601) | 例：`2026-04-02T10:22:05+08:00` | 首次发起通知尝试的时间（首次写入后不再覆盖） |
| `notify_last_attempt_at` | string (ISO8601) | 例：`2026-04-02T10:22:35+08:00` | 最后一次尝试时间（每次尝试后更新） |
| `notify_attempt_count` | integer | ≥ 0 | 通知发送累计尝试次数 |
| `notify_dedupe_key` | string | `{slug}_{YYYYMMDD}` | 幂等键，防止同一消息重复发送 |

#### 枚举值详细说明

| 枚举值 | 含义 |
|--------|------|
| `pending` | 通知尚未尝试 |
| `attempting` | 正在调用 message 工具（瞬态，正常情况下不应长时间停留此状态） |
| `api_ok` | message API 返回 `ok:true`（**不代表人类已收悉**） |
| `api_error` | message API 调用失败（含超时、非 ok 响应） |
| `retrying` | 等待重试中（api_error 后、下次 attempting 前） |
| `escalated` | 3次全败，需人工介入 |
| `manual_notified` | 人工补发完工通知后设置的终态 |
| `unknown` | 读取旧记录时字段缺失，读取方视同此值 |

---

## 完整记录示例

### 新格式记录（含通知状态）

```json
{
  "title": "你的仓库，现在有两种读者",
  "status": "published",
  "published_at": "2026-04-02T10:22:00+08:00",
  "note": "延误约2小时",
  "slug": "two-readers-for-your-repo",
  "source_file": "/root/.openclaw/workspace/wechat-article-writer/articles/two-readers.md",
  "notify_status": "api_ok",
  "notify_attempted_at": "2026-04-02T10:22:05+08:00",
  "notify_last_attempt_at": "2026-04-02T10:22:05+08:00",
  "notify_attempt_count": 1,
  "notify_dedupe_key": "two-readers-for-your-repo_20260402"
}
```

### 旧格式记录（不含通知状态，仍有效）

```json
{
  "title": "人形机器人最大的敌人，不是智商，是手速",
  "status": "published",
  "published_at": "2026-03-30T21:02:00+08:00",
  "note": "已发表",
  "slug": "robot-speed-problem",
  "source_file": "/root/.openclaw/workspace/wechat-article-writer/articles/robot-speed.md"
}
```

---

## 新旧记录兼容规则

- 旧记录不含新字段时，**读取方视同 `notify_status=unknown`**
- 不允许为旧记录批量补填新字段（禁止回填操作）
- 新字段对旧记录不产生约束（历史记录无需补齐）

---

## 更新操作规范

### 允许的操作

1. **追加新行**：在文件末尾追加 JSON 行（最常见操作）
2. **原子更新最后一行**：若最后一行状态需要更新（如 `attempting → api_ok`），可先读取、修改后，用新行覆盖（write-and-replace 最后一行）

### 禁止的操作

- ❌ 批量回填历史记录（inplace 修改中间行）
- ❌ 不完整 JSON（确保每行是有效的 JSON 对象）
- ❌ 同时修改多行（任何多行修改均需分步追加）
- ❌ 删除已有行（日志只增不减）

---

## 去重规则

同一 `slug` 可能在日志中多次出现（重试、补发等场景）。

### 读取时去重逻辑

同一 `slug` 多次出现时，取**最终态行**，优先级如下：

1. `notify_status` 为终态值（`api_ok` / `escalated` / `manual_notified`）的行
2. 若多行均为终态，取时间最新的一行（`notify_last_attempt_at` 或 `published_at` 最大值）
3. 仍有多个候选时，取文件中**最后出现**的一行

**非终态值**（`pending` / `attempting` / `api_error` / `retrying` / `unknown`）不作为最终态，在去重时跳过。

### 写入时去重逻辑

写入前检查：若已存在 `notify_dedupe_key` 相同且 `notify_status=api_ok` 的记录，**跳过本次写入和发送**（幂等保护）。

---

## 读取示例（Python）

```python
import json
from pathlib import Path

LOG_PATH = Path('/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl')

def read_latest_by_slug(slug: str) -> dict | None:
    """读取指定 slug 的最终态记录"""
    terminal_states = {'api_ok', 'escalated', 'manual_notified'}
    candidates = []

    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get('slug') == slug:
                    ns = record.get('notify_status', 'unknown')
                    if ns in terminal_states:
                        candidates.append(record)
            except json.JSONDecodeError:
                pass

    if not candidates:
        return None
    # 取最后出现的终态记录
    return candidates[-1]
```

---

## 通知状态唯一事实源

published-logs 是通知状态的**唯一事实源（Source of Truth）**。

`memory/YYYY-MM-DD.md` 中的通知状态描述属于审计镜像（human-readable），两者冲突时以 published-logs 为准。

---

## 关联文档

- `notify-state-spec.md`：通知状态机完整定义（状态转移、操作顺序、重试规则）
- `notify-runbook.md`：escalated 状态的人工处置手册
- `proposed-agents-md-changes.md`：AGENTS.md 建议变更（待老板批准）
