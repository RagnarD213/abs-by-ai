"""Ad 10's BT.709 grade, fitted from matched C1601/master camera frames."""

import os


LUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "his.cube")

CURVES = (
    "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,"
    f"format=rgb48le,lut3d=file='{LUT}':interp=tetrahedral,"
    "scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int"
)

# The approved kit's output-coordinate vignette. The tone/LUT fit excludes it.
VIGNETTE = [
    (0.05, 1.000), (0.15, 0.994), (0.24, 0.987), (0.34, 0.986),
    (0.44, 0.980), (0.53, 0.972), (0.63, 0.941), (0.72, 0.881),
    (0.82, 0.791), (0.92, 0.696), (1.01, 0.633), (1.11, 0.469),
    (1.21, 0.345), (1.30, 0.259), (1.40, 0.260)
]

SUBJECT_CX = 960
