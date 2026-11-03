import numpy as np, soundfile as sf, sys, os
from scipy import signal
SR = 48000; DUR = 30.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
B = os.path.dirname(os.path.abspath(__file__))

def tt(d): return np.arange(int(d * SR)) / SR
def place(buf, x, t, g=1.0, pan=0.0):
    i = int(t * SR); x = np.array(x, dtype=float)
    k = min(len(x), int(.006 * SR)); fade = np.linspace(1, 0, k)
    if x.ndim == 1: x[-k:] *= fade; x[:16] *= np.linspace(0, 1, min(16, len(x)))
    else: x[-k:] *= fade[:, None]
    if x.ndim == 1:
        l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
        x = np.stack([x * l * 1.414, x * r * 1.414], 1)
    j = min(N, i + len(x));
    if j > i: buf[i:j] += x[:j - i] * g
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b, o=2): return signal.sosfilt(signal.butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)
def env(n, a, d, curve=4):
    t = np.arange(n) / SR; e = np.exp(-t * curve / max(d, 1e-3))
    if a > 0: e *= np.clip(t / a, 0, 1)
    return e
def midi(m): return 440 * 2 ** ((m - 69) / 12)

def reverb_ir(dur=2.2, decay=3.0, seed=1):
    r = np.random.default_rng(seed); n = int(dur * SR); t = np.arange(n) / SR
    ir = r.standard_normal((n, 2)) * np.exp(-t * decay)[:, None]
    ir = lp(ir, 7000); ir[:int(.01 * SR)] *= np.linspace(0, 1, int(.01 * SR))[:, None]
    return ir / np.sqrt((ir ** 2).sum(0))
IR = reverb_ir()
def verb(x, wet=.25, ir=IR):
    if x.ndim == 1: x = np.stack([x, x], 1)
    w = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + w * wet

