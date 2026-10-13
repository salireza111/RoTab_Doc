# API and lifecycle

All public declarations are generated under `packages/rosetta-wasm/dist/`. The root import exports the client, methods, input utilities, protocol IDs, engine/source constants and typed events/results. Individual method subpaths are listed in the [catalogue](methods/index.md).

## Client construction and execution

```ts
const client = createRosetta({
  engineUrl: "/science/engine/",
  workerUrl: "/science/sdk/worker.js", // optional when default relative worker remains intact
});
const result = await client.run("minimize", pdb, options);
client.close();
```

`engineUrl` is a directory URL without query or fragment. It contains the four required engine files. One client owns one reusable dedicated worker. Construction does not calculate; `run` validates the request before creating its worker. Concurrent calls on the same client reject as busy. After a successful result, the next call reuses the module and resets the RNG seed. Separate clients are independent workers with independent memory.

The SDK checks the exact measured manifest, source and eight-protocol catalogue, then hashes the JS glue, WASM and database before instantiation. Verified WASM/database bytes are passed to the factory. JavaScript is imported from the trusted static URL after checking it; use immutable/versioned hosting. Pin checks detect mixed or corrupted deployments but cannot attest an untrusted browser or a hostile server that changes its response between checking and importing.

## RunOptions

| Field | Contract |
| --- | --- |
| `seed` | Integer from 1 to 2,000,000,000; default 17 |
| `dutyCycle` | Integer from 10 to 75; default 25; cooperative per-worker active-time target |
| `signal` | AbortSignal; abort terminates the worker and rejects with `AbortError` |
| `onPhase` | `verifying-assets`, `loading-module`, `calculating` |
| `onSnapshot` | Actual structure/REF2015 state callback |
| `onLog` | Optional Rosetta/runtime diagnostic strings; not structured scientific output |

Observer callback exceptions are logged and do not strand the scientific promise. There is no timer-enforced scientific deadline in the client; a caller can use an AbortController and its own watchdog. No arbitrary score weights, repeat counts, scripts, command-line flags or movers are accepted.

## StructureSnapshot

| Field | Meaning |
| --- | --- |
| `pdb`, `energy` | Actual intermediate structure and common REF2015 energy in REU |
| `source` | `initial`, `stage`, `minimizing`, `packing`, `final` |
| `sequence` | Per-call callback sequence, reset for each run |
| `iteration` | Source callback counter; not guaranteed to be an accepted optimizer step |
| `progress` | Stage estimate; some methods stay at zero until final; not time remaining |
| `timestamp` | Wall-clock callback timestamp, milliseconds |
| `heapBytes` | Allocated WASM linear memory at callback time; excludes process/compiler/viewer overhead |

Callback rate is scientific-state dependent, with a nominal internal 200 ms throttle. A `final` snapshot can arrive before final host hashing/validation resolves the Promise. Retain frame IDs together with a run/model identity if combining trajectories.

## Result

`pdb`, `energy`, `protocol`, `scoreFunction`, `sequence` are the scientific output. `energy` is REF2015 evaluation of the **returned PDB-rounded coordinates**. `objectiveEnergy` and `objectiveScoreFunction` describe the optimization objective before serialization. Cartesian methods use `ref2015_cart`; all reported final energies use `ref2015`.

`activeMs`, `sleepingMs`, `yields`, `liveSnapshots`, `minimizerEvaluations` and `packingMoves` are harness diagnostics. They are not OS CPU time, physical time or counts of scientifically independent samples. Their accounting omits some unyielded trailing work and does not replace a controlled performance experiment.

`provenance` records engine/source IDs, the three measured file hashes, input/output SHA-256, seed and duty target. It identifies bytes and settings; it does not cryptographically prove execution or native equivalence.

| Timing field | Scope |
| --- | --- |
| `initializationMs` | Cold SDK asset download/checking plus Emscripten factory; zero when reusing a loaded worker |
| `calculationMs` | The C ABI call, including lazy scientific initialization on the first call |
| `totalMs` | Worker-side request through final validation/hash preparation; excludes caller render/download/network delivery |

## Abort, close and restart

Abort terminates the current worker. The client may start a fresh worker on a later run, but unfinished scientific state is lost. Calling `close()` releases its worker, aborts pending work and permanently closes the client. Create another client for further work.

The standalone SDK does not implement pause/checkpoint/recovery or choose half the cores automatically. Its caller schedules separate seeded runs and persists completed outputs. RoTab's Session supplies those product behaviors above the same C ABI. Replaying an unfinished seed is not a resume from the last displayed PDB.

## Errors

Invalid inputs, unknown protocols, seed/intensity bounds, changed manifests, corrupted assets, load/runtime failures and invalid result contracts reject the run. A worker error terminates that worker before another attempt. Resource exhaustion is possible even for an admitted PDB because finite browser/compiler/heap memory remains. No method silently falls back to a different calculation.

## Low-level C ABI

```cpp
const char* rosettatab_run_protocol(
    const char* pdb, const char* protocol, int seed, int duty_percent);
```

Allocate the PDB as a null-terminated UTF-8 buffer on the WASM **heap**, then use Emscripten `ccall` with return type `string`, argument types `["number", "string", "number", "number"]`, values `[pdbPointer, protocol, seed, duty]` and `{ async: true }`. Keep the buffer allocated until the asynchronous call settles, and release it in `finally`. Read the current `HEAPU8` after allocation because memory growth replaces its view.

`ccall` string conversion places the complete argument on the C stack, which is only 1 MiB in this build. Large PDBs require the heap-buffer path. The extension and standalone worker share `packages/shared/src/wasm-bridge.ts`; both capture the pinned binary's existing `malloc`/`free` exports through the supported `instantiateWasm` hook. [Emscripten string and pointer arguments](https://emscripten.org/docs/api_reference/preamble.js.html#ccall).

Parse the returned JSON and reject its `error` field. The returned C string points to a harness-owned static response; copy/parse it before another call. The ABI permits only one active invocation per module. `rosettatab_run(pdb, relaxFlag, seed, duty)` remains only for older pilot compatibility. The SDK exposes the safe worker host rather than requiring consumers to manage globals manually.
