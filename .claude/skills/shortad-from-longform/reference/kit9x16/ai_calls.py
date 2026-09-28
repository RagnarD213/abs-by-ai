#!/usr/bin/env python3
"""The kit's ONLY door to a model: small, narrow, logged calls with a pluggable provider.

Every call appends one line to <ledger> (JSONL): when, what, provider, model, tokens in/out, cost in USD, and the
answer. `kit_run.py` totals the ledger into run_report.json. No other kit script talks to a model.

Providers:
  gemini   Google Generative Language REST API, key GEMINI_API_KEY (env, ~/.absbyai-secrets.env or bakeoff/.env).
           Quality review is standing-authorized by Dan under $5 per run (AGENTS.md).
  none     no model: every leftover escalates. The default for a dry run.
  (local)  an Ollama / LM Studio OpenAI-compatible endpoint can be added as another class with the same three
           methods; nothing else changes.

Calls (the three the handoff allows, and no others):
  classify_picture(image, question)  leftover classification: pick a kind from a fixed menu, or "real or AI"
  judge(images, prompt)              the watch pass judge (watch/JUDGE_PROMPT.md format)
  text(prompt)                       the <=0:59 cutdown sentence ranges over the transcript
"""
import base64
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

# USD per 1M tokens (input, output). Google AI pricing pages, paid tier, checked 2026-09-28. Output includes thinking.
PRICES = {
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.5-flash-lite": (0.10, 0.40),
    "gemini-2.5-pro": (1.25, 10.00),          # prompts <= 200k tokens
    "gemini-2.5-pro>200k": (2.50, 15.00),
}


def _key():
    k = os.environ.get("GEMINI_API_KEY")
    if k:
        return k
    for p in (os.path.expanduser("~/.absbyai-secrets.env"), os.path.join(REPO, "bakeoff/.env"),
              "/Users/danielrose/Documents/Claude/Projects/Abs By AI/bakeoff/.env"):
        if os.path.exists(p):
            for line in open(p):
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("GEMINI_API_KEY not found (env, ~/.absbyai-secrets.env, bakeoff/.env)")


def cost_of(model, tin, tout):
    key = model
    if model == "gemini-2.5-pro" and tin > 200_000:
        key = "gemini-2.5-pro>200k"
    pin, pout = PRICES.get(key, PRICES["gemini-2.5-pro"])      # unknown model: price it as the dearest we use
    return round(tin / 1e6 * pin + tout / 1e6 * pout, 6)


class Ledger:
    def __init__(self, path):
        self.path = path
        if path:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    def add(self, **row):
        row["when"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        if self.path:
            with open(self.path, "a") as f:
                f.write(json.dumps(row) + "\n")
        return row

    def total(self):
        if not self.path or not os.path.exists(self.path):
            return dict(calls=0, usd=0.0)
        rows = [json.loads(l) for l in open(self.path) if l.strip()]
        return dict(calls=len(rows), usd=round(sum(r.get("usd", 0.0) for r in rows), 4),
                    by_purpose={p: round(sum(r.get("usd", 0.0) for r in rows if r.get("purpose") == p), 4)
                                for p in sorted({r.get("purpose") for r in rows})})


def _img_part(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(ext, "image/png")
    return {"inline_data": {"mime_type": mime, "data": base64.b64encode(open(path, "rb").read()).decode()}}


class Gemini:
    name = "gemini"

    def __init__(self, ledger, model_small="gemini-2.5-flash", model_judge="gemini-2.5-pro"):
        self.ledger, self.model_small, self.model_judge = ledger, model_small, model_judge
        self.key = _key()

    def _call(self, model, parts, purpose, json_out=True, max_tokens=8192, temperature=0.0):
        body = {"contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}}
        if json_out:
            body["generationConfig"]["responseMimeType"] = "application/json"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.key}"
        last = None
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=600) as r:
                    d = json.loads(r.read())
                break
            except Exception as e:                                   # 429/5xx: back off and retry
                last = e
                time.sleep(5 * (attempt + 1))
        else:
            self.ledger.add(purpose=purpose, provider=self.name, model=model, error=str(last)[:300], usd=0.0)
            raise RuntimeError(f"gemini {model} failed: {last}")
        u = d.get("usageMetadata", {})
        tin = int(u.get("promptTokenCount", 0))
        tout = int(u.get("candidatesTokenCount", 0)) + int(u.get("thoughtsTokenCount", 0))
        txt = "".join(p.get("text", "") for c in d.get("candidates", [])[:1] for p in c.get("content", {}).get("parts", []))
        usd = cost_of(model, tin, tout)
        self.ledger.add(purpose=purpose, provider=self.name, model=model, tokens_in=tin, tokens_out=tout, usd=usd,
                        answer=txt[:2000])
        return json.loads(txt) if json_out else txt

    def classify_picture(self, image, question, choices, purpose="leftover"):
        prompt = (f"{question}\nAnswer with JSON: {{\"answer\": one of {json.dumps(choices)}, \"confidence\": 0..1, "
                  f"\"why\": short reason}}. If you are not sure, say so with a low confidence.")
        return self._call(self.model_small, [_img_part(image), {"text": prompt}], purpose)

    def judge(self, images, prompt, purpose="judge", model=None):
        parts = []
        for p in images:
            parts.append({"text": f"IMAGE FILE: {os.path.basename(p)}"})
            parts.append(_img_part(p))
        parts.append({"text": prompt})
        return self._call(model or self.model_judge, parts, purpose, max_tokens=32768)

    def text(self, prompt, purpose="cutdown", model=None):
        return self._call(model or self.model_small, [{"text": prompt}], purpose)


class NoModel:
    name = "none"

    def __init__(self, ledger, **_):
        self.ledger = ledger

    def classify_picture(self, *a, **k):
        return None

    def judge(self, *a, **k):
        raise SystemExit("no model provider: the judged watch pass needs --ai gemini (or fresh session judges)")

    def text(self, *a, **k):
        return None


def provider(name, ledger_path):
    led = Ledger(ledger_path)
    if name in (None, "", "none"):
        return NoModel(led)
    if name == "gemini":
        return Gemini(led)
    raise SystemExit(f"unknown AI provider {name!r} (gemini | none)")
