# Display, recovery and resources

## Live view and energy history

The viewport receives measured PDB snapshots from Rosetta's initial/final states, FastRelax commands, minimizer derivative evaluations and accepted packing assignments. Display-only copies are scored with full-weight REF2015. FastRelax's ramped objective is not mixed into the graph. The view follows the focused model when several independent models run concurrently.

Internal snapshots have a nominal 200 ms throttle, not a guaranteed five-frame-per-second stream. Rosetta initialization, large individual operations and event-loop scheduling can produce longer gaps. The source counter is not a fixed physical time step; a minimizer callback can be a trial state rather than an accepted optimizer step. Energies may rise and a final rounded-coordinate score need not equal the lowest displayed intermediate energy.

Retained graph points select exact measured frames. Selecting a baseline enables a rigidly aligned comparison and matched C-alpha RMSD against another frame. The overlay is a display transform, not a modification of either saved structure. Pinned residue selection persists independently of hover. Inspection does not pause science.

Visible rendering is capped at 30 FPS; hidden/offscreen views stop continuous rendering. Automatic orbit defaults on, with a saved **Rotate protein automatically** checkbox in Computation settings and a matching viewport control. Reduced motion disables orbit/transition motion, selecting a residue pauses orbit for inspection, and WebGL loss has a static fallback. These presentation controls do not alter the algorithm or seed.

## Display frames are not checkpoints

Each model keeps up to 240 coordinate frames within an estimated 8 MiB budget, alongside a 2,000-sample energy window. Exports retain frame hashes. These are visualization records, not complete Rosetta execution state.

A restart checkpoint records the original input, protocol, model IDs/seeds and completed outputs. It does not serialize the minimizer's stack, annealer, full Pose state or RNG continuation. Pause/stop, tab discard or owner closure terminates unfinished workers. A surviving owner skips finished models and replays unfinished seeds. Closing the last RoTab stops all browser workers; recovery follows the saved continuation preference.

## Resource readings

The strip distinguishes approximate JavaScript heap for the viewing page from fresh allocated WASM linear memory in scientific workers. These scopes exclude parts of renderer/process/compiler/GPU overhead and are not total tab RAM. Partial, stale, or unavailable readings are omitted.

Portable browser APIs do not provide reliable per-component CPU temperature, fan speed, CPU/GPU wattage or physical-core ownership for this product. The default browser UI does not show empty hardware fields. The browser-reported logical-processor count is a scheduling hint and may be reduced for privacy or resource policy.

Extension local/imported batches default to **one worker**, adjustable in settings. Each worker handles a separate model with its own heap. One Rosetta trajectory is still single-threaded. The single-owner guarantee means one supervised pool, not necessarily one scientific worker. Each browser accepts at most one network model at once and rests for 30 seconds after completion. Hosted attempts and available campaign assignments can use fewer workers than the configured maximum.

The extension's per-worker duty target defaults to 10% and accepts values from 10% to 75% in the scientific ABI. Profiles using the earlier implicit half-core/25% setting migrate once; distinct custom choices remain saved. **Use low-power defaults** restores one worker/10%. The standalone SDK independently defaults to 25% when its caller omits the option.

The target is cooperative active-versus-sleep time, not a promise of total machine CPU percentage. Rosetta initialization precedes the budget timer, and long synchronous operations can run until a yield hook. Concurrent extension pools share compiled code; a single-worker run compiles inside its disposable worker. Each model receives a new instance, so setup can repeat beyond the first extension use. The SDK can retain a warm instance for sequential calls. Memory increases with concurrent workers; hardware temperature/fan comparisons across users remain unmeasured. [Startup implementation](../wasm/port.md#startup-and-power-budget) and [completion memory lifetime](../wasm/memory.md#completion-and-retained-memory).
