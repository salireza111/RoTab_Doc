# Install and contribute

RoTab is distributed as a private unpacked Chromium extension. An authorized build can be loaded through Chrome or Brave's extension developer page. The documented interface is 0.5.6; the packaged shared-TURN pilot is 0.5.2. [Current capabilities](../status.md) distinguishes their validation records. [Illustrated Help](../help/index.md) describes the controls.

## Volunteer for a submitted protein

1. Network discovery starts automatically. The green Histidine/status indicator means a network connection is live; it does not mean a model is already running.
2. Choose **Start volunteering** in the simple protein widget or dashboard. This one click enables future compatible assignments; no connection settings are required. **Pause new tasks** stops accepting more work while the current model finishes.
3. Available campaigns show title, protocol, queue information and the sender's mandatory short description. **Contribute** still accepts one model without enabling automatic work.
4. The accepted protein appears in the molecular view. Its actual WASM snapshots drive the current/best energy and graph. Score-only tasks remain structurally static; optimization/design motion depends on the method.

The simple new-tab view retains the protein widget while computation runs. Returning to the dashboard restores its graphs and retained frames without starting another calculation. **Computation settings → Live demonstration → Try FastRelax · sample protein** starts a separate bundled demo when the session is available.

The computing tab has a histidine outline favicon: green for connected, pulsing green for research computation, yellow for a local benchmark/demo, gray for disconnected idle, and red for an error. Other tabs keep the same outline in a fixed gray. A reduced-motion preference disables pulsing. All tabs are titled **RoTab**. Linked tabs can start or pause volunteering without becoming a second coordinator; **Go to main tab** in Computation settings focuses the computing tab. When it closes, the next coordinator takes over the colored favicon.

The histidine beside **RoTab** in the page header uses those status colors in every tab, including linked tabs. Its pulse indicates research computation. There is no separate header status dot.

## Publish a target

Open the paper-plane **Volunteer network** panel. Upload a supported protein, select a method, provide a title and a description of 1 to 240 characters, choose the independent model count and starting seed, then submit. The campaign schema permits up to 1,000 model attempts. Each attempt runs the method's fixed work budget using its own seed; the model count does not change FastRelax repeats.

The publisher's browser stores the campaign before advertising it. Online compatible volunteers are discovered automatically; manual pairing is an advanced fallback rather than the normal submission step. Keep the publisher tab online to assign models and receive results. A submitted campaign can wait locally with no volunteers connected, then schedule when peers become available. **Also calculate on this browser** is checked by default: the publisher runs independent models alongside volunteers. Uncheck it for a coordinator-only campaign. Each browser runs one network assignment at a time; extra models wait for available participants.

The campaign panel distinguishes observed devices, ready volunteers, assignments waiting to start, and live running models. Each active model shows its worker, reported progress and latest energy when available. Updates come from the assigned browser, not estimated activity; stale telemetry is marked as awaiting an update.

Results retain campaign/attempt IDs, publisher/volunteer identities, seed, protocol, source/engine/data hashes and output hashes. The queue fences superseded/cancelled leases and deduplicates matching returned results; a delayed result can succeed while its token remains current. Export input, outputs and experiment records before removing local data. A received result remains scientifically **unverified** in the interface. [Assignment architecture](jobs.md).

## Local demonstrations and benchmarks

The live FastRelax demo uses packaged 1L2Y coordinates. The replay view uses previously recorded real frames and is explicitly playback. Offline import/export is available in computation settings for supported coordinate benchmarks. Neither the demo nor a local benchmark is an official Rosetta@home contribution.

A plain PDB import starts with **Fixed-coordinate scoring**. It evaluates the structure, saves initial/final snapshots, and completes without running relaxation. An unchanged structure and flat energy graph are expected for this method. In **Computation settings → Calculation protocol**, select **Torsion FastRelax** to optimize the imported protein; the selector applies to the imported target as well as bundled inputs. A completed imported Score also offers **Run FastRelax**. This starts a new run on the currently imported target, using the imported structure.

The next-run protocol choice persists locally. It does not change an active or paused checkpoint, previous results or the original protocol and reference declared by benchmark JSON. Exports record the executed protocol for each model; results from a different protocol are not labelled comparable to the original reference. Larger inputs can require substantially more time and memory. Successful large-input scoring does not establish FastRelax support for the same input. See [memory and verification scope](../wasm/memory.md).

Residue-energy colors read the weighted `total` column in each snapshot's Rosetta PDB energy table. The viewer maps the pinned standard residue types `HIS_D` to PDB `HIS`, and `CYZ` to `CYS`, including terminal variants, while retaining pose-ordinal and sequence-identity validation. A malformed/mismatched table remains unavailable rather than supplying guessed scores. Saved scored structures can be recolored after an extension update without rerunning Rosetta.

