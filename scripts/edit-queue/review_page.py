#!/usr/bin/env python3
"""Dan's morning review page for the overnight edit queue (handoff §6, first version: no frame picker yet).

  review_page.py serve     # http://127.0.0.1:8830  (launchd keeps it running)
  review_page.py build     # write a static snapshot (review-snapshot.html) without the buttons

The page only reads jobs.json, the scoreboard and the files each run left in its work directory. Dan's
verdict goes back through queue.py, with his exact words in the job note and on the scoreboard. It binds to
127.0.0.1 only and serves only the video files a run listed in its DELIVERY.json.
"""
import datetime, html, json, os, re, subprocess, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eq_common as eq                                          # noqa: E402
eq.unshadow()
q = eq.sibling("queue")
PORT = 8830
SNAPSHOT = os.path.join(eq.HERE, "review-snapshot.html")
SYSTEMIC = ["", "audio", "framing", "colour", "captions", "graphics", "cut/pacing"]
E = html.escape


def delivery(cfg, job_id):
    try:
        return json.load(open(os.path.join(eq.work_dir(cfg, job_id), "DELIVERY.json")))
    except Exception:
        return {}


def review_lines(cfg, job_id):
    """The newest reviewer report: its verdict and the two plain lines under it."""
    wd = eq.work_dir(cfg, job_id)
    try:
        names = sorted(n for n in os.listdir(wd) if re.match(r"QUEUE-REVIEW-\d+\.md$", n))
    except OSError:
        return "", []
    if not names:
        return "", []
    lines = [l.strip() for l in open(os.path.join(wd, names[-1]), errors="replace").read().splitlines() if l.strip()]
    return (lines[0] if lines else ""), [l for l in lines[1:] if not l.startswith(("#", "```"))][:2]


def allowed_media(cfg, data):
    ok = set()
    for j in data["jobs"]:
        d = delivery(cfg, j["id"])
        ok.update(p for p in (d.get("files") or []) + [d.get("review_copy")] if p)
    return ok


def summary_table(sb):
    rows = {}
    for r in sb["runs"]:
        s = rows.setdefault((r["executor"], r["group"]), {"runs": 0, "delivered": 0, "first_ship": 0, "reviewed": 0,
                                                          "approved": 0, "revised": 0, "hours": []})
        s["runs"] += 1
        s["delivered"] += r["outcome"] == "delivered"
        if r.get("reviewer_verdicts"):
            s["reviewed"] += 1
            s["first_ship"] += r["reviewer_verdicts"][0] == "SHIP"
        s["approved"] += r.get("dan_verdict") == "approved"
        s["revised"] += r.get("dan_verdict") in ("revise", "rejected")
        if r.get("wall_hours"):
            s["hours"].append(r["wall_hours"])
    if not rows:
        return "<p class=dim>No queue runs yet.</p>"
    out = ["<table><tr><th>who</th><th>group</th><th>runs</th><th>reached you</th><th>reviewer said SHIP first time</th>"
           "<th>you approved</th><th>you sent back</th><th>avg hours</th></tr>"]
    for (ex, g), s in sorted(rows.items()):
        avg = f"{sum(s['hours']) / len(s['hours']):.1f}" if s["hours"] else "–"
        out.append(f"<tr><td>{E(ex)}</td><td>{E(g)}</td><td>{s['runs']}</td><td>{s['delivered']}</td>"
                   f"<td>{s['first_ship']}/{s['reviewed']}</td><td>{s['approved']}</td><td>{s['revised']}</td><td>{avg}</td></tr>")
    return "".join(out) + "</table>"


