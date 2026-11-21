# Abs By AI — Trainer v3: Every Workout (7 days × 7 stages × women/men)

Companion to [HANDOFF_trainer_v3.md](HANDOFF_trainer_v3.md). This is the full daily programming for Dan to review. **Plan only — do not implement.**

## How to read this
- Each stage lists **7 unique days** for the **women's** track and **7 unique days** for the **men's** track. From **Stage 3 up, no exercise repeats on two consecutive days** (movements alternate, e.g. leg press → walking lunge → leg press).
- **Timed** stages (1–3): each move is worked for the listed seconds with a short rest; run the circuit for the round count shown. **Reps** stages (4–7): sets × reps.
- **Equipment ladder:** Stage 1 = none · Stage 2 = minimal · **Stage 3 = minimal (final home stage)** · **Stage 4 = full equipment (first gym stage)** · Stages 5–7 = full. The gym-upgrade prompt / minimal-vs-full track choice happens **entering Stage 4** (see handoff §4).
- **Cardio** (Stages 4+) = zone-2, member picks the machine (treadmill / bike / rower / incline walk). **Stages 1–3 have no cardio block** — they're home stages; the circuits themselves supply the conditioning.
- Every day is **total-body** and ends with an **abs finisher**. Women lean lower-body/glutes; men lean upper-body/delts+arms. Isolation moves appear **only at Stages 5–7**.
- `(func)` = functional move (Stages 5–7). `(iso)` = isolation move (Stages 5–7).
- Full-equipment track shown for Stages 4–7. Minimal-track swaps are in the **Substitution map** at the bottom.

---

# STAGE 1 — 5 min · no equipment · timed  ✅ finalized
**Format:** 4 moves × 30s work / 30s rest, **repeat the circuit ×1** (= 5:00). Scale push-ups to incline/knee and squats to a chair as needed.

## Women (glute lean)
| Day | Squat | Pull | Push | Abs / glute |
|---|---|---|---|---|
| 1 | Sumo bodyweight squat | Towel row | Knee push-up | Glute bridge |
| 2 | Wall sit | Towel row | Incline push-up | Dead-bug |
| 3 | Reverse lunge | Towel row | Push-up | Single-leg glute bridge |
| 4 | Sumo squat (pulse) | Superman | Push-up | Plank |
| 5 | Split squat | Towel row | Knee push-up | Glute bridge |
| 6 | Step-up (stair) | Towel row | Incline push-up | Bird-dog |
| 7 | Bodyweight squat | Towel row | Push-up | Side plank |

## Men (upper / delt lean)
| Day | Squat | Pull | Push | Abs |
|---|---|---|---|---|
| 1 | Bodyweight squat | Towel row | Push-up | Plank |
| 2 | Reverse lunge | Towel row | Pike push-up | Dead-bug |
| 3 | Bodyweight squat | Superman | Push-up | Mountain climber |
| 4 | Split squat | Towel row | Incline push-up | Hollow hold |
| 5 | Wall sit | Towel row | Pike push-up | Bicycle crunch |
| 6 | Bodyweight squat | Towel row | Push-up (slow) | Plank |
| 7 | Step-up (stair) | Superman | Pike push-up | Side plank |

---

# STAGE 2 — 10 min · minimal equipment · timed
**Format:** 6 moves, **30s work / 20s rest each**, **repeat the circuit ×1** (2 rounds) = 10:00. Equipment: kettlebell, push-up handles, ab wheel, mat.

## Women (glute lean)
| Day | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | KB deadlift | KB goblet squat (sumo) | Single-leg glute bridge | Deep push-up | KB row | Ab-wheel rollout |
| 2 | KB swing | Split squat | Glute bridge | Deep push-up | KB row | Plank |
| 3 | KB deadlift | KB goblet squat | KB swing | Deep push-up | KB row | Dead-bug |
| 4 | KB deadlift | Reverse lunge | Single-leg glute bridge | Deep push-up | KB row | Ab-wheel rollout |
| 5 | KB swing | KB goblet squat (sumo) | Glute bridge | Deep push-up | KB row | Side plank |
| 6 | KB deadlift | Step-up | Single-leg glute bridge | Deep push-up | KB row | Ab-wheel rollout |
| 7 | KB goblet squat (sumo) | KB deadlift | KB swing | Deep push-up | KB row | Bicycle crunch |

