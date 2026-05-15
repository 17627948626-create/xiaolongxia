# WeChat Desktop RPA (Pure Vision)

## Principle

This stack is **pure vision** — multimodal model only.

- Multimodal model: understand the screenshot / decide UI state / propose next action
- Traditional desktop automation: execute mouse + keyboard actions
- OCR: **not used, not a fallback, removed entirely**

## Target flow

1. Capture current WeChat window screenshot
2. Produce structured JSON describing UI state and recommended action
3. Execute action (click / type / paste / hotkey)
4. Capture again and verify

## Required JSON contract

See `vision_action_schema.json`.

## Current status

- XPS is connected as OpenClaw Node
- WeChat desktop is installed and launchable
- GUI session is available
- Window capture works
- Execution tools work (`xdotool`, `xclip`, `maim`)
- Recognition strategy switched to multimodal-first at the design level

## Next implementation step

Replace screenshot -> OCR -> heuristic branching with screenshot -> multimodal JSON -> action execution.
