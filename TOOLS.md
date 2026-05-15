# TOOLS.md - 工具与环境备注

## browser-use 环境说明（root VPS 专项）

### 2026-04-08 新规：agent 级 profile 隔离（强制）

这台机上现在**禁止裸用共享的 browser-use 持久目录**去跑多 agent。根因已经实战确认：`money` 会话曾错误占用 `/root/.config/browser-use-persistent`，导致 `xiaolongxia` 的 `default` 发布链路只有 daemon，没有真正接到浏览器，老板扫码结果写进了错误会话。

当前正式做法：

- 中央 registry：`/root/.openclaw/browser-use-agent-profiles.json`
- 统一入口：`/root/.openclaw/scripts/browser-use-agent.sh`
- 发布前 guard：`python3 /root/.openclaw/scripts/browser_use_profile_guard.py --agent xiaolongxia --json`

当前映射：

- `xiaolongxia` → `session=default` + `user_data_dir=/root/.config/browser-use-profiles/xiaolongxia`
- `money` → `session=money` + `user_data_dir=/root/.config/browser-use-profiles/money`

以后如果**新建 agent**也要用 browser-use：

1. 先在 registry 里新增一条唯一映射
2. 分配独立 `session`
3. 分配独立 `user_data_dir`
4. 只允许通过 wrapper 启动，不要裸跑 `browser-use --session ...`

**禁止事项：**
- 禁止让两个 agent 共享同一个 `user_data_dir`
- 禁止在 agent 删除/重建后继续复用旧 daemon 不清理
- 禁止在微信发布前跳过 guard 检查

### ⚠️ 升级提醒

每次 `pip install --upgrade browser-use` 后，必须重新执行 patch：

```bash
python3 /root/.openclaw/workspace-xiaolongxia/scripts/repatch-browser-use.py
# 然后重启 daemon 并验证：
browser-use close
browser-use --session default open "about:blank"
browser-use sessions   # 应看到 default headless
```

脚本会自动检查→补丁→验证三段，失败时 exit 非0。

**根因**：browser-use 在 root 用户下不自动加 `--no-sandbox`，Chrome 崩溃，watchdog 30s 超时。patch 在 `skill_cli/sessions.py` 的两处 `BrowserSession(...)` 里加了 `chromium_sandbox=False`。

**Cookie 持久化 patch（2026-04-01 新增）**：`profile=None` 分支额外加了 `user_data_dir='/root/.config/browser-use-persistent'`，防止 daemon 每次重启用随机 `/tmp/` 目录导致微信登录态丢失。升级后需同步补这一行：

```python
# skill_cli/sessions.py, profile is None 分支
return BrowserSession(
    headless=not headed,
    chromium_sandbox=False,  # root VPS: no sandbox
    user_data_dir='/root/.config/browser-use-persistent',  # persistent cookies across daemon restarts
)
```

⚠️ **安全红线（操作约束，不只是提醒）**：关闭 Chromium 沙盒（`chromium_sandbox=False` / `--no-sandbox`）是 root VPS 的必要妥协，但代价是宿主机暴露风险显著上升。**禁止用 browser-use（无论 CLI 还是 Agent 模式）访问不可信的外部网站。仅允许访问已知可信域名（如 mp.weixin.qq.com）。**

---

### browser-use CLI 模式（确定性操作，首选）

```bash
browser-use sessions                          # 查看活跃 session
browser-use --session default open "URL"      # 打开页面
browser-use --session default eval "JS"       # 执行 JS
browser-use --session default screenshot /tmp/out.png
browser-use --session default state           # 查看 DOM 状态
browser-use close                             # 关闭 daemon
```

**注意**：`--session default` 必须在子命令前面，不能放后面。

### browser-use Agent 模式（自主导航，用于不确定性任务）

#### 小龙虾当前正式接法（2026-04-18 起生效）

小龙虾以后默认不要再走旧的 Copilot/Claude 示例。当前正式接法已经换成：

- LLM backend：**OpenClaw Gateway**
- model：`openclaw/xiaolongxia`
- base_url：`http://127.0.0.1:18789/v1`
- token：OpenClaw gateway token
- 浏览器：`BrowserSession(is_local=True, chromium_sandbox=False, user_data_dir='/root/.config/browser-use-profiles/xiaolongxia')`

原因：这条链路已经实测跑通多步网页任务，能把 Browser Use Agent 的任务模型后端无感接到当前 OpenClaw 主模型体系上。

#### 推荐模板

