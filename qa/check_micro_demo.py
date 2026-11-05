"""Check four-scene illustration; no backend calls or real model testing."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('X0R_QA_URL', 'https://x0r-labs.github.io/site/')
OUT = Path(os.environ.get('QA_OUT', '/tmp/x0r-micro-qa'))
OUT.mkdir(parents=True, exist_ok=True)
reports = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in (320, 375, 390, 430, 768, 1280):
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        response = page.goto(BASE + 'micro-demo.html')
        assert response.status == 200
        for scene in range(4):
            page.locator('[data-scene]').nth(scene).click()
            assert page.locator('.scene:visible').count() == 1
            assert page.locator(f'#scene-{scene+1}').is_visible()
            assert page.locator('[aria-current=true]').count() == 1
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert page.locator('button:visible').evaluate_all('es=>es.every(e=>e.getBoundingClientRect().height>=44)')
            assert page.locator('h1,p,button,a,code,.apparatus').evaluate_all('es=>es.filter(e=>e.getBoundingClientRect().width).every(e=>{const r=e.getBoundingClientRect();return r.left>=-1&&r.right<=innerWidth+1})')
            if width in (390, 1280):
                page.wait_for_timeout(600)
                page.screenshot(path=str(OUT / f'scene-{scene+1}-{width}.png'), full_page=True)
        page.get_by_role('button', name='Scene 2: Operator denied').click()
        assert '0 handler entries' in page.locator('.scene:visible').inner_text()
        page.get_by_role('button', name='Next', exact=True).focus()
        page.keyboard.press('Enter')
        assert '1 handler entry' in page.locator('.scene:visible').inner_text()
        page.clock.install()
        page.get_by_role('button', name='Play walkthrough').click()
        page.clock.fast_forward(7100)
        assert page.locator('#scene-4').is_visible()
        page.clock.fast_forward(7100)
        assert page.locator('#play').get_attribute('aria-pressed') == 'false'
        page.get_by_role('button', name='Play walkthrough').click()
        assert page.locator('#scene-1').is_visible()
        page.get_by_role('button', name='Pause walkthrough').click()
        page.clock.fast_forward(8000)
        assert page.locator('#scene-1').is_visible()
        # Hidden-tab handling is simulated, not an OS-level background-tab test.
        page.get_by_role('button', name='Play walkthrough').click()
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
        assert page.locator('#play').get_attribute('aria-pressed') == 'false'
        assert not page.locator('.deck').evaluate("e=>e.classList.contains('motion-enabled')")
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'))")
        page.get_by_role('button', name='Scene 1: The request').click()
        assert not errors, errors
        page.clock.resume()
        axe = os.environ.get('AXE_PATH')
        if axe:
            page.add_script_tag(path=axe)
            violations = page.evaluate("async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})).violations")
            assert not violations, violations
        reports.append({'width': width, 'fourScenes': 'passed', 'keyboard': 'passed', 'playPauseEnd': 'passed', 'consoleErrors': errors})
        page.close()
    page = browser.new_page(reduced_motion='reduce')
    page.goto(BASE + 'micro-demo.html')
    assert page.locator('#play').is_hidden()
    page.get_by_role('button', name='Scene 3: Operator permitted').click()
    assert '1 handler entry' in page.locator('.scene:visible').inner_text()
    assert page.locator('.scene:visible .scene-copy').evaluate('e=>getComputedStyle(e).animationName') == 'none'
    page.close()
    page = browser.new_page(java_script_enabled=False, viewport={'width':320,'height':900})
    page.goto(BASE + 'micro-demo.html')
    assert page.locator('.scene:visible').count() == 4
    assert page.locator('.deck-controls').is_hidden()
    assert page.evaluate('document.documentElement.scrollWidth==innerWidth')
    assert page.get_by_role('link', name='Inspect the sample review').is_visible()
    browser.close()
(OUT / 'micro-results.json').write_text(json.dumps({'responsive':reports,'reducedMotion':'passed','noJavaScript':'passed'}, indent=2))
print('PASS: six widths, four scenes, keyboard, playback, reduced motion and no-JS fallback')