## Men (upper / delt lean)
*KB overhead press removed; replaced with **pike push-up** (bodyweight delt press, scalable — hands on a raised surface to ease).*
| Day | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | KB deadlift | KB goblet squat | Deep push-up | Pike push-up | KB row | Ab-wheel rollout |
| 2 | KB swing | Split squat | Deep push-up | Pike push-up | KB row | Plank |
| 3 | KB deadlift | KB goblet squat | Deep push-up (slow) | Pike push-up | KB row | Mountain climber |
| 4 | KB deadlift | Reverse lunge | Deep push-up | Pike push-up | KB row | Ab-wheel rollout |
| 5 | KB swing | KB goblet squat | Deep push-up | Pike push-up | KB row | Hollow hold |
| 6 | KB deadlift | Step-up | Deep push-up | Pike push-up | KB row | Ab-wheel rollout |
| 7 | KB goblet squat | KB deadlift | Deep push-up | Pike push-up | KB row | Bicycle crunch |

---

# STAGE 3 — 20 min · **minimal equipment** · timed · **no cardio**
**The final home / minimal-equipment stage** — same kit as Stage 2, just longer. Compound only. **No exercise repeats two days in a row.** No cardio block (no home cardio equipment) — the fast-paced circuit itself provides the conditioning.
**Format:** **6 moves × 40s work / 20s rest, 3 rounds** (60s rest between rounds) ≈ 20 min.

## Women (glute lean)
| Day | Quad | Glute | Lower / glute 2 | Push | Pull | Abs |
|---|---|---|---|---|---|---|
| 1 | KB goblet squat | KB deadlift | Walking lunge | Deep push-up | KB row | Lying leg raise |
| 2 | Split squat | Single-leg glute bridge | KB swing | Push-up | Towel row | Ab-wheel rollout |
| 3 | KB goblet squat | KB deadlift | Reverse lunge | Deep push-up | KB row | Bicycle crunch |
| 4 | Step-up | Glute bridge | KB swing | Push-up | Towel row | Plank |
| 5 | Split squat | KB deadlift | Walking lunge | Deep push-up | KB row | Reverse crunch |
| 6 | KB goblet squat | Single-leg glute bridge | Calf raise | Push-up | Towel row | Ab-wheel rollout |
| 7 | Step-up | KB deadlift | KB swing | Deep push-up | KB row | Hollow hold |

## Men (upper / delt lean)
| Day | Leg | Push (chest) | Pull | Upper A (delt/back) | Upper B (tri/chest) | Abs |
|---|---|---|---|---|---|---|
| 1 | KB goblet squat | Deep push-up | KB row | Pike push-up | Chair dip | Lying leg raise |
| 2 | Walking lunge | Push-up | Towel row | Superman | Incline push-up | Bicycle crunch |
| 3 | Step-up | Deep push-up | KB row | Pike push-up | Chair dip | Plank |
| 4 | Split squat | Push-up | Towel row | Superman | Incline push-up | Mountain climber |
| 5 | KB goblet squat | Deep push-up | KB row | Pike push-up | Chair dip | Reverse crunch |
| 6 | Walking lunge | Push-up | Towel row | Superman | Incline push-up | Ab-wheel rollout |
| 7 | Step-up | Deep push-up | KB row | Pike push-up | Chair dip | Hollow hold |

---

# STAGE 4 — 20 min · **full equipment** · sets & reps · 5 min cardio + 15 min lift
First gym stage; timed→reps transition. Compound only (chest = machine press / push-up; flies arrive at Stage 5). **No exercise repeats two days in a row.**

## Women (glute lean)
| Day | Quad | Glute | Push | Pull | Abs |
|---|---|---|---|---|---|
| 1 | Leg press 3×12 | Hip thrust 3×12 | Machine chest press 3×12 | Seated cable row 3×12 | Cable crunch 3×15 |
| 2 | Walking lunge 3×10 | Single-leg glute bridge 3×12 | Push-up 3×max | Lat pulldown 3×12 | Lying leg raise 3×15 |
| 3 | Leg press 3×15 | Hip thrust 3×12 | Machine chest press 3×12 | Machine row 3×12 | Hanging knee raise 3×12 |
| 4 | Step-up 3×12 | Glute bridge 3×15 | Push-up 3×max | Seated cable row 3×12 | Reverse crunch 3×15 |
| 5 | Leg press 3×12 | Hip thrust 3×12 | Machine chest press 3×12 | Lat pulldown 3×12 | Bicycle crunch 3×20 |
| 6 | Walking lunge 3×10 | Single-leg glute bridge 3×12 | Push-up 3×max | Machine row 3×12 | Plank 3×45s |
| 7 | Leg press 3×12 | Hip thrust 3×12 | Machine chest press 3×12 | Seated cable row 3×12 | Cable crunch 3×15 |

