# Rosetta C++ to WebAssembly architecture

The port compiles Rosetta's C++ scientific implementations for execution in browser workers. Platform adaptations provide browser-compatible builds, resource loading, cooperative scheduling and measured snapshots. The production coordinate API uses a harness with fixed protocol settings; it does not expose the unrestricted native command-line application.

## 1. Source pinning and build assembly

`scripts/fetch-engine.sh` checks out Rosetta commit `369e400415dd5c585f80dcf7b647147ee520e8ba`, initializes selected upstream submodules and activates Emscripten 6.0.11. `scripts/prepare-engine.py` checks the source HEAD, generates Rosetta options/type definitions and constructs CMake source lists from upstream project manifests.

Core/utility/scoring code is always included; `ROSETTATAB_WITH_RELAX=ON` adds the protocol libraries needed by all eight methods. Applications are not all linked into the bounded coordinate target. CUDA translation units are excluded. Native and WASM reference targets use the same harness and pinned scientific source; the build also applies the documented portability patches.

## 2. Platform adaptations

| Adaptation | Reason | Scientific effect |
| --- | --- | --- |
| Emscripten/Linux platform headers and definitions | Browser target has no native macOS/Windows ABI | Platform compilation, not energy formula replacement |
| POSIX backtrace guard | `execinfo` diagnostics are unavailable | Diagnostic fallback only |
| Bundled SQLite header; static dependencies | Avoid host-specific database/backend/linker dependencies | No task-server dependency in participant |
| Disable thread/shared-object/plugin loading paths | Current worker is a single CPU WASM instance | No native plugins, process/MPI/pthread execution |
| Merge split Boost headers | Portable header layout | Build adaptation |
| Bounded energy-method registration | Avoid linking unrelated creators into browser startup | Limits supported score/chemistry surface; not arbitrary Rosetta support |
| Traced database reads | Identify files used by admitted fixtures | Reduced resources need validation; a trace is not universal coverage |
| Heap-backed PDB arguments | `ccall`'s temporary string uses the 1 MiB C stack | Same complete input bytes; buffer retained across asynchronous yields |
| Iterative atom-tree release in WASM | Avoid a recursive shared-pointer cleanup cascade exceeding the browser stack | Ownership cleanup only; retained subtrees and scientific state are preserved; native reference unchanged |
| Iterative domain-map traversal in WASM | Deep recursive traversal can exceed Chromium's baseline VM stack | Preserve depth-first child order, sibling color propagation and domain assignments; native reference unchanged |

The registration list is `engine/ref2015-creators.txt`. Native reference registration remains complete; the WASM registry retains the supported REF2015-related creators. Excluded methods are unavailable through this host, with no substitute approximation.

## 3. Scientific ABI

`engine/rosettatab.cc` imports the PDB into an upstream `Pose`, constructs REF2015, resets the RNG to the requested seed and selects one allowlisted protocol. It calls upstream `FastRelax`, `MinMover`, `PackRotamersMover` or `FastDesign`, with the exact bounded settings documented per method. The final output includes sequence, rounded-coordinate REF2015 energy and separately identified objective energy.

Initialization uses explicit database path, constant seed and non-binary Dunbrack loading options. Rosetta's global options are initialized once per worker. Each subsequent coordinate call resets the RNG seed. No remote RosettaScripts, command strings, arbitrary score functions or executable modules enter this interface.

## 4. Browser asset package

`engine/CMakeLists.txt` builds ES-module output with `MODULARIZE`, `EXPORT_ES6`, environments `web,worker,node`, exceptions, memory growth, a 128 MiB initial heap and a 512 MiB maximum. The normal measured build uses `-O1`. The exported entry points are `rosettatab_run_protocol`, legacy `rosettatab_run` and `main`; `ccall`, filesystem and heap interfaces support the host.

The package has three scientific files:

- `rosetta.mjs`: Emscripten factory/glue and preloaded-resource mapping.
- `rosetta.wasm`: compiled scientific/runtime code.
- `rosetta.data`: required database bytes mounted under `/database` in the virtual filesystem.

