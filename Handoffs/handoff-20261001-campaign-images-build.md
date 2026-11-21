# Handoff: build the campaign image set (cold + remarketing) in the approved direction

Written 2026-10-01 by Claude (Campaign Images Research AD). Not executed.
Recommended: **Claude Opus 5.5, high effort.** Task name: `Campaign Images Build AD`.
**Use the Codex subscription to generate the images** (`.claude/skills/_shared/codex-image.sh`, rule in
`.claude/skills/_shared/IMAGE-GENERATION.md`).

## Goal

Make the still images for Google Ads: 10 for the cold Performance Max campaign and 10 for the Demand Gen remarketing
campaigns, **five versions of each**, all in the direction Dan approved on 2026-10-01. Show Dan every version on one
review page, stop for his picks, then export the finals. **This task does not build or change any campaign.**

Research behind it: `Docs/CAMPAIGN_IMAGES_RESEARCH.md` (sections 6 and 7 of that file, the old concept lists, are
replaced by this handoff).

## The approved direction (Dan, 2026-10-01)

Dan rejected the first mockups (a kettlebell with "7 DAYS FREE", his photo in front of an empty gym) as generic:
"this is just bullshit that no one's going to click on... it looks like you're signing up to do a whole bunch of work."
He rejected text-heavy cards too. He then approved three samples: "I think you nailed it with these samples. They're
all attention-getting without risking Google Ads policy."

**Every image tells a small story at a glance, with one short headline of Dan's own.** Three styles:

| Style | What it is | Approved sample |
|---|---|---|
| A. Dan in a staged scene | Dan's real photo, grinning, in front of an AI scene that acts out the headline | `dan_trainers_hate_him.jpg`: six furious personal trainers glaring behind him, "HUMAN TRAINERS HATE HIM" |
| B. The ripped older dad | A photoreal family snapshot of a gray-haired dad around 50 who is strikingly lean, in an everyday moment with his kids. Attention comes from the mismatch of gray hair and kids with that body. | `ai_gray_dad.jpg`: flexing by a pool, a kid hanging off each arm, "HOW 40+ DADS CAN GET ABS" |
| C. The comic story | An obviously staged joke that tells the ad's argument in one look | `ai_fire_your_trainer.jpg`: a sad trainer carries out his box while a robot with a whistle spots a grinning dad, "FIRE YOUR PERSONAL TRAINER" |

Samples: `output/campaign-images-mockups-20261001/` (local only, not in git).

**Never again:** objects or equipment with an offer line, an empty gym, charts, tables, price cards, bullet lists,
anything that looks like work to be done. **No transformation of any kind:** no mirror, no before and after, no
"two versions of one man" (Dan: Google would refuse the mirror sample).

## Rules for every image

