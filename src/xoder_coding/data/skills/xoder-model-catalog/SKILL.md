---
name: xoder-model-catalog
description: Add or update models and providers in Xoder's built-in catalog, including verified metadata, reasoning mappings, tests, documentation, and validation.
---

# Xoder model catalog

Use this workflow for changes to Xoder's built-in providers or models. Keep discovery focused.

## Relevant files

- `src/xoder_coding/data/catalog.toml`: source of truth.
- `tests/test_provider_catalog.py`: golden metadata tests.
- `tests/test_provider_config.py`: thinking and request-config mappings.
- `tests/test_provider_runtime.py`: runtime construction when transport changes.
- `src/xoder_coding/provider_config.py`: provider request and thinking mappings.
- `src/xoder_coding/data/docs/models.md`: bundled provider and model guidance.
- `src/xoder_coding/data/release-notes/releases.json`: inspect; update only when appropriate.

## Workflow

1. Decide whether this is a model on an existing provider or a new provider.
2. Read official provider/API documentation and verify the exact model ID, endpoint, transport, authentication, context window, modalities, output limit, reasoning values, pricing, and plan restrictions.
3. Never guess undocumented metadata. Omit optional values or preserve existing defaults.
4. Confirm Xoder supports the API transport before adding a provider.
5. Preserve the existing `default_model` unless changing it is intentional.
6. Match nearby TOML compatibility metadata.

Use focused searches rather than repository-wide model dumps:

```bash
rg -n 'name = "<provider>"|<model-id>' src/xoder_coding/data/catalog.toml
rg -n '<provider>|<model-id>' tests/test_provider_catalog.py tests/test_provider_config.py tests/test_provider_runtime.py
rg -n '<provider>|<model-name>' src/xoder_coding/data/docs/models.md src/xoder_coding/provider_config.py
```

## Thinking mappings

Xoder levels are `off`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Provider-level `thinking_levels` must include every level needed by its models. Use model metadata when the wire value differs or a model supports only a subset:

```toml
thinking_level_map = { xhigh = "max" }
unsupported_thinking_levels = ["off", "minimal", "low", "medium", "high"]
```

Test both the exposed levels and the actual API value produced by provider configuration.

## Verification

Add tests for provider membership, context/metadata, thinking filtering, wire mapping, and intentionally preserved defaults. Run:

```bash
uv run pytest tests/test_provider_catalog.py tests/test_provider_config.py tests/test_provider_runtime.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Update the bundled model/provider guide and directly relevant tests for substantial behavior. Link authoritative documentation and mention plan-dependent limits. Report any check that cannot run and why.
