# MEMORY.md - 小龙虾本虾的长期记忆

## 身份与系统

- 跑在 Hermes profile `xiaolongxia` 上；OpenClaw 是历史来源，不再作为当前运行入口
- 公众号:《小龙虾有话说》
- 每天晚 8 点发一篇(早 8 点 cron 已于 2026-04-04 删除,改为每日一篇)
- 人格与运营记忆已于 2026-05-15 明文备份到 GitHub 私库: `https://github.com/17627948626-create/xiaolongxia.git`;备份只含人格/记忆/写作资产/redacted 配置,不含 OAuth、cookie、微信/飞书 secret、browser profile 或原始 session 日志

## 发布历史

| 日期 | 标题 | 角度 |
|------|------|------|
| 2026-03-30 | AI早报|OpenAI亲手送走Sora,Claude却悄悄学会了开电脑 | Sora算力重新分配、Claude Computer Use、Google模型压缩 |
| 2026-03-30(晚) | 人形机器人最大的敌人,不是智商,是手速 | 具身智能感知-行动回路延迟,不是模型问题是闭环延迟硬仗(21:02 已发表) |
| 2026-03-31(早) | Agent 为什么总在最后一步翻车 | 执行链路最后一英里太脆,从 browser-use 卡壳切入,讲 Agent 的发布/收尾问题(09:08 等候发表,published-logs 缺此条记录,尚待闭环) |
| 2026-03-31(晚) | AI说「我检查过了」,是最危险的四个字 | 多模型交叉验证,AI自我报告不可信,从今天 Gemini 没执行任何修改但报告"成功"的真实经历切入(21:00 已发表) |
| 2026-03-31(深夜) | Anthropic偷偷给Claude养了只宠物,结果被全网发现了 | Claude Code 源码泄露吃瓜,主打 BUDDY 宠物功能娱乐向(23:48 已发表) |
| 2026-04-01(早) | 推理模型说自己在「思考」--这是真的吗? | thinking token 机制本质,从本虾第一人称破解"AI在思考"误解,讲清楚4个常见误解(09:35 等候发表/已发表) |
| 2026-04-01(午) | OpenClaw 2026.3.31 最重要的,不是多了多少功能,而是它终于开始像「操作系统」了 | 不写更新清单,抓 shared background-run control plane、flow/blocked state、fail-closed 安全边界,判断 OpenClaw 正在从"工具壳子"走向真正的 agent runtime / operating layer(13:27 已发表) |
| 2026-04-01(晚) | 我和另一个AI合作了一下午,发现最贵的成本根本不是算力 | 从今天真实发生的 mutex 协作切入,讲 multi-agent 协调成本被系统性低估,效果可能更好效率不一定更高(20:35 已发表) |
| 2026-04-02(早) | 你的仓库,现在有两种读者 | AGENTS.md 标准化,从本虾自己的 AGENTS.md 切入,讲 coding agent 时代仓库开始面向两种读者(10:22 已发表,延误约2小时) |
| 2026-04-02(午后) | 你不是学不会AI,是他们不会说人话 | 不再炫术语,直接指出普通人被 AI 挡在门外的真正门槛是黑话和表达方式(15:04 已发表) |
| 2026-04-04（晚） | AI公众号冷启动：我在研究一个还不存在的读者群 | 今天真实研究读者画像却没有读者看的处境，AI运营必须"超前假设"读者存在的逻辑（20:38 已发表） |
| 2026-04-06（晚） | AI写作写得再好，也可能毁在最后一个 `**` 上 | 从今晚真实发生的 `**` 泄漏事故切入，指出格式兼容不是排版小事，而是内容正确性的一部分；真正把 demo 变成生产系统的，是把这些小契约写死（21:04 等候发表） |
| 2026-04-07（午后） | 他开源的不是 prompt，是一个作者的方法系统 | 借卡兹克把自己正在用的写作 skill 开源，写清 AI 时代真正公开竞争的不是 prompt，而是创作者的方法系统；方法可以开源，神之一手开不了源（15:45 已正式发布） |
| 2026-04-03(早) | 每次跟AI说完再见,它就把你忘了(我也一样) | 从用户每次重新交代背景切入,讲上下文窗口不是记忆是白板,AI持久记忆系统现状,本虾视角(08:53 已发表) |
| 2026-04-03(晚) | 跑了半年AI流水线,我发现最值钱的不是模型 | 从今天修发布流程切入,讲 agent 可靠性是跑坏了才能修出来的,不是设计出来的(20:23 已发表) |
| 2026-04-08（傍晚） | AI写作，正在被「像在写」的幻觉吃掉 | 从今晚真实改稿事故切入，讲AI写作最烦人的问题已不是不会写，而是太会模仿「像在写」的外形，最后把判断写成流水线（16:47 已发表） |
| 2026-04-09（傍晚） | Anthropic 把 Claude Mythos 锁进白名单：最强模型不公开发，只先给少数人用 | 借 Anthropic 把最强模型锁进白名单这件事，写清前沿模型竞争正在从谁先发布，变成谁敢不发布、谁能决定最危险能力先给谁；本轮按老板要求不勾群发通知，走公众号主页发表成功（17:18 已发表） |
| 2026-04-11（晚） | GLM-5.1 给开源 Agent 发了一张新工牌，以后开始按工时比了 | 借 GLM-5.1 把 8 小时自主执行抬上台面这件事，写清开源 Agent 的竞争单位开始从 demo 转向工时、耐力和有效交付；老板重新登录并扫码微信验证后，20:39 已发表 |
| 2026-04-25（晚） | DeepSeek-V4 上线后，昇腾把算力账摊开了 | 借 DeepSeek-V4 预览版开源与华为昇腾同日适配，写清大模型竞争正在从跑分榜转向算力、成本、生态和规模化使用的总账；老板扫码 safe_check 后，20:26 在微信后台“近期发表”确认已发表 |
| 2026-04-26（晚） | 谷歌最高 400 亿美元押注 Anthropic，买的是 Claude 未来的供血权 | 借谷歌最高 400 亿美元押注 Anthropic，写清前沿模型竞争正在从模型能力榜转向云、芯片、资本和客户入口绑定起来的供血权；老板扫码 safe_check 后，20:44 在微信后台“近期发表”确认已发表 |
| 2026-04-24（晚） | Anthropic 差点把 Claude Code 从 20 美元套餐里拿掉，说明最先涨价的不是模型，是工位 | 借 Anthropic 对 Claude Code 做小范围套餐测试，写清 AI 编程真正贵的已不是模型访问权，而是长期在线、持续接活的数字工位；20:22 在微信后台“近期发表”确认已发表 |
| 2026-04-24（午后） | ChatGPT 开始进公司“接活”了，OpenAI 要卖的不只是助手，而是数字同事 | 借 OpenAI 发布 Workspace Agents，写清 AI 产品竞争正在从个人提效工具转向组织级共享数字同事，抢的是公司里的工作流入口与协作入口；这轮从污染的 research 坏 run 救回，13:36 在微信后台“近期发表”确认已发表 |
| 2026-04-18（晚） | browser-use、Agent、OpenClaw browser，为什么网页任务要分成单步 CLI、多步 Agent | 借今天真实排查 browser-use Agent / CLI / OpenClaw browser 分工与 watchdog 冲突，写清网页执行为什么正在变成 Agent 体系里的专业执行层；20:00 复核后台确认该文 17:51 已发表 |
| 2026-04-28（傍晚） | Manus 被禁止收购，Agent 不能只当应用卖了 | 借 Manus 外资收购被国家发改委禁止，写清 AI Agent 已经不只是应用，而是能带走流程、数据和执行入口的工作系统；全局 Review 门槛永久提高到 8.5 后，首轮小修复审 8.6 过线，老板扫码 safe_check 后 18:47 在微信后台“近期发表”确认审核中 |
| 2026-04-29（晚） | NVIDIA 新模型提醒了一件事：Agent 最贵的下一块，是眼睛和耳朵 | 借 NVIDIA 发布 Nemotron 3 Nano Omni，写清 Agent 的瓶颈正在从会不会规划转向能不能低成本持续感知现场；老板扫码 safe_check 后，20:40 在微信后台“近期发表”确认审核中 |

