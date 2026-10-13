# Standalone quick start

`@rotab/rosetta-wasm` is a browser library for the eight bounded Rosetta coordinate methods. It runs in a dedicated module worker and is independent of the extension, volunteer network, and native clients.

The adapter currently has local package metadata at version 0.1.0 and has not been published to a package registry. Integration requires the generated adapter files and a matching, authorized scientific engine. The adapter's MIT license is separate from Rosetta's license. [Build reference](build.md), [licensing and availability](../publishing.md).

## Use the package

The adapter is supplied as a local tarball for integration into a host application. If the application bundler does not preserve module workers and chunks, copy the package's complete `dist/` to a static asset directory and supply `workerUrl` explicitly.

```js
import { createRosetta, preparePdb } from "@rotab/rosetta-wasm";
import { relax } from "@rotab/rosetta-wasm/relax";

const client = createRosetta({
  engineUrl: new URL("/science/engine/", location.href),
  workerUrl: new URL("/science/sdk/worker.js", location.href),
});

const originalPdb = await (await fetch("/target.pdb")).text();
const prepared = preparePdb(originalPdb);
try {
  const result = await relax(client, prepared.pdb, {
    seed: 17,
    dutyCycle: 10,
    onPhase: phase => updateStatus(phase),
    onSnapshot: frame => {
      renderPdb(frame.pdb);
      appendEnergy(frame.energy); // REF2015 / REU
    },
  });
  saveRecord({ originalPdb, preparation: prepared.report, result });
} finally {
  client.close();
}
```

`updateStatus`, `renderPdb`, `appendEnergy` and `saveRecord` are application callbacks, not SDK exports. The provided vanilla example implements an energy graph and PDB/JSON download without a viewer dependency. Feed `frame.pdb` into Mol* or another viewer when embedding molecular rendering.

Alternatively call `client.relax(pdb, options)` or the generic `client.run("relax", pdb, options)`. Every method shares the same pinned engine; separate imports do not duplicate its 146 MB scientific payload.

## Plain browser example

The private bundle's entry point is `dist/rosetta-wasm-standalone/example/index.html`. It includes input upload, method/seed/intensity selection, run/abort controls, measured energy history and result/provenance downloads. Deploy the directory as static HTTPS assets or mount it in an existing development preview. Participants access the application through a browser without installing a compiler, native helper or local service.

```text
rosetta-wasm-standalone/
  example/index.html, main.js, input.pdb
  sdk/index.js, worker.js, chunks…, methods/…, *.d.ts
  engine/manifest.json, rosetta.mjs, rosetta.wasm, rosetta.data
  engine/ROSETTA_LICENSE.md, CITING_ROSETTA.md
```

Opening with `file://` does not provide a suitable module/fetch origin. Serve `.mjs/.js` as JavaScript and `.wasm` as `application/wasm`. Keep generated chunks in place. The worker should be same-origin; cross-origin scientific assets require CORS. Typical CSP needs local scripts, `worker-src 'self'` and permission to compile WASM (`'wasm-unsafe-eval'` in `script-src`). No SharedArrayBuffer/pthread headers are required for this build.

Cold initialization can take minutes. The first Rosetta call performs lazy database and scoring-table setup after the Emscripten factory returns, so `loading-module` is not the whole cold-start cost. Reuse a client for sequential runs to retain that setup, and call `close()` when finished to release the heap. See [API lifecycle](api.md) and [measured benchmarks](../benchmarks.md).

This example explicitly requests 10% intensity; the SDK's omitted-option default remains 25%. The extension independently defaults to one worker/10%. For static deployment, cancellation, warm reuse and persistence responsibilities, follow [Deployment and integration](hosting.md).
