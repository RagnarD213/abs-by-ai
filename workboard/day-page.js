'use strict';
(()=>{
 const day=d=>new Date(d+'T12:00:00Z'),label=d=>day(d).toLocaleDateString('en-US',{timeZone:'America/Chicago',weekday:'long',month:'long',day:'numeric'});
 const end=d=>day(d).getUTCDay()===2?'18:30':'19:00';
 const clock=t=>new Date('2000-01-01T'+t+':00Z').toLocaleTimeString('en-US',{timeZone:'UTC',hour:'numeric',minute:'2-digit'});
 function shift(d,n){const date=day(d);date.setUTCDate(date.getUTCDate()+n);return date.toISOString().slice(0,10);}
 function choose(d){if(busy)return;if(dirty()){notice('Save or close your open card before changing days.');return;}if(!/^\d{4}-\d{2}-\d{2}$/.test(d)||!Number.isFinite(day(d).getTime()))return;selectedDate=d;history.replaceState(null,'',location.pathname+'?date='+d);render();}
 const template=()=>({date:selectedDate,status:'proposed',note:'8 a.m. start. Keep 9:30–11:30 free for gym prep, training, shower and supplements. Work ends '+clock(end(selectedDate))+'.',blocks:[{id:'gym',title:'Gym prep, workout, shower & supplements',start:'09:30',end:'11:30',kind:'break'}]});
 const plan=()=>state.plans?.[selectedDate]||template();
 function editBlock(block=null){const snapshot=structuredClone(plan());showPanel(block?'Adjust calendar block':'Add calendar block',body=>{
  const f=el('form'),name=el('input'),start=el('input'),finish=el('input'),kind=el('select');
  name.required=true;name.maxLength=200;name.value=block?.title||'';name.setAttribute('aria-label','Block title');
  start.type=finish.type='time';start.required=finish.required=true;start.value=block?.start||'11:30';finish.value=block?.end||'12:00';start.setAttribute('aria-label','Block start');finish.setAttribute('aria-label','Block end');
  ['work','break','travel','commitment'].forEach(k=>kind.append(new Option(k[0].toUpperCase()+k.slice(1),k)));kind.value=block?.kind||'work';kind.setAttribute('aria-label','Block type');
  for(const [text,input] of [['Title',name],['Start',start],['End',finish],['Type',kind]]){const l=el('label','',text);l.append(input);f.append(l);}
  const submit=el('button','btn primary','Save block');submit.type='submit';f.append(submit);body.append(f);
  const save=async replacement=>{const latest=state.plans?.[snapshot.date]||snapshot,blocks=latest.blocks.filter(b=>b.id!==block?.id);if(replacement)blocks.push(replacement);if(await change('plan.save',{...latest,blocks,status:'proposed'}))$('panel-dialog').close();};
  f.onsubmit=e=>{e.preventDefault();save({...block,id:block?.id||crypto.randomUUID(),title:name.value,start:start.value,end:finish.value,kind:kind.value});};
  if(block)body.append(button('Remove block',()=>save(null),'btn danger'));
 });}
 window.renderDay=()=>{
  if(!state)return;const p=plan(),dateLabel=label(selectedDate),isToday=selectedDate===centralToday();
  $('plan-date').value=selectedDate;$('day-heading').textContent=isToday?'Today, in focus.':dateLabel;
  const personal=state.cards.filter(c=>!c.archived&&activeLists().some(l=>l.id===c.listId)&&(!c.plannedFor||c.plannedFor===selectedDate)),complete=personal.filter(c=>state.lists.find(l=>l.id===c.listId)?.role==='completed').length;
  $('day-summary').textContent=dateLabel+' · '+complete+' of '+personal.length+' completed';
  $('plan-status').textContent=p.status==='accepted'?'Accepted':'Proposed';$('plan-status').classList.toggle('accepted',p.status==='accepted');
  $('work-hours').textContent='8–9:30 a.m. · 11:30 a.m.–'+clock(end(selectedDate));
  $('plan-note').textContent=p.note||'Move the blocks until the day feels realistic.';
  $('accept-plan').hidden=p.status==='accepted';
  $('calendar-source').textContent=p.calendarCheckedAt?'Google Calendar checked '+new Date(p.calendarCheckedAt).toLocaleString('en-US',{timeZone:'America/Chicago',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'})+' CT. Work blocks are saved on this dashboard only.':'Google Calendar has not been checked for this date. Blocks are saved on this dashboard only.';
  const blocks=$('calendar-blocks');blocks.replaceChildren();
  blocks.append(el('div','calendar-boundary','8:00 a.m. · Start with your #1 task'));
  let closed=false;for(const b of [...p.blocks].sort((a,b)=>a.start.localeCompare(b.start))){if(!closed&&b.start>=end(selectedDate)){blocks.append(el('div','calendar-boundary',clock(end(selectedDate))+' · Finish work'));closed=true;}const row=el('article','calendar-block '+(b.kind||'work'));
   const time=el('div','block-time',clock(b.start)+' – '+clock(b.end)),main=el('div','block-main');main.append(el('h3','',b.title));
   const c=b.cardId&&state.cards.find(c=>c.id===b.cardId),done=c&&state.lists.find(l=>l.id===c.listId)?.role==='completed';
   main.append(el('span','block-status',done?'✓ Completed':b.source==='google'?'Google Calendar':b.kind==='break'?'Protected time':b.kind==='travel'?'Travel / preparation':p.status==='accepted'?'Planned':'Proposed'));
   if(done)row.classList.add('block-done');row.append(time,main);
   if(b.source!=='google'){const edit=button('Edit',()=>editBlock(b));edit.setAttribute('aria-label','Edit block: '+b.title);row.append(edit);}blocks.append(row);
  }
  if(!closed)blocks.append(el('div','calendar-boundary',clock(end(selectedDate))+' · Finish work'));
  $('reward-toggle').checked=state.preferences?.rewards!==false;
  const other=$('other-days');other.replaceChildren();const unscheduled=state.cards.filter(c=>!c.archived&&c.plannedFor&&c.plannedFor!==selectedDate&&activeLists().some(l=>l.id===c.listId&&l.role!=='completed'));
  if(unscheduled.length){const details=el('details','other-days'),summary=el('summary','',unscheduled.length+' unfinished cards from other days');details.append(summary);
   for(const c of unscheduled){const row=el('div','archive-row');row.append(el('span','',c.title+' · '+c.plannedFor),button('Plan for this day',()=>change('card.move',{id:c.id,listId:activeLists().find(l=>l.role==='planned').id,plannedFor:selectedDate,index:state.cards.length?state.cards.filter(x=>x.listId===activeLists().find(l=>l.role==='planned').id&&!x.archived).length:0})));details.append(row);}other.append(details);
  }
 };
 $('previous-day').onclick=()=>choose(shift(selectedDate,-1));$('next-day').onclick=()=>choose(shift(selectedDate,1));$('plan-date').onchange=e=>choose(e.target.value);$('today-button').onclick=()=>choose(centralToday());$('tomorrow-button').onclick=()=>choose(shift(centralToday(),1));
 $('accept-plan').onclick=()=>change('plan.save',{...plan(),status:'accepted'});$('add-block').onclick=()=>editBlock();
 $('reward-toggle').onchange=async e=>{const value=e.target.checked;if(!await change('preferences.update',{rewards:value}))e.target.checked=!value;};
 if(state)window.renderDay();
})();
