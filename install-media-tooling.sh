#!/usr/bin/env bash
set -euo pipefail
cd /Users/demo/.openclaw/workspace/eraofrobotics

# Install only the additive/pinned tooling that is safe to reproduce in this venv.
../.venv/bin/python -m pip install -r requirements-weblord-media.txt

# Validate the full working stack already present in this workspace venv.
../.venv/bin/python - <<'PY'
mods = ['openai', 'moviepy', 'PIL', 'pysubs2', 'srt', 'imageio_ffmpeg', 'numpy']
for name in mods:
    __import__(name)
print('Validated WebLord media stack in workspace venv.')
PY

printf '\nWebLord media tooling is ready in the workspace venv.\n'
