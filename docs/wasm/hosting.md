# Standalone deployment and integration

The SDK is a browser library independent of Chrome permissions, Nostr, job scheduling, React, backend databases and native companions. The host application provides its UI, consent controls, persistence and any transport of scientific inputs and results. [Quick start](quickstart.md) covers package imports; this chapter specifies deployment requirements and worker lifetime.

## Static file contract

```text
public/science/
  sdk/                       # copy the entire generated dist, not just index.js
    index.js, worker.js, chunks…, methods/…, *.d.ts
  engine/
    manifest.json
    rosetta.mjs
    rosetta.wasm
    rosetta.data
    licensing and citation files
```

Use a versioned directory on static HTTPS hosting. Supply that engine directory and the SDK worker URL to `createRosetta`. Keep worker dependencies/chunks together. Serve JavaScript as JavaScript, `.wasm` as `application/wasm` and `.data` as binary. A single-page-app fallback must not return `index.html` for a missing scientific file. Opening `file://` is not a supported module/fetch deployment.

The worker must be served from the application's origin. Cross-origin engine assets require CORS authorization for that origin and permission in the application's Content Security Policy (CSP). Relevant directives may include `script-src 'self' 'wasm-unsafe-eval'`, `worker-src 'self'` and a suitable `connect-src` for asset fetches. These fragments must be integrated into the site's complete policy. The current single-threaded build does not require pthreads, SharedArrayBuffer or COOP/COEP.

For a Chrome extension, bundle executable JS/WASM in the extension package. Do not copy a website's remote-executable-asset deployment into Manifest V3. [Chrome's remote hosted code guidance](https://developer.chrome.com/docs/extensions/develop/migrate/remote-hosted-code).

## Client lifecycle

```js
import { createRosetta, preparePdb } from "@rotab/rosetta-wasm";

const client = createRosetta({
  engineUrl: new URL("/science/engine/", location.href),
  workerUrl: new URL("/science/sdk/worker.js", location.href),
});
const controller = new AbortController();
const prepared = preparePdb(originalPdb);

try {
  const common = { seed: 17, dutyCycle: 10, signal: controller.signal };
  const initial = await client.score(prepared.pdb, common);
  const refined = await client.minimize(prepared.pdb, {
    ...common,
    onSnapshot: frame => recordMeasuredFrame(frame),
  });
  await saveLocally({ originalPdb, preparation: prepared.report, initial, refined });
} finally {
  client.close();
}
// A Stop control can call controller.abort() during an active call.
```

`originalPdb`, `recordMeasuredFrame` and `saveLocally` are supplied by the host application. Both runs in this example use the prepared original input. Chaining returned coordinates requires explicitly passing `initial.pdb` to the next call. Sequential calls reuse the client's initialized scientific state. Concurrent calls on one client are rejected; separate clients allocate separate heaps. One client is the recommended initial configuration, with parallelism selected only after resource assessment.

Abort terminates the worker and rejects with `AbortError`. A later run on the still-open client starts a fresh worker and repeats setup. `close()` permanently closes that client. Neither operation serializes unfinished Rosetta state. The host application is responsible for persisting completed outputs and seeds before starting another model.

## Asset verification and trust

The worker checks the manifest and all three scientific SHA-256 pins before instantiating the WASM module. It compiles verified WASM bytes, supplies them through `instantiateWasm`, and mounts verified database bytes through `getPreloadedPackage`. A changed engine/database needs deliberate pin updates and new matching scientific gates; disabling verification is not an integration fix.

The worker checks the fetched bytes of `rosetta.mjs` before importing it from the configured trusted static origin. A hash check cannot attest a hostile host or browser or prevent a server from changing the later import response. Deployment requires immutable, versioned assets from a controlled origin, with production-host checks for MIME types, CORS, CSP and error handling.

## Records and rendering

`onSnapshot` provides actual PDB coordinates, REF2015 energy (REU), source/counter/progress, timestamp and allocated heap bytes. Feed PDBs to a viewer such as Mol*, but retain measured values before any interpolation/downsampling. Score normally produces initial/final snapshots of the same coordinates; Minimize/FastRelax can provide a changing optimization trajectory. Callback counts are not a molecular-dynamics time axis.

Final results include output PDB, protocol, sequence, reported REF2015 score, distinct optimization objective, input/output hashes, source/engine identity, seed/intensity and timing scopes. `timing.initializationMs` covers asset checks/factory startup; lazy Rosetta setup on the first call belongs to `calculationMs`. Cooperative `activeMs`/`sleepingMs` omit initialization before the timer is enabled and are not hardware CPU/temperature readings.

Persistence and network delivery are responsibilities of the host application. The SDK does not save IndexedDB records, upload to a project or award BOINC credit. Integration and distribution requirements include the [input/output contracts](io.md), [memory limitations](memory.md), [benchmark scope](../benchmarks.md) and [licensing conditions](../publishing.md).

## Deployment verification

Deployment validation covers root and method imports, relative worker chunks, downloaded asset hashes, cold/warm Score and Minimize, cancellation, repeated sequential calls and offline/missing-file errors. Records identify the browser/version, input/seed, timing scope and memory availability. Intended larger inputs require separate testing because browser memory remains finite despite the absence of a residue-count cap. Private fixtures and native rescoring establish only their recorded scientific scope.
