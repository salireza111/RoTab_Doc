# Large protein memory handling

Memory regression testing includes an authorized private structure with 865 residues, 14,263 atom records, and 1,155,392 UTF-8 bytes. The calculation retains its protein coordinates without splitting the chain or imposing a residue-count cap. The structure and raw records are not distributed with this documentation.

## Stack and heap boundaries

Emscripten's `ccall` string conversion uses the C stack. The measured build has a 1 MiB stack, so a large PDB can exhaust it before scientific execution even when linear-memory usage remains below the 512 MiB heap ceiling.

The extension and SDK use `packages/shared/src/wasm-bridge.ts` to allocate a null-terminated UTF-8 input on the WASM heap. The bridge passes a numeric pointer, retains the allocation across asynchronous yields, and releases it after the call. It reads the current `HEAPU8` after allocation because memory growth replaces the typed-array view. Allocation failures are reported before Rosetta is entered. [Emscripten argument lifetime](https://emscripten.org/docs/api_reference/preamble.js.html#ccall).

## Atom-tree adaptations

Deep atom trees can also exceed Chromium's execution stack. The WASM build excludes synchronous `core::kinematics::tree::*` routines from Asyncify instrumentation because they cannot reach the scientific pause or snapshot hooks.

Two WASM-specific adaptations use heap worklists:

| Operation | Preserved behavior |
| --- | --- |
| Domain-map traversal | Depth-first child order, local color state, sibling color propagation, and domain assignments |
| Atom-tree release | Child ownership during cleanup and externally retained subtrees |

The native comparison retains the original recursive implementations. A native test host compared the exact iterative bodies against the recursive reference across 100 deterministic movement-mask combinations. It also checked release of unretained atoms and preservation of an externally held root's subtree. These checks passed for 20-residue 1L2Y and the larger structure, which produced 14,300 tree atoms.

The scientific ABI, score function, protocol budgets, and input-preparation policy are unchanged by these memory adaptations.

## Large-input validation

The complete 865-residue Score calculation passed in installed Chrome and Brave. The standalone SDK also processed that input after its score/minimize/relax checks. Its recorded warm WASM heap was 278,396,928 bytes (265.5 MiB).

| Measurement | Result |
| --- | ---: |
| WASM returned-coordinate energy | −1592.9555612337726 REU |
| Independent native returned-coordinate score | −1592.9555612336503 REU |
| Per-worker linear-memory ceiling | 512 MiB |

The large-input checks verified residue retention, original/prepared input provenance, and independent native rescoring. Raw private structures are excluded from the public records. Success with Score does not establish FastRelax, repacking, or sequence-design support for the same large input; packing can require substantially more memory.

Most eight-method scientific checks use 20-residue 1L2Y. The documented FastDesign fixture uses eight residues. The historical full 20-residue FastDesign result belongs to a different engine build. [Benchmark scope](../benchmarks.md).

## Parallel startup

A single-worker run compiles WASM inside its disposable worker. Concurrent extension pools compile one immutable `WebAssembly.Module` and share it through structured cloning. Each worker still owns its own instance, linear memory, filesystem, Rosetta globals, and RNG. The module is not a checkpoint and is not sent over the volunteer network. [Sharing compiled modules](https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/Module#sending_a_compiled_module_to_a_worker).

Shared compilation alone did not prevent a renderer crash during six simultaneous cold Rosetta initializations. Startup is therefore staged: the next worker begins after an earlier instance emits its first scientific frame. Initialized calculations can continue concurrently up to the configured worker limit.

A six-model Brave Score check retained all six outputs with one WASM fetch and no page errors. Its observed aggregate allocated heap peaked at 412,614,656 bytes (393.5 MiB) during staged startup. This was not a measurement of six fully initialized workers or total browser RAM. The corresponding Chrome observation did not complete the same six-output verification.

## Completion and retained memory

Completion terminates the scientific worker and clears its message/error handlers. The pool releases transient live data and its shared compiled-module reference when no further launch requires them. Saved PDBs, energy histories, and bounded coordinate frames remain available for replay and export.

The recovery path reads saved trajectories only when an incoming assignment needs a result recovered. An idle or fully delivered dashboard does not repeatedly deserialize all 20 retained runs.

**WASM heap** measures worker linear memory. **UI JS heap** estimates JavaScript allocation for the viewing page. Neither measures the complete browser tab, compiled code, renderer, GPU, or process overhead. Browser caching and garbage collection can delay reclamation after workers end. [Chrome memory measurement scopes](https://developer.chrome.com/docs/devtools/memory-problems).

## Recorded completion observations

Chrome 153 checks on October 12, 2026 sampled the largest renderer process after 30 seconds of natural idle. The measurements did not depend on forced garbage collection.

| Condition | Renderer RSS after idle |
| --- | ---: |
| Bundled single-worker FastRelax before the lifecycle change | Approximately 524 MiB |
| Bundled single-worker FastRelax after the lifecycle change | Approximately 185 MiB |
| First of two sequential Score runs on the private 865-residue input | Approximately 493 MiB |
| Second Score run on that input | Approximately 346 MiB |
| Two-worker 1L2Y Score | Approximately 281 MiB |

The FastRelax runs used different seeds and were not a controlled matched-seed benchmark. Both used the same scientific engine and 75% diagnostic intensity, which differs from participant defaults.

The two large-input Score runs produced identical output hashes and energies. Both workers terminated, and their results and initial/final frames remained saved. The two-worker 1L2Y check likewise retained both seeded outputs and terminated both workers after one shared compilation.

These observations did not reproduce persistent 1.5 GB retention. They do not establish a universal memory ceiling or reproduce a user's existing browser profile. Operating-system RSS also differs from Chrome's tab-hover attribution.
