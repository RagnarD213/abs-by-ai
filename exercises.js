// ============================================================
// EXERCISE LIBRARY — the authoritative whitelist for the AI trainer.
// The model SELECTS and SEQUENCES from this list; it never invents moves.
// equip: 'none' (bodyweight) | 'db' (dumbbells) | 'gym' (full gym).
// A user's equipment unlocks tiers cumulatively: gym ⊃ db ⊃ none.
// swap: the pre-baked one-tap substitute (same or lower equipment tier,
// joint-friendlier or simpler variation).
// video: hand-curated YouTube URL (null until curated — UI hides the button).
// Loaded by both server.js (require) and index.html (<script src>).
// ============================================================
const EXERCISES = [
  // ── Warm-up moves (bodyweight) ──
  { id: 'march-in-place', name: 'March in Place', equip: 'none', cat: 'warmup', muscles: 'full body',
    setup: 'Stand tall, arms relaxed.', execution: 'March with high knees at an easy pace, swinging arms naturally.', mistake: 'Slouching — keep the chest up and core lightly braced.', swap: 'jumping-jack', video: null },
  { id: 'jumping-jack', name: 'Jumping Jacks', equip: 'none', cat: 'warmup', muscles: 'full body',
    setup: 'Stand with feet together, arms at sides.', execution: 'Jump feet out while raising arms overhead, then jump back to start. Stay light on the balls of your feet.', mistake: 'Landing flat-footed and heavy — land softly with a slight knee bend.', swap: 'march-in-place', video: null },
  { id: 'arm-circles', name: 'Arm Circles', equip: 'none', cat: 'warmup', muscles: 'shoulders',
    setup: 'Stand tall, arms extended straight out to the sides.', execution: 'Make slow controlled circles, small to large, forward then backward.', mistake: 'Rushing — slow circles warm the shoulder capsule better.', swap: 'cat-cow', video: null },
  { id: 'leg-swings', name: 'Leg Swings', equip: 'none', cat: 'warmup', muscles: 'hips, hamstrings',
    setup: 'Stand beside a wall or chair for balance.', execution: 'Swing one leg forward and back in a smooth arc, gradually increasing range. Then switch legs.', mistake: 'Rounding the lower back to force height — keep the torso upright.', swap: 'hip-circles', video: null },
  { id: 'hip-circles', name: 'Hip Circles', equip: 'none', cat: 'warmup', muscles: 'hips',
    setup: 'Stand with hands on hips, feet shoulder-width.', execution: 'Draw slow, big circles with your hips in both directions.', mistake: 'Tiny fast circles — go slow and wide to open the hips.', swap: 'leg-swings', video: null },
  { id: 'cat-cow', name: 'Cat-Cow', equip: 'none', cat: 'warmup', muscles: 'spine, core',
    setup: 'On all fours, hands under shoulders, knees under hips.', execution: 'Alternate arching your back up (cat) and dipping it down with chest lifted (cow), moving with your breath.', mistake: 'Moving only the neck — the motion should travel through the whole spine.', swap: 'arm-circles', video: null },
  { id: 'inchworm', name: 'Inchworm', equip: 'none', cat: 'warmup', muscles: 'hamstrings, shoulders, core',
    setup: 'Stand tall with feet hip-width.', execution: 'Hinge down, walk your hands out to a plank, pause, then walk them back and stand up.', mistake: 'Bending the knees a lot — keep them softly straight to stretch the hamstrings.', swap: 'worlds-greatest-stretch', video: null },
  { id: 'worlds-greatest-stretch', name: "World's Greatest Stretch", equip: 'none', cat: 'warmup', muscles: 'hips, thoracic spine',
    setup: 'From a plank, step your right foot outside your right hand.', execution: 'Drop the back knee, sink the hips, then rotate the right arm to the ceiling. Switch sides.', mistake: 'Letting the front knee cave inward — keep it tracking over the foot.', swap: 'inchworm', video: null },

  // ── Bodyweight — push ──
  { id: 'pushup', name: 'Push-Up', equip: 'none', cat: 'push', muscles: 'chest, triceps, shoulders',
    setup: 'Plank position, hands slightly wider than shoulders, body in one straight line.', execution: 'Lower your chest to just above the floor with elbows ~45° from your body, then press back up.', mistake: 'Sagging hips — squeeze glutes and brace abs the whole set.', swap: 'incline-pushup', video: null },
  { id: 'incline-pushup', name: 'Incline Push-Up', equip: 'none', cat: 'push', muscles: 'chest, triceps',
    setup: 'Hands on a sturdy elevated surface (bench, counter, sofa arm), body straight.', execution: 'Lower chest to the edge, elbows ~45°, then press away.', mistake: 'Flaring elbows straight out — keep them at ~45°.', swap: 'knee-pushup', video: null },
  { id: 'knee-pushup', name: 'Knee Push-Up', equip: 'none', cat: 'push', muscles: 'chest, triceps',
    setup: 'Push-up position with knees on the floor, hips in line with shoulders and knees.', execution: 'Lower chest toward the floor and press back up without breaking the hip line.', mistake: 'Piking the hips up — keep a straight line from head to knees.', swap: 'incline-pushup', video: null },
  { id: 'pike-pushup', name: 'Pike Push-Up', equip: 'none', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'From push-up position, walk feet in and lift hips high into an inverted V.', execution: 'Bend elbows to lower the top of your head toward the floor, then press back up.', mistake: 'Shifting weight back to the legs — keep shoulders stacked over hands.', swap: 'pushup', video: null },
  { id: 'chair-dip', name: 'Chair Dip', equip: 'none', cat: 'push', muscles: 'triceps, chest',
    setup: 'Hands on the edge of a sturdy chair behind you, legs extended, hips off the seat.', execution: 'Bend elbows straight back to lower your hips, then press up until arms are straight.', mistake: 'Shrugging shoulders toward ears — keep them pulled down.', swap: 'knee-pushup', video: null },

  // ── Bodyweight — legs & hinge ──
  { id: 'bw-squat', name: 'Bodyweight Squat', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Feet shoulder-width, toes slightly out, arms forward for balance.', execution: 'Sit hips back and down until thighs are at least parallel, then drive up through mid-foot.', mistake: 'Knees caving inward — push them out in line with the toes.', swap: 'wall-sit', video: null },
  { id: 'split-squat', name: 'Split Squat', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Long stride stance, back heel up, torso tall.', execution: 'Lower the back knee toward the floor, then drive up through the front foot. Finish the set, then switch.', mistake: 'Front knee drifting far past the toes — keep the shin near vertical.', swap: 'bw-squat', video: null },
  { id: 'walking-lunge', name: 'Walking Lunge', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Stand tall with room to walk forward.', execution: 'Step forward and lower until both knees are ~90°, then push through the front foot into the next step.', mistake: 'Short choppy steps — take a full stride so the front shin stays vertical.', swap: 'split-squat', video: null },
  { id: 'reverse-lunge', name: 'Reverse Lunge', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Stand tall, feet hip-width.', execution: 'Step one foot back and lower the back knee toward the floor, then drive back to standing.', mistake: 'Leaning way forward — keep the torso mostly upright.', swap: 'split-squat', video: null },
  { id: 'glute-bridge', name: 'Glute Bridge', equip: 'none', cat: 'legs', muscles: 'glutes, hamstrings',
    setup: 'Lie on your back, knees bent, feet flat and hip-width.', execution: 'Drive through heels to lift hips until body is straight from shoulders to knees. Squeeze glutes at the top.', mistake: 'Arching the lower back at the top — finish with the glutes, not the spine.', swap: 'bw-squat', video: null },
  { id: 'single-leg-glute-bridge', name: 'Single-Leg Glute Bridge', equip: 'none', cat: 'legs', muscles: 'glutes, hamstrings',
    setup: 'Glute bridge position with one leg extended straight.', execution: 'Drive through the planted heel to lift the hips, keeping the pelvis level.', mistake: 'Hips tilting toward the free leg — keep them square.', swap: 'glute-bridge', video: null },
  { id: 'step-up', name: 'Step-Up', equip: 'none', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Stand facing a sturdy step or bench around knee height.', execution: 'Step up driving through the top heel, stand tall, then lower under control.', mistake: 'Pushing off the bottom leg — make the top leg do the work.', swap: 'reverse-lunge', video: null },
  { id: 'wall-sit', name: 'Wall Sit', equip: 'none', cat: 'legs', muscles: 'quads',
    setup: 'Back flat against a wall, feet out in front.', execution: 'Slide down until thighs are parallel and hold, knees at 90°.', mistake: 'Hands on thighs — keep them off; the legs hold the load.', swap: 'bw-squat', video: null },
  { id: 'calf-raise', name: 'Calf Raise', equip: 'none', cat: 'legs', muscles: 'calves',
    setup: 'Stand on the edge of a step (or flat floor), balls of feet planted.', execution: 'Rise as high as possible on your toes, pause, then lower slowly to a full stretch.', mistake: 'Bouncing — pause at the top and control the descent.', swap: 'bw-squat', video: null },
  { id: 'burpee', name: 'Burpee', equip: 'none', cat: 'conditioning', muscles: 'full body',
    setup: 'Stand tall, feet shoulder-width.', execution: 'Squat down, kick feet back to a plank, (optional push-up), hop feet in, and jump up.', mistake: 'Letting the hips sag in the plank phase — keep the core braced.', swap: 'mountain-climber', video: null },

  // ── Bodyweight — pull ──
  { id: 'table-row', name: 'Table / Doorframe Row', equip: 'none', cat: 'pull', muscles: 'back, biceps',
    setup: 'Lie under a sturdy table gripping its edge, or hold both sides of a doorframe leaning back.', execution: 'Pull your chest to your hands keeping the body in one line, then lower under control.', mistake: 'Hips sagging — brace like a plank throughout.', swap: 'superman', video: null },
  { id: 'superman', name: 'Superman', equip: 'none', cat: 'pull', muscles: 'lower back, glutes',
    setup: 'Lie face down, arms extended overhead.', execution: 'Lift arms, chest, and legs off the floor together, pause, and lower slowly.', mistake: 'Yanking the neck up — keep your gaze at the floor.', swap: 'bird-dog', video: null },

  // ── Bodyweight — core / abs ──
  { id: 'plank', name: 'Plank', equip: 'none', cat: 'abs', muscles: 'core',
    setup: 'Forearms on the floor, elbows under shoulders, body in one straight line.', execution: 'Hold, squeezing glutes and bracing abs as if about to be poked in the stomach.', mistake: 'Hips too high or sagging — a friend/mirror check keeps the line honest.', swap: 'knee-pushup', video: null },
  { id: 'side-plank', name: 'Side Plank', equip: 'none', cat: 'abs', muscles: 'obliques',
    setup: 'On your side, forearm under shoulder, feet stacked (or knees down to scale).', execution: 'Lift hips so the body forms a straight line, and hold. Switch sides.', mistake: 'Hips dropping — push the floor away and stay tall through the shoulder.', swap: 'plank', video: null },
  { id: 'dead-bug', name: 'Dead Bug', equip: 'none', cat: 'abs', muscles: 'deep core',
    setup: 'Lie on your back, arms up, knees bent 90° over hips, lower back pressed into the floor.', execution: 'Slowly lower opposite arm and leg toward the floor, return, and alternate.', mistake: 'Lower back arching off the floor — shrink the range until it stays glued down.', swap: 'plank', video: null },
  { id: 'bird-dog', name: 'Bird Dog', equip: 'none', cat: 'abs', muscles: 'core, lower back',
    setup: 'On all fours, hands under shoulders, knees under hips.', execution: 'Extend opposite arm and leg until parallel with the floor, pause, return, alternate.', mistake: 'Twisting the hips — imagine balancing a cup of water on your lower back.', swap: 'dead-bug', video: null },
  { id: 'crunch', name: 'Crunch', equip: 'none', cat: 'abs', muscles: 'upper abs',
    setup: 'Lie on your back, knees bent, fingertips lightly at temples.', execution: 'Curl shoulder blades off the floor by contracting the abs, pause, lower slowly.', mistake: 'Pulling on the neck — the hands never do the lifting.', swap: 'dead-bug', video: null },
  { id: 'reverse-crunch', name: 'Reverse Crunch', equip: 'none', cat: 'abs', muscles: 'lower abs',
    setup: 'Lie on your back, knees bent 90°, hands at your sides.', execution: 'Curl knees toward your chest lifting the hips off the floor, then lower slowly without arching.', mistake: 'Swinging the legs for momentum — slow curl up, slower down.', swap: 'crunch', video: null },
  { id: 'bicycle-crunch', name: 'Bicycle Crunch', equip: 'none', cat: 'abs', muscles: 'abs, obliques',
    setup: 'Lie on your back, hands at temples, legs lifted with knees bent.', execution: 'Bring opposite elbow toward opposite knee while extending the other leg, alternating in a slow pedal.', mistake: 'Racing through reps — slow rotation beats fast flailing.', swap: 'crunch', video: null },
  { id: 'lying-leg-raise', name: 'Lying Leg Raise', equip: 'none', cat: 'abs', muscles: 'lower abs, hip flexors',
    setup: 'Lie flat, legs straight, hands under hips for support.', execution: 'Raise legs to vertical keeping them straight, then lower slowly without letting the lower back arch.', mistake: 'Lower back popping off the floor — bend the knees slightly or shorten the range.', swap: 'reverse-crunch', video: null },
  { id: 'hollow-hold', name: 'Hollow Hold', equip: 'none', cat: 'abs', muscles: 'entire core',
    setup: 'Lie on your back, press the lower back into the floor.', execution: 'Lift shoulders and legs slightly off the floor, arms overhead, and hold the "banana" shape.', mistake: 'Lower back lifting — tuck knees or raise the legs higher to scale.', swap: 'dead-bug', video: null },
  { id: 'mountain-climber', name: 'Mountain Climber', equip: 'none', cat: 'abs', muscles: 'core, shoulders',
    setup: 'High plank, shoulders over wrists.', execution: 'Drive knees toward the chest one at a time at a controlled pace, hips level.', mistake: 'Butt rising into a pike — keep the plank line as the legs move.', swap: 'plank', video: null },
  { id: 'russian-twist', name: 'Russian Twist', equip: 'none', cat: 'abs', muscles: 'obliques',
    setup: 'Seated, knees bent, heels lightly down (or lifted to advance), torso leaned back ~45°.', execution: 'Rotate the torso side to side, touching the floor beside your hip each side.', mistake: 'Just swinging the arms — rotate the ribcage, chest follows the hands.', swap: 'bicycle-crunch', video: null },

  // ── Dumbbell ──
  { id: 'db-goblet-squat', name: 'Goblet Squat', equip: 'db', cat: 'legs', muscles: 'quads, glutes, core',
    setup: 'Hold one dumbbell vertically against your chest, elbows tucked, feet shoulder-width.', execution: 'Squat between your knees keeping the torso tall, elbows tracking inside the knees, then stand.', mistake: 'Letting the weight pull you forward — keep it glued to the chest.', swap: 'bw-squat', video: null },
  { id: 'db-rdl', name: 'Dumbbell Romanian Deadlift', equip: 'db', cat: 'legs', muscles: 'hamstrings, glutes',
    setup: 'Dumbbells in front of thighs, feet hip-width, soft knees.', execution: 'Hinge at the hips pushing them back, sliding the weights down the legs until you feel a hamstring stretch, then squeeze glutes to stand.', mistake: 'Rounding the back — chest proud, weights close to the legs.', swap: 'glute-bridge', video: null },
  { id: 'db-lunge', name: 'Dumbbell Lunge', equip: 'db', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Dumbbell in each hand at your sides, standing tall.', execution: 'Step forward (or back) into a lunge until both knees hit ~90°, then drive back up.', mistake: 'Torso collapsing forward — the weights hang, the torso stays tall.', swap: 'reverse-lunge', video: null },
  { id: 'db-step-up', name: 'Dumbbell Step-Up', equip: 'db', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Dumbbells at sides, facing a knee-height step or bench.', execution: 'Drive through the top heel to step up, stand fully tall, lower under control.', mistake: 'Bouncing off the back leg — strict, top-leg-only reps.', swap: 'step-up', video: null },
  { id: 'db-floor-press', name: 'Dumbbell Floor Press', equip: 'db', cat: 'push', muscles: 'chest, triceps',
    setup: 'Lie on the floor, knees bent, dumbbells pressed over the chest.', execution: 'Lower until the upper arms touch the floor, pause briefly, press back up.', mistake: 'Flaring elbows to 90° — keep them ~45° from the torso.', swap: 'pushup', video: null },
  { id: 'db-bench-press', name: 'Dumbbell Bench Press', equip: 'db', cat: 'push', muscles: 'chest, triceps, shoulders',
    setup: 'Lie on a bench, dumbbells over the chest, feet planted.', execution: 'Lower the weights to chest level with elbows ~45°, then press up and slightly together.', mistake: 'Bouncing out of the bottom — control down, drive up.', swap: 'db-floor-press', video: null },
  { id: 'db-shoulder-press', name: 'Dumbbell Shoulder Press', equip: 'db', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'Seated or standing tall, dumbbells at shoulder height, palms forward.', execution: 'Press overhead until arms are straight (biceps by ears), lower to shoulders under control.', mistake: 'Arching the lower back — squeeze glutes and ribs down.', swap: 'pike-pushup', video: null },
  { id: 'db-lateral-raise', name: 'Lateral Raise', equip: 'db', cat: 'push', muscles: 'side delts',
    setup: 'Stand tall, light dumbbells at your sides, slight elbow bend.', execution: 'Raise the weights out to shoulder height like pouring two jugs, then lower slowly.', mistake: 'Swinging heavy weight up — lighter, slower, no shrug.', swap: 'pike-pushup', video: null },
  { id: 'db-row', name: 'One-Arm Dumbbell Row', equip: 'db', cat: 'pull', muscles: 'lats, upper back, biceps',
    setup: 'One hand and knee on a bench (or hand on a chair), flat back, dumbbell hanging in the other hand.', execution: 'Pull the weight to your hip, driving the elbow back and squeezing the shoulder blade, then lower.', mistake: 'Twisting the torso to heave the weight — shoulders stay square to the floor.', swap: 'table-row', video: null },
  { id: 'db-renegade-row', name: 'Renegade Row', equip: 'db', cat: 'pull', muscles: 'back, core',
    setup: 'High plank with hands on dumbbells, feet wide.', execution: 'Row one dumbbell to the hip without rotating the hips, lower, alternate.', mistake: 'Hips swinging side to side — imagine headlights on your hips pointing at the floor.', swap: 'db-row', video: null },
  { id: 'db-pullover', name: 'Dumbbell Pullover', equip: 'db', cat: 'pull', muscles: 'lats, chest',
    setup: 'Lie on a bench (or floor), one dumbbell held with both hands above the chest.', execution: 'Lower the weight in an arc behind your head until you feel a lat stretch, then pull back over the chest.', mistake: 'Bending the elbows more as you lower — keep the arm angle fixed.', swap: 'db-row', video: null },
  { id: 'db-curl', name: 'Dumbbell Curl', equip: 'db', cat: 'pull', muscles: 'biceps',
    setup: 'Stand tall, dumbbells at sides, palms forward.', execution: 'Curl the weights to shoulder height keeping elbows pinned to your sides, lower slowly.', mistake: 'Swinging the hips to lift — if you must swing, the weight is too heavy.', swap: 'db-hammer-curl', video: null },
  { id: 'db-hammer-curl', name: 'Hammer Curl', equip: 'db', cat: 'pull', muscles: 'biceps, forearms',
    setup: 'Stand tall, dumbbells at sides, palms facing each other.', execution: 'Curl with a neutral grip, elbows pinned, lower under control.', mistake: 'Elbows drifting forward — they stay at your sides.', swap: 'db-curl', video: null },
  { id: 'db-tricep-extension', name: 'Overhead Triceps Extension', equip: 'db', cat: 'push', muscles: 'triceps',
    setup: 'Hold one dumbbell with both hands overhead, elbows pointing forward.', execution: 'Lower the weight behind your head by bending the elbows, then extend back to straight.', mistake: 'Elbows flaring wide — keep them narrow and pointed up.', swap: 'chair-dip', video: null },
  { id: 'db-kickback', name: 'Triceps Kickback', equip: 'db', cat: 'push', muscles: 'triceps',
    setup: 'Hinge forward with a flat back, upper arms pinned parallel to the floor.', execution: 'Extend the forearms straight back until arms are fully straight, squeeze, return.', mistake: 'Dropping the upper arm — only the forearm moves.', swap: 'chair-dip', video: null },
  { id: 'db-shrug', name: 'Dumbbell Shrug', equip: 'db', cat: 'pull', muscles: 'traps',
    setup: 'Stand tall, heavy-ish dumbbells at your sides.', execution: 'Shrug shoulders straight up toward your ears, pause, lower slowly.', mistake: 'Rolling the shoulders in circles — straight up and down only.', swap: 'db-row', video: null },
  { id: 'db-thruster', name: 'Dumbbell Thruster', equip: 'db', cat: 'conditioning', muscles: 'full body',
    setup: 'Dumbbells at shoulders, feet shoulder-width.', execution: 'Squat to parallel, then drive up and press the weights overhead in one motion.', mistake: 'Splitting it into a slow squat then press — it is one fluid drive.', swap: 'db-goblet-squat', video: null },
  { id: 'db-swing', name: 'Dumbbell Swing', equip: 'db', cat: 'conditioning', muscles: 'glutes, hamstrings, core',
    setup: 'Hold one dumbbell by the head with both hands, feet wide.', execution: 'Hinge and hike the weight back between your legs, then snap the hips forward to swing it to chest height.', mistake: 'Squatting and lifting with the arms — it is a hip hinge; the arms are ropes.', swap: 'db-rdl', video: null },
  { id: 'db-farmer-carry', name: 'Farmer Carry', equip: 'db', cat: 'conditioning', muscles: 'grip, traps, core',
    setup: 'Heavy dumbbell in each hand, stand tall.', execution: 'Walk with short quick steps, shoulders back, core braced, for the given distance or time.', mistake: 'Leaning to one side — walk as if balancing a book on your head.', swap: 'plank', video: null },
  { id: 'db-russian-twist', name: 'Weighted Russian Twist', equip: 'db', cat: 'abs', muscles: 'obliques',
    setup: 'Seated, lean back ~45°, hold one dumbbell at your chest, heels light on the floor.', execution: 'Rotate the torso side to side, moving the weight across your body under control.', mistake: 'Arms swinging while the torso stays still — the ribcage rotates.', swap: 'russian-twist', video: null },
  { id: 'db-crunch', name: 'Weighted Crunch', equip: 'db', cat: 'abs', muscles: 'upper abs',
    setup: 'Lie on your back, knees bent, dumbbell held on the chest.', execution: 'Curl shoulder blades off the floor, pause hard at the top, lower slowly.', mistake: 'Sitting all the way up — a crunch is a short, intense range.', swap: 'crunch', video: null },

  // ── Gym ──
  { id: 'bb-back-squat', name: 'Barbell Back Squat', equip: 'gym', cat: 'legs', muscles: 'quads, glutes, core',
    setup: 'Bar on upper traps in a rack, feet shoulder-width, toes slightly out.', execution: 'Brace, sit down until thighs are at least parallel, drive up through mid-foot.', mistake: 'Knees caving on the way up — push them out over the toes.', swap: 'db-goblet-squat', video: null },
  { id: 'bb-deadlift', name: 'Barbell Deadlift', equip: 'gym', cat: 'legs', muscles: 'hamstrings, glutes, back',
    setup: 'Bar over mid-foot, hinge to grip just outside the legs, flat back, shoulders over the bar.', execution: 'Push the floor away and stand tall, bar dragging up the legs; hinge it back down the same path.', mistake: 'Rounding the lower back off the floor — take slack out of the bar and brace first.', swap: 'db-rdl', video: null },
  { id: 'bb-hip-thrust', name: 'Barbell Hip Thrust', equip: 'gym', cat: 'legs', muscles: 'glutes',
    setup: 'Upper back on a bench, bar (padded) over the hips, feet flat.', execution: 'Drive hips up until the torso is level, chin tucked, squeeze glutes hard at the top.', mistake: 'Overarching at the top — finish with glutes, ribs stay down.', swap: 'single-leg-glute-bridge', video: null },
  { id: 'leg-press', name: 'Leg Press', equip: 'gym', cat: 'legs', muscles: 'quads, glutes',
    setup: 'Feet shoulder-width on the platform, back and hips flat against the pads.', execution: 'Lower under control until knees near 90°, then press without locking the knees hard.', mistake: 'Letting the hips curl off the pad at the bottom — shorten the range.', swap: 'db-goblet-squat', video: null },
  { id: 'leg-extension', name: 'Leg Extension', equip: 'gym', cat: 'legs', muscles: 'quads',
    setup: 'Sit with the pad on your lower shins, knees lined up with the machine pivot.', execution: 'Extend to straight, squeeze the quads for a beat, lower slowly.', mistake: 'Kicking the weight up fast — slow squeeze, slower lower.', swap: 'wall-sit', video: null },
  { id: 'leg-curl', name: 'Leg Curl', equip: 'gym', cat: 'legs', muscles: 'hamstrings',
    setup: 'Position the pad just above the heels (lying or seated machine).', execution: 'Curl the heels toward the glutes, pause, and return slowly.', mistake: 'Hips lifting off the pad — keep them pinned.', swap: 'db-rdl', video: null },
  { id: 'bb-bench-press', name: 'Barbell Bench Press', equip: 'gym', cat: 'push', muscles: 'chest, triceps, shoulders',
    setup: 'Lie with eyes under the bar, feet planted, slight arch, grip a bit wider than shoulders.', execution: 'Lower the bar to mid-chest with elbows ~45°, press back to lockout over the shoulders.', mistake: 'Bouncing off the chest — touch and press, no rebound.', swap: 'db-bench-press', video: null },
  { id: 'machine-chest-press', name: 'Machine Chest Press', equip: 'gym', cat: 'push', muscles: 'chest, triceps',
    setup: 'Adjust the seat so handles line up with mid-chest.', execution: 'Press to full extension without slamming the stack, return under control.', mistake: 'Shoulders rolling forward — keep the chest proud and shoulder blades back.', swap: 'db-floor-press', video: null },
  { id: 'bb-ohp', name: 'Barbell Overhead Press', equip: 'gym', cat: 'push', muscles: 'shoulders, triceps',
    setup: 'Bar at collarbone height, grip just outside shoulders, glutes and abs braced.', execution: 'Press the bar overhead moving the head slightly back then through, lockout over mid-foot.', mistake: 'Leaning way back to press — squeeze glutes; it is a press, not an incline bench.', swap: 'db-shoulder-press', video: null },
  { id: 'pullup', name: 'Pull-Up', equip: 'gym', cat: 'pull', muscles: 'lats, biceps',
    setup: 'Hang from a bar with an overhand grip just outside shoulders.', execution: 'Pull your chin over the bar driving elbows down, lower to a full hang.', mistake: 'Kipping half reps — full hang to chin-over, every rep.', swap: 'lat-pulldown', video: null },
  { id: 'chinup', name: 'Chin-Up', equip: 'gym', cat: 'pull', muscles: 'lats, biceps',
    setup: 'Hang with an underhand, shoulder-width grip.', execution: 'Pull chin over the bar, lower to a full hang with control.', mistake: 'Shrugging into the ears at the top — pull the shoulder blades down.', swap: 'lat-pulldown', video: null },
  { id: 'lat-pulldown', name: 'Lat Pulldown', equip: 'gym', cat: 'pull', muscles: 'lats, biceps',
    setup: 'Grip the bar wider than shoulders, thighs snug under the pads.', execution: 'Pull the bar to the top of the chest driving elbows down, return with a full stretch.', mistake: 'Leaning way back and heaving — slight lean, strict pull.', swap: 'table-row', video: null },
  { id: 'seated-cable-row', name: 'Seated Cable Row', equip: 'gym', cat: 'pull', muscles: 'mid-back, lats, biceps',
    setup: 'Sit tall, feet on the platform, slight knee bend, neutral grip.', execution: 'Pull the handle to your stomach squeezing the shoulder blades together, return with a full reach.', mistake: 'Rocking the torso back and forth — the arms and back row, the torso stays tall.', swap: 'db-row', video: null },
  { id: 'bb-row', name: 'Barbell Row', equip: 'gym', cat: 'pull', muscles: 'lats, mid-back',
    setup: 'Hinge to ~45°, flat back, bar hanging at knee height.', execution: 'Row the bar to your lower ribs, squeeze, and lower under control without standing up.', mistake: 'Torso bouncing upright each rep — hold the hinge.', swap: 'db-row', video: null },
  { id: 'face-pull', name: 'Face Pull', equip: 'gym', cat: 'pull', muscles: 'rear delts, upper back',
    setup: 'Rope on a cable set at face height, grab with thumbs toward you.', execution: 'Pull the rope toward your face, spreading the ends beside your ears, squeeze the rear delts.', mistake: 'Turning it into a row to the chest — pull high, elbows flared.', swap: 'superman', video: null },
  { id: 'cable-tricep-pushdown', name: 'Cable Triceps Pushdown', equip: 'gym', cat: 'push', muscles: 'triceps',
    setup: 'Cable set high with a bar or rope, elbows pinned to your sides.', execution: 'Push down to full extension, squeeze, and let the weight back up slowly.', mistake: 'Elbows drifting forward to press with the shoulders — elbows stay glued to the ribs.', swap: 'db-tricep-extension', video: null },
  { id: 'ez-bar-curl', name: 'EZ-Bar Curl', equip: 'gym', cat: 'pull', muscles: 'biceps',
    setup: 'Grip the EZ bar at the angled sections, elbows at your sides.', execution: 'Curl to shoulder height and lower over ~3 seconds.', mistake: 'Leaning back to swing the bar up — strict, or lighten it.', swap: 'db-curl', video: null },
  { id: 'cable-crunch', name: 'Cable Crunch', equip: 'gym', cat: 'abs', muscles: 'abs',
    setup: 'Kneel below a high cable holding the rope beside your head.', execution: 'Crunch your ribs toward your hips against the cable, pause, and return under control.', mistake: 'Pulling with the arms or hinging at the hips — the spine flexes, the hips stay still.', swap: 'db-crunch', video: null },
  { id: 'hanging-knee-raise', name: 'Hanging Knee Raise', equip: 'gym', cat: 'abs', muscles: 'lower abs, hip flexors',
    setup: 'Hang from a pull-up bar, shoulders active.', execution: 'Curl the knees up toward the chest tilting the pelvis, then lower slowly without swinging.', mistake: 'Swinging into momentum — pause at the bottom of every rep.', swap: 'lying-leg-raise', video: null },
  { id: 'ab-wheel-rollout', name: 'Ab Wheel Rollout', equip: 'gym', cat: 'abs', muscles: 'entire core',
    setup: 'Kneel holding the wheel under your shoulders.', execution: 'Roll forward keeping the hips tucked and abs braced as far as you can control, then pull back.', mistake: 'Lower back sagging into an arch — shorten the rollout until you can keep the brace.', swap: 'plank', video: null },
];

// Equipment tiers unlock cumulatively.
const EQUIP_TIERS = { none: ['none'], db: ['none', 'db'], gym: ['none', 'db', 'gym'] };

function exercisesForEquipment(equipLevel) {
  const allowed = EQUIP_TIERS[equipLevel] || EQUIP_TIERS.none;
  return EXERCISES.filter((e) => allowed.includes(e.equip));
}

const EXERCISE_BY_ID = Object.fromEntries(EXERCISES.map((e) => [e.id, e]));

// Works as a Node module (server whitelist) and a browser <script> (UI).
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { EXERCISES, EXERCISE_BY_ID, EQUIP_TIERS, exercisesForEquipment };
} else {
  window.EXERCISES = EXERCISES;
  window.EXERCISE_BY_ID = EXERCISE_BY_ID;
  window.exercisesForEquipment = exercisesForEquipment;
}
