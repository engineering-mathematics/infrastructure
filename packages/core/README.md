# engg-math-core

Shared base for the Engineering Mathematics packages. Depends on NumPy only.

- `Settings` / `get_settings` / `configure` / `override`: precision and conditioning thresholds, env-overridable.
- Error hierarchy rooted at `EnggMathError`.
- Array contracts: `as_fortran`, `require_fortran`, `require_shape`.
- `check_condition`: warn or raise on ill-conditioned solves.

```python
from engg_math.core import as_fortran, check_condition, override

with override(kappa_error=1e9):
    check_condition(2e8)
```

Environment: `ENGG_MATH_PRECISION` (`float32`|`float64`), `ENGG_MATH_STRICT`, `ENGG_MATH_KAPPA_WARNING`, `ENGG_MATH_KAPPA_ERROR`.
