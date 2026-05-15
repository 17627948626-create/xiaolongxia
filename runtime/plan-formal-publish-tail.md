# 微信正式发布尾段状态机：最小修复方案（2026-04-15）

## 目标

只修 reader-side formal publish 尾段，不扩到写稿链。目标是把现在依赖临场 DOM/截图判断的发布尾段，收口成一个**少状态、强信号、可恢复**的状态机。

这里的“最小”指：
- 不重做整条发布链
- 不引入第二套编排层
- 只把**最后一段**从“看到什么就临场点什么”改成“先判状态，再允许动作”
- 把 `safe_check / boss_confirm / login_scan` 三类人工接力，统一成**显式阻塞态 + 显式恢复点**

---

## 一句话核心思路

把尾段发布链压成 **8 个确定状态 + 3 个人工阻塞子态 + 1 个终态判定规则**，每一步只认 `AUTHORITATIVE_SIGNAL`，不再靠“像是到了这一步”的截图感觉继续乱点。

---

## 当前问题归因

今晚暴露的问题，核心不是“某个 selector 不稳”，而是：

1. **状态和动作没有强绑定**
   - 看到一个弹窗，就顺手点一个按钮
   - 但没有先回答：我当前究竟在哪个状态？

2. **AUTHORITATIVE_SIGNAL 混乱**
   - 有时看 URL
   - 有时看 DOM
   - 有时看截图
   - 有时看弹窗文案
   - 没有“每个状态唯一优先信号源”

3. **人工阻塞没有产品化恢复点**
   - `safe_check`、`login_scan`、`boss_confirm` 都会中断链路
   - 但恢复时常常只能靠上下文记忆和临场判断“应该从哪接着点”

4. **成功判定过晚、失败判定过慢**
   - 容易把“弹窗消失”误当成功
   - 又容易把“还没刷新出来”误当失败

所以最小修复不该是“再补几个 if”，而是：

> **先把尾段状态机定死，再让 DOM 判断服务于状态机，而不是反过来。**

---

## 最小状态机总览

建议正式发布尾段只保留下面这些状态：

1. `edit_ready`
2. `prepublish_config_ready`
3. `publish_entry_dialog`
4. `publish_confirm_dialog`
5. `waiting_safe_check_scan`
6. `waiting_login_scan`
7. `waiting_boss_confirm`
8. `submitted_pending_result`
9. `reader_side_in_review`
10. `reader_side_published`
11. `failed`

其中：
- `waiting_safe_check_scan / waiting_login_scan / waiting_boss_confirm` 是**人工阻塞态**
- `reader_side_in_review / reader_side_published` 是**业务成功态**
- `submitted_pending_result` 是**提交后等待判定态**，专门用来避免“刚点完就误报成功/失败”

---

## 状态定义

---

### 1) `edit_ready`

**含义**
已在目标文章编辑页，允许开始“发表前设置”。

**AUTHORITATIVE_SIGNAL**
以下条件同时成立：
- URL 在 `mp.weixin.qq.com/cgi-bin/appmsg` 编辑页
- 当前页面标题/正文上下文能确认是目标文章
- 可见主发表按钮（如 `button.mass_send` 或等价“发表”按钮）

**允许动作**
- 校验文章身份
- 校验并设置创作来源
- 校验并设置原创声明
- 进入 prepublish hard gate

**禁止误判**
- 仅因“还在 mp.weixin.qq.com 域名下”就视为可发表
- 仅因存在隐藏的 `mass_send` DOM 就视为 `edit_ready`
- 从草稿列表卡片页直接视作 `edit_ready`

**备注**
这是尾段状态机真正的起点。正式发布一律从编辑页起跑，不承认首页草稿卡片页为稳定起点。

---

### 2) `prepublish_config_ready`

**含义**
发表前必须设置项已完成，可以进入发表弹窗。

