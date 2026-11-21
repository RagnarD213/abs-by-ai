# HyperFrames for Abs By AI motion graphics: research and recommendation (2026-09-30)

Written for Dan. Plain language first, details after. Sources are at the bottom of each section.
Research transcripts and screenshots from the session are in the session scratchpad; the durable facts are here.

## 1. The short answer

**Use HyperFrames. Use it as the graphics layer only.** Keep our cutting, audio chain, gates and the Soft Blue Light
look exactly as they are, and replace the way the graphics themselves get drawn and animated.

Why:

1. It is the exact tool behind the look you want. Every Nate Herk video since April 2026 renders its graphics in it.
2. It is free and open source (Apache 2.0, made by HeyGen). No seats, no per-render fees, no subscription.
3. It has an official Claude Code plugin (21 skills) and a Codex plugin, so both of our editors can drive it.
4. It exports transparent overlays (ProRes 4444 MOV) that drop straight onto our graded footage in the pipeline we
   already have. Nothing downstream changes: same cut, same audio gates, same delivery gate.
5. It gives Claude a live preview and a "check" command. Today every graphic tweak is a Python re-render with no
   preview, which is why our graphics rounds are slow and expensive.
6. The animation language it uses (HTML, CSS, GSAP) is the thing AI models write best. Our current PIL frame renderer
   is the thing they write worst: every effect (glow, blur, spring, draw-on arrow) is hand-coded math.

The runner-up is Remotion. Same rendering idea, more mature, but it needs React, its licence is free only up to
three people, and Nate tested both on the same clip and found the HyperFrames output "more sophisticated".
HeyGen ships a porting skill between the two, so switching later is cheap if HyperFrames disappoints.

The most important finding is not about the tool. **What makes Nate's graphics look good is a written design
philosophy, word-level timing, a plan before any code, screenshot verification, and turning every approved result
into a reusable skill.** We already do three of those five. The two we are missing are the design philosophy
(depth, light, perpetual motion, easing rules) and a tool that makes iterating on it cheap. HyperFrames supplies the
second; section 5 supplies the first.

## 2. What Nate Herk actually does

Eight videos were transcribed in full (four tutorials, three "the AI made this whole video" demos, one Remotion
precursor). His method has not changed since April; only the agent changes (Claude Code, then Codex, then Opus 5.5).

**His five steps: transcribe, cut, plan the beats, use skills, verify.**

1. **Drop the raw file in** and get a word-level transcript (ElevenLabs Scribe or Whisper). Every graphic is
   anchored to the timestamp of a spoken word. His words: "the most important part is that you trim it first and
   that you have the motion graphics synced up to the exact moments." One reviewer who skipped this had every
   animation land 0.6 seconds late.
2. **Cut mistakes and silence first** (he uses video-use for this; we already have our own cut tools).
3. **Direct the graphics by voice, then switch to plan mode.** He dictates a long, specific brief, timestamp by
   timestamp, and makes the agent write a beat sheet (anchor word, position, palette, spec per beat) before it writes
   any HTML. Reason: "once you start creating them, that's where you're getting a lot of output tokens... if you
   accept the plan but then you end up not liking what it's doing, that will cost you more tokens."
4. **Preview and give feedback like to a human editor.** Timestamped, plain: "at about 5 seconds the text can't be
   seen because there's a blur effect on top of it... the blur needs to be behind it." Two to four rounds is normal.
5. **Render, then turn the result into a skill.** "If you get an output you really like, you say: cool, that was
   awesome, turn that into a skill. Next time you just say: edit this video, use this skill."

**His signature look** (from the screenshots): frosted "liquid glass" cards on the left or right third that never
cover his face, a tiny uppercase eyebrow label, a chrome-gradient headline, words popping in karaoke-style as he
says them, a dark overlay dimming the footage behind text, face-cam shrunk to a rounded vertical crop with a drop
shadow and slid to one side, little explainer animations that literally act out the sentence (clip cards turning
red and a scissor sweeping through them under "MISTAKES WILL BE CUT"), and captions near the lower third with the
current word highlighted.

**His design rules, shipped as a file the agent reads** (MOTION_PHILOSOPHY.md in his free student kit):

- One concept per scene, about 1.5 seconds each. 90 percent of the frame dark. "Light over color": gradients,
  halos, vignette, grain instead of flat fills.
- "Static = death." Something is always drifting, even on a held card. Cuts are hidden by motion whips.
- At most five hues, each owning one meaning (red = broken, teal = solution, and so on).
- One geometric sans-serif (Inter, SF Pro), chrome gradient on headlines, word-by-word reveals with a 0.35 s stagger.
- An easing table: word reveal expo.out 0.2 to 0.33 s, enter power2.out 0.2 to 0.5 s, exit power2.in, card settle
  back.out(1.2 to 1.5), drift sine.inOut 2 to 4 s.
