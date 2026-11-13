#!/usr/bin/env python3
"""Check generated guide integrity without contacting the network."""
from pathlib import Path
from html.parser import HTMLParser
import json
import xml.etree.ElementTree as ET
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
screens=json.loads((root/'content/screenshots.json').read_text())
for s in screens:
 assert s['chapter'] in ids
 assert s['caption'] and (root/'assets/screens'/s['file']).exists()
 assert s['publication'] and s['crop'],f'Missing capture provenance: {s["file"]}'
diagrams=json.loads((root/'content/diagrams.json').read_text())
assert len({d['id'] for d in diagrams})==len(diagrams)
for d in diagrams:
 assert d['chapter'] in ids
 node_ids={n['id'] for n in d['nodes']}
 assert len(node_ids)==len(d['nodes'])
 assert len({(n['col'],n['row']) for n in d['nodes']})==len(d['nodes']),d['id']
 assert all(e['from'] in node_ids and e['to'] in node_ids for e in d['edges'])
 assert d['summary'] and d['steps'] and d['checkpoint']
 svg=ET.parse(root/'assets/diagrams'/d['file']).getroot()
 assert svg.find('{http://www.w3.org/2000/svg}title').text==d['title']
 assert svg.find('{http://www.w3.org/2000/svg}desc').text
 assert not svg.findall('.//{http://www.w3.org/2000/svg}script')
 assert all(0<=n['col']<3 and n['row']>=0 for n in d['nodes'])
latest=site/'versions'/('v'+data['metadata']['guide_version'])
for folder in ['screens','diagrams']:
 for asset in (root/'assets'/folder).iterdir():
  assert asset.read_bytes()==(latest/'assets'/folder/asset.name).read_bytes(),asset
print(f'PASS: {count} HTML pages; 37 chapters; {len(screens)} screenshots; {len(diagrams)} accessible SVG process maps; local links, assets and captions valid.')
