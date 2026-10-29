# engg-math-viz

Shared terminal output layer.

- `make_console()`: Rich console that honours `NO_COLOR` and degrades on non-TTY output.
- `THEME`, `panel()`, `kv_table()`: one visual style for every package.
- `emit(data, as_json=..., render=...)`: stable JSON for pipelines, rich output for humans.
- `render_latex()` / `LatexRenderable`: LaTeX via the external [`txm`](https://github.com/thatmagicalcat/txm) binary
  with a plain-text fallback. Nothing is ever installed at import or call time; install `txm` yourself (`cargo install txm`).

Plotting backends (plotext, matplotlib) will be added as optional extras.
