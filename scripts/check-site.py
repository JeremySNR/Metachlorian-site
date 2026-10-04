from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,sys,gzip,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.links=[];self.assets=[];self.h1=0;self.title=False;self.description=False;self.canonical=False;self.json=False;self.jsontext='';self.schemas=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
  if tag=='link' and a.get('rel')=='canonical':self.canonical=bool(a.get('href'))
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ('img','script') and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('rel') in ('stylesheet','preload'):self.assets.append(a['href'])
  if tag=='script' and a.get('type')=='application/ld+json':self.json=True;self.jsontext=''
 def handle_data(self,data):
  if self.json:self.jsontext+=data
 def handle_endtag(self,tag):
  if tag=='script' and self.json:self.schemas.append(json.loads(self.jsontext));self.json=False
pages={}
for file in root.rglob('*.html'):
 p=Page();p.feed(file.read_text());pages[file.resolve()]=p
errors=[]
for file,p in pages.items():
 for condition,label in [(p.h1==1,'exactly one H1'),(p.title,'title'),(p.description,'description'),(p.canonical,'canonical URL'),(len(p.ids)==len(set(p.ids)),'unique IDs'),(bool(p.schemas),'structured data')]:
  if not condition:errors.append(f'{file.relative_to(root)}: missing/invalid {label}')
 for link in p.links+p.assets:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  path=root/unquote(u.path.lstrip('/')) if u.path.startswith('/') else file.parent/unquote(u.path)
  if not u.path:path=file
  if path.is_dir():path=path/'index.html'
  if not path.exists():errors.append(f'{file.relative_to(root)}: missing {link}')
  elif u.fragment and path.resolve() in pages and unquote(u.fragment) not in pages[path.resolve()].ids:errors.append(f'{file.relative_to(root)}: missing anchor {link}')
ET.parse(root/'sitemap.xml')
if errors:print('\n'.join(errors));sys.exit(1)
for filename in ('index.html','styles.css','app.js'):
 raw=(root/filename).read_bytes();print(f'{filename}: {len(raw):,} bytes / {len(gzip.compress(raw)):,} gzip bytes')
print(f'PASS: {len(pages)} pages; local links, assets, anchors, unique IDs, headings, metadata, structured data and sitemap.')
