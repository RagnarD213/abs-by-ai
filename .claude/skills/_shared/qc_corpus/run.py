#!/usr/bin/env python3
"""THE REGRESSION CORPUS. Every file Dan rejected, and every file he approved, with his own words.

  python3 run.py                    the audio selftest, then every gate we have over every entry
  python3 run.py --no-selftest      skip the selftest (it takes ~90 s and needs the Extreme SSD)
  python3 run.py --id website-rev3  one entry
  python3 run.py --fingerprint      re-record sha256 for every entry (after a deliberate re-render)
  python3 run.py --extract          build the excerpt cache (git-ignored; regenerable from the master)
  python3 run.py --strict-pending   also fail when a must_trigger names a check nothing implements yet

THE RULE (AGENTS.md, 2026-09-09):
    NO GATE OR SETTING CHANGE SHIPS UNLESS run.py PASSES.
    It must FAIL every rejected file and PASS every approved one.

WHY. Every gate we own was built backwards from the last rejection, so each new failure shipped
exactly once and the gate that caught it was never proven against the others. Twice that produced a
gate that scored a REJECTED build as better than an approved one:

  * 2026-09-02, audio: `edt`, `dryness` and `floor` all improve as suppression increases, so the
    build Dan called "underwater" beat the build he approved on every row the gate had.
  * 2026-09-08, framing: rev 3's own headroom gate PASSED rev 3 at 21-95 px, because its detector
    read the hairline 90 px inside his hair. Dan: "basically not usable."

Both are in the corpus now. A gate change that resurrects either one cannot ship.

TWO FAILURE MODES, REPORTED SEPARATELY -- they mean opposite things:

  * BLIND     a rejected file now PASSES -> the gate cannot see something Dan rejected on.
              Never fix this by relaxing anything. Add the row that sees it.
  * OVERTIGHT an approved file now FAILS -> the gate will block good work.
              ⚠ Read it before relaxing: the 09-09 do-no-harm row "over-tightened" onto 16 of 16
              shipped Shorts and was CORRECT. An OVERTIGHT that names a file Dan actually praised
              is a bug in the gate; one that names a file that shipped without him seeing it is a
              finding about the file.
  * GAP       an entry records a `known_gap`: one named check, on one named file, that is known to
              fail for a reason written down and dated, with the condition that clears it. Printed
              EVERY run, counted, and never inherited by any other check on that file -- if a
              different row fails, it is still a MISMATCH. ⚠ THIS IS NOT A BYPASS AND MUST NOT
              BECOME ONE: a gap names one check on one file, carries Dan-visible reasoning, and
              run.py tells you the moment it HEALS so you delete it. If you find yourself adding a
              gap to make a change ship, you are relaxing a bound -- stop.
  * PENDING   a must_trigger names a check that does not exist yet (Phases 1-6 build them).
              Counted and printed, never silently dropped, but does not fail the run until
              --strict-pending. ⚠ A PENDING is NOT a pass: it is a rejection nothing can catch.

⚠ NEVER RAISE A THRESHOLD TO MAKE AN ENTRY PASS (memory: audio-never-over-strip). If a corpus entry
fails a bound, that is the finding.
⚠ NEVER COMMIT A MASTER. The repo is public (memory: repo-is-public). corpus.json holds the path and
the sha256; excerpts live in the git-ignored cache and regenerate from the master with --extract.
"""
import argparse, hashlib, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SHARED_AUDIO = os.path.join(REPO, ".claude/skills/_shared/audio")
SHARED_DELIVER = os.path.join(REPO, ".claude/skills/_shared/deliver")
GATE = os.path.join(SHARED_AUDIO, "audio_gate.py")
DGATE = os.path.join(SHARED_DELIVER, "gate.py")
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
CORPUS = os.path.join(HERE, "corpus.json")
CACHE = os.path.join(HERE, "excerpts")

