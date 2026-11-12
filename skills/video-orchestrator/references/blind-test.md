# Three-way trial protocol

Authorized November 11, 2026. First job: **The Only 5 Machines You Need At The
Gym (DS-98)**, CONTENT/SFC. One dedicated vertical Short per arm, no derivatives,
covers, setup or publishing. The handoff is the film brief.

## Freeze equal inputs; leave creative decisions independent

Preparation leaves the queue READY with unattended execution disabled. Actual
launch checks ownership and claims one DS-98 job, one controller. Workers never
update the shared queue, board, libraries, global approvals or Git. Use the
current edit cap and render queue; serial arm production is the default.

Verify Extreme sources/hashes, roll sidecars and current approved library
masters. DS-98's map retains intake-era B-roll wording: the handoff's approved
permanent IDs govern eligibility. Freeze the handoff/map, transcripts/sidecars,
source/library manifest with hashes, rule versions, and common output settings.
Each arm gets the same entire take/hook universe, not a controller-selected EDL
or treatment. Reuse read-only preprocessing identically and charge it separately.
Never share another arm's plan, cut, fixes, metrics or newly created treatments.

Work media uses `renderq.py workdir DS-98-blind --need <honest GB>` and disjoint
arm directories. Controller-only state/logs go outside the public repository,
e.g. `~/.codex/video-trials/DS-98/`. Initialize after verified manifests exist:

```text
python3 <skill>/scripts/trial.py init <private-dir> --job DS-98 --brief <handoff> --source-map <map> --input assets=<verified-assets.json> --input rules=<rule-versions.json>
```

`init` freezes small files and randomizes execution order; it does not verify
media, launch agents, render or claim the job. Do not initialize twice. Keep
trial.json private from Dan's page and other arms. Run `verify` after resume.

## Model arms

| Arm | Planning/editor/self-QA | Fresh complete-candidate reviewer |
| --- | --- | --- |
| all_astra | Astra high | Astra high |
| all_sol | GPT-6.1 Sol high | GPT-6.1 Sol high |
| hybrid | Astra high directs; Sol high produces | Astra high |

Baseline agents don't receive the orchestrator's editorial plan. No unrequested
helpers; any mandatory helper uses that arm's model. Same-model independent
review remains required; all-Sol is not self-review. Hybrid uses the skill and
one fresh Sol editor with bounded Astra stage/exception work. If a mandatory
specialized check requires another provider/model, use the same check for all
arms as common evaluation and disclose this exception to "all". Shared image/
audio generation providers aren't editorial agents. All existing paid caps are
shared across the trial, not multiplied by three; subscription-first stays.
Reserve equal per-arm shares of any scarce generation/spending budget before
running arms; common approved asset generation is charged separately. Don't
let the first arm consume another arm's allowance or silently give a retry
subsidy to one arm.

The neutral root controller is common administrative overhead, logged as
`shared`. Start three isolated production owners as sibling contexts; hybrid's
Astra supervisor is separate from that controller and can spawn its own Sol
editor. Do not reuse a controller that has read baseline outputs as hybrid's
creative director. Thus "all" describes all editorial work/review within that
arm; common clerical coordination is disclosed separately. Never send baseline
outputs or conclusions into hybrid or another baseline's context.

## Same approval stages, blind presentation

First review follows SFC rules: opening/current-section preview, color and
level-matched voice/crop options, and every proposed graphic/clip in context.
Don't impose a long-form first minute or pad this Short. The existing whole-
Short exception applies only when its approval conditions are met. New AI
start/end pairs still precede motion generation. Keep the shared decision budget.

Show the three arms together at each required stage using randomized X1/X2/X3
labels and nested neutral IDs for options. Record actual Dan decisions by stage,
label and file hash. Route general instructions equally before resuming;
arm-specific corrections stay with that arm. Don't force one arm's creative
choices on others. Preserve first-presented cuts before feedback; post-feedback
results measure repairs, not independent first-cut quality.

Every candidate needs identical applicable exact-file checks and independent
review. Record failed/incomplete arms and their cost; don't omit them or call a
two-way result complete. Never relax checks to finish the experiment.

