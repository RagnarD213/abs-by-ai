"""S-Log3 / S-Gamut3.Cine -> Rec.709 (BT.1886 display) 3D LUT, 33^3 .cube.
Sony's published S-Log3 transfer + the S-Gamut3.Cine->Rec709 matrix (linear space).
Includes a mild highlight rolloff so skin/white does not clip hard at 709."""
import numpy as np, sys
N=33
def slog3_to_lin(x):
    x=np.asarray(x,dtype=np.float64)
    a=(x*1023-95)*0.01125000/(171.2102946929-95)
    b=(10**((x*1023-420)/261.5))*(0.18+0.01)-0.01
    return np.where(x>=171.2102946929/1023,b,a)
# S-Gamut3.Cine -> XYZ(D65) and XYZ -> Rec709 ; Sony matrix S-Gamut3.Cine -> Rec709:
M=np.array([[ 1.6269474, -0.5401385, -0.0868088],
            [-0.1785155,  1.4179409, -0.2394254],
            [-0.0263528, -0.3511834,  1.3775362]])
def rec709_oetf(l):
    l=np.clip(l,0,None)
    return np.where(l<0.018, 4.5*l, 1.099*np.power(l,0.45)-0.099)
def rolloff(l, knee=0.72, maxv=1.0):
    # soft shoulder above `knee` in scene-linear (normalised so 0.9 diffuse white -> ~1.0)
    l=np.asarray(l)
    out=np.where(l<=knee, l, knee+(1-knee)*(1-np.exp(-(l-knee)/(1-knee))))
    return out
EXPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.0   # linear exposure gain
g=np.linspace(0,1,N)
B,G,R=np.meshgrid(g,g,g,indexing='ij')   # cube order: R fastest
rgb=np.stack([R.ravel(),G.ravel(),B.ravel()],1)
lin=slog3_to_lin(rgb)*EXPO
lin=lin@M.T
lin=np.clip(lin,0,None)
# scene-linear 0.18 grey -> 709: scale so 90% diffuse white (~0.9 linear) lands near 1.0
lin=lin/0.9
lin=rolloff(lin,knee=0.75)
out=np.clip(rec709_oetf(lin),0,1)
with open(f"slog3_709_e{EXPO:.2f}.cube","w") as f:
    f.write("TITLE \"SLog3 SGamut3Cine to Rec709\"\n")
    f.write(f"LUT_3D_SIZE {N}\n")
    for r_,g_,b_ in out: f.write(f"{r_:.6f} {g_:.6f} {b_:.6f}\n")
print("wrote", f"slog3_709_e{EXPO:.2f}.cube")
