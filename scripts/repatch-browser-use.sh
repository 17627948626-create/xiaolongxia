#!/bin/bash
# 一键重打 browser-use sessions.py patch
# 用途：pip upgrade browser-use 后运行，恢复 root VPS 下的 --no-sandbox 支持
# 根因：browser-use 0.12.5+ 在 root 环境不自动加 --no-sandbox，Chrome 崩溃，watchdog 30s 超时

set -e

SESSIONS_PY=$(python3 -c "import browser_use.skill_cli.sessions as m, inspect; print(inspect.getfile(m))")
echo "[repatch] Target: $SESSIONS_PY"

if grep -q "chromium_sandbox=False" "$SESSIONS_PY"; then
    echo "[repatch] Already patched. Nothing to do."
    exit 0
fi

python3 /root/.openclaw/workspace-xiaolongxia/scripts/repatch-browser-use.py
echo "[repatch] Done. Restart daemon: browser-use close && browser-use open 'about:blank'"
