# Worked example: "AI Got Me Abs at 40" (Round 2, approved 2026-09-30)

Canvas: https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, page Round 2 (private). Doc: `1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o`.
Asset session Drive folder: `1FullVwvuRxdbbaKhpy1_KLdAGLlG3XnC`.

- `gen.py`: one function per section, built from doc blocks by index. `measure` writes plain pages for headless Chrome;
  `build` writes the 8 boards. Reads `blocks.json` (doc paragraphs, original numbering) and `assets.json`
  (`{slot: [/_blob url, width, height]}`), and `split_phone.json` / `split_desk.json` (from `../../scripts/split_boards.py`).
- `rebuild_blocks.py latest.json blocks.json`: after images are inserted into the doc, restores the original numbering
  and checks 28 anchor paragraphs.
- `allow.txt`: fragments intentionally not on the page, for `verify_boards.py --allow`.
- **Round 3 (2026-10-03):** the 365-day guarantee (`G_*` constants, `Build.seal`, `gcard`, `gline`, the FAQ item), the
  Lifetime wording and the 2026-10-01 live edits (`EDITS`, the note layout, the logo size). Canvas page
  "Round 3: guarantee" shows only the changed parts: `python3 gen.py build <root>/project split_r3`
  (`split_r3_phone.json`, `split_r3_desk.json`). `split_phone.json` / `split_desk.json` are still the whole page in 4 parts.

Rebuild from scratch (work folder with this folder's files and an empty sibling `root/project/`):

    python3 gen.py measure m
    bash ../../scripts/measure_sections.sh m/measure_phone.html m/h_phone.json
    bash ../../scripts/measure_sections.sh m/measure_desk.html m/h_desk.json
    python3 ../../scripts/split_boards.py split_config.json
    python3 gen.py build ../root/project
    python3 ../../scripts/verify_boards.py <latest blocks> "../root/project/R2-Letter*.dc.html" --assets assets.json --allow allow.txt --forbid "40-Year-Old" "Day 5"

(Adjust the relative script paths to wherever you copied the folder.)

**The live page (2026-09-30).** `build_live.py <repo>` writes `public/start.html` from the same sections: it renders
phone and desktop, turns every style that differs into a class (phone base, desktop in `@media (min-width: 900px)`),
makes board widths fluid, swaps in the real video, links and tracking (`tracking_head.html`), and applies Dan's build
decisions (both plan pickers cut, the FAQ note cut). Images: `assets_live.json` -> `public/img/letter/`. Proof:
`python3 verify_live.py <latest blocks> <repo>/public/start.html --allow allow_live.txt --forbid "Day 5" "_blob"`.
