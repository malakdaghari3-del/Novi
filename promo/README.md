# Novi AI — 30s promo video

**`novi-ai-promo-30s.mp4`**: 1920×1080, 30 fps, H.264 + AAC 320k, about 30 s, mixed to -14.7 LUFS (streaming standard).

## Storyboard (cuts on a 120 BPM beat grid)
| Time | Scene | Voiceover |
|---|---|---|
| 0–2.7s | "What's really in your food?" with a glowing light trail | "Ever wondered what's really in your food?" |
| 2.7–4.2s | Logo burst: Novi AI | "Meet Novi AI." |
| 4.2–7.2s | Phone: Home → tap Scan → label scanned (beam + highlights) | "Just scan any label," |
| 7.2–12.2s | Result screen; ingredient verdict cards fly out (Caution, Sugar ✓, Palm oil ✕, Hazelnuts ✕, Skimmed milk ✕) | "and AI checks every ingredient against your allergies and diet." |
| 12.2–15.2s | Zucchero → Sucre → … → **Sugar** (AI translation) | "In any language." |
| 15.2–19.2s | Preference nodes light up (Dairy-free, Vegan, Gluten-free…) | "Set your preferences once." |
| 19.2–23.7s | Ask-AI chat + better alternatives | "Ask anything, and discover better alternatives." |
| 23.7–26.7s | "Scan smarter. Shop safer." | same |
| 26.7–30s | Logo end card + "Try it free" CTA | "Novi AI. Try it free." |

## How it was made
- **Visuals:** `source/index.html` is a frame-accurate HTML/canvas motion scene with `render(t)`, rendered frame by frame by `source/render.js` (Playwright + ffmpeg).
- **Voiceover:** Kokoro neural TTS (voice `af_heart`), via `source/vo.py`.
- **Music and SFX:** an original track and sound effects synthesized in `source/audio.py`, so the audio is royalty-free and has no third-party samples.

Re-render: `node source/render.js full`, then `python3 source/audio.py`, then mux both with ffmpeg.
