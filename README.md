# Novi — Video Editing Studio

A command-line video studio: download footage, transcribe it, cut it, and add motion graphics.

| Tool | What it's for | Where |
| --- | --- | --- |
| **yt-dlp** | Download video/audio from YouTube and 1000+ sites | `scripts/download` |
| **Whisper** (faster-whisper) | Transcription, subtitles, word-level timings | `scripts/transcribe.py` |
| **HyperFrames** | Motion graphics, titles, captions, overlays (HTML → video) | `motion/` |
| **FFmpeg** | Cutting, joining, reframing, audio, burn-in subtitles | `scripts/ff` |
| **auto-editor** | Remove silence / dead air automatically | `scripts/ff silence` |
| **PySceneDetect** | Find shot changes | `scripts/ff scenes` |

## Setup

```bash
./setup.sh        # installs everything; safe to re-run
```

Needs Python 3.10+, Node 22+ and ffmpeg (the script installs ffmpeg with apt/brew if it's missing).

## Folder layout

```
media/
  downloads/   yt-dlp video downloads
  audio/       extracted / downloaded audio
  raw/         your own footage
  music/ sfx/ images/
transcripts/   Whisper output (.txt .srt .vtt .json .words.json)
motion/        HyperFrames project (motion graphics)
exports/       finished videos
scripts/       studio tools
```

Media, transcripts and exports are git-ignored (only the empty folders are committed).

## Typical workflow

```bash
# 1. Get footage
scripts/download "https://youtube.com/watch?v=..."          # → media/downloads/
scripts/download "https://youtube.com/watch?v=..." --audio  # audio only

# 2. Transcribe (auto-detects the language; --language ar / en / es ... to force)
.venv/bin/python scripts/transcribe.py media/downloads/clip.mp4 --model small
#   → transcripts/clip.srt, .vtt, .txt, .json, .words.json

# 3. Edit
scripts/ff trim     in.mp4 00:00:12 00:00:45 exports/cut.mp4
scripts/ff silence  exports/cut.mp4 exports/tight.mp4
scripts/ff concat   exports/final.mp4 intro.mp4 exports/tight.mp4 outro.mp4
scripts/ff vertical exports/final.mp4 exports/final-9x16.mp4      # Reels/TikTok/Shorts
scripts/ff subs     exports/final.mp4 transcripts/clip.srt exports/final-subs.mp4
scripts/ff mix      exports/final.mp4 media/music/bed.mp3 exports/final-music.mp4 0.12
scripts/ff loudnorm exports/final-music.mp4 exports/final-loud.mp4
scripts/ff          # full command list
```

Whisper models: `tiny`, `base`, `small` (default), `medium`, `large-v3`, `turbo`. Bigger models are more
accurate and slower. The `.en` variants (e.g. `small.en`) are English only. Models download on first use.

## Motion graphics (HyperFrames)

```bash
npm run motion:preview   # live preview in the browser
npm run motion:check     # lint the composition
npm run motion:render    # render to motion/renders/*.mp4
```

`motion/index.html` is the root composition (1920×1080, 30 fps). Scenes go in `motion/compositions/`,
media and fonts in `motion/assets/`. GSAP is loaded locally from `motion/assets/vendor/`, so renders
also work offline.

**Animated captions from your own transcript:**

```bash
cp transcripts/clip.words.json motion/assets/
cd motion && npx hyperframes transcribe assets/clip.words.json   # → motion/assets/transcript.json
```

**Graphics over footage:** render with a transparent background
(`npx hyperframes render --format mov`), then `scripts/ff overlay footage.mp4 motion/renders/x.mov out.mp4`.

The easiest way to build motion graphics is to ask Claude: *"make a 10-second animated title for …"*.

HyperFrames telemetry is turned off (`setup.sh` runs `hyperframes telemetry disable`).