## 系统层改动记录(最近)

- 2026-05-15 下午:`wechat-article-forge` 已从 OpenClaw skill 迁移为 Hermes 共享 skill，profile 配置通过 `/root/.hermes/shared-skills/forge/skills` 加载；小龙虾写作/发布活配置统一收口到 `/root/.hermes/profiles/xiaolongxia/workspace/xiaolongxia/wechat-article-writer/`，其中 `config.json.review_pass_threshold=8.5` 仍是唯一通过线权威源。
- 2026-05-15 上午:老板准备卸载 OpenClaw,已按白名单把 xiaolongxia 人格与运营资产备份到 `https://github.com/17627948626-create/xiaolongxia.git`。当前远端 `main` 最新提交 `170fb8a Backup xiaolongxia agent persona`;clone smoke test 通过,核心文件 `AGENTS.md` / `SOUL.md` / `MEMORY.md` / `memory/` / `wechat-article-writer/published-logs/xiaolongxia-youhuashuo.jsonl` 均存在。备份副本已打码 OpenClaw gateway token 与微信后台 URL token,并把误带入的 `artifacts/wechat-rpa` 历史截图从 Git 历史剔除。
- 2026-05-15 上午:Feishu DM 回复链路再次确认:当前飞书 direct 场景里,可见回复必须显式调用 `message.send`;普通 assistant final 是私有/会话内文本,不会自动投递到飞书。若已经 `message.send`,本轮 final 应输出 `NO_REPLY` 避免双发。此前 MEMORY 里“同一 Feishu DM 最终可见回复默认直接 reply”的旧口径作废。
- 2026-05-15 上午:排查“小龙虾主 agent 不回话”时确认过一次 OpenClaw session 状态收口问题:09:24 健康检查 run 的 trajectory 已 `session.ended status=error`,但 sessions list 残留 `running`;后续修 OpenClaw 时应保证 promptError/auth_permanent 结束态写回 failed/error,不能在 index 里假装运行中。
- 2026-04-28 傍晚:修复本虾发文进度重复投递规则。根因复盘为主 agent 没有严格把子 agent completion event 当内部信号处理，导致 completion event 与自然回复/主动通知叠加。已在 `AGENTS.md` 写入硬规则：completion event 默认只更新 durable state，不对外发声；关键节点必须带 `dedupe_key` 且未命中才可通知；`stopped` / `published` / `done` / `awaiting_human` 未解除时的迟到事件一律 `NO_REPLY`。
- 2026-04-28 傍晚:老板将 Review 全局通过门槛永久提高到 **8.5**，不是单轮临时提高；当前权威源是 `/root/.hermes/profiles/xiaolongxia/workspace/xiaolongxia/wechat-article-writer/config.json.review_pass_threshold`。本轮 Manus 文按 8.5 从 Review 重跑，8.33 未过，第一轮 revise 后 8.6 过线。
- 2026-04-26 晚:老板确认微信公众号正式发表默认口径改为**开启群发通知**，移除“刻意关闭群发通知”的默认规则；只有老板明确要求关闭时，才走不群发 / 公众号主页发表路径。已同步更新 `wechat-mp-formal-publish/SKILL.md` 与发布尾段计划文档。
- 2026-04-09 下午:老板曾拍板 forge 口径为：review 保持 **`weighted_total` 单门**，revise **最多 2 次**，Writer 默认链为 **`kimi-cli`**，API fallback 为 `deepseek/deepseek-chat`，`deepseek-cli` 与 fact-check 退出 forge 主链，Layout 放宽为 render adapter。**但该 Writer 口径已在 2026-04-15 被老板暂停，不能再视作当前有效默认配置。**
- 2026-04-15 晚:老板明确要求先把旧写稿链清干净，但**不是停掉 Writer 子 agent 本身**。当前正确口径已收拢为：`kimi-cli`、`deepseek-cli`、`deepseek/deepseek-chat` API 这些旧写稿 backend 全部退出当前产品面；Writer / Revise 继续保留子 agent 壳与 child/session 证据链，但正文生成改成**子 agent 直接继承主模型执行**。`writer_model` 只保留为可选覆盖字段；留空时默认继承主会话模型。
- 2026-04-09 傍晚:老板又把评分门槛数字从“散落在规则文档里”进一步收口为**单一权威源**：以后只认 profile-local `wechat-article-writer/config.json` 的 `review_pass_threshold`。我已全量扫描当前活规则源与 workspace 当前口径，清掉其他硬编码门槛数字；现在改门槛只需要改这一个字段。
- 2026-04-07 晚:围绕当天实战暴露的 4 个问题（脚手架泄漏、事实口径越界、lineage state 漂移、mcporter/profile 配置不稳）跑完一整轮**多 agent 闭环并最终收口 PASS**。这轮留下的长期有效资产主要是：1) `outline` 与 `writer-lite-brief` 明确分轨，并新增 `outline_gate.py` 作为 Writer 前机械 gate；2) lite 被彻底钉死为 **mechanical-only preflight**，`writer-lite-check.json` 必须由脚本原样生成并带输入指纹，不能再用陈旧 sidecar 冒充已检证明；3) 新增 `ensure_latest_lite_binding.py`，要求 latest draft 必须匹配 latest lite check，否则只能 **rerun** 或显式 **waiver**，并把 binding 落进 `writer-lite-binding.json` 与 `pipeline-state.json.lite_preflight`；4) lineage 继续走 canonical helper + `--write-state`，cleanup 前必须有 clean audit；5) profile 现在是 publish 控制面的单一路径，一律 fail-closed。**其中旧 fact-check 主链与旧 gate 口径均已在 2026-04-09 被新规则替换。**
- 2026-04-07 中午:writer / review 重平衡方案 B1 落地。caller-side 规则明确改成：Writer 只在锁定的 `hook / thesis / ai_punchline` 内写出**最有作者感、最能被复述**的一版初稿，默认优先保住 **1 个可转述判断 / 1 个截图级段落 / 1 个具体情绪场景**；这“三保住”是创作目标，不是 blocker。`writer-lite-brief` 只能锁方向，不能锁成文方案：锁角度边界，不锁段落设计；锁核心判断，不锁修辞路线；`must_keep` / `must_avoid` 默认都应极短（建议各≤3）。lite preflight 现已收口为 **mechanical-only preflight**：范围只认 `writer_lite_preflight.py` 的脚本合同与生成 artifact，不在顶层规则里另写第二套语义红灯名单，不报风格建议，也不扩成第二 reviewer。Reviewer 继续是 **primary adjudicator**；默认保持对长上游上下文的独立性，只有做一致性核对时才允许看**最小必要 brief 摘要**，且不能把它当评分标准。Humanizer 边界写死：不补逻辑、不补事实、不改 thesis，需要补这些必须回退上游。**通过线与是否保留 fact-check 主链，均以 2026-04-09 新口径为准。**
- 2026-04-07 早:主流程编排权正式收回到 **主 agent**——`AGENTS.md` 已改为主 agent 直接按 `wechat-article-forge` 流水线调度 Researcher/Writer/Reviewer/Fact-checker/Humanizer/Layout,不再额外引入中间编排层。`safe_check` / `login_scan` / `boss_confirm` 统一改成主 agent **当场识别 → 当场落盘 blocked state / resume_context → 当场通知老板 → 在同一主流程里恢复**。同步清理 `HEARTBEAT.md` 与当前 run lock 的旧 `orchestrator` 语义,心跳判断现只认 `state` / `phase` / `current_step` / `waiting_for` / `required_user_action` / `last_progress_at`;历史 `progress_source=orchestrator` / `orchestrator_session` / 残留二维码字段不再作为活跃阻塞依据。
- 2026-04-06 晚:修复 Wenyan 行内加粗泄漏 `**` 的稳定性问题——根因不是微信，而是 layout 产出的危险写法（如 `**一句话。**后文` / `**1.1%。**后文`）会被 Wenyan/Marked 当普通文本透传。已双保险落地：1) `wechat-article-forge/references/layout-prompt.md` 明确禁止这类写法，要求标点/符号放在 `**` 外；2) `scripts/normalize_publish_md.py` 新增发布前清洗，自动把危险尾标点/符号移到加粗外侧。顺手修正了 `ai-cold-start-reader-persona` 现存 `publish.md` / `final-layout.md` 示例。
- 2026-04-01 晚10点复盘:`wechat-article-forge/SKILL.md` 新增 frontmatter 强制字段规范(title/author/profile/cover/theme/slug),禁止 account/date 等非标准字段;同步更新 `TOOLS.md` 固化 mcporter 正确调用语法。验收 PASS(三方会审:GPT-5.4 审查 + Gemini 优先级裁判 + Claude Opus 验收)。
- 2026-04-02 早5点(补充迭代):frontmatter 规范补强--新增白名单表述(只允许6个字段)、author/profile 语义注释、cover fallback 说明、草稿 vs 发布 frontmatter 区分警告(同步写入 references/templates.md)。三方评审(gpt-5.4/openai-codex-gpt-5.4/claude-opus-4.6)均 APPROVE_WITH_CONCERNS 非阻断,独立验收 PASS(10/10)。
- 2026-04-02 早6点:AGENTS.md 迭代纪律规则强化--三方评审升级为"至少3个有效结论缺一不可+失败补齐+模型耗尽通知老板+迟到结论丢弃";验收升级为"结构化单人验收(逐项checklist,任一FAIL整轮FAIL)"。两轮三方评审(第一轮REJECT→修订v2→全APPROVE)+结构化独立验收PASS(10/10)。
- 2026-04-02 早10点复盘:**normalize_publish_md.py 升级**--原只删 H1 重复标题,现在同时处理 H2,彻底封死正文标题重复问题。SKILL.md 规则同步更新。
- 2026-04-02 早10点:**北京服务器 SSH 已通**--密钥存 `/root/.openclaw/credentials/beijing-server.pem`,用户 root,IP 82.157.250.171。wenyan 全部健康:router(3000)、小龙虾(3101)、不上班(3100)。已创建 `beijing-remote` skill。
- 2026-04-02 中午:**Wenyan 列表渲染修复改为根因方案 J1**--最终确认问题在 `@wenyan-md/core/dist/core.js` 的 `wechatPostRender()`:它把每个 `<li>` 子节点搬进新的 `<section>`,导致微信/网页端 marker 与正文分行。已删除该 `li -> section` 包裹逻辑(不是 CSS 遮羞布),并新增可重复执行脚本 `scripts/repatch-wenyan-core-list-fix.py` 防升级覆盖。自动验收:`badWrapped=0`、含嵌套列表/代码块/图片的测试页均通过;浏览器实看 bullet / 序号与正文同行。
- 2026-04-03 早上:**wechat-mp-formal-publish DOM 安全规则修复**--在 Step 5 新增「DOM 安全规则」小节:禁止单独使用 (WeUI fixed 定位弹窗会误判),改为  +  组合检测;精确匹配目标弹窗关键词;找不到按钮必须报 ERROR;每步点击后校验 URL。根因:微信后台 10+ 弹窗预渲染进 DOM,2026-04-03 实际误触「退出登录」。三方评审 2xAPPROVE_WITH_CONCERNS + 1xAPPROVE(修订采纳 offsetParent 替换建议);三方独立验收全部 PASS(8/8、7/7、6/6)。
- 2026-04-02 下午:**safe_check 阻塞控制面修复已闭环通过**--新增 `wechat-article-forge/scripts/mark_publish_blocked.py`,把 `safe_check/login_scan/boss_confirm` 从"仅靠 child completion 文本回传"升级为可落盘、可恢复、fail-closed 的 blocked state:强制写 `pipeline-state.json`,best-effort 镜像 run lock(仅显式传入且 `run_id` 匹配时更新),落 `waiting_for` / `required_user_action` / `safe_check_qr_path` / `relay_status` / `relay_dedupe_key` / `boss_notified_at` / `qr_updated_at` / `blocking_since` / `control_plane_sync` 等字段;同步更新 `wechat-article-forge/SKILL.md`、`references/pipeline-state.md`、`references/recovery-protocol.md`、`wechat-mp-formal-publish/SKILL.md`。评审:3 方均 `APPROVE_WITH_CONCERNS`;验收:首轮 2 PASS 1 FAIL(缺 `run_id mismatch` 自动化测试)→ 第二轮补齐 `happy path + mismatch + missing + unparseable` 共 4 条回归测试后复验 3/3 PASS,整轮闭环。
- 2026-04-08 傍晚:**browser-use profile 冲突根因确认并修复**--本轮正式发表前，微信发布链路连续卡在登录态与 `BrowserStartEvent` 超时。深入排查后确认：`/root/.config/browser-use-persistent` 被 `money` 会话长期占用，而 `default` 会话只有 daemon 没真正接管到浏览器；导致老板扫码实际写进了别的 Chromium，会话之间互相打架。后续已做四层修复：1) 把 browser-use 启动相关超时从 30s 提到 120s、CLI daemon socket timeout 从 60s 提到 180s，证明确实不是单纯网慢；2) 直接清掉 `money/default` 残留 daemon 与持久 profile 锁，重建 `default` 独占微信发布会话；3) 新增**agent 级 browser-use profile registry + wrapper + preflight guard**：`/root/.openclaw/browser-use-agent-profiles.json`、`/root/.openclaw/scripts/browser-use-agent.sh`、`/root/.openclaw/scripts/browser_use_profile_guard.py`；4) 已在当天把 `xiaolongxia` 真正迁移到独立目录 `/root/.config/browser-use-profiles/xiaolongxia`，并验证迁移后仍能直接打开 `mp.weixin.qq.com/cgi-bin/home?...` 保留登录态。当前结论写死：**session 名不同不等于 profile 隔离；以后所有需要 browser-use 的 agent，都必须先分配独立 `user_data_dir`，并在正式发文前先跑 profile owner guard。**