## Men (upper / delt lean)
| Day | Leg | Push | Pull | Shoulder | Abs |
|---|---|---|---|---|---|
| 1 | Leg press 3×12 | Machine chest press 3×12 | Lat pulldown 3×12 | DB shoulder press 3×12 | Hanging knee raise 3×12 |
| 2 | Leg curl 3×12 | Push-up 3×max | Seated cable row 3×12 | Pike push-up 3×10 | Cable crunch 3×15 |
| 3 | Walking lunge 3×10 | Machine chest press 3×12 | Machine row 3×12 | DB shoulder press 3×12 | Plank 3×45s |
| 4 | Leg press 3×12 | Push-up 3×max | Lat pulldown 3×12 | Pike push-up 3×10 | Bicycle crunch 3×20 |
| 5 | Leg curl 3×12 | Machine chest press 3×12 | Seated cable row 3×12 | DB shoulder press 3×12 | Hanging knee raise 3×12 |
| 6 | Walking lunge 3×10 | Push-up 3×max | Machine row 3×12 | Pike push-up 3×10 | Reverse crunch 3×15 |
| 7 | Leg press 3×12 | Machine chest press 3×12 | Lat pulldown 3×12 | DB shoulder press 3×12 | Cable crunch 3×15 |

---

# STAGE 5 — 30 min · full · 5 min cardio + 25 min lift · isolation + functional unlock
~7 lifts. Chest goes fly-dominant here. **No exercise repeats two days in a row.**

## Women (super-glute)
| Day | Quad | Glute | Glute iso | Extra iso | Chest (fly) | Pull | Abs finisher |
|---|---|---|---|---|---|---|---|
| 1 | Leg press 3×12 | Hip thrust 3×12 | Cable glute kickback 3×15 | Calf raise 3×15 | Cable fly 3×12 | Seated cable row 3×12 | Ab-wheel + lying leg raise |
| 2 | Walking lunge 3×10 (func) | Single-leg glute bridge 3×12 | Hip abduction 3×15 | — | Pec deck 3×12 | Lat pulldown 3×12 | Hanging knee raise + cable crunch |
| 3 | Step-up 3×12 | Hip thrust 3×12 | Cable glute kickback 3×15 | Calf raise 3×20 | Cable fly 3×12 | Machine row 3×12 | Reverse crunch + plank |
| 4 | Leg press 3×12 | Single-leg glute bridge 3×12 | Hip abduction 3×15 | — | Pec deck 3×12 | Seated cable row 3×12 | Bicycle + hollow hold |
| 5 | Split squat 3×12 | Hip thrust 3×12 | Cable glute kickback 3×15 | Calf raise 3×15 | Cable fly 3×12 | Lat pulldown 3×12 | Ab-wheel + cable crunch |
| 6 | Walking lunge 3×10 (func) | Single-leg glute bridge 3×12 | Hip abduction 3×15 | — | Pec deck 3×12 | Machine row 3×12 | Hanging knee raise + side plank |
| 7 | Leg press 3×12 | Hip thrust 3×12 | Cable glute kickback 3×15 | Calf raise 3×20 | Cable fly 3×12 | Seated cable row 3×12 | Lying leg raise + cable crunch |

## Men (super-delt / arm)
| Day | Leg | Chest | Pull | Shoulder (iso) | Biceps (iso) | Triceps (iso) | Abs |
|---|---|---|---|---|---|---|---|
| 1 | Leg press 3×12 | Machine chest press 3×10 | Lat pulldown 3×10 | DB lateral raise 3×15 | EZ-bar curl 3×12 | Cable tricep pushdown 3×12 | Hanging knee raise + cable crunch |
| 2 | Leg curl 3×12 | Cable fly 3×12 | Seated cable row 3×10 | DB shoulder press 3×10 | DB curl 3×12 | Overhead tricep extension 3×12 | Bicycle + plank |
| 3 | Walking lunge 3×10 (func) | Machine chest press 3×10 | Machine row 3×10 | DB lateral raise 3×15 | Hammer curl 3×12 | Tricep kickback 3×12 | Hanging knee raise + hollow hold |
| 4 | Leg press 3×12 | Cable fly 3×12 | Pull-up 3×max | Rear-delt fly 3×15 | EZ-bar curl 3×12 | Cable tricep pushdown 3×12 | Cable crunch + side plank |
| 5 | Leg curl 3×12 | Machine chest press 3×10 | Seated cable row 3×10 | DB lateral raise 3×15 | DB curl 3×12 | Overhead tricep extension 3×12 | Hanging knee raise + cable crunch |
| 6 | Split squat 3×12 | Cable fly 3×12 | Machine row 3×10 | DB shoulder press 3×10 | Hammer curl 3×12 | Tricep kickback 3×12 | Bicycle + plank |
| 7 | Leg press 3×12 | Machine chest press 3×10 | Lat pulldown 3×10 | DB lateral raise 3×15 | EZ-bar curl 3×12 | Cable tricep pushdown 3×12 | Hanging knee raise + hollow hold |