**AUTHORITATIVE_SIGNAL**
以下两项都成立：
- 创作来源已验证为 `内容由AI生成`
- 原创声明已验证为目标完成态（默认 `文字原创 · 作者: 当前作者配置 · 已开启快捷转载`，或显式记录为允许继续的 `original_timeout_continue`）

**允许动作**
- 跑 prepublish hard gate
- 点击编辑页主“发表”按钮，进入下一状态

**禁止误判**
- 只因“刚刚点过设置弹窗按钮”就认为配置完成
- 把“弹窗关了”当作“设置已生效”
- 跳过验证直接进入发表

**备注**
这个状态的本质是：**配置完成要靠结果验证，不靠操作过程回忆。**

---

### 3) `publish_entry_dialog`

**含义**
已进入第一层发表弹窗，系统等待对当前发布方式做确认。

**AUTHORITATIVE_SIGNAL**
存在**可见**目标弹窗，且弹窗文案命中以下之一：
- `群发通知`
- `未开启群发通知`
- `内容将展示在公众号主页`
- `原创校验超时`
- `链接不合法`
- `系统繁忙`
- `正在增加群发次数`
- 其他 publish 第一级弹窗关键词

**允许动作**
按弹窗文案分类，只允许：
- 群发通知开启路径：确认可见弹窗显示群发通知开启后，点本层 `发表`
- 未开启群发通知 / 公众号主页路径：除非老板明确要求关闭群发通知，否则停下并报告，不继续发表
- 原创校验超时路径：点 `继续群发`
- 风控/限流路径：切 `waiting_retry`（可作为 `failed` 的子类记录，最小版可先落 `failed` 并附 retry_not_before）
- 链接不合法：直接 `failed`
- 出现需要老板确认的合规弹窗：切 `waiting_boss_confirm`
- 出现微信验证：切 `waiting_safe_check_scan`

**禁止误判**
- 只看到“发表”两个字就点击，不区分弹窗类型
- 不做可见性过滤，误点隐藏弹窗里的高危按钮
- 把原创超时弹窗误当“群发通知”弹窗

**备注**
这里必须先“分型”，再“点击”。

---

### 4) `publish_confirm_dialog`

**含义**
已进入第二层确认弹窗，通常是“继续发表/继续群发/最终确认”。

**AUTHORITATIVE_SIGNAL**
存在**可见**二次确认弹窗，且弹窗文案与第一层动作形成闭环，例如：
- `继续发表`
- `继续群发`
- 文案继续确认群发通知开启
- 文案继续提到原创超时后的继续确认

若二次确认文案提示 `未开启群发通知 / 公众号主页`，且老板没有明确要求关闭群发通知，则视为路径不匹配，停下并报告。

**允许动作**
- 点击 `继续发表` 或 `继续群发`
- 若下一跳变为二维码验证，立即转阻塞态
- 若出现老板确认类文案，转 `waiting_boss_confirm`
- 点击后无论如何都进入 `submitted_pending_result`，等待结果判定

**禁止误判**
- 把第一层弹窗误认成第二层
- 因为按钮“长得像继续”就继续点
- 点完后继续留在原状态盲点，不重新判定

**备注**
第二层的关键不是“再点一次”，而是点完必须退出“点击模式”，进入“结果判定模式”。

---

### 5) `waiting_safe_check_scan`

**含义**
发布被微信安全验证拦下，等待老板扫本轮最新 `safe_check` 二维码。

**AUTHORITATIVE_SIGNAL**
以下条件成立：
- 页面存在可见 `微信验证 / safe_check` 区块
- 成功提取到**当前最新**二维码源（URL 或稳定截图路径）
- 二维码已通过本地自验
- blocked state 已持久化成功

**允许动作**
- 保存二维码到稳定路径
- 落盘 blocked state
- 对外转发二维码（由主 agent）
- 等待老板回复 `已扫`

**禁止误判**
- 没有二维码图，只看到“微信验证”文案就通知老板去扫
- 二维码未自验就外发
- 用旧二维码覆盖当前阻塞态
- 老板未明确回复已扫就自行恢复

