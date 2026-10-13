# Torsion minimization

Torsion minimization optimizes backbone and side-chain torsions with the pinned Rosetta L-BFGS minimizer.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/minimize.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/minimize.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/minimize`.
- Named/instance method: `minimize`.
- Scientific ABI identifier: `minimize`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { minimize } from "@rotab/rosetta-wasm/minimize";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await minimize(client, pdb, {
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
MinMover(movemap, objective, "lbfgs_armijo_nonmonotone", 0.01, true); max_iter(200); cartesian(false);
```

The minimizer uses at most 200 iterations and tolerance 0.01. Its MoveMap enables backbone and chi torsions and disables jumps.

Torsion-space coordinates can change. Sequence and residue identifiers remain fixed. The method does not perform rotamer packing or sequence design.

The optimization/reporting score function is REF2015. `objectiveEnergy` precedes PDB rounding; the returned `energy` is independently evaluated on the returned rounded PDB coordinates.

## Live view

Snapshots include initial and final states and throttled poses synchronized after derivative evaluations. Callback counts can exceed accepted iterations.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

The API does not expose custom MoveMaps, convergence tolerances, restraint files, iteration budgets or mutation lists. The method samples only the local minimization neighborhood.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://docs.rosettacommons.org/docs/latest/scripting_documentation/RosettaScripts/Movers/movers_pages/MinMover) documents the algorithm and source context.

