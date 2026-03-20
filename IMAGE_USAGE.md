# Image generation usage

## Requirements
- Python package: `openai`
- Environment variable: `OPENAI_API_KEY`
- Recommended interpreter in this workspace: `../.venv/bin/python`

## Recommended usage
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics
OPENAI_API_KEY=your_key_here ../.venv/bin/python generate_images.py "A cinematic editorial robotics lab scene" --outdir generated-images --name robotics-lab-hero
```

## Why use the workspace venv
The system Python on this machine may be externally managed and reject direct package installs. The workspace virtualenv already supports the `openai` dependency, so it is the safer default for WebLord image generation.

## Output
Images will be saved into the chosen output directory, e.g.:
- `generated-images/robotics-lab-hero.png`

## Notes
- Default model in the script: `gpt-image-1`
- Update prompts in `image-prompts.txt`
- Good target uses: homepage hero images, tools page visuals, downloadable covers
- Prefer grounded editorial prompts over generic shiny-future sludge