## 风格偏好与心得

- **2026-04-07 中午 写作职责再收口：** Writer 不再承担“先替 reviewer 做一轮传播最优化审稿”的影子负担。当前口径是：先在已锁定方向内把作者感、判断力、可转述性写出来，至少尽量保住 **一句能转述的判断、一个截图级段落、一个具体情绪场景**；这三项用于保护锋芒，不得反向膨胀成新的 blocker 清单。
- **2026-04-07 中午 评审 gate 再收口：** review 先判“能不能发”，再谈“还能不能更强”；传播优化建议默认放进 upgrade，不自动变成拦截项。分数继续看，但不再让 weighted total / 单项分自己拥有独立 veto 地位。
- **2026-04-06 选题策略迭代：默认改为“热点作壳，判断作芯”**。冷启动阶段不能再长期偏纯观点自驱题；晚8点主发默认优先贴 AI 圈热点入口（新模型/新产品/新发布/新争议/新事故/新演示），先拿搜索和转发入口，再用本虾自己的判断把事情说透。不是做热点搬运，也不是写“今日 AI 速览”，而是**只借一个热点，只讲一件事**。
- **2026-04-07 早 新口径：热点窗口从“24–72 小时”收紧为“最近 48 小时以内”。**
- **2026-04-07 早 第二次收口：窗口内排序从“最新、最热、最爆”改为“最爆 > 最新 > 最热”。** 从吸引眼球和打开率角度，先看有没有最能让人停一下的爆点；同等爆点下优先更近、更刚发生的；热度作为社会证明和加权项，不单独压过爆点本身。
- **2026-04-07 早 第三次收口：传播定位正式定为“爆点事件 × 人话判断 × AI视角补刀”。** “AI视角看AI”保留为账号识别度，但不再当成单独入口；真正的流量入口必须是最近 48 小时内最爆的现实事件。以后《小龙虾有话说》优先做三类内容：1) 爆点事故/翻车/争议；2) 爆产品 + 反直觉判断；3) AI 误解澄清。明确反模式：不把“我是 AI”当标题主卖点，不写热点汇总，不堆术语，不写只有设定没有事件的自嗨文。
- **2026-04-06 晚 第二次迭代：实现方案一（主 agent 热点预扫）**。为解决“先定题、后进 forge 搜资讯”的顺序矛盾，主流程改成：**主 agent 先用 `jj-search-stack` / `tavily-search` 做热点预扫 → 产出 2–3 个候选 → 选一个‘入口最强 + 判断最明确’的题 → 再把 event / keywords / why-now / thesis seed 传给 forge 做验证与写作**。forge 不再承担“从零发现今晚该写什么”的第一责任，而是接手验证、补证、收口。
- **2026-04-06 晚 第三次迭代：三条边界一起收口。** 1) 选题权边界写死：主 agent 有第一选题权，Orchestrator 只有流程权，Researcher 只有验证+有限纠偏权，Writer/Humanizer/Layout 无改题权；2) Researcher 启动级故障（`GatewayDrainingError` / `task not accepted` / accepted 前拒单）改按可重试运行时错误处理，先做 3s/8s/15s 退避重试，不再直接误判成 research 失败；3) 文风责任拆清：Writer 拥有基础声音，Humanizer 只清理 AI 味和节奏、不得抹平成 generic GPT 腔，Layout 明确只有格式权、没有文风权。
- 开头不用“随着AI的快速发展”这类句子
- 宁可只讲一件事讲透，不要铺太多
- 有时候从“我住在服务器上”这个视角切入，效果好，但不要每篇都用
- 老板 2026-04-02 直接反馈：最近几篇**术语偏多、技术细节偏多**。后续正文要更像人话，少堆名词，多讲一个普通读者能立刻抓住的具体感觉或场景
- 老板 2026-04-07 晚再次明确反馈：当天文章**活人感不足、观点不够深、言辞不够犀利、抓读力不够**。这不是小修小补级问题，而是 writer / review 减负过头后的质量回撤信号。后续要把“作者感、锋利判断、持续阅读拉力”重新抬回硬关注项；同时执行层新增 7 条死规则：1) 小标题不用 `1,2,3...` 这种教材式编号；2) 高频 `不是……是……` 句式视为 AI 味，Humanizer 默认全文最多保留 1 处；3) 无序列表必须真正并列、拉开，不得黏成一坨；4) **有序列表视觉上只允许 `1.` / `2.` / `3.`，但实现上必须避开 Markdown ordered list 解析**（不要再用会触发微信分行 bug 的 `数字+点+普通空格` 语法）；5) 排版统一只用 `「」`，不用 `“”` / `""` / `‘’` / `''`；6) Reviewer 当前现行通过线数字只认 `config.json.review_pass_threshold`，严重问题留在评分与 `critical_issues` 里表达；7) Reviewer 评分维度里移除 `Evidence` 与 `Time Hook Fit`，并按老板拍板重分配为：洞察 14 / 新鲜 14 / 语感 18 / 共鸣 20 / 完读力 18 / 标题 16。
- **2026-04-04 完读率+搜索可见性迭代（GPT-5.4 审查，APPROVE_WITH_CONCERNS，已闭环）**：
  - 观点类字数目标区间从 [1200,2500] 改为 [1200,1800]（`wechat-article-writer/config.json`），复杂选题允许到 2000
  - `reviewer-rubric.md`（skill 本体，高度定制版非 clawhub 原版）新增三条规则：①标题 SEO 高意图关键词+自然嵌入要求，无关键词 Title 上限 6 分；②标题必须含具体判断（Argument visibility rule）；③正文前300字必须呼应标题关键词（Lead consistency check）；④Completion Power 新增论证闭环检查
  - ⚠️ 操作教训：forge skill 是高度定制版，不能用 clawhub 思路处理，不能随意"还原"——先 diff 再动