- A rest beat of one second every seven to eight seconds. Hero holds: logo 2 s, outro card 4 to 6 s.
- Liquid glass recipe: diagonal gradient, backdrop blur 14 px with saturate 1.12, inner highlight, 1 px border.
- Pre-flight: "VIEW THE FRAMES" before handing anything over.

**Cost and time he reports:** 240k to 400k tokens per short video (a 30 to 60 second clip with four to six beats),
18 minutes for a first pass and 10 for a revision, two to four minutes to render. He keeps effort at high, never
above ("Ultra over-delegated to nine agents, about $300 equivalent").

**Problems he hit:** preview showing "0 of 0 seconds", blur rendered on top of text, numbers cut off at the frame
edge, a grid background bleeding into every scene, a card covering his face, a logo present in the draft but missing
from the final render, fanned videos "cutting through each other", a product demo going static after the opener.
All were fixed with plain-language feedback rounds. Rendering several videos at once maxed his CPU.

Videos: "Claude Just Destroyed Every Video Editing Tool" (04-18), "Claude Video Editing Just Became
Unrecognizable" (04-22), "GPT-6 Astra Finally Solves AI Video Editing" (09-08), "Opus 5.5 Just Changed Video
Editing Forever" (09-25). Kit: https://github.com/nateherkai/hyperframes-student-kit

## 3. What HyperFrames is

- Made by HeyGen. Public since 2026-04-16. Apache 2.0. Version 0.8.97 on 2026-09-30; 54,550 GitHub stars, about
  553,000 npm downloads a week. Repo: https://github.com/heygen-com/hyperframes. Docs: https://hyperframes.heygen.com
- How it works in plain words: Claude writes a normal web page. Each element on it carries a start time and a
  duration. A hidden Chrome opens the page, pauses it, jumps to each frame time, photographs it, and FFmpeg turns the
  photographs into a video. Same file in, byte-identical video out. A slow Mac never drops frames.
- Outputs: MP4, ProRes 4444 MOV with transparency (for dropping onto footage), WebM with transparency, PNG sequence,
  GIF. Any size (1920x1080, 1080x1920, 1080x1080). Any frame rate. Audio layers with ducking.
- Comes with a catalog of 388 ready-made blocks: 73 text and caption styles, 11 lower thirds, 18 charts and
  counters, 31 transitions, social-post cards, a macOS notification, device mockups, a "talking-head recut" workflow.
- Has a browser editor (Studio) where you can drag, shorten, resize; edits flow back into the file so Claude sees them.
- Claude Code install: `claude plugin marketplace add heygen-com/hyperframes` then
  `claude plugin install hyperframes@hyperframes`. Codex: `npx skills add heygen-com/hyperframes`.
- Requirements: Node 22+ (this Mac has 24), FFmpeg on the path, Chrome (downloads itself). No GPU needed.
- Checks Claude can run before rendering: `lint` (structure), `check` (opens the page headless and reports runtime
  errors, layout collisions and contrast failures), `snapshot --at 0,3,8` (still frames at chosen times).
- Cost: software free, local render free. Real cost is Claude tokens. Optional HeyGen cloud render is about
  $0.05 to $0.15 per output minute; we do not need it.
- Render speed on a Mac: roughly 3 to 5 seconds of render per second of 1080p video. Blurs, backdrop filters and
  shadows are the expensive effects; one CSS line took a 300-frame render from 10 s to 25 s. Soft Blue Light uses
  blur glass, so expect the slow end.
- Known traps: it moves fast (ten releases on Sept 29 and 30 alone, mostly Studio fixes), so pin a version.
  Animations must obey its "paused timeline" rules or they render wrong without an error. Keep each scene under
  about 40 seconds per file. One open issue today about video sampled between frames showing the next frame.

Reviewers' consensus after three to six months: "80 percent of the way there and then stalls on the last 20" for
full edits of raw footage; "for wiring video generation into an automated pipeline driven by Claude Code, nothing
else comes close." That is why the recommendation is graphics layer only, not full edits.

## 4. Alternatives, and why they lose

