from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parents[4];W=Path('/Volumes/Expansion/_edit_work/ds16-publish');v=json.load(open(R/'scripts/blotato/configs/ds16-last-ten-pounds.json'));qa=json.load(open(W/'hq-verification.json'));tik=json.load(open(W/'tiktok-verification.json'));u=json.load(open(W/'uploads.json'));master=json.load(open(W/'master.json'));wait=json.load(open(W/'waiting-list-receipt.json'));drive=(W/'drive-folder-url.txt').read_text().strip()
body=f'''# Last Ten Pounds SFC setup receipt

**Setup completed November 4, 2026. Shared waiting list, planned Saturday January 2, 2027 at 6 PM America/Chicago on YouTube, Facebook, Instagram @danrosefit and TikTok. No live schedules yet: Blotato is full at 200/200.**

DS-16 is an organic dedicated Short by Muhammad. Dan approved V3 November 3 and explicitly approved the HQ export in Upwork November 4 at 6:06 PM Central: “The Last Ten Pounds HQ is perfect, so that one’s done.” Dan selected X2 unchanged: “I like X2. Go ahead and install X2”.

## Exact final master and checks

- Project master: `{master['source']}`.
- Existing downloaded HQ used: `{qa['hq']['path']}`. Muhammad’s source: https://drive.google.com/file/d/1-GGtoEbTEtjn433cZbpc7N4TAP_-9goh/view . No new source video download was needed.
- 69,460,867 bytes; 1080×1920; 30000/1001 fps; 1,540 frames; 51.384667 seconds. SHA-256 `{master['sha256']}`, MD5 `{qa['hq']['md5']}`.
- Every native1080p frame subtracted against approved V3. Average luma difference {qa['picture']['mean_luma_absolute_difference_255']:.4f}/255; worst-frame average {qa['picture']['max_frame_mean_luma_absolute_difference_255']:.4f}/255; zero frames over5. Same frame count, frame rate and duration. Encoding noise only, matching the independent close-out check in `revision docs/shorts-closeout-muhammad-11-4-26.summary.md`.
- Offline aligned stereo PCM correlation {qa['audio']['correlation']:.6f}. Muhammad’s HQ mix retained intact. The close-out session measured -14.4 LUFS / -0.9 dB peak. This setup did not perform or claim audible listening, perceptual audio review or a new full editorial gate pass.
- Actual close: “Try those three tips and let me know how they work for you.” Organic classification confirmed. Dedicated Short, no parent or derivative editing job.

## Backups

- Exact project and Extreme master copies match SHA-256. External master: `{master['external_copy']}`.
- [Google Drive backup folder]({drive}), anyone with link. Remote master byte count and SHA-256 match. Anonymous folder listing positively returned the master and English SRT.
- English SRT saved beside the master on project, Extreme and Drive. Based on approved V3’s unchanged ASR timeline; Zepbound spelling corrected. The film already has burned captions; no second burned caption layer was added.
- Selected covers and setup records are saved with the local delivery and its Extreme/Drive copies.

## Approved X2 and media uploads

- X2 exact full-resolution paired originals installed in `Short-form video content/covers/approved-ds16/` and the delivery folders. Approval/hashes in `picks.json`. No revisions were made after Dan’s pick.
- Instagram cover SHA-256 `{u['instagram_cover']['sha256']}`; YouTube JPEG SHA-256 `{u['youtube_cover']['sha256']}`, {u['youtube_cover']['bytes']:,} bytes, below2MB.
- Facebook’s source registry and live installer contain the exact selected cover, hash-verified, matched to the precise opening caption line.
- TikTok has one X2 frame prepended: {tik['frames_src']}→{tik['frames_out']} frames, {tik['audio_pkts_src']}→{tik['audio_pkts_out']} audio packets, identical copied AAC payload, zero decode errors, first-frame cover PSNR {tik['cover_psnr']:.2f}dB. SHA-256 `{tik['sha256']}`. This preserves all original video frames and the editor’s audio.
- All four uploaded assets were downloaded in full and SHA-256 verified:
'''
for k in ['master','tiktok','instagram_cover','youtube_cover']:body+=f"  - {k}: {u[k]['bytes']:,} bytes, {u[k]['url']}\n"
body+=f'''
## Release package and waiting list

- Config: `scripts/blotato/configs/ds16-last-ten-pounds.json`. Exact YouTube title: **{v['title']}**. Description/social copy assembled from Dan’s recorded words, tracked AbsByAI root links, no free-preview offer. Four account targets only, retired @abs.by.ai mirror excluded.
- Synthetic footage flags true for the approved realistic AI opener. Poolside, kitchen=false, gym=false. Salad is a cutaway. No current dated-calendar GLP-1 hold was found.
- January2 at6PM is the next available allowed Short slot after all live posts, shared-waitlist configurations and named dated-calendar reservations. December10’s approved Fat Millionaire5PM exception uses that day’s evening slot, so no third Short was added there.
- Standard helper dry run found no account/time clash and correctly refused204/200 posts. No post creation was attempted. A single DS-16 entry was added to `scripts/blotato/video_waitlist.json`, read back, and all other entries were verified unchanged. The dated calendar now reserves January2 at6PM for DS-16.
- Four new payloads pass organic and cover guards. Full existing queue cover audit:200 posts, zero issues. Ad scan clean. Existing shared daily `video_topup.py` routine owns later scheduling as four spaces open. No per-video automation was created.
- Pinned comment: “{v['pinned_comment']}”. Saved in config; existing shared daily routine posts/pins it after release. Clean five-passage writer fallback used after Claude CLI authentication expired. No paid writer API used.
- Article: dedicated Short, no article due at setup. Existing shared post-release routine writes a searchable-question article or records a skip.
- Post-release actual cover tiles and pinned status remain future checks with the existing shared routines. Saved cover URLs alone do not prove public tiles.
- Edit Queue remains `finalized`, rev6 with completed setup/waitlist note; Drive status upload confirmed. It is not marked `uploaded` because the four live schedule records do not exist yet. Native Claude mirror remains pending the normal mirror writer.

## Durable evidence and source sync

`/Volumes/Expansion/_edit_work/ds16-publish/` contains HQ comparison, source/derivative hashes, full upload checks, queue snapshots, phase/slot justification, shared-waitlist readback, Drive readbacks and preflight reports. Copies of relevant setup records are beside the master.

Source/config changes are committed locally when possible. Shared live edits and an independently staged article deletion previously blocked the safe GitHub merge; no other owner’s files were adopted, removed or overwritten. A source-sync delay does not mean the media or waiting-list write failed. No further Dan approval is needed for this setup.
'''
(R/'Docs/DS16_SETUP_RECEIPT_20261103.md').write_text(body)
p=R/'Handoffs/handoff-20261103-last-ten-pounds-sfc-setup.md';p.write_text(f'''# Last Ten Pounds SFC Setup: EXECUTED

Completed November4, 2026 in the existing Codex setup chat. Do not start another setup or regenerate covers.

- Final HQ checked against approved V3: all1540 frames match apart from encoding noise. Dan also explicitly approved the HQ on Upwork November4.
- X2 approved unchanged, installed in both layouts and prepared for all four destinations.
- Exact master, subtitle, approved covers and setup records backed up to project, Extreme and [Google Drive]({drive}). Master SHA-256: `{master['sha256']}`.
- Media uploaded and full-download hash-verified; TikTok cover-first copy preserves original AAC payload.
- Blotato is200/200, so DS-16 is on the shared waiting list for Saturday January2, 2027,6PM Central. No live schedules yet. Existing shared daily top-up owns queueing.
- Title, descriptions, pinned question, AI flags, captions record and guards complete. No Dan action needed.

Receipt: `Docs/DS16_SETUP_RECEIPT_20261103.md`. Config: `scripts/blotato/configs/ds16-last-ten-pounds.json`.
''')
p=R/'Handoffs/README.md';s=p.read_text();s='\n'.join(line for line in s.split('\n') if not line.startswith('- [Last Ten Pounds SFC Setup]'));p.write_text(s)
p=R/'AI_COORDINATION.md';s=p.read_text();a=s.index('**LastTen:');b=s.index('\n',a);s=s[:a]+'**LastTen:WAITLIST:2026-11-04:Codex.** X2;HQ-verified;all-media-ready;Jan2 2027 6PM Central,200/200. Shared top-up owns queueing. `Docs/DS16_SETUP_RECEIPT_20261103.md`.'+s[b:];p.write_text(s)
# Review page reports the real release state and preserves approved X2 pictures.
b=R/'Short-form video content/covers/review/ds16-last-ten-pounds-20261103/blind-review';p=b/'index.html';s=p.read_text();s=s.replace('Muhammad’s HQ video export is still pending, so the video is not queued or scheduled.','The HQ video is verified and setup is complete. Blotato is full, so all four destinations are on the shared waiting list for January2, 2027 at6PM Central. No live schedules yet.');p.write_text(s)
p=R/'Short-form video content/covers/review/ds16-last-ten-pounds-20261103/setup-checkpoint.json';d=json.load(open(p));d.update(status='Setup complete; shared waiting list',hq_export=qa['hq'],exact_hq_comparison=qa,scheduled=False,waitlisted=True,planned_release=v['main'],next='Existing shared daily top-up creates four schedules when capacity opens; post-release shared cover/pinned/article checks. No Dan action.');p.write_text(json.dumps(d,indent=2))
# Preserve final receipt and waitlist evidence on both local delivery drives.
D=Path(master['source']).parent;E=Path('/Volumes/Extreme/Short-form video content/How To Lose The Last Ten Pounds Of Fat - DS-16')
for folder in [D/'Setup records',E/'Setup records']:
 shutil.copy2(R/'Docs/DS16_SETUP_RECEIPT_20261103.md',folder/'setup-receipt.md');shutil.copy2(W/'waiting-list-receipt.json',folder/'waiting-list-receipt.json')
print('Final receipt, handoff closure, status board and owner page updated.')
