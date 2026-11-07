#!/usr/bin/env python3
"""Transcribe audio/video with Whisper (faster-whisper).

Writes to transcripts/<name>.{txt,srt,vtt,json,words.json}:
  .txt         plain text
  .srt / .vtt  subtitle files (one cue per Whisper segment)
  .json        segments with word timings
  .words.json  flat word list in HyperFrames format:
               [{"id": "w0", "text": "Hello", "start": 0.0, "end": 0.5}, ...]
               Import into a motion project with:
               cp transcripts/<name>.words.json motion/assets/ && (cd motion && npx hyperframes transcribe assets/<name>.words.json)

Usage:
  scripts/transcribe.py <file> [--model small] [--language en] [--translate]
Models: tiny, base, small (default), medium, large-v3, turbo  (.en variants for English only)
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ts(t: float, sep: str) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input")
    p.add_argument("--model", default="small")
    p.add_argument("--language", default=None, help="language code, e.g. en, ar, es (auto-detect if omitted)")
    p.add_argument("--translate", action="store_true", help="translate speech to English")
    p.add_argument("--out", default=str(ROOT / "transcripts"), help="output directory")
    p.add_argument("--device", default="auto", help="cpu, cuda or auto")
    a = p.parse_args()

    from faster_whisper import WhisperModel

    src = Path(a.input)
    if not src.exists():
        print(f"not found: {src}", file=sys.stderr)
        return 1
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = out / src.stem

    compute = "int8" if a.device in ("cpu", "auto") else "float16"
    model = WhisperModel(a.model, device=a.device, compute_type=compute)
    segments, info = model.transcribe(
        str(src),
        language=a.language,
        task="translate" if a.translate else "transcribe",
        word_timestamps=True,
        vad_filter=True,  # skips silence, which cuts Whisper's invented "Thank you." lines
    )
    print(f"language: {info.language} ({info.language_probability:.0%}), duration {info.duration:.1f}s", file=sys.stderr)

    segs, words = [], []
    for s in segments:
        w = [{"text": x.word.strip(), "start": round(x.start, 3), "end": round(x.end, 3), "prob": round(x.probability, 3)}
             for x in (s.words or []) if x.word.strip()]
        segs.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": w})
        print(f"[{ts(s.start, '.')} -> {ts(s.end, '.')}] {s.text.strip()}", file=sys.stderr)
        for x in w:
            words.append({"id": f"w{len(words)}", "text": x["text"], "start": x["start"], "end": x["end"]})

    Path(f"{stem}.txt").write_text("\n".join(s["text"] for s in segs) + "\n")
    Path(f"{stem}.srt").write_text("".join(
        f"{i}\n{ts(s['start'], ',')} --> {ts(s['end'], ',')}\n{s['text']}\n\n" for i, s in enumerate(segs, 1)))
    Path(f"{stem}.vtt").write_text("WEBVTT\n\n" + "".join(
        f"{ts(s['start'], '.')} --> {ts(s['end'], '.')}\n{s['text']}\n\n" for s in segs))
    Path(f"{stem}.json").write_text(json.dumps(
        {"language": info.language, "duration": info.duration, "segments": segs}, indent=2, ensure_ascii=False))
    Path(f"{stem}.words.json").write_text(json.dumps(words, indent=2, ensure_ascii=False))
    print(f"wrote {stem}.{{txt,srt,vtt,json,words.json}}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
