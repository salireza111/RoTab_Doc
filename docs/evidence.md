# Validation evidence

The public summaries retain measured values, result flags, and scientific artifact hashes from selected validation records. Free-form logs, commands, participant identifiers, authentication material, raw structures, and private paths are excluded. Each summary records the SHA-256 of its original source record; the table below identifies the public summary's own bytes.

Validation applies to the stated fixtures and exact builds. Compilation, transport delivery, scientific agreement, and official project acceptance are separate results. A report can contain failed or unfinished subchecks even when its overall status is passing; the scope notes identify those cases.

| Record | Recorded status | Public summary SHA-256 |
| --- | --- | --- |
| [Historical coordinate engine / full 20-residue FastDesign](assets/evidence/historical--coordinate-engine-before-large-input.json) | Passed within recorded scope | `8b1628eedfbe6e7b461f10c0fb43af8c23a8de968e794d322d49725fc0df43da` |
| [Eight coordinate protocols / native and Node WASM](assets/evidence/wasm-protocol-proof.json) | Passed within recorded scope | `9d4f44e5b8e3911787cdad2330ff55ee00d79603b7c57a1ce7d80abfdb534b9f` |
| [Eight coordinate protocols / Chrome](assets/evidence/browser-protocols-chrome.json) | Passed within recorded scope | `fac482ec15a0235dd0087ebb5b65286a5d839a9c243487c56173a7f12367f109` |
| [Eight coordinate protocols / Brave](assets/evidence/browser-protocols-brave.json) | Passed within recorded scope | `969fbed28e8639e4efe7e6bf66c3059dbc2012730ea539327216489c4555f40c` |
| [Protocol capability audit](assets/evidence/protocol-capabilities.json) | Comparison record | `712a941b304d1987f1b75e805673ffb8ae39827daf7760d2cb6d185aee4fa6e8` |
| [Standalone SDK scientific browser checks](assets/evidence/wasm-sdk-browser-proof.json) | Passed within recorded scope | `2c47ba508d568d8ef2a12b203d5693cc8c6ce7c422f8efd4afeaf2caf3dd25ed` |
| [Official executable versus WASM reference](assets/evidence/benchmarks--official-beta-vs-wasm-2026-10-08--comparison.json) | Comparison record | `b84a2420eee98ccfc3462d18282035b76f89d892b35b7ad40027f1daf8c7ede4` |
| [Cyclic family / Node and native topology fixture](assets/evidence/wasm-cyclic-family-proof.json) | Passed within recorded scope | `f6243ece7c237856a4addec4729649b76c8b166a10d771454c950ec561b93b60` |
| [Unresolved native cyclic control discrepancy](assets/evidence/native-cyclic-rescore.json) | Failed / unresolved | `3f8cb857d6bde48128e8f9512966894297f733eff8cfeb781924d51b90263111` |
| [Multicore recovery, scientific snapshots and worker release](assets/evidence/multicore-browser-proof.json) | Passed within recorded scope | `218f9d185d56fd45da0a4b6985218c8e8a2858ffac5bf5d3806022162a983d11` |
| [Direct peer calculation and delivery](assets/evidence/peer-pilot-browser-proof.json) | Passed within recorded scope | `01d36fc63bb675d7b96f3958b2b0c03668c3bc2ba64ceb1530f25522906faf0a` |
| [Nostr-discovered scientific delivery](assets/evidence/nostr-network-browser-proof.json) | Passed within recorded scope | `7b7a2b64df374209f158e77e1b32e3c8906991c4d2f2a2ac13aecfcd861add12` |
| [Extension 0.5.1 release checks](assets/evidence/nostr-release-checks.json) | Passed within recorded scope | `f241c657040a3560e23b394da1e1e37638dd5f69eb04a15587889fef38c2a3c7` |
| [Publisher participation and WASM Score delivery](assets/evidence/volunteer-ux-browser-proof.json) | Passed within recorded scope | `430e7b426933d39db90beaeccb711f7516ce61fdbd59173ce4178590f4cb2bc0` |
| [Interface and transport checks](assets/evidence/volunteer-ux-ui-browser-proof.json) | Passed within recorded scope | `8d7576bd951448e1e1320e8264a208be025d5846f2575968157e7334a05e0108` |
| [October 11 network recovery / mixed-scope recording probe](assets/evidence/network-reliability-2026-10-11.json) | Passed within recorded scope | `8cb58a968de4fe586a9bd0d22bc45ef510cea1aff5c09bbe61b0e5e5d42dec67` |
| [October 12 late ICE / missed signaling recovery](assets/evidence/network-connectivity-2026-10-12.json) | Passed within recorded scope | `817a0d200571ec07dc7d8c0ebc427ab73eda0d69c380ab5b10b172a950a925af` |
| [October 12 TURN setup UI, connection states and attempt history](assets/evidence/turn-setup-2026-10-12.json) | Passed within recorded scope | `75ca714d40d36c4ce8ae983ccdb6ce5591e85aff129d817951c5a7115623dcbc` |
| [October 12 live managed TURN allocation and relay-only round trip](assets/evidence/turn-live-2026-10-12.json) | Passed within recorded scope | `3772818970458fa76264debfd63ab27b90e49b30b8c894a316792eaa401fca85` |
| [Shared-TURN 0.5.2 pilot defaults, upgrade and encrypted relay checks](assets/evidence/shared-turn-pilot-2026-10-12.json) | Passed within recorded scope | `1baa0e4fcc5a7f3109dbabc2bf56d97e1f0caf3066712b01807d5ac8ac0c0b55` |
| [Protein-only PDB preparation, visible caution and native-rescored WASM Score](assets/evidence/protein-cleanup-browser-proof.json) | Passed within recorded scope | `cdec0b0d724575185bec664742afde19df5953811306a3f3bd00f7cd7bc57426` |
| [Personal widgets and documentation links](assets/evidence/personal-widgets-browser-proof.json) | Passed within recorded scope | `d1bda6087380279158995039e6046393627ba46111e626379541372940f4ee01` |

