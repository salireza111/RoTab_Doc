# Side-chain repacking

Side-chain repacking searches Rosetta rotamer assignments while keeping the backbone and amino-acid sequence fixed.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/repack.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/repack.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/repack`.
- Named/instance method: `repack`.
- Scientific ABI identifier: `repack`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { repack } from "@rotab/rosetta-wasm/repack";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await repack(client, pdb, {
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
TaskFactory::create_packer_task(pose); or_include_current(true); restrict_to_repacking(); PackRotamersMover(objective, task, 1);
```

The protocol performs one PackRotamersMover invocation and packing round, including current rotamers.

Side-chain coordinates may change; sequence, backbone and residue identifiers are retained under the admitted operation.

The optimization/reporting score function is REF2015. `objectiveEnergy` precedes PDB rounding; the returned `energy` is independently evaluated on the returned rounded PDB coordinates.

## Live view

Snapshots include initial and final states and complete accepted rotamer assignments reconstructed on a display-only pose. Updates can be sparse.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

No resfile, residue subset or extra-rotamer command flags are exposed. It is neither backbone relaxation nor sequence design.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/protocols/minimization_packing/PackRotamersMover.cc) documents the algorithm and source context.

