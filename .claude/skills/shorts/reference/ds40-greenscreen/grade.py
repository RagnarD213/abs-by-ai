"""DS-40 foreground grade: BT.709 Y'CbCr tone curve + highlight shoulder, chroma gain, hue rotation."""
import numpy as np
KR, KB = 0.2126, 0.0722
def to_ycc(x):
    Y = KR*x[...,0] + (1-KR-KB)*x[...,1] + KB*x[...,2]
    return Y, (x[...,2]-Y)/1.8556, (x[...,0]-Y)/1.5748
def to_rgb(Y, Cb, Cr):
    r = Y + 1.5748*Cr; b = Y + 1.8556*Cb
    g = (Y - KR*r - KB*b) / (1-KR-KB)
    return np.stack([r, g, b], -1)
def curve(Y, gain=1.0, black=0.0, contrast=0.0, knee=0.55, shoulder=0.5):
    y = np.clip((Y - black) / (1 - black), 0, None) * gain
    if contrast:   # S-curve around 0.4, keeps 0 and 1
        p = 0.4
        s = np.where(y < p, p * (y / p) ** (1 + contrast), 1 - (1 - p) * ((1 - np.clip(y, 0, 1)) / (1 - p)) ** (1 + contrast))
        y = np.where(y <= 1, s, y)
    # soft highlight shoulder above knee: compresses toward 1
    over = np.clip(y - knee, 0, None)
    y = np.where(y > knee, knee + over / (1 + over * shoulder / (1 - knee)), y)
    return y
def grade(F, gain=1.0, black=0.0, contrast=0.0, knee=0.55, shoulder=0.5, sat=1.0, hue_deg=0.0, warm=0.0):
    Y, Cb, Cr = to_ycc(F)
    Y2 = curve(Y, gain, black, contrast, knee, shoulder)
    # chroma follows luma change proportionally (keeps saturation as a ratio), then sat
    k = np.where(Y > 1e-3, Y2 / np.maximum(Y, 1e-3), 1.0)
    k = np.clip(k, 0, 2.0) * sat
    Cb2, Cr2 = Cb * k, Cr * k
    if hue_deg:
        a = np.radians(hue_deg); c, s = np.cos(a), np.sin(a)
        Cb2, Cr2 = Cb2 * c - Cr2 * s, Cb2 * s + Cr2 * c
    if warm:   # push toward warm (Cr up, Cb down), scaled by luma so blacks stay neutral
        Cr2 = Cr2 + warm * Y2; Cb2 = Cb2 - warm * 0.8 * Y2
    return np.clip(to_rgb(Y2, Cb2, Cr2), 0, 1)
LOOKS = {
    "A_natural":   dict(gain=0.93, black=0.01, contrast=0.08, knee=0.50, shoulder=0.9, sat=1.04, hue_deg=0.0, warm=0.0),
    "B_warmvivid": dict(gain=0.89, black=0.015, contrast=0.14, knee=0.48, shoulder=1.1, sat=1.16, hue_deg=3.5, warm=0.010),
    "C_bold":      dict(gain=0.86, black=0.025, contrast=0.26, knee=0.46, shoulder=1.3, sat=1.12, hue_deg=2.0, warm=0.006),
}
