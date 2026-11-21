"""HyperFrames renders for the two text-bearing background types (panel = 4, bigtype = 7). Each segment becomes one
opaque 1920x1080 render of the whole background (moving field + graphic), read behind Dan by gsbg.HFLayer.

  python3 hfbg.py PLAN.json OUT_DIR [--render] [--only BG04,BG07] [--snap]

PLAN.json is the film's bg_plan.json (README "Plan format"); paths in it resolve against the plan's folder. Writes
OUT_DIR/projects/<id>/, OUT_DIR/<id>.mov (+ .cfg.sha: an unchanged segment is not re-rendered), and sets each
segment's "mov" in the plan.

panel segment:   {"type": "panel", "pair": {"photos": [before, after], "years": ["2012", "2023"], "crop_k": 6.0,
                  "credits": ["Eva Rinaldi (CC BY-SA 2.0)", "Dave Benett/Getty Images"]},
                  "name": "Sharon Osbourne", "stat": "42 lb, Ozempic"}
bigtype segment: {"type": "bigtype", "lines": ["-42 LB", "OZEMPIC"], "line_times": [53.6, 54.1]}   (a line starting with a
                 whole number counts up; line_times, film seconds, land each line on the word that says it)
"""
import hashlib, json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "hyperframes"))
import hfbuild as H                                    # noqa: E402
sys.path.insert(0, str(HERE))
import gsbg as G                                       # noqa: E402

# panel geometry (left of Dan; he stands right, 'right' placement): photos 3:4, the name and stat under them
PANEL = dict(x=84, y=84, pw=364, ph=486, gap=30, name_px=58, stat_px=52, cite_px=22, cite_w=600)   # everything ends above y 810 (lower thirds start at 840)


def year(s, x, y):
    px_, h, pad = 30, 50, 18
    return dict(s=s, x=x, y=y, w=round(H.text_w(s, px_) + 2 * pad), h=h, r=14, px=px_, pad=pad, pt=round((h - px_ * 1.4) / 2))


def panel_cfg(seg, root, work):
    P = dict(PANEL, y=seg.get("panel_y", PANEL["y"])); pr = seg["pair"]; photos, assets = [], []   # panel_y: room above the pair for the AI label (never on a face or abs)
    for n, (p, yr) in enumerate(zip(pr["photos"], pr["years"])):
        path = pathlib.Path(p if pathlib.Path(p).is_absolute() else root / p)
        im = G.person_crop(str(path), P["pw"] / P["ph"], k=pr.get("crop_k", 6.0), top=pr.get("top", 0.55))
        im = im.resize((round(P["pw"] * 1.6), round(P["ph"] * 1.6)), G.Image.Resampling.LANCZOS) if im.width > P["pw"] * 1.6 else im
        name = f"{seg['id']}_{n}.jpg"; out = work / name; im.save(out, quality=92)
        x = P["x"] + n * (P["pw"] + P["gap"])
        photos.append(dict(src=f"assets/{name}", x=x, y=P["y"], w=P["pw"], h=P["ph"], origin="50% 30%",
                           year=year(yr, x + 18, P["y"] + P["ph"] - 50 - 18)))
        assets.append((str(out), name))
    ty = P["y"] + P["ph"] + 26
    cfg = dict(id=seg["id"], dur=round(seg["t1"] - seg["t0"], 3), drift=-10, push=1.05, t_field=round(seg["t0"] % 60, 3),
               photos=photos,
               name=dict(s=seg["name"], x=P["x"], y=ty, px=P["name_px"]),
               acc=dict(x=P["x"], y=ty + 88, w=120),
               stat=dict(s=seg["stat"], x=P["x"], y=ty + 98, px=P["stat_px"]),
               cite=None)
    if pr.get("credits"):                  # the credit wraps inside cite_w so a tight shot's shoulder never covers it (RO-24 R3 review)
        words = ("Photos: " + ", ".join(dict.fromkeys(pr["credits"]))).split(" "); lines = [""]
        for wd in words:
            t = (lines[-1] + " " + wd).strip()
            if H.text_w(t, P["cite_px"], False) <= P["cite_w"] or not lines[-1]: lines[-1] = t
            else: lines.append(wd)
        assert len(lines) <= 2, f"{seg['id']}: the credit needs more than two lines"
        cfg["cite"] = dict(s="\n".join(lines), x=P["x"], y=ty + 172, px=P["cite_px"])
    right = P["x"] + 2 * P["pw"] + P["gap"]
    for s, px_, bold in ((seg["name"], P["name_px"], True), (seg["stat"], P["stat_px"], True)):
        assert P["x"] + H.text_w(s, px_, bold) <= right + 60, f"{seg['id']}: '{s}' is wider than the panel"
    for s in (seg["name"], seg["stat"]): assert "—" not in s
    return cfg, assets


