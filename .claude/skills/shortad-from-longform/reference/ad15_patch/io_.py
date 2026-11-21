import subprocess,numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
RAW="/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1604.MP4"
SRC="/Volumes/Extreme/_edit_work/revisions-20260921/dl/ad15.mp4"
FPS=30000/1001
CONV="scale=in_color_matrix=bt709:out_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int+bicubic"
def rgb(path,f0,n,conv=CONV,w=1920,h=1080):
    """frames f0..f0+n-1 by index (seek 2 s early, then select by exact frame via pts), float32 RGB"""
    pre=max(0,f0-60)
    # -ss before -i with accurate seek, then trim by frame count from pre
    cmd=[FF,"-v","error","-ss",f"{pre/FPS:.6f}","-i",path,"-vf",f"trim=start_frame={f0-pre}:end_frame={f0-pre+n},{conv},format=rgb48le","-vsync","0","-f","rawvideo","-"]
    p=subprocess.run(cmd,capture_output=True).stdout
    a=np.frombuffer(p,np.uint16).reshape(-1,h,w,3).astype(np.float32)/65535.0
    assert len(a)==n,(len(a),n)
    return a
