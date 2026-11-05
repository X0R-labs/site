#!/usr/bin/env python3
"""Responsive regression checks extended from the local launch QA utility.

Install Playwright separately. Output stays outside the site unless QA_OUT is set.
AXE_PATH optionally enables axe-core WCAG 2.2 AA checks from a local script.
"""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get('X0R_QA_URL', 'https://x0r-labs.github.io/site/')
OUT = Path(os.environ.get('QA_OUT', '/tmp/x0r-site-qa'))
OUT.mkdir(parents=True, exist_ok=True)
AXE = os.environ.get('AXE_PATH')
reports = []
GEOMETRY = '''() => {
 const overflow = [...document.querySelectorAll('h1,h2,h3,p,a,button,summary,fieldset,code,.demo,.report-preview')]
  .filter(e => e.getBoundingClientRect().width && getComputedStyle(e).position !== 'fixed')
  .filter(e => {const r=e.getBoundingClientRect();return r.left < -1 || r.right > innerWidth+1})
  .map(e=>e.tagName+'.'+e.className);
 return {width:innerWidth, documentWidth:document.documentElement.scrollWidth,overflow,
  missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).length,
  unloadedImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
  clippedContact:[...document.querySelectorAll('.cta > *, .cta .btn')].filter(e=>{
    const b=e.getBoundingClientRect(),c=e.closest('.cta').getBoundingClientRect();
    return b.left<c.left-1||b.right>c.right+1||e.scrollWidth>e.clientWidth+1;
  }).length};
}'''
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in (320, 375, 390, 430, 768, 1280):
        context = browser.new_context(viewport={'width': width, 'height': 900},
                                      is_mobile=width <= 430, has_touch=width <= 430,
                                      device_scale_factor=1)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.add_init_script('''window.metrics={lcp:0,cls:0,longTasks:[]};
          new PerformanceObserver(l=>l.getEntries().forEach(e=>metrics.lcp=e.startTime)).observe({type:'largest-contentful-paint',buffered:true});
          new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)metrics.cls+=e.value})).observe({type:'layout-shift',buffered:true});
          new PerformanceObserver(l=>l.getEntries().forEach(e=>metrics.longTasks.push(e.duration))).observe({type:'longtask',buffered:true});''')
        response = page.goto(URL, wait_until='networkidle')
        assert response and response.status == 200
        page.evaluate('document.fonts.ready')
        report = page.evaluate(GEOMETRY)
        assert report['width'] == width and report['documentWidth'] == width, report
        assert not report['overflow'], report
        assert not report['missingAnchors'] and not report['unloadedImages'], report
        assert report['clippedContact'] == 0
        report['performance'] = page.evaluate('''() => {
          const n=performance.getEntriesByType('navigation')[0];
          const r=performance.getEntriesByType('resource');
          return {domContentLoadedMs:n.domContentLoadedEventEnd,loadMs:n.loadEventEnd,
            lcpMs:metrics.lcp,cls:metrics.cls,longTasks:metrics.longTasks,
            transferredBytes:n.transferSize+r.reduce((s,e)=>s+e.transferSize,0),
            resourceCount:r.length,resourceOrigins:[...new Set(r.map(e=>new URL(e.name).origin))]};
        }''')
        assert report['performance']['resourceOrigins'] == [page.evaluate('location.origin')]
        page.keyboard.press('Tab')
        assert page.get_by_role('link',name='Skip to content').evaluate('e=>document.activeElement===e')
        page.keyboard.press('Enter')
        assert page.locator('#main').evaluate('e=>document.activeElement===e')
        assert page.locator('h1').count() == 1
        assert page.locator('link[rel=canonical]').get_attribute('href') == 'https://x0r-labs.github.io/site/'
        assert page.get_by_role('heading', name='Agents act. Boundaries matter.').is_visible()
        for price in ('$350', '$1,000', '$250'):
            assert price in page.locator('#services').inner_text()
        # Every shipped asset is fetched under the same base path, including /site/ live.
        for asset in ('favicon.svg', 'styles.css', 'site.js', 'social-preview.png'):
            assert context.request.get(URL + asset).status == 200, asset
        toggle = page.get_by_role('button', name='Toggle menu', exact=True)
        nav = page.get_by_role('navigation', name='Main', exact=True)
        if width <= 960:
            assert toggle.is_visible()
            toggle.click()
            assert toggle.get_attribute('aria-expanded') == 'true'
            nav.get_by_role('link', name='Services & pricing', exact=True).click()
            assert toggle.get_attribute('aria-expanded') == 'false'
            toggle.click()
            page.keyboard.press('Escape')
            assert toggle.get_attribute('aria-expanded') == 'false'
            assert toggle.evaluate('e=>document.activeElement===e')
        else:
            assert not toggle.is_visible() and nav.is_visible()
        denied = page.get_by_role('radio', name='Denied', exact=True)
        permitted = page.get_by_role('radio', name='Permitted', exact=True)
        denied.focus()
        page.keyboard.press('ArrowRight')
        assert permitted.is_checked()
        assert page.locator('.demo').get_attribute('data-state') == 'permitted'
        assert page.locator('#entry-count').inner_text() == '1'
        assert page.locator('#status-badge').inner_text() == 'succeeded'
        assert page.locator('#decision-reason').inner_text() == 'granted'
        assert '24 months' in page.locator('#handler-detail').inner_text()
        page.keyboard.press('ArrowLeft')
        assert denied.is_checked()
        assert page.locator('#entry-count').inner_text() == '0'
        assert page.locator('#status-badge').inner_text() == 'blocked'
        assert page.locator('#decision-reason').inner_text() == 'not_granted_by_operator'
        assert 'not_granted' in page.locator('#decision-reason').inner_text()
        assert page.locator('.demo-result').get_attribute('aria-live') == 'polite'
        faq = page.get_by_text('What does the $350 review include?', exact=True)
        faq.focus()
        page.keyboard.press('Enter')
        assert faq.evaluate('e=>e.closest("details").open')
        assert page.get_by_role('link', name='Start a conversation on LinkedIn').get_attribute('href') == 'https://www.linkedin.com/company/x0r-labs/'
        assert page.locator('form').count() == 0
        # Browser viewport screenshot plus section crops for direct visual inspection.
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(OUT / f'after-{width}.png'), full_page=True)
        if width in (320, 390, 1280):
            page.screenshot(path=str(OUT / f'hero-{width}.png'))
            for name, selector in [('demo','.demo'), ('pricing','.review-intro'), ('contact','.cta')]:
                page.locator(selector).screenshot(path=str(OUT / f'{name}-{width}.png'))
            permitted.check()
            page.locator('.demo').screenshot(path=str(OUT / f'demo-permitted-{width}.png'))
            denied.check()
        if AXE:
            page.add_script_tag(path=AXE)
            audit = page.evaluate('''async () => {
              const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});
              return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})),
              incomplete:r.incomplete.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),passes:r.passes.length};
            }''')
            report['axe'] = audit
            assert not audit['violations'], audit
        report['consoleErrors'] = errors
        assert not errors, errors
        report.update(sourceURL=URL, requestedWidth=width, keyboard='passed', states='passed', navigation='passed', faq='passed')
        reports.append(report)
        (OUT/'results.json').write_text(json.dumps(reports, indent=2)+'\n')
        print(f'PASS {width}px: layout, assets, states, keyboard, navigation, FAQ, console', flush=True)
        context.close()
    # No JS remains readable, with native navigation, FAQs, and both mock outcomes.
    context = browser.new_context(java_script_enabled=False, viewport={'width':320,'height':900})
    page = context.new_page()
    page.goto(URL, wait_until='networkidle')
    assert page.get_by_role('navigation', name='Main', exact=True).is_visible()
    nojs_geometry = page.evaluate(GEOMETRY)
    assert nojs_geometry['documentWidth'] == 320 and not nojs_geometry['overflow'], nojs_geometry
    assert page.locator('#policy-controls').get_attribute('disabled') is not None
    assert page.get_by_role('radio',name='Permitted',exact=True).is_disabled()
    assert '1 handler entry' in page.locator('.no-script').inner_text()
    assert page.get_by_role('link', name='Start a conversation on LinkedIn').count() == 1
    page.get_by_text('What does the $350 review include?',exact=True).click()
    assert page.locator('#faq details').first.get_attribute('open') is not None
    page.screenshot(path=str(OUT/'no-js-320.png'),full_page=True)
    context.close()
    context = browser.new_context(reduced_motion='reduce', viewport={'width':1280,'height':900})
    page = context.new_page()
    page.goto(URL, wait_until='networkidle')
    assert page.locator('.request-packet').evaluate('e=>getComputedStyle(e).animationName') == 'none'
    assert not page.locator('#motion-toggle').is_visible()
    page.get_by_role('radio',name='Permitted',exact=True).check()
    assert page.locator('#status-badge').inner_text() == 'succeeded'
    context.close()
    context = browser.new_context(viewport={'width':1280,'height':900})
    page = context.new_page()
    page.goto(URL,wait_until='networkidle')
    packet = page.locator('.request-packet')
    assert packet.evaluate('e=>getComputedStyle(e).animationPlayState') == 'running'
    pause = page.locator('#motion-toggle')
    pause.click()
    assert pause.get_attribute('aria-pressed') == 'true'
    assert packet.evaluate('e=>getComputedStyle(e).animationPlayState') == 'paused'
    pause.click()
    page.locator('#contact').scroll_into_view_if_needed()
    page.wait_for_function('document.querySelector(".motion").classList.contains("is-paused")')
    page.evaluate('scrollTo(0,0)')
    page.wait_for_function('!document.querySelector(".motion").classList.contains("is-paused")')
    # Synthetic visibility event tests the hidden-tab pause handler; not OS lifecycle emulation.
    page.evaluate('Object.defineProperty(document,"hidden",{configurable:true,get:()=>true});document.dispatchEvent(new Event("visibilitychange"))')
    assert packet.evaluate('e=>getComputedStyle(e).animationPlayState') == 'paused'
    context.close()
    browser.close()
(OUT/'supplemental.json').write_text(json.dumps({'noJavaScript':'passed','reducedMotion':'passed','motionPause':'passed','offscreenPause':'passed','simulatedHiddenTabPause':'passed','physicalSafari':'not tested'},indent=2)+'\n')
print('PASS: no-JS, reduced-motion, pause, offscreen and simulated hidden-tab checks',flush=True)
