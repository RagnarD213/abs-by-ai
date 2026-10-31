"""RO-31 visual plan ("How To Get Rid Of Man Boobs", 10/15 roll C1775). Every item is anchored to the words Dan says (phrase -> output time
via words_out.json). Graphics are HyperFrames only: lt (Motivation lower third), scene "fact", l3 (3A left card); D01/D02 are the hand-drawn
chest diagram (recipe/chest, a HyperFrames scene rendered to mp4). Clips: Dan's real B-roll first, clip library, then Pexels. kind "ai" = a new
AI clip: blind start frames go to Dan in round 1; until its motion is approved the presenter stays on screen.
Organic, not entirely about the drug: Zepbound is SAID, graphics say "Appetite Medication" (the script's own cue).
Title case; eyebrows in capitals (VIDEO-RULES 2026-10-20)."""
W = "/Volumes/Expansion/_edit_work/RO-31/round1"
ST = f"{W}/stock"; PH = f"{W}/stock/photos"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
AI = "AI-GENERATED"
BEFORE = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/before-photo-candidates/B_deckchair_UPSCALED_3x_1080x1440.jpg"
PLAN = [
 # ---------------- opening
 dict(id="A1", kind="ai", start="You think that you have man boobs", end="but you don't", tail=0.2, name="The Mirror Check",
      note="AI opener: a man frowns at himself in the mirror, holding up a big black T-shirt to hide in. Chest up, stomach out of shot"),
 dict(id="R01", kind="scene", scene="pair", start="and it comes off", end="belly fat does", tail=0.3, label="Real Photos Of Me, Not AI-Generated",
      photos=[BEFORE, "photo-251"], people="dan", physique=True, note="Your standard deck-chair before and a real pool photo, on the line 'it comes off the same way'"),
 dict(id="G01", kind="lt", topic_case="preserve", start="In today's video", end="fix each one", tail=0.6, topic="IN THIS VIDEO",
      point="Which One You Have + How To Fix It", parts=[["Which One You Have + How To Fix It", "which one"]]),
 dict(id="A2", kind="ai", start="Watch this video if", end="loose shirt", tail=0.3, name="The Pool Shirt",
      note="AI: pool party, everyone shirtless, one man roasting in a tent-sized black T-shirt, arms folded. A friend waves him in, he shakes his head and tugs the shirt down"),
 # ---------------- two kinds
 dict(id="D01", still_src_t=7.0, kind="clip", start="The first kind is chest fat", end="not fat", tail=0.45, src=[f"{W}/hf_extra/D01.mp4@0.0"], people="none", physique=False,
      note="The script's two-kinds diagram, drawn by hand in Soft Blue Light, no AI: the left panel lands on 'The first kind', the right on 'The second kind'"),
 dict(id="G02", kind="lt", topic_case="preserve", start="but for the majority of men", end="gland tissue", tail=0.5, topic="KEY POINT",
      point="For Most Men It's Fat, Not Gland", parts=[["For Most Men It's Fat, Not Gland", "majority of men"]]),
 # ---------------- the check
 dict(id="D02", still_src_t=6.5, kind="clip", start="Feel around your nipple", end="that's gland", tail=0.4, src=[f"{W}/hf_extra/D02.mp4@0.0"], people="none", physique=False,
      note="The same diagram with its call-outs, the script's 'two kinds diagram again with arrows'"),
 dict(id="A6", kind="ai", start="If you want a diagnosis", end="about a minute", tail=0.3, name="The One-Minute Diagnosis",
      note="AI gag: a doctor holds up a stopwatch, clicks it after a few seconds and gives the patient a calm thumbs-up"),
 dict(id="G03", kind="lt", topic_case="preserve", start="Check yourself today", end="fix you need", tail=0.6, topic="ACTION STEP",
      point="Check Which One You Have Today", parts=[["Check Which One You Have Today", "check yourself"]]),
 # ---------------- the fix for chest fat
 dict(id="G04", kind="lt", topic_case="preserve", start="Let's start with a fix", end="most of you guys have", tail=0.5, topic="PART 1",
      point="The Fix For Chest Fat", parts=[["The Fix For Chest Fat", "fix for chest fat"]]),
 dict(id="G05", kind="lt", topic_case="preserve", start="The first step is to lose", end="body fat", tail=1.3, topic="STEP 1 OF 2",
      point="Lose The Body Fat", parts=[["Lose The Body Fat", "lose your body fat"]]),
 dict(id="A3", kind="ai", start="you can't spot reduce it", end="your belly", tail=0.3, name="The Jiggle Belt",
      note="AI gag: a man stands strapped into a 1950s vibrating belt machine round his chest, calmly eating chips while it shakes him"),
 dict(id="L01", kind="l3", start="The fastest way I know", end="as hungry", tail=0.3, heading="Lose The Fat",
      points=["Appetite Meds (Ask A Doctor)", "AI Calorie Tracking", "No Liquid Calories"], reveal=["Zepbound", "tracking", "cutting"],
      note="the script's LOSE THE FAT list, on the side card so you stay on screen"),
 dict(id="G06", kind="lt", topic_case="preserve", start="On Zepbound, I went", end="as hungry", tail=0.6, topic="WHAT I DID",
      point="192 To About 175 Pounds In 3 Months", parts=[["192 To About 175 Pounds", "192"], ["In 3 Months", "three months"]]),
 dict(id="C01", kind="clip", start="Ask your doctor", end="not a doctor", tail=0.25, src=["A0166@0.5"], label=AI, people="other", physique=False,
      note="library A0166, the approved 'talk to your doctor' clip"),
 dict(id="C08", kind="clip", start="with an AI app", end="photo of your food", tail=0.1, src=["A0050@0.0"], label=AI, people="other", physique=False,
      note="library A0050 (AI): a man logs a plated meal on his phone at the kitchen counter; covers the take join before the phone card"),
 dict(id="P01", kind="phone", start="Try mine at", end="tracking app you like", tail=0.3, src=["B0038@1.0"], credit="AbsByAI.com",
      note="the real app: meal photo, itemised calories (library B0038, used in RO-16)"),
 dict(id="A4", kind="ai", start="And cut every liquid calorie", end="alcohol", tail=0.3, name="Four Straws",
      note="AI gag: a man drinks soda, juice, a sweet coffee and a beer at once through four long straws; the levels drop and he sighs happily"),
 dict(id="G07", kind="lt", topic_case="preserve", start="The second step is to build", end="your chest", tail=1.5, topic="STEP 2 OF 2", over_full=True,
      point="Build Your Chest", parts=[["Build Your Chest", "build your chest"]]),
 dict(id="C02", kind="clip", start="Push-ups", end="chest flies", tail=0.0, src=["B0546@0.2"], grade="eq=saturation=0.72:brightness=0.015,colorbalance=rm=-0.07:gm=-0.01:bm=0.03", people="dan", physique=True,
      note="Dan's real B-roll: push-ups on the handles"),
 dict(id="C03", kind="clip", start="build the muscle", end="saggy man boob", tail=0.25, src=["B0668@0.2"], grade="eq=brightness=0.035:saturation=1.3", people="dan", physique=False,
      note="Dan's real B-roll, 10/23 gym: chest fly machine from a low angle, no wall logos (Color C, lifted to sit with the studio)"),
 dict(id="R02", kind="scene", scene="portraits", start="As that fat comes off", end="man's chest", tail=0.3, label="Real Photos Of Me, Not AI-Generated",
      photos=["studio-blue-249", "studio-blue-110", "studio-blue-6"], people="dan", physique=True, note="three real studio portraits on 'what's left looks like a man's chest'"),
 dict(id="G08", kind="lt", topic_case="preserve", start="So add push-ups", end="reducing calories", tail=0.2, topic="ACTION STEP",
      point="Add Push-Ups And Chest Flies This Week", parts=[["Add Push-Ups And Chest Flies", "add push"], ["This Week", "this week"]]),
 dict(id="A5", kind="ai", start="you'll be shocked", end="few months", tail=0.3, name="T-Shirt Double Take",
      note="AI: a lean man tries on a fitted white T-shirt, sees himself, raises his eyebrows and smiles; his girlfriend looks up from her phone and does a double take"),
 # ---------------- the fix for true gynecomastia
 dict(id="G09", kind="lt", topic_case="preserve", start="Now let's talk about the fix", end="gynecomastia", tail=1.5, topic="PART 2", over_full=True,
      point="The Fix For True Gynecomastia", parts=[["The Fix For True Gynecomastia", "fix for true"]]),
 dict(id="C04", kind="clip", start="See a doctor first", end="what it is", tail=0.25, src=[f"{ST}/p7579840.mp4@1.0"], crop=(2160, 1215, 0, 1560), people="other", physique=False,
      note="Pexels 7579840: a doctor and a male patient at a desk"),
 dict(id="L02", kind="l3", start="In about a quarter of cases", end="other substances", tail=0.4, heading="What Causes It",
      points=["1 In 4: Left Over From Puberty", "1 In 4: No Known Cause", "Up To 1 In 4: Drugs"], reveal=["about a quarter", "another quarter", "up to a quarter"],
      note="source: American Family Physician, Dickson 2012"),
 dict(id="A7", kind="ai", start="Anabolic steroids", end="never goes away", tail=0.3, name="The Locker Room Flex",
      note="AI: a huge bodybuilder flexes in the locker room mirror, glances down, his smile fades and he quietly pulls a loose T-shirt out of his bag"),
 dict(id="G10", kind="lt", topic_case="preserve", start="Anabolic steroids", end="never goes away", tail=0.5, topic="AMERICAN FAMILY PHYSICIAN", over_full=True,
      point="Up To 1 In 4 Cases: Drugs, Including Steroids", parts=[["Up To 1 In 4 Cases: Drugs, Including Steroids", "anabolic"]]),
 dict(id="L03", kind="l3", start="Less often it comes from", end="anything else", tail=0.3, heading="Less Often",
      points=["Low Testosterone", "Liver Or Thyroid Problem", "Very Rarely, A Tumor"], reveal=["low testosterone", "liver", "tumor"]),
 dict(id="G11", kind="lt", topic_case="preserve", start="Now, diet won't remove", end="still be there", tail=0.5, topic="KEY POINT",
      point="Losing Fat Won't Shrink The Disc", parts=[["Losing Fat Won't Shrink The Disc", "diet won't"]]),
 dict(id="C05", kind="clip", start="If it's been there a long time", end="surgery is the fix", tail=0.3, src=[f"{ST}/p7584434.mp4@2.0"], people="other", physique=False,
      note="Pexels 7584434: a surgical team at work, nothing graphic"),
 dict(id="A8", kind="ai", start="So if it's a firm disc", end="another diet", tail=0.3, name="Push The Diets Aside",
      note="AI: a fed-up man pushes his stack of diet books aside and picks up his phone to call"),
 dict(id="G12", kind="lt", topic_case="preserve", start="So if it's a firm disc", end="another diet", tail=0.5, topic="ACTION STEP", over_full=True,
      point="Firm Disc? Book The Doctor", parts=[["Firm Disc? Book The Doctor", "book the doctor"]]),
 dict(id="G13", kind="lt", topic_case="preserve", start="So don't assume", end="diagnosis", tail=0.5, topic="KEY POINT",
      point="Get A Diagnosis Before You Assume", parts=[["Get A Diagnosis Before You Assume", "don't assume"]]),
 # ---------------- recap
 dict(id="L04", kind="l3", start="If you have chest fat", end="of you guys", tail=0.3, heading="Chest Fat", pad_to_next=True,
      points=["Appetite Meds (Ask A Doctor)", "AI Calorie Tracking", "No Liquid Calories", "Push-Ups And Chest Flies"], reveal=["Zetbound", "AI calorie", "cutting liquid", "push"]),
 dict(id="L05", kind="l3", start="If it's true gynecomastia", end="surgery is the fix", tail=0.3, heading="Gynecomastia",
      points=["See A Doctor", "Find The Cause", "Long Term? Surgery"], reveal=["see a doctor", "find the cause", "been there a long time"]),
 dict(id="C06", kind="clip", start="Either way", end="rest of your life", tail=0.3, max_len=2.1, src=["A0077@0.0"], label=AI, people="other", physique=True,
      note="library A0077 (AI): a fit man pulls his shirt off at the pool and his wife smiles, the payoff to the pool shirt"),
 dict(id="G14", kind="lt", topic_case="preserve", start="and go to", end="published", tail=-0.5, topic="SUBSCRIBE",
      point="New Videos First At SixPackAbs.com", parts=[["New Videos First", "go to"], ["At SixPackAbs.com", "newest videos"]]),
]
from grades import GR
for _it in PLAN:
    if _it["id"] in GR: _it["grade"] = GR[_it["id"]]