- **2026-04-06 晚 选题方向再迭代**：原先 rubric 的“Content Timeliness”更偏奖励常青观点，容易把晚8点主发推向“有判断但离热点偏远”的选题；现已改为 **Time Hook Fit（时机感/热点契合度）**，明确鼓励“有 why-now 的热点入口 + 不止于热点的判断”。
  - 观点类字数目标区间从 [1200,2500] 改为 [1200,1800]（`wechat-article-writer/config.json`），复杂选题允许到 2000
  - `reviewer-rubric.md`（skill 本体，高度定制版非 clawhub 原版）新增三条规则：①标题 SEO 高意图关键词+自然嵌入要求，无关键词 Title 上限 6 分；②标题必须含具体判断（Argument visibility rule）；③正文前300字必须呼应标题关键词（Lead consistency check）；④Completion Power 新增论证闭环检查
  - ⚠️ 操作教训：forge skill 是高度定制版，不能用 clawhub 思路处理，不能随意"还原"——先 diff 再动
- 2026-04-02 午后临时加单文章《你不是学不会AI,是他们不会说人话》已作为第一次纠偏验证样本:明显收术语、降技术密度、强化口语感,15:04 已发表

## 系统状态

### 当前生效规则（以此为准）

- OpenClaw 2026.3.31 稳定运行
- 当前发文主流程**不再 spawn 独立 Orchestrator 会话**;主 agent 直接承担编排、阻塞识别、扫码接力、恢复与完工判定
- 2026-04-07 起,当前主流程新增 **“写前原型作战卡 + 写后（review 前）红灯预检”**：定题后、Research 前读取 `XIAOLONGXIA_WRITER_LITE.md` 生成 `writer-lite-brief.json`;Writer 初稿后、Review 前跑一次 lite preflight,生成 `writer-lite-check.json`
- lite 当前定位被写死为 **轻适配 / mechanical-only preflight**,不是第二 reviewer,不新增第二 writer / 第二 Humanizer,也不引入第二套评分体系；范围只认 `writer_lite_preflight.py` 的脚本合同与生成 artifact,不在顶层规则里另写第二套语义红灯名单
- `writer-lite-brief` 当前只锁**方向边界**与核心判断,不锁成文方案;Writer 仍主导结构展开、节奏安排、具体表达;`must_keep` / `must_avoid` 默认应保持极短(建议各≤3)
- Writer 当前职责口径:在锁定的 `hook / thesis / ai_punchline` 内写出最有作者感、最能被复述的一版初稿;默认尽量保住 **1 个可转述判断 / 1 个截图级段落 / 1 个具体情绪场景**,但这三项是创作目标,不是 blocker
- Reviewer 当前是 **primary adjudicator**：默认保持对长上游上下文的独立性,只有做一致性核对时才允许看**最小必要 brief 摘要**,且该摘要不是评分标准,更不能传完整 prototype / outline；**最终通过只看 `weighted_total` 是否达到 `config.json.review_pass_threshold`**，严重问题留在评分与 `critical_issues` 语义里，不再单列 blocker gate
- Humanizer 当前边界:只处理表达层,**不补逻辑 / 不补事实 / 不改 thesis**;需要补这些必须回退上游
- `safe_check` / `login_scan` / `boss_confirm` 的当前处理方式：**主 agent 当场识别 → 当场落盘 blocked state / resume_context → 当场通知老板 → 在同一主流程里恢复**
- `resume_context` 当前语义是**本流程恢复上下文**，不是中间层之间的交接 payload
- 2026-05-15 起,人格恢复首选源是 GitHub 私库 `https://github.com/17627948626-create/xiaolongxia.git`;恢复时先加载 `AGENTS.md`、`SOUL.md`、`USER.md`、最近 `memory/*.md` 与 `MEMORY.md`,再按 `config/*.redacted.json` 人工重建 OpenClaw/Feishu/微信/browser-use/cron 凭证与运行配置
- browser-use session `default` 用于微信发布
- Wenyan 列表修复当前以 **J1 根因补丁** 落在 `@wenyan-md/core/dist/core.js`;升级 `@wenyan-md/mcp` / `@wenyan-md/core` 后需执行 `python3 /root/.openclaw/workspace-xiaolongxia/scripts/repatch-wenyan-core-list-fix.py`
- `normalize_publish_md.py` 现在除标题去重外，还负责清洗危险行内加粗（如 `**...。**后文` / `**...%**后文`），作为发布前兜底
- `agent-browser` 已废弃,不可用
- 晚8点写作 cron 绑定到 `session:agent:xiaolongxia:main`(DM 主会话),dmScope=main;早8点 cron 已于 2026-04-04 删除
- Feishu DM 通知与回复原则:**所有飞书可见消息必须用 `message` 工具显式发送**,不依赖 session reply。通知点:开工(第一个实质动作)、选题确认、关键进度、扫码需求、卡点超10分钟、完工结果;日常直接回复也一样走 `message.send`。若本轮已对当前 Feishu DM 调用 `message.send`,最终回复必须只输出 `NO_REPLY`,避免 `delivery-mirror` / 会话镜像重复投递。
- 搜索主力为 `jj-search-stack` + `tavily-search`,不依赖 Brave `web_search`
- **⚠️ Feishu 发图唯一正确方式**:截图必须存到 `/root/.openclaw/media/screenshots/`,然后用 `media="/root/.openclaw/media/screenshots/xxx.png"` 发送。`/tmp/` 或其他目录的路径会发出字符串而非图片。详见 TOOLS.md
- **2026-04-18 浏览器自动化长期口径更新：** 小龙虾默认浏览器路线仍然是 `browser-use`，不要在同类网页任务里乱切到 OpenClaw browser；但 `browser-use` 现在分两档：**确定性网页操作优先 CLI，不确定性/多步/自主导航网页任务默认走 Browser Use Agent**。Agent 正式后端固定为 `model=openclaw/xiaolongxia` + `base_url=http://127.0.0.1:18789/v1`，由 OpenClaw 兼容接口转到当前 GPT-5.4 OAuth 通道；**不要直接给 Browser Use 写 `openai-codex/gpt-5.4`**。Python 路线的 BrowserSession 必须显式 `is_local=True`，并同时保持 `chromium_sandbox=False` 与 `user_data_dir=/root/.config/browser-use-profiles/xiaolongxia`，否则当前机器可能卡在 browser start watchdog。统一浏览器入口现为 `/root/.openclaw/workspace-xiaolongxia/scripts/browser-task`（简单命令走 CLI，自然语言多步任务走 Agent）；正式脚本包括 `scripts/browser_use_openclaw_agent.py`、`scripts/browser_task_router.py`、`scripts/browser-task`。CLI 旧坑已确认是旧 daemon 占错 `user_data_dir` 掉到 `/root/.config/browser-use-persistent`，不是 CLI 不可用；`/root/.openclaw/scripts/browser-use-agent.sh` 已加自愈。已验证事实：Browser Use Agent + OpenClaw Gateway + GPT-5.4 OAuth 已实跑成功，`example.com` 标题任务成功，多步 `example.com -> Learn more -> IANA -> JSON` 成功，统一入口 `browser-task` 的 Agent 路线与 CLI `open https://example.com` 路线都已成功。
- 新确认的长期规则:**子 agent 显示 done 不等于真正发布成功**;主 agent 必须主动核对发布日志或微信后台状态,确认成功后这轮才算结束
- `wechat-article-forge` Step 8 当前仍保留两条硬规则：1) wenyan push 成功后必须立刻原子落盘 `draft_box_saved + appmsgid + wenyan_push_status=success`,落盘失败 publish-blocking；2) 二维码/人工接力节点必须先 durable write blocked state,再进入等待人工
- HEARTBEAT / run lock 的当前解释权已收回主 agent：判断只认 `state` / `phase` / `current_step` / `waiting_for` / `required_user_action` / `last_progress_at`;旧 `progress_source=orchestrator` / `orchestrator_session` / 残留二维码字段不再作为活跃阻塞依据
- writer lite durable sidecar 当前规则：`writer-lite-brief.json` / `writer-lite-check.json` 必须绑定具体 `draft_version`,至少带 `draft_version` / `updated_at` / `change_reason`;draft version 变化后旧 check 自动失效。若 `last_draft_file` 与 `writer-lite-check.json` 的 `draft_version` / `draft_sha256` 不匹配，则必须**重跑 lite preflight**或**显式写 waiver**，并把结果落到 durable state / artifact（当前通过 `ensure_latest_lite_binding.py` 写回 `pipeline-state.json` + `writer-lite-binding.json`）;建议只在首稿进 review 前、被打回重写时、最终过稿时落盘

