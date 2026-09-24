#!/usr/bin/env python3
"""Fixtures for the picture cut: no video, no detector. Run: python3 tests/test_piccuts.py"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import landing  # noqa: E402
import piccuts as P  # noqa: E402


def test_pick_k_prefers_the_head():
    sims = {-3: 0.70, 0: 0.40, 5: 0.45}
    jumps = {-3: 60.0, 0: 30.0, 5: 4.0}
    assert P.pick_k(sims, jumps) == 5, "NCC must not overrule a head that holds its place"
    # head tie within 4 px -> the higher similarity, then the smaller |k|
    assert P.pick_k({-2: 0.5, 2: 0.6}, {-2: 5.0, 2: 7.0}) == 2
    assert P.pick_k({-2: 0.6, 2: 0.6}, {-2: 5.0, 2: 5.0}) == -2
    # no face anywhere -> NCC alone, ties within 0.02 to the smaller |k|
    assert P.pick_k({-9: 0.61, 1: 0.60}, {-9: np.nan, 1: np.nan}) == 1


def test_picture_edl_keeps_length_and_audio():
    E = P.load_edl([{"roll": "a", "start": 10.0, "end": 13.0}, {"roll": "a", "start": 20.0, "end": 22.5},
                    {"roll": "b", "start": 5.0, "end": 9.0}])
    out = [dict(i=1, k=-7), dict(i=2, k=12)]
    Pe = P.picture_edl(E, out)
    assert Pe[-1]["n1"] == round(E[-1]["cut_out"] * P.FPS)
    assert Pe[1]["audio_cut_in"] == E[1]["cut_in"] and Pe[1]["rel"] == -7
    assert abs((Pe[1]["cut_in"] - E[1]["cut_in"]) * P.FPS + 7) < 1e-6
    assert abs(Pe[0]["cut_out"] - Pe[1]["cut_in"]) < 1e-9, "the picture cut moves both sides together"
    assert all(Pe[i]["n1"] == Pe[i + 1]["n0"] for i in range(len(Pe) - 1))


def test_load_edl_shapes():
    a = P.load_edl([{"cut_in": 0, "cut_out": 2, "src_in": 5}])
    b = P.load_edl([{"out_seconds": [0, 2], "src_in": 5, "src_out": 7}])
    c = P.load_edl({"ranges": [{"start": 5, "end": 7}]})
    for e in (a, b, c):
        assert (e[0]["cut_in"], e[0]["cut_out"], e[0]["src_in"], e[0]["src_out"]) == (0, 2, 5, 7)


def test_landing():
    assert landing.selftest() == 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