CPU worker count and per-worker intensity are local controls. Publishers cannot override them or enable automatic continuation remotely. Automatic acceptance starts off; **Start volunteering** explicitly enables it. Pausing terminates active scientific workers; completed models are retained, and unfinished models restart from their recorded seeds on resume.

## New-tab features

New installations use the simple view and light Doodle appearance. Appearance is separate from computation settings and includes dark/system variants, optional Doodle molecular rendering, local font stacks, custom accent, highlight and background colors, gradients and uploaded backgrounds. Accent colors charts and progress; highlights color selections and interaction states with theme-aware contrast. Highlights follow the accent unless a separate color is saved. Favorites support folders and zero to three configurable rows; fresh installs start with two, with the second using frequent sites when available. Hover over the favorites area (or focus it with the keyboard) to show add, folder and configuration controls. In configuration, edit/remove favorite tiles and folders directly from the simple view, including the bundled Google folder. Removing a folder keeps its links in the main list; removing a favorite deletes that link. An empty row list persists across new tabs and reloads.

**Appearance → Opening view** chooses the preferred layout for newly opened tabs. Opening the protein dashboard or returning to the simple view changes only the current tab. Other open tabs retain their layouts, and the next new tab opens in the saved preferred layout. Choosing an opening layout in Appearance previews it in the tab where it was selected.

**OK** closes Appearance and confirms valid connection/settings changes; X remains available. Many settings apply immediately, while forms retain their explicit Save/Create actions. Appearance also offers **Google search suggestions**, off by default. Enabling it sends typed queries after a short debounce. Disabling it stops suggestion requests; normal Google search remains available. The suggestion endpoint is not a guaranteed public API, so failures silently fall back to ordinary search.

The greeting follows the device's local clock: morning from 05:00, afternoon from 12:00, evening from 18:00 and night from 22:00 until 05:00. It updates while the tab stays open.

Weather attempts browser location once, then asks for a city if detection fails or is declined. It has no preset city; choices persist locally. Device coordinates are rounded to two decimal places. A cached browser-side Photon/OpenStreetMap lookup adds the city to the label, for example **Current location - Geneva**; older unnamed device locations are resolved too. If naming fails, **Current location** and its forecast remain usable. Click the location label to change city or retry detection. Forecast coordinates go to Open-Meteo; rounded device coordinates also go to Photon for city naming, never to volunteer peers. Forecasts are cached and offer configurable multi-day expansion. The compact card shows available wind, humidity, daily rain chance and local sunrise/sunset times. Missing readings are omitted. Expanded forecasts leave space between the low temperatures and footer. [Weather fields](https://open-meteo.com/en/docs). Chromium requires a declared location permission for extension pages. [Chrome location behavior](https://developer.chrome.com/docs/extensions/how-to/web-platform/geolocation), [Photon service](https://github.com/komoot/photon).

Calendar supports local events and optional Google Calendar integration after OAuth configuration. The simple-view tiles use shared row heights and a dense responsive grid: the protein stays first, while weather, calendar, queue and Pomodoro can be moved, resized or hidden.

Use the **gear in the calendar widget's top toolbar**, beside move, resize and hide, to enable Gregorian, Shamsi (Persian solar), or Qamari (Hijri lunar) calendars. Choose **One calendar** to place their dates together, with a primary calendar controlling the month and navigation, or **Separate widgets** for independent native months. Alternate day numbers share one line in the order shown by the legend, keeping date cells the same height with one, two or three calendars. Press **OK** to apply. These controls stay in the calendar widget; Appearance and computation settings do not contain them.

Qamari offers **Civil (tabular)** and **Umm al-Qura** calculations. These are calculated calendars, so a local moon-sighting date may differ. Conversion uses the browser's `Intl.DateTimeFormat` calendar support, without a service or installation. Local notes and Google events remain tied to the same civil date in every view. Event editors label their date fields Gregorian and show the equivalent enabled dates. Google event queries cover the displayed native month, including both Gregorian months when needed.

Click the Pomodoro minutes or seconds to edit hours, minutes and seconds directly; save with the tick or start immediately. Zero hours are omitted from the countdown. A shared browser deadline survives hiding the widget or opening the dashboard. A progress ring appears around the tab favicon, and one two-note chime plays at completion across open tabs after Start/Resume unlocks browser audio. Reloading an already-completed timer does not replay the chime. Sound depends on the browser permitting audio and at least one audio-enabled RoTab remaining open. [Chrome audio policy](https://developer.chrome.com/blog/autoplay/).

The protein-style Pomodoro is a timer visualization; it must not be counted as a scientific model or volunteer contribution. These widgets do not change Rosetta's methods.

## Connectivity troubleshooting

Use the same network protocol/build, room and at least one shared reachable relay. Distinguish relay connection from direct WebRTC connection and scientific engine initialization. Different networks can fail to establish a direct route; [the network page](network.md) explains STUN/TURN and what remains to be tested. The last RoTab's closure stops browser calculation rather than leaving an installed daemon running.
