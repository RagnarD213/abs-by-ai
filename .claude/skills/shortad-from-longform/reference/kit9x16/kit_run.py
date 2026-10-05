#!/usr/bin/env python3
"""A 9:16 VERTICAL (AND ITS <=0:59 CUTDOWN) AS ONE COMMAND. No editing session. Two ways in:

  1. FROM AN EDITOR'S FINISHED MASTER (Muhammad's and any human editor's): the edit is recovered by measurement.
  python3 kit_run.py --master HIS.mp4 --build B --name "<title> | claude | 9x16 | ad N"
                     [--shoot SHOOT_DIR | --raw ROLL] [--ai gemini] [--judge session|both]
                     [--from STAGE] [--until STAGE] [--deliver DIR]

  2. FROM THE EDIT SHEET OF A 16:9 THAT CLAUDE OR CODEX MADE (_shared/edit-sheet/): nothing is recovered, because
     the sheet already says which takes, frames, words, graphics and pictures. Graphics are drawn fresh at 9:16 in
     Soft Blue Light with HyperFrames (Dan, 2026-10-01: no more olive graphics).
  python3 kit_run.py --sheet SHEET.json --build B --name "<title> | claude | 9x16 | RO-10" [--from STAGE] [--until STAGE]

     sheet      sheet_to_kit.py     rolls, cut, grade on a hair-anchored window, words, content.json, assets.py
     (setup, audio, kit, base, track as below; the audio is the 16:9's delivered mix, untouched)
     graphics   sbl_graphics.py     every graphic and card plate rendered at 9:16 from the sheet's configs
     picture    render_sbl.py       instead of render.py's olive plates

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

STAGES = ["recover", "measure", "content", "restyle", "sheet", "setup", "audio", "kit", "base", "track", "graphics", "labels", "words", "picture",
          "captions", "mux", "prewatch", "judge", "fold", "labelcheck", "review", "pick", "cutdown", "cutgate",
          "cutjudge", "cutfold", "deliver"]


KEEP_CAPS = {"I", "I'm", "I'll", "I've", "I'd", "AI", "Dan", "ChatGPT", "Abs", "Zepbound", "Google", "Instagram", "YouTube",
             "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "OK", "Okay"}


def level_card_chips(beats):
    """One chip height across a run of back-to-back labelled cards (an app demo): a chip moved lower on one screen
    and back up on the next reads as a jump."""
    bs = sorted([b for b in beats if b.get("kind") == "card" and b.get("label")], key=lambda b: b["t0"])
    run = []
    for b in bs + [None]:
        if b is not None and run and abs(b["t0"] - run[-1]["t1"]) < 0.05:
            run.append(b); continue
        if run:
            dy = max(int(x.get("label_dy", 0)) for x in run)
            for x in run:
                if dy:
                    x["label_dy"] = dy
        run = [b] if b is not None else []


def label_obstructions(B, video):
    """The delivery gate's own compliance:labels clearance measurement on the delivered file -> {media key: [(t, px)]}
    for the full-bleed chips (kit_labels places those; a card's chip hangs under its hole)."""
    sys.path.insert(0, SHARED)
    from deliver.checks import compliance as CMP
    from deliver import formats as FMT
    plan = json.load(open(os.path.join(B, "plan.json")))
    tracks = [t for t in plan.get("label_tracks") or [] if t.get("visibility", "full") == "full"]
    px = getattr(FMT, "_LABELS", {}).get("clearance_px", 8)
    obs, _n, err = CMP._measure_label_clearance(video, tracks, px)
    if err:
        print("  label clearance not measured:", err, flush=True)
        return {}
    kinds = {b.get("media"): b.get("kind") for b in json.load(open(os.path.join(B, "beats.json")))["beats"]}
    out = {}
    for name, t, v in obs or []:
        key = name.split("-", 2)[-1].split("~")[0]
        if kinds.get(key) in ("bleed", "card"):
            out.setdefault(key, []).append((t, v))
    return out


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
    ap.add_argument("--master")
    ap.add_argument("--sheet", help="the 16:9's edit sheet (_shared/edit-sheet/): the second way in")
    ap.add_argument("--sbl", help="with --master: the Soft Blue Light copy file (master_to_sbl.py); graphics drawn with HyperFrames")
    ap.add_argument("--build", required=True)
    ap.add_argument("--name", required=True, help='deliverable base name, e.g. "ai showed me two futures | claude | 9x16 | ad 8"')
    ap.add_argument("--shoot", action="append", default=[])
    ap.add_argument("--raw", action="append", default=[])
    ap.add_argument("--ai", default="gemini")
    ap.add_argument("--judge", default="session", choices=["session", "both"])
    ap.add_argument("--dan-asked", help="Dan's own words asking for a vertical of THIS content video. Without it a sheet whose "
                                        "type is LFC / SFC is refused: content gets Shorts, ads get formats (Dan, 2026-10-04)")
    ap.add_argument("--format", dest="fmt", help="the delivery gate's format for the full film. Default: ad9x16; a sheet of an "
                                                 "organic film (type LFC / SFC) is organic9x16 and its 59 s cut is a `short`")
    ap.add_argument("--from", dest="start", choices=STAGES)
    ap.add_argument("--until", default="deliver", choices=STAGES)
    ap.add_argument("--deliver", help="the ad's folder under '<Editor> Ad Videos/' (deliver stage)")
    ap.add_argument("--tolerance", type=float, help="kit_track.py --tolerance for this build (source px of dead band; Dan's calmer camera)")
    a = ap.parse_args()
    if bool(a.master) == bool(a.sheet):
        ap.error("give exactly one of --master (an editor's finished master) or --sheet (our own 16:9's edit sheet)")
    SHEET = os.path.abspath(a.sheet) if a.sheet else None
    ORGANIC = False
    if SHEET:
        _S = json.load(open(SHEET))
        a.master = _S["video"]["master"]
        ORGANIC = str(_S.get("type", "")).upper() in ("LFC", "SFC")
    # THE GATE'S FORMAT. An ad is graded as an ad. An organic film's vertical is graded as organic (Dan, 2026-10-03):
    # `organic9x16` for the full film (the parent longform's pacing and speech bounds, the organic vertical's framing
    # and caption bounds; organic videos may name the drug), and its <= 0:59 cut is literally a `short`.
    # CONTENT IS NEVER GIVEN AN AD'S FORMATS (Dan, 2026-10-04; VIDEO-RULES "Categorize every video before editing it").
    # The vertical, the square and the 1-minute cut are made from an AD. A long-form gets Shorts (/shorts). RO-10's
    # proof run cost seven hours and 1.6 million judge tokens for a vertical nobody needed.
    if ORGANIC and not a.dan_asked:
        raise SystemExit(f"kit_run: STOP. {os.path.basename(SHEET)} is CONTENT (type {_S.get('type')}), not an ad. A content video is cut "
                         "into Shorts with /shorts; it does not get a vertical, a square or a 1-minute version. Tell Dan what was "
                         "asked. Only his own words naming this video and this format override it: --dan-asked \"<his words>\".")
    FMT = a.fmt or ("organic9x16" if ORGANIC else "ad9x16")
    CUT_FMT = "short" if FMT == "organic9x16" else FMT
    a.start = a.start or ("sheet" if SHEET else "recover")
    # --sbl COPY.json: an editor's master redrawn in Soft Blue Light (master_to_sbl.py after `content`; then the sheet
    # path's graphics and picture stages). Without it a master build still draws the olive kit (answer keys, regressions).
    SBL = os.path.abspath(a.sbl) if a.sbl else None
    skip = ("recover", "measure", "content", "restyle") if SHEET else (("sheet",) if SBL else ("sheet", "graphics", "restyle"))
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
    if a.dan_asked:
        R["dan_asked"] = a.dan_asked

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

    def sh(cmd, cwd=B, check=True, extra_env=None):
        print("$", " ".join(os.path.basename(str(c)) if i == 0 else str(c) for i, c in enumerate(cmd))[:300], flush=True)
        r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=dict(env, **(extra_env or {})))
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
        elif name == "restyle":
            sh([PY, K("master_to_sbl.py"), "--build", B, "--copy", SBL])
        elif name == "sheet":
            sh([PY, os.path.join(SHARED, "edit-sheet", "validate.py"), SHEET, "--hash"])
            sh([PY, K("sheet_to_kit.py"), "--sheet", SHEET, "--build", B, "--ai", a.ai, "--ledger", ledger])
        elif name == "graphics":
            sh([PY, K("sbl_graphics.py"), "--build", B, "--sheet", SHEET or os.path.join(B, "sbl_sheet.json")])
        elif name == "picture" and (SHEET or SBL):
            sh([PY, K("render_sbl.py"), "--selftest"]); sh([PY, K("render_sbl.py")])
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
                "--words", "m.whisper.json", "--reference", master, "--grade", "grade.py"] + rolls_args()
               + (["--piccuts", os.path.join(B, "piccuts.json")] if SHEET else []), check=not SHEET)
            # (a sheet build: the cuts are the sheet's own frames, so no pose search; build_kit's exit 1 only says the
            #  design is outside Muhammad's measured ranges, which is reported in kit_report.json and ruled on by Dan)
        elif name == "base":
            sh([PY, K("kit_base.py"), "--build", B, "--grade", "grade.py"] + rolls_args())
        elif name == "track":
            sh([PY, K("kit_track.py"), "--build", B] + (["--tolerance", str(a.tolerance)] if a.tolerance is not None else []))
        elif name == "labels":
            sh([PY, K("kit_labels.py"), "--build", B])
        elif name in ("words", "picture", "captions"):
            sh(D(name, "--build", B))
        elif name == "mux":
            sh(D("mux", "--build", B, "--out", full))
        elif name == "prewatch":
            bs = json.load(open(K("auto_sources.json"))).get("banned_screens") or {}
            extra = (["--banned-source", bs["source"], "--banned-times"] + [str(t) for t in bs["times"]]) \
                if bs.get("source") and os.path.exists(bs["source"]) else []
            # THE GATE'S LABEL CLEARANCE, CHECKED ON THE DELIVERED FILE BEFORE ANY JUDGE LOOKS: the person mask can
            # read a chip as part of him on a single compressed frame it reads as clear everywhere else (Ad 10
            # 29.83 s, kit autofill 2026-09-30). A chip that trips it is re-placed away from that spot, the changed
            # segments re-render, and the file is checked again (at most 3 times).
            for attempt in range(4):
                shutil.rmtree(os.path.join(B, "watch"), ignore_errors=True)     # no stale strips from an earlier pass
                sh(D("gate", "--build", B, "--video", full, "--reference-cut", master, *extra))
                obs = label_obstructions(B, full)
                if not obs:
                    break
                if attempt == 3:
                    raise Stop(1, f"label chips still touch him on the delivered file after 3 re-placements: {obs}")
                bj_p = os.path.join(B, "beats.json")
                bj = json.load(open(bj_p))
                cards = sorted(k_ for k_ in obs if any(b.get("media") == k_ and b.get("kind") == "card" for b in bj["beats"]))
                if cards and (SHEET or SBL):
                    # a Soft Blue Light card's chip is drawn by the HyperFrames plate at a fixed 68 px under the hole
                    # (vertical.media_card_scene); `label_dy` does not move it, so re-rendering would loop on nothing
                    raise Stop(1, f"a card's chip reads as touching the person in the card on the delivered file: {cards} "
                                  f"{ {k_: obs[k_][:3] for k_ in cards} }. Look at the frame: a real overlap is a layout "
                                  f"change in vertical.media_card_scene; a mask misread is recorded in plan.json label_clearance")
                if cards:
                    # a CARD's chip hangs under its hole: the mask read it as part of a person inside the card (the
                    # uploaded photo on a phone screen, Ad 10 122.0 s). It moves 48 px further below the card per try.
                    for b in bj["beats"]:
                        if b.get("media") in cards and b.get("kind") == "card":
                            b["label_dy"] = int(b.get("label_dy", 0)) + 72
                    level_card_chips(bj["beats"])
                    json.dump(bj, open(bj_p, "w"), indent=1)
                    print(f"  label clearance on the delivered file: card chips {cards} moved 72 px lower", flush=True)
                keys = sorted(k_ for k_ in obs if k_ not in cards)
                if not keys:
                    sh(D("picture", "--build", B)); sh(D("captions", "--build", B)); sh(D("mux", "--build", B, "--out", full))
                    continue
                ep = os.path.join(B, "labels", "exclude.json")
                ex = json.load(open(ep)) if os.path.exists(ep) else {}
                lp = json.load(open(os.path.join(B, "label_place.json")))
                for k_ in keys:
                    c_ = lp.get(k_, {})
                    ex.setdefault(k_, []).append([c_.get("x"), c_.get("y"), c_.get("lines"), c_.get("size")])
                json.dump(ex, open(ep, "w"), indent=1)
                print(f"  label clearance on the delivered file: {obs} -> re-placing {keys}", flush=True)
                sh([PY, K("kit_labels.py"), "--build", B, "--only", *keys])
                sh(D("picture", "--build", B)); sh(D("captions", "--build", B)); sh(D("mux", "--build", B, "--out", full))
            sh([PY, K("kit_negscan.py"), "sheet", "--build", B, "--video", full])
            # THE GATE ITSELF, BEFORE ANY JUDGE: every measured row must already pass; only the two rows the judges
            # write (the watch pass, the negative-events scan) may be open. Three judges spent on a file the gate
            # then fails on a measurement is the most expensive way to find it (kit autofill, 2026-09-30).
            gp = os.path.join(B, "gate_pre.json")
            subprocess.run([PY, os.path.join(SHARED, "deliver", "gate.py"), full, "--format", FMT, "--plan",
                            os.path.join(B, "plan.json"), "--json", gp], cwd=B, capture_output=True)
            if os.path.exists(gp):
                rows = [r for r in json.load(open(gp))["rows"] if r.get("ok") is not True and not r.get("na")
                        and r["key"] not in ("watch:pass", "compliance:negative_events")]
                if rows:
                    raise Stop(1, "the delivery gate fails on measured rows before the watch pass: "
                                  + "; ".join(f"{r['key']}: {r.get('detail', '')[:160]}" for r in rows))
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
            sh(["zsh", K("kit_fold.sh"), B, full, "session judges" + (" + Gemini judge" if a.judge == "both" else "")],
               extra_env=dict(FORMAT=FMT))
            g = json.load(open(os.path.join(B, "gate_final.json")))
            if g.get("verdict") != "PASS":
                raise Stop(1, f"GATE {g.get('verdict')}: " + "; ".join(r["key"] for r in g["rows"] if r.get("ok") is not True))
        elif name == "labelcheck":
            sh([PY, K("kit_labels.py"), "--build", B, "--verify", full])
        elif name == "review":
            sh(D("review", "--build", B, "--video", full))
        elif name == "pick":
            sh([PY, K("cutdown_pick.py"), "--build", B, "--ai", a.ai, "--ledger", ledger] + (["--organic"] if ORGANIC else []))
        elif name == "cutdown":
            sh([PY, K("kit_cutdown.py"), "--build", "--out", cut])            # run from the kit, in the build dir
        elif name == "cutgate":
            audit = os.path.join(B, "cut_audit")
            os.makedirs(audit, exist_ok=True)
            # the cutdown's reference is HIS MIX CUT AT THE SAME SEAMS (cut/his_mix.wav, kit_cutdown.py), never his
            # full mix: a selection's loudness is not the whole film's (AV-07's cutdown gate)
            sh([PY, os.path.join(SHARED, "audio/audio_gate.py"), cut, "--reference-mix", os.path.join(B, "cut", "his_mix.wav"),
                "--verbatim"])
            sh([PY, K("kit_plan_cutdown.py"), "--build", B, "--video", cut, "--audit", audit, "--source", full, "--transcribe"])
            sh([PY, os.path.join(SHARED, "deliver/watch.py"), cut, "--plan", os.path.join(audit, "plan.json"),
                "--out", os.path.join(audit, "watch"), "--log", os.path.join(audit, "logs", "watch_pass.json")], cwd=audit)
            sh([PY, K("kit_negscan.py"), "sheet", "--build", audit, "--video", cut], cwd=audit)
        elif name == "cutfold":
            audit = os.path.join(B, "cut_audit")
            sh(["zsh", K("kit_fold.sh"), audit, cut, "session judges" + (" + Gemini judge" if a.judge == "both" else "")],
               extra_env=dict(FORMAT=CUT_FMT))
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
            if os.path.exists(cut) and not os.path.exists(cut.replace(".mp4", "_REVIEW_540p.mp4")):
                sh(D("review", "--build", B, "--video", cut))            # the cutdown's review copy, beside the full's
            for f in [full, cut]:
                for x in glob.glob(glob.escape(f) + "*") + [f.replace(".mp4", "_REVIEW_540p.mp4")]:
                    if os.path.exists(x):
                        # the folder's naming: "<title> | REVIEW 540p 9x16 [59s] | ad N.mp4"
                        dst = os.path.basename(x).replace("_REVIEW_540p.mp4", ".mp4").replace("| claude | ", "| REVIEW 540p ") \
                            if x.endswith("_REVIEW_540p.mp4") else os.path.basename(x)
                        shutil.copy(x, os.path.join(a.deliver, dst))
            for extra in ("notes-vertical.md",):
                if os.path.exists(os.path.join(B, extra)):
                    shutil.copy(os.path.join(B, extra), os.path.join(a.deliver, extra))
            for f in ("content.json", "assets.py", "grade.py", "his.cube", "edl_final.json", "auto_content_report.json",
                      "recover_report.json", "kit_report.json", "plan.json", "gate_final.json", "cutdown_ranges.json",
                      "cut_plan.json", "beats.json", "label_place.json", "run_report.json", "ai_ledger.jsonl"):
                if os.path.exists(os.path.join(B, f)):
                    shutil.copy(os.path.join(B, f), os.path.join(rec, f))

    started = STAGES.index(a.start)
    stop = STAGES.index(a.until)
    code = 0
    for name in STAGES[started:stop + 1]:
        if name in skip:
            continue
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
