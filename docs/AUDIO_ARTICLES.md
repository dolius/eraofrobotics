# Audio Articles Workflow

This site can generate article + audio pairs from a single queue file.

## Files
- `data/audibles.md` — queued audio article topics
- `scripts/make_audio_article.py` — single-file generator
- output markdown articles → `audio-articles/`
- output mp3 files → `audio-articles/audio/`
- output HTML snippets → `audio-articles/snippets/`

## What the script does
1. reads one or more jobs from `data/audibles.md`
2. uses the OpenAI API to generate article text
3. writes the article as markdown
4. converts the article to MP3 using free TTS via `gTTS`
5. creates a small HTML snippet you can drop into the site

## Requirements
Install into the workspace venv:
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
../.venv/bin/python -m pip install openai gTTS
```

Set your key:
```bash
export OPENAI_API_KEY=your_key_here
```

Run one article:
```bash
../.venv/bin/python scripts/make_audio_article.py --limit 1
```

Run a specific slug:
```bash
../.venv/bin/python scripts/make_audio_article.py --slug warehouse-robotics-wedge
```

## Notes
- `gTTS` is a simple free TTS path, good for quick audio article generation.
- If you later want better voices, replace the TTS function while keeping the same queue format.
- This workflow is intentionally simple and single-file so it is easy to extend.
