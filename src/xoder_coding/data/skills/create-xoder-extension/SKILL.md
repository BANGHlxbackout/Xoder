---
name: create-xoder-extension
description: Create or modify an Xoder Python extension with custom tools, commands, hooks, dialogs, or message rendering. Use for Xoder extension requests.
---

# Create an Xoder extension

1. Read the installed `docs/extensions.md` and the closest example under `examples/extensions/` relative to Xoder's packaged documentation paths in the system prompt.
2. In an Xoder checkout, also read `examples/extensions/`, `src/xoder_coding/extensions/api.py`, and the relevant implementation before coding.
3. Put user extensions in `~/.xoder/extensions/`; project extensions require explicit trust through `--project-extensions`. Use `xoder -x PATH` for isolated testing.
4. Define `setup(xoder)` and use documented registration APIs. Do not reach into private session or Textual internals.
5. Keep portable tool/message types in `xoder_agent`; keep application and UI integration in `xoder_coding`.
6. For Xoder core changes, add deterministic tests with fake providers/tools and cover reload/lifecycle behavior when applicable.
7. Run relevant focused tests followed by `uv run pytest`, Ruff lint, Ruff format check, and mypy.
8. Update `src/xoder_coding/data/docs/extensions.md` and directly relevant tests for user-facing architectural changes.

Never enable an untrusted project extension: extensions execute arbitrary Python in the Xoder process.
