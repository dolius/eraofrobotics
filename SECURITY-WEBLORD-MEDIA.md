# WebLord Media Security Notes

This file documents the safe operating posture for the local image/video/caption tooling in `eraofrobotics`.

## Current safety posture
The current workflow is intentionally conservative:
- installs go into the workspace virtualenv only: `/Users/demo/.openclaw/workspace/.venv`
- no system Python package installs
- no `--break-system-packages`
- no random GitHub pip installs
- no elevated shell hacks just to force a dependency through
- API keys should be passed transiently via environment variables, not stored in project files

## Approved dependency posture
Keep the dependency set small and boring.

Currently pinned in `requirements-weblord-media.txt`:
- `openai`
- `pysubs2`
- `srt`
- `imageio-ffmpeg`
- `numpy`

Additionally validated in the current workspace venv:
- `moviepy`
- `Pillow`

These support:
- image generation scripts
- local image-to-video montage generation
- subtitle/caption file handling

## Installation policy
Use only the workspace venv:
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
../.venv/bin/python -m pip install -r requirements-weblord-media.txt
```

Do not:
- install into system Python
- use `sudo pip`
- use `pip --break-system-packages`
- install broad toolchains unless a real need exists

## Transcription caution
`openai-whisper` was NOT adopted in the current environment because it failed under this Python 3.14 stack. That was the correct security and maintenance choice.

If transcription is needed later, prefer one of:
1. isolated dedicated env for transcription
2. API-based transcription
3. a separately validated compatible local stack

## Audio caution
Audio files may come from Desktop/user folders. Treat them as local content inputs, not trusted code.
Only read them as media assets.

## Key handling
- never write API keys into HTML, JS, markdown docs, or repo config
- prefer one-shot env vars for local runs
- rotate keys that were pasted into chat or logs

## Decision rule
If a package is obscure, poorly maintained, or requires ugly system-level forcing, do not install it casually.
Stability and low blast radius beat feature greed.
