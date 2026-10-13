# Input and output contracts

## Strict coordinate input

The admitted methods take PDB text representing one nonempty protein chain of the 20 standard amino-acid types. Every residue needs N, CA, C and O backbone atoms. Coordinates must be finite and within the existing admission range of ±10,000 Å. Duplicate atoms, unresolved alternate-location labels, multiple coordinate models, HETATM chemistry and conflicting residue names are rejected by strict validation.

Input validation imposes no residue-count cap. Execution remains constrained by the 512 MiB per-worker heap ceiling, browser compiler/process memory and reduced database coverage. A large input may pass admission and still fail during calculation. Structure-record validation does not comprehensively detect missing biological segments, unusual covalent topology or every malformed PDB convention.

Full PDB arguments use a heap buffer rather than the small C stack. Browser-specific atom-tree traversal and release also use heap worklists to avoid deep call-stack failures. See [large protein memory](memory.md) for the adaptations, regression checks and remaining resource limits.

Use `validatePdb(pdb)` for admission without preparation. It returns `{ residues, atoms, chain }`. Supported standalone text input is PDB, not a general mmCIF/FASTA/fragments/silent-file API. The extension can unpack certain local file containers before applying the same coordinate policy; that capability is not implicitly part of the standalone method ABI.

## Explicit preparation

`preparePdb(original)` creates a protein-only copy, validates the prepared result, and returns `{ pdb, changed, report }`. Preparation is explicit in the standalone SDK and automatic for extension uploads. Keep the original bytes and report together with the calculation record.

| Situation | Preparation action |
| --- | --- |
| BOM / Windows line endings | Normalize text and record the change |
| Multiple MODEL records | Select the first complete coordinate model and record selection |
| Alternate atom locations | Choose one complete backbone conformer per residue, ranked by mean valid occupancy; A wins ties |
| Identical duplicate atom records | Remove exact duplicates and count them |
| Conflicting duplicates | Reject instead of guessing |
| Crystallographic HOH/WAT/DOD, including linked water | Remove for this implicit-solvent protocol and count atoms |
| Non-protein HETATM ions and ligands | Exclude from the protein-only copy; report component names, residue counts and atom counts |
| LINK/CONECT references to excluded components | Remove the LINK record or excluded CONECT target; preserve protein-to-protein connectivity |
| Standard amino acids recorded as HETATM | Retain coordinates and normalize the record type to ATOM |
| Modified/noncanonical protein residues | Reject rather than delete or substitute a protein residue |
| Extra protein chains or missing backbone | Retain/reject; never select a chain silently or fabricate coordinates |

Conformer selection does not choose each atom independently. Shared blank-location atoms can accompany the selected conformer. Removing alternate models/conformers or waters changes the input representation and must be reported. A prepared file's SHA-256 differs from the original when its bytes change.

The current report policy is `pdb-protein-only-preparation-v2`. It includes `nonProteinRemoved` entries with `name`, `kind`, `residues` and `atoms`, plus counts for removed LINK records, removed CONECT references and canonical HETATM records converted to ATOM. The existing `waterAtomsRemoved` count remains available. Saved v1 reports remain readable. Use the updated build on participants receiving prepared campaigns so that the v2 original-input provenance is recognized.

The extension displays an always-visible caution before calculation or submission, with expandable details and **Original PDB** / **Prepared PDB** downloads. Originals and both hashes are retained in local calculation provenance. The SDK caller must provide its own notice and retain the original; `preparePdb` does not overwrite a file or keep a separate archive.

Removing a metal, ligand, cofactor or linked water changes the modeled system. Results apply to the retained protein, with those components and their interactions excluded. This workflow does not reproduce the energy of the original complex or automatically repair covalent adducts. Modified protein residues declared by MODRES, common unsupported amino acids and protein-like HETATM backbones are rejected conservatively; incomplete or unusual chemistry can still need manual preparation. Standard-atom coordinates remain unchanged by component removal, but the complete scientific system is different.

Connectivity pruning follows the fixed-width endpoints in the [wwPDB LINK format](https://www.wwpdb.org/documentation/file-format-content/format33/sect6.html). Component cleanup is input preparation, not added Rosetta ligand or metal support.

## Output identity

Every method returns a PDB and the computed sequence. All eight preserve residue count and PDB residue identifiers in the admitted fixture contract. Non-design methods must also preserve residue names. `fixed_backbone_design` and `fastdesign` may change canonical residue identities; they are not safe substitutions when the scientific intent requires an unchanged sequence.

The host validates returned PDB syntax, residue identity and reported objective/energy types. These checks do not replace independent scientific rescoring or confirm all topology/geometry. Native acceptance tools rescore returned coordinates and compare with the tolerance defined in [benchmarks](../benchmarks.md).

## Energies and rounding

The C++ harness serializes coordinates to PDB, reimports those rounded coordinates, then computes the returned `energy` with full-weight REF2015. `objectiveEnergy` is evaluated on the pre-serialization pose. Cartesian objectives additionally change two weights; their values must not be directly mixed with common REF2015 history.

Intermediate display snapshots score a pose copy before PDB serialization. Reimporting the snapshot's rounded PDB can yield a slightly different value. Final `Result.energy` explicitly uses returned-coordinate rescoring. Preserve this distinction when comparing snapshot, pose-table, score-file and final-coordinate energies.

Rosetta Energy Units are objective values, not watts or physical time. Lower energy is a protocol-specific ranking signal, not proof that a designed sequence folds, is experimentally stable or has a particular function.

## Records for reuse or publication

Store the original file, prepared input/report, SHA-256 of both, protocol, seed, fixed work budget, complete result, output hash, engine/source/data hashes, browser/OS versions, timing scope and errors. If retaining frames, record which samples were dropped and which model owns each frame. Keep failed runs in the experimental record rather than reporting only successes.

The SDK's result provenance covers its exact prepared input and returned output. It does not automatically retain originals, browser versions, full history, experiment IDs, campaign/participant IDs or independent validation. Its caller owns those records; RoTab's Session/export formats add those product-level fields.
