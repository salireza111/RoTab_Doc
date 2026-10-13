# RoTab and Rosetta WebAssembly

RoTab is a Chromium new-tab extension for protein visualization and browser-based scientific computation. Selected Rosetta C++ methods are compiled to WebAssembly (WASM) and run in dedicated browser workers. The standalone library, `@rotab/rosetta-wasm`, exposes the same eight methods to other browser applications.

This reference describes RoTab 0.5.6, standalone adapter 0.1.0, and scientific source commit `369e400415dd5c585f80dcf7b647147ee520e8ba`. Validation records identify the versions and artifact hashes tested. The latest packaged private pilot is 0.5.2; later interface updates have separate validation records.

## Documentation guide

| Topic | Reference |
| --- | --- |
| Extension installation and participation | [Install and contribute](extension/usage.md) |
| Controls and common questions | [Illustrated Help](help/index.md), [troubleshooting](help/troubleshooting.md) |
| Rosetta and BOINC responsibilities | [BOINC comparison](boinc.md) |
| Rosetta in another browser application | [Standalone quick start](wasm/quickstart.md), [method catalogue](wasm/methods/index.md) |
| Static assets, workers, and application integration | [Deployment and integration](wasm/hosting.md) |
| Peer connections and job delivery | [Connection architecture](extension/connections.md), [job architecture](extension/jobs.md) |
| C++ compilation and the snapshot bridge | [Port mechanics](wasm/port.md), [build reference](wasm/build.md) |
| Measurements and validation limits | [Benchmarks](benchmarks.md), [evidence](evidence.md) |
| Data handling | [Data and privacy](policies/privacy.md) |
| Supported scope and licensing | [Scope](roadmap.md), [licensing and availability](publishing.md) |

## Components

Rosetta supplies the C++ scientific model, REF2015 energy evaluation, rotamer packing, minimization, FastRelax, and FastDesign. The WASM engine executes these compiled implementations.

The standalone adapter manages a dedicated worker, verifies engine and database identities, calls the compiled C ABI, and returns measured snapshots and final coordinates. It has no dependency on the extension's networking, storage, or UI.

RoTab adds the molecular viewer, energy history, shared-tab ownership, model checkpoints, and volunteer campaign coordination. Nostr provides discovery and signaling; WebRTC transfers jobs and results between browsers. The submitting browser coordinates each campaign.

## Browser execution

Calculations run in the browser. Participants do not need Docker, Node.js, Python, BOINC, a native companion, or a local task server. Standalone applications serve their JavaScript, WASM, and database assets over HTTP(S). Compilers and native reference tools are used separately for building and validation.

Independent Nostr relays support discovery. STUN and optional TURN infrastructure help browsers establish connections across networks. [Network architecture](extension/network.md) describes these services and their limits.

## Scientific scope

The eight supported methods accept a single chain of standard amino acids in PDB format. Input admission has no residue-count cap, but each worker has a 512 MiB linear-memory ceiling. Supported chemistry and database coverage depend on the method and its validated fixtures.

Relaxation optimizes an existing structure. Its snapshots describe optimization states, not a time-resolved molecular-dynamics folding experiment. [Rosetta relaxation reference](https://docs.rosettacommons.org/docs/latest/application_documentation/structure_prediction/relax).

RoTab does not implement official Rosetta@home workunit submission, project validation, or BOINC credit. The port is independent of endorsement by RosettaCommons, Rosetta@home, or BOINC. Rosetta's license is separate from the MIT application and adapter code.
