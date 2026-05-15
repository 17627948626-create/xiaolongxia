# 复盘：正式发表误触"退出登录"事故分析

**日期：** 2026-04-03  
**触发场景：** 早8点文章发布流水线，Step 8 formal-publish 阶段  
**问题类别：** 系统层 — skill 规则缺失导致子 Agent DOM 操作不安全  

---

## 事故经过

Orchestrator 子流程调用 `wechat-mp-formal-publish`，在编辑页完成发表弹窗交互时，误触了隐藏弹窗里的"退出登录"按钮，导致微信后台会话掉出，需要老板手动重新扫码登录。

## 根本原因

### 直接原因：未加可见性过滤的 DOM 点击

微信公众平台后台将 **10+ 个弹窗节点全部预渲染进 DOM**，其中包含"退出登录"等高危按钮，平时靠 CSS 控制显隐。子流程在点击按钮时，使用了未经可见性过滤的全局 querySelector，命中了隐藏弹窗里的错误按钮。

具体场景：
- 目标：点"发表"弹窗里的"发表"按钮
- 实际：误命中"未授权切换账号"隐藏弹窗里的"退出登录"

### 根本原因：SKILL.md 缺少 DOM 安全规则

`wechat-mp-formal-publish/SKILL.md` Step 5 只说"每步后截图确认"，**没有明确要求：**
1. 所有按钮点击必须先过滤 `offsetParent !== null`（可见性）
2. "退出登录"等高危按钮隐藏在预渲染弹窗中，是已知陷阱
3. 每次点击后必须校验 URL，防止意外跳转

### 架构原因：子 Agent 没有主 Agent 的历史经验

主 agent 在 MEMORY.md / TOOLS.md 有积累，但子 Agent 只读 SKILL.md。SKILL.md 的质量直接决定子 Agent 的安全操作边界。

## 这是系统层问题（不是内容/流程层问题）

本次问题不是文章内容问题，不是流水线架构问题，**是 SKILL.md 缺少一条关键的 DOM 操作安全规则**，导致子 Agent 在面对微信后台复杂 DOM 时行为不安全。

## 修改方案（v1）

**修改文件：** `~/.openclaw/skills/wechat-mp-formal-publish/SKILL.md`  
**修改位置：** Step 5（走发表主流程）

**新增内容：**

```
### ⚠️ DOM 安全规则（必须遵守，防止误触"退出登录"）

微信公众平台后台将 10+ 个弹窗全部预渲染进 DOM，其中包含"退出登录"等高危按钮（藏在"未授权切换账号"隐藏弹窗里），平时靠 CSS 控制显隐。

**强制规则：**
1. 所有按钮点击必须先过滤 `offsetParent !== null`，只操作当前可见弹窗
2. 精确匹配目标弹窗文字（如"群发通知"、"继续发表"），在确认弹窗内再找按钮
3. 每次点击后立即检查 URL，若跳回登录页或首页，说明触发了意外操作，停止并报告

**安全点击模板：**
```js
// ✅ 安全：先找可见弹窗，再在弹窗内找按钮
const dialogs = document.querySelectorAll('.weui-desktop-dialog');
for (const d of dialogs) {
  if (d.offsetParent !== null && d.innerText.includes('目标弹窗关键词')) {
    const btn = [...d.querySelectorAll('button')].find(b => b.innerText.trim() === '目标按钮文字');
    if (btn) { btn.click(); break; }
  }
}

// ❌ 危险：全局查找，可能命中隐藏弹窗里的高危按钮
document.querySelector('button').click()
```

**点击后必须验证 URL：**
```js
// 每步点击后立即执行
const url = location.href;
if (url.includes('mp.weixin.qq.com/') && !url.includes('cgi-bin/appmsg') && !url.includes('cgi-bin/home')) {
  // 可能意外跳转，停止操作，报告 need_user_action
}
```
```

**同步更新"已知环境经验"节，新增：**
```
- 微信后台存在 10+ 个预渲染隐藏弹窗，其中"未授权切换账号"弹窗含"退出登录"高危按钮。2026-04-03 曾在正式发表时误触导致会话掉出。所有 click 操作必须加 offsetParent 可见性过滤。
```

## 风险评估

- **改动范围：** 仅 SKILL.md 新增规则，不改架构、不改流程
- **兼容性：** 对现有正确执行无影响（可见性过滤不影响正确弹窗）
- **副作用：** 无
- **不改会怎样：** 下次子 Agent 执行 formal-publish 仍有相同风险

## 问题分类结论

**系统层问题，进入迭代。最严重问题唯一：缺少 DOM 安全规则。**
