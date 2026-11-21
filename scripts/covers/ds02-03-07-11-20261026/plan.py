"""Muhammad Shorts Batch A covers (DS-02, DS-03, DS-07, DS-11), 2026-10-26. Mix per VIDEO-RULES 2026-10-25:
A and B two distinct AI Dan concepts acting the topic, C one real studio photo on a Codex scene, D and E history-guided
Codex choices (D a third AI Dan, E a two-panel AI story). All generated with codex-image.sh, gpt-6.1-sol, high."""
from pathlib import Path
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
R=P/'Short-form video content/covers/review/ds-batch-a-20261026'
PH=P/'photos/finalized social media photos'
STYLE=("Vertical 9:16 photorealistic premium editorial fitness photography, masculine saturated palette, crisp directional light, "
 "large readable subject on a phone. No text, letters, digits, logo, watermark, labels or written marks anywhere. No branded packaging. ")
DAN=("Use the attached real photo only as an identity reference. The man is clearly Dan from that photo, same face, short black hair, "
 "Asian features, lean and shredded, not bulky, same size as the reference. Shirtless in plain dark athletic shorts. Sharply defined abs, "
 "whole arms and natural fingers, no stomach touching or pinching. ")
TOP="Upper 36% of the frame is plain dark uncluttered background with no head or objects; person and action in the lower 62%, entire hair and head visible. "
LOW="Lower 40% of the frame is a plain dark uncluttered area (floor, counter front or shadow) with no face in it; the man's head and torso fill the upper-middle of the frame with hair fully visible below the top 6%. "
LEFT="Person stands in the right two thirds of the frame; the left third and the top 30% are calm dark background for type; hair fully visible. "
TWO=("Two stacked photographic panels separated by a blank pure black horizontal band across the centre, band 20% of frame height. "
 "Nothing touches the band. Both panels show the same man with the same face. ")
STUDIO=("BACKGROUND ONLY, no person, no hands, no human figure. Upper 36% uncluttered dark negative space for typography. "
 "Centre lower two thirds clear for a real portrait composited later; topic props toward the lower side edges. ")
