---
name: touched-up-screenshot-means-real
description: 2026-11-06: "touched-up screenshot" = a real video frame with photo edits only (exposure, contrast, colour, sharpening), never an AI retouch
metadata:
  type: feedback
---
When Dan asks for "touched-up screenshots" of himself (covers, thumbnails), use the real frame and apply only photo-editing adjustments to the real pixels: exposure, tone curve, contrast/clarity, colour, sharpening, crop, downscale. No Codex, Google or any generative retouch, inpainting or frame extension. Title space comes from flat colour blocks or gradients, not generated background.

**Why:** On DS-77 T-Bar Rows (2026-11-06) four Codex "retouches" of real frames came back; Dan: "this isn't what I asked for. These are AI-generated images. I want four touch-up screenshots, real images, not AI-generated." (DS-76 F had been a Codex retouch and he picked it, so the old reading looked approved.)

**How to apply:** pull the frame at 16-bit (`-pix_fmt rgb48le`), edit in float, dither to 8-bit; skip heavy denoise and tile CLAHE (they made the skin blotchy). Pick frames where his face is focused, not grimacing. Working script: `scripts/covers/ds77-20261105/real_build.py`. Related: [[cover-photo-selection]], [[thumbnail-standard-codex-in-setup]].