# ---------- spectral noise sweeps (whoosh / riser) ----------
def sweep_noise(d, f0, f1, bw=.6, shape='bell', seed=0):
    nper = 1024; r = np.random.default_rng(seed); n = int(d * SR)
    frames = n // (nper // 4) + 2; freqs = np.fft.rfftfreq(nper, 1 / SR)
    u = np.linspace(0, 1, frames)
    fc = f0 * (f1 / f0) ** u
    lf = np.log2(np.maximum(freqs, 20))[:, None]
    mag = np.exp(-((lf - np.log2(fc)[None, :]) ** 2) / (2 * bw ** 2))
    if shape == 'bell': amp = np.sin(np.pi * u) ** 1.5
    elif shape == 'rise': amp = u ** 2.2
    else: amp = (1 - u) ** 2
    Z = mag * amp[None, :] * np.exp(2j * np.pi * r.random(mag.shape))
    _, x = signal.istft(Z, fs=SR, nperseg=nper, noverlap=nper * 3 // 4)
    x = x[:n]; return x / (np.abs(x).max() + 1e-9)
def whoosh(d=.7, f0=300, f1=3000, seed=0, pan_from=-.6, pan_to=.6):
    x = sweep_noise(d, f0, f1, .55, 'bell', seed)
    p = np.linspace(pan_from, pan_to, len(x))
    l = np.cos((p + 1) * np.pi / 4); r = np.sin((p + 1) * np.pi / 4)
    return verb(np.stack([x * l, x * r], 1) * 1.2, .3)
def riser(d=1.0, seed=3):
    x = sweep_noise(d, 400, 9000, .5, 'rise', seed) * .7
    t = tt(d); f = 200 * (8 ** (t / d)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / d) ** 2 * .25
    return verb(x + s[:len(x)], .35)
def impact(big=1.0, seed=4):
    d = 2.2; t = tt(d)
    f = 30 + 70 * np.exp(-t * 18); sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    n = np.random.default_rng(seed).standard_normal(len(t))
    crack = lp(n, 3500) * np.exp(-t * 14) * .7
    body = bp(n, 80, 400) * np.exp(-t * 6) * 1.2
    x = sub * 1.1 + crack + body
    x = np.tanh(x * 1.5) * .8
    return verb(x * big, .35)
def sparkle(d=1.4, n=26, seed=5, lo=2500, hi=7000):
    r = np.random.default_rng(seed); out = np.zeros((int(d * SR) + SR, 2))
    for i in range(n):
        st = r.random() ** 1.6 * d * .8; f = r.uniform(lo, hi); dd = r.uniform(.15, .5)
        tn = tt(dd); s = np.sin(2 * np.pi * f * tn) * np.exp(-tn * 9) * (1 - st / d) * r.uniform(.3, 1)
        place_local(out, s, st, r.uniform(-.8, .8))
    return verb(out[:int(d * SR) + SR // 2], .45)
def place_local(buf, x, t, pan):
    i = int(t * SR); l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    j = min(len(buf), i + len(x)); buf[i:j, 0] += x[:j - i] * l; buf[i:j, 1] += x[:j - i] * r
def blip(f0=700, f1=1300, d=.09, wave='sine'):
    t = tt(d + .05); f = f0 + (f1 - f0) * np.clip(t / d, 0, 1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + (.3 * np.sin(2 * ph) if wave == 'rich' else 0)
    return verb(s * env(len(t), .003, d * 1.4, 5), .2)
def ding(base=1318.5):
    def bell(f,d=1.2):
        t=tt(d);return sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t*(4+2*k)) for k,(m,a) in enumerate([(1,1),(2,.35),(3,.12)]))
    s=np.zeros(int(1.3*SR));b1=bell(base);b2=bell(base*1.5);i=int(.07*SR)
    s[:len(b1)]+=b1*.6;s[i:i+len(b2)]+=b2*.55
    return verb(s*.5,.35)
def err():
    out = np.zeros(int(.4 * SR))
    for k, (f, st) in enumerate([(392, 0), (311, .09)]):
        t = tt(.12); s = np.sign(np.sin(2 * np.pi * f * t)) * .4 + np.sin(2 * np.pi * f * t) * .6
        s = lp(s, 2200) * env(len(t), .003, .1, 4)
        i = int(st * SR); out[i:i + len(s)] += s
    return verb(out * .6, .2)
def tick(f=2800, d=.025):
    n = rng.standard_normal(int(d * SR)); t = tt(d)
    s = bp(n, f * .7, min(f * 1.4, 20000)) * np.exp(-t * 180) + np.sin(2 * np.pi * f * t) * np.exp(-t * 220) * .5
    return s
def tap():
    t = tt(.08); s = np.sin(2 * np.pi * (180 + 900 * np.exp(-t * 80)) * t) * np.exp(-t * 60) + tick(4000, .02).tolist().__len__() * 0
    return verb(s * .9 + np.pad(tick(3500, .02), (0, len(t) - int(.02 * SR))) * .6, .15)
def bloop(up=True):
    return blip(420, 980, .11) if up else blip(950, 620, .1)


import json
TLD = json.load(open(f"{B}/tl.json")); DUR = TLD['total']; N = int(SR * DUR)
SCN = {q['id']: q for q in TLD['scenes']}
def S(i): return SCN[i]['s']
def E(i): return SCN[i]['e']
def old2new(to):
    """map a time on the old 30s timeline to the new timeline via scene knots"""
    for q in TLD['scenes']:
        K = q.get('knots')
        if not K: continue
        if K[0][1] - 1e-6 <= to <= K[-1][1] + 1e-6:
            for i in range(1, len(K)):
                (a0, b0), (a1, b1) = K[i - 1], K[i]
                if b0 - 1e-6 <= to <= b1 + 1e-6:
                    u = a0 if b1 - b0 < 1e-6 else a0 + (to - b0) / (b1 - b0) * (a1 - a0)
                    return q['s'] + u
    return None
# ---------- MUSIC ----------
BEAT = .5; T0 = S('C')
mus = np.zeros((N, 2)); drums = np.zeros((N, 2)); bass = np.zeros((N, 2))
def kick():
    t = tt(.45); f = 45 + 110 * np.exp(-t * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7); return np.tanh(s * 1.6)
def clap():
    t = tt(.35); n = rng.standard_normal(len(t)); e = np.zeros_like(t)
    for o in (0, .011, .022): e += (t >= o) * np.exp(-(t - o).clip(0) * 90)
    e += np.exp(-t * 14) * .5; return verb(bp(n, 900, 5000) * e * .5, .3)
def hat():
    t = tt(.05); return hp(rng.standard_normal(len(t)), 7000, 4) * np.exp(-t * 90) * .35
CH = [[53, 57, 60, 64], [55, 59, 62, 67], [57, 60, 64, 69], [48, 55, 60, 64]]; ROOT = [41, 43, 45, 36]
CH_IN = [[57, 60, 64], [53, 57, 60], [57, 60, 64], [55, 59, 62]]  # calmer intro: Am F Am G
def saw(f, d, voices=3, det=.12):
    t = tt(d); s = np.zeros_like(t)
    for v in range(voices):
        ff = f * 2 ** ((v - (voices - 1) / 2) * det / 12); s += 2 * ((ff * t + rng.random()) % 1) - 1
    return s / voices
def pad_chord(notes, d, cut=1600):
    s = sum(saw(midi(m), d) for m in notes) / len(notes); s = lp(s, cut, 2)
    e = np.minimum(1, tt(d) / .6) * np.minimum(1, (d - tt(d)) / .5); return s * e
def pluck(m, d=.6):
    t = tt(d); f = midi(m); s = np.zeros_like(t)
    for h in range(1, 9): s += np.sin(2 * np.pi * f * h * t) / h * np.exp(-t * (7 + h * 3))
    return s * .5
BREAKS = [(S('H') - .5, S('H'))]
def in_break(t): return any(a <= t < b for a, b in BREAKS)
END_DRUMS = S('J') + 2.0
# intro bars (problem part: calm, curious)
k = 0; bt = T0 - 2.0
while bt > -2.0:
    c = (k % 4); d = 2.05
    if bt + d > 0: place(mus, pad_chord(CH_IN[3 - c], d + .3, 900)[max(0, int(-bt * SR)):], max(0, bt), .22)
    for j in range(4):
        st = bt + j * .5
        if st >= 0: place(mus, pluck(CH_IN[3 - c][j % 3] + 12), st, .13, pan=.4 * np.sin(j * 1.7 + k))
    k += 1; bt -= 2.0
nb = int((DUR - T0) / 2) + 1
for b in range(nb):
    bt = T0 + b * 2.0; c = b % 4; d = min(2.05, DUR - bt)
    if d <= 0: break
    final = bt >= S('J') + 2.0
    if not final: place(mus, pad_chord(CH[c], d + .3)[:int((d + .3) * SR)], bt, .26)
    for kk in range(16):
        st = bt + kk * .125
        if st >= END_DRUMS or in_break(st): continue
        if bt < S('E') and kk % 2: continue
        notes = CH[c] + [CH[c][1] + 12]; m = notes[[0, 2, 1, 3, 4, 2, 3, 1][kk % 8]] + 12
        place(mus, pluck(m), st, .16 if kk % 4 else .2, pan=.35 * np.sin(kk * 1.3))
    for kk in range(8):
        st = bt + kk * .25
        if st >= END_DRUMS or in_break(st) or st < S('E'): continue
        place(bass, lp(saw(midi(ROOT[c]), .24, 2, .08), 500) * env(int(.24 * SR), .005, .22, 2), st, .55)
    for kk in range(4):
        st = bt + kk * BEAT
        if st >= END_DRUMS or in_break(st): continue
        place(drums, kick(), st, .9)
        if st >= S('E') and kk % 2 == 1: place(drums, clap(), st, .5)
        if st >= S('E'):
            place(drums, hat(), st + .25, .5, pan=.25); place(drums, hat(), st + .125, .22, pan=-.2); place(drums, hat(), st + .375, .22, pan=-.2)
fin = T0 + np.ceil((END_DRUMS - T0) / 2) * 2
place(mus, pad_chord([48, 55, 60, 64, 67], max(1, DUR - fin + .2)), fin, .3)
place(bass, lp(saw(midi(36), max(1, DUR - fin), 2, .08), 400) * env(int(max(1, DUR - fin) * SR), .01, 2.5, 2), fin, .5)
pump = np.ones(N)
st = T0
while st < END_DRUMS:
    if not in_break(st):
        i = int(st * SR); j = min(N, i + int(.45 * SR)); tl_ = np.arange(j - i) / SR
        pump[i:j] = np.minimum(pump[i:j], 1 - .55 * np.exp(-tl_ * 9))
    st += BEAT
music = (verb(mus, .3) + bass) * pump[:, None] + drums * .8

# ---------- SFX ----------
fxb = np.zeros((N, 2))
def at(t, x, g, pan=0.0):
    if t is not None and 0 <= t < DUR: place(fxb, x, t, g, pan)
def boing(f0=260, d=.55):
    t = tt(d); f = f0 + 260 * (1 - np.exp(-t * 25)) + 70 * np.sin(2 * np.pi * 13 * t) * np.exp(-t * 5)
    ph = 2 * np.pi * np.cumsum(f) / SR; x = (np.sin(ph) + .25 * np.sin(2 * ph)) * env(len(t), .004, d, 4)
    return verb(x * .8, .25)
# A: the problem
a0 = S('A'); sp1 = SCN['A']['split']
at(a0 + .05, whoosh(1.6, 200, 2200, 1, -.9, .6), .3)
at(a0 + .55, whoosh(.7, 180, 1800, 2, 0, 0), .4)
at(a0 + 1.1, blip(700, 1100, .07), .2, .5)
for i in range(4): at(sp1 + .15 + i * .16, blip(900 - i * 60, 520 - i * 40, .12, 'rich'), .2, [.4, -.5, -.3, .5][i])
at(E('A') - .4, whoosh(.45, 2500, 300, 3, .4, -.4), .35)
# B: confusing names
b0 = S('B')
at(b0 + .25, impact(.35, 60), .35)
for i in range(6): at(b0 + .2 + i * .13, blip(500 + 40 * i, 760 + 50 * i, .07), .16, [-.6, .6, -.7, .7, -.5, .5][i])
at(E('B') - .62, riser(.62, 2), .7)
# old-timeline events, re-timed through the scene knots
OLD = [
 (2.7, impact(1.0, 4), .95, 0), (2.72, sparkle(1.4, 30, 5), .32, 0), (2.72, blip(500, 1400, .12, 'rich'), .25, 0), (2.78, boing(), .28, 0),
 (3.92, whoosh(.75, 2500, 250, 6, .3, -.4), .45, 0),
 (4.2, whoosh(.7, 180, 1800, 7, 0, 0), .5, 0), (4.35, sparkle(.7, 10, 8, 3000, 8000), .14, 0), (5.05, tap(), .55, 0),
 (5.28, whoosh(.32, 600, 4000, 9, .5, -.5), .35, 0), (5.62, blip(1200, 1800, .05), .22, 0), (5.72, blip(1500, 2200, .05), .2, 0),
 (6.05, tick(2200), .25, 0), (6.22, tick(2500), .25, 0), (6.4, tick(2800), .25, 0), (6.6, tick(3100), .25, 0),
 (7.15, whoosh(.5, 400, 3500, 11, -.3, .6), .45, 0), (7.72, blip(880, 660, .1, 'rich'), .25, 0), (7.88, boing(), .35, 0), (7.95, whoosh(.3, 800, 3000, 77, .2, .7), .2, 0),
 (8.25, ding(), .5, 0), (11.75, whoosh(.9, 250, 4000, 12, -1, 1), .55, 0),
 (15.3, boing(), .35, 0), (17.35, sparkle(.8, 10, 30), .14, 0), (18.75, whoosh(.5, 2800, 300, 31, -.4, .4), .4, 0),
 (19.2, whoosh(.6, 200, 2000, 32, 0, 0), .45, 0), (23.3, whoosh(.5, 2500, 300, 50, .4, -.4), .4, 0),
 (23.72, impact(.7, 52), .6, 0), (24.97, impact(.5, 53), .45, 0), (26.15, riser(.55, 54), .75, 0),
 (26.7, impact(1.0, 55), .95, 0), (26.72, sparkle(1.6, 34, 56), .35, 0), (26.75, boing(), .25, 0), (27.85, blip(600, 1200, .1, 'rich'), .25, 0), (28.5, sparkle(.6, 10, 57, 4000, 9000), .2, 0),
]
for tm in (8.75, 9.25, 9.75): OLD += [(tm, err(), .4, 0), (tm - .25, whoosh(.3, 800, 3000, int(tm * 10), .2, .7), .2, 0), (tm, boing(340, .3), .12, -.6)]
t = tt(1.2); beam = np.sin(2 * np.pi * (900 + 500 * np.abs(np.sin(np.pi * t / .6))) * t) * .5 + sweep_noise(1.2, 3000, 6000, .4, 'bell', 10) * .3
OLD.append((5.85, verb(beam * np.sin(np.pi * t / 1.2) ** .5 * (0.7 + .3 * np.sin(2 * np.pi * 12 * t)), .3), .09, 0))
for i in range(3):
    OLD += [(15.45 + i * .07, whoosh(.55, 300, 2500, 20 + i, -.5 + .5 * i, -.5 + .5 * i), .1, 0), (15.97 + i * .07, blip(300 + 40 * i, 520 + 60 * i, .07), .14, -.5 + .5 * i)]
    m = [72, 76, 79][i]; OLD += [(16.3 + i * .25, blip(midi(m), midi(m) * 1.5, .06, 'rich'), .22, -.5 + .5 * i), (16.3 + i * .25, boing(380 + 30 * i, .25), .07, 0)]
    OLD += [(21.3 + i * .25, whoosh(.35, 600, 3500, 40 + i, .2, .8), .25, 0), (21.55 + i * .25, blip(900 + i * 150, 1300 + i * 200, .05), .15, .6)]
for to, x, g, pan in OLD: at(old2new(to), x, g, pan)
# H: 12 languages counter
h0 = S('H'); hd = E('H') - h0; c0 = .5; c1 = min(1.9, hd - .9)
at(h0, whoosh(.6, 200, 2200, 70, -.3, .3), .4)
def eo3(x): return 1 - (1 - x) ** 3
prev = 1
for j in range(1, 400):
    u = c0 + (c1 - c0) * j / 400
    kk = min(12, 1 + int(11 * eo3((u - c0) / (c1 - c0)) + 1e-6))
    if kk != prev: at(h0 + u, tick(2000 + kk * 120, .03), .3, (kk % 2 - .5) * .5); at(h0 + u, blip(midi(60 + kk), midi(60 + kk) * 1.2, .05), .08); prev = kk
at(h0 + c1, impact(.6, 71), .55); at(h0 + c1, ding(1567.98), .35); at(h0 + c1 + .02, sparkle(1.0, 18, 72), .25)
at(E('H') - .4, whoosh(.45, 2800, 300, 73, .4, -.4), .35)

# ---------- VOICE ----------
vo = np.zeros((N, 2))
if TLD.get('vo'):
    x, sr = sf.read(TLD['vo'])
    if x.ndim > 1: x = x.mean(1)
    x = signal.resample_poly(x, SR, sr) if sr != SR else x
    x = hp(x, 80); x = x / (np.abs(x).max() + 1e-9)
    e = lp(np.abs(x), 30); g = np.where(e > .25, (.25 + (e - .25) * .35) / np.maximum(e, 1e-6), 1); x = x * g
    x = x + .3 * bp(x, 2500, 6000); x = x / (np.abs(x).max() + 1e-9)
    off = TLD['vo_offset']
    if off < 0: x = x[int(-off * SR):]; off = 0
    place(vo, x, off, .85)
    vo = verb(vo, .06)
ve = lp(np.abs(vo[:, 0]), 6); duck = 1 - .5 * np.clip(ve / .08, 0, 1)
mix = music * .55 * duck[:, None] + fxb * .9 * (1 - .25 * np.clip(ve / .08, 0, 1))[:, None] + vo
fi = np.minimum(1, np.arange(N) / (.05 * SR)); fo = np.clip((DUR - np.arange(N) / SR) / .5, 0, 1)
mix *= (fi * fo)[:, None]; mix = np.tanh(mix * 1.1) / 1.1; mix /= np.abs(mix).max() / .9
out = sys.argv[1] if len(sys.argv) > 1 else f"{B}/mix_tn.wav"
sf.write(out, mix.astype(np.float32), SR, subtype='FLOAT'); print('ok', out, DUR)
