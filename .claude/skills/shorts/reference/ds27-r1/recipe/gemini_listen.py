#!/usr/bin/env python3
"""Send small review clips to Gemini with one question; print the answer and the token cost.
usage: gemini_listen.py PROMPT_FILE CLIP [CLIP ...]  (clips < 5 MB each, sent inline)"""
import sys, os, json, base64, re, urllib.request, urllib.error
key = None
for line in open(os.path.expanduser("~/.absbyai-secrets.env")):
    m = re.match(r'\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*["\']?([^"\'\s]+)', line)
    if m: key = m.group(1)
assert key, "no GEMINI_API_KEY"
model = os.environ.get("GM", "gemini-2.5-pro")
parts = [{"text": open(sys.argv[1]).read()}]
for p in sys.argv[2:]:
    parts.append({"text": f"Clip: {os.path.basename(p)}"})
    mime = "video/mp4" if p.endswith(".mp4") else "audio/wav"
    parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(open(p, "rb").read()).decode()}})
body = {"contents": [{"parts": parts}], "generationConfig": {"temperature": 0.2}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
try:
    r = json.load(urllib.request.urlopen(req, timeout=600))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:600].replace(key, "<k>")); sys.exit(1)
print("".join(x.get("text", "") for x in r["candidates"][0]["content"]["parts"]))
u = r.get("usageMetadata", {}); print("\nUSAGE", model, u.get("promptTokenCount"), u.get("candidatesTokenCount"), u.get("thoughtsTokenCount"))
