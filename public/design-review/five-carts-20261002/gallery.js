'use strict';
let width=390;
const picks=[...document.querySelectorAll('[data-pick]')];
picks[1].selectedIndex=1;
function load(i){const slug=picks[i].value;document.querySelector(`[data-frame="${i}"]`).src=slug+'.html';document.querySelector(`[data-open="${i}"]`).href=slug+'.html';}
function resize(){document.querySelectorAll('.frame-shell').forEach(shell=>{const available=shell.parentElement.clientWidth-36;const scale=Math.min(1,available/width);const height=width===1440?1200:850;shell.style.width=(width*scale)+'px';shell.style.height=(height*scale)+'px';const frame=shell.querySelector('iframe');frame.style.width=width+'px';frame.style.height=height+'px';frame.style.transform=`scale(${scale})`;});}
picks.forEach((p,i)=>{p.addEventListener('change',()=>load(i));load(i);});
document.querySelectorAll('[data-width]').forEach(b=>b.addEventListener('click',()=>{width=Number(b.dataset.width);document.querySelectorAll('[data-width]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));resize();}));
document.querySelector('[data-restart]').addEventListener('click',()=>picks.forEach((p,i)=>load(i)));
window.addEventListener('resize',resize);resize();