| Tool | What it is | Why not (or when) |
|---|---|---|
| **Remotion** | React video framework, 61k stars, official Claude Code skills, ready-made caption and lower-third blocks, ProRes 4444 | The credible runner-up. Needs a React build step, source-available licence free only up to 3 people, and Nate found its output plainer on the same clip. Keep as fallback; a porting skill exists. |
| Motion Canvas | TypeScript explainer animator | Dead since Dec 2024; website gone. |
| Revideo | Fork of Motion Canvas for programmatic video | Still 0.x, thin docs, follows a startup's product roadmap. |
| Manim | Python math-animation engine (3Blue1Brown) | Chalkboard look; wrong for brand cards and phones. Possible chart helper only. |
| Lottie Creator, Rive | Animation asset editors with new MCP servers | Asset factories, not video. Could feed icon animations into HyperFrames later. |
| After Effects via MCP | Community servers, 199 operations | Needs Adobe subscription, cannot drive MOGRT templates, best server is non-commercial licence, agent is blind to results. Human-editor path only. |
| DaVinci Resolve 21.1 native MCP | Blackmagic shipped Claude Code support on 2026-09-08 | An assembly and compositing tool, not a graphics author. Phase-2 experiment at most. |
| Creatomate, Shotstack, JSON2Video, Plainly | Template render clouds | Per-render fees, template-bound. Fine for 1,000 variants of one ad, wrong for hand-directed video. |
| motion.so, iArt, varg | Hosted "motion agents" | Credits, and you do not own the look. |
| Kineweft, Motionly, Diffusion Studio | Newer agent-first editors | Weeks old, or browser-only with a watermark. |

## 5. Where our current graphics fall short (examples from the last five videos)

Frames were pulled from RO-01 (Codex, Zepbound), RO-05 (Claude, salad), RO-16 round 1 (Claude, Soft Blue Light),
WV-01 round 3 (the Soft Blue Light reference) and C1652 R4 (Codex, belly fat emergency, approved and the current bar).

The pattern across all of them: **every graphic is a flat rectangle with text on it, and the only motion is a
fade or slide.** No depth, no light, no physics, no draw-on, no counters, nothing that acts out the sentence.
The Soft Blue Light lower third is the best of the set and it still just fades in.

| Video and moment | What it is now | What HyperFrames would do |
|---|---|---|
| **C1652 4:32 "The downward spiral"** (cycle diagram, four boxes and arrows in an olive panel) | Boxes pop in one at a time, arrows appear instantly. Reads like PowerPoint SmartArt. | Arrows draw themselves along the path as Dan says each step; each box lands with a small spring settle; once the loop closes it pulses once and a soft light travels around the cycle. On "turn the spiral around" the loop reverses direction with the hues flipping red to teal. |
| **C1652 2:39 visceral fat anatomy** | Static AI illustration with two thin label lines. | Slow push-in on the illustration; when he says "around your organs" a soft highlight mask lights the fat region and the rest dims; labels type in with animated leader lines; a faint depth blur on the edges. |
| **RO-16 0:18 and WV-01 before card** ("TWO YEARS AGO, 200 lb at 5'7", No abs.") | Photo in a frame beside a static fact card. | The photo pushes in slowly with a light sweep across the glass; "200" counts up from 0 as he says it; the card drifts a few pixels the whole time it is up (his "static = death" rule). |
| **RO-16 lower third "1 lb A Week = 7 MONTHS. All In = 90 DAYS."** | A sentence on a strip. | A timeline bar beside the strip that starts at 7 months and shrinks to 90 days on the word "all in", with the two numbers as counters. Reuses the analysis-card idea Dan already approved. |
| **RO-05 ingredient chips** ("01 Arugula, 5 cal per salad") | White chip plus grey sub-chip, slides in. | A glass card whose calorie number ticks up, and a running total card in the corner that accumulates through the video, so by the chicken and eggs the viewer sees the whole salad's calories and protein add up live. |
| **RO-01 0:20 title card "Lose fat. Keep muscle."** | Flat olive box, corner brackets, blur-fade. | Kinetic type: "Lose fat." reveals word by word, "Keep muscle." lands with a highlight wipe, the navy field drifts behind it, a subtle chrome gradient on the headline. |
| **RO-01 6:06 split screen list** ("Keep your muscle: protein, vegetables, carbs") | Solid olive panel, numbered lines, Dan in a bordered box. | Items stagger in with an icon each; Dan's window becomes a rounded crop with a drop shadow (Nate's face-cam treatment) instead of a bordered rectangle. |
| **WV-01 phone demo** (shell rejected by Dan) | Drawn phone with a pasted screen. | A CSS iPhone with the screen recording clipped precisely to the rounded display, Dynamic Island, a 3D tilt and shadow. Solves the credibility problem in the standards doc. |
| **All CTA end cards** ("Try AbsByAI free for 7 days") | Eyebrow, headline, outlined button. | Button breathes, "7" counts, a light sweep crosses the card, the URL types itself. For ads: an animated price or timer where the script calls for it. |

None of these change the approved look. Soft Blue Light (navy field, drifting blue light, glass cards, pale type,
quiet motion) is almost exactly Nate's liquid-glass recipe, so the style lock stays; only the execution improves.