The engine with large-input memory adaptations totals 146,090,371 uncompressed bytes: 473,285 bytes of JavaScript glue, 117,465,890 bytes of WASM and 28,151,196 bytes of database resources. These sizes describe the scientific files rather than the private ZIP archive. Hashes identify the exact measured artifacts. [Emscripten file packaging](https://emscripten.org/docs/porting/files/packaging_files.html).

## 5. Cooperative scheduling and trajectory preservation

The browser ABI uses Asyncify so `emscripten_sleep` can yield to a worker's event loop. A hook between score evaluations measures active quanta and sleeps according to the requested duty target. It does not modify coordinates or consume random draws. Initialization is synchronous until the harness enables yielding. [Emscripten Asyncify](https://emscripten.org/docs/porting/asyncify.html).

Generated static constructors/options registration, enum dictionaries, topology parsing and energy-table setup caused excessive VM compilation allocations when fully instrumented. The measured build excludes specific synchronous routines from Asyncify instrumentation while preserving it on scientific callers that can yield. Earlier full builds crashed; the bounded build passed normal Chrome/Brave VM checks. Diagnostic flags are not required by participants.

Atom-tree routines are also excluded from Asyncify: coordinate/domain-map traversal and destruction do not call the scientific pause or snapshot hooks. Instrumenting every recursive frame unnecessarily consumes the VM stack for larger proteins. Two WASM-only adaptations use heap worklists for atom release and domain-map traversal. The domain-map traversal preserves depth-first order and the parent's color changes before visiting the next sibling. Native retains the original recursive implementation for comparison.

This is cooperative execution within one worker, not a portable serializable continuation. Worker termination destroys that execution stack. The extension checkpoints completed models; the SDK caller must implement its own completed-work persistence.

### Startup and power budget

There are several different startup costs: fetching assets, compiling immutable WASM code, instantiating memory/filesystem, Rosetta `core::init::init`, importing the Pose and building/scoring energy tables. The first emitted scientific frame follows those preparation steps. A finished Emscripten factory or a responsive page therefore does not mean Rosetta is already warm.

In `rosettatab_run_protocol`, `initialize(seed)` currently runs **before** `duty_percent` and `quantum_started` are set. Later hooks yield after accumulated work of about 12 ms, sleeping in proportion to the requested duty target; long synchronous sections are not preempted. Display snapshot scoring itself also takes work. The intensity setting is an approximate cooperative budget, not a total-machine CPU or temperature limit.

Concurrent extension pools share a compiled module, while single-worker runs compile inside their worker. The extension terminates each model's instance on completion, so scientific initialization can recur for each model. The SDK keeps an instance warm across sequential calls. Comparative hardware and fan measurements have not established the cause of temperature differences between M-series laptops. Extension defaults are one worker/10%, with a 30-second rest between automatic network models. The standalone SDK defaults to 25% when the option is omitted; `dutyCycle: 10` explicitly selects a lighter cooperative budget.

### Host memory boundary

`packages/shared/src/wasm-bridge.ts` UTF-8 encodes the complete PDB, allocates its bytes plus a NUL in the WASM heap, reads the current `HEAPU8` after allocation, and calls the fixed ABI with a numeric pointer. The allocation remains live across Asyncify yields and is released in `finally`. This avoids copying a large upload onto the separate 1 MiB C stack. Memory growth replaces typed-array views; callers must not retain an old heap view across allocations. [Emscripten C/JavaScript calls](https://emscripten.org/docs/api_reference/preamble.js.html#ccall).

The final JSON string belongs to the harness's static response buffer. Parse/copy it before another call, and never enter the same module concurrently. Isolated workers provide separate scientific global state; JavaScript promises alone do not make Rosetta globals reentrant.

## 6. Intermediate scientific snapshots

| Source hook | Snapshot meaning |
| --- | --- |
| Harness before/after protocol | Initial imported pose and final returned coordinates |
| `protocols/relax/FastRelax.cc` | Pose at fixed script-command boundaries |
| `core/optimization/AtomTreeMultifunc.cc` | Torsion minimizer pose synchronized after derivative evaluation |
| `core/optimization/CartesianMultifunc.cc` | Corresponding Cartesian derivative state |
| `core/pack/pack_rotamers.cc` / `FixbbSimAnnealer.cc` | Reconstruct a complete accepted rotamer assignment on a copy |

The C++ display bridge copies the pose, removes unsuitable minimizer neighbor-list/cache state, independently scores the copy with full REF2015 and emits PDB/energy metadata through an `EM_JS` callback. Accepted packing assignments live in the annealer until committed, so the bridge reconstructs them on a copy instead of reading stale original coordinates. Internal updates are throttled to approximately one per 200 ms.

Display scoring does not alter the scientific pose or RNG. Recorded validation compares seeded results with the live bridge disabled and enabled. The bridge exposes calculation states without shortening minimizer steps or changing convergence to increase visual motion. Native Rosetta@home graphics use a separate shared-memory implementation. [Pinned native graphics definition](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/protocols/boinc/boinc_shmem.hh).

## 7. Standalone browser host

The standalone SDK uses the same scientific ABI and verified engine bytes. It validates the manifest and hashes, compiles the checked WASM buffer with `WebAssembly.compile` and supplies the supported `instantiateWasm` callback to the Emscripten factory. Verified database bytes enter through `getPreloadedPackage`. This factory does not accept `Module.wasmBinary`; the supported callback permits standalone hosting without modifying or rebuilding the Rosetta glue.

The SDK worker maps `globalThis.rosettatabSnapshot` to typed messages, validates final result identity and adds input/output hashes and timing scopes. One client owns one worker; distinct method imports route to the same fixed ABI. React, Nostr, extension permissions and native clients are absent from this layer. [Emscripten C/JS interoperation](https://emscripten.org/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.html).

## Validation boundaries

Compilation is not proof of general scientific equivalence, arbitrary database support or official task acceptance. Native/WASM fixed-coordinate agreement and output rescoring are measured gates for recorded fixtures. Broader methods, chemistry, full workunit semantics, performance, project approval and public distribution each require their own evidence.
