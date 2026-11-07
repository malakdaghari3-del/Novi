# Novi video studio

This repo is a video editing workspace. See README.md for the tools and workflow.

- Run `./setup.sh` first in a fresh environment (creates `.venv`, installs Node packages, vendors GSAP).
- Python tools live in `.venv/bin/` (yt-dlp, auto-editor, scenedetect); Whisper runs via `.venv/bin/python scripts/transcribe.py`.
- Everyday edits: `scripts/ff <command>`. Downloads: `scripts/download <url>`.
- Motion graphics: `motion/` is a HyperFrames project. Load the `hyperframes` skill before touching it.
  Prefix HyperFrames commands with `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1`.
  Load GSAP from `assets/vendor/gsap.min.js`, never a CDN.
- Put inputs in `media/`, transcripts in `transcripts/`, finished videos in `exports/`. Never commit media files.
