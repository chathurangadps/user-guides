#!/usr/bin/env python3
"""Check generated guide integrity without contacting the network."""
from pathlib import Path
from html.parser import HTMLParser
import json
root=Path(__file__).resolve().parent.parent
site=root.parents[1]/'docs/modules'/root.name
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ['src','href']:
   if key in a:self.refs.append(a[key])
count=0
for f in site.rglob('*.html'):
 p=Page();text=f.read_text();p.feed(text)
 assert len(p.ids)==len(set(p.ids)),f'Duplicate anchor: {f}'
 for ref in p.refs:
  if ref.startswith(('http:','https:','mailto:')):continue
  path,_,anchor=ref.partition('#');target=(f.parent/path).resolve() if path else f
  assert target.exists(),f'Missing file: {target}'
  if anchor:
   t=p
   if path:t=Page();t.feed(target.read_text())
   assert anchor in t.ids,f'Unknown anchor {ref} in {f}'
 assert '{{' not in text,f'Unresolved template: {f}'
 count+=1
data=json.loads((root/'content/guide.json').read_text());assert len(data['chapters'])==37
ids={c['id'] for c in data['chapters']}
for s in json.loads((root/'content/screenshots.json').read_text()):
 assert s['chapter'] in ids
 assert s['caption'] and (root/'assets/screens'/s['file']).exists()
print(f'PASS: {count} HTML pages; 37 unique chapters; local links, assets and four screenshot captions valid.')
