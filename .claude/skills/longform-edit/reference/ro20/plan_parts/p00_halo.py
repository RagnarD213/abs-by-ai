# 0:00 to 1:39  Reason 1: the halo effect (written by the lead editor; the first minute lives here)
PART = [
 # round 2 (Dan, 2026-10-11): no AI opener, "Just use a camera scene for the intro". O1 removed; the film opens on camera.
 # round 3 (Dan, 2026-10-12: "Let's go with T3, the piggy bank, for the intro"): one Veo take from the approved T3 frames under his first
 # sentence, take 0.25 to 7.85 s played 12 % faster (T3-t1.x112.mp4) so the finished title holds about 2.4 s; he is on camera from "The first reason".
 dict(id="T3", kind="clip", start="Alright, so let's talk about why", end="right now", tail=0.34,
      src=[f"{W}/round3/motion/T3-t1.x112.mp4@0.0"], **AIL, **OTHER,
      note="INTRO, Dan's pick T3: a coin drops into a piggy bank on a gym bench, the pig pumps up into a bodybuilder and flexes, and the title WHY YOU NEED TO INVEST MORE IN YOUR HEALTH lights up beside it"),
 dict(id="Ga01", kind="lt", start="The first reason", end="halo effect", tail=1.6, topic="REASON 1 OF 4",
      point="The Halo Effect", parts=[["The Halo Effect", "The first reason"]]),
 dict(id="A1", kind="clip", start="Making money is my first priority", end="happy with that", tail=0.05,
      src=[f"{W}/round3/motion/A1-t2.mp4@0.05"], **AIL, **OTHER,
      note="EXCUSE VOICE, round 3 working version (Dan: 'the lip-syncing doesn't match up at all'): a new take from the approved START frame in which he keeps his mouth shut, smirks, pats the cash and shrugs while Dan's voice does the excuse, as the brokie does. Three lip-sync attempts failed on this face (README round 3)"),
 dict(id="Ga02", kind="lt", start="If you care about money", end="prioritizing your looks", tail=1.2, topic="KEY POINT",
      point="Care About Money? Then Care About Your Looks.", parts=[["Care About Money?", "If you care about money"], ["Then Care About Your Looks.", "then you need to be"]]),
 dict(id="Ga03", kind="lt", start="more likely to think", end="based on how you look", topic="THE HALO EFFECT",
      point="Good Looks Read As Smart, Capable, Funny.", parts=[["Good Looks Read As", "more likely to think"], ["Smart,", "intelligent"], ["Capable,", "good at your job"], ["Funny.", "funnier"]]),
 dict(id="Ca01", kind="clip", start="even very technical", end="based on the halo effect", tail=0.1, src=[stock("pexels-7552433-people-in-a-meeting.mp4", 0.5)], **OTHER,
      note="Pexels stock (new): three executives across a boardroom table size up the person facing them"),
 dict(id="Ca02", kind="clip", start="So let's say you're applying", end="if you look better", tail=0.1,
      src=[f"{W}/round3/motion/J1-t3.mp4@0.0"], **AIL, **OTHER,      # round 3 take 3 (takes 1 and 2: the interviewer shook the heavy man's hand; the provider refused one prompt)
      note="NEW AI clip (frames for approval; Dan, round 1: 'a guy in great shape getting a job while the fat guy looks on in envy... maybe in a boardroom'): a hiring panel in a boardroom, the fit candidate gets the handshake, the heavy candidate beside him looks on. Slot trimmed from 9.2 s to under 8 s"),
 dict(id="Ga04", kind="lt", start="Your odds of getting the job", end="if you look worse", tail=0.1, topic="THE JOB INTERVIEW",
      point="Better Looking Candidates Get Hired More.", parts=[["Better Looking Candidates Get Hired More.", "Your odds of getting the job"]]),
 dict(id="Ca03", kind="clip", start="they're gonna judge you based on that", end="less likely to get the partnership", tail=0.1,
      src=[f"{W}/round3/motion/J2-t3.mp4@0.0"], **AIL, **OTHER,      # round 3 take 3, from the approved END frame only (takes 1 and 2: the heavy man joined the handshake)
      note="NEW AI clip (frames for approval; the second of Dan's two 'similar, not the same scene' clips): on a golf clubhouse terrace the senior partner signs with the fit man and shakes his hand, the heavy man looks on"),
 dict(id="Ga05", kind="lt", start="you're gonna be sending the message", end="more likely to get that partnership", tail=0.3, topic="WHAT BEING IN SHAPE SAYS",
      point="Gets The Job Done. Disciplined. Trustworthy.", parts=[["Gets The Job Done.", "gets the job done"], ["Disciplined.", "disciplined"], ["Trustworthy.", "you can trust"]]),
]
