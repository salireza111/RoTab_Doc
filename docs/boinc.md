# BOINC, Rosetta@home and what was ported

Rosetta's scientific C++ methods have been ported to WebAssembly. The BOINC client has not been ported. BOINC provides the surrounding volunteer-computing platform: it allocates work, downloads application and data files, manages execution, reports results and supports project validation and credit. Rosetta is the scientific application launched by BOINC. [BOINC overview](https://github.com/BOINC/boinc/wiki/BOINC-overview), [native application API](https://github.com/BOINC/boinc/wiki/API-for-native-apps).

## BOINC reference environment

The arm64 macOS reference environment used for comparison contained BOINC 8.2.11, a Rosetta Beta 6.04 x86_64 scientific executable, its graphics executable and a 418,361,967-byte database ZIP. No downloaded Rosetta workunits or results were present, so the environment provided no assigned task for reproduction.

A reference experiment ran the installed scientific executable on the repository's 1L2Y fixture in isolated scratch storage with networking denied. The executable reported source `76e2f63f750b32d50338385a5e1d99ecb36da226`, which differs from the browser port's pinned source. Retained evidence includes inputs, outputs, hashes, sanitized logs and a common-scorer comparison. This experiment compares an official executable against WASM on a reference structure; it does not reproduce an assigned Rosetta@home workunit. See [benchmarks](benchmarks.md).

The capture utility, `scripts/capture-boinc-task.py`, preserves an already downloaded task's allowlisted metadata, files, mappings and hashes without controlling the BOINC client. It excludes account and authentication files and does not request new work or upload results. The browser importer can derive a supported coordinate benchmark from captured PDB data. That derived benchmark does not reproduce arbitrary original flags, constraints or application behavior.

On the project application page checked October 9, 2026, published families include Rosetta, Rosetta Beta, Rosetta Mini and VirtualBox-based Python projects. No browser/WASM platform is listed. The current listing is separate from locally retained older files. [Official application list](https://boinc.bakerlab.org/rosetta/apps.php).

## Native and browser execution paths

```text
Rosetta@home / BOINC                       RoTab browser campaign
------------------------------------      ----------------------------------
project work generator                    publisher's IndexedDB campaign
        ↓                                          ↓
BOINC scheduler and download servers      Nostr presence / encrypted signaling
        ↓                                          ↓
BOINC client + native app in slot          signed job via direct WebRTC
        ↓                                          ↓
native Rosetta C++ + full task files       packaged Rosetta C++ in WASM worker
        ↓                                          ↓
native output files / graphics memory     live PDB/REF2015 snapshots + output
        ↓                                          ↓
project upload, validation, credit        signed browser outbox → publisher
                                                  ↓
                                          stored receipt; science unverified
```

The arrows describe different protocols. A RoTab receipt means a matching output was stored once; it does not mean the Rosetta@home validator accepted it.

## Capability mapping

| BOINC / Rosetta behavior | Browser replacement or reuse | Current gap |
| --- | --- | --- |
| Rosetta Pose, chemical types, energy terms and movers | Compile upstream C++ libraries with Emscripten | Only reduced REF2015/canonical coordinate surface admitted |
| Native scientific executable | `rosetta.mjs` + `rosetta.wasm` | Native binaries cannot simply run as WASM |
| Scientific database files | Traced package preloaded into Emscripten `/database` | Resources not certified for all Rosetta protocols/chemistries |
| BOINC task slots and OS processes | Dedicated workers and Emscripten memory filesystem | No equivalent native process/VM/MPI execution |
| Work generator and scheduler | Publisher-owned campaign queue and fenced model leases | Custom RoTab schema, not BOINC scheduler XML |
| Workunit/application downloads | Packaged executable code; direct signed input data | No native-platform impersonation or general workunit downloader |
| Account, host and project identity | Local P-256 participant identity plus Nostr relay key | No BOINC account attachment, host ID or project authorization |
| CPU preference / suspend | Worker count, cooperative duty target, worker termination | No OS scheduler integration; startup is partly synchronous |
| Native checkpoint | Completed-model IndexedDB boundary plus seed replay | No exact mid-minimizer/annealer/Pose+RNG checkpoint |
| Shared-memory graphics | Instrumented snapshots of scientific states | Original native graphics ABI not reused in the browser |
| Result upload and retry | Signed durable outbox, direct receipt, idempotent storage | No official upload/report/assimilation path |
| Scientific validation and credit | Developer native rescoring; UI labels unverified peer results | No distributed validator, project acceptance or official credit |
| Always-on native daemon | Open-tab ownership and handover | Closing the last tab stops browser computation |

## What an official workunit contains

A BOINC job can reference **multiple input and output files** with logical names understood by the scientific application. Task metadata also identifies the application, arguments, deadlines and resource bounds. Per-application templates describe file mappings and output size limits. A ZIP is a container for some jobs, not a universal scientific workunit format. [BOINC job templates](https://github.com/BOINC/boinc/wiki/Job-templates), [job submission and control](https://github.com/BOINC/boinc/wiki/Job-submission-and-control).

The pinned Rosetta BOINC application includes archive extraction/file resolution and dispatches on `run:protocol`; work can involve sequence/fragments, structures, constraints, templates, ligands, symmetry definitions or scripts. It can emit silent structure records rather than just one PDB. The list of 19 source branches is documented in [experimental modules](wasm/experimental.md). A source branch's presence does not establish that Rosetta@home currently sends that workload. [Pinned `minirosetta.cc`](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/apps/public/boinc/minirosetta.cc).

Volunteer parallelism commonly distributes independent model attempts and sampling jobs. In RoTab, each attempt receives the complete supported input chain. Modeling a domain or segment requires a defined scientific protocol, boundary conditions and validation; cutting coordinates alone would not preserve interactions with omitted residues.

## Relationship to the native scientific application

The production coordinate harness calls upstream scientific classes directly. It does not call the BOINC scheduler, runtime supervisor, slot resolver or native shared-memory graphics. Separate research builds also link the upstream `minirosetta` scientific dispatcher and a smaller cyclic family, but those have their own unpassed browser/admission gates.

Official browser-client support would require project agreement on an application and platform identity, engine distribution rights, a reviewed input feed, exact protocol and file contracts, native/browser validation, safe result reporting and accepted project results. These contracts must also specify flags and database resources. The [scope reference](roadmap.md) describes related development areas. Agreement on one REF2015 score does not establish these operational requirements.
