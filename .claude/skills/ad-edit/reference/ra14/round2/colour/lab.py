#!/usr/bin/env python3
"""RA-14 round 2 colour lab: grade the S-Log3 frame analytically (the same maths make_lut.py bakes), with a white balance
in camera-linear, exposure, a display tone curve and a saturation, so candidates can be judged before any LUT is baked."""
import numpy as np, sys
from PIL import Image
M = np.array([[1.6269474, -0.5401385, -0.0868088], [-0.1785155, 1.4179409, -0.2394254], [-0.0263528, -0.3511834, 1.3775362]])

SKIN_ANG, SKIN_HALF = 118.0, 40.0

def slog3_to_lin(x):
    a = (x*1023-95)*0.01125/(171.2102946929-95)
    b = (10**((x*1023-420)/261.5))*0.19-0.01
    return np.where(x >= 171.2102946929/1023, b, a)

def oetf(l):
    l = np.clip(l, 0, None)
    return np.where(l < 0.018, 4.5*l, 1.099*np.power(l, 0.45)-0.099)

def rolloff(l, knee=0.75):
    return np.where(l <= knee, l, knee+(1-knee)*(1-np.exp(-(l-knee)/(1-knee))))

def grade(x, expo=1.15, wb=(1, 1, 1), sat=1.0, lift=0.0, gamma=1.0, contrast=0.0, pivot=0.42, knee=0.75, vib=0.0, post_sat=1.0, skin_rot=0.0, skin_sat=1.0):
    """x: float S-Log3 RGB 0..1 (N,3 or H,W,3). wb: camera-linear channel gains. sat: Rec.709 linear-luma saturation.
    lift: shadow lift in display space; gamma: mid gamma (>1 brighter mids); contrast: S-curve amount about pivot."""
    sh = x.shape; x = x.reshape(-1, 3).astype(np.float64)
    lin = slog3_to_lin(x)*expo*np.array(wb)
    lin = np.clip(lin@M.T, 0, None)
    if sat != 1.0 or vib:
        Y = (lin@np.array([0.2126, 0.7152, 0.0722]))[:, None]
        s = sat
        if vib:                                   # vibrance: push the dull colours more than the already strong ones
            mx, mn = lin.max(1, keepdims=True), lin.min(1, keepdims=True)
            cs = (mx-mn)/np.maximum(mx, 1e-6)
            s = sat + vib*(1-cs)
        lin = np.clip(Y+(lin-Y)*s, 0, None)
    lin = rolloff(lin/0.9, knee)
    v = np.clip(oetf(lin), 0, 1)
    if gamma != 1.0: v = np.power(v, 1.0/gamma)
    if contrast:                                  # smooth S about the pivot: steeper mids, protected ends
        k = 1+contrast
        lo = pivot*np.power(np.clip(v/pivot, 0, 1), k)
        hi = 1-(1-pivot)*np.power(np.clip((1-v)/(1-pivot), 0, 1), k)
        v = np.where(v < pivot, lo, hi)
    if lift: v = lift + v*(1-lift)
    if skin_rot or skin_sat != 1.0:              # a secondary on the skin hues only: rotate toward gold, neutrals untouched
        Yd = v@np.array([0.2126, 0.7152, 0.0722])
        cb = (v[:, 2]-Yd)/1.8556; cr = (v[:, 0]-Yd)/1.5748
        mag = np.hypot(cb, cr); ang = np.degrees(np.arctan2(cr, cb))          # skin sits near 115-125 deg here
        w = np.clip(1-np.abs(ang-SKIN_ANG)/SKIN_HALF, 0, 1); w = w*w*(3-2*w)
        m = np.clip((mag-0.015)/0.03, 0, 1); w = w*m*m*(3-2*m)
        th = np.radians(skin_rot*w); c_, s_ = np.cos(th), np.sin(th)
        cb2 = (cb*c_-cr*s_)*(1+(skin_sat-1)*w); cr2 = (cb*s_+cr*c_)*(1+(skin_sat-1)*w)
        r = Yd+1.5748*cr2; b = Yd+1.8556*cb2; g = (Yd-0.2126*r-0.0722*b)/0.7152
        v = np.clip(np.stack([r, g, b], 1), 0, 1)
    if post_sat != 1.0:                           # what ffmpeg eq=saturation does: scale chroma about Rec.709 luma, display space
        Yd = (v@np.array([0.2126, 0.7152, 0.0722]))[:, None]
        v = Yd+(v-Yd)*post_sat
    return np.clip(v, 0, 1).reshape(sh)

def load(p):
    """p: the .rgb48 dump (ffmpeg -pix_fmt rgb48le) of a 2160x3840 frame."""
    return np.fromfile(p.replace('.png', '.rgb48'), dtype='<u2').reshape(3840, 2160, 3).astype(np.float64)/65535.0

def to_img(v): return Image.fromarray((np.clip(v, 0, 1)*255+0.5).astype(np.uint8))