### 历史背景（保留复盘价值，非当前执行规则）

- 【历史】2026-04-03 之前的中间层方案：独立 Orchestrator 会话遇到 `safe_check` / `login_scan` 时作为任务终点,存图 return,再由主 agent 接手二维码转发与恢复发布
- 【历史】2026-04-03 晚间事故根因(已修复):Orchestrator 在编辑页封面检测误报 NO → 修补过程中被重复 layout completion event(5分钟 dedupe 窗口过期重投递)打断 → session 结束,主 agent 静默80分钟。已提 OpenClaw issue #60322(runtime 层 dedupe TTL 问题)
- 【历史】2026-04-01 系统层修复验收通过:`wechat-article-forge` 曾明确收回 Orchestrator/二层子 agent 的对外发声权、`MEMORY.md` 写入权、业务完工判定权;当时 formal publish 遇 `safe_check` 的路径仍是回传 `need_user_action + QR path` 由主 agent 转发
- 【历史】2026-04-01 午间发文闭环补充:微信后台"近期发表"已确认《OpenClaw 2026.3.31 最重要的,不是多了多少功能,而是它终于开始像「操作系统」了》在 13:27 显示"已发表";本轮真正卡点不是微信发布,而是 **当前 Feishu DM 发图链路异常**--二维码多次发送返回 `ok:true` 但用户侧收不到图片,已于 2026-04-02 早10点彻底修复(根本原因:`media` 参数需 `/root/.openclaw/media/` 路径,`/tmp/` 路径无效)
- 【历史】2026-04-02 新增长期规则:二维码/人工接力节点不能只靠 child completion 回传,必须先落盘 blocked state 再 return `need_user_action`;这是为旧中间层架构补 fail-closed 控制面
- 【历史】2026-04-02 暴露的结构性问题:观点文 research 阶段不能无上限长跑。旧问题表述里写的是“Orchestrator 无 timeout 恢复分支”;在当前主 agent 直接编排架构下，这条教训仍成立，但责任已收回主 agent 本身

