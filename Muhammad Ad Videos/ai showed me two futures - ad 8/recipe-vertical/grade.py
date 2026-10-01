"""His BT.709 grade, fitted by kit9x16/kit_recover.py from matched master/raw pixels (centre of frame,
flat regions, 2,079,222 pairs; median error 1.51 levels, ungraded 39.00)."""

import os

LUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "his.cube")

CURVES = (
    "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,"
    f"format=rgb48le,lut3d=file='{LUT}':interp=tetrahedral,"
    "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int"
)

# The kit's output-coordinate vignette (vlib.vignette_mask), same in every approved kit grade.
VIGNETTE = [(0.05, 1.000), (0.15, 0.994), (0.24, 0.987), (0.34, 0.986), (0.44, 0.980), (0.53, 0.972), (0.63, 0.941), (0.72, 0.881), (0.82, 0.791), (0.92, 0.696), (1.01, 0.633), (1.11, 0.469), (1.21, 0.345), (1.30, 0.259), (1.40, 0.260)]

SUBJECT_CX = 872
