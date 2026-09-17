#!/usr/bin/env python3
"""THE BLIND A/B PAGE. Two players side by side per pair, LABELS HIDDEN, ORDER RANDOMISED PER PAIR, the
mapping written to a sealed key.json the page never reads. One question per pair: which would you
publish, or is it a tie, and why in one line. Dan's words are saved verbatim to answers.json by the
loopback server, and go into the regression corpus whichever way it goes.

  python3 blind_page.py build --pairs pairs.json --out DIR [--seed N]
  python3 blind_page.py serve --dir DIR [--port 8830]

pairs.json: [{"id": "A", "title": "Ad 1 vertical", "files": {"kit": "/abs/path/kit.mp4", "approved": "/abs/path/approved.mp4"},
              "question": "Which would you publish?"}, ...]
The page shows every pair as "Left" / "Right" only. key.json (mode 0600, in the OUT dir, never linked
from the page) records which file sat where, with sha256 of the exact bytes served -- so his verdict
binds to the file he watched (the corpus entry needs that sha256).

Why the page and not our judgment: "The Muhammad Standard" -- every approval of our work came where the
design was fixed before the AI started; every rejection came where the AI invented the design. A session
grading its own kit is that failure mode again. Dan judges. Not us.
"""
import argparse
import hashlib
import html
import json
import os
import random
import shutil
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Blind review</title>
<style>
 body{font-family:-apple-system,Helvetica,Arial,sans-serif;background:#111;color:#eee;margin:0;padding:24px}
 h1{font-size:20px;margin:0 0 6px} p.lead{color:#aaa;margin:0 0 24px;max-width:900px}
 .pair{border:1px solid #333;border-radius:12px;padding:18px;margin:0 0 28px;background:#181818}
 .pair h2{font-size:17px;margin:0 0 12px} .players{display:flex;gap:18px;flex-wrap:wrap}
 .side{flex:1 1 380px;min-width:300px} .side h3{margin:0 0 8px;font-size:15px;color:#ccc}
 video{width:100%;background:#000;border-radius:8px;max-height:78vh}
 .q{margin-top:14px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
 label.pick{border:1px solid #444;border-radius:8px;padding:8px 12px;cursor:pointer}
 label.pick input{margin-right:6px} input.why{flex:1 1 320px;padding:9px;border-radius:8px;border:1px solid #444;background:#0d0d0d;color:#eee}
 button{padding:9px 16px;border-radius:8px;border:0;background:#8c995b;color:#111;font-weight:700;cursor:pointer}
 .saved{color:#8c995b;margin-left:10px} .hint{color:#777;font-size:12px;margin-top:6px}
</style></head><body>
<h1>Blind review — %(n)d pair%(s)s</h1>
<p class="lead">Each pair is two edits of the same ad. Nothing on this page says who made which; the order is random for every pair.
Watch both (sound on), then pick the one you would publish — or call it a tie — and say why in one line. Your words are saved as typed.</p>
%(pairs)s
<script>
async function save(id){
  const pick=(document.querySelector('input[name=pick_'+id+']:checked')||{}).value;
  const why=document.getElementById('why_'+id).value;
  if(!pick){alert('Pick Left, Right or Tie first');return;}
  const r=await fetch('/answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pair:id,pick:pick,why:why,when:new Date().toISOString()})});
  document.getElementById('saved_'+id).textContent = r.ok ? 'saved' : 'NOT saved';
}
</script></body></html>"""

PAIR = """<div class="pair"><h2>Pair %(id)s — %(title)s</h2>
<div class="players">
 <div class="side"><h3>Left</h3><video controls preload="metadata" src="%(left)s"></video></div>
 <div class="side"><h3>Right</h3><video controls preload="metadata" src="%(right)s"></video></div>
</div>
<div class="q">
 <label class="pick"><input type="radio" name="pick_%(id)s" value="left">Left</label>
 <label class="pick"><input type="radio" name="pick_%(id)s" value="right">Right</label>
 <label class="pick"><input type="radio" name="pick_%(id)s" value="tie">Tie</label>
 <input class="why" id="why_%(id)s" placeholder="%(question)s — why, in one line">
 <button onclick="save('%(id)s')">Save</button><span class="saved" id="saved_%(id)s"></span>
</div><div class="hint">%(hint)s</div></div>"""


def build(a):
    pairs = json.load(open(a.pairs))
    out = Path(a.out)
    (out / "media").mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed if a.seed is not None else time.time_ns())
    key, blocks = [], []
    for p in pairs:
        names = list(p["files"].keys())
        rng.shuffle(names)
        left, right = names[0], names[1]
        served = {}
        for side, name in (("left", left), ("right", right)):
            src = p["files"][name]
            if not os.path.exists(src):
                raise SystemExit(f"pair {p['id']}: {src} not on disk")
            dst = out / "media" / f"{p['id']}_{side}.mp4"
            if not dst.exists() or dst.stat().st_size != os.path.getsize(src):
                shutil.copy(src, dst)
            served[side] = dict(name=name, source=os.path.abspath(src), served=str(dst.relative_to(out)), sha256=sha256(dst))
        key.append(dict(pair=p["id"], title=p["title"], left=served["left"], right=served["right"]))
        blocks.append(PAIR % dict(id=html.escape(p["id"]), title=html.escape(p["title"]), left=f"media/{p['id']}_left.mp4",
                                  right=f"media/{p['id']}_right.mp4", question=html.escape(p.get("question", "Which would you publish?")),
                                  hint=html.escape(p.get("hint", ""))))
    (out / "index.html").write_text(PAGE % dict(n=len(pairs), s="" if len(pairs) == 1 else "s", pairs="\n".join(blocks)))
    kp = out / "key.json"
    json.dump(dict(sealed=time.strftime("%Y-%m-%dT%H:%M:%S%z"), seed=a.seed, pairs=key), open(kp, "w"), indent=1)
    os.chmod(kp, 0o600)
    print(f"{len(pairs)} pairs -> {out}/index.html ; key sealed in {kp} (never linked from the page)")


class Handler(SimpleHTTPRequestHandler):
    root = None

    def __init__(self, *args, **kwargs):
        self.byte_range = None
        super().__init__(*args, directory=str(self.root), **kwargs)

    def do_GET(self):
        if self.path.split("?")[0].endswith("key.json"):
            self.send_error(403, "sealed")
            return
        return super().do_GET()

    def do_POST(self):
        if self.path != "/answer":
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        p = Path(self.root) / "answers.json"
        cur = json.load(open(p)) if p.exists() else []
        cur.append(body)
        json.dump(cur, open(p, "w"), indent=1)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    # byte ranges so the players can seek (the Codex trial's review_server.py)
    def send_head(self):
        import re
        path = Path(self.translate_path(self.path))
        if not path.is_file() or not self.headers.get("Range"):
            return super().send_head()
        size = path.stat().st_size
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers["Range"])
        if not m:
            self.send_error(416)
            return None
        first, last = m.groups()
        start = int(first) if first else max(0, size - int(last))
        end = min(size - 1, int(last)) if first and last else size - 1
        if start > end or start >= size:
            self.send_error(416)
            return None
        f = path.open("rb")
        f.seek(start)
        self.byte_range = (start, end)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        return f

    def copyfile(self, source, output):
        if self.byte_range is None:
            return super().copyfile(source, output)
        remaining = self.byte_range[1] - self.byte_range[0] + 1
        try:
            while remaining:
                d = source.read(min(1 << 20, remaining))
                if not d:
                    break
                output.write(d)
                remaining -= len(d)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *args):
        pass


def serve(a):
    Handler.root = Path(a.dir).resolve()
    print(f"Blind review at http://127.0.0.1:{a.port}/index.html  (answers -> {Handler.root}/answers.json)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--pairs", required=True); b.add_argument("--out", required=True); b.add_argument("--seed", type=int)
    s = sub.add_parser("serve"); s.add_argument("--dir", required=True); s.add_argument("--port", type=int, default=8830)
    a = ap.parse_args()
    return dict(build=build, serve=serve)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
