# Muhammad's grade, measured off his final cut (2026-08-25).
# Tone curve fitted on the CENTRE box only, so it carries no vignette; the vignette is a
# separate radial gain applied AFTER reframing, in the OUTPUT frame's coordinates.
# Fitting them together smears one into the other and the background comes out too bright.
CURVES = ("curves="
 "r='0.0353/0.0000 0.0471/0.0392 0.0510/0.0431 0.1412/0.2549 0.2627/0.4118 0.3098/0.4667"
 " 0.3373/0.4980 0.3569/0.5216 0.3686/0.5412 0.4627/0.6588 0.6588/0.8196 0.7725/0.9137"
 " 0.8353/0.9569 1.0000/1.0000':"
 "g='0.0275/0.0000 0.0471/0.0392 0.0510/0.0471 0.1137/0.2157 0.1882/0.2941 0.2078/0.3294"
 " 0.2235/0.3529 0.2314/0.3725 0.2510/0.3961 0.3922/0.5804 0.6039/0.7725 0.7137/0.8824"
 " 0.7843/0.9333 1.0000/1.0000':"
 "b='0.0118/0.0000 0.0471/0.0471 0.0510/0.0549 0.0902/0.1647 0.1255/0.2118 0.1412/0.2353"
 " 0.1529/0.2510 0.1647/0.2706 0.1922/0.3294 0.3412/0.5059 0.5490/0.7569 0.6392/0.8471"
 " 0.7137/0.9216 0.9765/1.0000'")
# radial gain, r normalised so r=1 is the frame corner-ish (hypot of half-extents)
VIGNETTE = [(0.05,1.000),(0.15,0.994),(0.24,0.987),(0.34,0.986),(0.44,0.980),(0.53,0.972),
            (0.63,0.941),(0.72,0.881),(0.82,0.791),(0.92,0.696),(1.01,0.633),(1.11,0.469),
            (1.21,0.345),(1.30,0.259),(1.40,0.260)]
SUBJECT_CX = 918      # Dan's head centre in the 1920-wide source (sd 18px over the roll)