```python
import asyncio
from browser_use import Agent
from browser_use.browser.session import BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI as BUOpenAI

OPENCLAW_GATEWAY_TOKEN = '[REDACTED]'

async def run_agent(task: str):
    llm = BUOpenAI(
        model='openclaw/xiaolongxia',
        api_key=OPENCLAW_GATEWAY_TOKEN,
        base_url='http://127.0.0.1:18789/v1',
        timeout=120,
        max_retries=1,
        temperature=0.2,
        reasoning_effort='low',
        max_completion_tokens=2048,
    )

    browser = BrowserSession(
        is_local=True,
        headless=True,
        chromium_sandbox=False,
        user_data_dir='/root/.config/browser-use-profiles/xiaolongxia',
    )

    agent = Agent(
        task=task,
        llm=llm,
        browser_session=browser,
        use_vision=True,
        use_judge=False,
        enable_planning=False,
        max_actions_per_step=3,
    )

    result = await agent.run(max_steps=12)
    return result.final_result() if hasattr(result, 'final_result') else str(result)
```

#### 统一入口（推荐）

```bash
/root/.openclaw/workspace-xiaolongxia/scripts/browser-task "Open https://example.com"
/root/.openclaw/workspace-xiaolongxia/scripts/browser-task "去这个页面看一下，然后提取标题和链接"
```

默认分流：
- 简单确定性命令 → CLI
- 自然语言多步任务 → Agent

CLI 路线现在会先做 profile guard；若检测到只是旧 daemon 还占着错误 `user_data_dir`，wrapper 会先自愈重启，再继续执行。

#### 已验证的硬经验

- **`BrowserSession(...)` 必须显式带 `is_local=True`**。默认路径在这台机上可能卡住 browser start watchdog。
- 必须用 `browser_use.llm.openai.chat.ChatOpenAI`（browser-use 原生 wrapper），不能用 langchain 的 `ChatOpenAI`
- `use_judge=False` 必须设置，否则 Judge 会误判且浪费 token
- 当前兼容接口的模型名要写成 `openclaw/xiaolongxia`，**不要直接写 `openai-codex/gpt-5.4`**
- Agent 结束后 session 会 reset；如果要回到 CLI 路线继续用当前 profile，先执行：`browser-use --session default open "about:blank"` 重建 daemon/session
- 当前正式可复用脚本：`/root/.openclaw/workspace-xiaolongxia/scripts/browser_use_openclaw_agent.py`
- 当前统一入口：`/root/.openclaw/workspace-xiaolongxia/scripts/browser-task`

### CLI + Agent 融合用法

```
CLI: browser-use --session default open "起始页"         ← 快速导航到目标页
     browser-use --session default eval "JS"  ← 精确提取数据
        ↓
Agent: BrowserSession(cdp_url=...) → agent.run("完成复杂判断任务")
        ↓
CLI: browser-use --session default open "about:blank"   ← Agent 结束后重建 session（必须！）
     browser-use --session default eval "..."  ← 继续 CLI 操作
```

---

## 飞书发图（⚠️ 重要，必读）

### 唯一正确方式

**用 `message` tool 的 `media` 参数，路径必须在 OpenClaw 管理的媒体目录下。**

```python
message(action="send", channel="feishu", media="/root/.openclaw/media/screenshots/xxx.png", message="说明文字")
```

### 为什么 `/tmp/` 不行

`media` 参数只能访问 OpenClaw 管理的媒体目录（`/root/.openclaw/media/`），如果路径在 `/tmp/` 或其他地方，Feishu 插件收到的是字符串路径，发出去就是一段文字，不是图片。

### 截图必须存到这个目录

```bash
mkdir -p /root/.openclaw/media/screenshots
browser-use --session default screenshot /root/.openclaw/media/screenshots/xxx.png
```

然后发送：

```python
message(action="send", channel="feishu", media="/root/.openclaw/media/screenshots/xxx.png", message="说明")
```

### 禁止用这些方式发图

| 方式 | 结果 |
|------|------|
| `filePath: "/tmp/xxx.png"` | 发出去是字符串 |
| `media: "/tmp/xxx.png"` | 发出去是字符串 |
| `buffer + base64 + mimeType` | 可用但麻烦，仅在无法存文件时备用 |
| `MEDIA:./xxx.png` 内联语法 | 视 channel 配置而定，不稳定 |
| 外部 URL（如微信 QR URL）| 需要 cookies，通常 403 |

### 最佳实践

1. 截图 → 存到 `/root/.openclaw/media/screenshots/`
2. 可用 PIL 裁剪到目标区域（减小文件大小）
3. 用 `media="/root/.openclaw/media/screenshots/xxx.png"` 发送
4. `ok:true` 不代表用户看到了图片，要等用户明确回复确认

---

## 微信发布

