# infrastructure

uv workspace for the runtime foundations and tooling of the Engineering Mathematics ecosystem. Four independently versioned distributions ([RFC-0002](https://github.com/engineering-mathematics/roadmap/blob/main/RFCs/0002-infrastructure-monorepo.md)):

| Package | Import | Role | Dependencies |
|---|---|---|---|
| `engg-math-core` | `engg_math.core` | Settings, errors, array contracts, conditioning policy | numpy |
| `engg-math-units` | `engg_math.units` | Shared pint registry, dimensional tracking | core, pint |
| `engg-math-viz` | `engg_math.viz` | Console, theme, JSON output, txm LaTeX | core, rich |
| `engg-math-devtools` | `engg_math.devtools` | Tolerance-explicit validation, benchmark regression, dependency-graph check | core, numpy |

Layering is enforced by import-linter: `devtools > viz | units > core`. Libraries must never import `devtools`.

## Develop

```bash
uv sync --all-packages
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run lint-imports
uv run pytest
```

## Release

Tag `<pkg>-vX.Y.Z` (for example `core-v0.1.0`); the version must match the package's `pyproject.toml`.
Publishing uses PyPI Trusted Publishing behind the `pypi` environment's approval.

Apache-2.0.
