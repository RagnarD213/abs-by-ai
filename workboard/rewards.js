'use strict';
(()=>{
 let images=[],previous=null,timer=null,animation=null;
 fetch('/api/workboard/rewards',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject()).then(d=>{images=d.images||[];for(const i of images){const img=new Image();img.src=i.url;}}).catch(()=>{});
 function dismiss(){clearTimeout(timer);if(animation)cancelAnimationFrame(animation);document.getElementById('completion-reward')?.remove();}
 window.celebrateTask=title=>{
  if(state?.preferences?.rewards===false)return;dismiss();
  const overlay=el('div','completion-reward');overlay.id='completion-reward';overlay.setAttribute('popover','manual');overlay.setAttribute('role','status');overlay.setAttribute('aria-live','polite');
  const box=el('div','reward-box'),close=button('×',dismiss,'reward-close');close.setAttribute('aria-label','Dismiss celebration');box.append(close);
  const choices=images.filter(i=>i.sha256!==previous),chosen=(choices.length?choices:images)[Math.floor(Math.random()*(choices.length||images.length))];
  if(chosen){previous=chosen.sha256;const img=el('img','reward-image');img.alt='AI-generated image from your private favorites';img.src=chosen.url;img.onerror=()=>img.remove();box.append(img,el('span','reward-disclosure','AI-generated'));}
  box.append(el('p','reward-eyebrow','ANOTHER WIN'),el('h2','','Nice work, Dan.'),el('p','reward-title',title));overlay.append(box);document.body.append(overlay);overlay.showPopover?.();
  timer=setTimeout(dismiss,3200);
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const canvas=el('canvas','reward-confetti');overlay.append(canvas);const ctx=canvas.getContext('2d');if(!ctx)return;canvas.width=innerWidth;canvas.height=innerHeight;
  const colors=['#badfa0','#e8c67e','#eaa8bc','#97c9ec','#c1ace8'];let start=null;
  const pieces=Array.from({length:100},()=>({x:Math.random()*innerWidth,y:-Math.random()*innerHeight,dx:(Math.random()-.5)*2,dy:2+Math.random()*4,size:4+Math.random()*6,angle:Math.random()*6,color:colors[Math.floor(Math.random()*colors.length)]}));
  const frame=at=>{start??=at;ctx.clearRect(0,0,canvas.width,canvas.height);for(const p of pieces){p.x+=p.dx;p.y+=p.dy;p.angle+=.03;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.angle);ctx.fillStyle=p.color;ctx.fillRect(0,0,p.size,p.size*.6);ctx.restore();}if(at-start<3100)animation=requestAnimationFrame(frame);};animation=requestAnimationFrame(frame);
 };
 document.addEventListener('keydown',e=>{if(e.key==='Escape')dismiss();});
})();