SHORTS={
 'ds02':dict(title='How Getting Abs Looksmaxxes Your Face',lines=['How Getting Abs','Looksmaxxes Your Face'],badge='LOOKSMAXXING',
  slug='how-getting-abs-looksmaxxes-your-face',photo='studio-white-23',
  a="Dan in a modern bathroom leaning toward a mirror, running his thumb along his sharp chiseled jawline, confident satisfied closed-mouth smile, face in three-quarter view toward camera, cool steel-blue and warm amber light. ",
  b="Dan holding up a printed old photo of his own face from when he was much heavier, round puffy cheeks and double chin, next to his now lean angular face, raised eyebrow and amused grin at camera, deep teal studio backdrop. ",
  d="Dramatic close side-profile portrait of Dan from chest up turned three-quarter, razor sharp jawline and cheekbones carved by hard rim light, defined shoulders and upper abs, looking slightly off camera with quiet confidence, charcoal backdrop with red edge light. ",
  e="TOP panel: Dan heavier, about 200 pounds, round bloated puffy face with double chin and soft belly, plain grey t-shirt, dull flat light, unhappy neutral expression. BOTTOM panel: the same Dan now lean and shredded, shirtless, sharp jawline and defined cheekbones, confident smile, bright golden light.",
  scene="Moody luxury bathroom with a large round backlit mirror at right, marble counter, grooming items at lower left edge, deep navy and warm brass light. "),
 'ds03':dict(title='The 3 Most Important Supplements For Men',lines=['The 3 Most Important','Supplements For Men'],badge='SUPPLEMENTS',
  slug='the-3-most-important-supplements-for-men',photo='studio-blue-145',
  a="Dan at a dark kitchen counter holding three plain unlabeled supplement bottles fanned in one hand toward camera: an amber jar of golden fish oil softgels, a small brown dropper bottle, a white bottle of capsules, confident knowing smile, warm amber light. ",
  b="Dan at a counter pushing a big messy pile of a dozen plain unlabeled supplement bottles off to one side with his forearm while three bottles (amber jar of fish oil softgels, small brown dropper bottle, white capsule bottle) stand neatly in front of him, playful smirk at camera, cool blue light. ",
  d="Dan in morning sunlight by a kitchen window about to swallow one golden fish oil softgel held between two fingers, glass of water in the other hand, relaxed confident look at camera, fresh green and gold palette. ",
  e="TOP panel: a cluttered shelf jammed with a dozen plain unlabeled supplement tubs and bottles, gathering dust, dim cold light. BOTTOM panel: Dan shirtless and shredded smiling at camera holding just three plain bottles (amber jar of fish oil softgels, small brown dropper bottle, white capsule bottle), bright warm light.",
  scene="Dark slate kitchen counter, a few golden fish oil softgels and plain unlabeled supplement bottles grouped at lower left and lower right edges, soft sunrise rim light, deep forest green tones. "),
 'ds07':dict(title='Top 3 Ways To Use AI To Get Abs',lines=['Top 3 Ways To Use AI','To Get Abs'],badge='AI FITNESS',
  slug='top-3-ways-to-use-ai-to-get-abs',photo='studio-blue-213',
  a="Dan standing at a kitchen counter holding his phone over a plate of grilled chicken breast and broccoli to photograph it, the phone screen faces the camera showing the same plate with a glowing cyan scan outline, he looks at camera with a sly grin, dark kitchen with electric cyan accents. ",
  b="Dan surrounded by a futuristic translucent cyan holographic interface: glowing scan lines tracing his abs, abstract graphs and rings floating beside him, no readable text, he looks at camera impressed and confident, dark navy tech studio. ",
  d="Dan holding his phone up beside his face facing the camera; the phone screen shows an even more shredded version of himself, he points at the screen with his other hand and grins, clean bright teal backdrop. ",
  e="TOP panel: a frustrated man's hands weighing food on a kitchen scale beside a messy paper food log and calculator, dull grey light. BOTTOM panel: Dan shirtless and shredded smiling, simply snapping a photo of his chicken and broccoli plate with his phone, glowing cyan light.",
  scene="Dark modern tech kitchen, a plate of grilled chicken and broccoli at lower left edge, a phone with a glowing cyan screen and plain supplement bottles at lower right edge, electric cyan and navy palette. "),
 'ds11':dict(title='Why You Must Weigh Yourself Daily',lines=['Why You Must Weigh','Yourself Daily'],badge='DAILY WEIGH-IN',
  slug='why-you-must-weigh-yourself-daily',photo='studio-gray-87',
  a="Dan standing on a sleek glass bathroom scale in a bright bathroom at sunrise, looking down at the scale then up with a calm satisfied smile, one hand on hip, whole body from head to feet visible on the scale, warm morning light. ",
  b="Dan holding a sleek glass bathroom scale under one arm like a trophy, pointing at the camera with the other hand, confident grin, cool blue studio backdrop. ",
  d="Low wide angle from the floor: Dan stepping onto a bathroom scale first thing in the morning, his bare feet and the scale large in the foreground, his lean torso and face looking down at the camera with a determined smile above, soft sunrise window light. ",
  e="TOP panel: Dan heavier about 200 pounds in a loose t-shirt stepping onto a bathroom scale, worried expression, dim light. BOTTOM panel: the same Dan now lean and shredded shirtless on the same scale, calm confident smile, bright morning light.",
  scene="Bright minimalist bathroom at sunrise, a sleek glass bathroom scale on the floor at lower left, white towels and a plant at lower right edge, warm gold and clean white palette. "),
}
def jobs():
 out=[]
 for k,s in SHORTS.items():
  ref=[str(PH/(s['photo']+'_FINAL_PRIMARY.jpg'))]
  for which,prompt,r in [('a',STYLE+DAN+TOP+s['a'],ref),('b',STYLE+DAN+LOW+s['b'],ref),('studio',STYLE+STUDIO+s['scene'],[]),
                         ('d',STYLE+DAN+LEFT+s['d'],ref),('e',STYLE+DAN+TWO+s['e'],ref)]:
   out.append(dict(key=k,which=which,prompt=prompt,ref=r,out=str(R/'assets/gen'/f'{k}-{which}.png')))
 return out
