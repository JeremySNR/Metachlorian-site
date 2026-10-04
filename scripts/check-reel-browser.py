"""Render and exercise the animated hero in Chromium; save review screenshots."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.tmp/reel-review'
OUT.mkdir(parents=True, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT / 'dist')))
Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}'
errors = []

try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844)]:
            page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(url, wait_until='networkidle')
            page.wait_for_selector('.reel-art[data-ready]')
            page.locator('.hero').screenshot(path=str(OUT / f'{name}-initial.png'))
            button = page.get_by_role('button', name='Pause reel animation')
            button.click()
            page.wait_for_function("document.querySelector('.reel-art').dataset.motion === 'paused'")
            before = page.locator('canvas').evaluate('(c) => c.toDataURL()')
            page.wait_for_timeout(250)
            assert before == page.locator('canvas').evaluate('(c) => c.toDataURL()'), 'Pause must stop drawing'
            page.get_by_role('button', name='Play reel animation').click()
            page.wait_for_timeout(500)
            assert before != page.locator('canvas').evaluate('(c) => c.toDataURL()'), 'Play must advance the reel'
            page.get_by_role('button', name='Pause reel animation').click()
            page.evaluate('window.scrollTo(0, 0)')
            page.locator('.hero').screenshot(path=str(OUT / f'{name}-hero.png'))
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal page overflow'
            page.get_by_role('button', name='Play reel animation').click()
            page.locator('#demo').scroll_into_view_if_needed()
            page.wait_for_function("document.querySelector('.reel-art').dataset.motion === 'paused'")
            page.locator('#hero-query').fill('slow drone coastline')
            page.locator('#hero-search-form').evaluate('(form) => form.requestSubmit()')
            assert page.locator('#shot-results .shot-card').count() > 0, 'Hero search must still return shots'
            assert page.locator('#shot-query').input_value() == 'slow drone coastline'
            page.close()

        page = browser.new_page(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(url, wait_until='networkidle')
        page.wait_for_selector('.reel-art[data-ready]')
        control = page.locator('.reel-control')
        assert control.get_attribute('aria-label') == 'Play reel animation'
        assert control.get_attribute('aria-pressed') == 'true'
        before = page.locator('canvas').evaluate('(c) => c.toDataURL()')
        page.wait_for_timeout(350)
        assert before == page.locator('canvas').evaluate('(c) => c.toDataURL()'), 'Reduced motion must start static'
        control.focus()
        assert control.evaluate('(b) => b.matches(":focus-visible")'), 'Keyboard control must have visible focus'
        page.keyboard.press('Space')
        assert control.get_attribute('aria-pressed') == 'false', 'Explicit play must work from the keyboard'
        page.keyboard.press('Space')
        assert control.get_attribute('aria-pressed') == 'true'
        page.locator('.hero').screenshot(path=str(OUT / 'reduced-motion-hero.png'))
        page.close()

        page = browser.new_page(viewport={'width': 390, 'height': 844}, java_script_enabled=False)
        page.goto(url, wait_until='networkidle')
        assert page.locator('.reel-poster').is_visible(), 'No-JS poster must remain visible'
        assert not page.locator('.reel-control').is_visible(), 'Unavailable control must be hidden'
        page.locator('.hero').screenshot(path=str(OUT / 'no-js-hero.png'))
        page.close()
        browser.close()
    assert not errors, '\n'.join(errors)
    print('PASS: desktop/mobile, animation, pause, offscreen suspension, reduced motion, keyboard, no-JS fallback and hero search')
finally:
    server.shutdown()
