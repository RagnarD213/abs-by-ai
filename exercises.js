// ============================================================
// EXERCISE LIBRARY — the authoritative whitelist for the AI trainer.
// The model SELECTS and SEQUENCES from this list; it never invents moves.
// equip: 'none' (bodyweight + a towel everyone has)
//      | 'min' (minimal ≤$200 home kit: kettlebell, push-up handles, ab wheel, mat)
//      | 'full' (full gym / full home gym: dumbbells, barbells, machines, cables).
// A user's equipment unlocks tiers cumulatively: full ⊃ min ⊃ none.
// (v3: dumbbells are 'full' equipment now, not minimal — old 'db' moves are 'full'.)
// swap: the pre-baked one-tap substitute (same or lower equipment tier,
// joint-friendlier or simpler variation).
// video: hand-curated YouTube URL (null until curated — UI hides the button).
// Loaded by both server.js (require) and index.html (<script src>).
// ============================================================
const EXERCISES = [
  // ── Warm-up moves (bodyweight) ──
  { id: 'march-in-place', name: 'March in Place', equip: 'none', cat: 'warmup', muscles: 'full body',
    setup: 'Stand tall, arms relaxed.', execution: 'March with high knees at an easy pace, swinging arms naturally.', mistake: 'Slouching — keep the chest up and core lightly braced.', swap: 'jumping-jack', video: 'https://www.youtube.com/watch?v=QilgMPG7OaA' },
  { id: 'jumping-jack', name: 'Jumping Jacks', equip: 'none', cat: 'warmup', muscles: 'full body',
    setup: 'Stand with feet together, arms at sides.', execution: 'Jump feet out while raising arms overhead, then jump back to start. Stay light on the balls of your feet.', mistake: 'Landing flat-footed and heavy — land softly with a slight knee bend.', swap: 'march-in-place', video: 'https://www.youtube.com/watch?v=uLVt6u15L98' },
  { id: 'arm-circles', name: 'Arm Circles', equip: 'none', cat: 'warmup', muscles: 'shoulders',
    setup: 'Stand tall, arms extended straight out to the sides.', execution: 'Make slow controlled circles, small to large, forward then backward.', mistake: 'Rushing — slow circles warm the shoulder capsule better.', swap: 'cat-cow', video: 'https://www.youtube.com/watch?v=mwDgFY86zck' },
  { id: 'leg-swings', name: 'Leg Swings', equip: 'none', cat: 'warmup', muscles: 'hips, hamstrings',
    setup: 'Stand beside a wall or chair for balance.', execution: 'Swing one leg forward and back in a smooth arc, gradually increasing range. Then switch legs.', mistake: 'Rounding the lower back to force height — keep the torso upright.', swap: 'hip-circles', video: 'https://www.youtube.com/watch?v=D17eUtUt0zQ' },
  { id: 'hip-circles', name: 'Hip Circles', equip: 'none', cat: 'warmup', muscles: 'hips',
    setup: 'Stand with hands on hips, feet shoulder-width.', execution: 'Draw slow, big circles with your hips in both directions.', mistake: 'Tiny fast circles — go slow and wide to open the hips.', swap: 'leg-swings', video: 'https://www.youtube.com/watch?v=JYqLwajOGjI' },
  { id: 'cat-cow', name: 'Cat-Cow', equip: 'none', cat: 'warmup', muscles: 'spine, core',
    setup: 'On all fours, hands under shoulders, knees under hips.', execution: 'Alternate arching your back up (cat) and dipping it down with chest lifted (cow), moving with your breath.', mistake: 'Moving only the neck — the motion should travel through the whole spine.', swap: 'arm-circles', video: 'https://www.youtube.com/watch?v=xyNwxiuERXc' },
  { id: 'inchworm', name: 'Inchworm', equip: 'none', cat: 'warmup', muscles: 'hamstrings, shoulders, core',
    setup: 'Stand tall with feet hip-width.', execution: 'Hinge down, walk your hands out to a plank, pause, then walk them back and stand up.', mistake: 'Bending the knees a lot — keep them softly straight to stretch the hamstrings.', swap: 'worlds-greatest-stretch', video: 'https://www.youtube.com/watch?v=ml3MdmCkwbQ' },
  { id: 'worlds-greatest-stretch', name: "World's Greatest Stretch", equip: 'none', cat: 'warmup', muscles: 'hips, thoracic spine',
    setup: 'From a plank, step your right foot outside your right hand.', execution: 'Drop the back knee, sink the hips, then rotate the right arm to the ceiling. Switch sides.', mistake: 'Letting the front knee cave inward — keep it tracking over the foot.', swap: 'inchworm', video: 'https://www.youtube.com/watch?v=-CiWQ2IvY34' },

  // ── Bodyweight — push ──
  { id: 'pushup', name: 'Push-Up', equip: 'none', cat: 'push', muscles: 'chest, triceps, shoulders',
    setup: 'Plank position, hands slightly wider than shoulders, body in one straight line.', execution: 'Lower your chest to just above the floor with elbows ~45° from your body, then press back up.', mistake: 'Sagging hips — squeeze glutes and brace abs the whole set.', swap: 'incline-pushup', video: 'https://www.youtube.com/watch?v=Zi6c09DRGxk' },
  { id: 'incline-pushup', name: 'Incline Push-Up', equip: 'none', cat: 'push', muscles: 'chest, triceps',
    setup: 'Hands on a sturdy elevated surface (bench, counter, sofa arm), body straight.', execution: 'Lower chest to the edge, elbows ~45°, then press away.', mistake: 'Flaring elbows straight out — keep them at ~45°.', swap: 'knee-pushup', video: 'https://www.youtube.com/watch?v=0JUrOH--Kdk' },
  { id: 'knee-pushup', name: 'Knee Push-Up', equip: 'none', cat: 'push', muscles: 'chest, triceps',
    setup: 'Push-up position with knees on the floor, hips in line with shoulders and knees.', execution: 'Lower chest toward the floor and press back up without breaking the hip line.', mistake: 'Piking the hips up — keep a straight line from head to knees.', swap: 'incline-pushup', video: 'https://www.youtube.com/watch?v=z8nUnCdZXQI' },
  { id: 'pike-pushup', name: 'Pike Push-Up', equip: 'none', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'From push-up position, walk feet in and lift hips high into an inverted V.', execution: 'Bend elbows to lower the top of your head toward the floor, then press back up.', mistake: 'Shifting weight back to the legs — keep shoulders stacked over hands.', swap: 'pushup', video: 'https://www.youtube.com/watch?v=pHR5yG6xBps' },
  { id: 'chair-dip', name: 'Chair Dip', equip: 'none', cat: 'push', muscles: 'triceps, chest',
    setup: 'Hands on the edge of a sturdy chair behind you, legs extended, hips off the seat.', execution: 'Bend elbows straight back to lower your hips, then press up until arms are straight.', mistake: 'Shrugging shoulders toward ears — keep them pulled down.', swap: 'knee-pushup', video: 'https://www.youtube.com/watch?v=AWz_7B1cch0' },

  // ── Bodyweight — legs & hinge ──
  { id: 'chair-squat', name: 'Chair Sit-to-Stand', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Sit tall on the edge of a sturdy chair, feet flat and shoulder-width, arms crossed or reaching forward.', execution: 'Stand up under control without using your hands, squeeze the glutes at the top, then sit back down slowly.', mistake: 'Flopping back into the seat — lower slowly, the descent is half the work.', swap: 'wall-sit', video: null },
  { id: 'bw-squat', name: 'Bodyweight Squat', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Feet shoulder-width, toes slightly out, arms forward for balance.', execution: 'Sit hips back and down until thighs are at least parallel, then drive up through mid-foot.', mistake: 'Knees caving inward — push them out in line with the toes.', swap: 'wall-sit', video: 'https://www.youtube.com/watch?v=cB0cOX7gePg' },
  { id: 'split-squat', name: 'Split Squat', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Long stride stance, back heel up, torso tall.', execution: 'Lower the back knee toward the floor, then drive up through the front foot. Finish the set, then switch.', mistake: 'Front knee drifting far past the toes — keep the shin near vertical.', swap: 'bw-squat', video: 'https://www.youtube.com/watch?v=Ft-NS5Ogti0' },
  { id: 'walking-lunge', name: 'Walking Lunge', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Stand tall with room to walk forward.', execution: 'Step forward and lower until both knees are ~90°, then push through the front foot into the next step.', mistake: 'Short choppy steps — take a full stride so the front shin stays vertical.', swap: 'split-squat', video: 'https://www.youtube.com/watch?v=vYfp2t4XgqQ' },
  { id: 'reverse-lunge', name: 'Reverse Lunge', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Stand tall, feet hip-width.', execution: 'Step one foot back and lower the back knee toward the floor, then drive back to standing.', mistake: 'Leaning way forward — keep the torso mostly upright.', swap: 'split-squat', video: 'https://www.youtube.com/watch?v=u_zSfK5ZFU4' },
  { id: 'glute-bridge', name: 'Glute Bridge', equip: 'none', cat: 'legs', muscles: 'glutes, hamstrings',
    setup: 'Lie on your back, knees bent, feet flat and hip-width.', execution: 'Drive through heels to lift hips until body is straight from shoulders to knees. Squeeze glutes at the top.', mistake: 'Arching the lower back at the top — finish with the glutes, not the spine.', swap: 'bw-squat', video: 'https://www.youtube.com/watch?v=L9KZfxT654Y' },
  { id: 'single-leg-glute-bridge', name: 'Single-Leg Glute Bridge', equip: 'none', cat: 'legs', muscles: 'glutes, hamstrings',
    setup: 'Glute bridge position with one leg extended straight.', execution: 'Drive through the planted heel to lift the hips, keeping the pelvis level.', mistake: 'Hips tilting toward the free leg — keep them square.', swap: 'glute-bridge', video: 'https://www.youtube.com/watch?v=VUl8R0kn6v4' },
  { id: 'step-up', name: 'Step-Up', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Stand facing a sturdy step or bench around knee height.', execution: 'Step up driving through the top heel, stand tall, then lower under control.', mistake: 'Pushing off the bottom leg — make the top leg do the work.', swap: 'reverse-lunge', video: 'https://www.youtube.com/watch?v=vOiHvzj5XhA' },
  { id: 'wall-sit', name: 'Wall Sit', equip: 'none', cat: 'legs', muscles: 'quads',
    setup: 'Back flat against a wall, feet out in front.', execution: 'Slide down until thighs are parallel and hold, knees at 90°.', mistake: 'Hands on thighs — keep them off; the legs hold the load.', swap: 'bw-squat', video: 'https://www.youtube.com/watch?v=JaZNYM3zAP0' },
  { id: 'calf-raise', name: 'Calf Raise', equip: 'none', cat: 'legs', muscles: 'calves',
    setup: 'Stand on the edge of a step (or flat floor), balls of feet planted.', execution: 'Rise as high as possible on your toes, pause, then lower slowly to a full stretch.', mistake: 'Bouncing — pause at the top and control the descent.', swap: 'bw-squat', video: 'https://www.youtube.com/watch?v=KRJIKsY02nE' },
  { id: 'burpee', name: 'Burpee', equip: 'none', cat: 'conditioning', muscles: 'full body',
    setup: 'Stand tall, feet shoulder-width.', execution: 'Squat down, kick feet back to a plank, (optional push-up), hop feet in, and jump up.', mistake: 'Letting the hips sag in the plank phase — keep the core braced.', swap: 'mountain-climber', video: 'https://www.youtube.com/watch?v=G2hv_NYhM-A' },

  // ── Bodyweight — pull ──
  { id: 'towel-row', name: 'Towel Row (self-resisted)', equip: 'none', cat: 'pull', muscles: 'back, biceps',
    setup: 'Hold a towel at both ends in front of you, arms extended, sink into a slight squat and brace.', execution: 'Pull one end toward your chest while resisting hard with the other hand, squeezing the shoulder blade, then slowly let it return. Alternate sides.', mistake: 'No tension — the resisting hand must fight the whole way so the back actually works.', swap: 'superman', video: null },
  { id: 'table-row', name: 'Table / Doorframe Row', equip: 'none', cat: 'pull', muscles: 'back, biceps',
    setup: 'Lie under a sturdy table gripping its edge, or hold both sides of a doorframe leaning back.', execution: 'Pull your chest to your hands keeping the body in one line, then lower under control.', mistake: 'Hips sagging — brace like a plank throughout.', swap: 'superman', video: 'https://www.youtube.com/watch?v=dnpDUwqMX04' },
  { id: 'superman', name: 'Superman', equip: 'none', cat: 'pull', muscles: 'lower back, glutes',
    setup: 'Lie face down, arms extended overhead.', execution: 'Lift arms, chest, and legs off the floor together, pause, and lower slowly.', mistake: 'Yanking the neck up — keep your gaze at the floor.', swap: 'bird-dog', video: 'https://www.youtube.com/watch?v=6L2jJ029gBo' },

  // ── Bodyweight — core / abs ──
  { id: 'plank', name: 'Plank', equip: 'none', cat: 'abs', muscles: 'core',
    setup: 'Forearms on the floor, elbows under shoulders, body in one straight line.', execution: 'Hold, squeezing glutes and bracing abs as if about to be poked in the stomach.', mistake: 'Hips too high or sagging — a friend/mirror check keeps the line honest.', swap: 'knee-pushup', video: 'https://www.youtube.com/watch?v=mwlp75MS6Rg' },
  { id: 'side-plank', name: 'Side Plank', equip: 'none', cat: 'abs', muscles: 'obliques',
    setup: 'On your side, forearm under shoulder, feet stacked (or knees down to scale).', execution: 'Lift hips so the body forms a straight line, and hold. Switch sides.', mistake: 'Hips dropping — push the floor away and stay tall through the shoulder.', swap: 'plank', video: 'https://www.youtube.com/watch?v=iNbH7_edNI8' },
  { id: 'dead-bug', name: 'Dead Bug', equip: 'none', cat: 'abs', muscles: 'deep core',
    setup: 'Lie on your back, arms up, knees bent 90° over hips, lower back pressed into the floor.', execution: 'Slowly lower opposite arm and leg toward the floor, return, and alternate.', mistake: 'Lower back arching off the floor — shrink the range until it stays glued down.', swap: 'plank', video: 'https://www.youtube.com/watch?v=bxn9FBrt4-A' },
  { id: 'bird-dog', name: 'Bird Dog', equip: 'none', cat: 'abs', muscles: 'core, lower back',
    setup: 'On all fours, hands under shoulders, knees under hips.', execution: 'Extend opposite arm and leg until parallel with the floor, pause, return, alternate.', mistake: 'Twisting the hips — imagine balancing a cup of water on your lower back.', swap: 'dead-bug', video: 'https://www.youtube.com/watch?v=ZdAHe9_HeEw' },
  { id: 'crunch', name: 'Crunch', equip: 'none', cat: 'abs', muscles: 'upper abs',
    setup: 'Lie on your back, knees bent, fingertips lightly at temples.', execution: 'Curl shoulder blades off the floor by contracting the abs, pause, lower slowly.', mistake: 'Pulling on the neck — the hands never do the lifting.', swap: 'dead-bug', video: 'https://www.youtube.com/watch?v=0t4t3IpiEao' },
  { id: 'reverse-crunch', name: 'Reverse Crunch', equip: 'none', cat: 'abs', muscles: 'lower abs',
    setup: 'Lie on your back, knees bent 90°, hands at your sides.', execution: 'Curl knees toward your chest lifting the hips off the floor, then lower slowly without arching.', mistake: 'Swinging the legs for momentum — slow curl up, slower down.', swap: 'crunch', video: 'https://www.youtube.com/watch?v=yH-oSzE5_g0' },
  { id: 'bicycle-crunch', name: 'Bicycle Crunch', equip: 'none', cat: 'abs', muscles: 'abs, obliques',
    setup: 'Lie on your back, hands at temples, legs lifted with knees bent.', execution: 'Bring opposite elbow toward opposite knee while extending the other leg, alternating in a slow pedal.', mistake: 'Racing through reps — slow rotation beats fast flailing.', swap: 'crunch', video: 'https://www.youtube.com/watch?v=wpRI3xBhJmo' },
  { id: 'lying-leg-raise', name: 'Lying Leg Raise', equip: 'none', cat: 'abs', muscles: 'lower abs, hip flexors',
    setup: 'Lie flat, legs straight, hands under hips for support.', execution: 'Raise legs to vertical keeping them straight, then lower slowly without letting the lower back arch.', mistake: 'Lower back popping off the floor — bend the knees slightly or shorten the range.', swap: 'reverse-crunch', video: 'https://www.youtube.com/watch?v=0tzBVqiDwSs' },
  { id: 'hollow-hold', name: 'Hollow Hold', equip: 'none', cat: 'abs', muscles: 'entire core',
    setup: 'Lie on your back, press the lower back into the floor.', execution: 'Lift shoulders and legs slightly off the floor, arms overhead, and hold the "banana" shape.', mistake: 'Lower back lifting — tuck knees or raise the legs higher to scale.', swap: 'dead-bug', video: 'https://www.youtube.com/watch?v=hf00_b2sRdc' },
  { id: 'mountain-climber', name: 'Mountain Climber', equip: 'none', cat: 'abs', muscles: 'core, shoulders',
    setup: 'High plank, shoulders over wrists.', execution: 'Drive knees toward the chest one at a time at a controlled pace, hips level.', mistake: 'Butt rising into a pike — keep the plank line as the legs move.', swap: 'plank', video: 'https://www.youtube.com/watch?v=ZhiCSdOVJp0' },
  { id: 'russian-twist', name: 'Russian Twist', equip: 'none', cat: 'abs', muscles: 'obliques',
    setup: 'Seated, knees bent, heels lightly down (or lifted to advance), torso leaned back ~45°.', execution: 'Rotate the torso side to side, touching the floor beside your hip each side.', mistake: 'Just swinging the arms — rotate the ribcage, chest follows the hands.', swap: 'bicycle-crunch', video: 'https://www.youtube.com/watch?v=IJDOoVyVjhc' },

  // ── Minimal kit (kettlebell · push-up handles · ab wheel · mat) ──
  { id: 'kb-deadlift', name: 'Kettlebell Deadlift', equip: 'min', cat: 'legs', muscles: 'hamstrings, glutes, back',
    setup: 'Kettlebell on the floor between your feet, feet hip-width, soft knees, chest proud.', execution: 'Hinge at the hips to grip the bell, then drive the hips forward to stand tall, squeezing the glutes. Lower under control. This is the ONLY floor deadlift Abs By AI programs.', mistake: 'Rounding the back to reach the bell — hinge the hips and keep the spine long.', swap: 'single-leg-glute-bridge', video: null },
  { id: 'kb-swing', name: 'Kettlebell Swing', equip: 'min', cat: 'conditioning', muscles: 'glutes, hamstrings, core',
    setup: 'Kettlebell a foot in front of you, feet wide, hinge and grip it with both hands.', execution: 'Hike the bell back between your legs, then snap the hips forward to float it to chest height — the power is all hips, the arms are ropes.', mistake: 'Squatting and lifting with the arms — it is a hip hinge, not a front raise.', swap: 'glute-bridge', video: null },
  { id: 'kb-goblet-squat', name: 'Kettlebell Goblet Squat', equip: 'min', cat: 'legs', muscles: 'quads, glutes, core',
    setup: 'Hold the kettlebell by the horns against your chest, elbows tucked, feet shoulder-width (or wide/sumo for a glute bias).', execution: 'Squat between your knees keeping the torso tall and elbows inside the knees, then drive up.', mistake: 'Letting the bell pull you forward — keep it glued to the chest.', swap: 'bw-squat', video: null },
  { id: 'kb-row', name: 'Kettlebell Row', equip: 'min', cat: 'pull', muscles: 'lats, upper back, biceps',
    setup: 'Hinge forward with a flat back, kettlebell hanging in one hand, other hand on your thigh for support.', execution: 'Row the bell to your hip, driving the elbow back and squeezing the shoulder blade, then lower. Finish the set, then switch.', mistake: 'Twisting the torso to heave the bell — shoulders stay square to the floor.', swap: 'towel-row', video: null },
  { id: 'kb-press', name: 'Kettlebell Overhead Press', equip: 'min', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'Kettlebell racked at one shoulder, bell resting on the back of the forearm, feet hip-width, glutes and abs braced.', execution: 'Press the bell overhead until the arm is straight, then lower to the rack under control. Finish the set, then switch.', mistake: 'Arching the lower back to press — squeeze the glutes and keep the ribs down.', swap: 'pike-pushup', video: null },
  { id: 'deficit-pushup', name: 'Deep Push-Up (on handles)', equip: 'min', cat: 'push', muscles: 'chest, triceps, shoulders',
    setup: 'Grip a push-up handle in each hand, shoulder-width, body in one straight line.', execution: 'Lower your chest below the level of the handles for a deep stretch, elbows ~45°, then press back up.', mistake: 'Sagging hips as you reach depth — squeeze glutes and brace abs the whole set.', swap: 'pushup', video: null },

  // ── Dumbbell (full equipment in v3) ──
  { id: 'db-goblet-squat', name: 'Goblet Squat', equip: 'full', cat: 'legs', muscles: 'quads, glutes, core',
    setup: 'Hold one dumbbell vertically against your chest, elbows tucked, feet shoulder-width.', execution: 'Squat between your knees keeping the torso tall, elbows tracking inside the knees, then stand.', mistake: 'Letting the weight pull you forward — keep it glued to the chest.', swap: 'bw-squat', video: 'https://www.youtube.com/watch?v=-utXQMqTuVA' },
  { id: 'db-rdl', name: 'Dumbbell Hip Hinge', equip: 'full', cat: 'legs', muscles: 'hamstrings, glutes',
    setup: 'Dumbbells in front of thighs, feet hip-width, soft knees.', execution: 'Hinge at the hips pushing them back, sliding the weights down the legs until you feel a hamstring stretch, then squeeze glutes to stand.', mistake: 'Rounding the back — chest proud, weights close to the legs.', swap: 'glute-bridge', video: 'https://www.youtube.com/watch?v=aa57T45iFSE' },
  { id: 'db-lunge', name: 'Dumbbell Lunge', equip: 'full', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Dumbbell in each hand at your sides, standing tall.', execution: 'Step forward (or back) into a lunge until both knees hit ~90°, then drive back up.', mistake: 'Torso collapsing forward — the weights hang, the torso stays tall.', swap: 'reverse-lunge', video: 'https://www.youtube.com/watch?v=G4gAK8Bhyro' },
  { id: 'db-step-up', name: 'Dumbbell Step-Up', equip: 'full', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Dumbbells at sides, facing a knee-height step or bench.', execution: 'Drive through the top heel to step up, stand fully tall, lower under control.', mistake: 'Bouncing off the back leg — strict, top-leg-only reps.', swap: 'step-up', video: 'https://www.youtube.com/watch?v=9ZknEYboBOQ' },
  { id: 'db-floor-press', name: 'Dumbbell Floor Press', equip: 'full', cat: 'push', muscles: 'chest, triceps',
    setup: 'Lie on the floor, knees bent, dumbbells pressed over the chest.', execution: 'Lower until the upper arms touch the floor, pause briefly, press back up.', mistake: 'Flaring elbows to 90° — keep them ~45° from the torso.', swap: 'pushup', video: 'https://www.youtube.com/watch?v=vagdk94bFn4' },
  { id: 'db-bench-press', name: 'Dumbbell Bench Press', equip: 'full', cat: 'push', muscles: 'chest, triceps, shoulders',
    setup: 'Lie on a bench, dumbbells over the chest, feet planted.', execution: 'Lower the weights to chest level with elbows ~45°, then press up and slightly together.', mistake: 'Bouncing out of the bottom — control down, drive up.', swap: 'db-floor-press', video: 'https://www.youtube.com/watch?v=xhEhjF5ozuY' },
  { id: 'db-shoulder-press', name: 'Dumbbell Shoulder Press', equip: 'full', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'Seated or standing tall, dumbbells at shoulder height, palms forward.', execution: 'Press overhead until arms are straight (biceps by ears), lower to shoulders under control.', mistake: 'Arching the lower back — squeeze glutes and ribs down.', swap: 'pike-pushup', video: 'https://www.youtube.com/watch?v=qEwKCR5JCog' },
  { id: 'db-lateral-raise', name: 'Lateral Raise', equip: 'full', cat: 'push', muscles: 'side delts',
    setup: 'Stand tall, light dumbbells at your sides, slight elbow bend.', execution: 'Raise the weights out to shoulder height like pouring two jugs, then lower slowly.', mistake: 'Swinging heavy weight up — lighter, slower, no shrug.', swap: 'pike-pushup', video: 'https://www.youtube.com/watch?v=nnH63icHYXY' },
  { id: 'db-row', name: 'One-Arm Dumbbell Row', equip: 'full', cat: 'pull', muscles: 'lats, upper back, biceps',
    setup: 'One hand and knee on a bench (or hand on a chair), flat back, dumbbell hanging in the other hand.', execution: 'Pull the weight to your hip, driving the elbow back and squeezing the shoulder blade, then lower.', mistake: 'Twisting the torso to heave the weight — shoulders stay square to the floor.', swap: 'table-row', video: 'https://www.youtube.com/watch?v=pYcpY20QaE8' },
  { id: 'db-renegade-row', name: 'Renegade Row', equip: 'full', cat: 'pull', muscles: 'back, core',
    setup: 'High plank with hands on dumbbells, feet wide.', execution: 'Row one dumbbell to the hip without rotating the hips, lower, alternate.', mistake: 'Hips swinging side to side — imagine headlights on your hips pointing at the floor.', swap: 'db-row', video: 'https://www.youtube.com/watch?v=NTl_ALR8Tlc' },
  { id: 'db-pullover', name: 'Dumbbell Pullover', equip: 'full', cat: 'pull', muscles: 'lats, chest',
    setup: 'Lie on a bench (or floor), one dumbbell held with both hands above the chest.', execution: 'Lower the weight in an arc behind your head until you feel a lat stretch, then pull back over the chest.', mistake: 'Bending the elbows more as you lower — keep the arm angle fixed.', swap: 'db-row', video: 'https://www.youtube.com/watch?v=tcHaHIQStsk' },
  { id: 'db-curl', name: 'Dumbbell Curl', equip: 'full', cat: 'pull', muscles: 'biceps',
    setup: 'Stand tall, dumbbells at sides, palms forward.', execution: 'Curl the weights to shoulder height keeping elbows pinned to your sides, lower slowly.', mistake: 'Swinging the hips to lift — if you must swing, the weight is too heavy.', swap: 'db-hammer-curl', video: 'https://www.youtube.com/watch?v=XE_pHwbst04' },
  { id: 'db-hammer-curl', name: 'Hammer Curl', equip: 'full', cat: 'pull', muscles: 'biceps, forearms',
    setup: 'Stand tall, dumbbells at sides, palms facing each other.', execution: 'Curl with a neutral grip, elbows pinned, lower under control.', mistake: 'Elbows drifting forward — they stay at your sides.', swap: 'db-curl', video: 'https://www.youtube.com/watch?v=zC3nLlEvin4' },
  { id: 'db-fly', name: 'Dumbbell Fly', equip: 'full', cat: 'push', muscles: 'chest',
    setup: 'Lie on a bench (or the floor), dumbbells pressed over the chest, palms facing each other, slight elbow bend.', execution: 'Open the arms in a wide arc until you feel a chest stretch, then squeeze the weights back together like hugging a tree.', mistake: 'Bending the elbows more as you lower — keep the arm angle fixed; it is a hug, not a press.', swap: 'db-floor-press', video: null },
  { id: 'chest-supported-db-row', name: 'Chest-Supported Dumbbell Row', equip: 'full', cat: 'pull', muscles: 'mid-back, lats, biceps',
    setup: 'Lie chest-down on an incline bench (or hinge with your chest braced), dumbbells hanging straight down.', execution: 'Row both weights to your hips, squeezing the shoulder blades together, then lower with control.', mistake: 'Lifting the chest off the pad to heave — the bench takes the momentum away; keep it there.', swap: 'db-row', video: null },
  { id: 'db-rear-delt-fly', name: 'Bent-Over Dumbbell Rear Delt Fly', equip: 'full', cat: 'pull', muscles: 'rear delts, upper back',
    setup: 'Hinge forward with a flat back, light dumbbells hanging under the shoulders, slight elbow bend.', execution: 'Raise the weights out to the sides like spreading wings, squeeze the rear shoulders, lower slowly.', mistake: 'Swinging heavy weight with the torso — go light and strict; the rear delts are small.', swap: 'superman', video: null },
  { id: 'db-tricep-extension', name: 'Overhead Triceps Extension', equip: 'full', cat: 'push', muscles: 'triceps',
    setup: 'Hold one dumbbell with both hands overhead, elbows pointing forward.', execution: 'Lower the weight behind your head by bending the elbows, then extend back to straight.', mistake: 'Elbows flaring wide — keep them narrow and pointed up.', swap: 'chair-dip', video: 'https://www.youtube.com/watch?v=DZgpCf5alfI' },
  { id: 'db-kickback', name: 'Triceps Kickback', equip: 'full', cat: 'push', muscles: 'triceps',
    setup: 'Hinge forward with a flat back, upper arms pinned parallel to the floor.', execution: 'Extend the forearms straight back until arms are fully straight, squeeze, return.', mistake: 'Dropping the upper arm — only the forearm moves.', swap: 'chair-dip', video: 'https://www.youtube.com/watch?v=6SS6K3lAwZ8' },
  { id: 'db-shrug', name: 'Dumbbell Shrug', equip: 'full', cat: 'pull', muscles: 'traps',
    setup: 'Stand tall, heavy-ish dumbbells at your sides.', execution: 'Shrug shoulders straight up toward your ears, pause, lower slowly.', mistake: 'Rolling the shoulders in circles — straight up and down only.', swap: 'db-row', video: 'https://www.youtube.com/watch?v=cJRVVxmytaM' },
  { id: 'db-thruster', name: 'Dumbbell Thruster', equip: 'full', cat: 'conditioning', muscles: 'full body',
    setup: 'Dumbbells at shoulders, feet shoulder-width.', execution: 'Squat to parallel, then drive up and press the weights overhead in one motion.', mistake: 'Splitting it into a slow squat then press — it is one fluid drive.', swap: 'db-goblet-squat', video: 'https://www.youtube.com/watch?v=eDNt3biU9I4' },
  { id: 'db-swing', name: 'Dumbbell Swing', equip: 'full', cat: 'conditioning', muscles: 'glutes, hamstrings, core',
    setup: 'Hold one dumbbell by the head with both hands, feet wide.', execution: 'Hinge and hike the weight back between your legs, then snap the hips forward to swing it to chest height.', mistake: 'Squatting and lifting with the arms — it is a hip hinge; the arms are ropes.', swap: 'kb-swing', video: 'https://www.youtube.com/watch?v=Y30kFfgW-bY' },
  { id: 'db-farmer-carry', name: 'Farmer Carry', equip: 'full', cat: 'conditioning', muscles: 'grip, traps, core',
    setup: 'Heavy dumbbell in each hand, stand tall.', execution: 'Walk with short quick steps, shoulders back, core braced, for the given distance or time.', mistake: 'Leaning to one side — walk as if balancing a book on your head.', swap: 'plank', video: 'https://www.youtube.com/watch?v=62v48abT5-Y' },
  { id: 'db-russian-twist', name: 'Weighted Russian Twist', equip: 'full', cat: 'abs', muscles: 'obliques',
    setup: 'Seated, lean back ~45°, hold one dumbbell at your chest, heels light on the floor.', execution: 'Rotate the torso side to side, moving the weight across your body under control.', mistake: 'Arms swinging while the torso stays still — the ribcage rotates.', swap: 'russian-twist', video: 'https://www.youtube.com/watch?v=p_dPOhhgovg' },
  { id: 'db-crunch', name: 'Weighted Crunch', equip: 'full', cat: 'abs', muscles: 'upper abs',
    setup: 'Lie on your back, knees bent, dumbbell held on the chest.', execution: 'Curl shoulder blades off the floor, pause hard at the top, lower slowly.', mistake: 'Sitting all the way up — a crunch is a short, intense range.', swap: 'crunch', video: 'https://www.youtube.com/watch?v=_nzyLUvtgvs' },

  // ── Gym ──
  { id: 'bb-hip-thrust', name: 'Barbell Hip Thrust', equip: 'full', cat: 'legs', muscles: 'glutes',
    setup: 'Upper back on a bench, bar (padded) over the hips, feet flat.', execution: 'Drive hips up until the torso is level, chin tucked, squeeze glutes hard at the top.', mistake: 'Overarching at the top — finish with glutes, ribs stay down.', swap: 'single-leg-glute-bridge', video: 'https://www.youtube.com/watch?v=pF17m_CXfL0' },
  { id: 'safety-bar-squat', name: 'Safety-Bar Back Squat', equip: 'full', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Safety-bar racked on the upper back, handles forward, feet shoulder-width in the rack. Stages 6–7 only — the backup to the leg press.', execution: 'Brace, sit hips back and down to at least parallel keeping the chest up, then drive up through mid-foot.', mistake: 'Chest collapsing forward — the padded yoke wants to fold you; fight to stay upright.', swap: 'leg-press', video: null },
  { id: 'bb-back-squat', name: 'Barbell Back Squat', equip: 'full', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Bar on the upper back in a rack, feet shoulder-width. Stages 6–7 only — the tertiary squat, after leg press and safety-bar.', execution: 'Brace hard, sit down and back to at least parallel, then drive up keeping the bar over mid-foot.', mistake: 'Knees caving or heels lifting — push the knees out and keep the whole foot planted.', swap: 'safety-bar-squat', video: null },
  { id: 'cable-glute-kickback', name: 'Cable Glute Kickback', equip: 'full', cat: 'legs', muscles: 'glutes',
    setup: 'Ankle strap on a low cable, face the machine holding it for balance, slight hinge.', execution: 'Drive one leg straight back squeezing the glute at the top, then return under control. Finish the set, then switch.', mistake: 'Arching the lower back to swing the leg higher — the glute does the work, not the spine.', swap: 'single-leg-glute-bridge', video: null },
  { id: 'hip-abduction', name: 'Hip Abduction', equip: 'full', cat: 'legs', muscles: 'glute medius',
    setup: 'Seated hip-abduction machine, pads against the outer thighs (or a band around the knees).', execution: 'Press the knees outward against the resistance, squeeze at the widest point, then return slowly.', mistake: 'Leaning back to force the weight — sit tall and let the glutes push.', swap: 'glute-bridge', video: null },
  { id: 'sled-push', name: 'Prowler Sled Push', equip: 'full', cat: 'conditioning', muscles: 'quads, glutes, full body',
    setup: 'Load the sled, grip the high or low posts, arms long, torso leaning in. Functional work, Stages 5–7.', execution: 'Drive it forward with powerful, choppy steps for the given distance, staying low and braced.', mistake: 'Standing too upright — lean into it and push through the balls of the feet.', swap: 'walking-lunge', video: null },
  { id: 'battle-ropes', name: 'Battle Ropes', equip: 'full', cat: 'conditioning', muscles: 'shoulders, arms, core',
    setup: 'A rope end in each hand, feet shoulder-width, soft knees, athletic stance. Functional conditioning, Stages 5–7.', execution: 'Drive alternating waves down the ropes as fast as you can hold for the interval, bracing the core throughout.', mistake: 'Going all-arms and gassing out — use a little hip bounce and keep the whole body in it.', swap: 'mountain-climber', video: null },
  { id: 'leg-press', name: 'Leg Press', equip: 'full', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Feet shoulder-width on the platform, back and hips flat against the pads.', execution: 'Lower under control until knees near 90°, then press without locking the knees hard.', mistake: 'Letting the hips curl off the pad at the bottom — shorten the range.', swap: 'db-goblet-squat', video: 'https://www.youtube.com/watch?v=8nm863C0c60' },
  { id: 'leg-extension', name: 'Leg Extension', equip: 'full', cat: 'legs', muscles: 'quads',
    setup: 'Sit with the pad on your lower shins, knees lined up with the machine pivot.', execution: 'Extend to straight, squeeze the quads for a beat, lower slowly.', mistake: 'Kicking the weight up fast — slow squeeze, slower lower.', swap: 'wall-sit', video: 'https://www.youtube.com/watch?v=F1JfmctnmTE' },
  { id: 'leg-curl', name: 'Leg Curl', equip: 'full', cat: 'legs', muscles: 'hamstrings',
    setup: 'Position the pad just above the heels (lying or seated machine).', execution: 'Curl the heels toward the glutes, pause, and return slowly.', mistake: 'Hips lifting off the pad — keep them pinned.', swap: 'kb-deadlift', video: 'https://www.youtube.com/watch?v=lUH80pneL5w' },
  { id: 'machine-chest-press', name: 'Machine Chest Press', equip: 'full', cat: 'push', muscles: 'chest, triceps',
    setup: 'Adjust the seat so handles line up with mid-chest.', execution: 'Press to full extension without slamming the stack, return under control.', mistake: 'Shoulders rolling forward — keep the chest proud and shoulder blades back.', swap: 'db-floor-press', video: 'https://www.youtube.com/watch?v=pLofEAcfsO8' },
  { id: 'cable-fly', name: 'Cable Fly / Crossover', equip: 'full', cat: 'push', muscles: 'chest',
    setup: 'Set both cable pulleys at chest height (or high for a downward sweep), grab a handle in each hand and step forward into a staggered stance.', execution: 'With a slight elbow bend, sweep the handles together in front of your chest, squeeze for a beat, and return under control.', mistake: 'Turning it into a press by bending the elbows — the arms stay long; the chest does the hugging.', swap: 'db-fly', video: null },
  { id: 'pec-deck', name: 'Pec Deck Machine Fly', equip: 'full', cat: 'push', muscles: 'chest',
    setup: 'Sit tall with your back against the pad, handles at chest height, slight bend in the elbows.', execution: 'Bring the handles together in front of your chest, squeeze, and open back until you feel a comfortable stretch.', mistake: 'Slamming the weight together — pause and squeeze at the middle instead.', swap: 'cable-fly', video: null },
  { id: 'bb-ohp', name: 'Barbell Overhead Press', equip: 'full', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'Bar at collarbone height, grip just outside shoulders, glutes and abs braced.', execution: 'Press the bar overhead moving the head slightly back then through, lockout over mid-foot.', mistake: 'Leaning way back to press — squeeze glutes; it is a press, not an incline bench.', swap: 'db-shoulder-press', video: 'https://www.youtube.com/watch?v=a81SaIpjGlA' },
  { id: 'pullup', name: 'Pull-Up', equip: 'full', cat: 'pull', muscles: 'lats, biceps',
    setup: 'Hang from a bar with an overhand grip just outside shoulders.', execution: 'Pull your chin over the bar driving elbows down, lower to a full hang.', mistake: 'Kipping half reps — full hang to chin-over, every rep.', swap: 'lat-pulldown', video: 'https://www.youtube.com/watch?v=sIvJTfGxdFo' },
  { id: 'chinup', name: 'Chin-Up', equip: 'full', cat: 'pull', muscles: 'lats, biceps',
    setup: 'Hang with an underhand, shoulder-width grip.', execution: 'Pull chin over the bar, lower to a full hang with control.', mistake: 'Shrugging into the ears at the top — pull the shoulder blades down.', swap: 'lat-pulldown', video: 'https://www.youtube.com/watch?v=e1YSApl-QcM' },
  { id: 'lat-pulldown', name: 'Lat Pulldown', equip: 'full', cat: 'pull', muscles: 'lats, biceps',
    setup: 'Grip the bar wider than shoulders, thighs snug under the pads.', execution: 'Pull the bar to the top of the chest driving elbows down, return with a full stretch.', mistake: 'Leaning way back and heaving — slight lean, strict pull.', swap: 'table-row', video: 'https://www.youtube.com/watch?v=AOpi-p0cJkc' },
  { id: 'seated-cable-row', name: 'Seated Cable Row', equip: 'full', cat: 'pull', muscles: 'mid-back, lats, biceps',
    setup: 'Sit tall, feet on the platform, slight knee bend, neutral grip.', execution: 'Pull the handle to your stomach squeezing the shoulder blades together, return with a full reach.', mistake: 'Rocking the torso back and forth — the arms and back row, the torso stays tall.', swap: 'db-row', video: 'https://www.youtube.com/watch?v=EU7bOadUsNI' },
  { id: 'machine-row', name: 'Machine Row', equip: 'full', cat: 'pull', muscles: 'mid-back, lats, biceps',
    setup: 'Adjust the seat so the handles line up with your mid-chest, chest against the pad if there is one.', execution: 'Pull the handles to your torso driving the elbows back, squeeze the shoulder blades, and return with a full stretch.', mistake: 'Shrugging the shoulders up as you pull — pull the elbows back and down.', swap: 'seated-cable-row', video: null },
  { id: 'straight-arm-pulldown', name: 'Straight-Arm Cable Pulldown', equip: 'full', cat: 'pull', muscles: 'lats',
    setup: 'Stand facing a high cable with a bar or rope, arms extended, slight hinge at the hips.', execution: 'Keeping the arms nearly straight, sweep the bar down to your thighs with the lats, then let it rise slowly to a full stretch.', mistake: 'Bending the elbows and turning it into a pushdown — the arms stay long; the lats pull.', swap: 'lat-pulldown', video: null },
  { id: 'back-extension', name: '45° Back Extension', equip: 'full', cat: 'pull', muscles: 'lower back, glutes, hamstrings',
    setup: 'Set the pad at hip-crease height on the 45° bench, ankles locked in, arms crossed on your chest.', execution: 'Hinge down with a flat back, then squeeze the glutes to raise your torso until your body forms a straight line — no higher.', mistake: 'Hyperextending past straight at the top — finish in line with the legs, not arched.', swap: 'superman', video: null },
  { id: 'machine-rear-delt-fly', name: 'Reverse Pec Deck (Rear Delt Fly)', equip: 'full', cat: 'pull', muscles: 'rear delts, upper back',
    setup: 'Sit facing the pec deck pad with the handles set behind the machine, arms forward at shoulder height.', execution: 'Sweep the handles back and out until your arms are in line with your shoulders, squeeze the rear delts, return slowly.', mistake: 'Rocking backward to move more weight — stay glued to the pad and go lighter.', swap: 'db-rear-delt-fly', video: null },
  { id: 'bb-row', name: 'Barbell Row', equip: 'full', cat: 'pull', muscles: 'lats, mid-back',
    setup: 'Hinge to ~45°, flat back, bar hanging at knee height.', execution: 'Row the bar to your lower ribs, squeeze, and lower under control without standing up.', mistake: 'Torso bouncing upright each rep — hold the hinge.', swap: 'db-row', video: 'https://www.youtube.com/watch?v=rqTOAM8WoeM' },
  { id: 'face-pull', name: 'Face Pull', equip: 'full', cat: 'pull', muscles: 'rear delts, upper back',
    setup: 'Rope on a cable set at face height, grab with thumbs toward you.', execution: 'Pull the rope toward your face, spreading the ends beside your ears, squeeze the rear delts.', mistake: 'Turning it into a row to the chest — pull high, elbows flared.', swap: 'superman', video: 'https://www.youtube.com/watch?v=eTCBSFlCJ_s' },
  { id: 'cable-tricep-pushdown', name: 'Cable Triceps Pushdown', equip: 'full', cat: 'push', muscles: 'triceps',
    setup: 'Cable set high with a bar or rope, elbows pinned to your sides.', execution: 'Push down to full extension, squeeze, and let the weight back up slowly.', mistake: 'Elbows drifting forward to press with the shoulders — elbows stay glued to the ribs.', swap: 'db-tricep-extension', video: 'https://www.youtube.com/watch?v=_w-HpW70nSQ' },
  { id: 'ez-bar-curl', name: 'EZ-Bar Curl', equip: 'full', cat: 'pull', muscles: 'biceps',
    setup: 'Grip the EZ bar at the angled sections, elbows at your sides.', execution: 'Curl to shoulder height and lower over ~3 seconds.', mistake: 'Leaning back to swing the bar up — strict, or lighten it.', swap: 'db-curl', video: 'https://www.youtube.com/watch?v=5NsFLGUf0Fo' },
  { id: 'cable-crunch', name: 'Cable Crunch', equip: 'full', cat: 'abs', muscles: 'abs',
    setup: 'Kneel below a high cable holding the rope beside your head.', execution: 'Crunch your ribs toward your hips against the cable, pause, and return under control.', mistake: 'Pulling with the arms or hinging at the hips — the spine flexes, the hips stay still.', swap: 'db-crunch', video: 'https://www.youtube.com/watch?v=809A_MuZ2PY' },
  { id: 'hanging-knee-raise', name: 'Hanging Knee Raise', equip: 'full', cat: 'abs', muscles: 'lower abs, hip flexors',
    setup: 'Hang from a pull-up bar, shoulders active.', execution: 'Curl the knees up toward the chest tilting the pelvis, then lower slowly without swinging.', mistake: 'Swinging into momentum — pause at the bottom of every rep.', swap: 'lying-leg-raise', video: 'https://www.youtube.com/watch?v=l7OroezzX9k' },
  { id: 'ab-wheel-rollout', name: 'Ab Wheel Rollout', equip: 'min', cat: 'abs', muscles: 'entire core',
    setup: 'Kneel holding the wheel under your shoulders.', execution: 'Roll forward keeping the hips tucked and abs braced as far as you can control, then pull back.', mistake: 'Lower back sagging into an arch — shorten the rollout until you can keep the brace.', swap: 'plank', video: 'https://www.youtube.com/watch?v=rqiTPdK1c_I' },
];

// Equipment tiers unlock cumulatively (v3: none ⊂ min ⊂ full).
const EQUIP_TIERS = { none: ['none'], min: ['none', 'min'], full: ['none', 'min', 'full'] };

// Kept in EXERCISE_BY_ID so old stored programs still render, but NEVER offered
// to the model for new selection (v3 safety pass — §5 of the trainer handoff):
//  - db-rdl: a dumbbell deadlift variant; the kettlebell deadlift is the only
//    loaded floor hinge Abs By AI programs.
//  - db-bench-press: a flat dumbbell bench; chest is fly-dominant with pushing
//    only via machine press / floor press / push-ups.
const EXCLUDED_FROM_SELECTION = new Set(['db-rdl', 'db-bench-press']);

function exercisesForEquipment(equipLevel) {
  const allowed = EQUIP_TIERS[equipLevel] || EQUIP_TIERS.none;
  return EXERCISES.filter((e) => allowed.includes(e.equip) && !EXCLUDED_FROM_SELECTION.has(e.id));
}

const EXERCISE_BY_ID = Object.fromEntries(EXERCISES.map((e) => [e.id, e]));

// Works as a Node module (server whitelist) and a browser <script> (UI).
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { EXERCISES, EXERCISE_BY_ID, EQUIP_TIERS, EXCLUDED_FROM_SELECTION, exercisesForEquipment };
} else {
  window.EXERCISES = EXERCISES;
  window.EXERCISE_BY_ID = EXERCISE_BY_ID;
  window.exercisesForEquipment = exercisesForEquipment;
}
