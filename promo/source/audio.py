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

# ---------- MUSIC ----------
BPM = 120; BEAT = .5; T0 = 2.7
mus = np.zeros((N, 2)); drums = np.zeros((N, 2)); bass = np.zeros((N, 2))
def kick():
    t = tt(.45); f = 45 + 110 * np.exp(-t * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s[:int(.004 * SR)] += rng.standard_normal(int(.004 * SR)) * .3
    return np.tanh(s * 1.6)
def clap():
    t = tt(.35); n = rng.standard_normal(len(t)); e = np.zeros_like(t)
    for o in (0, .011, .022): e += (t >= o) * np.exp(-(t - o).clip(0) * 90)
    e += np.exp(-t * 14) * .5
    return verb(bp(n, 900, 5000) * e * .5, .3)
def hat(op=False):
    d = .2 if op else .05; t = tt(d); n = rng.standard_normal(len(t))
    return hp(n, 7000, 4) * np.exp(-t * (18 if op else 90)) * .35
# progression: F  G  Am  C  (2s each = 1 bar)
CH = [[53, 57, 60, 64], [55, 59, 62, 67], [57, 60, 64, 69], [48, 55, 60, 64]]
ROOT = [41, 43, 45, 36]
def saw(f, d, voices=3, det=.12):
    t = tt(d); s = np.zeros_like(t)
    for v in range(voices):
        ff = f * 2 ** ((v - (voices - 1) / 2) * det / 12)
        ph = (ff * t + rng.random()) % 1; s += 2 * ph - 1
    return s / voices
def pad_chord(notes, d):
    s = sum(saw(midi(m), d) for m in notes) / len(notes)
    s = lp(s, 1600, 2); e = np.minimum(1, tt(d) / .6) * np.minimum(1, (d - tt(d)) / .5)
    return s * e
def pluck(m, d=.6):
    t = tt(d); f = midi(m); s = np.zeros_like(t)
    for h in range(1, 9): s += np.sin(2 * np.pi * f * h * t) / h * np.exp(-t * (7 + h * 3))
    return s * .5

def bar_of(t): return int(np.floor((t - T0) / 2.0))
# intro pad swell 0..2.7 (Am -> G feel) quiet
place(mus, lp(pad_chord([57, 60, 64, 69], 2.9), 900) * np.linspace(0, 1, int(2.9 * SR)) ** 2 * .5, 0)
END_DRUMS = 28.7
for b in range(0, 14):
    bt = T0 + b * 2.0
    if bt >= 30: break
    c = b % 4
    # pads
    d = min(2.05, 30 - bt)
    g = .26 if bt < 26.7 else .32
    if 23.2 <= bt < 23.7: pass
    place(mus, pad_chord(CH[c], d + .3)[:int((d + .3) * SR)], bt, g)
    for k in range(16):  # 8ths arpeggio (16 per bar = 16ths? use 8ths -> 4 per beat? keep 8ths)
        st = bt + k * .125
        if st >= 29.0 or (23.2 <= st < 23.7) or (26.2 <= st < 26.7): continue
        if bt < 4.2 and k % 2: continue
        notes = CH[c] + [CH[c][1] + 12]
        m = notes[[0, 2, 1, 3, 4, 2, 3, 1][k % 8]] + 12
        place(mus, pluck(m), st, .16 if k % 4 else .2, pan=.35 * np.sin(k * 1.3))
    for k in range(8):  # bass 8ths
        st = bt + k * .25
        if st >= END_DRUMS or (23.2 <= st < 23.7) or (26.2 <= st < 26.7) or st < 4.2: continue
        s = lp(saw(midi(ROOT[c]), .24, 2, .08), 500) * env(int(.24 * SR), .005, .22, 2)
        place(bass, s, st, .55)
    for k in range(4):  # drums per beat
        st = bt + k * BEAT
        if st >= END_DRUMS or (23.2 <= st < 23.7) or (26.2 <= st < 26.7): continue
        if st < 7.2 and k % 2: pass
        place(drums, kick(), st, .9)
        if st >= 7.2 and k % 2 == 1: place(drums, clap(), st, .5)
        if st >= 4.2:
            place(drums, hat(), st + .25, .5, pan=.25)
            if st >= 7.2: place(drums, hat(), st + .125, .22, pan=-.2); place(drums, hat(), st + .375, .22, pan=-.2)
# final chord ring
place(mus, pad_chord([48, 55, 60, 64, 67], 3.0), 28.7, .3)
place(bass, lp(saw(midi(36), 2.5, 2, .08), 400) * env(int(2.5 * SR), .01, 2.5, 2), 28.7, .5)

# sidechain pump on music/bass from kick grid
pump = np.ones(N); t_all = np.arange(N) / SR
for k in range(200):
    st = T0 + k * BEAT
    if st >= END_DRUMS: break
    if (23.2 <= st < 23.7) or (26.2 <= st < 26.7): continue
    i = int(st * SR); j = min(N, i + int(.45 * SR)); tl = (np.arange(j - i)) / SR
    pump[i:j] = np.minimum(pump[i:j], 1 - .55 * np.exp(-tl * 9))
music = (verb(mus, .3) + bass) * pump[:, None] + drums * .8

# ---------- SFX ----------
fxb = np.zeros((N, 2))
place(fxb, whoosh(1.9, 200, 2500, 1, -.9, .7), .1, .35)
place(fxb, riser(.65, 2), 2.07, .7)
place(fxb, impact(1.0, 4), 2.7, .95)
place(fxb, sparkle(1.4, 30, 5), 2.72, .32)
place(fxb, blip(500, 1400, .12, 'rich'), 2.72, .25)
place(fxb, whoosh(.75, 2500, 250, 6, .3, -.4), 3.9, .45)
place(fxb, whoosh(.7, 180, 1800, 7, 0, 0), 4.2, .5)
place(fxb, sparkle(.7, 10, 8, 3000, 8000), 4.35, .14)
place(fxb, tap(), 5.05, .55)
place(fxb, whoosh(.32, 600, 4000, 9, .5, -.5), 5.28, .35)
place(fxb, blip(1200, 1800, .05), 5.62, .22); place(fxb, blip(1500, 2200, .05), 5.72, .2)
t = tt(1.2); beam = np.sin(2 * np.pi * (900 + 500 * np.abs(np.sin(np.pi * t / .6))) * t) * .5 + sweep_noise(1.2, 3000, 6000, .4, 'bell', 10) * .3
place(fxb, verb(beam * np.sin(np.pi * t / 1.2) ** .5 * (0.7 + .3 * np.sin(2 * np.pi * 12 * t)), .3), 5.85, .09)
for k, tm in enumerate([6.05, 6.22, 6.4, 6.6]): place(fxb, tick(2200 + k * 300), tm, .25)
place(fxb, whoosh(.5, 400, 3500, 11, -.3, .6), 7.15, .45)
place(fxb, blip(880, 660, .1, 'rich'), 7.72, .25)
place(fxb, ding(), 8.25, .5)
for tm in (8.75, 9.25, 9.75): place(fxb, err(), tm, .4); place(fxb, whoosh(.3, 800, 3000, int(tm * 10), .2, .7), tm - .25, .2)
place(fxb, whoosh(.3, 800, 3000, 77, .2, .7), 7.95, .2)
place(fxb, whoosh(.9, 250, 4000, 12, -1, 1), 11.75, .6)
for k in range(10): place(fxb, tick(2400 + (k % 3) * 400, .03), 12.3 + k * .19, .32, pan=(k % 2 - .5) * .4)
place(fxb, riser(.45, 13), 13.77, .4)
place(fxb, impact(.6, 14), 14.2, .6)
place(fxb, ding(1567.98), 14.22, .35)
place(fxb, sparkle(1.0, 18, 15), 14.22, .25)
place(fxb, whoosh(.5, 3000, 300, 16, .5, -.5), 14.9, .4)
for i in range(6): place(fxb, whoosh(.55, 300, 2500, 20 + i, -.8 + .32 * i, -.8 + .32 * i), 15.45 + i * .07, .1)
for i in range(6): place(fxb, blip(300 + 40 * i, 520 + 60 * i, .07), 15.97 + i * .07, .14, pan=-.7 + .28 * i)
SC = [72, 74, 76, 79, 81, 84]
for i in range(6): place(fxb, blip(midi(SC[i]), midi(SC[i]) * 1.5, .06, 'rich'), 16.3 + i * .25, .2, pan=-.7 + .28 * i)
place(fxb, sparkle(.8, 10, 30), 17.35, .14)
place(fxb, whoosh(.5, 2800, 300, 31, -.4, .4), 18.75, .4)
place(fxb, whoosh(.6, 200, 2000, 32, 0, 0), 19.2, .45)
place(fxb, blip(1000, 1400, .05), 19.8, .15)
place(fxb, bloop(True), 20.0, .4)
for k in range(13): place(fxb, tick(3200 + (k * 37 % 5) * 200, .015), 20.07 + k * .042, .12, pan=-.4)
place(fxb, bloop(False), 21.15, .4)
for i in range(3): place(fxb, whoosh(.35, 600, 3500, 40 + i, .2, .8), 21.3 + i * .25, .25); place(fxb, blip(900 + i * 150, 1300 + i * 200, .05), 21.55 + i * .25, .15, pan=.6)
place(fxb, whoosh(.5, 2500, 300, 50, .4, -.4), 23.3, .4)
place(fxb, riser(.45, 51), 23.25, .35)
place(fxb, impact(.7, 52), 23.72, .6)
place(fxb, impact(.5, 53), 24.97, .45)
place(fxb, riser(.55, 54), 26.15, .75)
place(fxb, impact(1.0, 55), 26.7, .95)
place(fxb, sparkle(1.6, 34, 56), 26.72, .35)
place(fxb, blip(600, 1200, .1, 'rich'), 27.85, .25)
place(fxb, sparkle(.6, 10, 57, 4000, 9000), 28.5, .2)

def boing(f0=260, d=.55):
    t = tt(d); f = f0 + 260 * (1 - np.exp(-t * 25)) + 70 * np.sin(2 * np.pi * 13 * t) * np.exp(-t * 5)
    ph = 2 * np.pi * np.cumsum(f) / SR; x = (np.sin(ph) + .25 * np.sin(2 * ph)) * env(len(t), .004, d, 4)
    return verb(x * .8, .25)
for tm, g in [(2.78, .28), (7.88, .35), (15.3, .35), (26.75, .25)]: place(fxb, boing(), tm, g)
for tm in (8.75, 9.25, 9.75): place(fxb, boing(340, .3), tm, .12, pan=-.6)
for i in range(6): place(fxb, boing(380 + 30 * i, .25), 16.3 + i * .25, .07)
# ---------- VOICE ----------
def load_vo(i):
    x, sr = sf.read(f"{B}/vo/vo_{i}.wav"); x = signal.resample_poly(x, SR, sr)
    x = hp(x, 90); x = x / np.abs(x).max()
    # gentle compression
    e = np.abs(signal.hilbert(x)); e = lp(e, 30); g = np.where(e > .3, (.3 + (e - .3) * .4) / np.maximum(e, 1e-6), 1)
    x = x * g; # presence boost
    x = x + .35 * bp(x, 2500, 6000)
    return x / np.abs(x).max()
def find_gap(x):  # longest internal silence (sec)
    e = lp(np.abs(x), 20); q = e < .02; best = (0, 0); s = None
    for i, v in enumerate(q[::48]):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s > best[1] - best[0] and s > 20: best = (s, i)
            s = None
    return best[0] * 48 / SR, best[1] * 48 / SR
VO_T = {0: .4, 1: 2.95, 2: 4.6, 3: 6.9, 4: 12.45, 5: 15.5, 6: 19.5, 8: 27.3}
vo = np.zeros((N, 2))
for i, st in VO_T.items(): place(vo, load_vo(i), st, .8)
x7 = load_vo(7); g0, g1 = find_gap(x7); st7 = 24.97 - g1 + .02; print('vo7 gap', g0, g1, 'start', st7)
place(vo, x7, st7, .8)
vo = verb(vo, .08)
# ducking
ve = lp(np.abs(vo[:, 0]), 6); duck = 1 - .5 * np.clip(ve / .08, 0, 1)
mix = music * .55 * duck[:, None] + fxb * .9 * (1 - .25 * np.clip(ve / .08, 0, 1))[:, None] + vo * 1.0
# fades
fi = np.minimum(1, np.arange(N) / (.05 * SR)); fo = np.clip((DUR - np.arange(N) / SR) / .5, 0, 1)
mix *= (fi * fo)[:, None]
mix = np.tanh(mix * 1.1) / 1.1
mix /= np.abs(mix).max() / .9
sf.write(f"{B}/mix.wav", mix.astype(np.float32), SR, subtype='FLOAT')
sf.write(f"{B}/music_only.wav", (music * .55 * (fi * fo)[:, None]).astype(np.float32), SR, subtype='FLOAT')
print('ok')
