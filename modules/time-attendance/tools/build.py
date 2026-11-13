#!/usr/bin/env python3
"""Build a dependency-free, offline-capable guide from reviewed chapter content."""
from pathlib import Path
import html,json,re,shutil
from diagrams import render as render_diagram
root=Path(__file__).resolve().parent.parent
site=root.parents[1]/'docs/modules'/root.name
site.mkdir(parents=True,exist_ok=True)
data=json.loads((root/'content/guide.json').read_text())
screens=json.loads((root/'content/screenshots.json').read_text())
diagrams=json.loads((root/'content/diagrams.json').read_text())
(root/'assets/diagrams').mkdir(exist_ok=True)
for diagram in diagrams:render_diagram(diagram,root/'assets/diagrams'/diagram['file'])
m=data['metadata'];chapters=data['chapters'];version=m['guide_version']
def esc(s):return html.escape(str(s),quote=True)
def rich(s):
 return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',esc(s)).replace('\n','<br>')
def block(b):
 k=b['kind']
 if k=='paragraph':return '<p>'+rich(b['text'])+'</p>'
 if k=='heading':return '<h{0}>{1}</h{0}>'.format(min(3,max(2,b['level'])),rich(b['text']))
 if k=='purpose':return '<div class="purpose"><div><strong>Who uses this</strong>'+rich(b['role'])+'</div><div><strong>Outcome</strong>'+rich(b['result'])+'</div></div>'
 if k=='check':return '<div class="check"><strong>Completion check</strong>'+rich(b['text'])+'</div>'
 if k=='list':
  tag='ol' if b['ordered'] else 'ul'
  return '<'+tag+'>'+''.join('<li>'+rich(x)+'</li>' for x in b['items'])+'</'+tag+'>'
 if k=='table':return '<div class="table-wrap" tabindex="0" role="region" aria-label="'+esc('Table: '+', '.join(map(str,b['headers'])))+'"><table><thead><tr>'+''.join('<th scope="col">'+rich(x)+'</th>' for x in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+rich(x)+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
 raise ValueError(k)
def figure(src,title,caption,kind):
 return f'<figure class="{kind}"><a class="visual-media" href="{src}" target="_blank" rel="noopener" aria-label="Enlarge: {esc(title)}"><img loading="lazy" src="{src}" alt="{esc(title)}"></a><figcaption><strong>{esc(title)}</strong>{esc(caption)} <a class="visual-media" href="{src}" target="_blank" rel="noopener" data-title="{esc(title)}">Enlarge {kind}</a></figcaption></figure>'
def process_map(d):
 return '<section class="process-map"><p class="visual-label">Process map</p>'+figure('assets/diagrams/'+d['file'],d['title'],d['summary'],'diagram')+'<ol class="map-steps">'+''.join('<li>'+rich(step)+'</li>' for step in d['steps'])+'</ol><div class="notice">'+rich(d['checkpoint'])+'</div></section>'
def screen_walkthrough(s):
 result=figure('assets/screens/'+s['file'],s['title'],s['caption'],'screenshot')
 if s.get('focus'):
  result+=block({'kind':'table','headers':['Find this control / section','What to check or do'],'rows':[[f['control'],f['explanation']] for f in s['focus']]})
 if s.get('outcome'):result+=block({'kind':'check','text':s['outcome']})
 return '<section class="screen-walkthrough">'+result+'</section>'
toc='<li><a href="#home"><span>⌂</span>Guide home</a></li>'+''.join(f'<li><a href="#{c["id"]}"><span>{i:02}</span>{esc(c["title"])}</a></li>' for i,c in enumerate(chapters,1))
body=[]
for i,c in enumerate(chapters):
 images=''.join(screen_walkthrough(s) for s in screens if s['chapter']==c['id'])
 maps=''.join(process_map(d) for d in diagrams if d['chapter']==c['id'])
 purpose=''.join(block(b) for b in c['blocks'] if b['kind']=='purpose')
 instructions=''.join(block(b) for b in c['blocks'] if b['kind']!='purpose')
 nav='<nav class="chapter-nav" aria-label="Chapter navigation">'
 nav+=f'<a href="#{chapters[i-1]["id"]}"><small>Previous</small>{esc(chapters[i-1]["title"])}</a>' if i else '<a href="#home"><small>Previous</small>Guide home</a>'
 nav+=f'<a href="#{chapters[i+1]["id"]}"><small>Next</small>{esc(chapters[i+1]["title"])}</a>' if i+1<len(chapters) else '<a href="#home"><small>Finished</small>Back to guide home</a>'
 body.append(f'<article class="chapter" id="{c["id"]}" data-title="{esc(c["title"])}"><p class="eyebrow">Chapter {i+1:02} / {len(chapters)}</p><h1>{esc(c["title"])}</h1>'+purpose+maps+(f'<h2>On-screen walkthrough</h2>{images}' if images else '')+('<h2>Operating instructions</h2>' if maps or images else '')+instructions+nav+'</nav></article>')
visual_index='<div class="visual-catalog"><section><h3>Follow a process</h3><ul>'+''.join(f'<li><a href="#{d["chapter"]}">{esc(d["title"])}</a></li>' for d in diagrams)+'</ul></section><section><h3>Explore the screens</h3><ul>'+''.join(f'<li><a href="#{c["id"]}">{esc(c["title"])}</a></li>' for c in chapters if any(s['chapter']==c['id'] for s in screens))+'</ul></section></div>'
versions=[]
for record in (site/'versions').glob('v*/metadata.json'):
 prior=json.loads(record.read_text())
 if prior['version']!=version:versions.append(prior)
versions.append({'version':version,'path':'versions/v'+version+'/index.html','date':m['date'],'plugin':m['plugin_version'],'dictionary':m['dictionary_version'],'status':m['status'],'screenshots':len(screens),'process_diagrams':len(diagrams)})
versions.sort(key=lambda x:tuple(int(n) for n in x['version'].split('.')),reverse=True)
version_options=''.join('<option value="../v'+esc(v['version'])+'/index.html"'+(' selected' if v['version']==version else '')+'>v'+esc(v['version'])+'</option>' for v in versions)
template=(root/'content/template.html').read_text()
values={'VERSION':version,'VERSION_OPTIONS':version_options,'STATUS':esc(m['status']),'DATE':m['date'],'PLUGIN':m['plugin_version'],'PACKIN':m['dictionary_version'],'COMPANY_PACKIN':m['company_packin_version'],'TOC':toc,'BODY':'\n'.join(body),'CHANGES':''.join('<li>'+esc(x)+'</li>' for x in m['changes']),'CHAPTER_COUNT':str(len(chapters))}
values.update({'VISUAL_INDEX':visual_index,'SCREEN_COUNT':str(len(screens)),'DIAGRAM_COUNT':str(len(diagrams))})
for key,value in values.items():template=template.replace('{{'+key+'}}',value)
if re.search(r'\{\{\w+\}\}',template):raise ValueError('Unresolved template placeholder')
dest=site/'versions'/('v'+version);dest.mkdir(parents=True,exist_ok=True)
(dest/'index.html').write_text(template)
shutil.copytree(root/'assets',dest/'assets',dirs_exist_ok=True)
shutil.copytree(root/'assets',site/'assets',dirs_exist_ok=True)
(site/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SLERPTECH User Guide</title><meta http-equiv="refresh" content="0;url=versions/v{version}/index.html"></head><body><p><a href="versions/v{version}/index.html">Open SLERPTECH Time &amp; Attendance Guide v{version}</a></p></body></html>')
(dest/'metadata.json').write_text(json.dumps(next(v for v in versions if v['version']==version),indent=2)+'\n')
(site/'versions.json').write_text(json.dumps({'current':version,'versions':versions},indent=2)+'\n')
edition_rows=''.join('<tr><td><a href="v'+esc(v['version'])+'/index.html">v'+esc(v['version'])+'</a>'+(' — latest' if v['version']==version else '')+'</td><td>'+esc(v['date'])+'</td><td>'+esc(v['plugin'])+'</td><td>'+esc(v['dictionary'])+'</td></tr>' for v in versions)
(site/'versions/index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>SLERPTECH Guide Editions</title><link rel="stylesheet" href="../assets/guide.css"></head><body><main style="margin:0 auto;max-width:1100px;padding:32px"><p class="eyebrow">SLERPTECH · iDempiere 13</p><h1>Time &amp; Attendance guide editions</h1><p><a href="../../../index.html">All modules</a> · <a href="../index.html">Open the latest edition</a>. Choose an earlier edition to match the instructions to your installed release.</p><div class="table-wrap"><table><thead><tr><th>Guide</th><th>Published</th><th>Plugin</th><th>Dictionary Pack In</th></tr></thead><tbody>'+edition_rows+'</tbody></table></div><p>Each edition retains its own HTML, styles and cropped screenshots.</p></main></body></html>')
(site/'.nojekyll').touch()
print(f'Built {len(chapters)} chapters, {len(screens)} screens, {len(diagrams)} process diagrams: {dest}/index.html')
