from pathlib import Path
import json,hashlib
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];Q=W/'review';V=Q/'Home Workouts SFC R2 - 1080p.mp4'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=json.load(open(str(V)+'.deliver_gate.json'));a=json.load(open(str(V)+'.audio_gate.json'));w=json.load(open(W/'evidence/watch.json'))
fail='\n'.join('- '+k+': '+v.get('detail','') for k,v in d['rows'].items() if not v['ok'])
text=f'''# Home Workouts SFC R2

CONTENT dedicated Short. Full61.428033s /1841frames at30000/1001,1080x1920, burned J2 captions plus optional SRT. Rendered for Dan's review, not finalized or published. Exact master SHA256:{sha(V)}. Phone SHA256:{sha(Q/'Home Workouts SFC R2 - REVIEW 540p.mp4')}.

## Approved choices and preservation

Dan's exact November2 instruction: “Go with Colour B and Gentle Bass voice. I approve the opening and inserts. Fix the remaining issues and finish the full Short.” Revision01a19c75-b53d-7871-9f4d-cb668400fc13, sole production owner01a19c79-c752-7650-93fe-698ca23fdc69. Original decisions.json and every R1 approved file/hash remain unchanged. execution.json records this revision's resumable disposition; it must not be applied twice.

Selected colour B uses the exact approved grade data. Full voice uses shared voice_chain.py, highpass70Hz and broad+1.5dB120Hz, no expander/dereverb,4x oversampling, shared finishing/limiter-delay compensation. Original measured dual-mono lav only; no camera-mic sum, music or synthesized speech. The source-specific selected tone is retained regardless of the absolute-reference heuristic.

Original four source windows and spoken edit are preserved. The full timeline has201 captioned words in81 cues, including the corrected “Once working out” closing section. The prior excerpt-local caption override is merged once at frame1467. No global500ms shift was applied. R2 exports actual ASS-rendered whole-cue PNG states with the first word identifying cue onset; this is cue-onset evidence, not word highlighting. Fresh delivered-AAC ASR and independent full-sequence reconciliation are stored separately.

## Repairs and review times

-0:18.018–0:23.957,0:38.372–0:44.645,0:48.949–0:52.753 and0:58.559–1:01.428: tighten the former very wide camera from2040x3626 to1350x2400. Keep the approved1120x1990 close size, with source-calibrated hair anchors and shared landing.py. No new continuous chasing. Review0:16–0:26 and0:48–end.
-0:52.753–0:55.255: clean first2.5s of approved A0157, over the client-results line. The later source has cropped trainer hair earlier than R1 noted. Full source height remains; no invented pixels, freeze, slow motion or new generation. Continuous FAR enters the insert; the return at0:55.255 uses a genuine NEAR cut measured at source259.3027s. The0:58.559 source join then uses the FAR close. Review0:50–end.
-The AI source itself has extremely tight headroom, at times only a few native source pixels even in the retained clean part. Later frames with hair outside the source were excluded. This is not a20px hair-clearance certification for that trainer. Dan's actual presenter framing has its own delivered-file reports.
-Real B0431 kettle footage, C1733–C1735 equipment montage, two lower thirds and moving blue media fields retain their approved content. B0431's historical filename says swings but its actual movement is deadlifts. All six equipment objects retain their speech-matched positions. Every insert is graded; no full-height horizontal crop is shortened.

## Verification and explicit limits

Exact-file delivery gate:{d['verdict']}, version{d['gate_version']}. Failed rows remain failed:

{fail}

Watch scan and independent judgments are bound to this master hash. Read independent-audit.md for actual inspected coverage, defects and limitations. Later limited metadata diagnostics passed completed watch judgments, the62-sample scan and script fidelity; they do not replace the full FAIL. The single invalid framing detection at52.75s was reconciled by extracting the same fps=4 sample: it shows the AI insert, not presenter T09. Native boundary frames1580/1581 were inspected; no actual presenter hair miss remains at that boundary. Original172/173 measurements stay unchanged. No audible speaker listening is claimed. Numerical decode, ASR, native still/sequence inspection and silent functional playback are not full-speed human picture/audio perception; unavailable perceptual checks remain incomplete. No gate threshold or corpus was changed.

Shared audio self-test ran before production. Four fixture-dependent cases failed because both historical Ad1 files named by the suite are missing. Available microphone selection, approved chain, wet/dry handling and rejected-processing damage tests passed. The original suite outcome/log is preserved, rather than stamped PASS. Fresh audio/delivery checks on this file are separate.

An internal complete candidate with a still-clipped AI source tail is retained in evidence/internal-v1 and was stopped before QA/review delivery. A stale cache comparison in the inherited renderer compared a tuple with its JSON list and rebuilt valid scenes; R2 stores the dimensions as a list so subsequent cache checks work. No approved media or shared gate code was modified.

## Storage and cost

Round2:/Volumes/Expansion/_edit_work/DS-27/round2. Full-quality delivery and VLC copies are actual files. The managed review caches linked assets locally for continued playback without the editing drive. The private Drive R2 folder preserves the R1 originals and sharing state.

R2 AI generation and paid review spend:$0. R1 file/model review usage was approximately$0.50; its receipts are preserved. Editor/reviewer runtime token usage is unavailable. No new files were downloaded; this round uses the existing raw rolls, approved library media and R1 graphics. No covers, publishing, scheduling, credentials, unrelated deletions or account changes.

Rebuild: use recipe/repair_build_r2.sh and the source/data packet. The original camera, library assets and immutable R1 HyperFrames renders are required at their recorded paths/hashes. The original R1 folder is preserved. Final approval and setup are separate owner decisions.

Git delivery: R2 recipe is locally committed; safe push is pending because unrelated shared files have live edits. No other owner’s changes were adopted or altered.
'''
(Q/'notes.md').write_text(text)
print('NOTES_WRITTEN',flush=True)
