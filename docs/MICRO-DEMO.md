# Four-scene micro demo

A shareable static presentation at `/site/micro-demo.html`, linked from the homepage. Request → operator denial → operator permission → evidence. The browser illustrates the pinned Core deterministic mock results; it does not call Core, a model or an external API. No analytics, storage, fonts, video player or new runtime dependency.

## Interaction and design

Navy/blue composition, native HTML execution nodes, short entrance and packet animations. Manual scene buttons and Previous/Next are always available with JavaScript. Optional Play advances every seven seconds and stops after the fourth scene; Pause stops progression and animation. Changing scenes stops playback. Hidden/offscreen presentation stops playback. Reduced-motion mode removes animation and timed playback; no JavaScript shows all four scenes and working evidence/contact links. No automatic start, audio or looping presentation.

The prominent mock-testing label, experimental status and operator-versus-user/resource limitations remain visible. Public evidence links are pinned to Core commit `8538e2dbb331ce0844837f81959eb3917ec60710`. No private GTM content or pending commercial terms were copied. Prices and existing contact routes are unchanged.

## Verification

Run `python qa/check_micro_demo.py` with the same Playwright setup and URL/output/axe environment variables as [existing QA](QA.md). It runs in CI alongside homepage checks. Local Chromium checks passed 320, 375, 390, 430, 768 and 1280px: four states, exact handler counts, no horizontal overflow, minimum 44px buttons, keyboard activation, play/pause/final stop, reduced motion and JavaScript-disabled fallback. Axe-core 4.14.0 reported zero violations in the checked state at all six widths; this is not a full accessibility audit. Hidden-tab handling is simulated, not an OS-level background-tab test. Physical Safari and manual screen-reader testing remain pending.

Desktop/mobile scene screenshots are retained in [micro-demo evidence](qa/micro-demo/). Deployment and post-deployment results are recorded in the PR; local results alone do not establish a live deployment.
