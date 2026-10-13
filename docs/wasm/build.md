# Build and validation reference

This chapter describes source builds and validation. Participants use packaged browser assets; rebuilding the scientific engine is optional. The coordinate port, standalone SDK and documentation require no Docker or task server.

## Scientific prerequisites

Rebuilding requires an authorized Rosetta source checkout, Git, Python, CMake, a native C++ toolchain and the pinned Emscripten SDK. Repository scripts fetch and build the source and dependencies, which can require substantial storage and build time. Existing verified artifacts can be reused for private SDK development after hash verification.

```sh
npm run engine:fetch
ROSETTATAB_WITH_RELAX=ON npm run engine:configure
ROSETTATAB_WITH_RELAX=ON ROSETTATAB_BUILD_MODE=native npm run engine:build
ROSETTATAB_WITH_RELAX=ON ROSETTATAB_BUILD_MODE=wasm npm run engine:build
```

The historical `WITH_RELAX` option name enables the complete current coordinate protocol set, including design/minimization. `ROSETTATAB_JOBS` controls compiler parallelism. Build-time concurrency is separate from scientific browser worker count. `ROSETTATAB_DATABASE` can choose a candidate database path; use the proven reduced database for matching existing artifacts.

## Reduced database preparation

The full upstream database is much larger than the measured browser package. Candidate resources are selected from actual successful native reads using `ROSETTATAB_TRACE_DATABASE=1` and `scripts/package-database.py`.

```sh
mkdir -p build
ROSETTATAB_TRACE_DATABASE=1 engine/artifacts/native/rosettatab-native \
  --input apps/extension/public/fixtures/1l2y.pdb \
  --database .vendor/rosetta/database --protocol relax --seed 17 \
  2> build/database-trace.log
python3 scripts/package-database.py build/database-trace.log
```

This single example creates only a **candidate** for its exercised reads. It is insufficient to reconstruct the current expanded 908-resource catalogue by itself or certify the eight protocols. A validated database requires traces from the intended chemistry/protocol fixtures, a resource manifest, and corresponding native/browser checks. A new database changes `rosetta.data` and invalidates old exact-build evidence.

## Scientific and browser gates

```sh
npm run engine:verify-protocols
npm run build
npm run engine:verify-browser
npm run engine:verify-browser-protocols
npm run engine:verify-browser-protocols -- --brave
npm run engine:verify-inputs
npm run engine:package
```

Native/Node protocol checks compare all eight methods and rescore outputs. Installed Chrome/Brave checks exercise normal VMs, live callbacks and matching assets. Recovery/input checks are separate. `engine:package` refuses changed or unverified builds and writes `engine/artifacts/verified`. This is the scientific payload used by the extension and standalone bundle.

## Standalone adapter

```sh
npm run sdk:build
npm run sdk:pack
npm run sdk:bundle
npm run sdk:verify-browser
```

The first command bundles original adapter/input-validation code with esbuild and emits declarations through TypeScript. It does not recompile or modify Rosetta. `sdk:pack` produces a local npm tarball; `sdk:bundle` makes the private static example with pinned science assets. `sdk:verify-browser` runs real score/minimize/relax through the standalone API in Chrome and Brave and independently rescores the outputs using the developer native reference.

The SDK browser verifier requires an existing static development preview at `127.0.0.1:5173` to stream the 117 MB WASM asset. The verifier does not launch that preview; other static fixtures use Playwright interception. No extension is loaded, all external requests are blocked, and records distinguish this three-method SDK smoke test from the engine's eight-protocol validation. Calculation does not contact a task API or native program; independent native rescoring is a separate validation step.

