'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const code=fs.readFileSync(require.resolve('../web/favorites-client.js'),'utf8');
class Node {
 constructor(){this.events={};this.children=[];this.disabled=false;this.hidden=false;this.textContent='';this.attrs={};}
 addEventListener(event,fn){this.events[event]=fn;}
 setAttribute(k,v){this.attrs[k]=v;}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=nodes;}
}
const tick=()=>new Promise(resolve=>setImmediate(resolve));
(async()=>{
 const nodes=Object.fromEntries(['favorite-image','daily-image','favorites-refresh','favorites-more','favorites-grid','favorites-status','favorite-status','favorites-details'].map(id=>[id,new Node()]));
 const old={sha256:'a'.repeat(64),forDate:'2026-10-21'},next={sha256:'b'.repeat(64),forDate:'2026-10-25'};
 let image=old,calls=[],pending=null;
 nodes['daily-image'].src='https://absbyai.com/api/brief/image?sha256='+old.sha256;nodes['daily-image'].naturalWidth=1920;
 async function fetch(url,options={}){
  calls.push({url,options});
  if(options.method&&pending)return pending;
  const value=url==='/api/brief/data'?{imageAvailable:true,image}:url==='/api/brief/favorites/manifest'?{rows:[],wallpaper:{message:'pending'}}:{favorite:{...JSON.parse(options.body),active:true},wallpaper:{message:'Waiting for Mac'}};
  return {status:200,ok:true,json:async()=>value};
 }
 vm.runInNewContext(code,{document:{getElementById:id=>nodes[id],createElement:()=>new Node()},location:{href:'https://absbyai.com/morningbrief',replace(){}},fetch,URL,AbortController,setTimeout,clearTimeout,Date});await tick();await tick();
 assert.equal(nodes['favorite-image'].disabled,false);
 await nodes['favorite-image'].events.click();assert.equal(JSON.parse(calls.find(c=>c.options.method).options.body).forDate,'2026-10-21');
 // Main page replaces the image URL before load. A stale enabled button must not save.
 nodes['daily-image'].src='https://absbyai.com/api/brief/image?sha256='+next.sha256;
 const previous=calls.filter(c=>c.options.method).length;
 await nodes['favorite-image'].events.click();assert.equal(calls.filter(c=>c.options.method).length,previous);
 // Metadata and image mismatch fails closed, then exact new source can bind.
 await nodes['daily-image'].events.load();assert.equal(nodes['favorite-image'].disabled,true);
 image=next;await nodes['daily-image'].events.load();assert.equal(nodes['favorite-image'].disabled,false);
 let resolve;pending=new Promise(r=>resolve=r);
 const saving=nodes['favorite-image'].events.click();
 image=old;nodes['daily-image'].src='https://absbyai.com/api/brief/image?sha256='+old.sha256;
 await nodes['daily-image'].events.load();
 resolve({ok:true,status:200,json:async()=>({favorite:{...next,active:true},wallpaper:{message:'old request'}})});await saving;
 assert.equal(nodes['favorite-image'].attrs['aria-pressed'],'false');
 nodes['daily-image'].events.error();assert.equal(nodes['favorite-image'].disabled,true);
 console.log('favorites_client: exact displayed-image date/digest, refresh race, metadata mismatch, in-flight publication change and failed-image controls passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
