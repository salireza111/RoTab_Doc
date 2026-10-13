# Fixed-backbone sequence design

Fixed-backbone design searches canonical amino-acid identities and side-chain rotamers on a fixed backbone using Rosetta's packer.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/fixed-backbone-design.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/fixed-backbone-design.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/fixed-backbone-design`.
- Named/instance method: `fixedBackboneDesign`.
- Scientific ABI identifier: `fixed_backbone_design`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { fixedBackboneDesign } from "@rotab/rosetta-wasm/fixed-backbone-design";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await fixedBackboneDesign(client, pdb, {
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
TaskFactory::create_packer_task(pose); or_include_current(true); PackRotamersMover(objective, task, 1);
```

The method performs one packing/design round. Unlike repacking, it can choose new amino-acid identities.

Canonical residue identities and sequence may change. Backbone and PDB residue identifiers/count remain fixed.

The optimization/reporting score function is REF2015. `objectiveEnergy` precedes PDB rounding; the returned `energy` is independently evaluated on the returned rounded PDB coordinates.

## Live view

Snapshots include initial and final states and throttled, complete accepted packing assignments. Intermediate states belong to one optimization run and are not independent designed models.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

No user resfile, per-position allowed identities, motif constraints or functional objective is exposed. Lower REF2015 energy does not establish folding, stability or biological function. Design can be much slower than repacking.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/core/pack/task/TaskFactory.cc) documents the algorithm and source context.

