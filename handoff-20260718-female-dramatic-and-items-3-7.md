# Handoff: Kill the "after looks the same" problem (female-first) + ship Items 3–7

**Date:** 2026-07-18
**Project:** Abs By AI / absbyai.com
**Business goal this serves:** Adoption + retention. The single most damaging user experience is generating a transformation that looks identical to the input photo — it makes the user conclude "this app doesn't work" and they never come back or convert. This is worst for **women**. Fixing it protects every downstream dollar (trial starts, memberships, prints).

---

## Objective (read this first — the priority order matters)

**PRIMARY GOAL (Goal A): Eliminate the "after looks the same as the before" failure, and make female transformations meaningfully more dramatic.** This is the main point of this task. Everything else is secondary. Two hard product facts from Dan drive the aggression budget:

- **Almost no users have ever complained that a transformation was *too* dramatic. ZERO female users have.** So we have large headroom to push harder, especially for women. When in doubt, push the transformation further, not gentler.
- A near-identical "after" is *demoralizing* and reads as a broken product. We would rather over-shoot the change than under-shoot it.

**SECONDARY GOAL (Goal B): Ship Items 3–7** from `handoff-20260717-security-and-prompt-improvements.md` (Items 1 and 2 are already done, committed, pushed, and live-verified — see `AI_COORDINATION.md`). Items 3 and 6 are the mechanism for Goal A; Items 4, 5, 7 are independent product polish.

