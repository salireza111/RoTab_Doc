# Connection setup architecture

RoTab has a rendezvous layer and a scientific-data layer. Nostr discovers compatible sessions and carries connection signals; WebRTC carries signed application messages after a peer session is established. The submitting browser remains the coordinator. There is no publisher-operated task API in this default path, but public relays and optional connectivity services are still servers.

## Establishing a session

```text
Browser A              Nostr relays                 Browser B
   │── signed presence ────┬──── signed presence ──────│
   │← compatible peer ─────┴──── compatible peer →────│
   │── encrypted offer ────────────────→──────────────│
   │←────────────── encrypted answer ─────────────────│
   │                 ICE / optional STUN or TURN      │
   └════════ authenticated WebRTC data channel ═══════┘
                     signed catalog / task / result
```

1. The owner loads a persistent P-256 participant signing identity and a separate local Nostr key. A signed binding ties the discovery key to the participant identity.
2. It subscribes to the selected room topic on up to three `wss://` relays. Fresh profiles use `rotab-pilot-v3`, `relay.damus.io` and `nos.lol`.
3. Public ephemeral presence kind `23370` advertises compatible engine/source/hashes, protocols, availability and bounded counts. Its application lifetime is 45 seconds. New public announcements are coalesced to at most one every ten seconds; direct updates can arrive sooner.
4. Compatible peers establish a signed offer/answer exchange. Signal kind `23371` carries a NIP-44 v2 encrypted payload for its intended recipient. Duplicate/older offers and repeated answers are handled idempotently.
5. Initial ICE gathering waits up to eight seconds. Candidates arriving later are sent as bounded encrypted connectivity updates (signaling payload version 2), tied to the current session. Updates arriving before their invitation/answer are held briefly; duplicates and obsolete sessions are discarded. Invitation payload version 1 and presence wire version 3 remain unchanged. Both devices need a build that supports late-candidate exchange.
6. ICE finds a network route. The resulting data channel verifies signed application messages and the expected participant before accepting a catalog, assignment, renewal, result or receipt.

RoTab's event kinds and payloads are application-specific. [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md) supplies the event/relay foundation; [NIP-44](https://github.com/nostr-protocol/nips/blob/master/44.md) specifies encrypted content. Neither defines RoTab's compute scheduler.

## Retry and diagnosis

Relay acceptance does not guarantee delivery to an online recipient. While a connection remains incomplete, the initiator repeats its signed invitation in a fresh encrypted Nostr event at the next maintenance tick after twelve seconds. A repeated invitation can trigger retransmission of the cached answer without creating another session or duplicating an assignment. Late candidate batches also retry. A fresh connection attempt replaces an unsuccessful session after sixty seconds; older answers cannot bind to the replacement.

**Live devices** distinguishes route gathering, waiting for a reply and connection checks. A visible peer is an observed presence, not proof of a usable transfer channel. **Retry connections** requests a new setup for disconnected peers and preserves working links, campaigns and saved results. The lower participant ID remains the initiator; an encrypted reconnect request handles retries initiated from the other device.

Pending checks remain a setup state rather than a confirmed failure. An actual ICE/transport failure can report whether STUN supplied an external candidate or TURN supplied a relay candidate; these observations do not independently prove a NAT/firewall cause. **Download connection diagnostics** exports current connection/gathering/ICE/transport state, candidate types, numeric ICE-server errors and public relay origins/status. Version 2 adds a built runtime filename and up to four previous attempts per observed peer, including replacement reason and the last confirmed failure state. This in-memory history clears on network reconfiguration, peer expiration or reload. Reports exclude candidate addresses, raw SDP, keys, participant identities, TURN credentials and protein/job data. Experiment-record export is a separate feature and can contain scientific data.

## Data visibility

| Recipient | Visible data |
| --- | --- |
| Nostr relay | Public keys, room topic, presence/capabilities/counts, timestamps, recipient tags and encrypted signaling bytes; network connection metadata |
| STUN provider | Network address/connectivity queries used to discover a route |
| TURN provider, when configured | Authenticated connection metadata and relayed encrypted WebRTC traffic |
| Connected participant | Signed catalog including title/description, protocol and counts; assignments/results it sends or receives |
| Campaign publisher | Assigned worker identities, bounded progress/energy, result/provenance and receipt state |

