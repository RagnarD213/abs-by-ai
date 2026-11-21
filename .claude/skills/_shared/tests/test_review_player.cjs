/* Deterministic player lifecycle tests. No browser or media is opened. */
const fs = require('fs'), vm = require('vm'), assert = require('node:assert/strict');
const code = fs.readFileSync(process.argv[2], 'utf8');
function setup() {
  let now = 100000, timers = new Map(), serial = 0, tick;
  class Element {
    constructor() { this.events={}; this.children=[]; this.style={}; this.attrs={}; }
    addEventListener(n, fn) { (this.events[n] ||= []).push(fn); }
    emit(n, e={}) { for (const fn of this.events[n] || []) fn(e); }
    setAttribute(n,v) {this.attrs[n]=v;} getAttribute(n) {return this.attrs[n] || null;}
    append(...xs) {this.children.push(...xs);}
    insertAdjacentElement(_,x) {this.box=x;}
  }
  const v = new Element();Object.assign(v,{currentTime:5,playbackRate:.5,muted:true,volume:.6,paused:true,ended:false,seeking:false,readyState:4,duration:10,isConnected:true,loads:0});
  v.setAttribute('src','media/sample.mp4');
  v.load=()=>{v.loads++;v.currentTime=0;v.readyState=0;v.paused=true;v.emit('loadstart');};
  v.play=()=>{v.paused=false;v.emit('play');return Promise.resolve();};v.pause=()=>{v.paused=true;};
  const document = new Element();document.hidden=false;document.documentElement=new Element();
  document.querySelectorAll=()=>[v];document.createElement=()=>new Element();
  const window=new Element();
  vm.runInNewContext(code,{document,window,Date:{now:()=>now},setInterval:fn=>{tick=fn;},setTimeout:(fn,ms)=>{let id=++serial;timers.set(id,{fn,ms});return id;},clearTimeout:id=>timers.delete(id),MutationObserver:class{observe(){}},Map,Number,Math});
  function settle() {v.readyState=4;v.emit('loadedmetadata');for(const [id,t] of [...timers])if(t.ms===0){timers.delete(id);t.fn();}v.emit('loadeddata');v.emit('canplay');}
  return {v,document,window,settle,tick:()=>tick(),advance:n=>{now+=n;},expire:()=>{for(const [id,t] of [...timers]){timers.delete(id);t.fn();}}};
}
{
 const t=setup();t.v.box.children[0].emit('click');t.settle();
 assert.equal(t.v.loads,1);assert.equal(t.v.currentTime,5);assert.equal(t.v.playbackRate,.5);assert.equal(t.v.volume,.6);assert.equal(t.v.muted,true);assert.equal(t.v.paused,true);
}
{
 const t=setup();t.document.hidden=true;t.document.emit('visibilitychange');t.advance(61000);t.document.hidden=false;t.document.emit('visibilitychange');t.settle();
 assert.equal(t.v.loads,1);assert.equal(t.v.currentTime,5);
 t.advance(61000);t.tick();t.settle();t.advance(61000);t.tick();t.settle();assert.equal(t.v.loads,3);
}
{
 const t=setup();t.v.paused=false;t.advance(11000);t.tick();t.settle();assert.equal(t.v.paused,false);assert.equal(t.v.loads,1);
 // Actual progress prevents a restart while watching normally.
 t.advance(2000);t.v.currentTime=7;t.v.emit('timeupdate');t.tick();assert.equal(t.v.loads,1);
}
{
 const t=setup();t.v.emit('error');t.expire();t.v.emit('error');t.expire();t.v.emit('error');assert.equal(t.v.loads,2);
 t.v.box.children[0].emit('click');t.settle();assert.equal(t.v.loads,3);
}
{
 const t=setup();t.v.box.children[0].emit('click');t.v.setAttribute('src','media/clearer.mp4');t.v.emit('loadstart');t.v.currentTime=2;t.settle();assert.equal(t.v.currentTime,2);
}
console.log('PASS: reload preserves controls; idle/sleep recovery; stalled playback; bounded retries; source switch cancels old restore');
