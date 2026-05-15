"""
browser-use sessions.py patch for root VPS environments.
Run this after: pip install --upgrade browser-use

Patches applied:
1. chromium_sandbox=False — root VPS: Chrome crashes without --no-sandbox
2. user_data_dir persistent — prevent cookie loss on daemon restart
"""
import sys
import inspect
import os
import browser_use.skill_cli.sessions as m

path = inspect.getfile(m)
content = open(path).read()

PERSISTENT_DIR = '/root/.config/browser-use-persistent'

# Patch 1: sandbox + persistent user_data_dir for profile=None branch
SANDBOX_OLD = '\t\treturn BrowserSession(\n\t\t\theadless=not headed,\n\t\t)'
SANDBOX_NEW = (
    '\t\treturn BrowserSession(\n'
    '\t\t\theadless=not headed,\n'
    '\t\t\tchromium_sandbox=False,  # root VPS: no sandbox\n'
    f"\t\t\tuser_data_dir='{PERSISTENT_DIR}',  # persistent cookies across daemon restarts\n"
    '\t\t)'
)

# Patch 2: sandbox for --profile branch
PROFILE_OLD = (
    '\treturn BrowserSession(\n'
    '\t\texecutable_path=chrome_path,\n'
    '\t\tuser_data_dir=user_data_dir,\n'
    '\t\tprofile_directory=profile_directory,\n'
    '\t\theadless=not headed,\n'
    '\t)'
)
PROFILE_NEW = (
    '\treturn BrowserSession(\n'
    '\t\texecutable_path=chrome_path,\n'
    '\t\tuser_data_dir=user_data_dir,\n'
    '\t\tprofile_directory=profile_directory,\n'
    '\t\theadless=not headed,\n'
    '\t\tchromium_sandbox=False,  # root VPS: no sandbox\n'
    '\t)'
)

already_sandbox = 'chromium_sandbox=False' in content
already_persistent = PERSISTENT_DIR in content

if already_sandbox and already_persistent:
    print(f'[repatch] {path} already fully patched. Nothing to do.')
    sys.exit(0)

applied = 0

if not already_sandbox or not already_persistent:
    if SANDBOX_OLD in content:
        content = content.replace(SANDBOX_OLD, SANDBOX_NEW)
        applied += 1
    elif already_sandbox and not already_persistent:
        # sandbox already patched but missing persistent dir — inject it
        old_with_sandbox = (
            '\t\treturn BrowserSession(\n'
            '\t\t\theadless=not headed,\n'
            '\t\t\tchromium_sandbox=False,  # root VPS: no sandbox\n'
            '\t\t)'
        )
        if old_with_sandbox in content:
            content = content.replace(old_with_sandbox, SANDBOX_NEW)
            applied += 1

if 'chromium_sandbox=False' not in content:
    if PROFILE_OLD in content:
        content = content.replace(PROFILE_OLD, PROFILE_NEW)
        applied += 1

if applied == 0:
    print(f'[repatch] ERROR: no patch points found in {path}')
    print('[repatch] browser-use API may have changed. Manual review needed.')
    sys.exit(1)

# Ensure persistent dir exists
os.makedirs(PERSISTENT_DIR, exist_ok=True)

open(path, 'w').write(content)
print(f'[repatch] Applied {applied} patch(es) to {path}')

# Verify
verify = open(path).read()
errors = []
if 'chromium_sandbox=False' not in verify:
    errors.append('chromium_sandbox=False missing')
if PERSISTENT_DIR not in verify:
    errors.append(f'user_data_dir={PERSISTENT_DIR!r} missing')

if errors:
    print(f'[repatch] ERROR: verification failed — {", ".join(errors)}')
    sys.exit(1)

print('[repatch] Verification OK: chromium_sandbox=False + persistent user_data_dir confirmed.')
