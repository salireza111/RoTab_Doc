# Scope and development directions

RoTab supports browser computation through eight bounded Rosetta coordinate methods. Each method has a fixed scientific contract and documented input, resource, and validation limits.

## Supported operation

The extension provides molecular visualization, retained energy snapshots, independent seeded models, and volunteer campaigns coordinated by the submitting browser. The standalone API provides the same scientific methods through its own worker host.

The current browser API supports scoring, torsion and Cartesian minimization, repacking, fixed-backbone design, FastRelax, FastDesign, and Cartesian FastRelax. [Method catalogue](wasm/methods/index.md).

## Development areas

| Area | Direction | Current boundary |
| --- | --- | --- |
| Scientific coverage | Additional structures, seeds, chemistry, and method fixtures | Current evidence is concentrated on small canonical proteins |
| Resource use | Broader cold/warm startup, memory, and throughput measurements | Heap readings are not total process RAM or thermal measurements |
| Standalone lifecycle | Caller-controlled persistence and interrupted-model recovery | The SDK currently leaves durable storage to its caller |
| Network reliability | Different-network trials, coordinator recovery, and redundant result validation | Recorded multi-profile trials shared one computer |
| Initialization | Reduced repeated database and scoring-table setup | Extension model workers currently start with fresh instances |
| Scientific validation | Broader native rescoring and task-specific validation | Delivery receipts do not establish scientific correctness |

These areas describe research and engineering directions, not release dates or commitments.

## Additional Rosetta families

| Family | Scientific requirements beyond the current API |
| --- | --- |
| Cyclic peptide prediction | Topology and noncanonical-residue contracts, native silent reimport, browser validation |
| Fragment-based folding | Sequence/fragments, centroid resources, stage-specific snapshots, full-atom validation |
| Loop and template modeling | Loop definitions, alignments, closure, and chain-continuity checks |
| Mutation ΔΔG | Paired ensembles, mutation schema, and a consistent reference objective |
| Docking and symmetry | Multichain/symmetry contracts, rigid-body moves, and interface validation |
| Ligand modeling | Chemical parameters, conformers, resources, and geometry validation |
| RosettaScripts | Fixed, reviewed templates and protocol-specific input contracts |

The [experimental inventory](wasm/experimental.md) distinguishes compiled research modules from methods supported in browsers. RNA/DNA, membranes, general noncanonical chemistry, Python/VirtualBox workloads, and GPU/MPI execution require separate scientific and resource evaluation.

## BOINC and Rosetta@home

Official participation would require project-approved application identity, task and output contracts, scientific validation, and result reporting. These interfaces are not implemented. Reading coordinates from a downloaded workunit does not reproduce all of that workunit's inputs or protocol settings. [BOINC comparison](boinc.md).

## Current exclusions

The production API does not expose arbitrary Rosetta flags, custom score weights, user-supplied executable scripts, or repeat settings. It does not accept general mmCIF, silent, FASTA, fragment, or multimolecular inputs.

Recovery retains completed models and replays unfinished seeds. It does not serialize a suspended minimizer, annealer, complete Pose, or RNG continuation. Closing the last RoTab stops browser computation.

One trajectory is single-threaded. Independent models can run in separate workers; there is no pthread/OpenMP/MPI, CUDA, or WebGPU scientific execution. RoTab does not provide hardware temperature, fan-speed, or component-wattage sensors.
