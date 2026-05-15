# xiaolongxia agent persona backup

This repository is the portable backup of the xiaolongxia agent persona and operating memory.

It intentionally stores identity, rules, writing memory, reusable scripts, and WeChat article production artifacts. It intentionally does not store live credentials, OAuth state, browser cookies, raw browser profiles, or full OpenClaw runtime session logs.

## What matters most

- `AGENTS.md`: primary behavior contract.
- `SOUL.md`, `IDENTITY.md`, `USER.md`: persona, identity, and owner context.
- `MEMORY.md` and `memory/`: long-term and daily memory.
- `XIAOLONGXIA_WRITER_LITE.md`: writing adapter and preflight rules.
- `wechat-article-writer/`: article workflow configuration, voice profile, published log, and draft archive.
- `TOOLS.md`, `scripts/`, `runtime/*.md`, `retrospectives/`: operational knowledge worth migrating.
- `config/*.redacted.json`: redacted reconstruction references for OpenClaw, browser-use, and cron.

## Restore outline

1. Install or prepare the new agent runtime.
2. Put these files under the new xiaolongxia workspace.
3. Load `AGENTS.md`, `SOUL.md`, `USER.md`, recent `memory/*.md`, and `MEMORY.md` as the agent startup context.
4. Recreate the OpenClaw agent entry from `config/openclaw.redacted.json`.
5. Recreate Feishu, WeChat, model, browser-use, and cron credentials manually. They are not stored here.
6. Recreate the browser-use profile mapping from `config/browser-use-agent-profiles.redacted.json`, then log in again where needed.
7. Resume article work from `wechat-article-writer/` and verify the latest published log before publishing again.

## Sensitive data policy

Do not commit:

- OpenClaw auth state or OAuth refresh tokens.
- API keys, app secrets, cookies, browser profiles, or raw session databases.
- `wechat-article-writer/secrets.json`.
- Raw `/root/.openclaw/agents/xiaolongxia/sessions/` logs.
- Historical UI screenshots and browser/RPA artifacts unless deliberately curated.
- SQLite state, cache, WAL/SHM files, and temporary runtime folders.

If a full machine-state backup is needed, create a separate encrypted archive and keep the decryption key outside GitHub.
