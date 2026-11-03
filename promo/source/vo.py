import sys, soundfile as sf
from kokoro_onnx import Kokoro
d=sys.argv[1]; voice=sys.argv[2]
k=Kokoro(f"{d}/kokoro-v1.0.onnx", f"{d}/voices-v1.0.bin")
lines=[
 "Ever wondered what's really in your food?",
 "Meet Novi A.I.",
 "Just scan any label,",
 "and A.I. checks every ingredient against your allergies and diet.",
 "In any language.",
 "Set your preferences once.",
 "Ask anything, and discover better alternatives.",
 "Scan smarter. Shop safer.",
 "Novi A.I. Try it free.",
]
for i,l in enumerate(lines):
    s,sr=k.create(l, voice=voice, speed=1.05, lang="en-us")
    sf.write(f"{sys.argv[3]}/vo_{i}.wav", s, sr); print(i, round(len(s)/sr,2), l)
