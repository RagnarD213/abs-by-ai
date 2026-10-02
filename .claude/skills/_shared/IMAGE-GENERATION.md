# Image generation goes through Codex (Dan, 2026-10-01)

**Every image a session generates is made by Codex on Dan's ChatGPT subscription, not by a paid API.**
This covers every skill and every ad hoc request: generated images, backgrounds and plates, AI start and
end frames for clips, long-form thumbnails, shorts covers, Instagram posts, marketing images, retouch
passes. Dan tested it against Nano Banana Pro on 2026-10-01 and ruled: "everything is now Codex."

Wherever a skill, script or handoff says Nano Banana Pro, Gemini 3 Pro Image, `gemini-image.js`,
`rep-t2i.js`, `replicate-edit.js`, Seedream or FLUX for a still image, read it as this helper instead.

## How

```bash
.claude/skills/_shared/codex-image.sh --prompt-file p.txt --out result.png [--image ref.jpg]...
```

**Thumbnails and covers always pass `--model gpt-6.1-sol --effort high`** (Dan, 2026-10-02), unless he names another model.

No handoff and no separate Codex task: the session calls it directly, the way it used to call Gemini.
One image takes about a minute and 22,000 to 40,000 Codex tokens. Run several at once with `&` and `wait`.
State the image count before a batch; it draws on the Codex allowance, so do not generate spares.

## What Codex gives back, and what to do about it

- **Size.** About 1672x941 (16:9), 941x1672 (9:16), 1122x1402 (4:5), 1024x1536 (2:3). Upscale locally
  with Real-ESRGAN when the deliverable needs more (shorts covers need 1080x1920). Never a paid upscaler.
- **It redraws people.** Told "do not edit the man", it still changed Dan's skin tone and size. So when
  the piece uses a real photo of Dan, generate the BACKGROUND ONLY with Codex, then layer his real cutout
  (`photos/finalized social media photos/_cutouts/`) and the type on top in code. This is how the Jelly
  Beans cover and the studio posts are built, and it stays the rule.
- **It adds bulk.** For a generated Dan (no real photo available), say "lean and shredded, not bulky,
  same size as the reference" in the prompt.
- **Text.** It spells headlines correctly but lets them touch the head and arms. Type that ships is set
  in code, not generated.

## Not covered

- The live app. `server.js` generates for visitors through the API and cannot use a subscription.
- AI video generation (Kling, Veo, Wan). There is no subscription path; it stays on the API.
- Background removal, upscaling, cropping and compositing. These are local tools, not generation.

## The old API scripts are locked

`gemini-image.js`, `rep-t2i.js` and `replicate-edit.js` refuse to run for still images unless
`ALLOW_API_IMAGE=1` is set. Set it only when Codex has failed twice on the same image, or Dan asks for
the API by name. Say so in chat when you do, with the cost.
