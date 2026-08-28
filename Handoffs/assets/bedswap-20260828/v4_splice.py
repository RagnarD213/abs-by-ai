#!/usr/bin/env python3
"""Splice the rebuilt region into V4. Everything outside [371.28, 451.64) is V4's own
samples, so sync outside the region is preserved by construction."""
import numpy as np, wave, struct
SR=44100; R_IN=371.28; R_OUT=451.64
XF_H=0.015   # head crossfade (Dan's speech ends 371.23)
XF_T=0.012   # tail crossfade (outro line starts 451.662)
def rd(p):
    """int16 via the wave module; IEEE-float (fmt tag 3) is read by hand -- python's
    wave module rejects it."""
    raw=open(p,'rb').read()
    assert raw[:4]==b'RIFF' and raw[8:12]==b'WAVE'
    i=12; fmt=None; data=None
    while i < len(raw)-8:
        cid=raw[i:i+4]; sz=struct.unpack('<I',raw[i+4:i+8])[0]; body=raw[i+8:i+8+sz]
        if cid==b'fmt ': fmt=struct.unpack('<HHIIHH', body[:16])
        elif cid==b'data': data=body; break
        i += 8 + sz + (sz & 1)
    tag,ch,sr,_,_,bits = fmt
    assert sr==SR, (p, sr)
    a = (np.frombuffer(data,dtype=np.float32).astype(np.float64) if tag==3
         else np.frombuffer(data,dtype=np.int16).astype(np.float64)/32768.)
    return a.reshape(-1,ch)
v4=rd("wav/v4_44k_st.wav"); reg=rd("wav/region_new.wav")
i0=int(round(R_IN*SR)); n=len(reg)
assert abs(n-(int(round(R_OUT*SR))-i0))<=1, (n, int(round(R_OUT*SR))-i0)
out=v4.copy()
xh=int(XF_H*SR); xt=int(XF_T*SR)
f=np.linspace(0,1,xh)[:,None]
out[i0:i0+xh]        = v4[i0:i0+xh]*(1-f) + reg[:xh]*f
out[i0+xh:i0+n-xt]   = reg[xh:n-xt]
f=np.linspace(0,1,xt)[:,None]
out[i0+n-xt:i0+n]    = reg[n-xt:]*(1-f) + v4[i0+n-xt:i0+n]*f
print(f"spliced {n/SR:.3f}s at {R_IN}s; peak {20*np.log10(np.abs(out).max()):+.2f} dBFS")
data=out.astype(np.float32).tobytes()
hdr=(b'RIFF'+struct.pack('<I',36+len(data))+b'WAVEfmt '+
     struct.pack('<IHHIIHH',16,3,2,SR,SR*8,8,32)+b'data'+struct.pack('<I',len(data)))
open("wav/v4_mix2.wav",'wb').write(hdr+data)
print(f"wrote wav/v4_mix2.wav  {len(out)/SR:.6f}s")
