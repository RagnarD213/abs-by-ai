#!/usr/bin/env python3
"""A 9:16 VERTICAL (AND ITS <=0:59 CUTDOWN) FROM AN EDITOR'S FINISHED MASTER, AS ONE COMMAND. No editing session.

  python3 kit_run.py --master HIS.mp4 --build B --name "<title> | claude | 9x16 | ad N"
                     [--shoot SHOOT_DIR | --raw ROLL] [--ai gemini] [--judge session|both]
                     [--from STAGE] [--until STAGE] [--deliver DIR]

Stages, in the kit README's build order, each one calling the kit's existing script (nothing here designs, draws or
grades):

  recover    kit_recover.py      his edit: transcript, roll(s), audio EDL, grade (skill Step 1, no model)
  measure    auto_measure.py     where his graphics are (master vs Dan's graded raw, every frame)
  content    auto_content.py     content.json + assets.py (escalations STOP the run: exit 3)
  setup      kit_deliver.py setup     audio   kit_deliver.py audio --mode master (his mix, untouched)
  kit        build_kit.py --from-master   base  kit_base.py   track  kit_track.py   labels  kit_labels.py
  words / picture / captions / mux        kit_deliver.py
  prewatch   kit_deliver.py gate: audio gate (--verbatim), plan, watch pass (sheets + strips)
  judge      the JUDGED watch pass. --judge session (default): stops (exit 4) until fresh session judges write
             logs/findings_part1..3.json (watch/JUDGE_PROMPT.md); resume with --from fold. --judge both: the Gemini
             judge (gemini_judge.py) ALSO writes its own findings file, folded in with the session judges'.
             The Gemini judge alone does not meet the bar (README: it missed 6 of 6 known defects on Ad 10's
             rejected build 1), so it is never the only judge.
  fold       kit_fold.sh -> gate_final.json (GATE PASS or the run stops)       labelcheck  kit_labels.py --verify
  review     540p review copy
  pick       cutdown_pick.py  (the ONE text call: which sentences)   cutdown  kit_cutdown.py --build
  cutgate    audio gate + kit_plan_cutdown.py + watch pass on the cutdown (judged like the full one: exit 4 again)
  cutfold    the cutdown's fold + gate                                deliver  copy masters, review copies, stamps, recipe

Writes B/run_report.json after every stage: stages with wall-clock and status, every AI call with its cost (the
ledger), every escalation, both gate verdicts.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SHARED = os.path.join(REPO, ".claude/skills/_shared")
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
PY = sys.executable
sys.path.insert(0, HERE)
import ai_calls  # noqa: E402

STAGES = ["recover", "measure", "content", "setup", "audio", "kit", "base", "track", "labels", "words", "picture",
          "captions", "mux", "prewatch", "judge", "fold", "labelcheck", "review", "pick", "cutdown", "cutgate",
          "cutjudge", "cutfold", "deliver"]


KEEP_CAPS = {"I", "I'm", "I'll", "I've", "I'd", "AI", "Dan", "ChatGPT", "Abs", "Zepbound", "Google", "Instagram", "YouTube",
             "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "OK", "Okay"}


def caption_case(d):
    """The captions read the transcript's words. Whisper capitalises some mid-sentence words ("of the Excuses",
    Ad 10 88.2 s, a judged junk_card): a Capitalised word that is not a sentence start, a name or an acronym is
    lowercased. Only the case changes; timings are untouched."""
    prev = "."
    for s in d.get("segments", []):
        for w in s.get("words", []):
            raw = w["word"]
            core = raw.strip()
            bare = core.strip(",.?!:;\"'")
            if bare and bare[0].isupper() and not bare.isupper() and prev[-1:] not in ".?!" and bare not in KEEP_CAPS \
                    and not any(bare.startswith(k + "'") for k in ("I",)):
                w["word"] = raw.replace(bare, bare[0].lower() + bare[1:], 1)
            if core:
                prev = core
    return d


class Stop(Exception):
    def __init__(self, code, why):
        self.code, self.why = code, why


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--master", required=True)
    ap.add_argument("--build", required=True)
    ap.add_argument("--name", required=True, help='deliverable base name, e.g. "ai showed me two futures | claude | 9x16 | ad 8"')
    ap.add_argument("--shoot", action="append", default=[])
    ap.add_argument("--raw", action="append", default=[])
    ap.add_argument("--ai", default="gemini")
    ap.add_argument("--judge", default="session", choices=["session", "both"])
    ap.add_argument("--from", dest="start", default="recover", choices=STAGES)
    ap.add_argument("--until", default="deliver", choices=STAGES)
    ap.add_argument("--deliver", help="the ad's folder under '<Editor> Ad Videos/' (deliver stage)")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    os.makedirs(B, exist_ok=True)
    master = os.path.abspath(a.master)
    full = os.path.join(B, a.name + ".mp4")
    cutname = a.name.replace("| 9x16 |", "| 9x16 59s |")
    cut = os.path.join(B, cutname + ".mp4")
    ledger = os.path.join(B, "ai_ledger.jsonl")
    env = dict(os.environ, PATH=os.path.dirname(FF) + ":" + os.environ.get("PATH", ""))
    rp = os.path.join(B, "run_report.json")
    R = json.load(open(rp)) if os.path.exists(rp) else dict(master=master, build=B, name=a.name, stages=[])

    def save(extra=None):
        R["ai"] = ai_calls.Ledger(ledger).total()
        R["wall_clock_s"] = round(sum(s.get("seconds", 0) for s in R["stages"]), 1)
        esc = []
        for f in ("recover_report.json", "auto_content_report.json"):
            p = os.path.join(B, f)
            if os.path.exists(p):
                d = json.load(open(p))
                esc += d.get("escalations", []) + ([dict(what=d["escalation"])] if d.get("escalation") else [])
        R["escalations"] = esc
        for g, f in (("gate_full", "gate_final.json"), ("gate_cutdown", "cut/gate_final.json")):
            p = os.path.join(B, f)
            if os.path.exists(p):
                R[g] = json.load(open(p)).get("verdict")
        if extra:
            R.update(extra)
        json.dump(R, open(rp, "w"), indent=1)

    def sh(cmd, cwd=B, check=True):
        print("$", " ".join(os.path.basename(str(c)) if i == 0 else str(c) for i, c in enumerate(cmd))[:300], flush=True)
        r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=env)
        if check and r.returncode:
            raise Stop(r.returncode if r.returncode in (3, 4) else 1, f"{os.path.basename(str(cmd[1]))} exited {r.returncode}")
        return r.returncode

    roll = lambda: list(json.load(open(os.path.join(B, "rolls.json"))).values())[0]

    def rolls_args():
        rl = json.load(open(os.path.join(B, "rolls.json")))
        if len(rl) == 1:
            return ["--raw", list(rl.values())[0]]
        json.dump(rl, open(os.path.join(B, "rolls_named.json"), "w"))
        return ["--raw", list(rl.values())[0], "--rolls", os.path.join(B, "rolls_named.json")]

    def stage(name):
        K = lambda s: os.path.join(HERE, s)
        D = lambda *x: [PY, K("kit_deliver.py")] + list(x)
        if name == "recover":
            cmd = [PY, K("kit_recover.py"), "--build", B, "--master", master]
            for s in a.shoot:
                cmd += ["--shoot", s]
            for r in a.raw:
                cmd += ["--raw", r]
            sh(cmd)
        elif name == "measure":
            rl = json.load(open(os.path.join(B, "rolls.json")))
            cmd = [PY, K("auto_measure.py"), "--build", B, "--master", master, "--edl", "edl_final.json", "--grade", "grade.py"]
            if len(rl) == 1:
                cmd += ["--raw", list(rl.values())[0]]
            else:
                json.dump(rl, open(os.path.join(B, "rolls_named.json"), "w")); cmd += ["--rolls", "rolls_named.json"]
            sh(cmd)
        elif name == "content":
            sh([PY, K("auto_content.py"), "--build", B, "--master", master, "--words", "m.whisper.json", "--ai", a.ai,
                "--ledger", ledger])
        elif name == "setup":
            empty = os.path.join(B, "_no_source"); os.makedirs(empty, exist_ok=True)
            sh(D("setup", "--build", B, "--from-build", empty))
            if not os.path.exists(os.path.join(B, "ref.whisper.json")):
                d = json.load(open(os.path.join(B, "m.whisper.json")))
                json.dump(caption_case(d), open(os.path.join(B, "ref.whisper.json"), "w"))
        elif name == "audio":
            sh(D("audio", "--build", B, "--mode", "master", "--approved", master))
        elif name == "kit":
            sh([PY, K("build_kit.py"), "--from-master", "--build", B, "--edl", "edl_final.json", "--content", "content.json",
                "--words", "m.whisper.json", "--reference", master, "--grade", "grade.py"] + rolls_args())
        elif name == "base":
            sh([PY, K("kit_base.py"), "--build", B, "--grade", "grade.py"] + rolls_args())
        elif name == "track":
            sh([PY, K("kit_track.py"), "--build", B])
        elif name == "labels":
            sh([PY, K("kit_labels.py"), "--build", B])
        elif name in ("words", "picture", "captions"):
            sh(D(name, "--build", B))
        elif name == "mux":
            sh(D("mux", "--build", B, "--out", full))
        elif name == "prewatch":
            sh(D("gate", "--build", B, "--video", full, "--reference-cut", master))
            sh([PY, K("kit_negscan.py"), "sheet", "--build", B, "--video", full])
        elif name in ("judge", "cutjudge"):
            wd = os.path.join(B, "watch") if name == "judge" else os.path.join(B, "cut_audit", "watch")
            logs = os.path.join(B, "logs") if name == "judge" else os.path.join(B, "cut_audit", "logs")
            vid = full if name == "judge" else cut
            parts = sorted(glob.glob(os.path.join(logs, "findings_part*.json")))
            if a.judge == "both" and not os.path.exists(os.path.join(logs, "gemini", "findings_part1.json")):
                sh([PY, K("gemini_judge.py"), "--build", B, "--video", vid, "--watch", wd, "--parts", "1",
                    "--out-dir", os.path.join(logs, "gemini"), "--ledger", ledger, "--model", "gemini-3.8-flash"])
            session = [p for p in parts]
            if len(session) < 3:
                raise Stop(4, f"awaiting the judged watch pass: fresh session judges read {wd}/JUDGE_PROMPT.md and write "
                              f"{logs}/findings_part1..3.json (+ negscan_findings.json); then rerun with --from "
                              f"{'fold' if name == 'judge' else 'cutfold'}")
            if a.judge == "both":
                g = os.path.join(logs, "gemini", "findings_part1.json")
                shutil.copy(g, os.path.join(logs, "findings_part9_gemini.json"))
        elif name == "fold":
            sh(["zsh", K("kit_fold.sh"), B, full, "session judges" + (" + Gemini judge" if a.judge == "both" else "")])
            g = json.load(open(os.path.join(B, "gate_final.json")))
            if g.get("verdict") != "PASS":
                raise Stop(1, f"GATE {g.get('verdict')}: " + "; ".join(r["key"] for r in g["rows"] if r.get("ok") is not True))
        elif name == "labelcheck":
            sh([PY, K("kit_labels.py"), "--build", B, "--verify", full])
        elif name == "review":
            sh(D("review", "--build", B, "--video", full))
        elif name == "pick":
            sh([PY, K("cutdown_pick.py"), "--build", B, "--ai", a.ai, "--ledger", ledger])
        elif name == "cutdown":
            shutil.copy(K("kit_cutdown.py"), os.path.join(B, "kit_cutdown.py"))
            sh([PY, "kit_cutdown.py", "--build", "--out", cut])
        elif name == "cutgate":
            audit = os.path.join(B, "cut_audit")
            os.makedirs(audit, exist_ok=True)
            sh([PY, os.path.join(SHARED, "audio/audio_gate.py"), cut, "--reference-mix", os.path.join(B, "his_mix.wav"),
                "--verbatim"], check=False)
            sh([PY, K("kit_plan_cutdown.py"), "--build", B, "--video", cut, "--audit", audit, "--source", full, "--transcribe"])
            sh([PY, os.path.join(SHARED, "deliver/watch.py"), cut, "--plan", os.path.join(audit, "plan.json"),
                "--out", os.path.join(audit, "watch"), "--log", os.path.join(audit, "logs", "watch_pass.json")], cwd=audit)
            sh([PY, K("kit_negscan.py"), "sheet", "--build", audit, "--video", cut], cwd=audit)
        elif name == "cutfold":
            audit = os.path.join(B, "cut_audit")
            sh(["zsh", K("kit_fold.sh"), audit, cut, "session judges" + (" + Gemini judge" if a.judge == "both" else "")])
            g = json.load(open(os.path.join(audit, "gate_final.json")))
            os.makedirs(os.path.join(B, "cut"), exist_ok=True)
            shutil.copy(os.path.join(audit, "gate_final.json"), os.path.join(B, "cut", "gate_final.json"))
            if g.get("verdict") != "PASS":
                raise Stop(1, f"CUTDOWN GATE {g.get('verdict')}")
            sh(D("review", "--build", B, "--video", cut))
        elif name == "deliver":
            if not a.deliver:
                raise Stop(0, "no --deliver folder: build complete, nothing copied")
            os.makedirs(a.deliver, exist_ok=True)
            rec = os.path.join(a.deliver, "recipe-vertical")
            os.makedirs(rec, exist_ok=True)
            for f in [full, cut]:
                for x in glob.glob(f + "*") + [f.replace(".mp4", "_REVIEW_540p.mp4")]:
                    if os.path.exists(x):
                        dst = os.path.basename(x).replace("_REVIEW_540p.mp4", ".mp4").replace("| claude |", "| REVIEW 540p |") \
                            if x.endswith("_REVIEW_540p.mp4") else os.path.basename(x)
                        shutil.copy(x, os.path.join(a.deliver, dst))
            for f in ("content.json", "assets.py", "grade.py", "his.cube", "edl_final.json", "auto_content_report.json",
                      "recover_report.json", "kit_report.json", "plan.json", "gate_final.json", "cutdown_ranges.json",
                      "run_report.json", "ai_ledger.jsonl"):
                if os.path.exists(os.path.join(B, f)):
                    shutil.copy(os.path.join(B, f), os.path.join(rec, f))

    started = STAGES.index(a.start)
    stop = STAGES.index(a.until)
    code = 0
    for name in STAGES[started:stop + 1]:
        t = time.time()
        row = dict(stage=name)
        try:
            stage(name)
            row.update(status="ok")
        except Stop as e:
            row.update(status="stopped", why=e.why)
            code = e.code
        row["seconds"] = round(time.time() - t, 1)
        R["stages"] = [s for s in R["stages"] if s["stage"] != name] + [row]
        save()
        print(f"== {name}: {row['status']} ({row['seconds']} s){' -- ' + row.get('why', '') if row.get('why') else ''}", flush=True)
        if row["status"] != "ok":
            break
    print(json.dumps({k: R.get(k) for k in ("wall_clock_s", "ai", "gate_full", "gate_cutdown")}, indent=1))
    return code


if __name__ == "__main__":
    sys.exit(main())
