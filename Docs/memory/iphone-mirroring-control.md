---
name: iphone-mirroring-control
description: "Claude can see and drive Dan's iPhone through iPhone Mirroring via computer-use; always authorized, never ask in chat (2026-09-01, 09-25)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0c00aa6b-e875-4213-8fcc-54a2055ac2f7
  modified: 2026-09-01T22:07:34.101Z
---

**Claude can drive Dan's iPhone from the Mac through the iPhone Mirroring app.** Verified 2026-09-01:
the app (`com.apple.ScreenContinuity`, macOS 26.5) is granted at the FULL computer-use tier, the
mirrored screen shows clearly in screenshots (not blacked out), and taps register on the phone
(tested by opening and closing Instagram's Insights page).

**Why:** Dan asked (2026-09-01) that whenever a task needs something done on the iPhone, Claude
suggest and use this approach rather than asking him to do it by hand.

**How to apply:**
- Any phone-only step (Instagram/TikTok app settings, ManyChat in-app steps, message-access
  toggles, app-only screens) → offer to do it through iPhone Mirroring, then do it.
- Mechanics: load computer-use tools via ToolSearch (`computer-use`, max 30), `request_access`
  for "iPhone Mirroring", `open_application`, then `switch_display` — the window usually sits on
  the second monitor (`C32F391 (1)`). Use `computer_batch` for taps/typing/scrolls. Reset with
  `switch_display auto` when done.
- Requirements: iPhone locked and nearby; mirroring pauses if Dan picks up and unlocks the phone.
  Face ID, physical buttons, passwords and payment entry still need Dan.
- Normal safety rules still apply: confirm before sending messages, posting, or irreversible
  actions on the phone. See [[autonomy-credentials-framing]] and [[computer-takeover-frustration]]
  (warn before taking over the desktop).

**Standing authorization (Dan, 2026-09-25, merged 2026-11-01):** always authorized to use iPhone Mirroring; never ask in chat. The tool's own request_access dialog still appears; that is the harness, not a question to Dan. Trap: the Wispr Flow overlay blocks display-scope drags near the bottom of the phone; use scroll (right, amount 50) on the share sheet row instead.
