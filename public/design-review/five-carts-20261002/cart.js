/* Standalone design review. No API, analytics, billing SDK, storage or real payment requests. */
'use strict';
const q = new URLSearchParams(location.search);
const sampleStart = new Date('2026-10-02T12:00:00Z');
const trialEnd = new Date(sampleStart); trialEnd.setUTCDate(trialEnd.getUTCDate()+7);
const fullDate = trialEnd.toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric',timeZone:'UTC'});
const shortDate = trialEnd.toLocaleDateString('en-US',{month:'short',day:'numeric',timeZone:'UTC'});
const plans = {monthly:{name:'Monthly',price:'$19.99',period:'month'},annual:{name:'Annual',price:'$69.99',period:'year'}};
let selected='monthly', method='card', busy=false;
const dialog=document.querySelector('dialog');
const form=document.querySelector('[data-payment-form]');
const error=document.querySelector('[data-error]');
const submit=document.querySelector('[data-submit]');
const scenario=document.querySelector('[data-scenario]');
scenario.value=q.get('scenario')==='decline'?'decline':'success';
if(q.get('capture')==='1')document.querySelector('.review-nav').hidden=true;
const all=(selector,fn)=>document.querySelectorAll(selector).forEach(fn);
function update(){
 const p=plans[selected];
 all('[data-plan-name]',e=>e.textContent=p.name);
 all('[data-charge-date]',e=>e.textContent=fullDate);
 all('[data-first-charge]',e=>e.textContent=`${p.price} on ${shortDate}`);
 all('[data-renewal]',e=>e.textContent=`${p.price} every ${p.period}`);
 all('[data-terms]',e=>e.textContent=`7 days free, then ${p.price} every ${p.period}, billed automatically until canceled. Cancel before ${fullDate} in Manage membership to pay nothing.`);
 all('[data-faq-renewal]',e=>e.textContent=`Your selected ${p.name.toLowerCase()} membership begins at ${p.price} and renews every ${p.period} until you cancel. Your first charge date is ${fullDate}.`);
 all('[data-dock-terms]',e=>e.textContent=`Then ${p.price}/${p.period}`);
 error.hidden=true;
}
all('input[name=plan]',e=>e.addEventListener('change',()=>{selected=e.value;const check=document.querySelector('[name=agreement]');if(check)check.checked=false;resetResult();update();}));
function resetResult(){document.querySelector('.payment-content').hidden=false;document.querySelector('[data-success]').hidden=true;error.hidden=true;busy=false;submit.disabled=false;submit.textContent='Start my free 7 days →';}
all('[data-open-payment]',e=>e.addEventListener('click',()=>{if(!dialog)return;dialog.showModal();}));
all('[data-close]',e=>e.addEventListener('click',()=>dialog.close()));
if(dialog)dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
all('[data-method]',e=>e.addEventListener('click',()=>{
 method=e.dataset.method;
 all('[data-method]',b=>b.setAttribute('aria-pressed',String(b===e)));
 document.querySelector('[data-card-fields]').hidden=method!=='card';
 document.querySelector('[data-wallet]').hidden=method==='card';
 document.querySelector('[data-wallet-name]').textContent=method==='apple'?'Apple Pay':'Link';
 submit.textContent=method==='card'?'Start my free 7 days →':`Start free trial with ${method==='apple'?'Apple Pay':'Link'}`;
 error.hidden=true;
}));
form.addEventListener('submit',e=>{
 e.preventDefault();if(busy)return;
 const email=form.querySelector('[name=email]');
 if(!email.validity.valid){error.textContent='Enter a valid email address to continue.';error.hidden=false;email.focus();return;}
 const agree=form.querySelector('[name=agreement]');
 if(agree&&!agree.checked){error.textContent='Please agree to the selected membership terms before continuing.';error.hidden=false;agree.focus();return;}
 busy=true;submit.disabled=true;submit.textContent='Confirming your trial…';error.hidden=true;
 setTimeout(()=>{
 busy=false;submit.disabled=false;
 if(scenario.value==='decline'){error.textContent='Your payment method was declined. Try another method or choose Success in the review bar to retry.';error.hidden=false;submit.textContent='Try again →';return;}
 document.querySelector('.payment-content').hidden=true;document.querySelector('[data-success]').hidden=false;
 if(dialog)dialog.scrollTop=0;else document.querySelector('[data-success]').scrollIntoView({behavior:'smooth',block:'start'});
 },650);
});
all('[data-reset]',e=>e.addEventListener('click',()=>{resetResult();if(dialog)dialog.close();else document.querySelector('[name=plan]').focus();}));
const dayCopy=[['Find your starting point','Confirm your preferences and open the first day of your 4-week training program.'],['Make food easier','Explore your meal-prep recipes and grocery list. Log your meals against your targets.'],['Know the movement','Use exercise guidance during your daily total-body session, including your core work.'],['Keep the routine going','Open the next daily workout and track the food you eat. Keep the process simple.'],['Look beyond the workout','Explore Sleep Coach and its evening protocol alongside your training and nutrition.'],['See your progress','Review your training and food history. Use your AI goal image as a motivation tool.'],['Check in and continue','Review how the week went. Check-ins help your program adapt as you keep going.']];
all('[data-day]',e=>e.addEventListener('click',()=>{all('[data-day]',b=>b.setAttribute('aria-pressed',String(b===e)));const n=Number(e.dataset.day);document.querySelector('[data-day-title]').textContent=`Day ${n} · ${dayCopy[n-1][0]}`;document.querySelector('[data-day-copy]').textContent=dayCopy[n-1][1];}));
update();
if(q.get('plan')==='annual'){const annual=document.querySelector('[value=annual]');annual.checked=true;selected='annual';update();}
if(q.get('payment')==='1'&&dialog)dialog.showModal();
