#!/usr/bin/env python3
"""
Training data for the Phase C pilot: a small open model fine-tuned on Dan's own text.

WHY THIS EXISTS (2026-10-16, Dan Voice P2C): prompting stalled at about 80% caught on the bench (Phase B). The plan's
Lane 3 trains a LoRA on an 8B open model with MLX on the Mac and scores it on the same bench. Each example is one
chunk of his real text (250 to 650 words) and, as the input, a content brief of it written with the bench's own
full-strength brief rule (`bench.BRIEF_PROMPT`), laid out exactly as the bench lays out a writing task
(`bench.task_lines`). So at test time the pilot gets the same kind of input as every other setup.

Rules:
- Pure piles only (tier 1 of each type). Never Claude's drafts, never other presenters' scripts.
- No file that holds a held-out passage, not even the rest of it, so the pilot cannot learn a test video's content.
- Targets get the bench's judging clean-up (`bench.for_judging`), the same form the judges see.
- Briefs come from Haiku 5.5 through the batch API (about $0.25 for the lot); the bench's own briefs are Opus.

Output: `voice-corpus/pilot/data/{train,valid}.jsonl` (chat format for `mlx_lm lora`) and `chunks.json`.
Run with the venv that has `anthropic`: `VOICE_BENCH_BACKEND=batch ~/.venvs/voice-pilot/bin/python scripts/voice/pilot_data.py`
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bench  # noqa: E402
import corpus  # noqa: E402

OUT = os.path.join(corpus.CORPUS, "pilot")
BRIEF_MODEL = "claude-haiku-5-5"
SYSTEM = "You write as Dan Rose. " + bench.IDENTITY


def chunks():
    held = {it["file"] for it in bench.load_index()}
    rng = random.Random(20261016)
    out = []
    for t in corpus.TYPES:
        for row, text in corpus.pile(t, 1):
            if row["file"] in held or row.get("authorship") == "dan-typed-lines-only":
                continue
            spoken = row.get("mode") == "spoken"
            us = bench.units(text, spoken)
            i = 0
            while i < len(us):
                target, j, words = rng.randint(280, 600), i, 0
                while j < len(us) and words < target:
                    words += corpus.count_words(text[us[j][0]:us[j][1]])
                    j += 1
                if words > 650 and j - 1 > i:  # one long last unit: stop before it
                    j -= 1
                    words = corpus.count_words(text[us[i][0]:us[j - 1][1]])
                if 250 <= words <= 650:
                    raw = text[us[i][0]:us[j - 1][1]]
                    pos = "opening" if i == 0 else ("close" if j == len(us) else "middle")
                    out.append({"key": f"{len(out):04d}", "type": t, "file": row["file"], "mode": row.get("mode"),
                                "position": pos, "words": words, "kind": bench.kind_of(row),
                                "text": bench.for_judging(raw, spoken)})
                i = j
    return out


def brief(c):
    path = os.path.join(OUT, "briefs", c["key"] + ".json")

    def make():
        d = bench.parse_json(bench.claude_call(bench.BRIEF_PROMPT.format(kind=c["kind"], passage=c["text"]),
                                               bench.BRIEF_SYS, BRIEF_MODEL))
        return json.dumps(d, indent=1)
    return c["key"], json.loads(bench.cached(path, make))


def main():
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    cs = chunks()
    with open(os.path.join(OUT, "chunks.json"), "w", encoding="utf-8") as fh:
        json.dump(cs, fh, indent=1)
    by = {}
    for c in cs:
        by[c["type"]] = by.get(c["type"], 0) + c["words"]
    print(f"{len(cs)} chunks; words by type: {by}", file=sys.stderr)
    got = {}
    bench.batched(lambda: got.update(dict(bench.pool(brief, cs))), "pilot briefs")
    rows = []
    for c in cs:
        b = got.get(c["key"])
        if not b or not b.get("usable") or not b.get("brief"):
            continue
        task = bench.task_lines({"kind": c["kind"], "position": c["position"], "words": c["words"], "brief": b["brief"]})
        user = (f"Write the following piece as Dan Rose.\n\n{task}\n\n"
                "Output only the piece itself: no title, no notes, no stage directions, no quotation marks around it.")
        rows.append({"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user},
                                  {"role": "assistant", "content": c["text"]}]})
    random.Random(7).shuffle(rows)
    nv = max(20, len(rows) // 20)
    for name, part in (("valid", rows[:nv]), ("train", rows[nv:])):
        with open(os.path.join(OUT, "data", name + ".jsonl"), "w", encoding="utf-8") as fh:
            for r in part:
                fh.write(json.dumps(r) + "\n")
    print(f"usable {len(rows)} of {len(cs)}: train {len(rows) - nv}, valid {nv}")


if __name__ == "__main__":
    main()