Ship as **separate commits per item**, each **live-verified on `absbyai.com` with real photos** before the next (per the project's standing delivery rules). The local dev environment has a dummy `GEMINI_API_KEY`/`ANTHROPIC_API_KEY` and cannot run real generation — **all transformation-quality verification must happen on prod.**

---

## Current State (verified against the code 2026-07-18)

The generation flow (`/api/generate-image`, `server.js:2018`):
1. Client assembles the image-edit prompt (Haiku, `GOAL_SYSTEM_PROMPT`) and calls `/api/generate-image` with `{ prompt, photoBase64, photoMime, intensity, deviceId, distinctId, attemptId, ... }`. **Note: `sex`/gender is baked into the prompt text but is NOT sent as a structured field** (`public/index.html:8162`). The server therefore cannot currently branch on gender.
2. Server calls Gemini 2.5 Flash Image (`callGemini`, `server.js:2036`). One automatic retry with a "SAFE FITNESS EDIT" preamble if the first call fails (`server.js:2122`).
3. **Change-verifier + intensify-retry ladder runs ONLY for `dramatic`/`max`** (`server.js:2128`: `if (result.ok && (intensity === 'dramatic' || intensity === 'max'))`). It calls `looksDramaticallyChanged` (`server.js:2084`, Haiku vision, returns YES/NO, **fails open** = returns `true` on any error so the paid flow is never blocked) and, if the change is too weak, re-calls Gemini with one of two escalating "you were too subtle, push harder" preambles (`server.js:2129–2132`).

**Why women get "looks the same" more than men — three stacking causes:**

1. **The safety net has a hole.** The verifier + intensify-retry only fires on `dramatic`/`max`. On **`subtle`/`moderate` there is NO check and NO retry** — if Gemini no-ops, the user just gets their photo back. Many women pick the gentler settings.
2. **A "correct" female result is a smaller visual delta than a male one.** Prompt body-fat anchors (`public/index.html:2770–2771`): MALE dramatic 9–11%, FEMALE dramatic 16–18% (floor 14%). A 16–18% feminine midsection is genuinely far less visually striking than a 10% male six-pack, so even a *successful* female edit reads as subtle.
3. **Gemini under-edits female bodies more often** (the reason the July-16 female-boost work happened). The prompt is already forceful (`public/index.html:2761`, `2794–2799`) but text alone doesn't fully stop the model hedging on women.

**The verifier prompt itself is male-biased** (`server.js:2106`): it asks for "ab muscle definition (actual separation lines)… tighter/more tapered waist." That's fine for men; for women the target is a *feminine four-pack / vertical midline / oblique lines*, so the verifier can both (a) miss weak female results it should catch and (b) be calibrated to the wrong bar.

**Good existing engineering — do NOT break:**
- `attemptId` idempotency cache (`server.js:2025`) prevents double-charging on replay — the verifier/retry logic runs *before* the response is cached, so extra retries never re-charge.
- `looksDramaticallyChanged` fail-open behavior (`server.js:2118`) — never make the verifier able to block a paid generation.
- The per-IP free cap (Item 2, `server.js`) and the credit-gating block — leave untouched.
- `state.gender` is already auto-detected from the photo (`public/index.html:7909`) and defaults to `'male'` (`public/index.html:2709`); intensity defaults to `'dramatic'` (`public/index.html:2711`).

---

## Key Decisions Already Made

- **Bias every ambiguous call toward MORE change, especially for women.** Given zero "too dramatic" complaints, the failure mode we optimize against is under-editing, not over-editing. Keep female results unmistakably *feminine* (four-pack not blocky six-pack, no vascularity/veins, no masculinized shoulders) — "more dramatic" means more visible definition + tighter taper, not "make her look like a man."
- **Pass `sex` as a structured field** from client → `/api/generate-image` so the server can run a gender-aware verifier and gender-aware retry. Small, safe addition to the existing body (`public/index.html:8162`).
- **Extend the verifier + intensify-retry to ALL intensities**, gender-aware. For **female, run it at every intensity** (subtle/moderate/dramatic/max). For **male, extend at least to `moderate`** (subtle can stay lighter). Keep fail-open.
- **Lower the female body-fat anchors and floor by ~one step** to widen the visual delta — but do this as a *tunable* change verified on real photos, and keep the feminine-archetype language. This is the highest-reward, highest-regression-risk edit; isolate it.
- **Item 6 (trim redundant prompt language) is now CONSTRAINED:** it must NOT reduce female aggression. Only consolidate genuinely duplicated *male* / generic reminders; the female-dramatic blocks stay or get stronger. If in doubt, skip Item 6 rather than risk softening female output.
- **Item 4 default stays "Dream."** The realism toggle is a retention feature, not a fix for this problem (a "realistic" mode makes the change *smaller*, which is the opposite of Goal A). Default must remain today's peak behavior.
- **All prompt edits stay additive/surgical** — same 7-section structure, same safety rules, same `REFUSED_MINOR`, same framing/preserve-verbatim blocks, same skin-tone rules. Do not restructure the prompt.

---

## Detailed Plan

### GOAL A — Items 3 + prompt aggression (do these FIRST, they are the point)

#### A1. Send `sex` to the server + add per-generation logging (Item 3, part 1) — OWN COMMIT
1. Client: add `sex: state.gender` (and `startCondition: state.condition`, `mode` if Item 4 lands later) to the `/api/generate-image` body (`public/index.html:8162`). Server: destructure `sex` in the handler (`server.js:2020`).
2. Add structured logging on **every** generation (both `console.log` for Railway logs AND a PostHog `capture` keyed by `distinctId`, which is already sent): `{ sex, intensity, startCondition, verifierRan, verifierPassedFirstTry, retryRungsUsed, finalVerifierPassed }`. Keep fail-open — logging must never throw into the flow.
3. **This ships first and alone** so we get real data on how often female `moderate`/`subtle` no-ops before we tune further. Watch the logs/PostHog for a day.
4. **Verify live:** run a female `moderate` and a female `dramatic` on prod; confirm the log/PostHog event records the fields and the image still returns.

#### A2. Verifier + intensify-retry on ALL intensities, gender-aware (Item 3, part 2) — OWN COMMIT
1. Change the gate at `server.js:2128` from `dramatic`/`max`-only to run for all intensities, with per-gender/-intensity retry budget: female = run at every intensity; male = run at `moderate`/`dramatic`/`max`. (Subtle-male may stay 0–1 rungs.)
2. Make `looksDramaticallyChanged` **gender-aware** (`server.js:2084`): for female, ask about a *feminine four-pack / vertical midline groove / oblique lines / visibly tighter waist-to-hip taper*; for male, keep the current six-pack/serratus wording. Loosen the bar slightly at `subtle`/`moderate` so it accepts a *smaller but real* change (don't demand "sharp separation lines" at subtle) — the goal is to catch true no-ops, not to reject legitimately gentle edits.
3. Give female its own intensify preambles (four-pack / feminine-taper language, "do NOT output a near-identical image") rather than the current male-worded ones (`server.js:2129`).
4. Keep fail-open everywhere; keep the whole loop *before* `cacheAttempt` so retries never re-charge.
5. **"Still weak after all retries" signal:** if the final verifier is still NO, return the image with a `weakChange: true` flag. Client: when `weakChange` is true and not locked, surface the existing **"More dramatic"** control (`public/index.html:1658`) prominently / auto-nudge, so the user gets a one-tap stronger redo instead of silently receiving a same-as-before. (Do not auto-spend another credit without consent.)
6. **Verify live on prod with REAL female photos** at subtle, moderate, and dramatic: confirm weak edits get caught and retried, and the returned image is visibly changed. Compare against current prod output.

#### A3. Turn up female transformation strength in the prompt (part of Goal A) — OWN COMMIT (highest regression risk — isolate)
1. Lower the FEMALE body-fat anchors ~one step and drop the floor (e.g. dramatic 16–18% → ~14–16%, max → ~13–15%, floor 14% → ~13%) in the anchor table (`public/index.html:2770–2771`), and mirror the user-facing display numbers (`BF_AFTER`, `public/index.html:2684`). Keep MALE as-is.
2. Apply the "twice the visible definition / do NOT output a near-identical image" female directive at **`moderate` too**, not only `dramatic`/`max` (`public/index.html:2761`). Strengthen the female GENDER-SPECIFIC block (`public/index.html:2794–2799`) toward more visible definition and a more pronounced waist-to-hip taper — while explicitly preserving femininity (no veins/vascularity, feminine four-pack not blocky, sculpted-not-bulky shoulders; these guards already exist at `2792`/`2797` — keep them).
3. Keep changes surgical and reversible; this is the edit most likely to subtly regress identity/femininity, so verify hardest.
4. **Verify live on prod with several REAL female photos** across body types and intensities: results must be clearly more dramatic than current prod, still unmistakably female, face/pose/framing/clothing preserved. This is a compare-before-you-ship edit.

### GOAL B — remaining Items (independent polish)

#### Item 4 — "Realistic 90-day" vs "Dream physique" toggle — OWN COMMIT
- Add a toggle near the intensity picker (`public/index.html:1465`), **default = Dream** (today's behavior). Persist in `state`. Thread `mode: 'dream'|'realistic'` through `makeUserJson()` (`public/index.html:7937`) into the prompt. In `realistic` mode, apply the existing "heavier → downgrade one body-fat step + believable mid-journey" logic to ALL starting conditions and add the mid-journey directive; `dream` = exactly as today. A mockup of the UX has been shown to Dan. **This is a retention lever, NOT a fix for Goal A** — do not let it soften the default path.

#### Item 5 — Auto before/after share card — OWN COMMIT (cheap growth lever)
- Client-side `<canvas>` composite (before left, after right, small "Abs by AI · absbyai.com" watermark) + a "Share / Save before-after" button on the result screen; wire `navigator.share` if present, else download the PNG. No server, no cost. Verify the card renders + saves/shares on mobile prod.

#### Item 6 — Trim redundant prompt language — OWN COMMIT, LOW priority, CONSTRAINED
- Consolidate only genuinely duplicated generic/male "must look different" reminders in `SYSTEM_PROMPT` (`public/index.html:2482`). **Must not weaken any female block** (that would fight Goal A). Do NOT touch safety rules, body-fat table, `REFUSED_MINOR`, framing/preserve blocks, skin-tone rules. If there's any risk of softening output, **skip this item** — the latency win is not worth a regression. Verify male + female dramatic + one subtle on prod before shipping.

#### Item 7 — Specific failure copy from Gemini block reason — OWN COMMIT, LOW priority
- The block path already logs `promptFeedback`/`finishReason`/text (`server.js:2144`). Map common reasons to tailored guidance returned to the client (`SAFETY` → "try standard gym wear or swimwear"; low-light/`IMAGE_*` → "try a brighter, front-facing photo") with a generic fallback (current copy at `server.js:2149`). Trigger a block on prod and confirm the tailored message shows.

---

## Things to Avoid / Lessons Learned
- **Don't let the verifier block a paid generation.** Keep `looksDramaticallyChanged` fail-open (`server.js:2118`) and keep all retries *before* `cacheAttempt`.
- **Don't masculinize women** while chasing drama — keep the feminine-archetype, no-vascularity, sculpted-not-bulky guards. "More dramatic" = more visible definition + tighter taper, not male morphology.
- **Don't verify transformation quality locally** — dummy API keys can't run Gemini/Haiku. Prod-only, with real photos (there are proof assets under `public/img/proof/` for smoke tests, but judge quality on varied real photos).
- **Ship A3 (female anchor retune) isolated** — it's the highest-regression edit; a bad tune degrades identity/femininity subtly. Compare against current prod output before pushing.
- **Item 6 must not fight Goal A** — when trimming, err toward keeping female aggression.
- **Coordinate ownership:** `AI_COORDINATION.md` currently shows the member-profile task as active (Codex-owned) and it also edits `public/index.html`. Confirm ownership/handoff before editing the same file to avoid clobbering — set yourself as Owner of this task in `AI_COORDINATION.md` first.
- Retries cost real Gemini money per rung — the extended verifier will raise per-generation cost on weak edits. That's an accepted trade (a same-as-before is worth far more lost revenue than a retry). The logging from A1 will quantify it.

## Relevant Files & Locations
- `server.js:2018` — `/api/generate-image` handler; `:2020` destructure (add `sex`).
- `server.js:2084` — `looksDramaticallyChanged` verifier (make gender-aware, loosen at subtle/moderate).
- `server.js:2106` — the verifier's male-biased question text.
- `server.js:2128` — the `dramatic`/`max`-only gate to widen to all intensities.
- `server.js:2129–2132` — intensify preambles (add female-specific set).
- `server.js:2144` / `:2149` — block logging + generic failure copy (Item 7).
- `public/index.html:8162` — `/api/generate-image` request body (add `sex`, `startCondition`, `mode`).
- `public/index.html:2770–2771` — prompt body-fat anchor table (female retune).
- `public/index.html:2684` — `BF_AFTER` user-facing display numbers (mirror female retune).
- `public/index.html:2761`, `2794–2799` — female dramatic directive + gender-specific block (strengthen; extend to moderate).
- `public/index.html:2482` — `SYSTEM_PROMPT` (Item 6 trims, constrained).
- `public/index.html:7937` — `makeUserJson()` (thread `mode` for Item 4).
- `public/index.html:1465` — intensity picker (Item 4 toggle placement); `:1658` — existing "More dramatic" button (reuse for the `weakChange` nudge).
- `public/index.html:7909` — sex auto-detect; `:2709`/`:2711` — gender/intensity defaults.
- Deploy: Railway auto-deploy on push to `main`; verify on `https://absbyai.com`. PostHog key already embedded in `index.html`. Persistence/serving caveats: server serves ONLY `public/`; root `*-data.json` files are the GitHub-API-persisted DB — never untrack them.

## Verification Strategy (every item)
Commit → push → confirm Railway deploy healthy (`/health` 200) → verify on `absbyai.com`. For Goal A items, verification = **real female photos across body types and intensities**, comparing the new output against current prod for (a) visibly more dramatic change, (b) preserved femininity/identity/framing, (c) the verifier catching and retrying weak edits (watch Railway logs / PostHog for the A1 fields). Do not rely on the local environment for any transformation-quality claim.

## Model & Effort Recommendation

This task is dominated by the **Anthropic-integration code (the Haiku verifier), the transformation prompt, and brand-facing output quality** — all "always-Claude" categories — and the female-aggression retune is a subtle-quality-judgment edit where being wrong degrades the core product quietly. That argues for the strongest reasoning available and real-photo verification, not raw throughput.

| Scenario | Recommendation |
|---|---|
| **Default (recommended)** | **Claude Opus 4.8, extended thinking (high effort)** for the whole batch. Goal A (A1–A3) and Items 4 and 6 all touch the prompt/verifier and demand careful, reversible edits + judgment about "did this go far enough without masculinizing." Opus + extended thinking is worth it here — this is the revenue-critical quality of the product. |
| **If Claude usage is high / cost-sensitive** | Keep **Goal A (A1–A3) and Item 6 on Claude Opus 4.8 / at minimum Claude Sonnet 5, extended thinking** — non-negotiable, they're prompt/verifier + brand output. Offload the two mechanical, well-specified items — **Item 5 (client-side share card)** and **Item 7 (failure-copy mapping)** — to **Claude Sonnet 5 standard thinking** (or Codex flagship, medium effort). Never send the prompt/verifier items to a non-Claude model. |

**Effort level:** **High / extended thinking** for A1–A3, 4, 6. **Medium / standard thinking** for 5 and 7. Rationale: the prompt/verifier/female-tuning items have subtle, hard-to-detect failure modes (a slightly-too-weak retune still "works" but quietly under-delivers, exactly the problem we're fixing) and each needs real-photo comparison; the share card and failure copy are deterministic and low-risk.

## Starter Prompt for the Next Task

> Read `handoff-20260718-female-dramatic-and-items-3-7.md` in the Abs By AI project root, then read `AI_COORDINATION.md` and set yourself as Owner of this task (confirm the member-profile task isn't mid-edit in `public/index.html` first). **The PRIMARY goal is to eliminate the "after looks the same as the before" failure and make FEMALE transformations meaningfully more dramatic** — Dan has confirmed almost no users, and zero women, have ever complained a result was too dramatic, so bias every call toward more change (while keeping women unmistakably feminine — no vascularity, feminine four-pack not blocky, sculpted-not-bulky). Start with A1: send `sex` from the client to `/api/generate-image` and add per-generation logging (verifier ran/passed, retry rungs, sex, intensity) to Railway logs + PostHog — ship that alone and read the data. Then A2 (gender-aware verifier + intensify-retry on ALL intensities, with a `weakChange` nudge) and A3 (retune the female body-fat anchors one step lower — highest regression risk, isolate and compare against current prod). Then Items 4, 5, 6 (constrained — must not soften female output), and 7 from the older security handoff. Ship each as its own commit and **live-verify on absbyai.com with REAL female photos** before the next — the local env can't run Gemini/Haiku. Keep the verifier fail-open and all retries before the attemptId cache so nothing double-charges. Use Claude Opus 4.8 with extended thinking for the prompt/verifier items.