The room is a discovery topic, not a private password or participant allowlist. Public presence is not anonymous, and a signature does not establish a real person's identity. No plaintext PDB, result coordinates or research description is intentionally published to Nostr relays.

## Connection settings

| Option | Purpose | Operational limit |
| --- | --- | --- |
| Network on/off | Join or leave automatic rendezvous | Discovery on does not consent to computation |
| Room | Select the discovery topic | Devices need compatible room and wire version |
| Continue automatically | Consent to later network assignments | CPU/intensity remain locally controlled |
| Relays | Up to three secure WebSocket rendezvous endpoints | A TCP/WebSocket connection alone does not prove writes/subscriptions are accepted |
| STUN | Candidate/address discovery; default `stun:stun.l.google.com:19302` | Does not relay scientific traffic or guarantee a direct route |
| TURN URL, username, credential | Fallback connectivity through bundled pilot access or a custom service | Shared pilot access is installed automatically where TURN is absent; custom credentials remain local |

Use **Connection settings → Relay settings** only when needed. A functioning relay and a connected scientific peer are different states. [WebRTC's connection guide](https://webrtc.org/getting-started/peer-connections) explains ICE and connectivity services.

**Test TURN** gathers candidates through a temporary relay-only WebRTC connection and closes it after success, failure, cancellation or twenty seconds. It uses the settings currently entered in the form, without applying them to active links. A relay candidate proves allocation only, not end-to-end job delivery. **Need a TURN service?** provides a managed setup option without installing a server. [Setup and verification](../help/turn.md).

## Shared relay access and campaign authority

The shared-TURN 0.5.2 pilot supplies generated relay authentication once to profiles without configured TURN, while retaining custom settings and previous opt-outs. It uses `turns:standard.relay.metered.ca:443?transport=tcp`; the standard source build supplies no shared credentials. Participants do not need separate provider accounts. Access is extractable from the private distributable, and relayed traffic from all recipients consumes the operator account's allowance. Previously applied credentials are not automatically replaced on an upgrade.

Relay authentication is independent of campaign authority. Any compatible connected participant can publish a campaign and volunteer; the TURN account owner has no special sender role. Each publishing browser coordinates its own durable queue and must remain available for assignment and result receipts. There is no approved-sender allowlist, and a room topic does not restrict access.

The current provider allowance, monthly renewal, availability limits and service-change instructions are documented in the [TURN usage guide](../help/turn.md#monthly-allowance-and-availability). TURN carries encrypted transfers and does not execute scientific workers or replace Nostr signaling. Provider quota failure can leave discovery working while fallback data channels cannot connect.

## Failure isolation and queue responsiveness

ICE gathering and connection setup run outside the durable ledger's serialized operations. A pending offer for one peer must not block another peer's renewal, assignment or result. Per-link sends preserve order, but backpressure on one channel does not stall the global scheduler. Repeated in-flight commands are bounded/deduplicated.

The Nostr transport retains a bounded, short-lived outbox: at most 65 pending items, with newer presence replacing older presence. Unacknowledged sends retry after eight seconds while their 45-second lifetime remains valid. Rate-limited writes back off for 15 seconds; other rejections back off for 60 seconds. Relay-specific errors remain visible without converting every healthy relay/direct peer into a global failure. Closed subscriptions reconnect; authentication-required relays are reported rather than silently treated as usable. NIP-42 authentication is not implemented.

Existing direct sessions can remain usable during relay rejection. If no ICE route works, adding relays alone does not solve it: configure a suitable TURN service or test another network. Scientific payloads do not fall back to a public Nostr event.

## Manual pairing and evidence

Advanced **Direct pairing / Peer collaboration** exchanges signed `RT1.` invitation/reply codes manually. It is a separate one-peer workflow with one to four independent models per job. Both peers should verify fingerprints and retain identity when retrying old results. It uses the same pinned science rather than requiring a native helper.

Recorded transport checks exercised delayed candidates, missing setup signals, rejecting relay fixtures, offline completion, and publisher reload. Separate scientific campaigns used public relays and real WASM. All recorded multi-profile acceptance ran on one computer; different-network reachability and comparative thermal behavior remain outside those results. [Validation summaries](../evidence.md), [benchmarks](../benchmarks.md).
