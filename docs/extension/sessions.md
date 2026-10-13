# Browser sessions, workers and recovery

## Computation ownership

`Session` in `apps/extension/src/session.ts` is the supervisor. The Manifest V3 background service worker can be suspended by Chromium, so it only performs install bookkeeping and helps locate/focus the computing tab. Scientific execution lives in dedicated workers owned by an open RoTab page.

An exclusive Web Lock elects one computing owner per browser profile. Linked tabs receive state through BroadcastChannel and send controls to the owner. A quiet or suspended owner is not replaced merely because a heartbeat is late: the browser must release the lock. Different devices/profiles have independent owners and signing identities.

The main tab's favicon reflects status; linked tabs retain a neutral Histidine outline. The Histidine beside the RoTab text reflects session status in both views. A linked tab offers **Go to main tab** for owner-only changes. Navigating between Simple and Dashboard is local to that tab. Choosing a preferred opening layout in Appearance controls future new tabs, rather than copying another tab's current navigation.

## Model pool

`BrowserModelPool` supervises independent models, not parallel parts of one trajectory. Each model has a task/seed, status, execution budget, history, retained structures and optional final result. A single-worker run compiles the engine inside that disposable worker. Concurrent pools share a compiled `WebAssembly.Module`; every worker still owns separate linear memory, filesystem, Rosetta globals and RNG state. The pool releases its module reference once all remaining models have launched, and on stop/completion. Worker message/error handlers and transient live readings are cleared when the corresponding worker ends. Saved structures and histories remain available.

```text
Session owner ── checkpoint: input + protocol + model IDs/seeds
      │
      ├── shared compiled WASM module (concurrent pools only)
      ├── model worker A → snapshots → final result → terminate
      └── model worker B → snapshots → final result → terminate
      │
      └── commit completed model → update focused view → fill available slot
```

Local batches use the configured concurrency. Defaults are **one worker at 10% cooperative intensity**; older implicit half-core/25% profiles migrate once, while distinct custom settings remain. A network browser accepts at most one network model at once and rests for 30 seconds after a completed model. The publisher's **Also calculate on this browser** option participates through the same network queue.

Cold starts are staged until the first scientific snapshot proves an earlier instance completed expensive preparation. This reduces overlapping startup allocation. It does not cap memory for arbitrary inputs or make initialization fully cooperative.

## Checkpoint boundaries

Before execution, the batch's original input, protocol, model identities and seeds are durable. When a model finishes, its output is committed before the batch is considered complete. The latest 20 completed browser run records are retained. A resumed batch skips completed models and replays unfinished seeds.

Pause/stop, tab discard and owner closure terminate active workers. A checkpoint does **not** contain a suspended minimizer stack, RNG continuation or full annealer state. Retained intermediate PDBs are display records, not executable checkpoints. A paused run may therefore redo unfinished computation when resumed.

Only the computing tab registers a `beforeunload` warning, and only while an identified calculation is loading or running. The handler checks the live session before requesting confirmation. Canceling departure leaves workers and ownership intact; accepting it allows the normal `pagehide` cleanup and lock release. Linked tabs and inactive runs do not register the warning. The browser controls the dialog text and may suppress it without prior page interaction or during a forced shutdown.

Closing the final RoTab stops scientific execution. A surviving linked tab can become owner after lock release and recover the saved boundary. Saved automatic continuation controls whether recovered work resumes automatically. Browser storage loss/eviction is outside this recovery mechanism.

## Display pipeline

Scientific callbacks include PDB, energy, source, sequence, iteration and timestamp. The owner follows one identified model; the chart does not interleave unrelated models. Per model, history retains up to 2,000 energy samples and at most 240 coordinate frames within an estimated 8 MiB frame budget. Large structures may therefore have more energy samples than retained coordinate frames.

Broadcasts carry frame metadata and new/changed coordinate payloads. Clock-only updates do not retransmit every PDB. A newly linked viewer receives a full frame reset. UI broadcasts are capped at five per second; the internal snapshot throttle is nominally 200 ms and does not guarantee continuous callbacks during a long operation.

Mol* draws the molecule on a transparent canvas at up to 30 FPS. Hidden/offscreen viewers skip drawing. Automatic rotation defaults on and its Settings/viewport controls save the same preference. Reduced motion disables rotation; selecting a residue pauses it for inspection. Smooth coordinate interpolation changes presentation only, and never inserts synthetic energies into the graph.

## Implementation reference

| Concern                                                   | Source                                                           |
| --------------------------------------------------------- | ---------------------------------------------------------------- |
| Owner election, commands and checkpoints                  | `session.ts`                                                     |
| Launch, staged startup, completion and worker termination | `browser-pool.ts`                                                |
| Compile code shared within a concurrent pool              | `science-module.ts`                                              |
| Packaged manifest and scientific worker events            | `science.worker.ts`                                              |
| PDB argument allocation/lifetime                          | `packages/shared/src/wasm-bridge.ts`                             |
| Local storage and migrations                              | `storage.ts`, `compute-settings.ts`                              |
| Measured-frame retention and inspection                   | `snapshot-frames.ts`, `EnergyChart.tsx`, `SnapshotInspector.tsx` |
| Molecular rendering and saved orbit                       | `Protein.tsx`, `protein-motion.ts`                               |

See [resource/heat limitations](lifecycle.md#resource-readings) and [Help](../help/calculations.md) for user controls.
