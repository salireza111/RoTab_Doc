# Data and privacy

This reference describes the data handled by RoTab 0.5.6. It explains browser storage, network recipients, optional services, and deletion behavior. It is a technical description, not an operator-specific legal privacy notice.

## Data handling

| Information | Purpose | Storage and recipients |
| --- | --- | --- |
| Appearance, preferred layout, favorites, widget order, timer, and local events | Personalize the new-tab page | Browser-profile storage |
| Optional most-visited site list | Populate frequent-site shortcuts | Read through the browser's optional `topSites` permission and displayed locally |
| Search text | Submit a Google search | Sent to Google on submission; optional suggestions also send partial queries while typing |
| City or device coordinates | Obtain weather and a location label | Stored locally; forecast/geocoding requests go to Open-Meteo and approximate device coordinates to Photon/Komoot |
| Imported structures, prepared inputs, protocol, seeds, coordinates, and energies | Local calculations and submitted campaigns | Local IndexedDB; submitted or accepted network work transfers relevant scientific data to participant browsers |
| Public participant identity, capability, availability, and bounded counts | Discover compatible volunteers | Public Nostr presence and connected peers |
| Encrypted signaling and ICE metadata | Establish WebRTC connections | Selected relays, peers, and STUN/TURN services |
| Signing identities and connection authentication | Authenticate sessions and relay access | Browser-profile storage; shared pilot relay access is included in its extension build |
| Optional Google Calendar events and access token | Display and edit the selected calendar | Google Calendar API; the token is retained in browser-session storage |
| To-do tasks, doodle strokes, and board notes | Personal Simple-view tools | Local IndexedDB, shared only with RoTab tabs in the same browser profile |
| Worker memory, progress, elapsed time, and optional energy | Display resource use and calculation status | Local UI; an assigned worker also reports bounded progress directly to its publisher |

RoTab has no developer analytics endpoint, advertising integration, or sale of personal information. External services apply their own data practices to requests they receive.

## Discovery and scientific sharing

Discovery is enabled by default while a coordinating RoTab session is open. It announces a persistent pseudonymous public identity, room topic, capabilities, and bounded availability metadata to the selected Nostr relays. Calculation requires **Start volunteering** or acceptance of a specific model. Connection settings can disable discovery.

The default discovery relays are `wss://relay.damus.io` and `wss://nos.lol`. Relays receive public presence and encrypted signaling. Protein files, returned structures, and research descriptions are transferred over WebRTC rather than published as plaintext relay events. A room name is a discovery topic, not a private access-control secret.

Connected participants receive campaign descriptions; assigned workers receive their targets. Publishers receive signed outputs and progress. Recipients can retain or export scientific content they receive. Transport encryption does not prevent an authorized recipient from copying a structure or establish the correctness of a result.

STUN/TURN services receive connectivity metadata and any authentication required for relay allocation. TURN relays carry encrypted WebRTC traffic when direct connectivity is unavailable. The shared pilot includes generated relay access, which can be extracted from the extension; it does not include the provider account password or account-management API secret. Custom connection settings remain local. **Test TURN** checks allocation without transferring a scientific input or starting a calculation.

## Optional services

Weather uses a manually entered city or device location with browser/OS permission. Device coordinates are rounded to two decimal places before the city-name lookup. Location is not published to volunteers. Failed or declined detection offers city entry.

Google search suggestions default off. Enabling them sends partial queries to Google; submitting a search opens Google independently of that preference. Most-visited shortcuts require optional browser permission.

Google Calendar requires optional access, authorization, and a configured OAuth client. Calendar data is used for the displayed calendar and requested event operations. It is not sent to volunteer peers or scientific exports and is not used by RoTab for advertising.

An explicitly configured hosted research API is a separate optional mode. It receives task/result data and protocol identifiers. The default browser build has no hosted research API origin.

## Local retention and deletion

Preferences and identities remain until changed or browser data is removed. The latest 20 completed browser run records are retained. Each model's display history is bounded to 2,000 energy samples and up to 240 coordinate frames within an estimated 8 MiB frame budget. Campaign records, imported inputs, and pending signed results remain until removed or browser storage is cleared or evicted.

Removing a campaign deletes its local input, attempts, and outcomes and withdraws future assignments. Up to 128 recent worker identifiers may remain as connection hints for acknowledging late returns. These hints contain no deleted protein coordinates or results. Separate browser run records and copies held by other participants remain independent.

Favorites, tasks, board contents, and local events have deletion controls. Clearing extension data removes the broader local stores. Downloaded exports and browser backups can remain separately. RoTab cannot erase another participant's copy or a service provider's logs.

Disconnecting Google Calendar removes RoTab's local token. It does not delete Google events or necessarily revoke authorization in the Google account. Disabling discovery stops future rendezvous activity but does not recall information already received by relays or peers.

## Security boundaries

Executable JavaScript and WASM are packaged with the extension. Network jobs select supported protocols and cannot supply executable code. Signed messages and encrypted signaling authenticate transfer paths; they do not provide independent scientific validation.

Profile storage is not protected by an additional application-level encryption layer or a claim of hardware-backed key storage. Access to the browser profile can expose its records and authentication material. Experiment exports omit signing secrets, OAuth tokens, and TURN authentication, but can contain complete structures, descriptions, and participant identifiers.

## Documentation website

The documentation is hosted through GitHub Pages. Requests can disclose ordinary web metadata, including IP address and browser details, to GitHub under its [privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). The site uses local system fonts and contains no RoTab advertising or analytics integration.

[Help and security](support.md) describes troubleshooting and the information appropriate for a public issue.
