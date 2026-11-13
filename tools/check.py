#!/usr/bin/env python3
"""Validate the module catalog, version archives and published local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'docs'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.refs = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])


modules = json.loads((ROOT / 'modules.json').read_text())['modules']
catalog = json.loads((SITE / 'modules.json').read_text())['modules']
assert {m['id'] for m in modules} == {m['id'] for m in catalog}
for module in modules:
    slug = module['id']
    subprocess.run([sys.executable, str(ROOT / 'modules' / slug / 'tools/check.py')], check=True)
    destination = SITE / 'modules' / slug
    versions = json.loads((destination / 'versions.json').read_text())
    assert versions['current'] in {v['version'] for v in versions['versions']}
    for version in versions['versions']:
        assert (destination / version['path']).is_file(), version

pages = list(SITE.rglob('*.html'))
pages += [ROOT / 'OPEN-GUIDE.html'] + list((ROOT / 'modules').glob('*/OPEN-GUIDE.html'))
for path in pages:
    assert '{{' not in path.read_text(), path
    page = Page(path)
    assert len(page.ids) == len(set(page.ids)), ('Duplicate ID', path)
    for ref in page.refs:
        parts = urlsplit(ref)
        if parts.scheme or parts.netloc:
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), (path, ref)
        if parts.fragment:
            assert unquote(parts.fragment) in Page(target).ids, (path, ref)
print(f'PASS: {len(modules)} module(s), {len(pages)} HTML pages, version catalog and local links.')
