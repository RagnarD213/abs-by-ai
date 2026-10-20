/* Agent-side controller. No private app storage, credentials, or background worker. */
'use strict';
const prefix = 'mcp__codex_app__';
function unwrap(r) {
  if (r?.isError) throw new Error(JSON.stringify(r));
  if (r?.structuredContent) return r.structuredContent;
  const block = r?.content?.find(x => x.type === 'text');
  if (block) { try { return JSON.parse(block.text); } catch { throw new Error(block.text); } }
  return r;
}
function check(ok, message) { if (!ok) throw new Error(message); }
function catalogFromDescription(description) {
  const models = [...description.matchAll(/\b(gpt-\d+(?:\.\d+)*-(?:sol|astra|luna|terra))\s*\([^)]*supported reasoning efforts: ([^)]*)\)/g)]
    .map(m => ({id:m[1], efforts:m[2].split(',').map(x=>x.trim())}));
  return models.length ? models : null;
}
function plan(input, catalog) {
  check(input.jobId && input.oldThreadId && input.oldHostId && input.projectId, 'Missing exact job/thread/host/project identity');
  check(Number.isInteger(input.round) && input.round >= 1, 'Invalid round');
  check(input.title && input.type && input.revisionId && input.revisions && input.handoffPath && input.journalPath, 'Missing round packet');
  check(Array.isArray(input.approvedFiles) && input.decisionsPath, 'Missing approval manifest or decisions file');
  check(input.approvedFiles.some(x => x.path === input.decisionsPath) && input.approvedFiles.every(x => x.path && /^[a-f0-9]{64}$/.test(x.sha256)), 'Manifest must include decisions and exact SHA256s');
  const available = Array.isArray(catalog);
  let model = input.override?.model;
  if (!model) {
    const sol = (catalog || []).filter(x => /^gpt-\d+(?:\.\d+)*-sol$/.test(x.id) && x.efforts.includes('high'));
    sol.sort((a, b) => {
      const av = a.id.slice(4, -4).split('.').map(Number), bv = b.id.slice(4, -4).split('.').map(Number);
      for (let i = 0; i < Math.max(av.length, bv.length); i++) if ((av[i] || 0) !== (bv[i] || 0)) return (bv[i] || 0) - (av[i] || 0);
      return 0;
    });
    model = available ? sol[0]?.id : 'gpt-6.1-sol';
  }
  const thinking = input.override?.thinking || 'high';
  check(model, 'Catalog has no available Sol/high model; do not guess or silently downgrade');
  if (available) check(catalog.some(x => x.id === model && x.efforts.includes(thinking)), 'Explicit/default model and effort unavailable');
  check(['small', 'heavy'].includes(input.work), 'Classify remaining stage as small or heavy');
  const same = input.work === 'small' && Number.isFinite(input.contextFraction) && input.contextFraction < 0.4 &&
    Number.isFinite(input.replyMinutes) && input.replyMinutes <= 60 && !input.struggled && !input.requiresFreshTask;
  const mode = same ? 'same' : 'fresh';
  return {...input, model, thinking, mode, catalogSource: available ? 'supported runtime catalog' : 'known baseline; catalog unavailable',
    key: `${input.jobId}:R${input.round + 1}`, nextRound: input.round + 1,
    nextTitle: `${input.title} ${input.type} R${input.round + 1}`,
    reason: same ? 'Small contained work, recent reply, context below 40%' : 'Stage/context warrants a fresh task; preserve prior round',
    queueContinuation: same && (input.currentModel !== model || input.currentThinking !== thinking)};
}
async function run(p, {call, store, verifyLocks}, options = {}) {
  // dryRun performs zero reads/writes or task calls, so it can be safely used on production inputs.
  if (options.dryRun) return {dryRun: true, plan: p};
  check(options.authorized === true, 'Execution requires the actual revision trigger, not a workflow implementation test');
  for (const name of ['list_projects','list_threads','read_thread','set_thread_title','move_thread_to_sidebar_section',
    ...(p.mode === 'fresh' ? ['create_thread','send_message_to_thread'] : p.queueContinuation ? ['send_message_to_thread'] : [])]) {
    check(options.capabilities?.includes(prefix + name), `Required supported capability unavailable: ${name}; retain old pin`);
  }
  await verifyLocks(p.approvedFiles, p.decisionsPath);
  let s = await store.load();
  if (!s) {
    s = {schemaVersion: 1, revision: 0, key: p.key, plan: p, phase: 'prepared', productionOwner: null,
      previousOwner: p.oldThreadId, child: null, pending: null, supersededBy: null};
    await store.cas(null, s);
  }
  check(s.key === p.key, 'Journal belongs to another round');
  check(JSON.stringify(s.plan) === JSON.stringify(p), 'Round already reserved with a different packet; reconcile it before continuing');
  check(!s.pending, `Uncertain ${s.pending?.action} outcome. Reconcile exact target/result before resuming; never recreate/resend blindly`);
  if ((s.phase === 'complete' && (p.mode === 'same' || s.wakeSent)) || s.phase === 'continuation_queued') return s;
  async function save(changes) {
    const next = {...s, ...changes, revision: s.revision + 1};
    await store.cas(s.revision, next); s = next;
  }
  async function read(name, args) { return unwrap(await call(prefix + name, args)); }
  async function mutate(name, args, changes) {
    await save({pending: {action: name, args}}); // CAS wins before any external mutation.
    const r = await read(name, args);
    check(r && r.success !== false && !r.error && !r.isError, `Unconfirmed ${name}; journal remains pending`);
    const delta = typeof changes === 'function' ? changes(r) : changes;
    await save({...delta, pending: null});
    return r;
  }
  const projects = await read('list_projects', {});
  const project = projects.projects?.find(x => x.projectId === p.projectId);
  check(project?.path === p.repoPath && project?.hostId === p.oldHostId, 'Project path/host mismatch; do not create elsewhere');
  let listing = await read('list_threads', {limit: 100});
  const find = (l, id, host) => [...(l.pinnedThreads || []), ...(l.threads || [])].find(x => x.id === id && x.hostId === host && x.kind === 'codex');
  const isPinned = (l, id, host) => (l.pinnedThreads || []).some(x => x.id === id && x.hostId === host && x.kind === 'codex');
  let old = find(listing, p.oldThreadId, p.oldHostId);
  if (!old) old = (await read('read_thread',{threadId:p.oldThreadId,hostId:p.oldHostId,turnLimit:1,includeOutputs:false})).thread;
  check(old && old.cwd === p.repoPath, 'Old task identity or repo cannot be verified');
  check(old.id === p.oldThreadId && old.hostId === p.oldHostId &&
    (old.title === `${p.title} ${p.type} R${p.round}` || (p.mode === 'same' && s.phase !== 'prepared' && old.title === p.nextTitle)),
    'Old task title/round does not match this video; never unpin an unrelated task');
  const threadArgs = (id, host) => ({threadId: id, hostId: host, source: 'codex'});
  const starter = `Name this task ${p.nextTitle}. Use ${p.model} at ${p.thinking} effort.\n` +
    `Video ${p.jobId}, round ${p.nextRound}. Revision ${p.revisionId}.\nRead AGENTS.md, VIDEO-RULES.md, ` +
    `${p.handoffPath} and ${p.decisionsPath}. Preserve every approved file/hash and Dan's exact decisions.\n` +
    `Round controller journal: ${p.journalPath}; key: ${p.key}. Before production, verify productionOwner is ` +
    `your exact task ID and the round is complete (or continuation_queued for same-task next turn). ` +
    `If transfer is still pending, prepare read-only, then stop. Do not render or generate until ownership is recorded.\n` +
    `Process revision ${p.revisionId} only once for ${p.key}. If already in progress, resume its checkpoint; ` +
    `if delivered, do not execute it again. Record that disposition in the round decisions.\n` +
    `Previous task: ${p.oldThreadId}. Revisions:\n${p.revisions}\n` +
    `No publishing, spending, new credentials, archive/delete, or unrelated changes authorized by this handoff.`;
  if (p.mode === 'same') {
    if (s.phase === 'prepared') await mutate('set_thread_title', {threadId: p.oldThreadId, source: 'codex', title: p.nextTitle}, {phase: 'renamed'});
    if (s.phase === 'renamed') await mutate('move_thread_to_sidebar_section', {...threadArgs(p.oldThreadId, p.oldHostId), sectionId: 'pinned'}, {phase: 'pinned'});
    listing = await read('list_threads', {limit: 100});
    check(isPinned(listing, p.oldThreadId, p.oldHostId) && find(listing,p.oldThreadId,p.oldHostId)?.title === p.nextTitle, 'Same-task name/pin not verified');
    if (p.queueContinuation) {
      await mutate('send_message_to_thread', {threadId:p.oldThreadId, hostId:p.oldHostId, prompt:starter, model:p.model, thinking:p.thinking},
        {phase:'continuation_queued', productionOwner:p.oldThreadId});
      // Active inference cannot change model. Stop here; production resumes in the queued turn.
    } else await save({phase:'complete', productionOwner:p.oldThreadId});
    return s;
  }
  if (s.phase === 'prepared') {
    await mutate('create_thread', {title:p.nextTitle, model:p.model, thinking:p.thinking, prompt:starter,
      target:{type:'project', projectId:p.projectId, environment:{type:'local'}}}, r => {
      check(r.threadId && r.hostId && r.threadId !== p.oldThreadId, 'Creation lacks exact ready threadId/hostId; inspect pending clientThreadId, never recreate');
      return {phase:'created', child:{threadId:r.threadId,hostId:r.hostId}};
    });
  }
  check(s.child && s.child.threadId !== p.oldThreadId && s.child.hostId === p.oldHostId, 'Invalid child identity');
  const child = s.child;
  if (s.phase === 'created') await mutate('move_thread_to_sidebar_section', {...threadArgs(child.threadId,child.hostId), sectionId:'pinned'}, {phase:'pinned'});
  const observation = await read('read_thread', {threadId:child.threadId,hostId:child.hostId,turnLimit:1,includeOutputs:false});
  check(observation.thread?.id === child.threadId && observation.thread?.hostId === child.hostId && observation.thread?.cwd === p.repoPath,
    'New task identity/repo not verified');
  check(observation.turns?.some(t => t.startedAt != null && t.status !== 'failed' && !t.error), 'New task has no verified started turn');
  listing = await read('list_threads', {limit:100});
  check(isPinned(listing,child.threadId,child.hostId) && find(listing,child.threadId,child.hostId)?.title === p.nextTitle,
    'New task title/pin not verified; old task stays pinned');
  // Re-check immutable approvals immediately before transferring production ownership.
  await verifyLocks(p.approvedFiles,p.decisionsPath);
  if (s.phase === 'pinned') await save({phase:'verified', startedTurn:observation.turns[0].id, pinVerified:true});
  if (s.phase === 'verified') {
    // Only this packet's old task is eligible; no reorder or bulk/sidebar operations.
    await mutate('move_thread_to_sidebar_section', {...threadArgs(p.oldThreadId,p.oldHostId),sectionId:null}, {phase:'unpinned'});
  }
  listing = await read('list_threads',{limit:100});
  check(!isPinned(listing,p.oldThreadId,p.oldHostId) && isPinned(listing,child.threadId,child.hostId), 'Final pin transfer not verified');
  await save({phase:'complete',productionOwner:child.threadId,supersededBy:child.threadId,supersedes:p.oldThreadId,
    modelVerification:'Explicit model/effort accepted by create_thread; read_thread does not expose active model'});
  // A child may already have stopped after its bootstrap. Wake it exactly once after ownership transfer.
  // This is a continuation of the created task, never a second task.
  check(options.capabilities.includes(prefix+'send_message_to_thread'), 'Transfer complete; child wake capability missing');
  await mutate('send_message_to_thread',{threadId:child.threadId,hostId:child.hostId,
    prompt:`Ownership transferred for ${p.key}, revision ${p.revisionId}. Re-read ${p.journalPath}, verify your ID is productionOwner, then execute ${p.handoffPath}. If this revision is already in progress, resume its checkpoint; if delivered, acknowledge without reapplying any edit.`,
    model:p.model,thinking:p.thinking},{phase:'complete',wakeSent:true});
  return s;
}
module.exports = {plan,run,unwrap,catalogFromDescription};
