# Benchmarks and interpretation

The benchmark record separates scientific correctness of the pinned port, comparison with an installed official application, and reproduction of assigned Rosetta@home workunits. Recorded results are available for the first two categories. Official workunit reproduction remains pending.

## 1. Same-source scientific correctness

The native harness and WASM harness use pinned source `369e400415dd5c585f80dcf7b647147ee520e8ba`. Fixed-coordinate scores must agree within:

```text
absolute difference ≤ max(0.001 REU, 0.00001 × |native score|)
```

For optimization/design, the returned WASM coordinates are independently rescored natively under the same reporting function. Native and WASM trajectories need not be identical. Differences in their final chosen models are not a substitute for rescoring the **same returned coordinates**.

| Recorded 1L2Y measurement | Value |
| --- | ---: |
| Native fixed-coordinate REF2015 | 32.33483681374909 REU |
| WASM fixed-coordinate REF2015 | 32.33483681375084 REU |
| Absolute fixed-score discrepancy | approximately 1.75 × 10⁻¹² REU |
| WASM FastRelax returned-coordinate energy | −48.17565422427388 REU |
| Native rescore of that returned structure | −48.17565422424631 REU |
| Absolute returned-score discrepancy | approximately 2.76 × 10⁻¹¹ REU |
| Eight-protocol measured peak allocated heap | 278,396,928 bytes |
| Scientific JS/WASM/database package | 146,090,371 bytes |

Recorded checks cover all eight engine methods against native Rosetta and standard Chrome and Brave virtual machines. Most fixtures use 20-residue 1L2Y, seed 17; FastDesign checks for the engine with large-input memory adaptations use its first eight residues in Node and browsers. The historical engine's full 20-residue FastDesign run took approximately 27 minutes and has separate recorded hashes in the evidence inventory. A separate 76-residue 1UBQ browser scoring check and the private [865-residue memory regression](wasm/memory.md) test larger inputs. These fixtures do not establish general input coverage, size scalability or reliable runtimes for new proteins.

## 2. Standalone SDK acceptance

The SDK acceptance script loads no extension in installed Chrome and Brave. Each browser performs real **score, minimize and relax** on 1L2Y, seed 17, at a 75% duty target. All six outputs require independent rescoring and input/output provenance checks, together with real snapshots, sequential warm worker reuse, mismatched-manifest rejection and wrong-asset-hash rejection. Every external request is blocked. A temporary loopback listener streams the single WASM asset for this developer test and closes afterward; no task server, container or participant helper is involved.

Standalone scientific browser coverage includes score, minimize and relax. Dispatch and contract checks cover all eight methods, with separate scientific evidence from the matching engine's eight-protocol tests. These records do not constitute an all-eight-method standalone browser benchmark. Exact SDK hashes, output records and measured values are in [the evidence inventory](evidence.md).

The SDK adds asset hashing and uses a verified-byte instantiation hook. Its cold timing is not directly comparable to the extension's different worker host, and the two browsers were exercised concurrently during acceptance. Those timings are observations, not a controlled Chrome-versus-Brave performance ranking.

## 3. Installed official Beta versus browser reference

The installed Rosetta Beta 6.04 executable and browser WASM ran one-repeat FastRelax on the repository's same first 1L2Y model, seed 17. Returned structures were scored with one common pinned REF2015 reference.

| Measurement | Result |
| --- | ---: |
| Initial common score | 32.334836814 REU |
| Official executable's returned coordinates, common score | −48.202634589 REU |
| Browser returned coordinates, common score | −48.175654224 REU |
| Browser minus official common score | +0.026980364 REU |
| Aligned C-alpha RMSD | 0.007551132 Å over 20 residues |

The structures are close for this fixture. The official binary self-reports source `76e2f63f750b32d50338385a5e1d99ecb36da226`, while WASM uses a different source/database baseline. Binary/source correspondence and native database parity were not independently attested. The native run used an x86_64 binary on arm64 macOS. It was network-denied and isolated from BOINC credentials and live task slots.

Native score-file and pose-table energies precede PDB rounding and differ from common returned-coordinate rescoring. The native process wall time was 14.818 s including startup and shutdown, and its BOINC CPU summary conflicted with wall time. These records do not support a valid native/browser speed ratio.

## 4. Parallelism, recovery and volunteer delivery

Historical extension 0.2.0 multicore checks defaulted to four workers on eight reported processors. Ten tabs retained one computation owner. Pause/resume and active-owner handover preserved completed outputs, IDs and seeds; unfinished models replayed. Two-worker FastRelax batches at 75% duty took 118.518 s in Chrome and 105.287 s in Brave. These are operation observations, not randomized equal-resource speedup trials. Seeds 17 and 18 produced identical final coordinates on that fixture.

