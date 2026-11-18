'use strict';
const $=s=>document.getElementById(s), tm=t=>t?new Date(t*1000).toLocaleTimeString([], {hour:'numeric',minute:'2-digit',second:'2-digit'}):'never';
function el(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e}
let ETA={jobs:{}};
function etaLine(id){const e=ETA.jobs&&ETA.jobs[id];if(!e||e.kind==='dan')return null;
 const p=el('div','eta '+e.kind,(e.kind==='eta'?'ETA ':'')+e.text);if(e.confidence)p.append(el('span','conf',e.confidence));
 const w=el('div','etawrap');w.append(p);if(e.detail)w.append(el('div','etadetail',e.detail));return w}
function job(a,stage){let r=el('div','job');r.append(el('strong','',a.title),el('div','',stage+(a.urgent?' · Priority':'')));const e=a.id&&etaLine(a.id);if(e)r.append(e);return r}
function card(h,v,route,now,titles={}){
 const d=v.data||{}, box=el('article'),top=el('div','cardtop'),name=el('div'),c=el('div','slots',(d.lowerBound?'≥ ':'')+String(d.used??'?')+' / '+String(d.cap??'?'));c.append(el('span','','edit slots used'));name.append(el('h3','macname',h.toUpperCase()),el('div','role',h==='m6'?'Dan’s daily Mac':'Editing Mac'));top.append(name,c);box.append(top);
 if(d.cap){const bar=el('div','bar');for(let i=0;i<Math.min(d.cap,12);i++)bar.append(el('i',d.used!=null&&i<d.used?'on':''));box.append(bar)}
 box.append(el('p','muted','Last full reading: '+tm(v.lastSuccess)+(v.busy?' · Updating…':'')));
 if(v.error||(v.age||0)>120)box.append(el('p','warn',(v.error||'Reading is stale')+'. Last attempt: '+tm(v.attempt)));
 if(d.note)box.append(el('p','muted',d.note));
 for(const alert of d.alerts||[])box.append(el('p','warn','Overnight queue: '+alert));
 for(const issue of d.issues||[])box.append(el('p','warn',issue));
 if(!v.data)return box;
 const jobs=d.jobs,active=jobs.filter(j=>j.occupies),res=(route?.reserved[h]||[]).filter(id=>!active.some(j=>j.id===id));
 box.append(el('small','label','IN PRODUCTION'));
 for(const a of active){let stage=a.held?'Render slot held'+(a.held>1?' × '+a.held:''):a.tickets?'Waiting for a render step':a.states.includes('promoted')?'Slot reserved':'In production, current step unknown';box.append(job(a,stage))}
 if(!active.length)box.append(el('p','muted',d.used==null?'Current edits unknown.':'No production edits recorded.'));
 const isWaiting = a => !a.occupies && (a.batchStage || res.includes(a.id) ||
   ((!a.auxiliary || a.workKind!=='setup') && a.states.some(s=>s==='waiting'||s==='parked')));
 const waiting=jobs.filter(isWaiting);
 const auxiliary=jobs.filter(j=>j.auxiliary && !isWaiting(j));
 if(auxiliary.length){
   box.append(el('small','label','SETUP / HELPER WORK (NOT EDIT SLOTS)'));
   for(const a of auxiliary)box.append(job(a,(a.workKind==='setup'?'Setup':'Helper work')+' · '+(a.held?'Render step running':'Waiting for a render step')+(a.states.includes('stalled')?' · Edit slot released':'')));
 }
 if(waiting.length||res.length||d.dedicated){
   box.append(el('small','label','WAITING OR RESERVED'));
   for(const a of waiting){
     const status=[a.batchStage || (a.states.includes('parked')?'Parked for reserved work':'Waiting for an edit slot')];
     if(res.includes(a.id))status.push('Slot reserved');
     if(a.held)status.push('Render step running');
     if(a.tickets)status.push(a.tickets+' render steps queued');
     box.append(job(a,status.join(' · ')));
   }
   for(const id of res.filter(id=>!waiting.some(j=>j.id===id)))box.append(job({title:titles[id]||'Project name needs checking'},'Routed here, slot reserved'));
   if(d.dedicated)box.append(el('p','job','Dedicated to '+(titles[d.dedicated]||'Project name needs checking')));
 }
 box.append(el('div','health','Memory: '+(d.pressure||'unknown')+' · '+(d.renders??'?')+(d.renders===1?' render step running · ':' render steps running · ')+(d.tickets??'?')+' render steps queued'));
 const more=el('details');more.dataset.key=h+'info';more.append(el('summary','','Machine details'));
 const outside=d.outside?d.outside.count+' at '+tm(d.outside.at)+(now-d.outside.at>60?' (older reading)':''):'unknown';
 for(const text of ['Render allowance: '+(d.assigned??'?')+' assigned / '+(d.budget??'?')+' cores ('+(d.presence||'unknown')+'). This is a budget, not measured CPU use.','Work outside the render queue: '+outside+'.','New priority features: '+(d.priorityEnabled===true?'enabled':d.priorityEnabled===false?'off':'unknown')+'.','Last attempt: '+tm(v.attempt)+'.'])more.append(el('p','',text));
 for(const a of jobs.filter(j=>j.tickets))more.append(el('p','',a.title+': '+a.tickets+' render step(s) waiting.'));
 for(const a of jobs.filter(j=>!j.occupies&&j.held))more.append(el('p','',a.title+': '+a.held+' render step(s) observed.'));
 for(const a of jobs)more.append(el('p','',a.title+' · '+a.id));
 box.append(more);
 const stalled=jobs.filter(j=>!j.occupies&&!j.auxiliary&&j.states.includes('stalled'));if(stalled.length){const det=el('details');det.dataset.key=h+'stalled';det.append(el('summary','','Possible stalls ('+stalled.length+')'));for(const a of stalled)det.append(job(a,'Marked stalled in the edit register'));box.append(det)}
 return box
}
function paint(s){ETA=s.eta||{jobs:{}};const open=new Set([...document.querySelectorAll('details[open]')].map(x=>x.dataset.key));const [tone,title,why]=s.advice;$('rec').className='recommend '+tone;$('advice').textContent=title;$('why').textContent=why;const rows=$('reviews');
 rows.replaceChildren();
 const partial=Object.values(s.hosts).some(v=>!v.data || v.error || (v.age??999)>120 ||
   v.data.issues.some(issue=>/register|catalog|production queue/i.test(issue)));
 for(const r of s.reviews){
   const item=job(r,r.question),link=el('a','','Open review');
   link.href=r.link;item.append(link);rows.append(item);
 }
 if(!s.reviews.length)rows.append(el('p','',partial?'No confirmed decisions in the available readings.':'No edit decisions waiting for you.'));
 if(partial)rows.append(el('p','warn','Review information is incomplete or out of date.'));
 for(const name of s.unconfirmed)rows.append(el('p','warn','Review handoff needs checking: '+name));
 const route=s.hosts.m6.data?.route;const boxes=['m6','m2'].map(h=>card(h,s.hosts[h],route,s.now,s.titles));$('hosts').replaceChildren(...boxes);for(const det of document.querySelectorAll('details'))det.open=open.has(det.dataset.key);$('when').textContent=(Object.values(s.hosts).some(v=>v.busy)?'Checking now…':'Updated '+tm(Math.max(...Object.values(s.hosts).map(x=>x.readAt||0))))+(ETA.checked?' · ETAs checked '+ETA.checked+' (every 10 min)':'');$('line').textContent=route?(s.shared.length?s.shared.join(' • '):'No additional edits waiting for assignment.'):'Shared list unavailable.';if(s.hosts.m6.error||(s.hosts.m6.age??0)>120)$('line').textContent+=' Last known reading.';}
let timer,seq=0,controller;
function stop(){seq++;clearTimeout(timer);controller?.abort()}
async function update(manual=false){
 stop();if(document.hidden)return;const id=seq,signal=(controller=new AbortController()).signal;
 try{let path=manual?'/manual':'/refresh',deadline=Date.now()+10000;
 for(;;){let response=await fetch(path,{method:path==='/state'?'GET':'POST',headers:{'X-Edit-View':'visible'},signal});if(!response.ok)throw Error();let s=await response.json();if(id!==seq||document.hidden)return;paint(s);if(!Object.values(s.hosts).some(v=>v.busy)||Date.now()>deadline)break;await new Promise(ok=>setTimeout(ok,300));if(id!==seq||document.hidden)return;path='/state'}
 }catch(e){if(id!==seq||document.hidden)return;$('advice').textContent='Check status before starting';$('why').textContent='The dashboard could not refresh. The readings below may be old.';$('rec').className='recommend check'}
 if(id===seq&&!document.hidden)timer=setTimeout(()=>update(),60000);
}
$('refresh').addEventListener('click',()=>update(true));document.addEventListener('visibilitychange',()=>document.hidden?stop():update());window.addEventListener('pagehide',stop);window.addEventListener('pageshow',()=>update());
