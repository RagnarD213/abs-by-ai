#!/usr/bin/env python3
"""
The Phase C pilot writes the bench's 40 pieces with the fine-tuned local model.

WHY THIS EXISTS (2026-10-16, Dan Voice P2C): the bench needs the pilot's drafts in the same place and from the same
input as every other setup: the held-out brief, laid out by `bench.task_lines`. This writes them to
`voice-corpus/bench/<date>-<setup>/gen/`; then `bench.py run --setup <setup> --date <date>` judges and reports them.

    ~/.venvs/voice-pilot/bin/python scripts/voice/pilot_write.py --adapter /Volumes/Expansion/voice-pilot/adapters/r1 \\
        --date 2026-10-16

Runs on the Mac's GPU, free. The model is read from `~/.cache/voice-pilot/` (a copy of `/Volumes/Expansion/voice-pilot/models/`).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bench  # noqa: E402
import pilot_data  # noqa: E402

MODEL = os.path.expanduser("~/.cache/voice-pilot/llama31-8b-4bit")  # a copy of the Expansion download; much faster


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--setup", default="pilot")
    ap.add_argument("--temp", type=float, default=0.8)
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args()
    from mlx_lm import generate, load
    from mlx_lm.sample_utils import make_sampler
    model, tok = load(a.model, adapter_path=a.adapter)
    sampler = make_sampler(temp=a.temp, top_p=0.95)
    out = os.path.join(bench.run_dir(a.setup, a.date), "gen")
    os.makedirs(out, exist_ok=True)
    for it in bench.load_index():
        path = os.path.join(out, it["id"] + ".txt")
        if os.path.isfile(path) and os.path.getsize(path):
            continue
        user = (f"Write the following piece as Dan Rose.\n\n{bench.task_lines(it)}\n\n"
                "Output only the piece itself: no title, no notes, no stage directions, no quotation marks around it.")
        prompt = tok.apply_chat_template([{"role": "system", "content": pilot_data.SYSTEM},
                                          {"role": "user", "content": user}], add_generation_prompt=True)
        text = generate(model, tok, prompt, max_tokens=int(it["words"] * 2.2) + 80, sampler=sampler)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.strip())
        print(f"{it['id']}: {len(text.split())} words (asked {it['words']})", flush=True)


if __name__ == "__main__":
    main()
