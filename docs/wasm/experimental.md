# Research application modules

The coordinate SDK exposes eight methods with fixed settings. Two additional research WASM targets under `engine/artifacts/wasm` provide broader scientific dispatch and cyclic peptide experiments. Both remain outside the extension and supported SDK.

| Module family | Scientific files, total bytes | Evidence | Browser volunteer admission |
| --- | ---: | --- | --- |
| `rosetta-application` | 455,406,615 | Links upstream `minirosetta.cc` and release registration; limited cyclic Node WASM outputs rescored | No; exceeds 250 MB package gate and lacks most per-mode fixtures |
| `rosetta-cyclic` | 154,392,541 | One eight-residue cyclic/D-amino-acid fixture in Node WASM, native rescore and topology checks | No; browser, broader chemistry, snapshots and task contracts pending |

The research host mounts explicit input files in Emscripten `/work`, passes newline-framed arguments to `rosettatab_run_application`, and collects file outputs. It is an operator experiment, not a remote arbitrary-code/job endpoint. The current Node runner requires a fresh module for an application invocation because Rosetta global options are process-wide.

## Linked upstream dispatch modes

The following modes are linked into the research target from the pinned source. Runtime validation is incomplete, and the inventory does not identify the current task mix distributed by Rosetta@home.

| Mode | Intended operation / data needed | Current evidence / remaining work |
| --- | --- | --- |
| `abrelax` | Fragment-based folding; FASTA, fragments, centroid resources | Compiled; bounded stages/input/browser validation pending |
| `simple_cycpep_predict` | Cyclic peptide prediction; sequence/chemical types | Node fixture rescored; browser and broader chemistry pending |
| `symdock` | Symmetric docking; symmetry definition and multichain input | Compiled; docking/topology fixtures pending |
| `broker` | Topology-broker workflow; claims/constraints | Compiled; reviewed preset/data contract pending |
| `loophash` | Loop-hash sampling; libraries | Compiled; database and sampling budgets pending |
| `ligand_dock` | Protein-ligand docking; ligand parameters/conformers | Compiled; chemistry, multichain/interface validation pending |
| `relax` | Full upstream relaxation application | Native smoke; full-dispatcher WASM runtime untested; separate bounded adapter proven |
| `looprelax` | Loop building/relaxation; loop definitions | Compiled; closure fixtures and checkpoints pending |
| `threading` | Template/comparative modeling; alignment/templates | Compiled; topology/input fixtures pending |
| `medal` | Comparative modeling/sampling | Compiled; archives/template contract pending |
| `medal_exchange` | Exchange variant | Compiled; exchange/scheduling semantics pending |
| `star` | STAR folding workflow; fragments/constraints | Compiled; fixed fixtures/stages pending |
| `rbsegmentrelax` | Rigid-body segment relaxation | Compiled; segment/multibody fixtures pending |
| `boinc_debug` | Runtime diagnostic workload | Not a scientific contribution method |
| `flxbb` | Flexible-backbone design | Compiled; bounded presets and design validation pending |
| `jd2_scripting` | RosettaScripts/JD2 | Compiled; requires reviewed packaged templates |
| `ddg` | Mutation stability ΔΔG | Compiled; paired ensembles/mutation list and ΔΔG validation pending |
| `canonical_sampling` | Canonical Monte Carlo | Compiled; sampling/output/checkpoint fixtures pending |
| `nonlocal_frags` | Nonlocal fragment workflow | Compiled; libraries and fixtures pending |

RNA/DNA, membrane systems, general noncanonical chemistry, Python/VirtualBox workflows, GPU inference and MPI are not supplied by the eight-method coordinate SDK. Their existence in the source tree or project application list does not establish a usable browser port.

## Cyclic evidence and unresolved issue

The smaller cyclic family produced one eight-residue fixture containing two D-residues. Its stored energy 10.319999695 REU agreed with native silent-record rescoring 10.319698257 within 0.001 REU. Topology checks found the N-to-C ring bond, a 1.328840518 Å closure distance and two D-amino-acid residue types. Recorded heap was 231,997,440 bytes. This is one Node WASM fixture, not general cyclic validation.

Silent records preserve annotated chemical topology. Converting a cyclic/D-residue record to an ordinary linear canonical PDB and rescoring would test a different molecule. A separate native control's first silent record failed score agreement on reimport (9.826 versus 55.383 REU); that unresolved result remains in the evidence and blocks a general silent-format compatibility claim. The returned WASM cyclic fixtures passed their own independent rescoring.

## Browser availability

These modules have no supported participant browser API and are unavailable through `client.run`. A supported family requires a fixed input schema, validated resources, a browser host, measured snapshots, and output/topology validation.
