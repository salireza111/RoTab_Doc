# Cartesian FastRelax

Cartesian FastRelax interleaves Rosetta rotamer packing with Cartesian minimization in one FastRelax repeat.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/cartesian-relax.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/cartesian-relax.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/cartesian-relax`.
- Named/instance method: `cartesianRelax`.
- Scientific ABI identifier: `cartesian_relax`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { cartesianRelax } from "@rotab/rosetta-wasm/cartesian-relax";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await cartesianRelax(client, pdb, {
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
FastRelax mover(objective, 1); cartesian(true); max_iter(200); apply(pose);
```

The protocol performs one repeat, with at most 200 minimizer iterations per invocation within the upstream script. The iteration limit applies to each minimizer invocation rather than the entire relaxation.

Backbone and side-chain atomic geometry can change. Sequence and residue identifiers remain fixed.

The optimization objective starts from REF2015, sets `cart_bonded=0.5` and `pro_close=0`, and is identified as `ref2015_cart`. `objectiveEnergy` is evaluated before PDB rounding. The returned `energy` and live history use the common full-weight REF2015 function.

## Live view

Snapshots include stages, Cartesian derivative states, accepted packing assignments, and initial and final structures.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

The API does not expose custom scripts, restraints, repeat counts, bond-geometry policies or dual-space mode. Geometry and topology across a wider input set require separate validation.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://docs.rosettacommons.org/docs/latest/application_documentation/structure_prediction/relax) documents the algorithm and source context.

