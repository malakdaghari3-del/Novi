"""Build the Tunisian-version timeline from voiceover line timings.

Usage:
  python3 timeline_tn.py draft              -> estimated timings (no recording yet)
  python3 timeline_tn.py vo.wav             -> detect the 9 lines in the recording (pauses between lines)
Writes tl.js (for the page) and tl.json (for audio_tn.py).
"""
import sys, json, os
import numpy as np

B = os.path.dirname(os.path.abspath(__file__))

def detect_lines(path, n_lines=9, min_gap=0.45):
    import soundfile as sf
    from scipy import signal
    x, sr = sf.read(path)
    if x.ndim > 1: x = x.mean(1)
    e = signal.sosfilt(signal.butter(2, 15, 'low', fs=sr, output='sos'), np.abs(x))
    thr = max(np.percentile(e, 20) * 3, e.max() * 0.04)
    hop = int(sr * 0.01); env = e[::hop]; on = env > thr
    segs = []; s = None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None: segs.append([s, i]); s = None
    if s is not None: segs.append([s, len(on)])
    # merge segments separated by gaps shorter than min_gap (pauses inside a sentence)
    merged = []
    for a, b in segs:
        if merged and (a - merged[-1][1]) * 0.01 < min_gap: merged[-1][1] = b
        else: merged.append([a, b])
    merged = [m for m in merged if (m[1] - m[0]) * 0.01 > 0.25]
    # if too many, merge across the smallest gaps until n_lines remain
    while len(merged) > n_lines:
        gaps = [merged[i + 1][0] - merged[i][1] for i in range(len(merged) - 1)]
        k = int(np.argmin(gaps)); merged[k][1] = merged[k + 1][1]; del merged[k + 1]
    lines = [[a * 0.01, b * 0.01] for a, b in merged]
    return lines, len(x) / sr

def inner_split(path, a, b, frac=.55):
    """time of the longest internal pause within [a,b] (for 2-part sentences)"""
    try:
        import soundfile as sf
        from scipy import signal
        x, sr = sf.read(path)
        if x.ndim > 1: x = x.mean(1)
        seg = np.abs(x[int(a * sr):int(b * sr)])
        e = signal.sosfilt(signal.butter(2, 15, 'low', fs=sr, output='sos'), seg)[::int(sr * .01)]
        q = e < max(e.max() * .06, 1e-4); best = (0, 0); s = None
        for i, v in enumerate(q):
            if v and s is None: s = i
            if not v and s is not None:
                if i - s > best[1] - best[0] and s > 30 and i < len(q) - 30: best = (s, i)
                s = None
        if best[1] - best[0] >= 8: return a + best[1] * 0.01
    except Exception:
        pass
    return a + (b - a) * frac

if sys.argv[1] == 'draft':
    est = [(0.6, 5.2), (6.3, 2.8), (9.6, 2.0), (11.8, 1.9), (14.0, 6.2), (20.7, 3.2), (24.2, 3.3), (27.9, 2.8), (31.1, 4.2)]
    L = [[s, s + d] for s, d in est]
    split1 = L[0][0] + (L[0][1] - L[0][0]) * .55
    split9 = L[8][0] + (L[8][1] - L[8][0]) * .5
    vo_offset = 0.0; vo_path = None
else:
    vo_path = sys.argv[1]
    raw, total = detect_lines(vo_path)
    assert len(raw) == 9, f"expected 9 lines, found {len(raw)}: {raw}"
    # the recording is placed so the first line starts at 0.6s
    vo_offset = 0.6 - raw[0][0]
    split1 = inner_split(vo_path, *raw[0]) + vo_offset
    split9 = inner_split(vo_path, *raw[8], frac=.5) + vo_offset
    L = [[a + vo_offset, b + vo_offset] for a, b in raw]

Ls = [l[0] for l in L]; Le = [l[1] for l in L]
sc = []
def add(id, s, e, **kw): sc.append(dict(id=id, s=round(s, 3), e=round(e, 3), **kw))
A_e = Ls[1] - .3; add('A', 0, A_e, split=round(split1, 3))
B_e = Ls[2] - .15; add('B', A_e, B_e)
C_e = Ls[4] - .2; add('C', B_e, C_e, l4=round(Ls[3] - B_e, 3))
E_e = Ls[5] - .2; add('E', C_e, E_e)
F_e = Ls[6] - .2; add('F', E_e, F_e)
G_e = Ls[7] - .2; add('G', F_e, G_e)
H_e = Ls[8] - .2; add('H', G_e, H_e)
I_e = max(Le[8] + .45, H_e + 3.2); add('I', H_e, I_e, split=round(split9 - H_e, 3))
J_e = I_e + 3.8; add('J', I_e, J_e)

def knots(s):
    d = s['e'] - s['s']; i = s['id']
    if i == 'C':
        l4 = s['l4']
        return [[0, 2.7], [.6, 3.25], [max(.7, l4 - .1), 3.3], [max(.8, l4 + .5), 3.9], [max(.9, d - .4), 3.94], [d, 4.3]]
    if i == 'E':
        r = min(max(d * .42, 2.6), 3.2)
        return [[0, 4.2], [r, 7.2], [min(r + 2.7, d - .5), 9.9], [d - .45, 11.75], [d, 12.2]]
    if i == 'F': return [[0, 15.2], [d - .45, 18.75], [d, 19.2]]
    if i == 'G': return [[0, 19.2], [.55, 19.75], [.6, 21.1], [d - .45, 23.3], [d, 23.75]]
    if i == 'I':
        sp = min(max(s['split'], .9), d - 1.2)
        return [[0, 23.7], [sp - .05, 24.9], [d - .55, 26.15], [d, 26.7]]
    if i == 'J': return [[0, 26.7], [d - .5, 29.5], [d, 30]]
    return None
for s in sc:
    k = knots(s)
    if k: s['knots'] = [[round(a, 3), round(b, 3)] for a, b in k]

tl = dict(total=round(J_e, 3), lines=[[round(a, 3), round(b, 3)] for a, b in L], scenes=sc, vo=vo_path, vo_offset=round(vo_offset, 3))
open(f"{B}/tl.json", 'w').write(json.dumps(tl, indent=1))
open(f"{B}/tl.js", 'w').write("window.TL=" + json.dumps(tl) + ";")
print(json.dumps(dict(total=tl['total'], scenes=[(s['id'], s['s'], s['e']) for s in sc]), indent=None))