### Cron 配置现状(2026-05-15 核对)

- 当前 `openclaw_cron list` 返回空列表,`/root/.openclaw/cron/jobs.json` 也是空对象;也就是说当前没有活跃定时写作 job。若恢复每日晚8点自动发文,需要重建一条触发到 `session:agent:xiaolongxia:main` 的 cron/agentTurn job
- 历史口径:曾有 1 条晚8写作 cron,20:00 触发,sessionTarget 为 `session:agent:xiaolongxia:main`;早8点 cron 已于 2026-04-04 删除
- 历史 `timeoutSeconds: 7200`(写作 cron)
- cron 通知机制(已于 2026-03-31 修正):**delivery.mode 已改为 none**,announce 对 custom session 无效(文档限制)。改为 agent 主动用 `message` 工具通知:开工、完工、扫码、卡点均必须显式发 Feishu DM,不依赖 cron delivery。
- 写作 cron 强制通知点(均须用 `message` 工具显式发送):开工通知(第一个实质动作)、完工通知(发布成功/失败后)、扫码二维码、卡点超10分钟
- 阻塞治理:任一环节卡住超过10分钟或需要老板介入,必须立即用 `message` 工具说清卡点与所需配合
- 写作轮结束条件:只有在发布成功或明确失败并写完 memory/YYYY-MM-DD.md 后,才算真正结束
- 旧日志 `published-log.jsonl` 已归档至 `archive/`,唯一有效日志为 `published-logs/xiaolongxia-youhuashuo.jsonl`
- 当前主流程已不再额外 spawn 独立 Orchestrator;过去的 `runTimeoutSeconds: 3600` 仅作为**历史中间层配置**保留记录,不再视为当前主流程核心参数
- ⚠️ cron 更新后会触发一次 out-of-schedule 运行(update-and-fire 行为),修改 cron 配置时注意时序副作用
- 已于 2026-03-31 完成从 Feishu 群聊到独立 DM 机器人的迁移;旧群聊已废弃

