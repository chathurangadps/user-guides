'use strict';
document.body.classList.add('js');
const chapters = [...document.querySelectorAll('.chapter')];
const links = [...document.querySelectorAll('.contents a')];
const home = document.getElementById('home');
const search = document.getElementById('search');
const results = document.getElementById('results');
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menu-toggle');
const textIndex = chapters.map(section => ({id:section.id,title:section.dataset.title,text:[...section.querySelectorAll('h1,h2,h3,p,li,th,td,.purpose,.check,figcaption')].filter(n=>!n.closest('.chapter-nav')).map(n=>n.textContent.trim()).join(' ').replace(/\s+/g,' ')}));
function showHash() {
  const id = decodeURIComponent(location.hash.slice(1));
  const current = chapters.find(c => c.id === id);
  search.value = ''; results.hidden = true;
  document.getElementById('search-status').textContent = '';
  home.hidden = !!current;
  chapters.forEach(c => { c.classList.toggle('active',c === current); });
  links.forEach(a => {a.removeAttribute('aria-current'); if(a.hash === '#' + (current ? current.id : 'home')) a.setAttribute('aria-current','page');});
  document.title = (current ? current.dataset.title + ' | ' : '') + 'SLERPTECH Time & Attendance Guide';
  sidebar.classList.remove('open');menuToggle.setAttribute('aria-expanded','false');
  window.scrollTo(0,0);
}
function searchGuide() {
  const q = search.value.trim();
  if(!q) { showHash(); return; }
  home.hidden=true;chapters.forEach(c=>c.classList.remove('active'));results.hidden=false;
  const tokens=q.toLocaleLowerCase().split(/\s+/);
  const matches=textIndex.filter(c=>tokens.every(t=>(c.title+' '+c.text).toLocaleLowerCase().includes(t)));
  const list=document.getElementById('result-list');list.replaceChildren();
  document.getElementById('search-status').textContent=matches.length+' matching chapters';
  document.getElementById('result-count').textContent=matches.length ? matches.length+' chapters match “'+q+'”. Select a chapter to read the steps.' : 'No matching chapters. Try “roster”, “missing”, “correction” or “payroll”.';
  matches.forEach(c=>{const a=document.createElement('a');a.href='#'+c.id;const b=document.createElement('b');b.textContent=c.title;const small=document.createElement('small');const pos=c.text.toLocaleLowerCase().indexOf(tokens[0]);const start=Math.max(0,pos-45);small.textContent=(start?'…':'')+c.text.slice(start,start+230)+'…';a.append(b,small);a.addEventListener('click',()=>{if(location.hash===a.hash)showHash();});list.append(a);});
}
search.addEventListener('input',searchGuide);
document.getElementById('clear-search').addEventListener('click',()=>{search.value='';showHash();search.focus();});
menuToggle.addEventListener('click',()=>{const open=sidebar.classList.toggle('open');menuToggle.setAttribute('aria-expanded',String(open));});
links.forEach(a=>a.addEventListener('click',()=>{if(location.hash===a.hash)showHash();}));
window.addEventListener('hashchange',showHash);showHash();
document.getElementById('version').addEventListener('change',e=>{location.href=e.target.value+location.hash;});

// Standard links remain usable when dialog support or JavaScript is unavailable.
const imageViewer = document.getElementById('image-viewer');
const imageDetail = document.getElementById('image-detail');
const imageZoom = document.getElementById('image-zoom');
const imageCanvas = imageViewer.querySelector('.image-canvas');
let imageOpener = null;
if (typeof imageViewer.showModal === 'function') {
  document.querySelectorAll('a.visual-media').forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); imageOpener = link;
    const title = link.dataset.title || link.querySelector('img')?.alt || 'Guide image';
    document.getElementById('image-title').textContent = title;
    imageDetail.src = link.href; imageDetail.alt = title;
    document.getElementById('image-original').href = link.href;
    imageCanvas.classList.remove('actual-size'); imageZoom.textContent = 'Actual size'; imageZoom.setAttribute('aria-pressed','false');
    imageViewer.showModal(); imageCanvas.scrollTo(0,0); document.getElementById('image-close').focus();
  }));
  document.getElementById('image-close').addEventListener('click', () => imageViewer.close());
  imageViewer.addEventListener('click', event => { if (event.target === imageViewer) imageViewer.close(); });
  imageViewer.addEventListener('close', () => imageOpener?.focus());
  imageZoom.addEventListener('click', () => {
    const actual = imageCanvas.classList.toggle('actual-size');
    imageZoom.textContent = actual ? 'Fit to window' : 'Actual size';
    imageZoom.setAttribute('aria-pressed', String(actual)); imageCanvas.scrollTo(0,0);
  });
}
