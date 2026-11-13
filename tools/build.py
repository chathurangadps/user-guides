#!/usr/bin/env python3
"""Build registered modules, the guide directory and compatibility links."""
from pathlib import Path
import html
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'docs'


def redirect(title, target):
    # Keep chapter bookmarks when a guide moves or a module's latest version changes.
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + html.escape(title) + '</title>'
            '<script>location.replace(' + json.dumps(target) + '+location.search+location.hash);</script>'
            '<noscript><meta http-equiv="refresh" content="0;url=' + html.escape(target, quote=True) + '"></noscript>'
            '</head><body><p><a href="' + html.escape(target, quote=True) + '">'
            + html.escape(title) + '</a></p></body></html>\n')


modules = json.loads((ROOT / 'modules.json').read_text())['modules']
cards = []
catalog = []
for module in modules:
    slug = module['id']
    source = ROOT / 'modules' / slug
    destination = SITE / 'modules' / slug
    subprocess.run([sys.executable, str(source / 'tools/build.py')], check=True)
    editions = json.loads((destination / 'versions.json').read_text())
    latest = editions['current']
    (destination / 'index.html').write_text(redirect(
        'Open ' + module['title'] + ' guide v' + latest,
        'versions/v' + latest + '/index.html'))
    (source / 'OPEN-GUIDE.html').write_text(redirect(
        'Open ' + module['title'] + ' guide', '../../docs/modules/' + slug + '/index.html'))
    href = 'modules/' + slug + '/'
    versions = ' · '.join('<a href="' + href + 'versions/v' + html.escape(v['version'])
                          + '/index.html">v' + html.escape(v['version']) + '</a>'
                          for v in editions['versions'])
    cards.append('<article><p class="eyebrow">Latest edition · v' + html.escape(latest)
                 + '</p><h2>' + html.escape(module['title']) + '</h2><p>'
                 + html.escape(module['description']) + '</p><div class="actions"><a class="primary" href="'
                 + href + '">Open guide</a><a href="' + href + 'versions/">Version history</a></div>'
                 + '<p class="versions">Available editions: ' + versions + '</p></article>')
    catalog.append({**module, 'current': latest, 'path': href,
                    'versions': href + 'versions.json'})

style = '''
:root{color-scheme:light;--ink:#242b3b;--accent:#63428c;--line:#dfe1e9}
*{box-sizing:border-box}body{margin:0;background:#f7f8fc;color:var(--ink);font:16px/1.6 system-ui,-apple-system,sans-serif}
header{background:#2f2244;color:white;padding:24px max(24px,calc((100vw - 1100px)/2))}header strong{display:block;letter-spacing:.05em}header small{opacity:.8}
main{max-width:1150px;margin:auto;padding:40px 24px}h1{font-size:clamp(28px,4vw,42px);line-height:1.15;margin:0 0 16px}h2{font-size:25px;margin:0 0 12px}
.lead{max-width:750px;color:#535d6c;margin-bottom:32px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:24px}
article{background:white;border:1px solid var(--line);border-radius:12px;padding:28px}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.06em;font-size:12px;font-weight:750}
a{color:var(--accent);text-underline-offset:3px}a:focus-visible{outline:3px solid #a889c5;outline-offset:4px}.actions{display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin:24px 0}
.primary{background:var(--accent);color:white;padding:10px 18px;border-radius:6px;text-decoration:none;font-weight:650}.versions{border-top:1px solid var(--line);padding-top:18px;margin-bottom:0}
footer{color:#667080;font-size:14px;margin-top:36px}.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;background:white;padding:8px}
'''
(SITE / 'index.html').write_text(
    '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="robots" content="noindex,nofollow"><title>SLERPTECH User Guides</title><style>' + style + '</style></head>'
    '<body><a class="skip" href="#main">Skip to guides</a><header><strong>SLERPTECH</strong><small>iDempiere 13 · User documentation</small></header>'
    '<main id="main"><h1>User guides</h1><p class="lead">Choose a module, then open its latest guide or an earlier edition that matches your installed release.</p>'
    '<section class="cards" aria-label="Available modules">' + ''.join(cards) + '</section>'
    '<footer>Each module keeps its own version history, instructions and screenshots.</footer></main></body></html>\n')
(SITE / 'modules.json').write_text(json.dumps({'modules': catalog}, indent=2) + '\n')
(SITE / '.nojekyll').touch()
(ROOT / 'OPEN-GUIDE.html').write_text(redirect('Open SLERPTECH user guides', 'docs/index.html'))

# Previously shared Time & Attendance URLs remain small redirects, not duplicate guides.
attendance = SITE / 'modules/time-attendance'
if attendance.exists():
    editions = json.loads((attendance / 'versions.json').read_text())
    legacy = SITE / 'versions'
    legacy.mkdir(exist_ok=True)
    (legacy / 'index.html').write_text(redirect(
        'Time & Attendance guide editions', '../modules/time-attendance/versions/index.html'))
    for edition in editions['versions']:
        version = edition['version']
        old = legacy / ('v' + version)
        old.mkdir(exist_ok=True)
        (old / 'index.html').write_text(redirect(
            'Time & Attendance guide v' + version,
            '../../modules/time-attendance/versions/v' + version + '/index.html'))
    (SITE / 'versions.json').write_text(json.dumps({
        'module': 'time-attendance', 'current': editions['current'],
        'versions': [{**v, 'path': 'modules/time-attendance/' + v['path']}
                     for v in editions['versions']]
    }, indent=2) + '\n')
print('Built module directory, module entry links and legacy URL redirects.')
