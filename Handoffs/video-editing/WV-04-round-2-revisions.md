AD (Great Again T upsell video). Task name: `GAT Upsell 1 AD R2`.

# Great Again T Upsell 1: Prepaid Packs (WV-04): round 2 handoff (2026-11-16)

Written by the launcher chat after Dan's round 1 review. **Model: Claude Opus 5.5, high effort** (a video started on Claude
stays on Opus 5.5 high). **Dan fires this himself.** **Run the chat ON THE M2** (SSH connection `m2`): the job lives on the
M2 and job work never goes through the network share.

One native 9:16 upsell video (1080x1920, 29.97), Dan on green screen over Wood Kitchen 1, roll C1904 0:00-13:45. No 16:9.

## 0. Where things are (M2)
- Job folder: `/Volumes/Expansion/_edit_work/WV-04` (the Seagate: checksum every final; never the only copy).
- Dan's round 1 words, verbatim: `round2-plan/notes_r1.txt`. His words outrank this file.
- Round 1 state, written by the round 1 editor: `round1/ROUND-1-NOTES.md` (read it first; it is updated after Dan's review
  with the keyed pieces, graphics build files, recipe paths and traps). Take map for the whole upsell: `plan/take_map.md`.
- Round 1 film (first minute): `round1/GAT Upsell 1 AD R1 - First Minute.mp4`. Review page: http://127.0.0.1:9812/.
- Look and voice recipes: `look/LOOK_WV04.json`, `look/VOICE_WV04.json`. Key recipe `key/recipe`, stamps in `key/`.
  **Only pieces A and B (the first minute, takes T01 and T02) are keyed.** Nothing after the first minute is keyed: every
  later take needs new pieces (copy `key/chain_piece.sh`, add them to `key/pieces.json`, same settings, absolute paths).
  Never re-key A or B. Keying the rest is the long step of round 2: queue it first and do pictures and graphics while it runs.
- Great Again T VSL (WV-03, same shoot and set): `/Volumes/Extreme/_edit_work/WV-03`. Copy from it; never run inside it.
  Characters: `round5/frames/characters/` (`everyman_after`, `wife`, ...). Approved graphics: `round7/graphics/` (bottle
  render, Tongkat root X1, Maca root X2). Its round 8 handoff: `Handoffs/handoff-20261116-great-again-t-vsl-round8.md`.
- Script: Google Doc `1lOl-CdLLIkvMQmECAmHz2WmrHfbpDOzxMuKlTMtXRcc` (copy in `script/doc_full.txt`). Filmed wording wins.

## 1. Dan's round 1 decisions
- **Colour: Matched. Voice: House bass.** Locked for this upsell.
- **Green-screen key:** he gave no note on it. Treat as accepted as shown; say so on the round 2 page.
- **0:52.4 to 0:55.0 (the bottle beside Dan, G03): remove the whole camera scene there.** Replace it with a FULL-SCREEN
  Great Again T product shot: the bottle with its ingredients laid out in front of it (tongkat ali root and the others),
  slowly panning, so the product reads natural and safe.
  - Use the real approved bottle (the VSL's bottle render and the locked label, `Contest/approved/DESIGN-LOCK.md`), never an
    AI-drawn label. Show only ingredients that are on the label (Supliful Men's Vitality: zinc, tongkat root, maca and the
    listed botanicals; read the supplement facts, do not guess). Natural light, wood surface that fits the kitchen.
  - Dan allows either a pan across a still or a clip made from the still. Default: blind Codex/Google stills (Google
    subscription first), then a slow coded pan or push in HyperFrames on Dan's pick, because clips with a printed label
    failed the motion gate on the VSL. Offer a Flow take beside it only if it passes the gate with the label sharp.
  - Non-person product illustration: no on-screen AI label.
- **Key-point cards (G01 Warning, G02 Average Or Head-Turning Results): slightly larger.** Taller, and clearly wider when
  the card carries that much text. Apply the new size to every key-point card in this upsell. Keep Dan's face and hair
  clear, no caption collision. This is a change from the VSL round 6 size, for the upsells only.
- **Wide Awake On The Sofa (0:31 to 0:34): keep the idea and her look at him; recast both people.**
  - The man: the same man as the VSL's prospect story, in his AFTER state (`everyman_after`), not the before version.
  - His wife: a little younger and more attractive than the VSL wife, looking at him exactly the way she does now (only her
    head turns to him, warm closed-mouth smile).
  - New START and END pairs, blind Codex/Google pair, frame gate plus a fresh `frame-reviewer` on each, before Dan sees them.
- **The three "guys who..." lines:** stay on Dan on camera (his new direction below). Any picture pairs the round 1 session
  already made (`round1/frames/AI-U01` to `AI-U03`) are not placed; list them under "What I decided" as available.

## 2. Dan's direction for this upsell and upsells 2 to 4
Cleaner, less busy and more trustworthy than the VSL. More camera scene, fewer AI clips. Graphics and clips only now and
then, to illustrate a key point. High production value. In practice:
- Dan on camera is the default for every line. A graphic or clip has to earn its place on a key point.
- AI clips: at most two or three in the whole upsell (the sofa clip is one). Every one reaches Dan first as a complete
  START and END blind pair.
- Graphics: the script's own on-screen cues (the "6 Bottles. $199. Just $33 Per Bottle" card, the unchecked checkbox, the
  button pill from the first "click the big button" to the end) plus a small number of key-point cards. Outside the offer
  section, aim for no more than about one graphic or clip a minute. No stacked or back-to-back devices.
