# Volunteer network

The submitting browser is the campaign coordinator. It stores a target, discovers online volunteers, issues bounded model assignments and receives signed results. All scientific computation runs in the accepting browsers. Nostr relays carry discovery/signaling, while protein data and result envelopes travel through direct WebRTC data channels.

## Discovery infrastructure

The default room is `rotab-pilot-v3`, with `wss://relay.damus.io` and `wss://nos.lol` as the default relays. Discovery is enabled on a fresh installation; computation requires explicit volunteer consent. Connection settings support up to three secure relay URLs. These independent servers have their own availability and policies. The default discovery path does not use a publisher-operated test server.

RoTab uses signed NIP-01 events, with application-specific ephemeral presence kind `23370` and signal kind `23371`. Presence expires after 45 seconds. It binds a persistent local Nostr key to the existing P-256 participant identity and announces bounded availability, engine/protocol and queue-count metadata. Connection signals are encrypted with NIP-44 v2 for the intended peer. This is an application protocol, not a standard Nostr compute-market protocol. [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md), [NIP-44](https://github.com/nostr-protocol/nips/blob/master/44.md).

Room names are discovery topics, not access-control secrets. Relays can see public presence, keys, timing and connection metadata; they do not receive plaintext input proteins, result structures or research descriptions. A signed direct-browser catalog supplies campaign title, mandatory description, method and remaining counts after peers connect.

## Task lifecycle

```text
upload / prepare / describe / choose protocol and model seeds
        ↓ durable publisher storage
campaign ready → presence → authenticated direct peer → signed catalog
        ↓ volunteer consent or persistent automatic opt-in
fenced assignment (one model, seed, input and engine hashes)
        ↓
WASM computation → durable signed result outbox
        ↓ reconnect/retry as needed
publisher validates envelope + current lease → durable result → receipt
```

The coordinator gives each independent model an attempt identity and seed. Leases expire after 120 seconds and are renewed for active work. Expiry permits reassignment; a delayed renewal/result can still succeed while its original token remains current. Reassignment replaces that token, fencing the old output. Storage must commit before assignments/results/receipts become visible. Duplicate matching deliveries are acknowledged without adding another accepted result; conflicting, superseded or cancelled attempts are rejected. [Assignment state machine](jobs.md).

The current application wire version is **3**. All participants must update together; the former default room migrates to `rotab-pilot-v3`, while custom rooms and an explicit network-off choice are retained.

The publisher is an eligible worker when **Also calculate on this browser** is checked (the submission default). Local assignments use the same fenced queue, signed results and receipt path. At most one network model runs per browser at a time. A short initial dispatch window lets already-online volunteers establish direct links before a fast local worker drains a small campaign.

Active workers report bounded state, fraction, snapshot count, elapsed time and optional energy in authenticated lease renewals. Updates are throttled and bound to the current worker/attempt/token; older elapsed-time telemetry cannot replace newer telemetry. The UI differentiates a lease assignment from actual running progress and labels stale updates. These reports travel directly, including local loopback, never as public Nostr events. Progress is worker-reported and is not independent scientific verification.

Consent is local. A one-model request does not authorize automatic future work. **Start volunteering** explicitly opts into future assignments; **Pause new tasks** stops new acceptance while preserving the active run. A publisher cannot change a volunteer's worker count, intensity or automatic preference. Preference changes announce availability without tearing down existing connections.

## Participant and result identity

Every browser profile has its own durable signing identity. A public fingerprint identifies the sender; it is not an account verified against a person's legal identity. Multiple tabs in one profile share the computational session and identity, while separate profiles/devices can be separate participants.

Signed assignments/results bind campaign/job/attempt IDs, input hash, method, seed, source commit, engine/database hashes and output provenance. Local keys and connection credentials are excluded from experiment exports. Clearing storage can destroy identity and pending records. There is no distributed identity recovery or Sybil-resistant reputation mechanism yet.

## Transport and reachability

WebRTC uses ICE to find a route. STUN helps peers discover reachable addresses; TURN can relay encrypted traffic when direct connectivity fails. Neither service performs Rosetta calculations. The standard source build includes STUN configuration. The shared pilot additionally includes generated access to an independent TURN provider. Direct reachability across all NAT/firewall combinations is not guaranteed. [WebRTC peer connection documentation](https://webrtc.org/getting-started/peer-connections).

Manual signed `RT1.` offer/answer pairing remains available for advanced testing. It supports one peer connection and one to four independent models per direct job; the automatic campaign queue has a separate larger attempt budget. Re-pairing must preserve identity to retry old outbox results. Manual-pairing bounds should not be mistaken for automatic campaign limits.

Automatic setup exchanges candidates that arrive after the initial eight-second gathering window. Missed invitations/answers and late candidates retry without creating duplicate jobs. Connection checks, retry controls and redacted diagnostics are described in [Connection setup architecture](connections.md). These recovery mechanisms improve signaling reliability; they cannot supply a TURN route when no such service is configured.

Relay settings include a managed-service guide and **Test TURN** allocation preflight. The test uses the entered settings without applying them, closes its temporary connection and starts no calculation. A successful allocation is followed by saving settings and verifying a real peer/job exchange. [Cross-network setup](../help/turn.md).

## Network counters

Online counts reflect currently observed, compatible, unexpired participants in this room and reachable relays. Queue counts come from direct publisher catalogs. They are local observations, not globally complete network statistics. Relay partitions, blocked peers and offline publishers can hide work or users. There is no authoritative worldwide membership count.

## Failure boundaries

Completed local work survives reload through checkpoints/outboxes, and delivery retries on reconnection. An offline publisher cannot issue assignments or immediately receipt results. A lost publisher database is not reconstructed from relays: relays hold no campaign proteins/results. There is no replicated coordinator ownership, global consensus, blockchain, storage availability guarantee or automatic publisher takeover.

The recorded 0.5.1 Chrome/Brave tests used public Nostr signaling, three isolated profiles per browser and real WASM minimization. Eight returned models passed independent native rescoring. All profiles shared one computer; volunteer testing across different networks remains pending. Transport tests that use synthetic workers are listed separately from this scientific evidence in [benchmarks](../benchmarks.md).
