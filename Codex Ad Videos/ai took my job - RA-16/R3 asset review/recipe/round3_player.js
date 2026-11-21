const dock=document.getElementById('dock');
let selection=media.find(m=>m.src===document.getElementById('player').getAttribute('src'));
let generation=0;
const status=document.getElementById('player-status');
function bindPlayer(v){
  v.addEventListener('error',()=>{status.textContent='This clip could not load. Use Reload Clip to try again.';});
  v.addEventListener('playing',()=>{status.textContent='';});
}
function play(src,label){
  selection=media.find(m=>m.src===src)||{src,label};
  const old=document.getElementById('player');
  old.pause();
  const v=document.createElement('video');
  v.id='player'; v.controls=true; v.preload='auto'; v.playsInline=true;
  if(selection.poster)v.poster=selection.poster;
  v.setAttribute('aria-label',label);
  old.replaceWith(v);
  old.removeAttribute('src'); old.load();
  document.getElementById('now').textContent=label;
  document.getElementById('open-clip').href=src;
  status.textContent='Loading clip...';
  bindPlayer(v);
  // Put the video surface on screen before starting its decoder. In the narrow
  // review panel the asset buttons are below the player, outside its viewport.
  const token=++generation;
  requestAnimationFrame(()=>{
    if(token!==generation)return;
    dock.scrollIntoView({block:'start',behavior:'instant'});
    v.src=src; v.load();
    v.play().catch(()=>{status.textContent='Press Play to start this clip.';});
  });
}
function seekBy(delta){
 const v=document.getElementById('player');
 if(!Number.isFinite(v.duration))return;
 v.currentTime=Math.max(0,Math.min(v.duration-0.04,v.currentTime+delta));
}
function reloadClip(){play(selection.src,selection.label);}
bindPlayer(document.getElementById('player'));

function togglePlayback(){const v=document.getElementById('player');if(v.paused)v.play().catch(()=>{status.textContent='Use Reload Clip to try again.';});else v.pause();}
