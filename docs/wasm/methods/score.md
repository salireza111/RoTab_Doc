# Fixed-coordinate scoring

Fixed-coordinate scoring evaluates an imported structure with full-weight REF2015 without applying an optimization mover.

## Standalone API

- Source: `packages/rosetta-wasm/src/methods/score.ts`.
- Built entry: `packages/rosetta-wasm/dist/methods/score.js` and `.d.ts`.
- Public import: `@rotab/rosetta-wasm/score`.
- Named/instance method: `score`.
- Scientific ABI identifier: `score`.

```js
import { createRosetta } from "@rotab/rosetta-wasm";
import { score } from "@rotab/rosetta-wasm/score";

const client = createRosetta({ engineUrl: "/science/engine/" });
try {
  const result = await score(client, pdb, {
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
ScoreFunctionFactory::create_score_function("ref2015"); score(pose);
```

The protocol performs score evaluation without packing or minimization.

Sequence and residue IDs are preserved. There is no conformational search. Pose import can complete missing standard atoms or hydrogens; this is scoring after Rosetta import, not a promise of a byte-identical PDB.

The optimization/reporting score function is REF2015. `objectiveEnergy` precedes PDB rounding; the returned `energy` is independently evaluated on the returned rounded PDB coordinates.

## Live view

Score emits initial and final states without an optimization trajectory. Camera rotation and display motion do not represent relaxation.

Snapshots are visualization records, not execution checkpoints or physical time steps. Energy can rise between callbacks.

## Evidence and limits

Recorded native/Node and Chrome/Brave scientific checks use the first 20-residue 1L2Y model, seed 17, with independent rescoring of returned structures. Standalone SDK checks have their own scope in [the evidence inventory](../../evidence.md). Shared engine validation does not establish an all-method standalone browser benchmark.

There is no relaxation, folding trajectory, custom weight set or external constraints interface. The separate 76-residue 1UBQ browser proof extends scoring input-size coverage, not all-protocol coverage.

All inputs remain subject to [canonical single-chain chemistry and finite memory](../io.md). BOINC workunit flags and official Rosetta@home result acceptance are outside this adapter.

The scientific harness `engine/rosettatab.cc` defines these settings; [upstream reference](https://github.com/RosettaCommons/rosetta/blob/369e400415dd5c585f80dcf7b647147ee520e8ba/source/src/core/scoring/ScoreFunction.cc) documents the algorithm and source context.

