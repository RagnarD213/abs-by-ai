#!/usr/bin/env python3
"""
Draft a piece as Dan, the way the bench scored best: real passages first, no rules, a clean writer.

WHY THIS EXISTS (2026-10-10, Dan Voice P2B): on the blind bench the only thing that made Claude harder to catch was
showing a fresh writer whole real passages of Dan's and nothing else (caught 82% of the time, against 91% with the
old guide). Adding voice notes to the same prompt put it back to 92%; a critic and checker revision pass changed
nothing. A session that has read thousands of words of writing rules is the losing condition. So the draft is
written by a separate, clean Claude call that sees only: 5 real passages chosen by format and length, Dan's own
wording for the piece if there is any, and the content plan. This script builds that prompt and makes the call.

    python3 scripts/voice/write.py --type content --format video --plan plan.md --words 320
    python3 scripts/voice/write.py --type ads --format ad-own --plan plan.md --his-words outline.txt --out draft.txt
    python3 scripts/voice/write.py --type content --format script --plan plan.md --words 900     # teleprompter script
    python3 scripts/voice/write.py --type conversion --format sales-script --plan plan.md --print-prompt

--plan       the content plan: what the piece is, who it is for, every point, fact and number in order, the ask.
             Content only. Do not put style instructions in it.
--his-words  Dan's own wording for this piece (his outline bullets, his notes, a dictated line). Used as the seed.
--format     see `bank.py`. `script` (content only) is a long-form teleprompter script: there is no long script
             wholly written by him to learn from, so the writer gets his written shorts and ads for the script
             register plus two video transcripts for his wording. That mix has not been scored on the bench.
--seed       any text; a different seed shows the writer different passages (use it for a second draft).
--print-prompt  print the prompt and stop: for a session with no `claude` command line, which then writes the
             piece itself from exactly this prompt, in a subagent that has read nothing else.

After the draft it runs the hard-rule check and prints the checker's score as a tripwire. It never revises.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import bench  # noqa: E402
import voice_check  # noqa: E402

N = 5
POSITION_NOTE = {"whole": "the whole piece", "opening": "the opening of a longer piece",
                 "middle": "the middle of a longer piece", "close": "the close of a longer piece"}


def passages(type_, fmt, words, seed, position):
    if fmt == "script":  # his written, read-aloud pieces for the register; two transcripts for his wording
        got = bank.pick("content", "video", words, 2, seed=seed)
        got += bank.pick("ads", "ad-own", words, 1, seed=seed)
        got += bank.pick("content", "short", words, 2, seed=seed)
        return got
    return bank.pick(type_, fmt, words, N, seed=seed, position=position)


def build(a):
    plan = open(a.plan, encoding="utf-8").read().strip()
    items = passages(a.type, a.format, a.words, a.seed, a.position)
    what = a.kind or ("a script for a YouTube video that Dan will read from a teleprompter" if a.format == "script"
                      else bank.FORMAT_NOTE[a.format])
    lead = bench.SET_LEAD.format(n=len(items), identity=bench.IDENTITY)
    seed = ""
    if a.his_words:
        his = open(a.his_words, encoding="utf-8").read().strip()
        seed = ("Dan's own words for this piece (his outline or notes). Keep his wording wherever it fits and build "
                f"out from it:\n<his_own_words>\n{his}\n</his_own_words>\n\n")
    script_note = ""
    if a.format == "script":
        script_note = ("The transcripts above show how he talks; the written pieces show how he writes for the "
                       "camera. Piece {n} is a script: his words and his directness, in order, with a line break "
                       "between thoughts.\n\n").format(n=len(items) + 1)
    return (f"{lead}\n\n{bank.show(items)}\n\n---\n\nNow piece {len(items) + 1}, the next piece in this set. Write it "
            f"as Dan Rose.\n\nWhat it is: {what}\nWhere in the piece: {POSITION_NOTE[a.position]}.\n"
            f"Length: about {a.words} words (stay within 10 percent).\n\n{seed}{script_note}"
            f"Content plan. Say all of it and add no new facts:\n{plan}\n\n"
            "Output only the piece itself: no title, no notes, no stage directions, no quotation marks around it.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", required=True, choices=["content", "ads", "conversion", "products"])
    ap.add_argument("--format", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--his-words")
    ap.add_argument("--words", type=int, default=300)
    ap.add_argument("--position", default="whole", choices=list(POSITION_NOTE))
    ap.add_argument("--kind", help="one line saying what the piece is, if the format's stock line does not fit")
    ap.add_argument("--seed", default="1")
    ap.add_argument("--model", default=bench.WRITER_MODEL)
    ap.add_argument("--out")
    ap.add_argument("--print-prompt", action="store_true")
    a = ap.parse_args()
    if a.format != "script" and a.format not in bank.FORMATS[a.type]:
        ap.error(f"--format for {a.type} is one of: {', '.join(bank.FORMATS[a.type])}" + (", script" if a.type == "content" else ""))
    prompt = build(a)
    if a.print_prompt:
        print(prompt)
        return 0
    draft = bench.claude_call(prompt, "You are a writer.", a.model)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(draft + "\n")
    print(draft)
    fmt = "video" if a.format == "script" else a.format
    _, hard, report = voice_check.report(draft, a.type, fmt)
    print("\n--- voice_check (a tripwire: fix hard fails; the rest is information, not a rewrite list) ---\n" + report,
          file=sys.stderr)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