---

# STAGE 6 — 45 min · full · 10 min cardio + 35 min lift · more isolation + volume
Squat = **leg press primary**, safety-bar backup, barbell back squat tertiary. **No exercise repeats two days in a row.**

## Women (super-glute) — ~9 moves
| Day | Quad | Glute hinge | Glute iso | Extra (ham/delt/calf) | Chest (fly) | Pull | Abs (2) | Functional |
|---|---|---|---|---|---|---|---|---|
| 1 | Leg press 4×12 | Hip thrust 4×12 | Cable glute kickback 3×15 | Leg curl 3×12 | Cable fly 3×12 | Seated cable row 3×12 | Ab-wheel + cable crunch | Sled push 3×20m |
| 2 | Walking lunge 3×12 | Single-leg glute bridge 4×12 | Hip abduction 3×15 | Rear-delt fly 3×15 | Pec deck 3×12 | Lat pulldown 3×12 | Hanging knee raise + side plank | Farmer carry 3×40s |
| 3 | Step-up 3×12 | Hip thrust 4×12 | Cable glute kickback 3×15 | Calf raise 3×20 | Cable fly 3×12 | Machine row 3×12 | Lying leg raise + cable crunch | Sled push 3×20m |
| 4 | Leg press 4×12 | Single-leg glute bridge 4×12 | Hip abduction 3×15 | Leg curl 3×12 | Pec deck 3×12 | Seated cable row 3×12 | Bicycle + plank | Farmer carry 3×40s |
| 5 | Split squat 3×12 | Hip thrust 4×12 | Cable glute kickback 3×15 | Rear-delt fly 3×15 | Cable fly 3×12 | Lat pulldown 3×12 | Reverse crunch + side plank | Sled push 3×20m |
| 6 | Walking lunge 3×12 | Single-leg glute bridge 4×12 | Hip abduction 3×15 | Calf raise 3×20 | Pec deck 3×12 | Machine row 3×12 | Hanging knee raise + hollow hold | Farmer carry 3×40s |
| 7 | Leg press 4×12 | Hip thrust 4×12 | Cable glute kickback 3×15 | Leg curl 3×12 | Cable fly 3×12 | Seated cable row 3×12 | Lying leg raise + bicycle | Sled push 3×20m |

