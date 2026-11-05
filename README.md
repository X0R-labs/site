# X0R Labs website

Static HTML, CSS and small JavaScript. No build step, external fonts, analytics,
forms, backend or runtime package dependencies. Hosted at
<https://x0r-labs.github.io/site/> by GitHub Pages from `main` / repository root.
No custom domain is configured by this project.

## Preview

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. Assets are relative to this page so the same files
work under `/site/`. Canonical, Open Graph and structured URLs use the public
Pages address. Preserve the original `favicon.svg` logo proportions and the
existing `social-preview.png`.

## Design and behavior

See [design direction](docs/DESIGN.md). The labeled hero request/policy/outcome diagram uses three brief animation
cycles, a pause control, offscreen/tab visibility pausing and reduced-motion
support. Native HTML labels remain readable on mobile. The demo provides short
state-change animations and a replay button; semantic outcomes update immediately.
A report preview has a one-time entrance. All diagrams are static without JS.

The native radio controls illustrate pinned Core mock-test results; they do not
call a backend. A polite status region announces result changes. Without JS,
navigation, FAQs, contact and source links remain usable, the illustration is
static, and both outcomes are explained in a noscript fallback. No visitor data
is collected or stored.

Public copy must keep experimental/mock evidence separate from client work and
production assurances. Keep pending commercial decisions and private GTM
material out of this repository. Use the verified LinkedIn contact route.

## Verification

Use a separate Python environment for QA tooling (Python 3.11+):

```bash
python3 -m venv /tmp/x0r-site-qa-venv
/tmp/x0r-site-qa-venv/bin/python -m pip install playwright==1.64.1
PLAYWRIGHT_BROWSERS_PATH=/tmp/x0r-playwright /tmp/x0r-site-qa-venv/bin/python -m playwright install chromium
X0R_QA_URL=http://127.0.0.1:8765/ PLAYWRIGHT_BROWSERS_PATH=/tmp/x0r-playwright /tmp/x0r-site-qa-venv/bin/python qa/check_site.py
```

The URL must end with `/`. `QA_OUT` selects a screenshot/JSON output directory;
default `/tmp/x0r-site-qa`. `AXE_PATH` optionally points to a locally installed
axe-core script for WCAG 2.2 AA automated checks. CI uses axe-core 4.14.0.
QA tools are development-only; the website does not load them.

The checks extend the original local launch utility: 320, 375, 390, 430, 768 and
1280px, overflow/contact clipping, assets/anchors, navigation, FAQ, both demo
states, keyboard operation, no-JS, reduced motion, pause behavior, console
errors and browser performance entries. The hidden-tab handler is checked
with a synthetic visibility event, not an OS lifecycle test. Raw timings are
single unthrottled browser observations, not Lighthouse scores or field metrics.

See [verification evidence](docs/QA.md) for actual observations and screenshots.
Physical iPhone Safari and a screen-reader audit remain separate checks.