- Production value comes from the camera scene itself: a clean key, steady NEAR/FAR zoom steps on every join, exact
  captions, smooth audio joins, a calm frame.

## 3. Order of work, and what Dan sees at the end of round 2
1. `editroute.py pick WV-04 --kind AD --round 2 --chroma` (expect m2) and `resume.py check WV-04`, then
   `editcap.py acquire WV-04 --title "Great Again T Upsell 1: Prepaid Packs" --type AD`.
2. Save Dan's reading as `round2-plan/decisions.json`. Tell Dan the Codex image count before generating (small: the product
   still and the sofa pairs).
3. Make the product stills and the recast sofa pairs. Rebuild G01 and G02 at the larger size.
4. Build the WHOLE upsell from `plan/take_map.md` in the approved look, voice and key: best take of every line, zoom cuts
   on every join, the larger cards, the full-screen product shot at 0:52, the script's on-screen cues, and the camera scene
   in any slot that waits on a picture pick. Fix the one-frame-short mux (`apad -t`). Editor default, chosen because look,
   voice and key are settled and this upsell carries few graphics; every new graphic is still listed with its timestamp
   for review.
5. Full checks on the exact file: hair clearance, caption proof, sync, audio gate (seamscan every join), delivery gate,
   watch pass, and a fresh independent `ra-reviewer` before Dan sees it.
6. Round 2 review page (1080p, tested in the side pane at 800 and 1150 px, silent checks then owner handoff): what changed
   in the first minute with timestamps, the full film, every new graphic in context, the product-shot stills and sofa pairs
   to pick. Copy the film to `Videos to Review/`. Then `editcap.py release WV-04 --review` and STOP.
7. Queue row stays in progress until the full review copy is delivered, then `queue.py set WV-04 delivered` and mirror it
   to the Edit Queue page. One short dated board line.

## 4. Traps
- The M2's fast drives were near full, so the job is on the Seagate: checksum finals and keep a second copy.
- Gate checks time out when the M2 queue is busy: re-run with no time limit before calling a pair failed.
- VSL lessons that apply here: `.claude/skills/_shared/chroma-key/README.md`, "Three traps from the Great Again T VSL roll";
  Google END frames can carry the START's portrait chips, so check identity on every END.
- Take map flags to settle on the listen: T11 "random them strangers" slip; T24 line the medium model dropped.

## Starter prompt (Claude: Opus 5.5, high effort; start the chat on the SSH connection `m2`)

> AD (Great Again T upsell video). Name this chat "GAT Upsell 1 AD R2". Run it on the M2. Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/video-editing/WV-04-round-2-revisions.md`, then run round 2 of Great Again T Upsell 1: Prepaid Packs (WV-04) as that handoff lists. My round 1 notes are saved word for word in `round2-plan/notes_r1.txt` in the job folder. Matched colour, House bass voice. Replace the scene at 54 seconds with a full-screen Great Again T product shot with the ingredients in front of the bottle, make the key-point cards larger, recast the sofa pictures with the after guy and a younger wife, and keep this upsell cleaner than the VSL: more of me on camera, fewer AI clips. Build the whole upsell and send me the round 2 review page tested in the side pane. Use /ad-edit.
