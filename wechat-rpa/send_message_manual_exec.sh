#!/usr/bin/env bash
set -euo pipefail
CONTACT="${1:?contact required}"
MSG="${2:?message required}"
WID=$(su - ewq -c 'DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool search --name 微信 | head -n 1')
GEOM=$(su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool getwindowgeometry --shell $WID")
eval "$GEOM"
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool windowactivate --sync $WID"
# NOTE: execution-only scaffolding. Recognition is handled by pure multimodal vision.
SX=$((X + 120)); SY=$((Y + 38))
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool mousemove --sync $SX $SY click 1"
sleep 0.3
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool key --clearmodifiers ctrl+a BackSpace"
printf "%s" "$CONTACT" | su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xclip -selection clipboard -in"
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool key --clearmodifiers ctrl+v"
sleep 0.6
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool key Return"
sleep 1
IX=$((X + 700)); IY=$((Y + HEIGHT - 45))
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool mousemove --sync $IX $IY click 1"
sleep 0.3
printf "%s" "$MSG" | su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xclip -selection clipboard -in"
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool key --clearmodifiers ctrl+v"
sleep 0.4
su - ewq -c "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus xdotool key Return"
