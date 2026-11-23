"""Original sound effects for the Wick classroom sound library.
Every sound here is generated from scratch by this script, so the set can be
shared freely (released under CC0)."""
import json, os, re, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
rng = np.random.default_rng(7)

def T(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def sweep(f0, f1, d, curve='exp'):
    t = T(d)
    f = f0 * (f1 / f0) ** (t / d) if curve == 'exp' else f0 + (f1 - f0) * t / d
    return f
def osc(freq, kind='sine'):
    ph = 2 * np.pi * np.cumsum(freq) / SR
    if kind == 'sine': return np.sin(ph)
    if kind == 'square': return np.sign(np.sin(ph)) * 0.6
    if kind == 'saw': return ((ph / (2 * np.pi)) % 1) * 2 - 1
    if kind == 'tri': return 2 * np.abs(((ph / (2 * np.pi)) % 1) * 2 - 1) - 1
def env(n, a=0.005, r=None, d=None):
    e = np.ones(n); ai = max(1, int(a * SR)); e[:ai] = np.linspace(0, 1, ai)
    if d is not None: e *= np.exp(-np.arange(n) / SR / d)
    if r: ri = min(n, int(r * SR)); e[-ri:] *= np.linspace(1, 0, ri)
    return e
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def tv_bp(x, centers, q=4, block=256):
    """Band-pass with a moving center frequency (block by block)."""
    y = np.zeros_like(x)
    for i in range(0, len(x), block):
        c = centers[min(i, len(centers) - 1)]
        lo, hi = max(30, c / (1 + 1 / q)), min(SR / 2 - 100, c * (1 + 1 / q))
        y[i:i + block] = bp(x[max(0, i - 2048):i + block], lo, hi)[-len(x[i:i + block]):]
    return y
def at(total, *parts):
    out = np.zeros(int(SR * total))
    for start, sig in parts:
        s = int(SR * start); n = min(len(sig), len(out) - s)
        out[s:s + n] += sig[:n]
    return out
def mix(*s):
    n = max(len(x) for x in s); out = np.zeros(n)
    for x in s: out[:len(x)] += x
    return out
def bell(f, d, partials=((1, 1), (2.76, .5), (5.4, .25), (8.93, .12))):
    t = T(d)
    return sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * (3 + m)) for m, a in partials)
def note(f, d, kind='square', dec=None):
    s = osc(np.full(int(SR * d), f), kind); return s * env(len(s), 0.004, 0.03, dec)
def woodblock(f=800, d=0.12):
    t = T(d)
    return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.3 * t)) * np.exp(-t * 45) + hp(noise(d), 2000) * np.exp(-t * 200) * .4
def thump(f0=110, f1=40, d=0.35):
    s = osc(sweep(f0, f1, d)) * env(int(SR * d), 0.002, d=d / 3)
    return mix(s, lp(noise(d), 400) * env(int(SR * d), 0.001, d=0.03) * .6)
def snare(d=0.18):
    t = T(d)
    return bp(noise(d), 1200, 7000) * np.exp(-t * 25) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 35) * .5

S = {}
def add(cat, name, sig):
    S[(cat, name)] = sig

