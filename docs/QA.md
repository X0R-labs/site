# Redesign verification — 5 November 2026

Static site, checked with Playwright 1.64.1 / Chromium 156 (headless Linux), DPR 1,
900px viewport height. QA dependencies do not ship to visitors. Physical iPhone
Safari and an assistive-technology/screen-reader audit are not completed.

## Changes verified locally

The original handoff responsive utility passed at 320, 375, 390, 430, 768 and
1280 CSS pixels. The tracked [extended checks](../qa/check_site.py) also passed
at those widths, including:

- No document/element horizontal overflow, missing anchors, unloaded images or
  contact-card clipping. All four public assets return HTTP 200.
- Both operator configurations, replay animation, exact status/reason/counter values and synthetic
  answer indication. Native radio click and arrow-key operation, polite live status.
- Mobile navigation open/link-close/Escape-close, focus return, skip-link focus,
  keyboard FAQ operation, expected CTA targets and no contact form. The review
  CTA lands below the sticky navigation rather than under it.
- JavaScript-disabled layout/navigation/FAQ/contact and both outcomes in a static
  fallback; reduced motion disables the animation without disabling the demo.
- Pause/resume and offscreen animation pausing. A synthetic visibility-change
  event checks the hidden-tab handler; it is not an OS-level background-tab test.
- No console errors or uncaught page exceptions observed.

Axe-core 4.14.0 WCAG A/AA through 2.2: **zero reported violations at all six
widths**. Some contrast checks are incomplete (SVG labels, decorative symbols
and selected text) and require human review. Screenshot review and sRGB contrast spot checks were completed for body text,
controls and illustration labels; the unchanged report note pair is 6.63:1. This is scoped
QA evidence, not a claim of accessibility certification or complete WCAG conformance.
Visible keyboard focus was checked; native semantics were inspected, but screen
reader announcements have not been manually audited.

Metadata and source checks passed: unique IDs, local asset/fragment targets,
canonical, Open Graph image/URL and Organization JSON-LD under `/site/`.
The three pinned Core document targets were verified through GitHub's contents
API. GitHub and LinkedIn are the only outbound destinations in page links; the
LinkedIn route is the existing project contact, with no newly invented address.
The favicon/logo and social image are unchanged. No private GTM material was copied.

## Measured performance — local preview

Single unthrottled observations on this shared host, before interaction and
before axe injection; these are **not Lighthouse scores, field metrics or
cross-device performance guarantees**. Fresh browser contexts; system fonts.

| Width | Load event (ms) | Observed LCP (ms) | Observed CLS | Transferred bytes |
| --- | ---: | ---: | ---: | ---: |
| 320 | 109.1 | 292 | 0.0000 | 78,808 |
| 375 | 100.3 | 224 | 0.0000 | 78,808 |
| 390 | 85.0 | 196 | 0.0000 | 78,808 |
| 430 | 96.0 | 212 | 0.0000 | 78,808 |
| 768 | 255.6 | 300 | 0.0000 | 78,808 |
| 1280 | 103.0 | 292 | 0.0000 | 78,808 |

The initial document fetches three same-origin resources (CSS, JavaScript, SVG).
No third-party font, analytics or API requests. Long tasks were observed and
are retained in the raw results; a single local load does not establish smoothness
on low-end hardware. Hero movement uses a transform for three short cycles,
with visibility/reduced-motion guards; no canvas, render loop or framework.

Raw evidence: [local results](qa/local-results.json),
[supplemental checks](qa/local-supplemental.json).

## Screenshots reviewed

Before full-page images are from the pre-redesign live site.
[Previous desktop hero](qa/previous-hero-1280.png) and
[previous mobile hero](qa/previous-hero-390.png) show the first redesign before
this hierarchy/diagram refinement. After images are from
this local redesign. Hero, demo (denied/permitted), pricing and contact were
inspected at 320 and 1280px; 390px captures and full pages are retained below. Hero viewports are captured
before interaction; full-page composite captures make the header non-sticky
only during capture to avoid a repeated header artifact. Actual sticky-header
behavior is checked separately.

| View | Before | After |
| --- | --- | --- |
| Desktop, 1280 | [Full page](qa/before-1280.png) | [Full page](qa/after-1280.png) / [Hero](qa/hero-1280.png) |
| Mobile, 390 | [Full page](qa/before-390.png) | [Full page](qa/after-390.png) / [Hero](qa/hero-390.png) |
| Demo, denied | — | [Desktop](qa/demo-1280.png) / [Mobile](qa/demo-390.png) |
| Demo, permitted | — | [Desktop](qa/demo-permitted-1280.png) / [Mobile](qa/demo-permitted-390.png) |
| Pricing | — | [Desktop](qa/pricing-1280.png) / [Mobile](qa/pricing-390.png) |
| Contact | — | [Desktop](qa/contact-1280.png) / [Mobile](qa/contact-390.png) |

## Deployment

PR CI, Pages status and post-deployment checks will be recorded in the PR after
publication. Do not infer live verification from these local results.

## Refined motion and diagram evidence

[Silent walkthrough](qa/motion-walkthrough.webm): finite hero request/policy
sequence, pause/resume, permitted/denied transitions and replay. The hero now uses
connected native HTML nodes so its labels do not shrink inside an SVG on mobile.
Demo nodes have explicit edges and state-dependent emphasis. Motion does not
delay semantic results or imply backend execution. The sample report has a brief
one-time entrance; all motion respects the reduced-motion and pause guards.

PR #4 initially deployed successfully with live six-width checks. This refinement
is delivered through PR #5; its final CI/Pages/live results are recorded in that PR.