## Men (super-delt / arm) — single alternating pull · shoulder every day
*Per Dan: no double pull — one pull/day alternating **vertical** and **horizontal**. Shoulder every day, alternating **compound (military/DB press)** and **isolation (side lateral / rear delt)**.*
| Day | Leg | Chest (press + fly) | Pull (alt V/H) | Shoulder (alt) | Biceps | Triceps | Abs | Functional |
|---|---|---|---|---|---|---|---|---|
| 1 | Leg press 4×12 · Leg curl 3×12 | Machine chest press 3×10 + Cable fly 3×12 | Lat pulldown 3×10 (V) | DB shoulder press 3×10 (comp) | EZ-bar curl 3×12 | Cable tricep pushdown 3×12 | Hanging knee raise + cable crunch | Battle ropes 3×30s |
| 2 | Walking lunge 3×12 | DB floor press 3×10 + Pec deck 3×12 | Seated cable row 3×10 (H) | DB lateral raise 3×15 (iso) | DB curl 3×12 | Overhead tricep extension 3×12 | Bicycle + side plank | Sled push 3×20m |
| 3 | Leg press 4×12 · Leg curl 3×12 | Machine chest press 3×10 + Cable fly 3×12 | Pull-up 3×max (V) | Military press (BB OHP) 3×10 (comp) | Hammer curl 3×12 | Tricep kickback 3×12 | Hanging knee raise + plank | Farmer carry 3×40s |
| 4 | Split squat 3×12 | DB floor press 3×10 + Pec deck 3×12 | Machine row 3×10 (H) | Rear-delt fly 3×15 (iso) | EZ-bar curl 3×12 | Cable tricep pushdown 3×12 | Cable crunch + bicycle | Battle ropes 3×30s |
| 5 | Leg press 4×12 · Leg curl 3×12 | Machine chest press 3×10 + Cable fly 3×12 | Straight-arm pulldown 3×12 (V) | DB shoulder press 3×10 (comp) | DB curl 3×12 | Overhead tricep extension 3×12 | Hanging knee raise + hollow hold | Sled push 3×20m |
| 6 | Walking lunge 3×12 | DB floor press 3×10 + Pec deck 3×12 | Seated cable row 3×10 (H) | DB lateral raise 3×15 (iso) | Hammer curl 3×12 | Tricep kickback 3×12 | Bicycle + side plank | Farmer carry 3×40s |
| 7 | Leg press 4×12 · Leg curl 3×12 | Machine chest press 3×10 + Cable fly 3×12 | Chin-up 3×max (V) | Military press (BB OHP) 3×10 (comp) | EZ-bar curl 3×12 | Cable tricep pushdown 3×12 | Hanging knee raise + cable crunch | Battle ropes 3×30s |

---

# STAGE 7 — 60 min · full · 15 min cardio + 45 min lift · peak volume · everyone ends here
**No exercise repeats two days in a row.**

## Women (super-glute) — ~9 moves
| Day | Quad | Glute hinge | Glute iso | Extra (ham/delt) | Chest (fly) | Pull | Calf | Functional | Abs (3) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Leg press 4×12 | Hip thrust 4×10 | Cable glute kickback 3×15 | Leg curl 3×12 | Cable fly 3×12 | Seated cable row 3×12 | Calf raise 3×20 | Sled push 4×20m | Ab-wheel + hanging leg raise + cable crunch |
| 2 | Walking lunge 4×12 | Single-leg glute bridge 4×12 | Hip abduction 3×15 | Rear-delt fly 3×15 | Pec deck 3×12 | Lat pulldown 3×12 | — | Farmer carry 4×40s | Reverse crunch + bicycle + side plank |
| 3 | Step-up 3×12 | Hip thrust 4×10 | Cable glute kickback 3×15 | Leg curl 3×12 | Cable fly 3×12 | Machine row 3×12 | Calf raise 3×20 | Sled push 4×20m | Ab-wheel + lying leg raise + hollow hold |
| 4 | Leg press 4×12 | Single-leg glute bridge 4×12 | Hip abduction 3×15 | Rear-delt fly 3×15 | Pec deck 3×12 | Seated cable row 3×12 | — | Farmer carry 4×40s | Hanging leg raise + bicycle + plank |
| 5 | Split squat 3×12 | Hip thrust 4×10 | Cable glute kickback 3×15 | Leg curl 3×12 | Cable fly 3×12 | Lat pulldown 3×12 | Calf raise 3×20 | Sled push 4×20m | Cable crunch + reverse crunch + side plank |
| 6 | Walking lunge 4×12 | Single-leg glute bridge 4×12 | Hip abduction 3×15 | Rear-delt fly 3×15 | Pec deck 3×12 | Machine row 3×12 | — | Farmer carry 4×40s | Ab-wheel + hanging leg raise + hollow hold |
| 7 | Leg press 4×12 | Hip thrust 4×10 | Cable glute kickback 3×15 | Leg curl 3×12 | Cable fly 3×12 | Seated cable row 3×12 | Calf raise 3×20 | Sled push 4×20m | Lying leg raise + bicycle + plank |

