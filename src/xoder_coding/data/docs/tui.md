# Xoder TUI

Xoder's full interactive interface uses Textual behind an adapter boundary. `xoder_agent` emits provider-neutral events; `xoder_coding.tui` consumes and renders them.

For current behavior in an Xoder checkout, read:

- `src/xoder_coding/tui/`
- `tests/test_tui_app.py`
- `tests/test_tui_components.py`

Do not introduce Textual dependencies into `xoder_agent`. Keep reusable behavior in the harness/session layers and UI behavior in the adapter. Use Textual pilot tests and fake providers for deterministic interaction tests.