Use 1080p, neutral names/URLs, and no model/usage/identity-bearing notes or media
metadata on the page. Keep identities sealed until Dan judges all three final
candidates, unless he explicitly asks to reveal earlier. Use the maintained
review server/player: silent checks, verified pause, sound-ready handoff.

## Capture evidence

Register every fresh production session, descendants, retries and continuations:

```text
python3 <skill>/scripts/trial.py log <private-dir> --arm hybrid --role editor --file <native-session.jsonl>
python3 <skill>/scripts/trial.py usage <private-dir>
```

Roles: editor, coordinator, reviewer, helper. Hybrid editor/helper = Sol;
coordinator/reviewer = Astra. Shared preprocessing/evaluation uses arm shared
with `--model <actual-model>`. Native logs verify observed model/effort; CLI
exports alone don't prove these settings. Only one log representation per
session. Use sessions that contain no unrelated prior work. Reconcile actual
runtime agents with the registry at every stage and explicitly record missing
logs. `usage` is controller-only and contains identities.

Record Dan's real preference/notes on hook, pacing, takes, graphics, teaching
clarity and sound; hard defects; first-pass QA; reviewer findings; repairs;
approval rounds; active/render/queue/approval-wait time; all session token
counters; actual external charges and Flow credits when exposed. Unknown stays
blank. Don't invent listening passes or quality scores. Tool pass != approval.

```text
python3 <skill>/scripts/trial.py checks-template > <checks.json>
python3 <skill>/scripts/trial.py artifact <private-dir> --arm hybrid --stage first-review --file <checked-preview.mp4> --checks <filled-checks.json>
python3 <skill>/scripts/trial.py blind <private-dir> --stage first-review
```

The helper requires three checked files, removes metadata/chapters by remuxing,
hashes the exact neutral files, and creates a neutral manifest and blank ballot.
Remuxing changes file bytes. The initial manifest has `ready_for_owner: false`.
Run every applicable exact-file check on each **neutral MP4**, bind its checks
to `review_file_sha256`, then register them with:

```text
python3 <skill>/scripts/trial.py neutral-check <private-dir> --stage first-review --label X1 --checks <neutral-X1-checks.json>
```

Repeat for X2 and X3. Only three passing neutral checks set `ready_for_owner`
true. Do not deliver the page earlier or reuse source-file stamps for the remux.
Build the managed page from that manifest, never trial.json. Serve **only** the
stage review directory; the key/logs live outside it. The helper handles the
primary cut only: give every supplementary color/audio/context asset neutral
names, stripped metadata and a secret mapping too. Don't serve symlinks back to
private arm folders. Never overwrite a presented stage; use a new stage name.

Before blinding, fill editor picture/audio/source checks with real evidence.
Use overall status `ready_for_blinding` and independent-review status
`pending_neutral_file`: the one fresh independent reviewer checks the final
neutral file after packaging. Do not pay for a duplicate independent review of
the source export merely to package it. An already reviewed source can instead
be recorded as `pass`, but it does not waive final neutral-file verification.
Save first-pass status and later fixes in checks history.
The quality record also carries reviewer findings, repairs, approval rounds,
timings, external spend and missing evidence; preserve unavailable values as null.

Fill the blank ballot from Dan's actual response before revealing identities:

```text
python3 <skill>/scripts/trial.py reveal <private-dir> --stage candidate --ballot <Dan-ballot.json>
```

Final stage names end in `candidate`. Early reveal requires explicit Dan
direction and `--early-reveal-reason` containing that direction. Rank all three
and retain notes; ties use grouped labels, e.g. `[["X1","X2"],["X3"]]`.
An explicit early reveal can keep ranking empty and is recorded as unjudged.
Dan's preference is the main artistic result; checks set the
technical floor. Compare hybrid to each baseline separately using known raw
tokens and Astra tokens, with missing coverage and common overhead separate.
No credit/dollar conversion unless measured. One Short is a pilot, not a broad
model benchmark. Picking a winner isn't final-film approval.

Controller alone updates DS-98: in_progress at launch; draft_review while
choices wait; delivered only when all complete candidates reach Dan. Finalized
requires his explicit approval of an exact film. No setup or publishing here.
