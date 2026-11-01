"""Check crawlable pages, local links and consistent production SEO metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import gzip
import json
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1] / 'dist'
origin = 'https://www.metachlorian.xyz'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.schemas = [], [], [], []
        self.h1 = 0
        self.in_title = self.in_json = False
        self.title = self.jsontext = self.canonical = ''
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            self.meta[a.get('name') or a.get('property')] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href', '')
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag in ('img', 'script') and a.get('src'):
            self.assets.append(a['src'])
        if tag == 'link' and a.get('rel') in ('stylesheet', 'preload'):
            self.assets.append(a['href'])
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_json = True
            self.jsontext = ''

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_json:
            self.jsontext += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.in_json:
            self.schemas.append(json.loads(self.jsontext))
            self.in_json = False

# Verification files at the root are ownership tokens, not indexable site pages.
pages = {}
errors = []
for file in root.rglob('index.html'):
    p = Page()
    source = file.read_text(encoding='utf-8')
    p.feed(source)
    pages[file.resolve()] = p
    if 'metachlorian.jezalexandersmith.chatgpt.site' in source:
        errors.append(f'{file.relative_to(root)}: obsolete production origin')

for file, p in pages.items():
    relative = file.relative_to(root).as_posix()
    expected_url = origin + '/' + relative.removesuffix('index.html')
    requirements = [
        (p.h1 == 1, 'exactly one H1'),
        (bool(p.title.strip()), 'title'),
        (bool(p.meta.get('description')), 'description'),
        (p.canonical == expected_url, 'self-referencing production canonical'),
        (p.meta.get('og:url') == expected_url, 'matching Open Graph URL'),
        (len(p.ids) == len(set(p.ids)), 'unique IDs'),
        (bool(p.schemas), 'structured data'),
        (p.meta.get('twitter:card') == 'summary_large_image', 'large social preview'),
    ]
    for condition, label in requirements:
        if not condition:
            errors.append(f'{relative}: missing/invalid {label}')
    for field in ('og:image', 'twitter:image'):
        image_url = p.meta.get(field, '')
        if not image_url.startswith(origin + '/'):
            errors.append(f'{relative}: missing production {field}')
        else:
            p.assets.append(urlsplit(image_url).path)
    for link in p.links + p.assets:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        path = root / unquote(u.path.lstrip('/')) if u.path.startswith('/') else file.parent / unquote(u.path)
        if not u.path:
            path = file
        if path.is_dir():
            path = path / 'index.html'
        if not path.exists():
            errors.append(f'{relative}: missing {link}')
        elif u.fragment and path.resolve() in pages and unquote(u.fragment) not in pages[path.resolve()].ids:
            errors.append(f'{relative}: missing anchor {link}')

for label, values in [('titles', [p.title for p in pages.values()]), ('descriptions', [p.meta.get('description') for p in pages.values()])]:
    if len(values) != len(set(values)):
        errors.append(f'Site pages must have unique {label}')

tree = ET.parse(root / 'sitemap.xml')
urls = [node.text for node in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
canonicals = [p.canonical for p in pages.values()]
if sorted(urls) != sorted(canonicals):
    errors.append('Sitemap must contain every canonical page exactly once')
robots = (root / 'robots.txt').read_text(encoding='utf-8')
if f'Sitemap: {origin}/sitemap.xml' not in robots or 'Disallow: /' in robots:
    errors.append('robots.txt must allow crawling and point at the production sitemap')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
for filename in ('index.html', 'styles.css', 'app.js'):
    raw = (root / filename).read_bytes()
    print(f'{filename}: {len(raw):,} bytes / {len(gzip.compress(raw)):,} gzip bytes')
print(f'PASS: {len(pages)} pages; local links, assets, anchors, headings, unique metadata, production canonicals, social previews, structured data and sitemap coverage.')