## 6. How to use it here (the rules for the pilot)

- **Graphics layer only.** HyperFrames renders transparent MOV overlays and full-screen graphic scenes. Our cut,
  audio chain, gates, delivery and Blotato steps do not change. The editor composites the overlay with ffmpeg
  exactly as it composites the alpha MOVs from motionlib today.
- **Soft Blue Light is the style.** Port `softblue.py`'s geometry and colours into two or three locked HTML
  templates (lower third, left-third card, full-screen fact card, CTA). The 388-item catalog and Nate's 406 cards are
  for motion ideas, not for a new look.
- **Word-level timing from our existing transcripts** (`mapped-words.json` in every build folder). Every graphic
  is anchored to a word.
- **Plan before code.** A beat sheet Dan sees (or the editor decides under the decision budget) before HTML is
  written. Same as our round method.
- **Verify by frames.** `lint`, `check` and `snapshot` before every render; the reviewer watches the composited
  result, never the HTML.
- **Approved result becomes a component.** Each approved graphic is saved as a reusable template under
  `.claude/skills/_shared/hyperframes/` with its own README, same as Nate's "turn that into a skill".
- **Pin the version.** Install a specific version and only bump it deliberately.
- **Watch render time.** Glass blur is the expensive effect; draft quality for previews, high only for the final.
- **Do not point it at raw footage edits.** That is where every reviewer hit the wall, and our cut tools are better
  for our footage.

## 7. Getting started, step by step

Dan does not need to type any commands. A Claude Code session does the install, following Nate's own approach
(hand the agent the repo and tell it to set itself up).

1. **Open a new Claude Code session** in the Abs By AI project. Model Opus 5.5, effort high (Nate's rule: high, never above).
2. **Paste the starter prompt** from `Handoffs/handoff-20260930-hyperframes-pilot.md`. The session will: install the
   HyperFrames Claude Code plugin, pin the version, create a test project under `Media/hyperframes/`, render the
   built-in 8-second demo to prove the chain works, then rebuild ONE existing graphic (the C1652 "downward spiral"
   cycle) in Soft Blue Light as a transparent overlay, composite it on the real footage, and put the old and new
   versions side by side on a review page.
3. **Watch the side-by-side** (about 20 seconds). Give feedback the way Nate does: a timestamp and plain words
   ("at 0:04 the arrow is too fast", "the glow is too strong"). Two or three rounds is normal.
4. **Say "approved, make it a template."** The session saves the graphic as a reusable component with a README and
   records the design rules that came out of the rounds.
5. **Repeat for the lower third and the before card** (the two most-used graphics), one per short session.
6. **First real video:** RO-16 round 2 is the natural candidate, because its opener and graphics are not built yet.
   Its handoff gets one added line: graphics layer in HyperFrames from the approved templates.
7. **Codex adopts second.** Once three templates are approved, a small Codex handoff installs the Codex plugin and
   the same templates so RA/RO/DS first cuts use them too.

Expected cost: no dollars. Tokens: about the same as one of our current graphics rounds (Nate reports 250k to 400k
per short clip). Time: an hour for the pilot session including install.

## 8. Sources

HyperFrames: repo https://github.com/heygen-com/hyperframes, docs https://hyperframes.heygen.com (quickstart,
rendering, CLI, plugins, skills, motion-graphics guide, catalog, performance, troubleshooting, vs Remotion),
launch HN thread 2026-04-25, HeyGen July 2026 release notes, issues #677 #1231 #2824 #3329 #4294 #4584 #4763.
Reviews: andrew.ooo (05-28), mejba.me (04-18), Trilogy AI (05-27), OneWave (09-04), cutback.video (09-22),
voyageragent (09-21), autoae (06-20), Geeky Gadgets (04-21). Nate Herk: the four tutorials and three demos listed in
section 2, his X post 2026-04-23, his student kit repo and its MOTION_PHILOSOPHY.md, PROMPTS.md, WORKFLOW.md.
Alternatives: remotion.dev (skills, license, transparent videos, Elements, Recorder, Lambda), motion-canvas repo and
HN 47191103, canvas-commons, redotvideo/revideo, ManimCommunity, LottieFiles MCP docs, Rive x MCP announcement,
Immersive-Media-Technologies/aftereffects-mcp, kumoproductions/mcp-aftereffects, lobodosaas/premiere-pro-mcp,
Resolve 21.1 MCP coverage (digitalproduction.com 09-08), DareDev256/fcp-mcp-server, diffusionstudio/core, editly,
ephyro/kineweft, Motionly review, iart-ai/motion-skills, varg comparison docs, descriptinc/descript-mcp.
