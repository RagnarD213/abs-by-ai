'use strict';
const $ = id => document.getElementById(id);
const put = (id, value) => { const node = $(id); if (node) node.textContent = value; };
const date = value => new Date(value + 'T12:00:00Z').toLocaleDateString('en-US', {timeZone:'America/Chicago', weekday:'long', month:'long', day:'numeric'});
const instant = value => new Date(value).toLocaleString('en-US', {timeZone:'America/Chicago', month:'short', day:'numeric', hour:'numeric', minute:'2-digit'}) + ' Central';
const dayOf = value => { const parts = new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date(value)); const part = type => parts.find(p => p.type === type).value; return `${part('year')}-${part('month')}-${part('day')}`; };
const number = value => value === null ? 'Unknown' : new Intl.NumberFormat('en-US',{maximumFractionDigits:2}).format(value);
const dollars = value => value === null ? 'Unknown' : new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(value);
function el(tag, content, className) { const node = document.createElement(tag); if (content !== undefined) node.textContent = content; if (className) node.className = className; return node; }
function link(parent, title, url) { if (!url) return; const a = el('a', title); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; parent.append(a); }
function routineStatus(d) {
  if (!d.routineEnabled || !d.routine) return 'No enabled daily schedule is recorded for this edition.';
  const clock = value => { const [h,m]=value.split(':').map(Number); return `${h%12 || 12}:${String(m).padStart(2,'0')} ${h<12 ? 'AM' : 'PM'}`; };
  const r=d.routine;
  return `Daily updates enabled from ${date(r.startsOn)}. Cloud run starts ${clock(r.startTime)} Central; target ready ${clock(r.readyBy)}. Your Mac must be online. Source availability is shown below. Status confirmed ${instant(r.confirmedAt)}.`;
}
function cards(id, rows, empty) {
  if (!rows.length) return $(id).append(el('p',empty,'note'));
  for (const row of rows) { const box = el('div',undefined,'row'); box.append(el('h3',row.title),el('p',row.detail),el('p',row.source,'note')); link(box,'Review',row.url); $(id).append(box); }
}
function imageProvenance(d) {
  if (!d.image) { put('image-caption','Image date not supplied'); return; }
  const source = '/api/brief/image?sha256=' + d.image.sha256;
  if (dailyImage.getAttribute('src') !== source) {
    $('image-section').hidden = true;
    dailyImage.src = source;
  }
  put('image-caption',`${d.image.forDate === d.forDate ? 'Daily image' : 'Retained image'}: ${date(d.image.forDate)}`);
}
function queue(document) {
  const q = document.socialReleaseQueue;
  if (!q) { $('queue-rows').append(el('p','Scheduled media could not be loaded. Please try again.','note')); return; }
  const days = new Map();
  const first = dayOf(q.windowFrom);
  for (let i=0;i<7;i++) {
    const day = new Date(first + 'T12:00:00Z'); day.setUTCDate(day.getUTCDate()+i);
    const key = day.toISOString().slice(0,10), column = el('section',undefined,'queue-day');
    column.append(el('h3',date(key))); days.set(key,column); $('queue-rows').append(column);
  }
  for (const row of q.rows) {
    const box = el('article',undefined,'row release-card');
    box.append(el('h3',row.title),el('p',`${platformName(row.platform)} · ${instant(row.scheduledAt)}`,'note'));
    preview(box,row.id,row.coverReviewUrl,row.mediaUrl,row.platform,row.coverFrameAt,`${platformName(row.platform)} · ${instant(row.scheduledAt)} · ${row.title}`,row.mediaSource);
    if (row.caption) { const details=el('details');details.append(el('summary','Caption'),el('p',row.caption));box.append(details); }
    const issues = Object.entries(row.preflight).filter(([,v])=>['missing','broken','duplicate','mismatch'].includes(v));
    if (issues.length) box.append(el('p',issues.map(([k])=>({cover:'Check the scheduled cover.',links:'Check a caption link.',duplicates:'Another post is scheduled at this time.',cadence:'Check the release day.',assetMatch:'The scheduled media is unavailable.',description:'Caption is missing.',crop:'Check the cover crop.'}[k] || 'Review this post.')).join(' '),'media-warning'));
    if (!row.mediaUrl && row.reviewUrl?.startsWith('https://studio.youtube.com/')) box.append(el('p','Private video, available in Studio.','note'));
    if (row.reviewUrl?.startsWith('https://studio.youtube.com/')) link(box,'Play in Studio',row.reviewUrl);
    (days.get(dayOf(row.scheduledAt)) || $('queue-rows')).append(box);
  }
  for (const [key,column] of days) if (!q.rows.some(r=>dayOf(r.scheduledAt) === key)) column.append(el('p','No Blotato release observed. Unavailable sources remain unknown.','note'));
}