**恢复点（RESUME POINT）**
收到老板 `已扫` 后：
- 不返回前面重做
- 直接从 `submitted_pending_result` 恢复
- 首先检查二维码弹窗是否消失、页面是否仍在微信后台、是否已出现首页/近期发表状态

**为什么恢复到这里**
因为扫码后真正发生的是“已提交链继续往后跑”，不是“重新进入设置/发表弹窗”。

---

### 6) `waiting_login_scan`

**含义**
发布链不是被 safe_check 拦下，而是浏览器登录态已失效，需要老板重新登录公众号后台。

**AUTHORITATIVE_SIGNAL**
以下条件成立：
- 当前 URL 或页面主体明确显示登录页
- 已抓取到当前登录二维码
- 二维码已自验
- blocked state 已持久化成功

**允许动作**
- 保存登录二维码
- 落盘 blocked state
- 通知老板扫码登录
- 等老板回复 `已扫`

**禁止误判**
- 只因 URL 短暂跳转或刷新异常就认为掉登录
- 把 safe_check 误当 login_scan
- 扫码后默认回到原编辑页，不重新判上下文

**恢复点（RESUME POINT）**
收到老板 `已扫` 后：
- 恢复到 `edit_ready` 重判
- 然后重新走 `prepublish_config_ready -> publish_entry_dialog`

**为什么恢复到这里**
登录态丢失意味着页面上下文不可信，不能假设之前的编辑页/弹窗还在。

---

### 7) `waiting_boss_confirm`

**含义**
被产品/合规/运营确认类弹窗拦住，需要老板做显式业务确认，而不是扫码。

**AUTHORITATIVE_SIGNAL**
以下条件成立：
- 页面存在可见确认弹窗
- 弹窗不属于扫码，不属于登录，而是明确的人类确认/决策型问题
- 已将证据（截图/文案）稳定落盘
- blocked state 已持久化成功

**允许动作**
- 抓取证据
- 向老板转发一句确定的话：要确认什么
- 等老板回复“继续/确认/同意”等显式指令

**禁止误判**
- 把任何未知弹窗都归为 `boss_confirm`
- 没搞清楚让老板确认的是什么就发消息
- 老板未回复明确确认语义就恢复

**恢复点（RESUME POINT）**
收到老板明确确认后：
- 恢复到 `publish_confirm_dialog`
- 因为它本质上仍处于“最终确认前一跳”

**为什么恢复到这里**
`boss_confirm` 不是丢上下文，而是对当前确认链做人工放行。

---

### 8) `submitted_pending_result`

**含义**
最后一个确认动作已经点完，但还不能宣布结果，必须等待权威结果面出现。

**AUTHORITATIVE_SIGNAL**
以下任一成立：
- 刚执行完最终确认点击
- `safe_check/login/boss_confirm` 恢复后，页面重新进入提交后过渡状态

这不是靠某个固定 DOM 判定，而是**状态迁移规则**：
- 一旦最终确认动作成功发出，就进入此态

**允许动作**
- 重新抓页面状态
- 检查是否跳首页
- 检查近期发表
- 检查是否出现 `审核中 / 已发表`
- 检查是否仍被新的阻塞态拦下

**禁止误判**
- 按钮点下去就立刻宣布成功
- 页面暂时没变化就立刻宣布失败
- 继续盲点原按钮

**备注**
这是今晚最该补的状态。没有它，所有恢复动作都会重新变成“边看边猜”。

---

### 9) `reader_side_in_review`

**含义**
文章已成功提交给微信，当前权威状态为审核中。

**AUTHORITATIVE_SIGNAL**
优先级从高到低：
1. 首页/近期发表中出现目标文章，状态为 `审核中`
2. 其他微信后台明确状态文案能确认 `审核中`

**允许动作**
- 宣布 reader-side 提交成功
- 清理 blocked state
- 结束 formal publish 子流程