Recorded aggregate allocated heap peaked at 695,992,320 bytes with three fully initialized models active after handover; that is not a measured four-model full-initialization peak. Browser/compiler/viewer/process memory is additional.

The 0.5.2 acceptance run verified the current one-worker default, staged initialization, pause/resume and ten-tab ownership transfer in Chrome and Brave. Each browser produced four minimization outputs and two FastRelax outputs; every returned structure passed native rescoring. Tests explicitly requested four workers and observed a maximum of two simultaneously active workers under staged startup. Maximum measured allocated WASM heap was 231,997,440 bytes per worker and 366,215,168 bytes in aggregate in each browser. Worker memory was released on pause and completion, and saved coordinate frames restored and replayed. These heap figures exclude browser/viewer/process memory. The runs overlapped other acceptance workloads and are not controlled performance comparisons. [Build-specific multicore report](assets/evidence/multicore-browser-proof.json).

Extension 0.5.1's direct-peer checks produced four real WASM score/minimize outputs across Chrome and Brave. Its Nostr tests used a public relay, three isolated profiles per browser, two volunteers and four minimization outputs per browser. All eight network outputs passed independent native rescoring; maximum discrepancy was approximately 1.77 × 10⁻¹¹ REU. Publisher profiles ran no scientific worker. All profiles shared one machine, so reachability between volunteers on different networks remains untested.

The shared-TURN 0.5.2 pilot completed a scientific campaign check through the supplied Metered Free-tier `standard.relay.metered.ca` relay. Chrome and Brave each used three isolated profiles and a real public Nostr relay; two volunteers returned four packaged-WASM minimization models per browser family. Relay-only policy was forced in the test harness, and selected candidates at both endpoints were TURN relays over TLS. All eight outputs passed independent native rescoring (maximum absolute discrepancy 1.77e-11 REU). The test used no manual TURN credential entry. All profiles still shared one computer; different-network field testing remains required. [Scientific relay campaign report](assets/evidence/nostr-network-browser-proof.json).

UI/transport tests also use synthetic worker fixtures to exercise failures and scheduling quickly. Those establish behavior, not scientific execution, and are not counted as Rosetta models in the scientific evidence.

The October 11 volunteer UX check separately returned four actual packaged WASM **Score** jobs in each installed browser family, distributed among the publisher and two volunteers (eight returned jobs total). It used an in-process Nostr transport fixture with actual signatures, NIP-44 and local WebRTC. No native scorer or listening service ran for this check. The [report](assets/evidence/volunteer-ux-browser-proof.json) binds the tested runtime; this confirms execution and delivery, not new native equivalence or different-network reachability. Interface-only checks are separate from scientific acceptance.

## 5. October 11 recovery and low-intensity observations

The [reliability report](assets/evidence/network-reliability-2026-10-11.json) records six isolated profiles in each installed Chrome/Brave test, actual signatures/NIP-44/WebRTC, a rejecting relay fixture, five retained remote outboxes while the publisher was offline, publisher participation, and six received models after recovery. Scientific workers were deterministic fixtures. This tests transport/scheduling and durable return, not real scientific equivalence, cross-NAT routing or public-relay write acceptance.

The same report contains a **failed/unfinished** 10%-intensity actual-WASM recording probe: only an initial Score frame was captured before its timeout. The report's top-level `passed` flag refers to the combined reliability work and must not be interpreted as a successful nested recording/thermal measurement. Existing successful scientific SDK/protocol reports remain separate and identify their own inputs, budgets and hashes. The recovery report applies to its recorded runtime hash.

Comparative temperature, fan-speed, battery and wattage measurements across users' Macs are not available. Startup can recur per extension model and begins before the cooperative budget timer; a low target can also lengthen waits. Further resource measurements need to distinguish cold and warm startup, active work and sleeping time.

## 6. Official task replay remains pending

The saved October 8 local inventory contained no Rosetta workunits/results. Historical project-status observations recorded an empty queue at their stated timestamps; they are not a live availability guarantee. No approved browser task feed, scheduler allocation, official result upload or credit has been demonstrated.

A complete workunit comparison requires the original application/version, exact input files and logical mappings, flags, restraints, seed, budgets, and output contract. A PDB extracted from a task can support a separate coordinate experiment without reproducing the original job.

## Measurement design

Controlled performance measurements require a fixed dataset, multiple seeds and input sizes, and repeated paired trials. Download, compilation, first-call scientific setup, warm execution, rendering, and result transfer have separate timing scopes. Worker comparisons also require equal model counts, seeds, and resource policies.

The current records provide fixture-specific observations. They do not establish a general native/browser speed ratio, equal-resource speedup, or a thermal guarantee.
