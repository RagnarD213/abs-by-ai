# Pickups to record at the studio shoot (list made 2026-10-13)

Dan, 2026-10-13, after hearing the desk-mic pickups in the "Invest In Your Health" first minutes: *"Yeah, that audio doesn't work.
What I'm going to do is I'm just going to record these pickups on my studio set instead... get all of the pickups that we need for
this task and every other outstanding video edit that we have... For pickups, I'll just do those first to make sure we get them,
and then I'll just upload the pickups. From there, we can finish out all the videos."*

**Standing consequence:** a pickup for any video goes on the next shoot's list and is recorded on the studio set with the shoot's
clip-on mic. The desk Yeti is for timing placeholders only. (The 2026-10-11 rule in `VIDEO-RULES.md` said to record pickups into the
desk mic in the editing session; Dan's words above replace that part.)

## How to record them

- First thing on the shoot, on the studio set, wearing the shoot's clip-on mic, camera rolling (only the sound is used; every pickup is
  covered by a graphic or a clip).
- Read each pickup twice. They are printed twice in the pickups teleprompter document for that reason.
- 11 pickups, about two and a half minutes of talking in total.
- Documents: the "PICKUPS" section at the top of the shoot doc (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`) and the pickups-only
  teleprompter document (id in `Docs/SHOOT_1017_DOCS.md`), also loaded into PromptSmart.

## The pickups

### Invest In Your Health, three long-form videos (RO-20, RO-20B, RO-20C)

Read these in the energy of the kitchen-doorway video. Wording is Dan's own from his 2026-10-13 read.

1. **Video 1, ending** (after "You need to be spending more money on your health."):
   In the next video, I'm going to tell you what you should cut to find that money, even if you're a brokie right now. And in the video
   after that, I'll walk you through exactly what to buy for your health at every level, from dead broke to mega baller.
2. **Video 2, opening** (after his on-camera "...no matter how little money you have.", before "But I know at this point in the video..."):
   In the last video, I told you why you need to spend more on your health. Being in shape makes you more money and it makes you more
   productive, and bad health is ludicrously expensive. In this video, I'll tell you exactly what to cut, so you can spend more money on
   your health.
3. **Video 2, ending** (after "...you'll be so glad you did once you're there in a couple months."):
   That's what to cut. Now you have the money. In the next video, I'll walk you through exactly what to buy for your health at every
   income level, from dead broke to baller. To take the first step to getting in shape, go to AbsByAI.com. Upload a picture of yourself,
   and AI makes a picture of you with ripped six-pack abs, for free. Thanks for watching guys, and I'll see you in the next video.
4. **Video 3, opening** (before "All right. So let me walk you through it."):
   Here's exactly what you should be buying for your health, whether you're dead broke, middle class, or making over $10,000 a month.
   You need to be spending more money on your health no matter how little you have right now. Because money does you no good if you're
   dead or if you're sick. The last video covered what to cut to find the money. Now let's spend it.

### Top 5 Zepbound Tips, shorts cut from the long-form (SL-06)

Each one opens a Short. Read them like the first line of a video.

5. **Short A** (before "And for most of you watching this channel, you should be taking less than the standard 2.5 milligram minimum dose."):
   Here's why you should start Zepbound at 1 milligram to avoid the side effects.
6. **Short B** (before "There are two ways to inject Zepbound..."), Dan's own longer wording, then the short version, so the edit can use either:
   Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead.
   Here's why you should stop using the pen to inject Zepbound.
7. **Short C** (before "This takes about 10 seconds once you know what you are doing."):
   Here's how to inject Zepbound with a needle, step by step.
8. **Short D** (before "The medication is strongest in the first few days after your shot..."):
   Here's why Thursday evening is the best time to inject Zepbound.
9. **Short E** (before "Coming off is where I see people destroy everything they built."):
   Here's how to come off Zepbound without gaining the fat back.

### If I Had Belly Fat, Here's How I'd Lose It In 90 Days, shorts cut from the long-form (SL-07)

10. **Short B** (before "Weigh yourself every morning, right after you use the bathroom and before you eat or drink anything."):
    Here's how to know if your fat loss plan is working.
11. **Short D** (before "Most guys do it the opposite way."):
    Here's why you should work out every single morning.

## Not pickups, but waiting on this shoot (already on the B-roll list or the next-shoot list)

- RO-09 Pushup Masterclass: the on-camera talking was never found and level 1 countertop pushups need about 30 seconds of filming. No
  lines are written. `Handoffs/video-editing/RO-09-pushup-masterclass.md`.
- DS-25 M100s: filmed B-roll only (squat thrusts, mountain climbers, squat jumps), no speech. `Docs/NEXT_SHOOT_LIST.md`.
- SL-08 to SL-14: no segments picked yet, so no pickup lines exist. Any batch cut after the shoot puts its pickups on the next shoot's list.

## After the shoot: which task finishes which video

When the pickup clips are uploaded (Dan uploads them himself), each job below finds its lines on the shoot roll (`pick_lav.py` per file,
`roll_sidecar.py`), takes the last clean take, and lays it in with the film's own voice chain. The studio lav should need little or no
tone matching; check it by ear and on the audio gate rows.

| job | handoff | what the pickups unblock |
|---|---|---|
| RO-20, RO-20B, RO-20C | `Handoffs/handoff-20261012-ro20-round3b-pickup-rerecord-first-minutes-films.md` | first minutes of videos 2 and 3 again, then the three films |
| SL-06 | `Handoffs/handoff-20261012-sl06-round2-build-after-dan-review.md` | round 2 build of the six shorts |
| SL-07 | `Handoffs/handoff-20261012-sl07-belly-fat-shorts-pickups-and-build.md` | shorts B and D |

Desk recordings kept for timing only: `Media/longform-raw/ro20-pickups/`, `/Volumes/Extreme/_edit_work/sl06/pickups/`,
`/Volumes/Extreme/_edit_work/sl07/pickups/`.
