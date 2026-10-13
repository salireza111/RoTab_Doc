# Architecture

The scientific engine is the shared layer. The extension and standalone SDK use separate worker hosts for its fixed application binary interface (ABI). The SDK is independent of the extension's session management, network and UI code. Each host has its own validation evidence.

```text
                                 pinned Rosetta C++
                                          │
                            engine/rosettatab.cc harness
                                          │ Emscripten 6.0.11
                    ┌─────────────────────┴─────────────────────┐
                    │ rosetta.mjs / rosetta.wasm / rosetta.data │
                    └──────────┬────────────────────┬───────────┘
                               │                    │
                    extension scientific       standalone SDK
                    worker host                module worker
                               │                    │
                     Session + worker pool     RosettaClient
                               │                    │
                 IndexedDB / shared tabs       caller's application
                               │
                     RoTab UI + Mol* viewer
                               │
                 campaign scheduler / WebRTC
                               │
                   Nostr discovery/signaling
```

## Component source map

| Path | Responsibility | Needed by a participant? |
| --- | --- | --- |
| `engine/rosettatab.cc` | Scientific C ABI, fixed mover settings, snapshots and duty hooks | Compiled into WASM |
| `engine/CMakeLists.txt` | Native/WASM build options | No; developer build |
| `scripts/prepare-engine.py` | Source portability and instrumentation patches | No; developer build |
| `engine/ref2015-creators.txt` | Bounded energy-method registration catalogue | Compiled into WASM |
| `packages/shared/src/` | Shared protocol/input contracts | Bundled by each host |
| `packages/rosetta-wasm/src/` | Reusable browser client, worker, types and method imports | Yes for standalone applications |
| `apps/extension/src/science.worker.ts` | Extension scientific worker host | Yes in extension |
| `apps/extension/src/session.ts` | Task supervision, pool, checkpoints and snapshots | Yes in extension |
| `apps/extension/src/campaign-queue.ts` | Publisher's durable campaign/attempt ledger | Yes for campaign publishers |
| `apps/extension/src/volunteer-network.ts` | Direct assignment/result coordination | Yes for volunteering |
| `apps/extension/src/nostr-discovery.ts` | Relay subscriptions and encrypted signaling | Yes for automatic discovery |
| `apps/api`, `native/companion`, compose files | Retained optional/legacy experiments | No in selected browser product |
| `scripts/verify-*`, benchmark comparison tools | Scientific validation tooling | No |

## One computing owner, many views

An exclusive Web Lock selects the computing tab. Other RoTabs receive BroadcastChannel status/structure updates and send controls to that owner. They do not independently start duplicate pools. Ownership is released by the browser; late heartbeats never authorize another tab to steal a lock from a suspended owner.

The owner creates dedicated workers for independent seeded models. Each worker has its own Rosetta globals, RNG, Emscripten filesystem and heap. Completed models are persisted before batch finalization. Handover replays unfinished model seeds and retains completed outputs. The extension service worker performs bookkeeping rather than hosting long scientific execution.

## Scientific message flow

1. A bundled fixture, imported benchmark or signed campaign assignment supplies PDB text, protocol and seed.
2. Admission checks the input, fixed protocol and exact source/engine/data identity.
3. The worker loads the packaged engine and calls `rosettatab_run_protocol` asynchronously.
4. C++ snapshot hooks report real coordinates and full-weight REF2015 energy from display-only copies.
5. The owner updates the focused model's history, renderer and resource readings, then broadcasts changed data.
6. A finished result is checked, hashed and durably recorded. Campaign outputs enter a signed delivery outbox.

The renderer can interpolate between measured structures for presentation. Those interpolation frames are not scientific samples. The energy chart retains measured values, including rises during optimization.

## Trust and storage boundaries

Input data is untrusted even when signed. Protocols are allowlisted and executable JS/WASM is packaged, not supplied by a job publisher. Signatures bind provenance and sender identity; they do not prove scientific correctness. Browser queue receipts establish matching durable delivery; independent scientific validation is a separate step.

The publisher is the campaign coordinator. Its IndexedDB copy is not replicated into a globally authoritative ledger. Browser storage can be cleared or evicted; experiment exports are necessary durable copies. Only the SDK's caller decides whether to retain frames/results: the SDK itself has no IndexedDB policy or autonomous uploads.

