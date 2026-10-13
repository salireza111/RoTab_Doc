# Cartesian minimization

Cartesian minimization optimizes atomic coordinates with Rosetta's Cartesian MinMover and a fixed Cartesian-compatible objective.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/cartesian-minimize.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/cartesian-minimize.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/cartesian-minimize`.
- Named/instance method: `cartesianMinimize`.
- Scientific ABI identifier: `cartesian_minimize`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { cartesianMinimize } from "@rotab/rosetta-wasm/cartesian-minimize";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await cartesianMinimize(client, pdb, {
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
MinMover(movemap, objective, "lbfgs_armijo_nonmonotone", 0.01, true); max_iter(200); cartesian(true);
```

The minimizer uses at most 200 iterations and tolerance 0.01, with backbone and chi degrees of freedom enabled and jumps disabled.

Atomic coordinates can change. Sequence and residue identifiers remain fixed.

The optimization objective starts from REF2015, sets `cart_bonded=0.5` and `pro_close=0`, and is identified as `ref2015_cart`. `objectiveEnergy` is evaluated before PDB rounding. The returned `energy` and live history use the common full-weight REF2015 function.

## Live view

Snapshots include Cartesian derivative-evaluation states and initial and final structures. Reported progress does not predict remaining time.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

The API does not expose custom nonideal degrees of freedom, restraints, MoveMaps or score weights. Its optimization objective is distinct from the full-weight REF2015 history and is not directly comparable.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://docs.rosettacommons.org/docs/latest/scripting_documentation/RosettaScripts/Movers/movers_pages/MinMover) documents the algorithm and source context.

