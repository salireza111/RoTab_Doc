# Current capabilities

This reference distinguishes supported features, recorded validation, and experimental work. Compilation, transport delivery, scientific validation, and official project acceptance are separate results.

| Component | Status | Validation boundary |
| --- | --- | --- |
| Eight coordinate methods | Supported | Native/WASM and Chrome/Brave checks, principally 1L2Y with seed 17 |
| Standalone browser API | Supported | Dedicated worker, typed results, asset verification, and cancellation; scientific SDK checks cover score/minimize/relax |
| Molecular and energy display | Supported | Measured callbacks, bounded retained frames, and baseline comparison |
| Independent parallel models | Supported in the extension | One isolated worker per model; no threading within a trajectory |
| Shared tabs and model recovery | Supported | Exclusive Web Lock, BroadcastChannel, and IndexedDB; unfinished seeds replay |
| Campaign coordination | Supported | Nostr discovery, signed catalogs, WebRTC assignments/results, and publisher-owned storage |
| TURN relay fallback | Supported in the shared pilot | Eight returned and natively rescored models across isolated Chrome/Brave profiles on one computer |
| Protein-only input preparation | Supported | Visible removal report, original retention, and a natively rescored 20-residue fixture |
| Personal widgets | Supported | Optional Simple-view tasks and drawing/notes; left, middle, or right placement |
| Different-network volunteer reliability | Not established | Recorded multi-profile acceptance shared one computer |
| Cyclic peptides and full upstream dispatcher | Experimental | Separate compiled modules with incomplete browser/scientific coverage |
| Official BOINC task replay and result submission | Not implemented | No project-approved task feed, accepted result, or credit |
| Public scientific binary distribution | Unresolved | Rosetta redistribution authorization has not been established |

## Version identity

The interface described here is RoTab 0.5.6. The packaged private pilot is 0.5.2; later input-preparation, personal-widget, and documentation-link updates have separate interface checks. Those checks do not repeat the complete scientific/network acceptance matrix.

| Component | Identity |
| --- | --- |
| Browser network protocol | `3` |
| Default discovery room | `rotab-pilot-v3` |
| Standalone adapter | `0.1.0` |
| Coordinate engine | `rosetta-protocols-v2` |
| Scientific source | `369e400415dd5c585f80dcf7b647147ee520e8ba` |
| Emscripten | `6.0.11` |

Each validation record binds its own inputs and runtime hashes. The scientific source is not asserted to match Rosetta Beta 6.06, Rosetta 4.20/4.21, Mini 3.78, or the Beta 6.04 reference executable used in the comparison experiment.

## Resource defaults

The extension defaults to one worker at 10% cooperative intensity and a 30-second rest between automatic network models. Rotation defaults on with a saved opt-out. Scientific startup can precede cooperative throttling and repeats in fresh model workers. These settings are not thermal guarantees.

The standalone API has a separate 25% default when intensity is omitted. Its client can retain a warm instance for sequential calls. [Worker lifecycle](extension/sessions.md) and [memory scope](wasm/memory.md) explain these differences.

## Experimental components

The source workspace retains optional Fastify/PostgreSQL queue code and a native BOINC companion experiment. They are outside the browser participant product. Participants do not need those services or a native helper.

The [scope reference](roadmap.md) describes development areas; the [evidence inventory](evidence.md) identifies the limits of recorded measurements.
