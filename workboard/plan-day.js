'use strict';
// Owner-side planning helper. Reuses the existing private DB connection; no new credentials.
const fs=require('node:fs'),{Pool}=require('pg'),{createStore}=require('./store');
function settings(file){const e={...process.env};if(file)for(const l of fs.readFileSync(file,'utf8').split(/\r?\n/)){const m=l.match(/^(?:export )?([A-Z0-9_]+)=(.*)$/);if(m)e[m[1]]=m[2].trim().replace(/^['"]|['"]$/g,'');}return e;}
async function propose(store,input){
 let s=await store.read();if(!s.personalVersion)throw Error('Personal board unavailable.');
 if(!Array.isArray(input.priorities)||input.priorities.some(t=>typeof t!=='string'||!t.trim()||t.length>200))throw Error('Priorities must be short card titles.');
 const planned=s.lists.find(l=>l.role==='planned'),ids=new Map();
 // Validate the entire proposed plan before making any changes.
 require('./model').mutate(s,'plan.save',{date:input.date,blocks:input.blocks.map(b=>({...b,cardId:null})),note:input.note||'',calendarCheckedAt:input.calendarCheckedAt});
 for(const title of input.priorities){let c=s.cards.find(c=>!c.archived&&c.plannedFor===input.date&&c.title===title&&s.lists.some(l=>!l.archived&&l.id===c.listId));
  if(!c){s=await store.change(s.version,'card.create',{title,listId:planned.id,plannedFor:input.date});c=s.cards.find(c=>c.id===s.target);}ids.set(title,c.id);
 }
 for(let i=input.priorities.length-1;i>=0;i--){const id=ids.get(input.priorities[i]),c=s.cards.find(c=>c.id===id);if(c.listId===planned.id)s=await store.change(s.version,'card.move',{id,listId:planned.id,index:0});}
 const blocks=input.blocks.map(b=>({...b,cardId:ids.get(b.cardTitle)||null}));
 s=await store.change(s.version,'plan.save',{date:input.date,blocks,note:input.note||'',status:'proposed',calendarCheckedAt:input.calendarCheckedAt});return s;
}
async function main(){const args=process.argv.slice(2),file=args.includes('--env-file')?args[args.indexOf('--env-file')+1]:null,e=settings(file),url=e.DATABASE_PUBLIC_URL||e.DATABASE_URL;if(!url)throw Error('Existing database connection unavailable.');const pool=new Pool({connectionString:url,ssl:/localhost|127\.0\.0\.1|railway\.internal/.test(url)?false:{rejectUnauthorized:false},connectionTimeoutMillis:10000});
 try{const store=createStore(pool);const s=args[0]==='propose'?await propose(store,JSON.parse(fs.readFileSync(0,'utf8'))):await store.read();console.log(JSON.stringify({version:s.version,lists:s.lists.filter(l=>!l.archived),cards:s.cards.filter(c=>!c.archived&&s.lists.some(l=>!l.archived&&l.id===c.listId)),plans:s.plans},null,2));}finally{await pool.end();}}
if(require.main===module)main().catch(e=>{console.error('Planning update failed:',e.name==='BoardError'?e.message:'No confirmed plan saved. Check input and the existing private database connection.');process.exitCode=1;});
module.exports={propose};