# ---------------------------------------------------------------- the checks this runner can run.
# ⚠ ONE ENTRY PER CHECK, and the value is what RUNS it. A check with no runner is PENDING, printed
# as such, and is the queue for Phases 1-6. Do NOT delete a must_trigger to make the run green.
IMPLEMENTED = {
    # audio_gate rows -- the row keys audio_gate.py emits
    "audio_gate": "audio_gate",
    "audio_gate:lr_corr": "audio_gate", "audio_gate:comb": "audio_gate",
    "audio_gate:edt": "audio_gate", "audio_gate:tone": "audio_gate",
    "audio_gate:floor": "audio_gate", "audio_gate:dryness": "audio_gate",
    "audio_gate:lufs": "audio_gate", "audio_gate:spread": "audio_gate",
    "audio_gate:tp": "audio_gate", "audio_gate:silence": "audio_gate",
    "audio_gate:length": "audio_gate", "audio_gate:artifacts": "audio_gate",
    "audio_gate:do_no_harm": "audio_gate", "audio_gate:reference_rows": "audio_gate",
    # --reference-mix --verbatim (2026-09-10): the editor's mix, untouched
    "audio_gate:provenance": "audio_gate", "audio_gate:verbatim_level": "audio_gate",
    "audio_gate:verbatim_image": "audio_gate", "audio_gate:verbatim_lufs": "audio_gate",
    # _shared/deliver/gate.py rows (2026-09-11, Phase 1). The value is the runner; the entry says
    # which FORMAT to grade against in its "deliver" block, because one pinned reference cannot
    # grade every programme -- a trust video holds on Dan's face on purpose and a longform does not.
    "style:coverage": "deliver_gate", "style:static_run": "deliver_gate",
    "cut:uncovered_joins": "deliver_gate",
    # Phase 2 (2026-09-12): the portable framing tracker (checks/framing.py) and the banned-screen
    # row's stage 3 (the screen's own signature inside the box the chrome located).
    "framing:hair_top": "deliver_gate", "framing:headroom": "deliver_gate",
    "framing:centering": "deliver_gate", "framing:no_wide_level": "deliver_gate",
    "framing:push_coverage": "deliver_gate",
    "compliance:banned_screen": "deliver_gate",
}
# Row key by human name, so an entry can name either.
ROWKEY = {"one voice": "lr_corr", "no comb": "comb", "dry room": "edt", "tone": "tone",
          "clean between words": "floor", "words stop cleanly": "dryness", "loudness": "lufs",
          "not crushed": "spread", "no clipping": "tp", "nothing missing": "silence",
          "no processing damage": "artifacts", "do no harm": "do_no_harm", "audio": "length",
          "reference mix": "provenance", "verbatim level": "verbatim_level",
          "verbatim image": "verbatim_image", "verbatim loudness": "verbatim_lufs"}

# Phases that will implement the rest. Printed with each PENDING so the queue is legible.
PENDING_OWNER = {
    "cut:": "nothing implements this yet -- VQC-C phase 4 (pose-matched picture cuts)",
    "junk:": "nothing implements this yet -- handoff-20260911-junk-footage-pass.md",
    "style:": "nothing implements this yet -- Phase 1 (_shared/deliver)",
    "captions:": "nothing implements this yet -- Phase 1 (_shared/deliver)",
    "compliance:": "nothing implements this yet -- Phase 1 (_shared/deliver)",
    "music:": "nothing implements this yet -- VQC-C phase 4 (grade + bed vs his ranges)",
}

