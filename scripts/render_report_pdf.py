#!/usr/bin/env python3
from pathlib import Path
import sys
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
slug = sys.argv[1] if len(sys.argv) > 1 else 'robotics-economics-brief'
html_path = ROOT / f'{slug}.html'
out_path = ROOT / 'assets' / 'pdf' / f'{slug}.pdf'
out_path.parent.mkdir(parents=True, exist_ok=True)
if not html_path.exists():
    raise SystemExit(f'Missing HTML report: {html_path}')
HTML(filename=str(html_path), base_url=str(ROOT)).write_pdf(str(out_path))
print(out_path)
