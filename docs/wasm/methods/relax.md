# Torsion FastRelax

Torsion FastRelax refines an existing structure through Rosetta's interleaved side-chain packing and torsion-space minimization.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/relax.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/relax.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/relax`.
- Named/instance method: `relax`.
- Scientific ABI identifier: `relax`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { relax } from "@rotab/rosetta-wasm/relax";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await relax(client, pdb, {
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
protocols::relax::FastRelax mover(objective, 1); mover.apply(pose);
```

The method performs one FastRelax repeat using the pinned upstream default script and convergence settings.

Backbone and side-chain conformations can change. Sequence and residue IDs are preserved.

The optimization/reporting score function is REF2015. `objectiveEnergy` precedes PDB rounding; the returned `energy` is independently evaluated on the returned rounded PDB coordinates.

## Live view

Snapshots include FastRelax script-command boundaries, synchronized minimizer trial states, accepted packing assignments, and initial and final structures.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

This API does not accept custom scripts, repeat counts, restraints or MoveMaps. A campaign's model count requests independent attempts, not additional repeats within a model. This is local refinement, not de novo folding or molecular dynamics.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://docs.rosettacommons.org/docs/latest/application_documentation/structure_prediction/relax) documents the algorithm and source context.

