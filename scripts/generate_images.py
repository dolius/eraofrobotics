#!/usr/bin/env python3
import argparse
import base64
import os
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("Missing dependency: pip install openai")


def slugify(text: str) -> str:
    keep = []
    for ch in text.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in (' ', '-', '_'):
            keep.append('-')
    slug = ''.join(keep)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-') or 'image'


def main():
    parser = argparse.ArgumentParser(description="Generate images with OpenAI and save them locally.")
    parser.add_argument("prompt", help="Image prompt")
    parser.add_argument("--outdir", default="generated-images", help="Output directory")
    parser.add_argument("--size", default="1024x1024", help="Image size, e.g. 1024x1024")
    parser.add_argument("--quality", default="high", help="Image quality")
    parser.add_argument("--background", default="auto", help="Background setting")
    parser.add_argument("--format", default="png", help="Output format")
    parser.add_argument("--name", default=None, help="Optional base filename")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=args.prompt,
        size=args.size,
        quality=args.quality,
        background=args.background,
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    stem = args.name or slugify(args.prompt[:80])
    outfile = outdir / f"{stem}.{args.format}"
    outfile.write_bytes(image_bytes)

    print(f"Saved: {outfile}")


if __name__ == "__main__":
    main()