## Standalone SDK measurements

The standalone checks used 1L2Y with score, minimize, and relax. Both browsers ran concurrently; these wall times are observations, not a browser speed ranking. The first score includes lazy Rosetta initialization; later calls reuse that worker. No extension was loaded.

| Browser | Method | Energy (REU) | Native discrepancy (REU) | Real snapshots | Factory/assets (s) | Scientific call (s) | Heap (MiB) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| chrome 153.0.8010.54 | score | 32.334836814 | 1.748e-12 | 2 | 2.430 | 117.401 | 221.25 |
| chrome 153.0.8010.54 | minimize | -15.259485314 | 1.766e-11 | 8 | 0.000 | 2.038 | 221.25 |
| chrome 153.0.8010.54 | relax | -48.175654224 | 2.757e-11 | 48 | 0.000 | 16.138 | 221.25 |
| brave 155.0.8059.40 | score | 32.334836814 | 1.748e-12 | 2 | 2.542 | 119.955 | 221.25 |
| brave 155.0.8059.40 | minimize | -15.259485314 | 1.766e-11 | 8 | 0.000 | 2.030 | 221.25 |
| brave 155.0.8059.40 | relax | -48.175654224 | 2.757e-11 | 47 | 0.000 | 15.561 | 221.25 |

### Standalone result summaries

These summaries contain measured results and provenance hashes. Raw structures and complete frame records are retained separately and are not included in the public website.

- [chrome / score](assets/evidence/chrome-score.json) · Public summary SHA-256 `c9aeb8b089cc1d0f274a5c150c8d3fb0fa0c3613b9d7e03c920bb3983f19f399`.
- [chrome / minimize](assets/evidence/chrome-minimize.json) · Public summary SHA-256 `3275a2e9deb29be60f0449b2350298316e70f0dbee25d8a0905dc62e9f0646b5`.
- [chrome / relax](assets/evidence/chrome-relax.json) · Public summary SHA-256 `01a66a5ffce8810eca47984e33bb1d9d7b71c672bfbccc3ef54560c5769cbf33`.
- [brave / score](assets/evidence/brave-score.json) · Public summary SHA-256 `618e987360a34af998c10a01005d323611eebb1a3dfc4bb445e3d5d961519fd7`.
- [brave / minimize](assets/evidence/brave-minimize.json) · Public summary SHA-256 `f581de519d80546b303ee06a4811cdbed8325e3e934aab2a5e0ae9fd8306acb9`.
- [brave / relax](assets/evidence/brave-relax.json) · Public summary SHA-256 `94d68d8acd2fa540a8194ab4e1c70faaa55cea483a9be3ac21dc6a708f1442ea`.

## Scientific build identity

The bounded engine uses source `369e400415dd5c585f80dcf7b647147ee520e8ba` and engine ID `rosetta-protocols-v2`. Its measured scientific files are:

| File | SHA-256 |
| --- | --- |
| `rosetta.mjs` | `b5c9ebbb4c30cd54e1eb62ad08f32b2ef54179ccdd29d3ce077365f3cad5f65c` |
| `rosetta.wasm` | `81b86e799406616dde525a7598342f279a6e7fef0b9153eef4f40c8ca5c237c7` |
| `rosetta.data` | `c3ede09e4c3f652f36d0661e12007fcf1d87cde8ecf9e47f0a02aba1873c9d8a` |

The standalone proof additionally records every SDK JavaScript/chunk hash, while extension reports bind their own runtime/worker hashes. These hosts have separate identities even when they use the same scientific payload.

## Scope boundaries

- Eight-method engine coverage is principally 1L2Y/seed 17; browser FastDesign uses eight residues. Standalone SDK scientific checks cover score, minimize, and relax.
- Native/Node FastDesign checks for the engine with large-input memory adaptations use eight residues. The older 20-residue FastDesign run has a different engine hash and provides historical evidence for that build alone.
- The official-executable comparison is a reference fixture, not an assigned Rosetta@home workunit, and uses different source/database identities.
- Public-relay network acceptance used isolated profiles on one computer; volunteer reachability across different networks remains pending.
- The failed native cyclic control is intentionally retained. It is separate from returned WASM cyclic records that passed rescoring.
- Synthetic scientific-worker fixtures test UI/transport behavior, never scientific equivalence.
- The TURN setup report validates deterministic allocation UI/cleanup in Chrome/Brave and six-profile Chrome transport recovery. No actual provider account or cross-network TURN connection was tested.
- The later live TURN report validates supplied managed-service credentials and a TLS relay-only message round trip in Chrome/Brave on one computer. It does not validate different physical networks, a complete campaign exchange over that service or scientific execution. Credentials, addresses and raw SDP are omitted.
- The 0.5.3 protein-cleanup check validates upload cautions, exact original retention and actual WASM Score/native rescoring of a 20-residue fixture augmented with water, zinc, a ligand and connectivity records in Chrome/Brave. It does not certify arbitrary uploaded chemistry or repeat the full peer/multicore release matrix. The scientific worker and engine are unchanged.
- A result signature/receipt is provenance/delivery evidence, not an independently validated contribution or official BOINC credit.
- The October 11 reliability report contains passing six-profile transport recovery and an unfinished/failed 10% scientific recording probe. The top-level passing status does not establish success of that nested probe. Later default-rotation UI builds have a different frontend hash.
