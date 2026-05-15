#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-/tmp/wechat-window-current.png}"
WID=$(su - ewq -c 'DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool search --name 微信 | head -n 1')
if [ -z "$WID" ]; then
  echo "wechat window not found" >&2
  exit 1
fi
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus maim -i $WID '$OUT'"
echo "$OUT"
