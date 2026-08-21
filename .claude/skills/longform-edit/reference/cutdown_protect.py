"""Hard source spans no deletion may touch: every J2 chip's anchor sentence, every
v2/v3 insert's beat, the Abs-By-AI plugs and the outro CTA."""
CHIP_SRC = [3.0, 9.6, 392.7, 628.3, 742.5, 931.5, 1233.5, 1346.8, 1464.9, 1570.8,
            1612.4, 1699.6, 1858.3, 1979.0, 2105.5, 2270.0, 2499.0, 2664.5, 2789.0,
            2967.3, 3078.0, 3258.5, 3419.7, 3547.2, 3597.0, 3799.0, 4066.0]
PROTECT = [
    (1521.9, 1565.2, "absbyai-tracking-plug"),
    (1531.0, 1537.4, "soup-split-insert"),
    (1855.0, 1868.0, "placeholder-corner"),
    (1884.0, 1912.0, "placeholder-fullscreen"),
    (2668.9, 2675.2, "oura-card"),
    (2716.6, 2722.6, "whoop-card"),
    (3056.5, 3060.2, "supplements-card"),
    (3800.0, 3808.6, "bryan-johnson-pip"),
    (4062.0, 4127.0, "outro-cta"),
]

# CHIP_SRC is asserted exactly: each chip's anchor word must survive in a
# kept range of the finished EDL (an interval test false-alarms whenever a cut
# merely ENDS where a chip's sentence begins).