BIG = dict(x=86, y0=110, max_w=1060, max_px=250, gap=50, color=(40, 92, 168), opacity=0.80)


def bigtype_cfg(seg, root, work):
    B = dict(BIG, **({"max_w": seg["max_w"]} if seg.get("max_w") else {})); lines = seg["lines"]   # max_w: a long word that would run
    # behind Dan on a tight shot gets narrower type (RO-24 R4: "MICRODOSE" read "MICRODOS"); the default keeps every film unchanged
    px_ = min(B["max_px"], *[int(B["max_px"] * B["max_w"] / max(1, H.text_w(s, B["max_px"]))) for s in lines])
    out, y = [], B["y0"]
    for n, s in enumerate(lines):
        lt = (seg.get("line_times") or [None] * len(lines))[n]
        L = dict(s=s, x=B["x"], y=y, px=px_, t=round(lt - seg["t0"], 2) if lt else round(0.1 + 0.22 * n, 2), dy=-10 - 14 * n)
        m = re.match(r"^([^\d]*)(\d+)(.*)$", s)
        if m and n == 0 and "." not in m.group(3)[:1]:
            L["count"] = dict(pre=m.group(1), value=int(m.group(2)), post=m.group(3))
        out.append(L); y += round(px_ * 1.0) + B["gap"]
    assert y < 1000, f"{seg['id']}: the lines do not fit"
    for s in lines: assert "—" not in s
    return dict(id=seg["id"], dur=round(seg["t1"] - seg["t0"], 3), t_field=round(seg["t0"] % 60, 3),
                lines=out, color=list(B["color"]), opacity=B["opacity"]), []


TPL = {"panel": (HERE / "templates/panel.template.htm", panel_cfg), "bigtype": (HERE / "templates/bigtype.template.htm", bigtype_cfg)}


def build(seg, root, out, render=True, snap=False):
    tpl, fn = TPL[seg["type"]]
    work = pathlib.Path(out) / "assets"; work.mkdir(parents=True, exist_ok=True)
    cfg, assets = fn(seg, pathlib.Path(root), work)
    d = H.make_scene(tpl, cfg, pathlib.Path(out) / "projects", assets); H.lint_check(d)
    sha = hashlib.sha256((json.dumps(cfg, sort_keys=True) + tpl.read_text() +
                          "".join(pathlib.Path(s).read_bytes().hex()[:4096] for s, _ in assets)).encode()).hexdigest()[:16]
    mov = pathlib.Path(out) / f"{seg['id']}.mov"; stamp = pathlib.Path(out) / f"{seg['id']}.cfg.sha"
    if snap:
        for f in H.snapshot(d, [round(min(cfg["dur"] - 0.2, 1.6), 2)]):
            if not f.name.startswith("._"): (pathlib.Path(out) / f"{seg['id']}-snap.png").write_bytes(f.read_bytes())
    if render:
        if stamp.exists() and stamp.read_text() == sha and mov.exists():
            print(seg["id"], "unchanged, render kept", flush=True)
        else:
            if mov.exists(): mov.unlink()
            H.render(d, mov); stamp.write_text(sha)
    return str(mov)


def main():
    plan_path = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    plan = json.load(open(plan_path))
    for seg in plan["segments"]:
        if seg["type"] in TPL and (not only or seg["id"] in only):
            seg["mov"] = build(seg, plan_path.parent, out, "--render" in sys.argv, "--snap" in sys.argv)
    json.dump(plan, open(plan_path, "w"), indent=1)


if __name__ == "__main__":
    main()
