# Worked example: "AI Got Me Abs at 40" (Round 2, approved 2026-09-30)

Canvas: https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, page Round 2 (private). Doc: `1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o`.
Asset session Drive folder: `1FullVwvuRxdbbaKhpy1_KLdAGLlG3XnC`.

- `gen.py`: one function per section, built from doc blocks by index. `measure` writes plain pages for headless Chrome;
  `build` writes the 8 boards. Reads `blocks.json` (doc paragraphs, original numbering) and `assets.json`
  (`{slot: [/_blob url, width, height]}`), and `split_phone.json` / `split_desk.json` (from `../../scripts/split_boards.py`).
- `rebuild_blocks.py latest.json blocks.json`: after images are inserted into the doc, restores the original numbering
  and checks 28 anchor paragraphs.
- `allow.txt`: fragments intentionally not on the page, for `verify_boards.py --allow`.

Rebuild from scratch (work folder with this folder's files and an empty sibling `root/project/`):

    python3 gen.py measure m
    bash ../../scripts/measure_sections.sh m/measure_phone.html m/h_phone.json
    bash ../../scripts/measure_sections.sh m/measure_desk.html m/h_desk.json
    python3 ../../scripts/split_boards.py split_config.json
    python3 gen.py build ../root/project
    python3 ../../scripts/verify_boards.py <latest blocks> "../root/project/R2-Letter*.dc.html" --assets assets.json --allow allow.txt --forbid "40-Year-Old" "Day 5"

(Adjust the relative script paths to wherever you copied the folder.)
