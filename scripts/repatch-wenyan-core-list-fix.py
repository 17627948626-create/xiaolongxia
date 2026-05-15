#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

TARGET = Path('/root/.nvm/versions/node/v22.22.1/lib/node_modules/@wenyan-md/mcp/node_modules/@wenyan-md/core/dist/core.js')
BACKUP = TARGET.with_name('core.js.bak.before-li-section-removal')
BROKEN_BLOCK = '''  const listElements = element.querySelectorAll("li");
  listElements.forEach((li) => {
    const doc = element.ownerDocument;
    const section = doc.createElement("section");
    while (li.firstChild) {
      section.appendChild(li.firstChild);
    }
    li.appendChild(section);
  });
'''


def fail(msg: str, code: int = 1) -> None:
    print(f'ERROR: {msg}', file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    if not TARGET.exists():
        fail(f'target not found: {TARGET}')

    text = TARGET.read_text()

    if BROKEN_BLOCK not in text:
        if 'const listElements = element.querySelectorAll("li");' in text or 'doc.createElement("section")' in text:
            fail('target file contains an unexpected li/section variant; patch not applied automatically')
        print('OK: patch already present (li -> section wrapper block absent)')
        return

    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
        print(f'Backup created: {BACKUP}')

    patched = text.replace(BROKEN_BLOCK, '', 1)
    TARGET.write_text(patched)

    verify = TARGET.read_text()
    if BROKEN_BLOCK in verify:
        fail('verification failed: wrapper block still present after write')
    if 'function wechatPostRender(element)' not in verify:
        fail('verification failed: wechatPostRender missing after patch')

    print('OK: removed li -> section wrapper block from wechatPostRender()')
    print(f'Patched: {TARGET}')


if __name__ == '__main__':
    main()