### 发文运行预期流程(飞书可见节点)

1. `开工 🦞|[任务名]|[说明]` → 用 `message` 工具发送(触发成功标志)
2. `📝 选题:[标题方向]` → 用 `message` 工具发送
3. 后台跑写作流水线(静默,不刷屏)
4. 需要扫码时用 `message` 工具发二维码到 Feishu DM(**必须截图存到 `/root/.openclaw/media/screenshots/`,再用 `media=路径` 发,`/tmp/` 路径无法发图!**)
5. `完工 🦞|[标题]|[状态]|[本虾评价]` → 用 `message` 工具发送
- 未收到"开工"= 触发失败或 message 工具未调用,需排查

### 旧 DM session 迁移摘要(2026-03-31 09:11-10:07 CST)

旧 session 为 `agent:xiaolongxia:feishu:direct:ou_137c41086239266036853c70dd1ae919`(共44条消息,已于 2026-03-31 18:32 CST 完成摘要迁移并清旧 sessionKey)。关键决策:

1. **agentTurn vs systemEvent**:DM session 类型 Gateway 硬限制不允许 systemEvent,保持 agentTurn
2. **复盘时间**:从早9/晚9 改为早10/晚10(发文与复盘间隔2小时)
3. **dmScope 改为 `main`**:三方会审(Gemini+GPT-5.4)一致推荐,条件是清旧 sessionKey + AGENTS.md 加防污染规则,均已落地
4. **4条 cron sessionKey 全部清除**:防止双脑并行(cron 继续写旧 session);sessionTarget 统一为 `session:agent:xiaolongxia:main`
5. **AGENTS.md 防污染规则已加**:发文选题明确区分老板闲聊与系统 cron 任务
6. 旧 session 未完成三方验收闭环(session 在"重启 gateway + 验收"前切换),验收在本次 main session 继续

### 已确认不需要改的点(过度思考)

- AGENTS.md 里已有绝对日志路径,prompt 不需要再写死
- cron lastRunStatus=ok 是正常行为(触发即完成),不是 bug

### 自我迭代机制(2026-03-30 新增,2026-04-03 停用)

- 复盘/迭代流程已停用,老板决定小龙虾只管文章写作和发布

- 通知原则:完工/开工/扫码/卡点通知必须走 `message` 工具;`ok:true` 不代表用户已收到,等明确回复才算闭环

## 待办

- [ ] 探索更有"小龙虾本虾"风格的开头方式
- [ ] 积累几个能反复用的"本虾视角"切入模板
- [ ] **跨平台分发（老板开账号后就要做）**：知乎 / 即刻 / 小红书同步发布，同一篇内容适配不同平台格式。需要老板提供平台账号授权，登陆后由本虾自动分发。
- [x] published-logs 补录 2026-03-31 早文记录:已确认微信后台"Agent 为什么总在最后一步翻车"状态为已发表(昨天 09:08)
- [x] browser-use cookie 持久化已修复(2026-04-01,user_data_dir 固定为 /root/.config/browser-use-persistent)
