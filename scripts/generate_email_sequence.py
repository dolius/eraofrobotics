#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'email-sequence-pages'
OUT.mkdir(parents=True, exist_ok=True)

emails = [
    (
        '01-brief-delivery.html',
        'Your robotics brief is ready',
        'Here is your free robotics brief, plus the two smartest next steps: read the explainer if you want the thesis, or go straight to the tools if you want to test the economics.',
    ),
    (
        '02-reality-filter.html',
        'The mistake people make when they evaluate robotics',
        'The most common robotics error is skipping the boring questions. Before you care about the machine, care about the workflow: repetition, labor pressure, stability, maintenance, and payback.',
    ),
    (
        '03-category-signal.html',
        'Where robotics is becoming commercially real first',
        'The best early categories are usually the least mystical ones: warehousing, logistics, industrial support, and painful repetitive work where the economics can actually explain themselves.',
    ),
    (
        '04-premium-offer.html',
        'Want the deeper robotics market brief?',
        'If you need more than broad signal, the premium robotics market brief is the next layer: categories, deployment realism, and where commercial gravity looks stronger than public hype.',
    ),
]

base = """<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/><title>{title}</title><link rel=\"stylesheet\" href=\"../global.css\" /></head>
<body><div class=\"wrap-narrow\"><section class=\"hero card\"><div class=\"eyebrow\">Email sequence</div><h1>{title}</h1><p>{body}</p><div class=\"button-row\"><a class=\"btn\" href=\"../robotics-brief-download.html\">Free brief</a><a class=\"btn ghost\" href=\"../tools.html\">Tools</a><a class=\"btn ghost\" href=\"../premium-robotics-brief.html\">Premium offer</a></div></section></div></body></html>"""

for filename, title, body in emails:
    (OUT / filename).write_text(base.format(title=title, body=body), encoding='utf-8')
    print(OUT / filename)