# ---------- Cartoon ----------
d = 1.1; t = T(d)
add('Cartoon', 'Boing', osc(220 + 140 * np.exp(-t * 3) * np.sin(2 * np.pi * 14 * t) + 120 * np.exp(-t * 2)) * env(len(t), .003, d=.45))
d = 0.7; t = T(d)
add('Cartoon', 'Spring', osc(500 + 320 * np.exp(-t * 4) * np.sin(2 * np.pi * 22 * t), 'tri') * env(len(t), .002, d=.25))
d = 0.12
add('Cartoon', 'Pop', osc(sweep(1400, 180, d)) * env(int(SR * d), .001, d=.04) + hp(noise(d), 3000) * env(int(SR * d), .0005, d=.005) * .5)
d = 0.9; t = T(d)
add('Cartoon', 'Slide Whistle Up', osc(sweep(380, 1700, d) * (1 + .02 * np.sin(2 * np.pi * 6 * t))) * env(len(t), .03, .1) * .8 + .03 * noise(d) * env(len(t), .03, .1))
add('Cartoon', 'Slide Whistle Down', osc(sweep(1700, 380, d) * (1 + .02 * np.sin(2 * np.pi * 6 * t))) * env(len(t), .03, .1) * .8 + .03 * noise(d) * env(len(t), .03, .1))
sq = lambda: osc(sweep(1800, 2600, .09, 'lin'), 'tri') * env(int(SR * .09), .005, .03)
add('Cartoon', 'Squeak', at(.3, (0, sq()), (.13, sq())))
add('Cartoon', 'Bonk', mix(woodblock(620, .25), thump(160, 70, .2) * .6))
d = 1.0; t = T(d)
add('Cartoon', 'Wobble', osc(300 + 90 * np.sin(2 * np.pi * 9 * t), 'tri') * env(len(t), .02, .2))
d = 0.25
add('Cartoon', 'Zip', tv_bp(noise(d), sweep(800, 7000, d), q=3) * env(int(SR * d), .01, .05) * 2.5)
add('Cartoon', 'Zoom Away', tv_bp(noise(.7), sweep(3000, 300, .7), q=5) * env(int(SR * .7), .01, .3, .3) * 3 + osc(sweep(900, 200, .7)) * env(int(SR * .7), .01, .3, .2) * .3)
add('Cartoon', 'Running Feet', at(1.3, *[(i * .075, woodblock(900 + 200 * (i % 2), .06) * .7) for i in range(16)]))

# ---------- Movement ----------
for name, d, f0, f1 in [('Whoosh Fast', .35, 400, 2500), ('Whoosh Slow', 1.0, 300, 1800), ('Swish', .2, 2000, 5000)]:
    n = int(SR * d); bell_env = np.sin(np.pi * np.arange(n) / n) ** 2
    add('Movement', name, tv_bp(noise(d), np.concatenate([sweep(f0, f1, d / 2), sweep(f1, f0 * 1.2, d / 2)]), q=2.5) * bell_env * 3)
add('Movement', 'Jump', osc(sweep(250, 900, .22), 'square') * env(int(SR * .22), .002, .05) * .6)
add('Movement', 'Land', mix(thump(130, 45, .4), lp(noise(.15), 1200) * env(int(SR * .15), .001, d=.03) * .5))
add('Movement', 'Footsteps', at(2.2, *[(i * .5, mix(thump(120, 60, .12) * .7, bp(noise(.08), 300, 2500) * env(int(SR * .08), .001, d=.02) * .5)) for i in range(4)]))
add('Movement', 'Tiptoe', at(1.6, *[(i * .38, woodblock(1500 + 150 * (i % 2), .05) * .35) for i in range(4)]))
d = .6
add('Movement', 'Fall', osc(sweep(1400, 250, d)) * env(int(SR * d), .01, .05) * .5)

# ---------- Hits & Crashes ----------
add('Hits & Crashes', 'Punch', mix(thump(150, 50, .25), lp(noise(.12), 3000) * env(int(SR * .12), .001, d=.02) * .9))
add('Hits & Crashes', 'Thud', thump(90, 35, .5))
d = 1.6
cr = hp(noise(d), 2500) * env(int(SR * d), .001, d=.35) + sum(np.sin(2 * np.pi * f * T(d)) * np.exp(-T(d) * 4) * .15 for f in (1730, 2410, 3330, 4710))
add('Hits & Crashes', 'Crash', mix(cr, thump(100, 40, .4) * .7))
d = 2.5
ex = lp(noise(d), 900, 4) * env(int(SR * d), .003, d=.6) * 2.2 + osc(sweep(70, 30, d)) * env(int(SR * d), .002, d=.5)
add('Hits & Crashes', 'Explosion', ex)
add('Hits & Crashes', 'Knock Knock', at(1.0, *[(s, mix(woodblock(260, .15) * .9, thump(140, 80, .1) * .5)) for s in (0, .22, .44)]))
add('Hits & Crashes', 'Glass Clink', bell(2350, 1.2, ((1, 1), (2.32, .6), (4.25, .3), (6.63, .2))) * .6)
d = .5
add('Hits & Crashes', 'Splat', mix(lp(noise(d), 1500) * env(int(SR * d), .002, d=.08) * 1.5, osc(sweep(300, 60, .15)) * env(int(SR * .15), .002, d=.05) * .6))