- 浏览器 session：`browser-use --session default`
- 这是 **xiaolongxia 专属 session**，不得与其他 agent 混用
- 持久目录：`/root/.config/browser-use-profiles/xiaolongxia`
- 浏览器路线固定：**xiaolongxia 默认就走 browser-use**，不要在同一类发布任务里改走 OpenClaw browser
- 原则：宁可其他 agent 各自重新登录，也不要共用这个 session
- ⚠️ `agent-browser` 已废弃，不可用
- 发布路径：必须进**编辑页**（不是草稿列表页）才能正常弹出发表对话框
- 获取 appmsgid：点草稿列表的编辑按钮 → 新 tab 打开 → `browser-use --session default switch 2` 切换 → 从 URL 取 appmsgid
- safe_check 二维码 selector：`img.js_qrcode`，src 如是相对路径要补全为 `https://mp.weixin.qq.com/safe/safeqrcode?...`

## 微信草稿 appmsgid 获取方法

在已登录的 browser-use session 里，用 AJAX 接口直接拿，比从 DOM 找稳：

```bash
browser-use --session default eval "
fetch('/cgi-bin/appmsg?action=list_ex&begin=0&count=10&type=77&token=TOKEN&lang=zh_CN&f=json&ajax=1', {credentials:'include'})
  .then(r=>r.text()).then(t=>window.__drafts=t);
'fetching'
"
# 等 2 秒再读结果
browser-use --session default eval "window.__drafts"
```

返回的 JSON 里每条草稿有 `appmsgid`，取第一条即最新草稿。

## 发布配置

- MCP config: `/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/mcp-xiaolongxia-youhuashuo.json`
- 发布日志: `/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl`
- 文章 workspace: `/root/.openclaw/workspace-xiaolongxia/wechat-article-writer/`

## Subagent 超时

所有 spawn 的子 agent 统一设 `runTimeoutSeconds: 3600`（1小时），不再按角色分别设小值。

## 搜索工具优先级

中文内容：`jj-search-stack`（主力，含微信文章/国内内容）
深度爬取/国际内容：`tavily-search`（search/extract/crawl 模式，6 key 轮询）
注意：`cn-web-search` 无独立 skill，功能由 `jj-search-stack` 覆盖；`web_search`（Brave）未配置 API key，不可用

## mcporter + wenyan-mcp 发布备注

### 正确调用语法（已验证可用）

```bash
# ✅ 正确：dot notation + key=value
mcporter call wenyan-mcp.publish_article "file=/path/to/publish.md"

# ❌ 错误：--server + --tool + --params（会报"missing input-content"或触发其他解析错误）
mcporter call --server wenyan-mcp --tool publish_article --params '{"file":"..."}'
```

### 常见错误"未能找到文章标题"

原因：`publish.md` 的 frontmatter 字段不符合 wenyan-mcp 协议。
必须包含：`title`、`author`、`profile`、`cover`（有效 URL）、`theme`（值为 `sspai`）、`slug`
禁止字段：`account`、`date`、`公众号` 等非标准字段

## Wenyan 列表 bullet 分行修复（2026-04-02）

### 根因

`@wenyan-md/core/dist/core.js` 的 `wechatPostRender()` 会把每个 `<li>` 的子节点搬进新的 `<section>`：

```js
const listElements = element.querySelectorAll("li");
listElements.forEach((li) => {
  const doc = element.ownerDocument;
  const section = doc.createElement("section");
  while (li.firstChild) {
    section.appendChild(li.firstChild);
  }
  li.appendChild(section);
});
```

`section` 是块级元素，结果就是 bullet / 序号单独占一行，正文掉到下一行。

### 正确修法（J1）

**直接删掉这段 `li -> section` 包裹逻辑**，不要再用 CSS `display:inline` 去遮。

### 升级后重打补丁

```bash
python3 /root/.openclaw/workspace-xiaolongxia/scripts/repatch-wenyan-core-list-fix.py
```

脚本会：
1. 检查目标文件是否存在
2. 发现原始坏块时自动备份
3. 精确删除坏块
4. 验证 `wechatPostRender()` 仍在且坏块已消失

### 验收页

```bash
node /root/.openclaw/workspace-xiaolongxia/out/render_wenyan_list_fix_preview.mjs
# 输出：/root/.openclaw/workspace-xiaolongxia/out/wenyan-list-fix-preview.html
python3 -m http.server 8765 --bind 127.0.0.1  # 在 out/ 目录下
# 浏览器打开 http://127.0.0.1:8765/wenyan-list-fix-preview.html
```

验收关注：普通列表、粗体开头、有序列表、嵌套列表、列表中的代码块、列表中的图片，都应保持 marker 与正文同行。
