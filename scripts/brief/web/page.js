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
  if (!q) { put('queue-coverage','Release queue not yet verified. Blotato and direct YouTube Studio schedules still need checking.'); return; }
  const stale = !q.checkedAt || Date.now() - Date.parse(q.checkedAt) > 12 * 3600000;
  put('queue-coverage',`Blotato: ${q.sourceCoverage.blotato}. YouTube Studio: ${q.sourceCoverage.youtubeStudio}.${stale ? ' Queue review is stale or undated.' : ' Checked ' + instant(q.checkedAt) + '.'} ${q.coverageNote || ''}`);
  put('queue-window',instant(q.windowFrom) + ' through ' + instant(q.windowTo) + ' (exclusive).');
  const tomorrow = dayOf(Date.now() + 86400000);
  const problem = row => row.notes.length > 0 || Object.values(row.preflight).some(v => ['missing','broken','duplicate','mismatch'].includes(v));
  const flags = q.rows.filter(row => problem(row) || dayOf(row.scheduledAt) === tomorrow).slice(0,3);
  if (!flags.length) $('queue-flags').append(el('p',stale ? 'No current preflight conclusion.' : 'No tomorrow or urgent flags in the verified subset.','note'));
  for (const row of flags) $('queue-flags').append(el('p',`${row.platform}, ${instant(row.scheduledAt)}: ${row.title}. ${problem(row) ? 'Preflight needs review.' : 'Releases tomorrow.'}${stale ? ' Recheck the stale snapshot first.' : ''}`));
  const days = new Map();
  const first = dayOf(q.windowFrom);
  for (let i=0;i<7;i++) {
    const day = new Date(first + 'T12:00:00Z'); day.setUTCDate(day.getUTCDate()+i);
    const key = day.toISOString().slice(0,10), column = el('section',undefined,'queue-day');
    column.append(el('h3',date(key))); days.set(key,column); $('queue-rows').append(column);
  }
  for (const row of q.rows) {
    const box = el('article',undefined,'row release-card');
    box.append(el('h3',row.title),el('p',`${row.platform} / ${row.account} / ${instant(row.scheduledAt)}`,'note'));
    preview(box,row.id,row.coverReviewUrl,row.mediaUrl);
    if (row.caption) { const details=el('details');details.append(el('summary','Caption'),el('p',row.caption));box.append(details); }
    box.append(el('p',Object.entries(row.preflight).map(([k,v]) => `${k}: ${v.replaceAll('_',' ')}`).join(' · '),'note'));
    for (const note of row.notes) box.append(el('p',note));
    link(box,'Open release',row.reviewUrl); link(box,'Open original video',row.mediaUrl);
    (days.get(dayOf(row.scheduledAt)) || $('queue-rows')).append(box);
  }
  for (const [key,column] of days) if (!q.rows.some(r=>dayOf(r.scheduledAt) === key)) column.append(el('p','No Blotato release observed. Unavailable sources remain unknown.','note'));
  put('public-coverage',Object.entries(q.publicCoverage || {}).map(([p,s])=>`${p}: ${s.replaceAll('_',' ')}`).join(' · ') || 'Public profile tiles have not been observed.');
  for (const r of q.released || []) { const box=el('div',undefined,'row');box.append(el('h3',r.title),el('p',`${r.platform}: ${r.status}. ${r.reason}`));link(box,'Public post',r.reviewUrl);$('public-rows').append(box); }
}
function preview(box,id,cover,video) {
  if (!/^[a-f0-9]{64}$/.test(id || '')) return;
  const fallback=el('p','Cover preview unavailable; open the source for review.','note'); fallback.hidden=true;
  if (cover && !video) { const img=el('img');img.src=`/api/brief/media/${id}/cover`;img.alt='Scheduled cover';img.loading='lazy';img.className='release-cover';img.addEventListener('error',()=>{img.hidden=true;fallback.hidden=false;});box.append(img,fallback); }
  else if (!cover) box.append(el('p','Cover not verified for this platform.','note'));
  if (video) { const player=el('video');player.src=`/api/brief/media/${id}/video`;player.controls=true;player.playsInline=true;player.preload='none';player.className='release-video';if(cover)player.poster=`/api/brief/media/${id}/cover`;player.addEventListener('error',()=>{box.append(el('p','Inline playback unavailable. Use the original video link.','note'));});box.append(player); }
}
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
  for (const id of ['yesterday','opportunities','sites','campaigns','queue-flags','queue-rows','public-rows','useful','sources']) $(id).replaceChildren();
  for (const id of ['stats-section','useful-section']) $(id).hidden = true;
  for (const id of ['edition-note','routine-status','focus-why','focus-source','queue-coverage','queue-window']) put(id,'');
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
