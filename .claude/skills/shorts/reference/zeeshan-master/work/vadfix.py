"""Shared: move a word's onset/offset out of MEASURED silence (work/vad.py gaps): the three
fixonsets.py rules. CTC can place a word inside, or across, the pause next to it (short1 "even":
CTC 23.12 spanning a 0.39 s silence that ends 23.56; short3 "then" spanning a 0.22 s one)."""
def vadfix(words, gaps, key_t='t', key_e='e'):
    n = 0
    for w in words:
        s, e = w[key_t], w[key_e]
        moved = False
        for g0, g1 in gaps:                       # 1. onset inside a gap -> gap end
            if g0 < s < g1 and g1 < e:
                w[key_t] = round(g1, 3); n += 1; moved = True; break
        if not moved:                             # 3. a word wholly containing a gap >= 0.2 s begins after it
            for g0, g1 in gaps:
                if g0 > s + 0.02 and g1 < e - 0.02 and g1 - g0 >= 0.2:
                    w[key_t] = round(g1, 3); n += 1; break
        s, e = w[key_t], w[key_e]
        for g0, g1 in gaps:                       # 2. offset inside a gap -> gap start
            if g0 < e < g1 and g0 > s:
                w[key_e] = round(g0, 3); break
    return n