**禁止误判**
- 仅凭编辑页弹窗消失宣布 `审核中`
- 仅凭用户已扫二维码宣布 `审核中`

---

### 10) `reader_side_published`

**含义**
文章已正式发表成功。

**AUTHORITATIVE_SIGNAL**
优先级从高到低：
1. 首页/近期发表中出现目标文章，状态为 `已发表`
2. 其他微信后台明确状态文案能确认 `已发表`

**允许动作**
- 宣布发布成功
- 清理 blocked state
- 结束 formal publish 子流程

**禁止误判**
- 只因“刚才不是审核中就是成功了”推断已发表
- 只凭 published log 未同步就判断失败

---

### 11) `failed`

**含义**
遇到确定性失败，当前 run 不能继续点下去。

**AUTHORITATIVE_SIGNAL**
以下任一即可：
- `链接不合法`
- 运营规则学习/答题
- 明确内容违规/平台拒绝
- 可见错误文案说明必须人工修内容/稍后重试
- 登录会话异常且二维码也无法抓取
- 状态不明但已经违反安全点击边界

**允许动作**
- 终止点击链
- 上报失败原因
- 给出下一步需要的人工动作或内容修复项

**禁止误判**
- 把暂时等待结果当 `failed`
- 把可恢复的人类扫码阻塞当 `failed`

---

## 人工阻塞态统一协议

三类人工阻塞必须统一写入 durable state：

- `status=need_user_action`
- `waiting_for`：`boss_scan` / `boss_confirm`
- `required_user_action`：`safe_check_scan` / `login_scan` / `boss_confirm`
- `resume_context`
- `blocking_since`
- `timeout_at`
- `qr_updated_at`（有二维码时）
- `safe_check_qr_path`（有二维码时）
- `relay_status`
- `relay_dedupe_key`

### 最关键的最小约束

1. **恢复点必须和阻塞类型绑定，不允许统一“从上次继续”**
   - `safe_check` → `submitted_pending_result`
   - `login_scan` → `edit_ready`
   - `boss_confirm` → `publish_confirm_dialog`

2. **二维码/证据文件必须版本化**
   - 同一 run 内旧码不能覆盖新码语义

3. **老板回复语义必须显式匹配**
   - `已扫` 只解锁扫码类
   - `继续/确认/同意` 只解锁确认类

---

## AUTHORITATIVE_SIGNAL 优先级规则

为避免多信号互相打架，尾段状态机统一采用下面的信号优先级：

### A. 业务结果态优先级最高
用于判定 `reader_side_in_review / reader_side_published`
- 首看首页/近期发表状态
- 不用弹窗消失做代理信号

### B. 阻塞态次高
用于判定 `safe_check / login_scan / boss_confirm`
- 首看可见阻塞弹窗 + 二维码/文案证据
- 不用“好像卡住了”作为判定

### C. 中间态靠可见弹窗分类
用于 `publish_entry_dialog / publish_confirm_dialog`
- 只认可见弹窗文案
- 一律禁止隐藏 DOM 参与动作决策

### D. 编辑起点靠 URL + 目标文章双确认
用于 `edit_ready`
- 仅 URL 不够
- 仅标题模糊相似也不够

---

## 允许动作 / 禁止动作：最小硬规则

### 全局允许动作
- 读当前 URL
- 读可见弹窗文案
- 读可见二维码元素
- 读首页近期发表状态
- 按状态迁移图执行唯一允许点击

### 全局禁止动作
1. **禁止跨状态盲点**
   - 未完成重新判态前，不能连续点两个按钮

2. **禁止隐藏 DOM 参与高危点击**
   - 所有按钮查找必须带可见性过滤

3. **禁止把“操作成功”当“业务成功”**
   - 点击成功 ≠ 发布成功
   - 扫码成功 ≠ 发布成功

4. **禁止把“阻塞态恢复”当“回到原步骤继续乱点”**
   - 恢复后必须先回到对应恢复点重新判态