## Men (super-delt / arm)
*Per Dan: leg slot **alternates traditional (leg press) with leg-primary functional (sled / walking lunge / farmer carry)**; non-leg functional (battle ropes) removed. **Shoulder every day**, alternating side-lateral (iso) and military press (comp). **Chest trimmed to one move/day, one set lighter**, alternating **press and fly**. Pull kept at two/day (one vertical + one horizontal), rotated so nothing repeats.*
| Day | Leg (alt trad/func) | Ham | Chest (alt press/fly) | Pull V | Pull H | Shoulder (alt) | Biceps (2) | Triceps (2) | Abs (3) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Leg press 4×12 | Leg curl 3×12 | Machine chest press 3×10 (press) | Lat pulldown 4×10 | Seated cable row 4×10 | DB lateral raise 4×15 (iso) | EZ-bar curl 4×12 | Cable tricep pushdown 4×12 | Ab-wheel + hanging leg raise + cable crunch |
| 2 | Sled push 4×20m (func) | — | Cable fly 3×12 (fly) | Pull-up 4×max | Machine row 4×10 | Military press 4×10 (comp) | DB curl 4×12 | Overhead tricep extension 4×12 | Bicycle + reverse crunch + side plank |
| 3 | Leg press 4×12 | Leg curl 3×12 | DB floor press 3×10 (press) | Chin-up 4×max | Seated cable row 4×10 | DB lateral raise 4×15 (iso) | Hammer curl 4×12 | Tricep kickback 4×12 | Ab-wheel + hanging leg raise + hollow hold |
| 4 | Walking lunge 4×12 (func) | — | Pec deck 3×12 (fly) | Straight-arm pulldown 4×12 | Machine row 4×10 | Military press 4×10 (comp) | EZ-bar curl 4×12 | Cable tricep pushdown 4×12 | Cable crunch + bicycle + plank |
| 5 | Leg press 4×12 | Leg curl 3×12 | Machine chest press 3×10 (press) | Lat pulldown 4×10 | Seated cable row 4×10 | DB lateral raise 4×15 (iso) | DB curl 4×12 | Overhead tricep extension 4×12 | Hanging leg raise + reverse crunch + side plank |
| 6 | Farmer carry 4×40s (func) | — | Cable fly 3×12 (fly) | Pull-up 4×max | Machine row 4×10 | Military press 4×10 (comp) | Hammer curl 4×12 | Tricep kickback 4×12 | Bicycle + hollow hold + plank |
| 7 | Leg press 4×12 | Leg curl 3×12 | DB floor press 3×10 (press) | Chin-up 4×max | Seated cable row 4×10 | DB lateral raise 4×15 (iso) | EZ-bar curl 4×12 | Cable tricep pushdown 4×12 | Ab-wheel + hanging leg raise + cable crunch |

---

# Substitution map (full → minimal → no-equipment)
Stages 1–3 are already minimal/none. This map covers **Stage 4+ minimal-track members** (declined the gym at Stage 4) and no-equipment fallbacks. Same day structure; swap each move down its row.

| Movement | Full equipment | Minimal (KB / handles / wheel / mat) | No equipment |
|---|---|---|---|
| Squat | Leg press | KB goblet squat | Bodyweight / sumo squat |
| Lunge / step | Walking lunge (DBs) | Bodyweight walking lunge · step-up | Reverse lunge · split squat |
| Glute hinge | Hip thrust | KB deadlift · KB swing | Single-leg glute bridge |
| Glute iso | Cable glute kickback · hip abduction | Band kickback · band abduction* | Donkey kick · fire hydrant |
| Hamstring | Leg curl (machine) | KB deadlift | Single-leg glute bridge |
| Chest press | Machine chest press · DB floor press | Deep push-up (handles) | Push-up / incline push-up |
| Chest fly | Cable fly · pec deck | Band fly* | Slow push-up (tempo) |
| Back row (H) | Seated cable row · machine row | KB row | Towel row · table row |
| Vertical pull | Lat pulldown · pull-up · chin-up | KB high pull | Towel row |
| Shoulder (comp) | DB shoulder press · military press | KB overhead press | Pike push-up |
| Lateral raise (iso) | DB lateral raise | KB / band lateral raise* | — (skip on no-equip) |
| Rear delt (iso) | Rear-delt fly (machine/DB) | Band rear-delt fly* | Superman |
| Biceps (iso) | EZ-bar / DB curl | Band / KB curl* | Towel curl (self-resisted) |
| Triceps (iso) | Cable pushdown · overhead ext | KB overhead extension | Chair dip |
| Calves (iso) | Calf raise (machine) | Standing calf raise | Standing calf raise |
| Functional (legs) | Sled · walking lunge · farmer carry | KB swing · KB farmer carry | Walking lunge · step-up |
| Cardio | Any machine, zone-2 | Brisk walk / jog, zone-2 | Brisk walk / jog, zone-2 |

\* Band moves require adding a **resistance band (~$15)** to the minimal kit — the open item flagged in HANDOFF_trainer_v3.md §6. Without a band, minimal-track chest is push-up-dominant and delt/arm/glute isolation is limited.