- **Text:** one headline, 2 to 5 words, two lines at most, in the top band. Manrope ExtraBold, first line white,
  second line yellow `rgb(255,214,10)`, black stroke, centred (the samples' look). Type is always set in code, never
  generated. Text never covers a face or abs. Everything important sits in the centre 80%.
- **Headlines come only from Dan's own approved lines** (`/ad-copy` skill, `DAN_APPROVED`). No new wording, no offer
  lines, no result numbers, never the word "trick".
- **Dan is never redrawn.** Codex makes the scene with an empty space for him; his real cutout
  (`photos/finalized social media photos/_cutouts/`) goes on in code with a soft shadow, then gets graded in code to
  match the scene's light. Smiling or neutral, never frowning. Abs visible. Speedo photos crop at the waistband.
- **Style B bodies:** "lean and shredded, not bulky, not a bodybuilder". It must look like a real phone photo, with a
  large, clear face. Kids are always fully dressed for the setting (swim shirts and shorts at a pool).
- **Generated plates carry no text, no logos, no readable words.** No logo is added on the image (the campaign has its
  own logo asset).
- **Check every generated image at full size** before it goes on the review page: hands, fingers, faces, extra limbs,
  gibberish text. Regenerate a bad one; do not show it.
- At least one image with no text in each shape, as Google asks (marked "clean" below).

## The image list

Shapes: landscape 1.91:1, square 1:1, portrait 4:5. Generate each plate in its own shape.

### Cold set (Performance Max)

| Slot | Shape | Style | Scene | Headline |
|---|---|---|---|---|
| K1 | Landscape | A | Dan in front of the furious trainers (approved design, new photo of Dan) | HUMAN TRAINERS / HATE HIM |
| K2 | Square | A | Same | HUMAN TRAINERS / HATE HIM |
| K3 | Landscape | C | Fired trainer with his box, robot spotting the dad (approved) | FIRE YOUR / PERSONAL TRAINER |
| K4 | Square | C | Same | FIRE YOUR / PERSONAL TRAINER |
| K5 | Square | B | Gray-haired ripped dad by the pool, a kid on each arm (approved) | HOW 40+ DADS / CAN GET ABS |
| K6 | Landscape | B | Same scene | clean, no text |
| K7 | Landscape | C | Angry trainers with their faces pressed to a garage window, watching a dad train happily with his phone | TRAINERS HATE / THIS AI APP |
| K8 | Square | B | Gray-haired ripped dad on a beach, carrying one kid on his shoulders and one under his arm, all laughing | clean, no text |
| K9 | Portrait | B | Gray-haired ripped dad at the backyard grill, shirtless, a kid on his shoulders, the other dads at the barbecue staring | HOW BUSY DADS / GET ABS |
| K10 | Portrait | A | Dan in front of a boardroom of furious executives in suits, the table piled with unbranded supplement tubs | SUPPLEMENT CORPS / HATE HIM |

### Remarketing set (Demand Gen remarketing `24305381214`, `24316408288`)

More of Dan, because these people already know his face. 6 Dan, 4 AI.

| Slot | Shape | Style | Scene | Headline |
|---|---|---|---|---|
| R1 | Landscape | A | Dan in front of his own 40th birthday party: "40" balloons, a cake, guests gawking at him | HOW I GOT / ABS AT 40 |
| R2 | Square | A | Same | HOW I GOT / ABS AT 40 |
| R3 | Landscape | A | Dan in front, a friendly robot coach behind him with a whistle and clipboard giving a thumbs up | HOW AI / GOT ME ABS |
| R4 | Square | A | Same | HOW AI / GOT ME ABS |
| R5 | Portrait | A | Dan and the furious trainers (K2's scene, portrait plate) | HUMAN TRAINERS / HATE HIM |
| R6 | Landscape | A | Dan and the furious trainers | clean, no text |
| R7 | Landscape | C | A nutritionist in a white coat walks out with her box while a robot chef serves a grinning dad a plate of real food | FIRE YOUR / NUTRITIONIST |
| R8 | Square | C | Same | FIRE YOUR / NUTRITIONIST |
| R9 | Square | B | Gray-haired ripped dad in the driveway washing the car, kids spraying him with the hose | clean, no text |
| R10 | Portrait | B | The pool dad (K5's scene, portrait plate) | HOW 40+ DADS / CAN GET ABS |

Round two, not now: Ad 13 cost angle, and new takes on whichever style wins.

## Five versions of each slot (Dan's instruction)

20 slots x 5 = **100 finished images.** A version must differ in something a viewer notices:

- **Style A:** a different photo of Dan AND a different take of the scene (cast, setting, how they react). Dan asked
  to change the photo in the trainers image and keep the design, so the five K1/K2 versions are the place he picks
  his photo. Candidates that fit the rules: `studio-white-49`, `studio-white-25`, `studio-white-1`, `studio-white-90`,
  `studio-blue-222`, `studio-blue-10` (white-42 was the mockup). Look through the cutouts for others.
- **Style B:** a different man (hair, beard, build stays lean), different kids, different pose or setting detail.
- **Style C:** a different take of the joke (who is in it, the robot's design, the angle).
- Where a slot has a headline, at most two of its five versions may use another line of Dan's that fits the scene
  (for example K1: "TRAINERS DESPISE HIM").

State the image count before each batch. Run several at once with `&` and `wait`.

## Budget

Codex on the ChatGPT subscription first; it costs no cash. Dan authorised **up to $50 of paid AI image generation**
for this task (above the usual $25 session cap, for this task only). Spend it only on an image Codex has failed
twice (`ALLOW_API_IMAGE=1`) or on a second model's take of a slot where all five Codex versions are weak. Say so in
chat with the cost and keep a running total. Upscaling is local only.

## Prompts that produced the approved samples (start from these)

K1/K2 scene (medium effort):

> Square 1:1 photorealistic image, no text, no logos, no readable words anywhere. Inside a big commercial gym, six personal trainers (four men, two women, late 20s to 30s, very fit, matching plain black polo shirts, whistles around their necks, some holding clipboards) stand in a line across the back, arms crossed, all glaring angrily and jealously straight at the camera, scowling, exaggerated annoyed expressions, slightly comedic. Three stand on the left third of the frame and three on the right third. The centre third of the frame is left open and empty, showing only the gym floor and equipment behind, as space for a person to be added in the foreground later. The trainers are seen from the knees up, their heads in the middle band of the frame, the top quarter of the frame is plain dark gym ceiling. Dramatic, punchy, high contrast lighting, sharp, vivid colour.

K5 scene (medium effort):

> Square 1:1 photorealistic photo, no text, no logos, no readable words anywhere. A candid family snapshot in a sunny suburban backyard next to a swimming pool, looks like a real photo taken on a phone, not a stock photo and not a studio shot. A dad around 50 years old with a full head of silver gray hair and a short gray beard stands shirtless in navy swim shorts, facing the camera, laughing. He is strikingly lean and shredded with a sharply defined six-pack, visible obliques and veins on his forearms: lean and athletic like a fitness model, not bulky, not a bodybuilder. He is flexing both arms out to the sides, and his two kids are hanging off his biceps with their feet off the ground, laughing: a boy about 9 on one arm and a girl about 7 on the other, both wearing colourful swim shirts and shorts. His torso and abs are fully visible and unobstructed in the centre of the frame. Bright natural afternoon sunlight, vivid colour, sharp focus on the dad. The dad's head sits about one third down from the top; the top fifth of the frame is plain blue sky and treetops with nothing important in it.

K3/K4 scene (medium effort):

> Square 1:1 photorealistic image, no text, no logos, no readable words anywhere. A funny, instantly readable scene in a bright modern gym. In the foreground on the left, a very muscular human personal trainer in his 30s, wearing a plain black polo shirt, walks toward the camera looking sad, defeated and humiliated, carrying a cardboard box of his belongings: a whistle on a lanyard hanging over the edge, a clipboard, a protein shaker and a small potted plant. Behind him on the right, in sharp focus, a sleek white and chrome humanoid robot with a friendly glowing blue visor and a whistle around its neck stands at the head of a bench press, hands under the barbell, spotting an ordinary, cheerful 45 year old dad in a grey t-shirt who is lifting and grinning. The robot is the clear centre of attention. Vivid colour, punchy high contrast lighting, sharp, cinematic, slightly comedic. All three figures sit in the lower three quarters of the frame; the top quarter of the frame is plain dark gym ceiling with nothing in it.

Composite recipe used: plate resized to the final size, Dan's cutout cropped to its box and scaled so his head sits
just under the headline and his abs are fully in frame, a blurred black shadow behind him, headline centred at the
top. The sample's lighting on Dan did not match the gym; fix that with a grade on the cutout.

## Steps

1. Read this file, `Docs/CAMPAIGN_IMAGES_RESEARCH.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, and the
   `/ad-copy` skill's approved lines. Look at the three samples.
2. Generate and build all 100 versions. Work in `output/campaign-images-20261001/` (local, not in git: the repo is
   public and these include Dan's photos).
3. Build one review page, grouped by slot, five versions side by side, each with a short id (K1-a to K1-e). Put the
   pick list at the bottom. **Stop for Dan's picks.** He may pick up to two versions per slot.
4. Export the picks: landscape 1200x628, square 1200x1200, portrait 960x1200, JPG under 5 MB. Upload the finals folder
   to Google Drive with anyone-with-the-link view. Write `Docs/CAMPAIGN_IMAGES_FINALS.md`: slot, file name, headline,
   style, which are AI-made (the campaign build sets Google's AI label on those), and the Drive link.
5. Stop. The Performance Max build and the remarketing image ads are a separate task that takes this folder.

## Open risks

- Codex redraws people and adds bulk; that is why Dan is composited and Style B prompts say "not bulky".
- Children appear in Style B. Keep them clothed, happy and incidental; the dad is the subject.
- 100 generations is a large draw on the Codex allowance (about 15,000 to 40,000 tokens each). Tell Dan the count
  before starting.
- The Performance Max credit's terms are still unread; that belongs to the campaign build task.

## Starter prompt

> Name this task `Campaign Images Build AD`. Read `Handoffs/handoff-20261001-campaign-images-build.md` and execute it.
> Build the 20 campaign images (10 cold, 10 remarketing) in the direction I approved, five versions of each, 100 in
> total. Use the Codex subscription to generate the images. You may spend up to $50 on paid image generation only where
> Codex fails. Put every version on one review page and stop for my picks. Do not build or change any campaign.

Model: Claude Opus 5.5, high effort.