def efficiency_line(run):
    usage = []
    for row in run.get("model_usage") or []:
        model = row.get("model") or "model unavailable"
        effort = row.get("effort") or "effort unavailable"
        if row.get("total_tokens") is not None:
            tokens = f"{row['total_tokens']:,} total tokens (split unavailable)"
        elif row.get("input_tokens") is None or row.get("output_tokens") is None:
            tokens = "tokens unavailable"
        else:
            tokens = f"{row['input_tokens']} in / {row['output_tokens']} out"
        usage.append(f"{row.get('role', 'session')}: {model}, {effort}, {tokens}")
    if not usage:
        usage.append("model usage unavailable (no session measurement was recorded)")
    costs = []
    for row in run.get("paid_provider_costs") or []:
        amount = f"${row['usd']:.2f}" if isinstance(row.get("usd"), (int, float)) else "cost unavailable"
        reason = f" ({row['reason']})" if row.get("usd") is None and row.get("reason") else ""
        costs.append(f"{row.get('provider', 'provider')}: {amount}{reason}")
    if not costs:
        costs.append("paid-provider costs unavailable (no per-video cost record was supplied)")
    return " · ".join(usage + costs)


def status_block(cfg, data, sb):
    d = eq.sibling("dispatcher")
    dec = d.decide(data, cfg, d.gather(cfg, data), sb)
    bits = []
    if os.path.exists(eq.PAUSE_FILE):
        bits.append("<p class=warn><b>PAUSED.</b> Running jobs finish; nothing new starts.</p>")
    for s in dec["stops"]:
        if not s.startswith("PAUSE"):
            bits.append(f"<p class=dim>Not launching: {E(s)}</p>")
    for w in dec["executor_stops"].values():
        bits.append(f"<p class=warn>{E(w)}</p>")
    for p in cfg.get("paused_groups", []):
        bits.append(f"<p class=warn>Group {E(p['group'])} is paused for {E(p['executor'])}: {E(p.get('reason', ''))}</p>")
    nxt = ", ".join(f"{j} ({ex})" for j, ex in dec.get("eligible", [])[:5]) or "nothing eligible"
    bits.append(f"<p class=dim>Next in line: {E(nxt)}</p>")
    return "".join(bits)


