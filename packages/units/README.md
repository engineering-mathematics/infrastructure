# engg-math-units

One shared `pint` registry for the whole ecosystem, plus axis-level dimensional tracking for matrices.

- `get_registry()`: process-wide registry. Quantities from different registries cannot be mixed, so never create your own.
- `DimensionalTracker`: per-axis units. Entry `A[i, j]` carries `row[i] / col[j]`.
- `DimensionalTracker.validate_matmul(a_cols, b_rows)`: raises `DimensionalError` on mismatch.

Dimensionless axes are compatible with any unit by design. Pass explicit units to opt out of that leniency.
