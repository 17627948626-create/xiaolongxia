#!/usr/bin/env python3
import argparse
import asyncio
import json
import subprocess
import traceback
from pathlib import Path

from browser_use import Agent
from browser_use.browser.session import BrowserSession
from browser_use.llm.openai.chat import ChatOpenAI as BUOpenAI

OPENCLAW_GATEWAY_TOKEN = '[REDACTED]'
DEFAULT_MODEL = 'openclaw/xiaolongxia'
DEFAULT_BASE_URL = 'http://127.0.0.1:18789/v1'
DEFAULT_USER_DATA_DIR = '/root/.config/browser-use-profiles/xiaolongxia'
DEFAULT_SESSION = 'default'


def get_existing_cdp_url(session_name: str = DEFAULT_SESSION) -> str | None:
    try:
        out = subprocess.check_output(
            ['browser-use', '--session', session_name, 'python', 'print(browser._session.cdp_url)'],
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=20,
        ).strip()
        return out if out.startswith('ws://') or out.startswith('http://') else None
    except Exception:
        return None


async def run_task(task: str, *, model: str, base_url: str, out: str | None, headed: bool, max_steps: int) -> int:
    llm = BUOpenAI(
        model=model,
        api_key=OPENCLAW_GATEWAY_TOKEN,
        base_url=base_url,
        timeout=120,
        max_retries=1,
        temperature=0.2,
        reasoning_effort='low',
        max_completion_tokens=2048,
    )

    existing_cdp_url = get_existing_cdp_url(DEFAULT_SESSION)
    if existing_cdp_url:
        browser_session = BrowserSession(cdp_url=existing_cdp_url)
        session_mode = 'reuse-default-cdp'
    else:
        browser_session = BrowserSession(
            is_local=True,
            headless=not headed,
            chromium_sandbox=False,
            user_data_dir=DEFAULT_USER_DATA_DIR,
        )
        session_mode = 'local-profile'

    agent = Agent(
        task=task,
        llm=llm,
        browser_session=browser_session,
        use_vision=True,
        use_judge=False,
        enable_planning=False,
        max_actions_per_step=3,
        step_timeout=120,
    )

    payload: dict = {'ok': False, 'task': task, 'model': model, 'session_mode': session_mode, 'cdp_url': existing_cdp_url}
    try:
        history = await agent.run(max_steps=max_steps)
        payload = {
            'ok': True,
            'task': task,
            'model': model,
            'session_mode': session_mode,
            'cdp_url': existing_cdp_url,
            'final_result': history.final_result() if hasattr(history, 'final_result') else None,
            'urls': history.urls() if hasattr(history, 'urls') else None,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        payload = {
            'ok': False,
            'task': task,
            'model': model,
            'session_mode': session_mode,
            'cdp_url': existing_cdp_url,
            'error': str(e),
            'traceback': traceback.format_exc(),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1
    finally:
        try:
            await browser_session.stop()
        except Exception:
            pass
        if out:
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            Path(out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Run Browser Use Agent via OpenClaw Gateway for xiaolongxia.')
    parser.add_argument('task', help='Natural-language browser task to run')
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--base-url', default=DEFAULT_BASE_URL)
    parser.add_argument('--out', help='Optional JSON output path')
    parser.add_argument('--headed', action='store_true', help='Run browser headed instead of headless')
    parser.add_argument('--max-steps', type=int, default=12)
    args = parser.parse_args()
    return asyncio.run(
        run_task(
            args.task,
            model=args.model,
            base_url=args.base_url,
            out=args.out,
            headed=args.headed,
            max_steps=args.max_steps,
        )
    )


if __name__ == '__main__':
    raise SystemExit(main())
