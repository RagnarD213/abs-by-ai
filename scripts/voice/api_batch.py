#!/usr/bin/env python3
"""
Claude calls for the voice scripts through the Message Batches API (half price), for when the `claude` command line
cannot log in.

WHY THIS EXISTS (2026-10-16, Dan Voice P2C step C0): the bench's calls go through the `claude` command line on Dan's
subscription. On 2026-10-16 its stored login had expired ("OAuth session expired and could not be refreshed") and only
Dan can log it back in. Rather than stop, the same calls go to the API with `ANTHROPIC_API_KEY` from
`~/.absbyai-secrets.env`, batched so they cost half the normal price.

How it works: with `VOICE_BENCH_BACKEND=batch`, `bench.claude_call` asks `call()` here. A finished answer is read from
`voice-corpus/bench/_api/done/`; a new one is recorded and `Pending` is raised, so the stage skips that item. `drive()`
reruns a stage until nothing is pending: each round sends every pending call as one batch, waits for it, and saves the
answers. Every stage in bench.py is already resumable, so no other logic changes.

Needs the `anthropic` package (Python 3.10+): `~/.venvs/voice-pilot/bin/python scripts/voice/bench.py ...`.
Settings: Opus 5.5 at effort high (Dan's routing default), adaptive thinking (always on for this model).
Spend is logged to `voice-corpus/bench/_api/usage.jsonl`; `python3 scripts/voice/api_batch.py` prints the total.
"""
import hashlib
import json
import os
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, "voice-corpus", "bench", "_api")
# batch prices, dollars per million tokens in / out (half the list price; checked 2026-10-16 in the claude-api skill)
PRICE = {"claude-opus-5-5": (2.0, 10.0), "claude-sonnet-5-5": (1.0, 5.0), "claude-fable-5-1": (5.0, 25.0),
         "claude-haiku-5-5": (0.05, 0.25)}
EFFORT = os.environ.get("VOICE_BENCH_EFFORT", "high")

_lock = threading.Lock()
PENDING = {}
FAILED = {}


class Pending(Exception):
    """The answer is not back yet. The caller skips this item; `drive()` sends it and reruns the stage."""


def key(prompt, system, model):
    return hashlib.sha256(json.dumps([model, system, prompt, EFFORT]).encode("utf-8")).hexdigest()[:32]


def call(prompt, system, model):
    k = key(prompt, system, model)
    done = os.path.join(CACHE, "done", k + ".txt")
    if os.path.isfile(done) and os.path.getsize(done):
        with open(done, encoding="utf-8") as fh:
            return fh.read()
    with _lock:
        if FAILED.get(k, 0) >= 3:
            raise RuntimeError("batch call failed 3 times: " + k)
        PENDING[k] = {"prompt": prompt, "system": system, "model": model}
    raise Pending(k)


def _secret(name):
    if os.environ.get(name):
        return os.environ[name]
    with open(os.path.expanduser("~/.absbyai-secrets.env"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(name + " not in ~/.absbyai-secrets.env")


def _send(jobs):
    import anthropic
    client = anthropic.Anthropic(api_key=_secret("ANTHROPIC_API_KEY"))
    reqs = [{"custom_id": k, "params": {"model": j["model"], "max_tokens": 16000, "system": j["system"],
                                         "output_config": {"effort": EFFORT},
                                         "messages": [{"role": "user", "content": j["prompt"]}]}}
            for k, j in jobs.items()]
    batch = client.messages.batches.create(requests=reqs)
    print(f"  batch {batch.id}: {len(reqs)} calls sent", file=sys.stderr)
    t0 = time.time()
    while True:
        b = client.messages.batches.retrieve(batch.id)
        if b.processing_status == "ended":
            break
        time.sleep(20)
    print(f"  batch {batch.id} ended after {round((time.time() - t0) / 60, 1)} min", file=sys.stderr)
    os.makedirs(os.path.join(CACHE, "done"), exist_ok=True)
    ok = bad = 0
    with open(os.path.join(CACHE, "usage.jsonl"), "a", encoding="utf-8") as log:
        for r in client.messages.batches.results(batch.id):
            k = r.custom_id
            if r.result.type == "succeeded":
                msg = r.result.message
                text = "".join(getattr(c, "text", "") for c in msg.content if c.type == "text").strip()
                u = msg.usage
                log.write(json.dumps({"batch": batch.id, "key": k, "model": msg.model, "in": u.input_tokens,
                                      "out": u.output_tokens, "stop": msg.stop_reason}) + "\n")
                if text and msg.stop_reason != "refusal":
                    with open(os.path.join(CACHE, "done", k + ".txt"), "w", encoding="utf-8") as fh:
                        fh.write(text)
                    ok += 1
                    continue
            bad += 1
            FAILED[k] = FAILED.get(k, 0) + 1
            print(f"  {k}: {r.result.type}" + (f" ({r.result.message.stop_reason})" if r.result.type == "succeeded" else ""),
                  file=sys.stderr)
    print(f"  saved {ok}, failed {bad}", file=sys.stderr)


def drive(stage, label="stage", rounds=8):
    """Run `stage()` until no call is pending. Each round sends what the last pass asked for."""
    for n in range(1, rounds + 1):
        PENDING.clear()
        stage()
        if not PENDING:
            return
        print(f"{label}: round {n}, {len(PENDING)} calls to send", file=sys.stderr)
        _send(dict(PENDING))
    PENDING.clear()
    stage()
    if PENDING:
        sys.exit(f"{label}: still {len(PENDING)} calls pending after {rounds} rounds")


def spend():
    total, n = 0.0, 0
    path = os.path.join(CACHE, "usage.jsonl")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                d = json.loads(line)
                pin, pout = PRICE.get(d["model"], PRICE["claude-opus-5-5"])
                total += (d["in"] * pin + d["out"] * pout) / 1e6
                n += 1
    return total, n


if __name__ == "__main__":
    t, n = spend()
    print(f"{n} batch calls, ${t:.2f}")