# ⚠ ONE PHASE-1 ROW IS BUILT BUT DELIBERATELY NOT REGISTERED, and this is the honest reason.
# `captions:graphic_clearance` EXISTS in _shared/deliver/checks/captions.py and runs on every future
# delivery: it renders each cue over green for its true ink bbox and compares that against the
# graphic's own alpha -- the measurement that caught website rev 2. It cannot be PROVEN against
# corpus entry `website-rev2`, because that build's plan (tight_cuts.json, cap.ass, gfx/*.mov) is
# not on disk: it lived in Media/, which is gitignored. Registering it would turn a NOT MEASURED
# into a green must_trigger, which is exactly the lie this file exists to prevent. Four delivered-
# pixel substitutes were tried and measured on 2026-09-11 and none separated rev 2 from rev 4 --
# they could not tell a caption from a phone screen recording's on-screen keyboard, from B-roll
# texture behind a locked-off camera, or from the two halves of one caption line split at a word
# space ("goal physique." alone read as two blocks 44 px apart). It clears the first time a
# delivery carries both the defect and its plan.
# `compliance:banned_screen` was registered 2026-09-12 (Phase 2 item 0). Its stage 3 -- the screen's
# own signature inside the phone box the chrome located: L/R pairing of the photo band for a
# before/after screen, a higher chrome bound for the single-photo email-capture screen -- separates
# the real violation from approved rev 4's macro screen with the margins recorded in
# _shared/deliver/formats.py `_BANNED`. It also found the email-capture screen in Muhammad's Ad 2
# master at 3:12 and 3:23 (a reference entry here; reported, not registered as a must_trigger).
PENDING_OWNER["captions:graphic_clearance"] = (
    "BUILT in Phase 1 (_shared/deliver/checks/captions.py) and running on every future delivery, "
    "but it needs the build's cap.ass + gfx MOVs and rev 2's are not on disk")


def sha256(p, cap=None):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 22)
            if not b: break
            h.update(b)
    return h.hexdigest()


def resolve(e, corpus):
    root = corpus["roots"][e.get("root", "repo")]
    base = REPO if root == "." else root
    return os.path.join(base, e["path"])


def run_deliver_gate(path, fmt, rows, plan=None):
    """Run _shared/deliver/gate.py for just these rows. --row implies a partial run: it never
    stamps, so the corpus cannot change a file's delivery state by measuring it."""
    import tempfile
    out = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
    cmd = ["python3", DGATE, path, "--format", fmt, "--no-stamp", "--json", out]
    if plan:
        cmd += ["--plan", plan]
    for r in rows:
        cmd += ["--row", r]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
    try:
        d = json.load(open(out))
    except Exception:
        return {}, p.stdout + p.stderr
    finally:
        try: os.unlink(out)
        except OSError: pass
    return {r["key"]: r for r in d["rows"]}, p.stdout + p.stderr


def run_audio_gate(path, extra=()):
    """--no-stamp always: the corpus MEASURES, it never changes a file's delivery state."""
    r = subprocess.run(["python3", GATE, path, "--no-stamp", *extra],
                       capture_output=True, text=True, timeout=3600)
    out = r.stdout + r.stderr
    rows = {}
    for line in out.splitlines():
        s = line.strip()
        for tag, ok in (("PASS  ", True), ("FAIL  ", False), ("info  ", None)):
            if s.startswith(tag):
                text = s[6:]
                name = text.split(":")[0].strip()
                rows[ROWKEY.get(name, name)] = ok
                break
    return r.returncode == 0, rows, out