# ---------- Bells & Tones ----------
add('Bells & Tones', 'Ding', bell(1320, 2.0))
add('Bells & Tones', 'Chime', at(2.2, (0, bell(1047, 1.8)), (.15, bell(1319, 1.8)), (.3, bell(1568, 1.9))))
C5, E5, G5, C6 = 523.25, 659.25, 783.99, 1046.5
add('Bells & Tones', 'Success', at(1.2, (0, note(C5, .12)), (.12, note(E5, .12)), (.24, note(G5, .12)), (.36, note(C6, .6, dec=.3))))
def trombone(f, d):
    t = T(d); return lp(osc(f * (1 + .012 * np.sin(2 * np.pi * 5 * t)), 'saw'), 1400) * env(len(t), .03, .08)
add('Bells & Tones', 'Fail (Wah Wah)', at(2.4, (0, trombone(311, .4)), (.45, trombone(293, .4)), (.9, trombone(277, .4)), (1.35, trombone(262, 1.0))))
add('Bells & Tones', 'Coin', at(.5, (0, note(988, .08)), (.08, note(1319, .4, dec=.15))))
add('Bells & Tones', 'Magic Sparkle', at(1.8, *[(i * .09 + rng.uniform(0, .04), bell(rng.uniform(1800, 4200), .6) * .35) for i in range(14)]))
add('Bells & Tones', 'Alarm', np.concatenate([note(880 if i % 2 == 0 else 660, .25, 'square') for i in range(8)]) * .5)
add('Bells & Tones', 'Click', mix(hp(noise(.02), 2000) * env(int(SR * .02), .0005, d=.003), woodblock(2000, .03) * .3))
add('Bells & Tones', 'Countdown', at(4.0, *[(i, note(880, .15, 'sine') * .7) for i in range(3)], (3, note(1760, .6, 'sine', .3) * .8)))
add('Bells & Tones', 'Camera Shutter', at(.25, (0, hp(noise(.03), 1500) * env(int(SR * .03), .001, d=.006)), (.09, hp(noise(.05), 1000) * env(int(SR * .05), .001, d=.01) * 1.2)))

# ---------- Sci-Fi & Game ----------
add('Sci-Fi & Game', 'Laser', osc(sweep(1800, 180, .3)) * env(int(SR * .3), .002, d=.12))
add('Sci-Fi & Game', 'Laser Blast', osc(sweep(2400, 120, .45), 'square') * env(int(SR * .45), .002, d=.15) * .6)
add('Sci-Fi & Game', 'Power Up', np.concatenate([note(f, .07) for f in (262, 330, 392, 523, 659, 784, 1047)]) * .7)
add('Sci-Fi & Game', 'Power Down', osc(sweep(900, 80, 1.0), 'square') * env(int(SR * 1.0), .01, .2) * .5)
d = 1.2; t = T(d)
add('Sci-Fi & Game', 'Teleport', osc(sweep(200, 2400, d) * (1 + .3 * np.sin(2 * np.pi * 30 * t))) * env(len(t), .05, .3) * .6)
add('Sci-Fi & Game', 'Robot Beeps', np.concatenate([note(rng.choice([440, 587, 659, 784, 988, 1175]), .09, 'square') * (i % 3 != 2) for i in range(12)]) * .5)
d = 2.0; t = T(d)
add('Sci-Fi & Game', 'Warp', (osc(sweep(80, 600, d), 'saw') * .3 + tv_bp(noise(d), sweep(300, 4000, d), q=6) * 2) * env(len(t), .4, .4))
add('Sci-Fi & Game', 'Game Over', at(1.6, (0, note(392, .25)), (.27, note(330, .25)), (.54, note(262, .8, dec=.5))))

