// AI cover clips for the joins, rev 3.
//
// Dan: "Make an AI-generated video to cover these awkward cuts... Cover that awkward cut with
// an AI-generated clip illustrating what's being said in the video at the time."
//
// One clip per join WE created by removing a pause or a clause. Each illustrates the line it
// lands on. Native 9:16 so it goes in full-bleed at ~1.0x rather than being cropped out of
// 16:9. No people unless the casting rule can be met (white or Asian men 30-50); no text or
// graphics in frame - our own caption band and title sit over these.
module.exports = [
  // ⚠ REV 4, Dan: "for the vitamin D one, the third one at 3 seconds, there's kind of an
  // awkward cut... cover that with an AI-generated video that's about 3 or 4 seconds long of a
  // ripped man in his 40s, shirtless, taking vitamin D... make it a good video since it's in
  // the beginning." Three attempts generated; the best is picked by eye. Casting is stated
  // explicitly (the standing rule is white or Asian men 30-50) and the prompt names no label
  // surface, because anything with a label invites invented lettering.
  // PICKED: j0a, copied to j0.mp4. Chosen on CONTENT, not looks - it is the dropper, and this
  // short's own script recommends liquid vitamin D over capsules ("cheaper per dose if you take
  // liquid versus capsule"), so j0b's capsule would have contradicted the line it sits over.
  // j0c was rejected: backlit to near-silhouette, the action is not readable.
  { id: 'j0a', seg: 'J', after: 'Critically, critically important', why: "Dan's ask, attempt A - PICKED",
    prompt: 'Cinematic photorealistic shot in a bright modern bathroom with soft morning window light. A lean muscular Asian man in his early forties, shirtless with visible abs, tilts his head slightly back and places a few drops from a small plain glass dropper onto his tongue, then lowers it and smiles faintly. Warm natural light, shallow depth of field, premium fitness advertising look. One person only. No text, no labels, no packaging, no lettering.' },
  { id: 'j0b', seg: 'J', after: 'Critically, critically important', why: "attempt B - kitchen, capsule",
    prompt: 'Cinematic photorealistic shot in a sunlit modern kitchen. A lean athletic white man in his early forties, shirtless with a defined midsection, holds a single small golden softgel capsule between his fingers, raises it, takes it with a glass of water and sets the glass down. Warm morning light streaming across him, shallow depth of field, premium fitness advertising look. One person only. No text, no labels, no packaging, no lettering.' },
  { id: 'j0c', seg: 'J', after: 'Critically, critically important', why: "attempt C - by a window, sunlight",
    prompt: 'Cinematic photorealistic slow shot. A muscular Asian man in his early forties, shirtless with visible abs, stands in warm golden sunlight beside a large window, tilts his head back and takes a supplement dropper under his tongue, then turns his face into the sun with his eyes closed. Strong warm backlight, dust motes in the air, shallow depth of field, premium fitness cinematography. One person only. No text, no labels, no packaging, no lettering.' },
  { id: 'h1', seg: 'H', after: 'benefits for muscle building',
    why: "Dan's explicit ask: illustrate creatine's benefits for muscular and brain health",
    prompt: 'Cinematic photorealistic 3D medical visualization on a deep black background. A translucent anatomical human torso slowly rotates as dense skeletal muscle fibres illuminate from within in warm amber light, the glow travelling upward until the brain lights with the same warm energy. Slow controlled camera push in, shallow depth of field, premium science documentary look. No people, no text, no graphics, no lettering.' },
  { id: 'h2', seg: 'H', after: 'diarrhea and gas that I get',
    why: 'lands on "For you, though, that probably isn\'t gonna happen" - creatine taken normally',
    prompt: 'Cinematic photorealistic shot in a bright modern kitchen. A fit Asian man in his late thirties wearing a plain dark t-shirt stirs a white powder into a tall glass of water with a spoon, lifts it and drinks calmly, relaxed and healthy. Soft natural window light, shallow depth of field. One person only. No text, no graphics, no lettering.' },
  { id: 'c1', seg: 'C', after: 'it should be fish oil',
    why: 'lands on "Fish oil improves your heart health"',
    prompt: 'Cinematic extreme macro in slow motion. Translucent golden amber omega-3 fish oil softgel capsules tumble and settle against a clean bright white surface, warm light refracting through them. Very shallow depth of field, premium pharmaceutical advertising look. No people, no text, no graphics, no lettering.' },
  { id: 'c2', seg: 'C', after: 'the most proven supplement that you can take',
    why: 'lands on "especially if you\'re not eating a lot of fish right now"',
    prompt: 'Cinematic overhead shot, slow drift. Fresh raw salmon fillets glistening on crushed ice at a clean fish market counter, deep orange flesh, cool natural daylight, water droplets catching the light. Photorealistic food cinematography. No people, no text, no graphics, no lettering.' },
  { id: 'j1', seg: 'J', after: 'daily vitamin D supplementation',
    why: 'lands on the vitamin D dosing advice - sunlight is the plain visual for vitamin D',
    prompt: 'Cinematic photorealistic shot. Warm golden morning sunlight streams through a tall window across a clean stone kitchen counter, dust motes drifting slowly through the light beam, long soft shadows. Slow gentle camera drift. No people, no text, no graphics, no lettering.' },
  { id: 'm1', seg: 'M', after: 'it has other health benefits too',
    why: 'lands on "And then finally, it has zinc"',
    prompt: 'Cinematic extreme macro, slow rotation. A small pile of matte silver-grey mineral supplement tablets on a dark slate surface, one directional cool light raking across them revealing texture. Very shallow depth of field, premium product photography. No people, no text, no graphics, no lettering.' },
  { id: 'd1', seg: 'D', after: "It's only about 5%",
    why: 'lands on the point that training and sleep are the other 95%',
    prompt: 'Cinematic photorealistic shot in a dim industrial gym, dramatic side lighting. A lean athletic Asian man in his late thirties performs a heavy barbell back squat, chalk dust in the air, deep shadows and a single warm key light. Slow motion, shallow depth of field. One person only. No text, no graphics, no lettering.' },
  { id: 'd2', seg: 'D', after: 'so I always iron my clothes before I go out on a date',
    why: 'lands on "For that same reason, you should be taking supplements" - his own analogy',
    prompt: 'Cinematic photorealistic close shot. A man\'s hands press a hot iron across a crisp white dress shirt on an ironing board, a soft plume of steam rising and catching warm evening window light. Shallow depth of field, calm and premium. Hands only, no face. No text, no graphics, no lettering.' },
  { id: 'e1', seg: 'E', after: "I just wasn't consistent",
    why: 'lands on "It\'s better to take one or two supplements consistently every day"',
    // ⚠ REGENERATED. The first version put a weekly pill organiser in frame and the model
    // wrote garbled day labels on it ("MON MON THE 2ND FRI"). Anything with a label surface
    // invites invented lettering - ask for objects that carry no text at all.
    // ⚠ casting stated explicitly. The regenerated version came back with hands that did not
    // match the standing b-roll casting rule (white or Asian men 30-50) - a hands-only shot
    // still shows a person, so the rule still applies.
    prompt: 'Cinematic photorealistic close overhead shot. The open palm of an athletic East Asian man in his late thirties holds two plain white capsules beside a simple glass of water on a bright stone kitchen counter in soft morning light. His other hand lifts the glass. Calm, orderly, deliberate. Hands and forearms only, no face, no bottles, no labels, no packaging. No text, no graphics, no lettering.' },
];