def check_entry(e, corpus, strict_pending):
    p = resolve(e, corpus)
    res = dict(id=e["id"], verdict=e["verdict"], path=p, results=[], pending=[], state="ok")
    if not os.path.exists(p):
        vol = corpus["roots"].get(e.get("root", "repo"), "")
        res["state"] = "UNAVAILABLE"
        res["why"] = (f"not on disk: {p}" +
                      ("   (the Extreme SSD is not mounted)" if vol.startswith("/Volumes") and
                       not os.path.isdir(vol.split("/_edit_work")[0]) else ""))
        return res
    have = sha256(p)
    if e.get("sha256") and e["sha256"] != have:
        res["state"] = "CHANGED"
        res["why"] = (f"sha256 differs from the corpus record -- this is not the file Dan judged. "
                      f"Recorded {e['sha256'][:12]}, on disk {have[:12]}. "
                      f"Re-run with --fingerprint ONLY if the change was deliberate.")
        return res
    res["sha256"] = have

    # ⚠ Read the gaps FIRST: "audio_gate" means "no row fails", and a row excused by a dated,
    # written-down known_gap must not drag the whole-gate result down with it.
    gaps = {g["check"]: g for g in e.get("known_gap", [])}
    gapped_rows = {c.split(":", 1)[1] for c in gaps if c.startswith("audio_gate:")}
    wants = list(e.get("must_trigger", [])) + [f"+{c}" for c in e.get("must_pass", [])]
    audio_needed = any(w.lstrip("+").startswith("audio_gate") for w in wants)
    gate_ok, rows, log = (None, {}, "")
    if audio_needed:
        extra = ["--reference-rows-only"] if e["verdict"] == "reference" else []
        # per-entry gate arguments (2026-09-10): a {root, path} item resolves like the entry's own path, so an entry
        # can name the editor's mix its audio must equal (--reference-mix <his export> --verbatim)
        for x in e.get("gate_args", []):
            extra.append(resolve(x, corpus) if isinstance(x, dict) else x)
        gate_ok, rows, log = run_audio_gate(p, extra)
        res["gate"] = "PASS" if gate_ok else "FAIL"
        res["failing_rows"] = sorted(k for k, v in rows.items() if v is False)

    # ---- the delivery gate, for the rows it owns
    dneed = sorted({w.lstrip("+") for w in wants
                    if IMPLEMENTED.get(w.lstrip("+")) == "deliver_gate"})
    drows = {}
    if dneed:
        dcfg = e.get("deliver")
        if not dcfg or not dcfg.get("format"):
            # ⚠ NOT a skip. An entry that asks for a delivery-gate row without saying which format
            # to grade it against cannot be measured, and an unmeasured check is a FAILURE.
            res["state"] = "UNGRADED"
            res["why"] = (f"{', '.join(dneed)} need a \"deliver\": {{\"format\": ...}} block on "
                          f"this entry -- the bound is per format and nothing can pick one for it")
            return res
        dplan = dcfg.get("plan")
        if dplan and not os.path.isabs(dplan):
            dplan = os.path.join(HERE, dplan)
        drows, dlog = run_deliver_gate(p, dcfg["format"], dneed, dplan)
        res["deliver_failing"] = sorted(k for k, v in drows.items() if v.get("ok") is False)
        res["deliver_unmeasured"] = sorted(k for k, v in drows.items() if v.get("ok") is None)

    for w in wants:
        must_pass = w.startswith("+")
        c = w.lstrip("+")
        if c not in IMPLEMENTED:
            owner = PENDING_OWNER.get(c) or next(
                (v for k, v in PENDING_OWNER.items() if c.startswith(k)), "unassigned")
            res["pending"].append(dict(check=c, owner=owner, must_pass=must_pass))
            continue
        if IMPLEMENTED.get(c) == "deliver_gate":
            d = drows.get(c)
            # ⚠ A ROW THAT DID NOT RUN IS NOT A PASS AND NOT A FAIL -- it is a MISMATCH, reported
            # here rather than counted as whichever the entry happened to want.
            if d is None or d.get("ok") is None:
                res["results"].append(dict(
                    check=c, want="PASS" if must_pass else "FAIL", got="NOT MEASURED", ok=False,
                    why=(d or {}).get("detail", "the delivery gate returned nothing for this row")))
                continue
            got = bool(d["ok"])
        elif c == "audio_gate":                     # the whole gate = no row fails
            failing = {k for k, v in rows.items() if v is False} - gapped_rows
            got = bool(gate_ok) or not failing
        else:                                       # one named row
            key = c.split(":", 1)[1]
            if key == "reference_rows": got = bool(gate_ok)
            else: got = rows.get(key) is not False   # True or info(None) = did not fail
        want = True if must_pass else False          # must_trigger = the check must FAIL the file
        res["results"].append(dict(check=c, want="PASS" if want else "FAIL",
                                   got="PASS" if got else "FAIL", ok=(got == want)))

    # ⚠ A known_gap excuses exactly ONE named check on THIS file, and only while it still fails.
    for g in gaps.values():
        row = g["check"].split(":", 1)[1] if g["check"].startswith("audio_gate:") else None
        if row and rows.get(row) is False:
            res.setdefault("gaps", []).append(f"{g['check']}: {g['why']}")
        elif row and row in rows:
            res.setdefault("healed", []).append(
                f"{g['check']} now passes -- DELETE its known_gap from corpus.json ({g['clears_when']})")
    for r in res["results"]:
        if r["ok"] or r["check"] not in gaps: continue
        g = gaps[r["check"]]
        r["ok"] = True; r["gap"] = True
        res.setdefault("gaps", []).append(f"{r['check']}: {g['why']}")
    # ...and a gap that no longer fails is stale: say so, loudly, so it gets deleted.
    for r in res["results"]:
        if r["check"] in gaps and not r.get("gap"):
            res.setdefault("healed", []).append(
                f"{r['check']} now behaves -- DELETE its known_gap from corpus.json "
                f"({gaps[r['check']]['clears_when']})")
    bad = [r for r in res["results"] if not r["ok"]]
    if bad:
        res["state"] = "BLIND" if e["verdict"] == "rejected" and any(
            r["want"] == "FAIL" for r in bad) else "OVERTIGHT"
        res["why"] = "; ".join(f"{r['check']} wanted {r['want']}, got {r['got']}" for r in bad)
    elif res.get("healed"):
        res["state"] = "STALE-GAP"; res["why"] = "; ".join(res["healed"])
    elif res.get("gaps"):
        res["state"] = "GAP"; res["why"] = "; ".join(res["gaps"])
    elif res["pending"] and strict_pending:
        res["state"] = "PENDING"
        res["why"] = "; ".join(f"{q['check']} ({q['owner']})" for q in res["pending"])
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", action="append", help="only these entries")
    ap.add_argument("--fingerprint", action="store_true", help="re-record sha256 for every entry")
    ap.add_argument("--extract", action="store_true", help="build the git-ignored excerpt cache")
    ap.add_argument("--strict-pending", action="store_true",
                    help="a must_trigger with no implementation fails the run (turn this on as the phases land)")
    ap.add_argument("--json", help="write the full result to this path")
    ap.add_argument("--no-selftest", action="store_true",
                    help="skip _shared/audio/selftest.sh (~90 s, needs the Extreme SSD mounted)")
    A = ap.parse_args()
    corpus = json.load(open(CORPUS))
    entries = [e for e in corpus["entries"] if not A.id or e["id"] in A.id]

    if A.fingerprint:
        for e in entries:
            p = resolve(e, corpus)
            if os.path.exists(p):
                e["sha256"] = sha256(p); e["bytes"] = os.path.getsize(p)
                print(f"  {e['id']:28s} {e['sha256'][:16]}  {e['bytes']/1e6:8.1f} MB")
            else:
                print(f"  {e['id']:28s} NOT ON DISK -- left as recorded")
        json.dump(corpus, open(CORPUS, "w"), indent=1)
        print(f"\nfingerprints written to {CORPUS}"); return 0

    if A.extract:
        os.makedirs(CACHE, exist_ok=True)
        for e in entries:
            p = resolve(e, corpus)
            if not os.path.exists(p): print(f"  {e['id']:28s} skipped (not on disk)"); continue
            ss, t = e.get("excerpt", [0, 30])
            o = os.path.join(CACHE, f"{e['id']}.mp4")
            subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", str(ss), "-t", str(t),
                            "-i", p, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                            "-c:a", "aac", "-b:a", "192k", o], check=True)
            print(f"  {e['id']:28s} -> excerpts/{e['id']}.mp4  ({ss}s +{t}s)")
        print("\n⚠ the cache is git-ignored and regenerable; the master is never committed."); return 0

    # ---- the audio selftest is step 0. It is the working ancestor of this whole idea (PASS on the
    # approved website rev 2, FAIL on the rejected rev 1) and it proves the MODULE still measures what
    # it claims before the corpus asks it about specific files. A broken module makes every corpus
    # result meaningless, so it runs first and a failure stops the run.
    selftest_ok = None
    if not A.no_selftest and not A.id:
        st = os.path.join(SHARED_AUDIO, "selftest.sh")
        print("_shared/audio/selftest.sh ...", flush=True)
        r = subprocess.run(["zsh", st], capture_output=True, text=True, cwd=SHARED_AUDIO)
        selftest_ok = r.returncode == 0
        tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1:]
        print(f"  {'PASS' if selftest_ok else 'FAIL'}  {tail[0].strip() if tail else ''}")
        if not selftest_ok:
            for l in (r.stdout + r.stderr).splitlines():
                if "✗" in l: print("   " + l.strip())
            print("\nCORPUS FAIL -- the audio module's own selftest is failing; fix that first.")
            return 1
    print(f"\nQC CORPUS  {len(entries)} entries  (corpus v{corpus['version']}, {corpus['updated']})\n")
    out, t0 = [], time.time()
    for e in entries:
        r = check_entry(e, corpus, A.strict_pending)
        out.append(r)
        tag = {"ok": "  ok  ", "BLIND": " BLIND", "OVERTIGHT": " TIGHT", "PENDING": "  ...  ",
               "GAP": " gap  ", "STALE-GAP": "STALE!", "UNAVAILABLE": " ---- ",
               "UNGRADED": "UNGRAD", "CHANGED": "CHANGED"}[r["state"]]
        print(f"[{tag}] {r['id']:28s} {r['verdict']:20s} {r.get('gate', ''):5s}")
        if r.get("failing_rows"): print(f"           audio rows failing: {', '.join(r['failing_rows'])}")
        if r.get("deliver_failing"): print(f"           delivery rows failing: {', '.join(r['deliver_failing'])}")
        if r.get("deliver_unmeasured"): print(f"           delivery rows NOT MEASURED: {', '.join(r['deliver_unmeasured'])}")
        if r.get("why"): print(f"           {r['why']}")
        for q in r["pending"]:
            print(f"           PENDING  {q['check']:28s} {q['owner']}")

    mism = [r for r in out if r["state"] in ("BLIND", "OVERTIGHT", "CHANGED", "PENDING",
                                            "STALE-GAP", "UNGRADED")]
    unav = [r for r in out if r["state"] == "UNAVAILABLE"]
    gapd = [r for r in out if r["state"] == "GAP"]
    pend = sorted({q["check"] for r in out for q in r["pending"]})
    print(f"\n{len(out)-len(mism)-len(unav)}/{len(out)} as expected"
          f"{f' ({len(gapd)} carrying a recorded known_gap)' if gapd else ''}"
          f"{f', {len(unav)} not on disk' if unav else ''}"
          f"{f', {len(mism)} MISMATCH' if mism else ''}")
    if pend:
        print(f"\n{len(pend)} check(s) the corpus asks for and nothing implements "
              f"(this is the Phase 1-6 queue, not a pass):")
        for c in pend:
            owner = PENDING_OWNER.get(c) or next(
                (v for k, v in PENDING_OWNER.items() if c.startswith(k)), "unassigned")
            print(f"    {c:28s} {owner}")
    if A.json: json.dump(out, open(A.json, "w"), indent=1)
    print(f"\nCORPUS {'PASS' if not mism else 'FAIL'}   ({time.time()-t0:.0f}s)")
    return 1 if mism else 0


if __name__ == "__main__":
    sys.exit(main())
