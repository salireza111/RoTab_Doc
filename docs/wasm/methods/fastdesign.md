# Flexible-backbone FastDesign

FastDesign combines sequence design with backbone and side-chain relaxation through Rosetta's FastDesign mover.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/fastdesign.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/fastdesign.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/fastdesign`.
- Named/instance method: `fastDesign`.
- Scientific ABI identifier: `fastdesign`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { fastDesign } from "@rotab/rosetta-wasm/fastdesign";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await fastDesign(client, pdb, {
    seed: 17,
    dutyCycle: 25,
    onSnapshot: frame => console.log(frame.source, frame.energy),
  });
  console.log(result.pdb, result.energy, result.sequence);
} finally {
  client.close();
}
```

`pdb` is caller-supplied, strictly validated PDB text. See [input preparation](../io.md), [shared API options](../api.md) and the [deployment example](../quickstart.md). Execution takes place in the dedicated browser worker, independently of volunteer networking or native processes.

## Exact scientific settings

```cpp
protocols::denovo_design::movers::FastDesign mover(objective, 1); set_up_default_task_factory(); apply(pose);
```

The protocol performs one FastDesign repeat with the pinned default task factory and upstream script.

Sequence, side-chain packing and backbone coordinates can change. PDB residue identifiers/count are preserved.

The optimization/reporting score function is REF2015. `objectiveEnergy` precedes PDB rounding; the returned `energy` is independently evaluated on the returned rounded PDB coordinates.

## Live view

Snapshots include FastRelax-derived stage, minimization and packing callbacks, together with initial and final structures.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Native/Node and Chrome/Brave checks for the engine with large-input memory adaptations use the first eight residues of 1L2Y, seed 17, with independent returned-coordinate rescoring. The older engine's full 20-residue native/Node test is retained as historical evidence with its original hashes in [the evidence inventory](../../evidence.md). It does not establish 20-residue FastDesign coverage for the current binary. Standalone SDK validation is reported separately.

The API does not expose custom design task factories, motifs, constraints, residue restrictions or scripts. The historical engine's 20-residue native/Node fixture took about 27 minutes at the recorded duty target. Current coverage uses only residues 1 to 8 of 1L2Y and does not establish general design scalability.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://docs.rosettacommons.org/docs/latest/scripting_documentation/RosettaScripts/Movers/movers_pages/FastDesignMover) documents the algorithm and source context.