def render(static=False):
    cfg, data, sb = eq.load_config(), q.load(), eq.scoreboard_load()
    latest = {}
    for r in sb["runs"]:
        latest[r["job"]] = r
    waiting = [j for j in data["jobs"] if j["state"] in cfg["stop"]["review_queue_states"]]
    parked = [j for j in data["jobs"] if j["state"] in ("needs", "stalled") and j.get("queue_owned")]
    running = [j for j in data["jobs"] if j.get("claim") and j["state"] != "stalled"]
    waiting.sort(key=lambda j: (latest.get(j["id"], {}).get("ended") or j.get("updated", "")), reverse=True)

    def media(path):
        return ("file://" + quote(path)) if static else ("/media?p=" + quote(path, safe=""))

    cards = []
    for j in waiting:
        run, dl = latest.get(j["id"]), delivery(cfg, j["id"])
        verdict, lines = review_lines(cfg, j["id"])
        head = f"<h3>{E(j['id'])} · {E(j['title'])}</h3>"
        if not run:
            cards.append(f"<div class=card>{head}<p class=dim>Delivered by a hand-run session ({E(j.get('by', ''))}), not by the queue. "
                         f"It still counts toward your limit of {cfg['stop']['review_queue_limit']}. {E(j.get('note', ''))}</p></div>")
            continue
        vid = dl.get("review_copy") or (dl.get("files") or [None])[0]
        gate = dl.get("gate", "not reported")
        fails = "".join(f"<li>{E(x)}</li>" for x in dl.get("gate_failures") or [])
        form = "" if static else f"""
          <div class=form data-job="{E(j['id'])}">
            <textarea placeholder="Your words (dictate here). Required to send it back."></textarea>
            <label>If the problem would repeat on every video of this kind, what is it?
              <select>{''.join(f'<option value="{s}">{s or "not a repeating problem"}</option>' for s in SYSTEMIC)}</select></label>
            <button class=ok data-v=approved>Approve: this is final</button>
            <button data-v=revise>Send back for a revision</button>
            <button class=bad data-v=rejected>Reject</button><span class=msg></span>
          </div>"""
        cards.append(f"""<div class=card>{head}
          <p class=dim>{E(run['executor'])} edited · {E(str(run.get('reviewer')))} reviewed once · revision {run.get('revision_number', run.get('revision_rounds', 0))} · {run.get('wall_hours') or '?'} h</p>
          <p class=dim>{E(efficiency_line(run))}</p>
          {f'<video controls preload=metadata src="{media(vid)}"></video>' if vid else '<p class=warn>No review copy listed in DELIVERY.json.</p>'}
          <p>{E(dl.get('summary', ''))}</p>
          <p><b>Reviewer:</b> {E(verdict)}<br>{'<br>'.join(E(l) for l in lines)}</p>
          <p><b>Gate:</b> <span class="{'okc' if gate == 'PASS' else 'warn'}">{E(gate)}</span></p>{f'<ul>{fails}</ul>' if fails else ''}
          <p class=dim>Files: {'<br>'.join(E(f) for f in dl.get('files') or [])}</p>{form}</div>""")

    parked_html = "".join(f"<div class=card><h3>{E(j['id'])} · {E(j['title'])}</h3><p class=warn>{E(j['state'].upper())}</p>"
                          f"<p>{E(j.get('note', ''))}</p><p class=dim>Work folder: {E(eq.work_dir(cfg, j['id']))}</p></div>" for j in parked)
    running_html = "".join(f"<li>{E(j['id'])} · {E(j['title'])}: {E(j['claim']['by'])} since {E(j['claim']['started'][11:16])}, "
                           f"last heartbeat {E(j['claim']['heartbeat'][11:16])}</li>" for j in running)
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Edit Queue Review</title><style>
body{{font:15px/1.5 -apple-system,Helvetica,sans-serif;background:#111;color:#eee;margin:0;padding:24px 16px;max-width:860px;margin-inline:auto}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:16px;margin:28px 0 8px;border-bottom:2px solid #e11;padding-bottom:4px}} h3{{margin:0 0 4px;font-size:16px}}
.card{{background:#1c1c1c;border-radius:10px;padding:16px;margin:12px 0}} video{{width:100%;max-height:70vh;border-radius:8px;background:#000}}
.dim{{color:#999;font-size:13px}} .warn{{color:#ffb020}} .okc{{color:#4cd964}} table{{border-collapse:collapse;font-size:13px;display:block;overflow-x:auto}}
td,th{{border:1px solid #333;padding:4px 8px;text-align:left}} textarea{{width:100%;box-sizing:border-box;min-height:70px;background:#000;color:#eee;border:1px solid #444;border-radius:6px;padding:8px;font:inherit}}
label{{display:block;margin:8px 0;font-size:13px;color:#bbb}} select{{font:inherit}} button{{font:inherit;padding:8px 14px;margin:4px 6px 0 0;border-radius:6px;border:0;background:#444;color:#fff;cursor:pointer}}
button.ok{{background:#1a7f37}} button.bad{{background:#a1260d}} .msg{{margin-left:8px;color:#4cd964}}</style>
<h1>Edit Queue Review</h1><p class=dim>Built {datetime.datetime.now():%a %b %d, %H:%M}. {'Snapshot: open http://127.0.0.1:' + str(PORT) + ' for the buttons.' if static else ''}</p>
{status_block(cfg, data, sb)}
<h2>Waiting for you ({len(waiting)} of {cfg['stop']['review_queue_limit']})</h2>{''.join(cards) or '<p class=dim>Nothing to review.</p>'}
<h2>Parked: needs you ({len(parked)})</h2>{parked_html or '<p class=dim>Nothing parked.</p>'}
<h2>Running now</h2><ul>{running_html or '<li class=dim>No queue job is running.</li>'}</ul>
<h2>Scoreboard</h2>{summary_table(sb)}
<script>
document.querySelectorAll('.form button').forEach(b=>b.onclick=async()=>{{
  const f=b.closest('.form'),words=f.querySelector('textarea').value.trim(),v=b.dataset.v;
  if(v!=='approved'&&!words){{f.querySelector('.msg').textContent='Say what is wrong first.';return}}
  if(!confirm(v==='approved'?'Mark '+f.dataset.job+' FINAL?':'Send this verdict for '+f.dataset.job+'?'))return;
  const r=await fetch('/verdict',{{method:'POST',headers:{{'Content-Type':'application/json','X-Edit-Queue':'1'}},
    body:JSON.stringify({{job:f.dataset.job,verdict:v,words,systemic:f.querySelector('select').value}})}});
  f.querySelector('.msg').textContent=await r.text(); if(r.ok)setTimeout(()=>location.reload(),1200);
}});
</script>"""


def record_verdict(job_id, verdict, words, systemic):
    """Dan's decision, in his words. approved -> finalized; revise -> back in line as a revision round;
    rejected -> needs. A systemic reason trips the circuit breaker for that group and executor."""
    cfg = eq.load_config()
    run = eq.scoreboard_latest(job_id)
    if verdict not in ("approved", "revise", "rejected"):
        return False, "unknown verdict"
    if verdict != "approved" and not words:
        return False, "words required"
    today = datetime.date.today().isoformat()
    state = {"approved": "finalized", "revise": "ready", "rejected": "needs"}[verdict]
    note = {"approved": f"Dan approved on the review page {today}" + (f": \"{words}\"" if words else ""),
            "revise": f"Dan asked for a revision {today}: \"{words}\"",
            "rejected": f"Dan rejected {today}: \"{words}\""}[verdict]
    with q.locked():
        data = q.load(); j = q.find(data, job_id)
        if j["state"] not in cfg["stop"]["review_queue_states"]:
            return False, f"{job_id} is {j['state']}, not waiting for review"
        if verdict == "revise":
            prior_round = int((run or {}).get("revision_number", 0))
            approved = delivery(cfg, job_id).get("approved_elements") or []
            j["queue_revision"] = {"round": prior_round + 1, "words": words, "requested_changes": [words],
                                   "approved_elements": approved, "date": today}
        q.set_state(data, job_id, state, "Dan (review page)", note)
        q.save(data)
    q.master_status(job_id, q.STATES[state])
    q.push_drive(q.load())
    if run:
        eq.scoreboard_update(run["run_id"], dan_verdict=verdict, dan_words=words, systemic_reason=systemic or None,
                             corpus_entry="owed: the next session on this job records Dan's words in qc_corpus")
    if systemic and verdict != "approved" and run:
        cfg["paused_groups"].append({"group": eq.group_of(job_id), "executor": run["executor"], "date": today,
                                     "reason": f"{systemic}: \"{words[:120]}\" ({job_id})"})
        eq.save_config(cfg)
    return True, {"approved": "Marked final.", "revise": "Sent back; it goes to the front of the line.",
                  "rejected": "Rejected and parked."}[verdict] + (f" {eq.group_of(job_id)} jobs are paused for {run['executor']} until the cause is fixed." if systemic and verdict != "approved" and run else "")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        body = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            return self._send(200, render())
        if u.path == "/media":
            path = parse_qs(u.query).get("p", [""])[0]
            if path not in allowed_media(eq.load_config(), q.load()) or not os.path.isfile(path):
                return self._send(404, "not a delivered file")
            size = os.path.getsize(path)
            m = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
            start = int(m.group(1)) if m and m.group(1) else 0
            end = min(int(m.group(2)) if m and m.group(2) else size - 1, size - 1)
            self.send_response(206 if m else 200)
            self.send_header("Content-Type", "video/mp4"); self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1))
            if m:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.end_headers()
            with open(path, "rb") as f:
                f.seek(start); left = end - start + 1
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        return
                    left -= len(chunk)
            return
        self._send(404, "not found")

    def do_POST(self):
        if urlparse(self.path).path != "/verdict" or self.headers.get("X-Edit-Queue") != "1":
            return self._send(403, "forbidden")
        try:
            b = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            ok, msg = record_verdict(b["job"], b["verdict"], (b.get("words") or "").strip(), b.get("systemic") or "")
        except Exception as e:
            ok, msg = False, f"error: {e!s:.120}"
        self._send(200 if ok else 400, msg, "text/plain; charset=utf-8")


def build():
    with open(SNAPSHOT, "w") as f:
        f.write(render(static=True))
    return SNAPSHOT


if __name__ == "__main__":
    if sys.argv[1:] == ["build"]:
        print(build())
    elif sys.argv[1:] == ["serve"]:
        print(f"Edit Queue Review on http://127.0.0.1:{PORT}")
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    else:
        sys.exit(__doc__)
