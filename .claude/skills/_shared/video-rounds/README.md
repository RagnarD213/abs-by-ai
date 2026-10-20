# Automatic video rounds

Dan authorized this workflow on 2026-10-20. His revisions trigger the next round. The editor chooses same task or fresh task and operates the supported task tools itself. Dan does not fire cards or manage pins. This module is invoked by the editor on a real revision; it is not a background watcher, scheduled task, or a replacement for media approvals.

## Invocation in a Codex turn

Read this runbook and the controller first. Prepare a self-contained handoff, Dan's exact decisions, immutable approval manifest, and new round folder. The decisions file itself must be in the SHA256 manifest. Record content/ad category, scope, timeline changes, prior applied cuts, costs, gate evidence, expected hashes, and previous task ID in the handoff. Never overwrite reviewed media. The current editor must stop production and release its existing queue claim before transfer. The child must acquire the existing queue claim if applicable; this journal does not bypass the queue's production ownership or build cap.

Make `input` with exact fields shown in `tests/controller.test.cjs`, replacing every fixture value with verified production identity. Use an absolute `journalPath` ending in `roundN/round-controller.json` under this video's work directory. It must be the SAME path for every attempt to advance this delivered round, including revisions that arrive during recovery. Never allocate a second journal for an uncertain transition. The key is `<jobId>:R<next>`; a different packet for the same reserved round is blocked. `revisionId` is the actual owner message ID or saved submission ID, never a timestamp invented on retry. `repoPath` must equal the path from `list_projects`. Do not supply an override merely because this task used Astra. Only Dan's explicit instruction for this round or all rounds becomes `override`.

Use this pattern inside `functions.exec`, where the native tool facade exists. No external/private RPC bridge is needed. The loader reads only these reviewed repo modules. Shell arguments in the adapter use single-quote escaping.

```js
const repo = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
async function loadModule(name) {
  const result = await tools.exec_command({
    cmd: "cat '" + repo + "/.claude/skills/_shared/video-rounds/" + name + "'",
    max_output_tokens: 16000
  });
  if (result.exit_code !== 0) throw Error(result.output);
  const mod = {exports:{}};
  new Function('module', result.output)(mod);
  return mod.exports;
}
const controller = await loadModule('controller.cjs');
const adapter = await loadModule('adapter.cjs');
const metadata = ALL_TOOLS.find(x => x.name === 'mcp__codex_app__create_thread');
const catalog = metadata ? controller.catalogFromDescription(metadata.description) : null;
const proposal = controller.plan(input, catalog);
// First inspect the plan. This call performs zero tool or journal operations:
text(await controller.run(proposal, {}, {dryRun:true}));
// On an actual authorized owner revision, execute, do not ask Dan to fire a card:
const result = await controller.run(proposal, adapter(tools,repo,input.journalPath), {
  authorized:true, capabilities:ALL_TOOLS.map(x=>x.name)
});
text(result);
```

This example requires the editor to construct `input`; it must never execute merely because this runbook was opened. Workflow installation/testing is not an edit request. Inspect the dry-run result in a separate tool call before executing. Do not print the whole decisions/manifest if it contains private material.

## What it enforces

- Small, recent revisions with known/estimated context under 40% keep the same task. Heavy stages, stale replies, repeated failures or context pressure choose a fresh task. State context estimates honestly; account usage percentages are not context usage. Do not fabricate `get_usage` availability.
- Resolve the highest numeric stable Sol ID supporting high from the current destination/client catalog. Native `create_thread` metadata is the supported catalog available here. No speculative future IDs. If unavailable, disclose the known `gpt-6.1-sol` baseline. If a catalog exists but has no compatible Sol, stop rather than downgrade. Explicit model/effort overrides win.
- Same task: next round/title, preserve pin, keep the production owner. If the active model/effort differs, enqueue exactly one native follow-up with Sol/high, then stop the old turn. The change applies to the queued turn, never the active inference. A supported immediate model setter can be used instead if actually exposed later.
- Fresh task: suspend parent production, create once in the existing local project, save exact ready ID, pin child, read started turn, verify pin from `pinnedThreads`, recheck hashes, unpin only the recorded old task, verify both pins, record superseded pointers and one production owner, wake the child once. Child bootstrap is read-only until ownership transfer. Old task ends after transfer.
- Durable CAS before external mutations prevents racing controllers. A timeout/crash/ambiguous result leaves `pending` and blocks blind retries. `clientThreadId` is never treated as `threadId`. The old task remains pinned until child start and pin are verified. Unrelated pins and task data are never changed; no archive/delete operation exists here.

## Recovery and capability limits

On `pending`, inspect the exact saved action and its original tool output. For create, use the returned thread ID if present and `read_thread` on that exact ID. If only a client ID exists, inspect the app's setup status and locate the ready thread via supported listing. Verify project/host, next-round title, starter's journal key, revision ID and parent ID. Do not infer identity from title alone. Never issue another create while the outcome is unknown. If the exact task cannot be recovered, report the blocked action; keep old pin and suspend production. For send/pin/unpin/rename, read the saved exact target and inspect current state before deciding whether the operation ran. Do not blindly resend a continuation. Recovery currently requires the editor to reconcile the journal with supported read-back evidence; the controller deliberately fails closed rather than guess an uncertain outcome.

On a read-only verification failure, the known child ID stays saved and rerunning resumes it without creating again. On a pending mutation, do not edit away `pending` until evidence resolves it. Use `journal.py cas` with the expected revision to checkpoint a verified outcome; preserve the packet, child ID and audit evidence. For a create recovery, transition to `created` only with exact ready IDs and verified starter identity. Do not change approval hashes to make verification pass.

Verified on this Mac mini, 2026-10-20: native `create_thread`, `send_message_to_thread` support model/thinking; `move_thread_to_sidebar_section` supports `pinned` and null; `list_threads` returns all pinned tasks; `read_thread` returns identity and `turns[].startedAt`. Read-only calls succeeded. The tool metadata currently lists `gpt-6.1-sol` with high. `read_thread` does not expose the active model, so accepted explicit creation arguments are evidence of the requested configuration, not independent active-model inspection. No private database or app-server store was used. Claude's previously disabled start-session tool is not assumed fixed; Claude must use actually available supported controls or report the limitation with the old pin retained.

No real edit or disposable task was created/pinned/unpinned during installation. End-to-end desktop mutation verification still needs a separately authorized disposable test task, with a harmless prompt. Unit tests exercise actual controller ordering and failures using fake tool responses; they do not prove live app mutation behavior.

## Tests

```sh
node --test .claude/skills/_shared/video-rounds/tests/controller.test.cjs
python3 -m unittest discover -s .claude/skills/_shared/video-rounds/tests -p 'test_*.py'
```

Tests use only memory and temporary files, with no model calls, media renders, queue changes or task mutations.
