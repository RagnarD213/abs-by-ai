'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {plan,run}=require('../controller.cjs');
const catalog=[{id:'gpt-6-sol',efforts:['high']},{id:'gpt-6.1-sol',efforts:['high']},{id:'gpt-6-astra',efforts:['high','max']}];
const input={jobId:'TEST',oldThreadId:'old',oldHostId:'local',projectId:'project',repoPath:'/test',title:'Sample',type:'LFC',round:2,
  revisionId:'message-1',revisions:'Trim the opening',handoffPath:'/test/handoff.md',journalPath:'/test/round3/round-controller.json',
  decisionsPath:'/test/decisions.json',approvedFiles:[{path:'/test/decisions.json',sha256:'a'.repeat(64)}],work:'heavy',contextFraction:0.5,replyMinutes:5,
  currentModel:'gpt-6-astra',currentThinking:'max'};
const caps=['list_projects','list_threads','read_thread','set_thread_title','move_thread_to_sidebar_section','create_thread','send_message_to_thread'].map(n=>'mcp__codex_app__'+n);
function fixture(opts={}) {
  let state=null;const calls=[],pins=new Set(['old','unrelated']);let title=opts.oldTitle||'Sample LFC R2';
  return {calls,pins,get state(){return state},
    deps:{verifyLocks:async()=>{if(opts.hashFailure)throw Error('hash changed')},
      store:{load:async()=>state,cas:async(expected,next)=>{assert.equal(state?.revision??null,expected);state=structuredClone(next)}},
      call:async(name,args)=>{
        name=name.replace('mcp__codex_app__','');calls.push([name,args]);
        if(name==='list_threads')assert(args.limit<=50,'Supported app limit is 50; pinned threads are always included');
        if(opts.fail===name)throw Error('network lost');
        if(name==='list_projects')return{projects:[{projectId:'project',path:opts.projectPath||'/test',hostId:'local'}]};
        if(name==='list_threads')return{pinnedThreads:[...pins].map(id=>({id,kind:'codex',hostId:'local',cwd:opts.oldCwd||'/test',title:id==='old'?title:'Sample LFC R3'})),threads:[{id:'old',kind:'codex',hostId:'local',cwd:opts.oldCwd||'/test',title}]};
        if(name==='create_thread')return opts.pendingCreate?{clientThreadId:'pending'}:{threadId:'child',hostId:'local'};
        if(name==='read_thread')return{thread:{id:'child',hostId:'local',cwd:opts.childCwd||'/test'},turns:opts.notStarted?[]:[{id:'turn',status:'inProgress',startedAt:123}]};
        if(name==='set_thread_title')title=args.title;
        if(name==='move_thread_to_sidebar_section') {
          if(args.sectionId==='pinned'){if(!opts.pinNotApplied)pins.add(args.threadId)}else pins.delete(args.threadId);
        }
        return{success:true};
      }} };
}
const exec={authorized:true,capabilities:caps};
test('newest supported Sol/high replaces inherited Astra/max',()=>{const p=plan(input,catalog);assert.equal(p.model,'gpt-6.1-sol');assert.equal(p.thinking,'high');assert.equal(p.nextTitle,'Sample LFC R3')});
test('numeric catalog ordering, no invented IDs or preview aliases',()=>{const p=plan(input,[...catalog,{id:'gpt-6.10-sol',efforts:['high']},{id:'gpt-99-sol-preview',efforts:['high']}]);assert.equal(p.model,'gpt-6.10-sol')});
test('explicit model and effort preserved; unavailable override fails',()=>{assert.equal(plan({...input,override:{model:'gpt-6-astra',thinking:'max'}},catalog).thinking,'max');assert.throws(()=>plan({...input,override:{model:'not-real'}},catalog),/unavailable/)});
test('catalog unavailable uses disclosed known baseline; empty Sol catalog blocks',()=>{assert.match(plan(input,null).catalogSource,/unavailable/);assert.throws(()=>plan(input,[catalog[2]]),/no available/);assert.throws(()=>plan(input,[]),/no available/)});
test('small recent work continues; context, delay, struggle, heavy stage choose fresh',()=>{const small={...input,work:'small',contextFraction:.2};assert.equal(plan(small,catalog).mode,'same');for(const change of [{contextFraction:.45},{replyMinutes:90},{struggled:true},{work:'heavy'},{contextFraction:null}])assert.equal(plan({...small,...change},catalog).mode,'fresh')});
test('dry run has no task/journal calls',async()=>{const f=fixture();await run(plan(input,catalog),f.deps,{dryRun:true});assert.equal(f.calls.length,0);assert.equal(f.state,null)});
test('fresh create -> started/pin verification -> old unpin; unrelated preserved; idempotent repeat',async()=>{
  const f=fixture(),p=plan(input,catalog),s=await run(p,f.deps,exec);
  assert.equal(s.productionOwner,'child');assert.equal(s.supersededBy,'child');assert(f.pins.has('child'));assert(f.pins.has('unrelated'));assert(!f.pins.has('old'));
  const names=f.calls.map(x=>x[0]),unpin=f.calls.findIndex(x=>x[0]==='move_thread_to_sidebar_section'&&x[1].sectionId===null);
  assert(names.indexOf('create_thread')<names.indexOf('read_thread'));assert(names.indexOf('read_thread')<unpin);
  const before=f.calls.length;await run(p,f.deps,exec);assert.equal(f.calls.length,before);
  assert.deepEqual(s.plan.approvedFiles,input.approvedFiles);
});
test('creation timeout is durable pending and cannot duplicate',async()=>{const f=fixture({fail:'create_thread'}),p=plan(input,catalog);await assert.rejects(run(p,f.deps,exec),/network/);assert.equal(f.state.pending.action,'create_thread');await assert.rejects(run(p,f.deps,exec),/Uncertain/);assert.equal(f.calls.filter(x=>x[0]==='create_thread').length,1);assert(f.pins.has('old'));assert.equal(f.state.productionOwner,null)});
test('clientThreadId is never treated as a ready child or retried',async()=>{const f=fixture({pendingCreate:true}),p=plan(input,catalog);await assert.rejects(run(p,f.deps,exec),/exact ready/);await assert.rejects(run(p,f.deps,exec),/Uncertain/);assert(f.pins.has('old'))});
test('unverified start or pin retains old pin, no production owner',async()=>{for(const opt of [{notStarted:true},{pinNotApplied:true}]){const f=fixture(opt);await assert.rejects(run(plan(input,catalog),f.deps,exec),/verified/);assert(f.pins.has('old'));assert.equal(f.state.productionOwner,null)}});
test('missing pin capability or changed hashes causes zero mutations',async()=>{for(const opt of [{},{hashFailure:true}]){const f=fixture(opt);await assert.rejects(run(plan(input,catalog),f.deps,{...exec,capabilities:opt.hashFailure?caps:[] }));assert.equal(f.calls.length,0)}});
test('same task renames and keeps pin, queues Sol/high next turn once, creates no child',async()=>{const f=fixture(),p=plan({...input,work:'small',contextFraction:.2},catalog),s=await run(p,f.deps,exec);assert.equal(s.phase,'continuation_queued');assert.equal(s.productionOwner,'old');assert(f.pins.has('old'));assert(!f.calls.some(x=>x[0]==='create_thread'));const send=f.calls.find(x=>x[0]==='send_message_to_thread');assert.equal(send[1].model,'gpt-6.1-sol');assert.equal(send[1].thinking,'high');await run(p,f.deps,exec);assert.equal(f.calls.filter(x=>x[0]==='send_message_to_thread').length,1)});
test('same Sol/high task continues inline without messaging or new task',async()=>{const f=fixture(),p=plan({...input,work:'small',contextFraction:.2,currentModel:'gpt-6.1-sol',currentThinking:'high'},catalog);const s=await run(p,f.deps,exec);assert.equal(s.phase,'complete');assert(!f.calls.some(x=>['create_thread','send_message_to_thread'].includes(x[0])))});
test('changed revision packet cannot create second child for reserved round',async()=>{const f=fixture();await run(plan(input,catalog),f.deps,exec);await assert.rejects(run(plan({...input,revisions:'different'},catalog),f.deps,exec),/different packet/);assert.equal(f.calls.filter(x=>x[0]==='create_thread').length,1)});
test('child wake uncertainty blocks resend despite completed pin transfer',async()=>{const f=fixture({fail:'send_message_to_thread'}),p=plan(input,catalog);await assert.rejects(run(p,f.deps,exec),/network/);await assert.rejects(run(p,f.deps,exec),/Uncertain/);assert.equal(f.calls.filter(x=>x[0]==='send_message_to_thread').length,1);assert.equal(f.state.productionOwner,'child')});
test('unrelated predecessor title blocks creation and unpin',async()=>{const f=fixture({oldTitle:'Other Video LFC R2'});await assert.rejects(run(plan(input,catalog),f.deps,exec),/unrelated task/);assert(f.pins.has('old'));assert(!f.calls.some(x=>x[0]==='create_thread'))});

test('filesystem-verified symlink aliases retain task and host checks',async()=>{
 const f=fixture({projectPath:'/old-alias',oldCwd:'/canonical',childCwd:'/canonical'});
 const pairs=[];f.deps.verifyRepoPath=async(a,b)=>{pairs.push([a,b]);return ['/old-alias','/canonical','/test'].includes(a)&&b==='/test'};
 const s=await run(plan(input,catalog),f.deps,exec);assert.equal(s.productionOwner,'child');assert(pairs.some(x=>x[0]==='/old-alias'));assert(pairs.some(x=>x[0]==='/canonical'));
});
test('unverified or unrelated repository aliases never create a task',async()=>{
 for(const resolver of [undefined,async()=>false]){
  const f=fixture({projectPath:'/unrelated'});f.deps.verifyRepoPath=resolver;
  await assert.rejects(run(plan(input,catalog),f.deps,exec),/Project path/);assert(!f.calls.some(x=>x[0]==='create_thread'));assert(f.pins.has('old'));
 }
});
