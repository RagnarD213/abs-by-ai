"""Shared plumbing for the Soft Blue Light HyperFrames templates (lower-third/, before-card/, side-list/).

Every template folder has <name>.template.htm (with __CFG__, __ID__, __DUR__ placeholders) and a build.py that turns a
config into scene-relative numbers and calls make_scene() here. One HyperFrames project per scene (lint rejects two
roots in one folder). Pinned version, PATH and CLI notes: Media/hyperframes/README.md.

Text placement matches softblue.py (PIL) pixel for pixel: Poppins has ascent 1050 / descent 350 per 1000 units, so a
CSS box with `line-height: 1.4` and `top: y` puts the baseline exactly where PIL's default "la" anchor at y does.
"""
import json, os, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
VERSION = "0.8.97"
FONTS = ROOT / "Media/codex-video-trial/assets/fonts"
BIN = ROOT / "Media/video_edit/bin"
sys.path.insert(0, str(HERE.parent))           # _shared/softblue.py for geometry and colours
import softblue as B                           # noqa: E402

ENV = dict(os.environ, PATH=f"{BIN}:{os.environ['PATH']}", HYPERFRAMES_SKIP_SKILLS="1")
NPX = ["npx", "-y", f"hyperframes@{VERSION}"]


def rel(t, a):
    return round(t - a, 3)


def text_w(s, px, bold=True):
    return round(B.text_w(s, B.font(px, bold)), 1)


def package_json(name):
    cmd = lambda v: f"npx --yes hyperframes@{VERSION} {v}"
    return json.dumps(dict(name=name, private=True, type="module",
                           scripts=dict(dev=cmd("preview"), check=cmd("check"), render=cmd("render"))), indent=2)


def make_scene(tpl_path, cfg, out_dir, assets=()):
    """Write OUT/<id>/ as a HyperFrames project: index.html from the template, package.json, fonts, extra assets."""
    d = pathlib.Path(out_dir) / cfg["id"]
    (d / "assets").mkdir(parents=True, exist_ok=True)
    html = pathlib.Path(tpl_path).read_text()
    cw, ch = cfg.get("canvas", (1920, 1080))            # 1080x1920 for a vertical (vertical.py); templates carry __W__/__H__
    (d / "index.html").write_text(html.replace("__CFG__", json.dumps(cfg, indent=2))
                                  .replace("__ID__", cfg["id"]).replace("__DUR__", str(cfg["dur"]))
                                  .replace("__W__", str(cw)).replace("__H__", str(ch)))
    (d / "package.json").write_text(package_json(cfg["id"]))
    (d / "hyperframes.json").write_text(json.dumps({"paths": {"assets": "assets"}}, indent=2))
    for f in ("Poppins-Bold.ttf", "Poppins-Regular.ttf"):
        dst = d / "assets" / f
        if not dst.exists(): dst.write_bytes((FONTS / f).read_bytes())
    for src, name in assets:
        (d / "assets" / name).write_bytes(pathlib.Path(src).read_bytes())
    return d


def lint_check(d):
    for step in (["lint"], ["check"]):
        r = subprocess.run(NPX + step, cwd=d, env=ENV, capture_output=True, text=True)
        out = r.stdout + r.stderr
        ok = r.returncode == 0 and (" 0 error" in out.replace("0 errors", " 0 error") or "error" not in out.lower())
        print(d.name, step[0], "ok" if ok else "FAILED", flush=True)
        if not ok:
            print(out[-4000:]); sys.exit(1)


def snapshot(d, times):
    subprocess.run(NPX + ["snapshot", "--at", ",".join(str(t) for t in times)], cwd=d, env=ENV, check=True,
                   capture_output=True)
    return sorted((d / "snapshots").glob("*.png"))


def _rq():
    sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "renderq"))
    import renderq
    return renderq


def _queue(label, d=None, out=None):
    """A slot in the render queue (VIDEO-RULES, "Video builds"), or nothing if the queue cannot load. Heavy; a
    graphic of 10 s or less goes in the quick lane so it never waits behind long renders."""
    try:
        rq = _rq()
        pool = getattr(rq, "pool_for_hyperframes", lambda *a, **k: "heavy")(d) if d else "heavy"
        kw = dict(drives=[str(d), str(out)]) if d and out and hasattr(rq, "drive_of") else {}
        return rq.slot(label, pool=pool, **kw)
    except Exception:
        from contextlib import nullcontext
        return nullcontext()


def _scratch_for(out_mov):
    """Where Chrome's frames and the encoder's chunks go while rendering: the internal SSD scratch folder when the
    queue offers one (renderq.scratch_dir), else beside the output as before."""
    try:
        rq = _rq()
        if hasattr(rq, "scratch_dir"):
            return rq.scratch_dir(need_gb=3) / "hf-render"
    except Exception:
        pass
    return None


def render(d, out_mov):
    """Transparent ProRes 4444 at 29.97 (opaque scenes render the same way; their alpha is simply full).
    Renders in scratch on the internal SSD and moves the finished .mov into place."""
    out_mov = pathlib.Path(out_mov).resolve()
    out_mov.parent.mkdir(parents=True, exist_ok=True)
    tmp_dir = _scratch_for(out_mov)
    target = out_mov
    if tmp_dir is not None:
        tmp_dir = tmp_dir / "{}-{}".format(os.getpid(), out_mov.stem)
        tmp_dir.mkdir(parents=True, exist_ok=True)
        target = tmp_dir / out_mov.name
    with _queue("HyperFrames render " + out_mov.name, d, out_mov):    # headless Chrome plus an encoder
        subprocess.run(NPX + ["render", "--format", "mov", "--fps", "30000/1001", "-o", str(target)], cwd=d,
                       env=dict(ENV, **{k: v for k, v in os.environ.items() if k == "GATE_HELD"}), check=True)
    if target != out_mov:
        import shutil
        shutil.move(str(target), str(out_mov))
        shutil.rmtree(str(tmp_dir), ignore_errors=True)
    print(d.name, "rendered", out_mov, flush=True)
    return out_mov


def run_all(scenes, out, do_render):
    """scenes: [(template_path, cfg, assets)]. Builds, lints and checks every scene, then renders if asked."""
    built = [make_scene(t, c, out, a) for t, c, a in scenes]
    for d in built: lint_check(d)
    if do_render:
        for d in built: render(d, pathlib.Path(out) / f"{d.name}.mov")
    return built