## Component boundaries and contracts

| Component | Accepts | Produces | Does not own |
| --- | --- | --- | --- |
| Input preparation | Original PDB/ENT or supported compressed input | Prepared single-chain PDB, preparation report and original/prepared hashes | Scientific scoring or silent arbitrary chemistry repair |
| Scientific C++ harness | PDB pointer, protocol ID, seed and intensity | Measured snapshots and a final JSON result | Peers, browser storage, user permissions |
| WASM host | Trusted engine assets and validated run request | Worker messages, allocated-heap telemetry, result/error | A globally authoritative project queue |
| Session and model pool | Accepted local/peer task and local resource preferences | Model checkpoints, focused trajectory and completed outputs | Relay discovery or arbitrary native execution |
| Campaign coordinator | Target, short description, independent model count and seeds | Fenced leases, signed catalogs and result receipts | Other volunteers' CPU settings |
| WebRTC transport | Signed application messages | Ordered authenticated peer delivery | Durable acceptance or proof of correct science |
| Nostr rendezvous | Signed public presence and encrypted offer/answer payloads | Discovered participants and connection signals | PDBs, scientific results or campaign storage |
| React/Mol* view | Session snapshots and local presentation state | Molecular rendering, energy graph and user controls | Execution checkpoints or interpolated scientific evidence |

The two browser hosts deliberately have different lifetimes. The **extension** shares compiled WASM code within concurrent model pools; single-worker runs compile inside their disposable worker. Each model receives an isolated instance that terminates on completion. The **standalone client** retains one instance for sequential calls until cancellation, failure or `close()`. A first call on either host includes Rosetta's lazy initialization. Reusing an SDK client can avoid repeating that initialization; reopening an extension model currently cannot. [WASM startup and resource scheduling](wasm/port.md#startup-and-power-budget).

## Storage and recovery map

| Location | Records | Recovery/deletion meaning |
| --- | --- | --- |
| `localStorage` | `rosettatab:preferences`, profile client ID, timer/presentation state | Saved opening layout and appearance are separate from each tab's current view |
| IndexedDB `rosettatab`, `state` store | `checkpoint`, `browser-results`, imported inputs | Completed models survive; unfinished work restarts from its recorded seed |
| Same store | `campaign-ledger` | Publisher's campaign, model attempts, current lease tokens and received results |
| Same store | `network-ledger`, `network-settings` | Incoming assignments, signed delivery outbox/receipts, room and optional TURN settings |
| Same store | `peer-identity`, `nostr-secret` | Persistent local signing identities; loss can break continuity with old work |
| `chrome.storage.local` | Installation timestamp | Install bookkeeping, not a scientific scheduler |
| `chrome.storage.session` | Computing-tab ID, optional Google Calendar OAuth session | Browser-session data; Calendar token is not included in experiment exports |

These are profile-local stores. Experiment export omits signing secrets, OAuth tokens and TURN credentials. Exported scientific records can still contain full uploaded structures, research descriptions and participant identifiers: review them before sharing. Clearing site data or uninstalling loses locally retained records and keys; it does not recall files already delivered to another browser.

## End-to-end calculation flow

1. The UI prepares an input and records its provenance. A local start creates a task; a network start verifies a signed assignment first.
2. The exclusive Session owner persists the batch definition before launching a scientific worker. A linked tab renders the same session without launching a second pool.
3. The pool supplies the pinned manifest identity, protocol, seed, prepared PDB and local duty budget. Cold starts are staged until an earlier worker emits its first real frame.
4. The host initializes the WASM instance and virtual filesystem, then enters the fixed C ABI with a heap-backed input buffer.
5. C++ emits actual coordinates and REF2015 scores. Session retains bounded measured frames; Mol* interpolates only for display. Progress is an estimate of protocol stages, not a time-to-completion prediction.
6. The finished model is committed locally. Network work additionally enters a durable signed outbox and remains pending until the publisher's matching receipt arrives.

Further architecture: [browser ownership and model execution](extension/sessions.md), [connection establishment](extension/connections.md), [assignment and return protocol](extension/jobs.md), and [standalone hosting](wasm/hosting.md).
