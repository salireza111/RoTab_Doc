# Troubleshooting

## Network is red or a relay rejects the session

Open Volunteer settings → Connection settings → Relay settings and read the exact provider error. Authentication-required, restricted or rate-limited relays are not necessarily usable just because the WebSocket opens. RoTab retries/backoffs per relay and keeps healthy relays/direct links usable. Avoid repeated rapid reconnects. NIP-42 authentication is not implemented; choose a provider that permits this application's rendezvous traffic.

If peers are visible but cannot exchange work, open **Live devices**. "Waiting for reply" points to the setup exchange; "Reply received" with failed connection checks points to route establishment. Use **Retry connections** once and allow setup to finish. Update/reload RoTab on both devices so late ICE candidates can be exchanged. Working links and saved jobs/results are retained.

For peers on different networks, successful Nostr discovery does not guarantee a direct WebRTC route. The shared-TURN private pilot includes generated relay access; standard source builds require custom TURN configuration. When connection checks fail, TURN may provide a usable fallback. A slow check or an exchanged reply alone does not prove a firewall restriction. The [managed TURN setup guide](turn.md) explains how to obtain credentials, use **Test TURN**, save settings on both devices and verify a one-model exchange. More Nostr relays cannot replace TURN.

**Download connection diagnostics** produces a report without candidate IP addresses, raw SDP, participant keys, TURN credentials or scientific payloads. Version 2 includes the built runtime filename and up to four previous connection attempts per peer, so a retry need not erase the earlier failure evidence. Current and previous attempt states can differ. Download from both devices before reloading or changing network settings. Public reports must still exclude private data and any screenshots containing credentials.

## Shared TURN stops working

Run **Test TURN** on each device and check whether the configured URL belongs to the current provider tier. Provider quota, authentication expiry, and service availability can affect the shared relay. All shared-pilot users consume one account allowance; a visible Nostr peer can still lack a usable TURN route. See [monthly allowance and availability](turn.md#monthly-allowance-and-availability).

When access changes, apply the replacement URL, username and credential on each affected profile, test it and retry connections. An upgrade preserves previously applied TURN settings, so installing a new pilot alone may retain old access. Clearing the URL disables TURN and persists after reload; it does not restore the bundled default. Avoid clearing the browser's identity or campaign ledger to fix relay authentication.

## Uneven job distribution

Check actual **connected** status, automatic volunteer consent, compatible protocol/engine and whether other sessions are busy or cooling down. One browser profile counts once across its linked tabs. Each network browser accepts one model at a time. A small campaign has only its requested number of independent models, and scheduling is not guaranteed equal-share. The publisher participates only when its campaign's local-participation option is enabled and the session is available.

## A finished result has not returned

Keep/reopen the same publisher profile and its main RoTab. Retained signed outboxes retry over a working direct link. Check whether the publisher is offline, the link failed or the attempt became obsolete through reassignment/cancellation. A lease time passing alone does not discard an otherwise-current result. Clearing either browser's identity/ledger can prevent recovery; relays cannot reconstruct campaign/result data. Export records before deleting local data.

## Calculation starts, then memory access fails

Pause/stop first, reduce worker count and inspect the exact error. Heap allocation failures and stack/out-of-bounds failures are different issues; more browser cores do not fix either. There is no residue-count cap, but the WASM worker has a 512 MiB linear-memory maximum plus separate compiler/renderer/process overhead. Supported input chemistry/protocol coverage also matters.

The importer uses heap-backed arguments and iterative atom-tree handling. Large designs can still exceed available resources. A minimal authorized input, protocol/seed, browser version and sanitized exported provenance help reproduce a failure. [Memory details](../wasm/memory.md).

## Uploaded PDB contains water, ions or ligands

The protein-only importer removes those non-protein components and prunes their LINK/CONECT references. A visible preparation caution identifies the removed components. Review the removed-component details and retain the original PDB. The resulting calculation describes the protein alone, not the original complex.

A modified/nonstandard protein-residue error is different: such residues are retained for review rather than deleted or guessed. Supply a standard-amino-acid structure appropriate to the scientific question. Malformed identifiers, missing backbone coordinates or multiple protein chains also remain explicit errors. [Preparation policy and limitations](../wasm/io.md#explicit-preparation).

## Long startup or heat while running

Rosetta's first call initializes scientific state and prepares the input before the first measured snapshot. The extension creates a fresh worker per model, so this setup can repeat. Startup is not fully throttled. One worker/10% and the automatic network rest reduce sustained load but do not guarantee temperature/fan behavior. Saved budgets and protocols can differ across devices; cross-device thermal measurements remain pending.

Pause/stop the calculation to end active worker execution. **Pause new tasks** prevents the next assignment but lets the current one finish. An open extension alone is a different condition from active scientific work. Turning off automatic rotation affects rendering, not the scientific startup path.

## One or two snapshots, flat graph, or neutral color

Check the method first: Score keeps coordinates fixed and normally emits initial/final snapshots. Minimize/FastRelax can produce an optimization trajectory. Stable starting structures, fast protocols, long operations and the nominal snapshot throttle also affect callback count.

Coordinate storage is bounded to 240 frames and an estimated 8 MiB, so a large target may have fewer retained frames than graph energy samples. Residue-energy coloring requires scored per-residue data in the selected snapshot. A reference structure without that data can appear neutral. Missing intermediate frames cannot be recovered from a final PDB; a new calculation is required to record another trajectory.

## Weather, Calendar, suggestions or timer sound

Weather: use manual city entry after denied/failed location lookup, and confirm the provider is reachable. Calendar: local events need no account; Google events need a configured OAuth client and authorization. Search suggestions: enable their Appearance checkbox; submitted searches work separately. Timer sound: start via a user action and ensure the tab/browser permits audio; closing all tabs or muting can prevent the ding.

If settings cannot be changed from a linked tab, select **Go to main tab**. For support, follow the [sanitized reporting guide](../policies/support.md).