function platformName(value) { return {facebook:'Facebook',instagram:'Instagram',tiktok:'TikTok',youtube:'YouTube'}[value.toLowerCase()] || value; }
function preview(box,id,cover,video,platform='',coverFrameAt=null,title='Scheduled media',source='scheduled') {
  if (!/^[a-f0-9]{64}$/.test(id || '')) return;
  const media=el('div',undefined,'scheduled-media');
  box.append(media);
  if (cover) {
    const videoCover=!!video || source==='native_private';
    const figure=el('figure',undefined,videoCover ? 'cover-panel' : 'photo-panel');
    const img=el('img');img.src=`/api/brief/media/${id}/cover`;img.alt=videoCover ? 'Scheduled platform cover' : 'Scheduled photo';img.loading='eager';img.className='release-cover';
    const fallback=el('p','This image could not load. Open the scheduled post.','media-warning');fallback.hidden=true;
    img.addEventListener('error',()=>{img.hidden=true;fallback.hidden=false;});
    figure.append(img,el('figcaption',videoCover ? 'Cover' : 'Photo'),fallback);media.append(figure);
    inspectable(img,{type:'image',src:img.src,title:title+(videoCover ? ' · Cover' : ' · Photo')});
  }
  if (!video) return;
  const figure=el('figure',undefined,'video-panel');
  const player=el('video');player.src=`/api/brief/media/${id}/video#t=0.001`;player.controls=false;player.playsInline=true;player.preload='metadata';player.className='release-video';player.hidden=true;
  player.setAttribute('aria-label',`Open scheduled ${platformName(platform)} video`);
  if(cover)player.poster=`/api/brief/media/${id}/cover`;
  const state=el('p','Loading preview…','note');
  const play=el('button','Play video','play-video');play.type='button';play.disabled=true;
  const entry={type:'video',src:player.src,poster:cover ? `/api/brief/media/${id}/cover` : '',title:title+(source==='verified_upload_source' ? ' · Verified upload source' : ' · Video')};
  inspectable(player,entry);
  play.addEventListener('click',()=>openViewer(entry));
  const caption=el('figcaption',source==='verified_upload_source' ? 'Verified upload source' : 'Video');
  figure.append(player,caption,state,play);media.append(figure);
  const duration=()=>`${Math.floor(player.duration/60)}:${String(Math.floor(player.duration%60)).padStart(2,'0')}`;
  player.addEventListener('loadedmetadata',()=>{play.disabled=false;state.textContent=Number.isFinite(player.duration) ? duration() : 'Ready to play';});
  player.addEventListener('loadeddata',()=>{player.hidden=false;});
  player.addEventListener('play',()=>{play.textContent='Pause video';});
  player.addEventListener('pause',()=>{play.textContent='Play video';});
  player.addEventListener('ended',()=>{play.textContent='Play video';});
  player.addEventListener('error',()=>{player.hidden=true;play.hidden=true;state.textContent='This video could not load. Open the original video below.';});
  entry.original=video;
  if (!cover && platform==='tiktok' && coverFrameAt===0) {
    const frame=el('figure',undefined,'cover-panel');
    const canvas=el('canvas');canvas.className='release-cover';canvas.hidden=true;
    const isTikTok=platform==='tiktok' && coverFrameAt===0;
    inspectable(canvas,{type:'frame',canvas,title:title+' · Video frame at 0 seconds'});
    frame.append(canvas,el('figcaption',isTikTok ? 'Cover frame · 0 seconds' : 'Video frame'),el('p',isTikTok ? 'Approval unverified.' : 'Separate cover unavailable.','note'));media.prepend(frame);
    const capture=()=>{if(!player.videoWidth || player.currentTime>0.1)return;try{canvas.width=player.videoWidth;canvas.height=player.videoHeight;canvas.getContext('2d').drawImage(player,0,0);canvas.hidden=false;}catch{}};
    player.addEventListener('loadeddata',capture,{once:true});
  }
}
const gallery=[];
let viewerEntry=null,viewerReturn=null,viewerOverflow='',viewerHistory=false;
function inspectable(node,entry) {
  gallery.push(entry);node.tabIndex=0;node.setAttribute('role','button');node.setAttribute('aria-label','Inspect '+entry.title);node.className += ' inspect-media';
  node.addEventListener('click',()=>openViewer(entry));
  node.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)){e.preventDefault();openViewer(entry);}});
}
function stopViewerMedia() { const v=$('viewer-content').querySelector('video');if(v){v.pause();v.removeAttribute('src');v.load();} }
function renderViewer(entry) {
  stopViewerMedia();viewerEntry=entry;put('viewer-title',entry.title);$('viewer-content').replaceChildren();
  if(entry.type==='video') {
    const v=el('video');v.src=entry.src;v.controls=true;v.playsInline=true;v.preload='auto';v.setAttribute('aria-label','Full size scheduled video');if(entry.poster)v.poster=entry.poster;
    const play=el('button','Play video');play.type='button';play.addEventListener('click',async()=>{try{if(v.paused)await v.play();else v.pause();}catch{play.textContent='Use the video controls to play';}});
    v.addEventListener('play',()=>{play.textContent='Pause video';});v.addEventListener('pause',()=>{play.textContent='Play video';});
    const error=el('p','Video could not load. Use the original video link.','media-warning');error.hidden=true;v.addEventListener('error',()=>{error.hidden=false;});
    $('viewer-content').append(v,play,error);link($('viewer-content'),'Open original video',entry.original);
  } else if(entry.type==='frame') {
    const canvas=el('canvas');canvas.width=entry.canvas.width;canvas.height=entry.canvas.height;canvas.getContext('2d').drawImage(entry.canvas,0,0);$('viewer-content').append(canvas);
  } else {const img=el('img');img.src=entry.src;img.alt=entry.title;$('viewer-content').append(img);}
  const index=gallery.indexOf(entry);$('viewer-prev').disabled=index<=0;$('viewer-next').disabled=index>=gallery.length-1;
}
function openViewer(entry) {
  const dialog=$('media-viewer');
  if(!dialog.open){viewerReturn=document.activeElement;viewerOverflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog.showModal();history.pushState({briefMediaViewer:true},'');viewerHistory=true;}
  renderViewer(entry);$('viewer-close').focus();
}
function dismissViewer(fromHistory=false) {
  const dialog=$('media-viewer');if(!dialog.open)return;stopViewerMedia();dialog.close();document.body.style.overflow=viewerOverflow;viewerReturn?.focus();viewerEntry=null;
  if(viewerHistory&&!fromHistory){viewerHistory=false;history.back();}else viewerHistory=false;
}
$('viewer-close').addEventListener('click',()=>dismissViewer());
$('media-viewer').addEventListener('keydown',e=>{
  if(e.key!=='Tab')return;
  const nodes=[...$('media-viewer').querySelectorAll('button:not([disabled]),a[href],video[controls]')].filter(n=>n.getClientRects().length);
  const first=nodes[0],last=nodes.at(-1);if(!first)return;
  if(e.shiftKey && document.activeElement===first){e.preventDefault();last.focus();}
  else if(!e.shiftKey && document.activeElement===last){e.preventDefault();first.focus();}
});
$('media-viewer').addEventListener('cancel',e=>{e.preventDefault();dismissViewer();});
$('media-viewer').addEventListener('click',e=>{if(e.target===$('media-viewer')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dismissViewer();}});
for(const [id,step] of [['viewer-prev',-1],['viewer-next',1]])$(id).addEventListener('click',()=>{const entry=gallery[gallery.indexOf(viewerEntry)+step];if(entry)renderViewer(entry);});
window.addEventListener('popstate',()=>dismissViewer(true));
let masterAfter='',masterLoading=false;
async function loadMaster() {
  if (masterLoading) return;
  masterLoading=true; $('master-more').disabled=true;
  try {
    const r=await fetch('/api/brief/master'+(masterAfter ? '?after='+masterAfter : ''),{credentials:'same-origin',cache:'no-store'});
    if(r.status===401){location.replace('/brief-login');return;}
    if(!r.ok)throw new Error();
    const page=await r.json();
    for(const item of page.rows){const box=el('article',undefined,'row release-card');box.append(el('h3',item.title),el('p',`${item.platform} / ${item.account} / ${instant(item.scheduledAt)}`,'note'),el('p',`Approval: ${item.approval.status.replaceAll('_',' ')}. ${item.approval.reference}`,'note'));preview(box,item.id,item.cover,item.media.find(u=>/\.(mp4|webm)$/.test(u)));const details=el('details');details.append(el('summary','Caption and approval evidence'),el('p',item.caption),el('p',item.approval.quote,'note'));box.append(details);for(const u of item.media)link(box,'Original media',u);$('master-rows').append(box);}
    masterAfter=page.next || ''; $('master-more').hidden=!page.next;put('master-status',page.rows.length ? 'Inventory retained beyond the Blotato cap. Dates are shown in Central time.' : 'No inventory imported yet.');
  }catch{put('master-status','Private inventory could not be loaded. Try again.');}
  finally{masterLoading=false;$('master-more').disabled=false;}
}
let loading = false;
function resetEdition() {
  gallery.length=0;
  for (const id of ['yesterday','opportunities','sites','campaigns','queue-rows','useful','sources']) $(id).replaceChildren();
  for (const id of ['stats-section','useful-section']) $(id).hidden = true;
  for (const id of ['edition-note','routine-status','focus-why','focus-source']) put(id,'');
}
async function load() {
  if (loading) return;
  loading = true;
  const retry = $('retry');
  if (retry) { retry.hidden = true; retry.disabled = true; }
  put('notice','');
  let phase = 'fetch';
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(),15000);
  try {
    const response = await fetch('/api/brief/data',{credentials:'same-origin',cache:'no-store',signal:controller.signal});
    if (response.status === 401) { location.replace('/brief-login'); return; }
    if (!response.ok) { const error = new Error('Brief request failed'); error.status = response.status; throw error; }
    phase = 'data';
    const d = await response.json();
    phase = 'render';
    resetEdition();
    put('edition',date(d.forDate)); put('edition-note',`${d.editionType === 'retrospective' ? 'Retrospective proof' : 'Verified edition'} · Updated ${instant(d.generatedAt)} · About two to three minutes`);
    imageProvenance(d);
    put('routine-status',routineStatus(d));
    if (d.forDate !== dayOf(Date.now())) put('notice',`This is the ${date(d.forDate)} edition. It does not establish today's priority.`);
    const currentFocus = d.focus.status === 'current' && d.forDate === dayOf(Date.now());
    put('focus-title',currentFocus ? d.focus.task : 'Confirm your current priority');
    put('focus-why',currentFocus ? d.focus.why : (d.editionType === 'retrospective' ? `Historical plan for ${date(d.forDate)}: ${d.focus.task} ${d.focus.why} This is not today's priority.` : 'There is no fresh, applicable explicit planning priority. Trello is not connected. Choose the task before starting an old backlog item.'));
    put('focus-source',`${d.focus.source}${d.focus.statedAt ? ' · ' + instant(d.focus.statedAt) : ''}${d.focus.status !== 'current' ? ' · ' + d.focus.status : ''}`);
    cards('yesterday',d.yesterday,'No confirmed completion supplied.'); cards('opportunities',d.opportunities,'No verified inbox conclusion supplied.');
    if (d.stats) {
      $('stats-section').hidden = false;
      put('stats-window',`${date(d.stats.day)}, full day in America/Chicago. Seven-day spend: ${d.stats.weekFrom} through ${d.stats.weekThrough}, inclusive.`);
      for (const s of d.stats.sites) { const box = el('div'); box.append(el('h3',s.name),el('div',number(s.visitors) + ' visitors','big'),el('p',`Same weekday last week: ${number(s.previousVisitors)}. First newsletter captures: ${number(s.emailLeads)}.`,'note'),el('p',`Free generations: ${number(s.freeGenerations)}. New trials: ${number(s.trials)}. Paid customers: ${number(s.paid)}.`,'note')); $('sites').append(box); }
      for (const c of d.stats.campaigns) { const row = el('tr'); row.append(el('td',c.name),el('td',dollars(c.daySpend)),el('td',dollars(c.last7dSpend))); $('campaigns').append(row); }
      put('stats-note',d.stats.note);
    }
    queue(d);
    if (d.useful.length) { $('useful-section').hidden = false; cards('useful',d.useful,''); }
    for (const source of d.sources) $('sources').append(el('p',`${source.name}: ${source.status}${source.sourceAt ? ' · ' + instant(source.sourceAt) : ''}`));
  } catch (error) {
    resetEdition();
    put('edition','Your morning brief');
    const reason = error.status ? `The brief data request returned HTTP ${error.status}.` : phase === 'render' ? 'The edition could not be displayed.' : phase === 'data' ? 'The data response could not be read.' : error.name === 'AbortError' ? 'The brief data request timed out.' : 'The brief data request could not connect.';
    put('notice',`${reason} Try loading again. No old priority or zero count has been substituted.`);
    put('focus-title','Confirm your current priority');
    if (retry) retry.hidden = false;
  } finally { clearTimeout(timeout); loading = false; if (retry) retry.disabled = false; }
}
$('logout').addEventListener('click',async () => {
  const response = await fetch('/api/brief/logout',{method:'POST',credentials:'same-origin',headers:{'X-Brief-Action':'logout'}});
  if (response.ok) location.replace('/brief-login'); else put('notice','Sign-out could not be verified. Try again.');
});
// The owner-protected image has its own request, so a data failure cannot hide it.
const dailyImage = $('daily-image');
dailyImage.addEventListener('load',() => { $('image-section').hidden = false; });
dailyImage.addEventListener('error',() => { $('image-section').hidden = true; });
dailyImage.src = '/api/brief/image';
if ($('retry')) $('retry').addEventListener('click',load);
$('master-more').addEventListener('click',loadMaster);
load();
