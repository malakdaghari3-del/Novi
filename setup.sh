#!/usr/bin/env bash
# Novi studio setup: safe to run again at any time.
set -euo pipefail
cd "$(dirname "$0")"

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }

# 1. System tools (ffmpeg is the core of everything)
if ! command -v ffmpeg >/dev/null 2>&1; then
  say "Installing ffmpeg"
  if command -v apt-get >/dev/null 2>&1; then
    sudo_cmd=""; [ "$(id -u)" -ne 0 ] && sudo_cmd="sudo"
    $sudo_cmd apt-get update -y && $sudo_cmd apt-get install -y ffmpeg
  elif command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  else
    echo "Please install ffmpeg manually: https://ffmpeg.org/download.html" >&2; exit 1
  fi
fi

# 2. Python tools: yt-dlp, Whisper (faster-whisper), auto-editor, scenedetect
say "Python environment (.venv)"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -U pip
.venv/bin/pip install -q -r requirements.txt

# 3. Node tools: HyperFrames + GSAP (vendored so renders work offline)
say "Node packages (HyperFrames)"
npm install --no-audit --no-fund --loglevel=error
mkdir -p motion/assets/vendor
cp node_modules/gsap/dist/gsap.min.js motion/assets/vendor/gsap.min.js
HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx hyperframes telemetry disable >/dev/null 2>&1 || true

chmod +x scripts/* 2>/dev/null || true

say "Versions"
ffmpeg -version | head -1
.venv/bin/yt-dlp --version | sed 's/^/yt-dlp /'
.venv/bin/python -c "import faster_whisper; print('faster-whisper', faster_whisper.__version__)"
.venv/bin/auto-editor --version 2>/dev/null | sed 's/^/auto-editor /' || true
npx hyperframes --version | sed 's/^/hyperframes /'
echo; echo "Studio ready. See README.md."
