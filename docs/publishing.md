# Licensing and availability

RoTab comprises application and adapter source, a compiled scientific engine, and this documentation. These components have separate distribution and licensing conditions.

## Availability

The extension is available as a private Chromium build. The standalone adapter has local package metadata under `@rotab/rosetta-wasm` version 0.1.0 and has not been published to a package registry. No Chrome Web Store release is available.

The documentation repository contains reference material, screenshots, and selected validation summaries. It does not distribute Rosetta binaries, the scientific database, browser profiles, or authentication material. [Current status](status.md) identifies the available components and their validation scope.

## Application and documentation license

The MIT license covers original RoTab application, adapter, and documentation material. It does not license Rosetta, its database, BOINC, or third-party dependencies. Those components retain their own terms and notices.

The static documentation uses MkDocs and Material for MkDocs. Their license notices are included with the website. Scientific results also remain subject to the rights associated with their input data.

## Rosetta license

The pinned [Rosetta license](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/LICENSE.md) governs the scientific source and executables. It provides specified internal noncommercial rights and directs commercial licensing questions to UW CoMotion. Authorization for public distribution of this modified WASM binary and database has not been established. The MIT adapter license does not grant those rights.

The engine identity includes the scientific source commit, compiler version, resource manifest, and per-file SHA-256 values. Validation applies to those exact artifacts. Changes to the scientific engine or database require corresponding validation and host compatibility checks.

## Citation and affiliation

Rosetta use is subject to its [citation guidance](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/CITING_ROSETTA.md), relevant method references, and structure-specific citations. RoTab is an independent project and does not represent endorsement by RosettaCommons, Rosetta@home, or BOINC.
