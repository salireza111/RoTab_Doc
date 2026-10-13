# Help and security

The [illustrated Help guide](../help/index.md) covers controls and ordinary workflows. [Troubleshooting](../help/troubleshooting.md) explains connection failures, missing results, snapshots, and memory use.

## Problem reports

A useful report identifies the extension version, browser and operating system, calculation protocol, resource settings, and steps that reproduce the problem. The stage of failure also matters: connection, engine startup, calculation, or result delivery.

**Live devices → Download connection diagnostics** exports route types and setup state without candidate addresses, raw SDP, authentication values, participant identities, or scientific payloads. This is separate from an experiment export.

A scientific report can include an authorized minimal structure, seed, method, and provenance. Experiment exports can contain complete structures and research descriptions. Public issues are suitable only for information authorized for disclosure.

The [documentation repository](https://github.com/salireza111/RoTab_Doc) provides a reference point for readers with repository access. No private security-reporting address is listed in this documentation. Passwords, access tokens, signing keys, browser profiles, and confidential datasets should not be posted publicly.

## Security boundaries

Potential security problems include exposed authentication material, signature/admission bypass, acceptance of executable job content, or cross-origin data leakage. RoTab does not provide remote key recovery or deletion of another participant's copies. No security-audit certification or guaranteed response time is represented here.

## Local data controls

Favorites, tasks, board contents, and local events can be removed through their editors. Browser extension-data controls remove the broader profile-local stores. Required scientific records should be exported before deletion.

Disconnecting Google Calendar discards RoTab's local session token. Google account authorization and existing Google events remain separate. The [data reference](privacy.md) describes retention and recipients.