---

## 最小迁移图

```text
edit_ready
  -> prepublish_config_ready
  -> publish_entry_dialog
  -> publish_confirm_dialog
  -> submitted_pending_result

submitted_pending_result
  -> waiting_safe_check_scan
  -> waiting_login_scan
  -> waiting_boss_confirm
  -> reader_side_in_review
  -> reader_side_published
  -> failed

waiting_safe_check_scan --(老板已扫)--> submitted_pending_result
waiting_login_scan     --(老板已扫)--> edit_ready
waiting_boss_confirm   --(老板确认)--> publish_confirm_dialog
```

这个迁移图的意义是：

- **扫码不是成功**
- **扫码只是回到一个确定恢复点**
- **恢复点之后仍要重新判业务结果**

---

## 必须马上修的 3 件事

### 1. 必须补 `submitted_pending_result`

这是最急的。

没有这个状态，就会把：
- 最后确认按钮点完
- 老板刚扫完码
- 页面刚关闭弹窗

这些“提交后过渡瞬间”误判成成功或失败。

**不补这个状态，恢复逻辑永远不稳。**

---

### 2. 必须把三类人工阻塞的恢复点写死

当前最危险的是：
- `safe_check` 扫完后，有时回头重找发表按钮
- `login_scan` 扫完后，还想从原弹窗继续
- `boss_confirm` 后，不知道该回哪一步

最小修复就是把恢复点固定成：
- `safe_check -> submitted_pending_result`
- `login_scan -> edit_ready`
- `boss_confirm -> publish_confirm_dialog`

**恢复点不写死，所有 blocked state 都只是“记了个卡点”，不是产品化恢复。**

---

### 3. 必须统一 AUTHORITATIVE_SIGNAL 优先级

最少要把下面三条固定下来：
- 成功态只认“近期发表=审核中/已发表”
- 中间态只认可见弹窗文案
- 阻塞态只认可见二维码/登录页/确认弹窗证据

**否则同一页面上 URL、DOM、截图、body 文本会互相打架。**

---

## 可延后的问题

### A. `waiting_retry` 单独建模

像：
- 系统繁忙
- 增加群发次数，请5分钟后再试

严格说应单独建 `waiting_retry`。
但作为最小修复版，短期可以先落到 `failed` 并带 `retry_not_before` 字段，不影响主稳定性。

### B. 更细的 publish 分支枚举

例如把：
- 原创校验超时
- 群发通知关闭确认
- 内容风险提醒

拆得更细。

这个有价值，但不是今晚最小修复的必要条件。先保住“分层 + 恢复点 + 成功判定”。

### C. 基于截图/视觉的兜底分类器

截图分类可做兜底，但不该成为权威主判器。短期不必上。

### D. run 级二维码版本回收策略

旧码清理、文件生命周期管理、自动淘汰策略可以后补；短期只要做到“不复用旧码”就够。

---

## 最小实施建议（不涉及具体代码）

### 控制面层面

给 formal publish 尾段 durable state 至少补齐这些字段：
- `state_node`
- `authoritative_signal_kind`
- `authoritative_signal_summary`
- `resume_point`
- `last_user_gate_type`
- `result_probe_status`

### 运行纪律层面

每次动作都走三步：
1. 先判状态
2. 再看这个状态唯一允许动作
3. 动作后立刻重判状态

而不是：
- 看到按钮就点
- 点完再解释自己在哪

---

## 最终结论

这条链现在不够硬，根因不是 selector 少，而是**缺一个真正可恢复的尾段状态机**。

最小修复不用大改，只要把尾段压成：
- `edit_ready`
- `prepublish_config_ready`
- `publish_entry_dialog`
- `publish_confirm_dialog`
- `submitted_pending_result`
- 三个 `waiting_*`
- 两个结果态

再把三类人工阻塞恢复点写死，成功态只认近期发表状态，基本就能把“今晚能跑通”和“以后能稳定复用”之间的差距补上。
