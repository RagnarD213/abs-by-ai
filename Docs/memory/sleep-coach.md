---
name: sleep-coach
description: "AI Sleep Coach — SHIPPED July 10 2026: endpoints, gating, cross-feature wiring, what remains (Phase 2/3)"
metadata:
  node_type: memory
  type: project
  originSessionId: fde75fca-a07f-4de9-af59-1bcaf4d6cca2
---

AI Sleep Coach MVP shipped to prod July 10, 2026 (commit 06fab14; plan in repo `HANDOFF_sleep_coach.md`). Dan's locked rules implemented: verdict is ALWAYS "GO HARD" (enforced server-side after the model call); bad night → "watch your eating" + "stay tight" tactics; great night → push a higher deficit; trend escalation touches sleep fixes only; minimal red-flag safety valve (never paywalled) + not-medical-advice footer.

Built: `sleep_entries` table (one row per user per day, upsert on re-check-in); `POST /api/sleep/checkin` (aiLimiter+optionalAuth; manual form OR tracker-screenshot vision — one claude-sonnet-4-6 call extracts numbers AND writes the briefing via json_schema output); `GET /api/sleep/history` (last 30, trend strip). Gating follows [[ai-trainer-membership]]: free = verdict/headline/justification/parsed numbers; members = tactics/tonight/trend. Cross-feature prompt injection via `getTodaysSleep()`: trainer (generate-program + program/checkin) bad night → longer warm-up, never shorter/lighter; nutritionist (generate-mealplan + mealplan/checkin) bad night → calories up via protein ONLY, great night → higher deficit. Verified on prod: manual bad/great, screenshot parse (read a fake Oura screen exactly), save/upsert/history, mealplan picked up sleep context.

Pending: member full-briefing + unlock flow untested with a real paid account; screenshot misread "edit numbers" affordance if misreads show up; Phase 2 (protocol builder, weekly summary, wind-down push), Phase 3 (HealthKit in [[ios-capacitor-app]], Oura/Whoop APIs).
