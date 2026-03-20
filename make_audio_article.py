#!/usr/bin/env python3
"""
Single-file audio article agent for Era of Robotics.

What it does:
- reads audibles.md for article jobs
- generates article text with the OpenAI API
- writes markdown article files
- converts article text to MP3 using a free TTS service (gTTS)
- writes a small HTML embed snippet for site use

Requirements:
- OPENAI_API_KEY in environment
- pip install openai gTTS
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from openai import OpenAI
from gtts import gTTS

ROOT = Path(__file__).resolve().parent
AUDIBLES_MD = ROOT / "audibles.md"
OUTPUT_MD_DIR = ROOT / "audio-articles"
OUTPUT_MP3_DIR = ROOT / "audio-articles" / "audio"
OUTPUT_SNIPPET_DIR = ROOT / "audio-articles" / "snippets"


@dataclass
class AudibleJob:
    slug: str
    title: str
    angle: str
    audience: str
    length: str
    voice_language: str = "en"
    status: str = "todo"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "audio-article"


def parse_jobs(md_text: str) -> List[AudibleJob]:
    jobs: List[AudibleJob] = []
    blocks = [b.strip() for b in md_text.split("\n---\n") if b.strip()]
    for block in blocks:
        fields = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            fields[k.strip().lower()] = v.strip()
        if not fields:
            continue
        title = fields.get("title")
        angle = fields.get("angle", "Explain the topic clearly, practically, and with a strong point of view.")
        audience = fields.get("audience", "curious readers, builders, and operators")
        length = fields.get("length", "900-1200 words")
        slug = fields.get("slug") or slugify(title or angle)
        status = fields.get("status", "todo")
        voice_language = fields.get("voice_language", "en")
        if title:
            jobs.append(AudibleJob(slug=slug, title=title, angle=angle, audience=audience, length=length, status=status, voice_language=voice_language))
    return jobs


def generate_article(client: OpenAI, job: AudibleJob) -> str:
    prompt = f"""
You are writing for Era of Robotics, a practical, sharp editorial website about robotics.

Write a strong article with:
- title: {job.title}
- audience: {job.audience}
- target length: {job.length}
- angle: {job.angle}

Voice requirements:
- practical, clear, intelligent, slightly sharp
- no corporate filler
- no fake futurist hype
- grounded in robotics adoption, economics, use cases, and real-world implications
- readable aloud as an audio article

Output format:
- markdown
- start with an H1 title
- use short sections with H2 headings
- no tables
- finish with a short conclusion
""".strip()

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text.strip()


def markdown_to_plaintext(md: str) -> str:
    text = md
    text = re.sub(r"^#\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def synthesize_audio(job: AudibleJob, plaintext: str, out_mp3: Path) -> None:
    tts = gTTS(text=plaintext, lang=job.voice_language)
    tts.save(str(out_mp3))


def write_html_snippet(job: AudibleJob, md_path: Path, mp3_path: Path, out_snippet: Path) -> None:
    html = f"""<article class=\"audio-article-card\">
  <div class=\"tag\">Audio article</div>
  <h2>{job.title}</h2>
  <p><a href=\"{md_path.name}\">Read article →</a></p>
  <audio controls preload=\"none\">
    <source src=\"audio/{mp3_path.name}\" type=\"audio/mpeg\" />
    Your browser does not support the audio element.
  </audio>
</article>
"""
    out_snippet.write_text(html, encoding="utf-8")


def ensure_dirs() -> None:
    OUTPUT_MD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_MP3_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_SNIPPET_DIR.mkdir(parents=True, exist_ok=True)


def load_jobs() -> List[AudibleJob]:
    if not AUDIBLES_MD.exists():
        raise SystemExit(f"Missing {AUDIBLES_MD}")
    return parse_jobs(AUDIBLES_MD.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate audio articles from audibles.md")
    parser.add_argument("--slug", help="Run only one slug from audibles.md")
    parser.add_argument("--limit", type=int, default=1, help="How many todo jobs to process")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")

    ensure_dirs()
    jobs = load_jobs()
    if args.slug:
        jobs = [j for j in jobs if j.slug == args.slug]
    else:
        jobs = [j for j in jobs if j.status.lower() == "todo"][: args.limit]

    if not jobs:
        raise SystemExit("No matching jobs found")

    client = OpenAI(api_key=api_key)

    for job in jobs:
        article_md = generate_article(client, job)
        plain = markdown_to_plaintext(article_md)

        md_path = OUTPUT_MD_DIR / f"{job.slug}.md"
        mp3_path = OUTPUT_MP3_DIR / f"{job.slug}.mp3"
        snippet_path = OUTPUT_SNIPPET_DIR / f"{job.slug}.html"

        md_path.write_text(article_md, encoding="utf-8")
        synthesize_audio(job, plain, mp3_path)
        write_html_snippet(job, md_path, mp3_path, snippet_path)

        print(f"Generated article: {md_path}")
        print(f"Generated audio:   {mp3_path}")
        print(f"Generated snippet: {snippet_path}")


if __name__ == "__main__":
    main()
