'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../web');
const html=fs.readFileSync(path.join(root,'page.html'),'utf8');
const script=fs.readFileSync(path.join(root,'page.js'),'utf8');
const now=Date.parse('2026-10-05T21:00:00Z');
const fixture={schemaVersion:1,forDate:'2026-10-05',generatedAt:'2026-10-05T12:05:00Z',editionType:'daily',routineEnabled:false,imageAvailable:true,focus:{status:'missing',task:'Confirm priority',why:'No current planning source.',source:'Synthetic'},yesterday:[{title:'Completed task',detail:'Synthetic completion',source:'Synthetic'}],opportunities:[{title:'Reply to customer',detail:'Synthetic opportunity',source:'Synthetic'}],useful:[{title:'Review delivery',detail:'Synthetic context',source:'Synthetic'}],sources:[{name:'Planning',status:'missing'}],stats:{day:'2026-10-04',weekFrom:'2026-09-28',weekThrough:'2026-10-04',sites:[{name:'absbyai.com',visitors:10,previousVisitors:9,emailLeads:0,freeGenerations:null,trials:null,paid:null}],campaigns:[{name:'Synthetic campaign',daySpend:1.5,last7dSpend:8}],note:'Actual outcomes unknown.'},socialReleaseQueue:{checkedAt:'2026-10-05T20:00:00Z',sourceCoverage:{blotato:'ok',youtubeStudio:'missing'},windowFrom:'2026-10-05T05:00:00Z',windowTo:'2026-10-12T05:00:00Z',rows:[{title:'Synthetic release',platform:'YouTube',account:'Synthetic',scheduledAt:'2026-10-06T14:00:00Z',preflight:{cover:'verified',description:'verified',links:'unverified',duplicates:'verified',assetMatch:'verified'},notes:[]}]}};
class Node {
  constructor(){this.children=[];this.textContent='';this.hidden=false;this.events={};}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=nodes;this.textContent='';}
  addEventListener(name,fn){this.events[name]=fn;}
}
async function harness(response){
  const nodes=Object.fromEntries([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new Node()]));
  for(const id of ['image-section','stats-section','useful-section','retry']) nodes[id].hidden=true;
  let next=response,redirect=null;
  const scope={document:{getElementById:id=>nodes[id]||null,createElement:()=>new Node()},fetch:async()=>{if(next instanceof Error)throw next;return next;},location:{replace:url=>{redirect=url;}},Date:class extends Date {static now(){return now;}},Intl,AbortController,setTimeout,clearTimeout};
  vm.runInNewContext(script,scope);await tick();
  return {nodes,scope,setResponse:r=>{next=r;},redirect:()=>redirect};
}
const tick=()=>new Promise(resolve=>setImmediate(resolve));
const response=d=>({status:200,ok:true,json:async()=>d});
(async()=>{
  assert(html.indexOf('id="image-section"')<html.indexOf('class="first"'),'Hero precedes priority');
  const h=await harness(response(fixture));
  assert.equal(h.nodes.notice.textContent,'');assert.match(h.nodes.edition.textContent,/October 5/);
  assert.equal(h.nodes.yesterday.children.length,1);assert.equal(h.nodes.opportunities.children.length,1);assert.equal(h.nodes['queue-rows'].children.length,7);
  assert.match(h.nodes.sites.children[0].children[3].textContent,/Free generations: Unknown\. New trials: Unknown\. Paid customers: Unknown/);
  assert.equal(h.nodes['daily-image'].src,'/api/brief/image');h.nodes['daily-image'].events.load();assert.equal(h.nodes['image-section'].hidden,false);
  await h.scope.load();assert.equal(h.nodes.yesterday.children.length,1);assert.equal(h.nodes.campaigns.children.length,1);assert.equal(h.nodes.sources.children.length,1);
  h.setResponse({status:503,ok:false});await h.scope.load();assert.match(h.nodes.notice.textContent,/HTTP 503/);assert.equal(h.nodes.yesterday.children.length,0);assert.equal(h.nodes['stats-section'].hidden,true);assert.equal(h.nodes['image-section'].hidden,false);assert.equal(h.nodes.retry.hidden,false);
  h.setResponse(response(fixture));await h.nodes.retry.events.click();assert.equal(h.nodes.notice.textContent,'');assert.equal(h.nodes.retry.hidden,true);assert.equal(h.nodes.yesterday.children.length,1);
  for(const [r,pattern] of [[Object.assign(new Error('timeout'),{name:'AbortError'}),/timed out/],[new Error('network'),/could not connect/],[{status:200,ok:true,json:async()=>{throw new Error('parse');}},/could not be read/],[response({...fixture,focus:null}),/could not be displayed/]]){h.setResponse(r);await h.scope.load();assert.match(h.nodes.notice.textContent,pattern);assert.equal(h.nodes.yesterday.children.length,0);}
  const denied=await harness({status:401});assert.equal(denied.redirect(),'/brief-login');
  const old=await harness(response({...fixture,forDate:'2026-09-30',focus:{...fixture.focus,status:'current',task:'Historical work'}}));assert.match(old.nodes.notice.textContent,/does not establish today's priority/);assert.equal(old.nodes['focus-title'].textContent,'Confirm your current priority');
  h.nodes['daily-image'].events.error();assert.equal(h.nodes['image-section'].hidden,true);
  console.log('page_render: complete edition, unknown outcomes, independent top hero, clear retry, separate errors, stale priority and auth redirect passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
