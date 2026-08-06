# Xoder CLI and commands

Xoder supports print mode and a Textual interactive TUI. The CLI entry point is `xoder_coding.cli:app`.

For current user-facing behavior in an Xoder checkout, read:

- `README.md`
- `src/xoder_coding/cli.py`
- `src/xoder_coding/commands.py`
- `tests/test_cli.py` and `tests/test_commands.py`

Keep command parsing and application-specific resource loading in `xoder_coding`, not the reusable `xoder_agent` harness. When changing behavior, test both command results and the relevant print/TUI integration, then update the README or bundled reference documentation.
