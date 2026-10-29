# engg-math-devtools

Test-time tooling. Libraries never import this package.

- `assert_close(actual, expected, *, rtol, atol)`: tolerances are mandatory keyword arguments; failures report max abs/rel error and its index.
- `measure` / `find_regressions`: wall-clock benchmarks and baseline comparison.
- `check_graph`: verifies the ecosystem dependency graph is acyclic and points down the tiers.

```bash
python -m engg_math.devtools.graph path/to/*/pyproject.toml
```
Exit code 1 on any violation.
