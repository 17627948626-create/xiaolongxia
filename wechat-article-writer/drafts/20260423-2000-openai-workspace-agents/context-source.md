# Recovery context — 2026-04-24

## Locked topic
- topic: OpenAI Workspace Agents 让 ChatGPT 开始进公司接活
- title_direction: ChatGPT 开始进公司“接活”了，OpenAI 要卖的不只是助手，而是数字同事
- purpose: 借 OpenAI 发布 Workspace Agents，写清 AI 产品竞争正在从个人提效工具转向组织级共享数字同事，争夺的是公司里的工作流入口与协作入口。

## Locked brief summary
- hot_hook: OpenAI 刚把 Workspace Agents 端出来，ChatGPT 开始不只陪你聊天，而是准备进公司流程里接活了。
- thesis: 这轮竞争变的不是 AI 更像助手，而是模型公司开始争谁先成为公司里的数字同事和工作流入口。
- ai_punchline: 以后大家抢的不是谁更会答，而是谁先被接进组织协作链路里。

## Hard recovery rules
1. Use a proper Researcher subagent flow. Do NOT use llm-task to directly generate research.json.
2. Write a clean, valid JSON `research.json` and prose-safe `outline.md`.
3. Run these gates before finishing:
   - python3 /root/.openclaw/skills/wechat-article-forge.bak-20260422-164008/scripts/validate_research_artifact.py <draft-dir>/research.json --output <draft-dir>/research-gate.json
   - python3 /root/.openclaw/skills/wechat-article-forge.bak-20260422-164008/scripts/outline_gate.py <draft-dir>/outline.md --output <draft-dir>/outline-gate.json
4. If either gate fails, fix the artifact and rerun.
5. Do not silently change topic unless evidence collapses; if you must retopic, write the reason explicitly in research.json.
6. Search/verify current facts about OpenAI Workspace Agents, timing, pricing/availability, and competitive context (Google enterprise agent platform / organization workflow angle) using validated sources.
