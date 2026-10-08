'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const web=path.resolve(__dirname,'../web');
class Element {
  constructor(){this.hidden=false;this.children=[];this.listeners={};this.attributes={};this.textContent='';}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(){this.children=[];}
  addEventListener(event,callback){this.listeners[event]=callback;}
  getAttribute(name){return this.attributes[name] || null;}
  set src(value){this.attributes.src=value;}
  get src(){return this.attributes.src;}
}
async function render(image,failed=false) {
  const nodes=Object.fromEntries([...fs.readFileSync(path.join(web,'page.html'),'utf8').matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new Element()]));
  const fixture={forDate:'2026-10-08',generatedAt:new Date().toISOString(),editionType:'daily',routineEnabled:false,focus:{status:'missing',source:'Fixture'},yesterday:[],opportunities:[],useful:[],sources:[],image};
  const context={document:{getElementById:id=>nodes[id],createElement:()=>new Element()},fetch:async()=>({status:failed?503:200,ok:!failed,json:async()=>fixture}),Date,Intl,AbortController,setTimeout:()=>0,clearTimeout:()=>{},location:{replace:()=>{}}};
  vm.runInNewContext(fs.readFileSync(path.join(web,'page.js'),'utf8'),context);
  await new Promise(resolve=>setImmediate(resolve));
  return nodes;
}
(async()=>{
  const image={forDate:'2026-10-08',sha256:'a'.repeat(64)};
  const current=await render(image);
  assert.equal(current['daily-image'].src,'/api/brief/image?sha256='+image.sha256);
  assert.match(current['image-caption'].textContent,/Daily image:.*October 8/);
  assert.equal(current['image-section'].hidden,true); // Wait for the matching image to load.
  current['daily-image'].listeners.load();assert.equal(current['image-section'].hidden,false);
  current['daily-image'].listeners.error();assert.equal(current['image-section'].hidden,true);
  const fallback=await render({...image,forDate:'2026-10-06'});
  assert.match(fallback['image-caption'].textContent,/Retained image:.*October 6/);
  const legacy=await render(null);
  assert.equal(legacy['daily-image'].src,'/api/brief/image');assert.equal(legacy['image-caption'].textContent,'Image date not supplied');
  const failure=await render(null,true);
  assert.equal(failure['daily-image'].src,'/api/brief/image');
  failure['daily-image'].listeners.load();assert.equal(failure['image-section'].hidden,false); // Independent hero survives a data failure.
  console.log('image freshness: digest-bound source, truthful current/fallback dates, legacy handling and independent image loading passed');
})().catch(error=>{console.error(error);process.exitCode=1;});
