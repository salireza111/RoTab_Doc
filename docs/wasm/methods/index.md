# Method catalogue

All eight methods share one scientific module/database. Each has a separate standalone import and documentation page; importing several methods does not create several engine copies. Create one client for sequential operations, or several explicitly scheduled clients for independent parallel models.

| Import suffix | Function / instance method | ABI ID | Changes sequence | Fixed work budget |
| --- | --- | --- | --- | --- |
| [/score](score.md) | `score` | `score` | No | Scoring only |
| [/relax](relax.md) | `relax` | `relax` | No | One torsion FastRelax repeat |
| [/minimize](minimize.md) | `minimize` | `minimize` | No | ≤200 L-BFGS iterations |
| [/repack](repack.md) | `repack` | `repack` | No | One side-chain packing round |
| [/fixed-backbone-design](fixed-backbone-design.md) | `fixedBackboneDesign` | `fixed_backbone_design` | Yes | One fixed-backbone packing/design round |
| [/fastdesign](fastdesign.md) | `fastDesign` | `fastdesign` | Yes | One FastDesign repeat |
| [/cartesian-minimize](cartesian-minimize.md) | `cartesianMinimize` | `cartesian_minimize` | No | ≤200 Cartesian iterations |
| [/cartesian-relax](cartesian-relax.md) | `cartesianRelax` | `cartesian_relax` | No | One repeat, ≤200 iterations per minimizer invocation |

Common options are seed, per-worker duty target, AbortSignal and observation callbacks. Repeats, convergence settings, score functions, custom constraints and residue-specific design policies are fixed rather than user-selectable in this API. [Input/output contracts](../io.md) define canonical single-chain PDB admission with no residue-count cap; finite resource limits still apply.

All eight methods passed the recorded engine's native/WASM and Chrome/Brave protocol checks. Coverage is fixture-specific: most tests use 20-residue 1L2Y, while browser FastDesign uses eight residues. Separate 1UBQ scoring extends the input-size evidence. The [benchmarks](../../benchmarks.md) describe these limits; input admission does not establish general scientific coverage.

Broader upstream application modes live in [separate research modules](../experimental.md). They are not silently routed through `client.run`, and unknown identifiers reject instead of falling back to scoring.
