"""Verify committed token exports, actual colour pairs, and exact SVG source bytes."""
from pathlib import Path
import base64
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from build import compile_tokens

ROOT = Path(__file__).resolve().parents[1]
tokens = json.loads((ROOT / 'design-system/tokens.json').read_text())
assert (ROOT / 'dist/foundations.css').read_text() == compile_tokens(), 'Stale generated CSS'

def luminance(value):
    channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return sum(c*w for c, w in zip(linear, (.2126, .7152, .0722)))

def contrast(foreground, background):
    a, b = sorted((luminance(foreground), luminance(background)))
    return (b + .05) / (a + .05)

def colour(group, name):
    return tokens['color'][group][name]['$value']

pairs = [
    ('primary action', colour('neutral', 'white'), colour('brand', 'violet'), 4.5),
    ('primary hover', colour('neutral', 'white'), colour('brand', 'violet-hover'), 4.5),
    ('body text', colour('brand', 'ink'), colour('neutral', 'white'), 4.5),
    ('secondary text', colour('neutral', 'muted'), colour('neutral', 'paper'), 4.5),
    ('secondary on narrative tint', colour('neutral', 'muted'), colour('brand', 'tint'), 4.5),
    ('dark secondary', colour('neutral', 'dark-muted'), colour('neutral', 'dark-panel'), 4.5),
    ('dark violet label', colour('brand', 'violet-on-dark'), colour('neutral', 'dark-panel'), 4.5),
    ('field boundary', '#6e6e6e', colour('neutral', 'white'), 3),
]
for state in ('cleared', 'caution', 'blocked', 'info'):
    pairs.append((state, colour('status', state), colour('status', state+'-bg'), 4.5))
for name, fg, bg, minimum in pairs:
    ratio = contrast(fg, bg)
    assert ratio >= minimum, f'{name}: {ratio:.2f} < {minimum}'
    print(f'PASS: {name}: {ratio:.2f}:1')

master = (ROOT / 'dist/assets/metachlorian-logo.png').read_bytes()
assert hashlib.sha256(master).hexdigest() == '3e96712252f308a84198b706fb5d1ec0c7a0be90663c701a277ecbc872a1f61e', 'The approved logo master changed'
for name in ('metachlorian-logo.svg', 'metachlorian-mark.svg', 'favicon.svg'):
    svg = ET.parse(ROOT / 'dist/assets' / name).getroot()
    image = svg.find('{http://www.w3.org/2000/svg}image')
    data = image.attrib['href']
    assert data.startswith('data:image/png;base64,')
    assert base64.b64decode(data.split(',', 1)[1]) == master, f'{name} changed the approved artwork'
    assert image.attrib['width'] == '2172' and image.attrib['height'] == '724'
    assert len(svg) == 2 and all('filter' not in e.attrib and 'transform' not in e.attrib for e in svg.iter())
    print(f'PASS: {name} embeds the unchanged approved PNG')
assert ET.parse(ROOT / 'dist/assets/metachlorian-logo.svg').getroot().attrib['viewBox'] == '0 0 2172 724'
print('Master SHA-256:', hashlib.sha256(master).hexdigest())

for page in (ROOT / 'dist').rglob('*.html'):
    source = page.read_text()
    for css in ('foundations.css', 'tokens.css', 'styles.css', 'family.css'):
        assert f'href="/{css}"' in source, f'{page}: missing {css}'
    assert source.count('src="/assets/metachlorian-logo.svg"') == 2, f'{page}: inconsistent header/footer identity'
    assert 'href="/assets/favicon.svg"' in source
    assert 'class="brand-mark"' not in source
print('PASS: all three pages use the same SVG identity and profile styles')
