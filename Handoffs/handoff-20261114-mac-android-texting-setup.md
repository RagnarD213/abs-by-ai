# Handoff: make texting Android phones work on the new Mac (Codex and Grokbot)

Date: 2026-11-14. Owner: whichever of Codex or Grokbot starts first; do not both work it.

## Goal
Dan's new Mac can send texts to Android contacts the way his old Mac did. Today a message to Brittany Dolan (Android, thread shows "Text Message • RCS") ends as "Not Delivered" with a red alert. Done means: the failed message is resent from the Mac and shows delivered, and a fresh test text to an Android contact goes through.

## Authorization (Dan, 2026-11-14)
Dan asked for this to be set up. You are authorized to do the whole step, including any iPhone settings change, any Mac Messages setting, and any Apple ID prompt or verification code that appears. Do not stop to ask him. Only rule: do not write secret values (passwords, codes) into repo files.

## Why Claude stopped
Claude's request for control of Messages, System Settings and iPhone Mirroring was denied in its session, so it changed nothing. Nothing has been attempted on the Mac or the iPhone.

## Diagnosis so far
The Mac already labels the thread RCS, so Messages is working. The Mac sends Android texts by relaying through Dan's iPhone (Text Message Forwarding). A new Mac is not added automatically, so the relay is almost certainly not enabled for it.

## Steps
1. iPhone: Settings, Apps, Messages, Text Message Forwarding. Turn on the toggle for the new Mac. If a 6-digit code appears on the Mac, enter it on the iPhone (iPhone Mirroring can do this).
2. iPhone: Settings, Apps, Messages, confirm RCS Messaging is on.
3. Mac: Messages, Settings, iMessage tab. Confirm the same Apple ID as the iPhone and that the phone number and email are ticked under "You can be reached for messages at".
4. If the Mac is missing from the iPhone list: toggle forwarding off and on, quit and reopen Messages, confirm both devices are online.
5. Resend the failed message to Brittany Dolan ("I'll be done working at 3. Can you come by then?") by right-clicking the Not Delivered message and choosing Resend. Dan wrote this message, so resending is already authorized. Send no other new messages to real contacts; if a separate test is needed, text Dan's own Android number only if one is on file, otherwise rely on the resend.
6. Verify the message shows Delivered (or no red alert) and report.

## Done report
Say which setting was off, what was changed, and the result of the resend.
