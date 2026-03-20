#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import List, Tuple

from moviepy import AudioFileClip, ImageClip, afx, concatenate_videoclips

VALID_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}
PRESETS = {
    'landscape': (1280, 720),
    'vertical': (1080, 1920),
    'square': (1080, 1080),
    'hero': (1600, 900),
}


def collect_images(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(x for x in p.iterdir() if x.suffix.lower() in VALID_EXTS))
        elif p.is_file() and p.suffix.lower() in VALID_EXTS:
            files.append(p)
    return files


def resolve_size(preset: str | None, width: int | None, height: int | None) -> Tuple[int, int]:
    if preset:
        return PRESETS[preset]
    if width and height:
        return width, height
    return PRESETS['landscape']


def fit_clip(img: Path, seconds: float, width: int, height: int, zoom: float) -> ImageClip:
    clip = ImageClip(str(img)).with_duration(seconds)
    base_scale = max(width / clip.w, height / clip.h)
    scale = base_scale * max(zoom, 1.0)
    clip = clip.resized(scale)
    clip = clip.cropped(
        x_center=clip.w / 2,
        y_center=clip.h / 2,
        width=width,
        height=height,
    )
    return clip


def build_audio(audio_path: str | None, target_duration: float, fade_in: float, fade_out: float, volume: float):
    if not audio_path:
        return None
    audio = AudioFileClip(audio_path)
    if audio.duration > target_duration:
        audio = audio.subclipped(0, target_duration)
    else:
        audio = audio.with_duration(target_duration)
    effects = []
    if fade_in > 0:
        effects.append(afx.AudioFadeIn(fade_in))
    if fade_out > 0:
        effects.append(afx.AudioFadeOut(fade_out))
    if effects:
        audio = audio.with_effects(effects)
    if volume != 1.0:
        audio = audio.with_volume_scaled(volume)
    return audio


def main():
    parser = argparse.ArgumentParser(description='Generate a simple video from static images.')
    parser.add_argument('inputs', nargs='+', help='Image files and/or directories')
    parser.add_argument('--output', default='output/generated-videos/robotics-montage.mp4', help='Output video file')
    parser.add_argument('--seconds-per-image', type=float, default=3.0, help='Duration for each image')
    parser.add_argument('--fps', type=int, default=24, help='Frames per second')
    parser.add_argument('--preset', choices=sorted(PRESETS.keys()), default='landscape', help='Output size preset')
    parser.add_argument('--width', type=int, default=None, help='Output width override')
    parser.add_argument('--height', type=int, default=None, help='Output height override')
    parser.add_argument('--zoom', type=float, default=1.03, help='Slight overscale for tighter framing')
    parser.add_argument('--audio', default=None, help='Optional audio file to mix in')
    parser.add_argument('--audio-fade-in', type=float, default=1.5, help='Audio fade-in seconds')
    parser.add_argument('--audio-fade-out', type=float, default=2.5, help='Audio fade-out seconds')
    parser.add_argument('--audio-volume', type=float, default=0.7, help='Audio volume multiplier')
    args = parser.parse_args()

    images = collect_images(args.inputs)
    if not images:
        raise SystemExit('No valid images found.')

    width, height = resolve_size(args.preset, args.width, args.height)
    clips = [fit_clip(img, args.seconds_per_image, width, height, args.zoom) for img in images]
    video = concatenate_videoclips(clips, method='compose')

    audio = build_audio(args.audio, video.duration, args.audio_fade_in, args.audio_fade_out, args.audio_volume)
    if audio is not None:
        video = video.with_audio(audio)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    video.write_videofile(str(output), fps=args.fps, codec='libx264', audio_codec='aac' if audio else None)
    print(f'Saved video: {output}')


if __name__ == '__main__':
    main()
