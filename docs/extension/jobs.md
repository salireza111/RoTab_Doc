# Job assignment and result architecture

## Campaign, model, assignment and result

| Object | Meaning | Durable owner |
| --- | --- | --- |
| Target | Prepared PDB plus input/preparation hashes and provenance | Publisher, then assigned workers |
| Campaign | Title, required description (up to 240 characters), protocol, model count and base seed | Publisher `campaign-ledger` |
| Model attempt | One independent model index and its seed | Publisher |
| Lease | Current worker, signed job, unique token and expiry | Publisher; signed assignment retained by worker |
| Progress | Worker-reported state, fraction, elapsed time, snapshots and optional energy | Publisher's current lease |
| Result outbox entry | Signed completed coordinates and provenance awaiting receipt | Worker `network-ledger` |
| Outcome/receipt | Publisher's durable matching result and delivery acknowledgment | Publisher; receipt retained by worker |

One submitted protein can request 1 to 1,000 independent models with distinct sequential seeds. Each attempt receives the complete supported input chain. Independent models may converge to similar structures, and the number requested does not guarantee that many volunteers are available.

## Submission and admission

The submitting browser prepares the file locally, requires a short research description and chooses a fixed protocol. The coordinator saves the campaign before advertising it through signed direct catalogs. Public presence exposes counts/capabilities rather than the full protein or description. **Also calculate on this browser** defaults checked, so the sender can be a worker as well as coordinator.

A received assignment is untrusted input despite its signature. Admission verifies publisher/recipient identity, schema, prepared input hash, current engine/source/database hashes, method, seed and protocol budget. Peers cannot supply arbitrary scripts, command-line flags, plugins, a replacement WASM URL or a volunteer's CPU preferences.

## Scheduling algorithm

`VolunteerNetwork.schedule()` collects compatible connected participants and the eligible local participant. `CampaignQueue.assign()` serializes the durable decision:

1. Build the set of workers with unexpired leases across campaigns.
2. Skip duplicate, stale (30-second scheduler presence), unavailable, occupied or non-consenting workers.
3. Scan active campaigns in stored order. Require matching scientific identity/protocol, a description and local participation permission for the publisher.
4. Find an unfinished model whose lease is absent or expired. Create a new signed job identity and random lease token for that model's seed.
5. Commit the ledger, then send the assignment. Each eligible browser gets at most one network model at a time.

A newly submitted campaign can wait about five seconds for already-observed automatic volunteers to finish their direct handshake before a fast local scorer consumes its small queue. This is not equal-share or hardware-weighted scheduling. A small four-model campaign cannot simultaneously occupy six devices; connection readiness, local work and saved consent also affect distribution. Fairness across many publishers and malicious identity resistance remain future work.

## Worker lifecycle and live feedback

```text
publisher commits lease → worker verifies + retains assignment
        → acceptance renewal / "loading" acknowledgment
        → Session checkpoint → Rosetta worker → real snapshots
        → authenticated progress renewals
        → completed model committed → signed result outbox
        → publisher validates and commits outcome → signed receipt
```

The 120-second lease is renewed during accepted/running work. Acceptance acknowledgment stops repeated full-PDB assignment sends. Progress is throttled, tied to the worker/attempt/token and checked for nondecreasing elapsed time. The sender can distinguish assigned/loading/running, latest energy/snapshot count, stale updates and completed work. A heartbeat or reported energy is not independent proof that a scientific result is valid.

After completion, automatic network work rests for 30 seconds before the next assignment. **Pause new tasks** revokes acceptance of later work while allowing a current model to finish; pausing/stopping the calculation itself terminates its worker and uses model-boundary recovery.

## Expiry, reassignment and delayed results

Expiry makes a model eligible for reassignment. It does not by itself erase the current token. A delayed renewal or valid result can still succeed if the same worker/token remains authoritative and the campaign has not been cancelled or the lease released. This matters when the publisher was offline while a volunteer finished.

Reassignment creates a new job/token. The previous worker's output becomes **obsolete**, even if its signature and coordinates are well formed. It cannot overwrite the new attempt. Duplicate delivery of the same recorded output receives the same acknowledgment; a conflicting output for that already-recorded assignment is rejected. Cancelled campaigns reject late completion.

Explicit campaign removal deletes its input, attempts and saved campaign outcomes in one durable ledger update, including withdrawal of active leases. The UI confirms this deletion first. It does not remotely interrupt an already-running worker or erase a separate browser run record. A delayed authenticated result for an absent campaign receives an **obsolete** receipt, allowing its outbox to settle without restoring deleted campaign data. Up to 128 recent former worker IDs are retained as connection hints so a reloaded publisher can initiate that return handshake; no deleted coordinates/results are kept in those hints. Default queue removal still requires a finished/cancelled campaign; the explicit controller action authorizes active removal.

The worker commits its signed outbox before sending and retries after reconnection until it sees a matching receipt. The publisher commits the outcome before acknowledging it. These commit-before-send rules and token fencing support idempotent delivery despite reloads and duplicates; they do not make the browser network a globally transactional database.

## Result receipt and scientific validation

The publisher checks the signed envelope, current token, input/method/seed/engine provenance and returned structure contract. Its saved outcome is explicitly marked `scientificValidation: "not-verified"`. A **received** receipt confirms durable matching delivery, not independent energy rescoring, malicious-worker detection or official Rosetta@home credit.

Native/WASM comparison reports provide scientific evidence for their recorded fixtures. They are separate from live result admission. No native scorer is installed on volunteers' computers. Replicated coordinator storage, consensus, redundant-result scientific validation, project-approved credit and automatic publisher takeover are not implemented.

## Recovery and inspection

Keep the publisher's RoTab available to issue work and receive results. If it closes, volunteers can retain completed outboxes; new assignments and receipts wait for the same publisher identity/database to return. Clearing the publisher's data loses its authoritative campaign ledger. Export campaign records and completed structures for a separate backup; relays cannot reconstruct them.

Relevant sources: `campaign-queue.ts` (durable ledger/fencing), `volunteer-network.ts` (discovery/dispatch/retries), `peer-protocol.ts` (signed message and input/result contracts), and `session.ts` (scientific execution). See [connection architecture](connections.md) and [user troubleshooting](../help/troubleshooting.md).
