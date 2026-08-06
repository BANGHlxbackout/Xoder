# Xoder providers and models

Xoder separates provider/model streaming (`xoder_ai`), the portable harness (`xoder_agent`), and application configuration (`xoder_coding`).

## User configuration

Use `/login` and `/model` for built-in providers. The custom-provider flow supports OpenAI-compatible endpoints. Durable provider settings live under Xoder's home directory. In an Xoder checkout, the built-in schema and models are defined in `src/xoder_coding/data/catalog.toml`, with configuration behavior covered by `src/xoder_coding/provider_config.py` and its tests.

## Changing the built-in catalog

Use the bundled `xoder-model-catalog` skill when adding or updating a first-party model/provider. The source of truth is:

```text
src/xoder_coding/data/catalog.toml
```

Do not guess model IDs, context limits, modalities, reasoning values, output limits, or pricing. Verify them in official provider documentation. Confirm Xoder supports the transport before adding a provider. Preserve existing defaults unless a change is intentional.

Relevant tests usually include:

```text
tests/test_provider_catalog.py
tests/test_provider_config.py
tests/test_provider_runtime.py
```

Update this bundled provider guide and directly relevant tests for substantial user-facing changes.
