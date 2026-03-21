# Video generation from static images

## What this does
This project can now create simple promo-style videos from static images using Python plus ffmpeg.

The script:
- takes one or more images or image directories
- turns them into a slideshow video
- applies subtle zoom motion
- uses crossfades between frames
- exports an MP4

## Files
- `scripts/generate_video_from_images.py` — image-to-video generator
- output folder: `output/generated-videos/`

## Requirements
- workspace virtualenv: `../.venv/bin/python`
- Python package: `moviepy` (already present in the workspace venv)
- ffmpeg access via `imageio_ffmpeg` in the Python stack

You do **not** need a separately installed system `ffmpeg` binary for the current workflow if the workspace venv is intact.

## Example
```bash
cd /Users/demo/.openclaw/workspace/eraofrobotics-copy
../.venv/bin/python scripts/generate_video_from_images.py generated-images \
  --output output/generated-videos/eraofrobotics-montage.mp4 \
  --seconds-per-image 2.8 \
  --fps 24 \
  --width 1280 \
  --height 720
```

## Recommended use cases
- social promo clips
- homepage/background concept videos
- post teasers from generated artwork
- short editorial montages

## Verified outputs created in this workspace
- `output/generated-videos/eraofrobotics-vertical-social.mp4` — 1080x1920 with audio
- `output/generated-videos/eraofrobotics-landscape-promo.mp4` — 1280x720 with audio
- `output/generated-videos/eraofrobotics-homepage-loop.mp4` — 1600x900 without audio

## Notes
- This is not Sora video generation. It is a local montage generator from static images.
- ffmpeg must exist on the machine.
- If you want captions, branded end cards, or music sync, extend this script instead of creating random one-off export workflows.