# ---------- Music Bits ----------
roll = []; s = 0.0; gap = .09
while s < 1.8: roll.append((s, snare(.12) * (.4 + .6 * s / 1.8))); gap = max(.035, gap * .93); s += gap
add('Music Bits', 'Drum Roll', at(2.6, *roll, (1.85, mix(hp(noise(.8), 3000) * env(int(SR * .8), .001, d=.3), thump(100, 45, .4)))))
add('Music Bits', 'Ba Dum Tss', at(1.5, (0, snare()), (.18, thump(110, 50, .3) * .9), (.42, hp(noise(1.0), 4000) * env(int(SR * 1.0), .001, d=.25) * .8)))
add('Music Bits', 'Cymbal', hp(noise(2.0), 3500) * env(int(SR * 2.0), .001, d=.5))
add('Music Bits', 'Kick Drum', thump(120, 45, .45))
add('Music Bits', 'Clap', at(.3, *[(i * .011, bp(noise(.08), 900, 4000) * env(int(SR * .08), .001, d=.015)) for i in range(3)]) * 1.5)
add('Music Bits', 'Heartbeat', at(2.0, (0, thump(70, 40, .2)), (.22, thump(60, 35, .2) * .8), (1.0, thump(70, 40, .2)), (1.22, thump(60, 35, .2) * .8)) * 1.4)
add('Music Bits', 'Tick Tock', at(4.0, *[(i * .5, woodblock(1800 if i % 2 == 0 else 1300, .06) * .6) for i in range(8)]))

# ---------- Nature ----------
d = 5.0; t = T(d)
add('Nature', 'Wind', tv_bp(noise(d), 500 + 350 * np.sin(2 * np.pi * .23 * t) + 150 * np.sin(2 * np.pi * .61 * t), q=1.5) * (0.6 + .4 * np.sin(2 * np.pi * .31 * t)) * env(len(t), .8, .8) * 2.5)
rain = lp(hp(noise(d), 800), 6000) * .25
for _ in range(400):
    s = rng.integers(0, len(rain) - 600); rain[s:s + 600] += hp(noise(600 / SR), 2500) * np.exp(-np.arange(600) / 60) * rng.uniform(.1, .5)
add('Nature', 'Rain', rain * env(len(rain), .6, .6))
add('Nature', 'Water Drop', mix(osc(sweep(500, 1400, .08)) * env(int(SR * .08), .001, d=.03), osc(np.full(int(SR * .2), 1300)) * env(int(SR * .2), .001, d=.04) * .3))
add('Nature', 'Bubbles', at(1.6, *[(rng.uniform(0, 1.4), osc(sweep(rng.uniform(300, 700), rng.uniform(900, 1800), .06)) * env(int(SR * .06), .001, d=.02) * .6) for _ in range(14)]))
d = 4.0
add('Nature', 'Thunder', mix(lp(noise(d), 300, 4) * env(int(SR * d), .05, d=1.2) * (1 + .6 * np.abs(lp(noise(d), 3))) * 6, lp(noise(.25), 2500) * env(int(SR * .25), .001, d=.05) * .6))
fire = lp(noise(d), 700) * .7
for _ in range(120):
    s = rng.integers(0, len(fire) - 300); fire[s:s + 300] += hp(noise(300 / SR), 1500) * np.exp(-np.arange(300) / 25) * rng.uniform(.3, 1)
add('Nature', 'Campfire', fire * env(len(fire), .4, .4))

os.makedirs(OUT, exist_ok=True)
catalog = []
for (cat, name), sig in S.items():
    sig = np.asarray(sig, dtype=float)
    fade = min(len(sig) // 4, int(.01 * SR)); sig[-fade:] *= np.linspace(1, 0, fade)
    peak = np.max(np.abs(sig)) + 1e-9; rms = np.sqrt(np.mean(sig ** 2)) + 1e-9
    sig = sig * min(0.89 / peak, 10 ** (-15 / 20) / rms)  # aim for even loudness, never clip
    slug = re.sub('-+', '-', ''.join(ch if ch.isalnum() else '-' for ch in name.lower())).strip('-')
    folder = os.path.join(OUT, re.sub('-+', '-', ''.join(ch if ch.isalnum() else '-' for ch in cat.lower())))
    os.makedirs(folder, exist_ok=True)
    wav = '/tmp/_sfx.wav'; wavfile.write(wav, SR, (sig * 32767).astype(np.int16))
    mp3 = os.path.join(folder, slug + '.mp3')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-codec:a', 'libmp3lame', '-b:a', '96k', mp3], check=True)
    catalog.append({'category': cat, 'name': name, 'file': os.path.relpath(mp3, OUT), 'seconds': round(len(sig) / SR, 2), 'credit': 'Original sound made for this site', 'license': 'CC0'})
json.dump(catalog, open(os.path.join(OUT, 'made-here.json'), 'w'), indent=1)
print(len(catalog), 'sounds')
