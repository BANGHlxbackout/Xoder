# Xoder extensions

Xoder extensions are Python modules that can register custom tools and slash commands, observe lifecycle events, intercept tool calls and results, show UI dialogs, and customize message rendering.

## Start here

When working in an Xoder checkout, read:

- `examples/extensions/hello_tool.py` and `examples/extensions/permission_gate.py`
- `src/xoder_coding/extensions/api.py`
- `tests/test_extensions.py`

Installed examples are under `examples/extensions/` next to these docs. Read the relevant example completely before implementing an extension.

## Locations

- `~/.xoder/extensions/`: discovered by default.
- `<project>/.xoder/extensions/`: enabled explicitly with `--project-extensions`.
- `xoder -x PATH`: explicitly load a file or directory.

An extension defines `setup(xoder)`. Project extensions execute arbitrary Python and are disabled by default; enable only trusted repositories.

## Development checklist

1. Confirm the requested capability exists in the extension API before inventing a workaround.
2. Keep extension behavior out of `xoder_agent`; extensions belong to `xoder_coding`.
3. Use `xoder_agent` types for portable messages and tools, and keep Textual behind Xoder's UI adapter APIs.
4. Start from the closest installed example.
5. Add deterministic tests with fake providers/tools when changing Xoder's extension implementation.
6. Run the repository's documented tests, Ruff checks, formatting, and mypy.
