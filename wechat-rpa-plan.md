# WeChat RPA Multimodal-First Plan

## Current principle

- Recognition: multimodal (pure vision, no OCR)
- Execution: xdotool/xclip/maim on XPS

## Real gap to close

The missing chain is:

1. capture screenshot from XPS
2. bring screenshot back to cloud/workspace
3. produce structured action JSON
4. execute on XPS
5. capture again
6. verify result

## Minimal practical architecture

### On XPS
- `capture_wechat_window.sh` — capture current WeChat window
- `send_message_manual_exec.sh` — execution-only script

### On cloud workspace
- `scripts/xps_pull_wechat_window.sh`
  - trigger remote capture on XPS
  - stream screenshot back to local workspace
- `scripts/xps_exec_wechat_send.sh`
  - call execution-only script on XPS
- `artifacts/wechat-rpa/`
  - store before/after screenshots
  - store latest structured action JSON

## JSON contract

```json
{
  "screen": "wechat_main|wechat_chat|wechat_search_results|wechat_login|wechat_qr|wechat_popup|unknown",
  "active_contact": "string|null",
  "input_box_visible": true,
  "send_button_visible": true,
  "risk_popup": false,
  "recommended_action": {
    "type": "click|double_click|type|paste|keypress|noop",
    "target": "search_box|first_contact|input_box|send_button|popup_close|unknown",
    "x": 0,
    "y": 0,
    "text": "",
    "keys": []
  },
  "confidence": 0.0,
  "reason": "short explanation"
}
```

## Honest status

As of now, the multimodal-first **design direction is switched**, but the actual automated multimodal inference call is not yet wired into the loop.

The next concrete milestone is:
- make screenshot capture + pullback stable
- make action/result JSON and before/after artifacts stable
- then plug a real multimodal model into the recognition step
