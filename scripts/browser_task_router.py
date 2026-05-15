#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

AGENT_SCRIPT = '/root/.openclaw/workspace-xiaolongxia/scripts/browser_use_openclaw_agent.py'
CLI_WRAPPER = '/root/.openclaw/scripts/browser-use-agent.sh'
AGENT_ID = 'xiaolongxia'


def detect_cli_plan(task: str, out: str | None = None) -> dict | None:
    text = task.strip()

    m = re.match(r'^(?:open|打开)\s+(https?://\S+)\s*$', text, re.I)
    if m:
        return {'kind': 'cli', 'args': ['open', m.group(1)]}

    if text.lower() in {'state', 'status', '页面状态', '当前页面状态'}:
        return {'kind': 'cli', 'args': ['state']}

    m = re.match(r'^(?:screenshot|截图)\s*$', text, re.I)
    if m and out:
        return {'kind': 'cli', 'args': ['screenshot', out]}

    m = re.match(r'^(?:eval|执行js|执行 JS|执行 js)\s+(.+)$', text, re.I | re.S)
    if m:
        return {'kind': 'cli', 'args': ['eval', m.group(1)]}

    return None


def should_use_agent(task: str) -> bool:
    text = task.strip().lower()
    if detect_cli_plan(task) is not None:
        return False

    agent_signals = [
        '去', '看一下', '处理', '操作', '跑一下', '流程', '点击', '点开', '跳转', '抽取', '提取', '判断',
        '登录', '发布', '提交', '填写', '搜索', 'compare', 'click', 'extract', 'navigate', 'after', 'then'
    ]
    return any(s in text for s in agent_signals) or True


def run_cli(plan: dict) -> int:
    cmd = [CLI_WRAPPER, AGENT_ID, *plan['args']]
    return subprocess.call(cmd)


def run_agent(task: str, out: str | None, headed: bool, max_steps: int) -> int:
    cmd = ['python3', AGENT_SCRIPT, task, '--max-steps', str(max_steps)]
    if out:
        cmd += ['--out', out]
    if headed:
        cmd += ['--headed']
    return subprocess.call(cmd)


def main() -> int:
    ap = argparse.ArgumentParser(description='Unified browser task entry for xiaolongxia.')
    ap.add_argument('task', help='Natural-language browser task or simple CLI-like command')
    ap.add_argument('--mode', choices=['auto', 'agent', 'cli'], default='auto')
    ap.add_argument('--out', help='Optional output path; also used as screenshot path in CLI screenshot mode')
    ap.add_argument('--headed', action='store_true')
    ap.add_argument('--max-steps', type=int, default=12)
    args = ap.parse_args()

    if args.mode == 'cli':
        plan = detect_cli_plan(args.task, args.out)
        if plan is None:
            print(json.dumps({'ok': False, 'error': 'Task cannot be mapped to deterministic CLI mode', 'task': args.task}, ensure_ascii=False, indent=2))
            return 2
        return run_cli(plan)

    if args.mode == 'agent':
        return run_agent(args.task, args.out, args.headed, args.max_steps)

    plan = detect_cli_plan(args.task, args.out)
    if plan is not None and not should_use_agent(args.task):
        return run_cli(plan)
    return run_agent(args.task, args.out, args.headed, args.max_steps)


if __name__ == '__main__':
    raise SystemExit(main())
