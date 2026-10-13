# Primary sources

External sources below were checked October 9, 2026. Implementation status and numerical results are based on the source repository and [recorded evidence](evidence.md). Upstream documentation provides scientific and platform context and may describe options outside the supported API.

## Rosetta and Rosetta@home

- [Pinned Rosetta source](https://github.com/RosettaCommons/rosetta/tree/369e400415dd5c585f80dcf7b647147ee520e8ba).
- [Pinned scientific BOINC dispatcher](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/apps/public/boinc/minirosetta.cc).
- [Pinned native graphics memory definition](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/protocols/boinc/boinc_shmem.hh).
- [Published project applications](https://boinc.bakerlab.org/rosetta/apps.php).
- [Relax scientific/application documentation](https://docs.rosettacommons.org/docs/latest/application_documentation/structure_prediction/relax).
- [FastDesign](https://docs.rosettacommons.org/docs/latest/scripting_documentation/RosettaScripts/Movers/movers_pages/FastDesignMover).
- [MinMover](https://docs.rosettacommons.org/docs/latest/scripting_documentation/RosettaScripts/Movers/movers_pages/MinMover).
- [Energy terms](https://docs.rosettacommons.org/docs/latest/rosetta_basics/scoring/score-types).
- [Pinned license](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/LICENSE.md) and [citation guidance](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/CITING_ROSETTA.md).
- [RCSB 1L2Y](https://www.rcsb.org/structure/1L2Y), [RCSB 1UBQ](https://www.rcsb.org/structure/1UBQ).

## BOINC

- [Overview](https://github.com/BOINC/boinc/wiki/BOINC-overview).
- [API for native applications](https://github.com/BOINC/boinc/wiki/API-for-native-apps).
- [Job templates and logical file contracts](https://github.com/BOINC/boinc/wiki/Job-templates).
- [Job submission and control](https://github.com/BOINC/boinc/wiki/Job-submission-and-control).

## Browser runtime and network

- [Emscripten asynchronous execution / Asyncify](https://emscripten.org/docs/porting/asyncify.html).
- [Emscripten file packaging](https://emscripten.org/docs/porting/files/packaging_files.html).
- [C++ / JavaScript interoperation](https://emscripten.org/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.html).
- [WebRTC peer connections](https://webrtc.org/getting-started/peer-connections).
- [Nostr NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md), [NIP-44](https://github.com/nostr-protocol/nips/blob/master/44.md).
- [Chrome extension CSP](https://developer.chrome.com/docs/extensions/reference/manifest/content-security-policy), [remote executable-code rules](https://developer.chrome.com/docs/extensions/develop/migrate/remote-hosted-code).
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/creating-your-site/).

## TURN provider setup and service limits

The following Metered references were checked **October 13, 2026**. Published provider terms and account-specific settings can change; the [TURN usage guide](help/turn.md) distinguishes current advertised limits from RoTab behavior.

- [Open Relay monthly free allowance](https://www.metered.ca/tools/openrelay/).
- [Provider terms](https://www.metered.ca/terms): section 7 covers free-plan availability; Schedule 1 defines measured relay traffic.
- [Free and paid endpoint availability](https://www.metered.ca/docs/turnserver-guides/turnserver-regions/).
- [Creating generated TURN credentials](https://www.metered.ca/docs/turn-server-service/creating-turn-credentials/).
- [Supported transport examples](https://www.metered.ca/docs/turn-server-service/quickstart/).

## PDB input records

Checked October 13, 2026: [wwPDB coordinate records](https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html) and [LINK connectivity fields](https://www.wwpdb.org/documentation/file-format-content/format33/sect6.html). These define file records; RoTab's protein-only preparation and supported chemistry are documented in the [input contract](wasm/io.md).
