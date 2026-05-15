# notify-runbook.md — 通知失败人工处置手册

> 创建时间：2026-04-02  
> 适用场景：`notify_status=escalated`（3次重试全部失败）时的人工处置流程  
> 关联文档：`notify-state-spec.md`、`published-logs-format-spec.md`

---

## 触发条件

当 published-logs 中出现 `"notify_status": "escalated"` 时，表示完工通知经过 3 次尝试（初次 + 2次重试，间隔各 30s）仍未成功发送，需要人工介入。

---

## 第一步：找到 escalated 条目

```bash
# 查看 published-logs 中所有 escalated 条目
grep '"notify_status"' /root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl \
  | grep '"escalated"'

# 或查看整个日志文件（末尾几行通常是最新）
tail -20 /root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl \
  | python3 -m json.tool 2>/dev/null || \
  tail -20 /root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl
```

记录以下信息，供后续操作：
- `slug`：文章标识符
- `title`：文章标题
- `published_at`：发布时间
- `notify_attempt_count`：已尝试次数（应为 3）
- `notify_last_attempt_at`：最后一次尝试时间

---

## 第二步：排查 api_error 常见原因

在手动补发之前，先排查失败原因，避免补发也失败。

### 2.1 检查 message 工具 target 格式

```
正确格式：user:ou_137c41086239266036853c70dd1ae919
常见错误：
  - 缺少 "user:" 前缀（如直接用 ou_137c41086239266036853c70dd1ae919）
  - 使用 group/chat ID 代替 user ID
  - ID 有空格或换行
```

### 2.2 检查 channel 参数

```
正确值：feishu
常见错误：
  - channel 未传或传空
  - 拼写错误（如 "lark" 或 "飞书"）
```

### 2.3 检查媒体路径（若通知含图片）

```
正确路径：/root/.openclaw/media/screenshots/xxx.png
错误路径：/tmp/xxx.png（会导致发出字符串而非图片，但 ok:true）
```

### 2.4 检查 Feishu 插件状态

```bash
# 查看 OpenClaw 运行状态
openclaw gateway status
```

若 gateway 未运行，先重启：
```bash
openclaw gateway restart
```

### 2.5 验证 message 工具是否可用

在 openclaw 环境中执行简单测试：

```
message(action="send", channel="feishu", target="user:ou_137c41086239266036853c70dd1ae919", message="测试消息")
```

若返回 `ok:true` 则链路恢复，可继续补发。

---

## 第三步：手动补发完工通知

确认链路正常后，手动发送完工通知：

```
message(
  action="send",
  channel="feishu",
  target="user:ou_137c41086239266036853c70dd1ae919",
  message="完工 🦞｜[文章标题]｜[发布状态]｜[补发说明：原通知3次失败，现人工补发]"
)
```

将 `[文章标题]` 替换为 escalated 条目的 `title` 字段值。

---

## 第四步：更新 notify_status 为 manual_notified

手动补发成功后，需更新 published-logs 对应条目的状态。

**操作规范**：只允许追加新行（不允许 inplace 修改中间行）。脚本必须精确定位目标记录，要求 slug 匹配 + notify_status=escalated，并通过 dry-run + 人工确认后才执行写入。

**保存以下脚本为 `/tmp/fix_notify.py`，然后执行 `python3 /tmp/fix_notify.py <slug>`：**

```python
import json, sys
LOG_PATH = "/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl"

if len(sys.argv) < 2:
    print("用法: python3 fix_notify.py <slug>")
    sys.exit(1)
target_slug = sys.argv[1]

records = []
with open(LOG_PATH, 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            records.append(json.loads(line))

targets = [r for r in records if r.get("slug") == target_slug and r.get("notify_status") == "escalated"]

if len(targets) == 0:
    print(f"❌ 未找到 slug={target_slug} 且 notify_status=escalated 的记录，拒绝写入")
    sys.exit(1)
if len(targets) > 1:
    print(f"❌ 找到 {len(targets)} 条匹配记录，需人工确认唯一目标，拒绝自动写入")
    for t in targets:
        print(f"  - {t.get('title')} | {t.get('published_at')} | {t.get('notify_dedupe_key')}")
    sys.exit(1)

target = targets[0]
print(f"[DRY-RUN] 将更新以下记录为 manual_notified:")
print(f"  slug: {target.get('slug')}")
print(f"  title: {target.get('title')}")
print(f"  published_at: {target.get('published_at')}")
print(f"  notify_dedupe_key: {target.get('notify_dedupe_key')}")

confirm = input("确认写入? (yes/no): ")
if confirm.strip().lower() != "yes":
    print("已取消")
    sys.exit(0)

# 追加新行（不修改原记录）
from datetime import datetime, timezone
new_record = dict(target)
new_record["notify_status"] = "manual_notified"
new_record["notify_manual_notified_at"] = datetime.now(timezone.utc).isoformat()
with open(LOG_PATH, 'a') as f:
    f.write(json.dumps(new_record, ensure_ascii=False) + '\n')
print(f"✅ 已追加 manual_notified 记录")
```

**关键保障**：
- 匹配到 0 条或 >1 条时，打印警告并拒绝写入，要求人工确认
- 写入前先 dry-run 打印将要更新的记录摘要（slug/title/published_at/notify_dedupe_key）
- 需人工输入 "yes" 确认后才执行写入

---

## 第五步：确认恢复完成

满足以下所有条件，视为本轮通知链路恢复完成：

- [x] published-logs 中存在同一 `slug` 的 `notify_status=manual_notified` 记录
- [x] 老板已在 Feishu 收到补发的完工通知（有回复或已读标记）
- [x] `notify_dedupe_key` 对应的记录中最终态为 `manual_notified`（非 `escalated`）

**注意**：`manual_notified` 是人工处置终态，与 `api_ok` 等价，表示通知已送达（人工确认）。

---

## 常见问题

### Q：escalated 后 message 工具本身也失败怎么办？

1. 在 session 内明确说明：`通知发送失败且 message 工具不可用，请老板检查 Feishu 机器人状态`
2. 检查 `openclaw gateway status`，尝试重启
3. 若 gateway 正常但 Feishu 插件报错，查看 openclaw 日志：`journalctl -u openclaw -n 50` 或等价命令

### Q：如何区分"从未尝试"和"尝试中崩溃"？

- `notify_status` 为空或 `unknown`：从未走过通知状态机
- `notify_status=attempting` 且无后续记录：尝试中崩溃（agent 被终止或超时）
- 后者需按 escalated 处理（从头重发）

### Q：`notify_attempt_count` 怎么不是 3？

- 可能 agent 在中途崩溃，未完成全部重试
- 按实际情况判断，若已确认多次失败，直接进入人工处置流程

---

## 关联文档

- `notify-state-spec.md`：状态机完整定义
- `published-logs-format-spec.md`：日志格式与兼容性规范
- `proposed-agents-md-changes.md`：AGENTS.md 建议变更（待老板批准）
