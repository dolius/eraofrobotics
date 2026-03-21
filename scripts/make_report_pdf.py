#!/usr/bin/env python3
from pathlib import Path
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / 'assets' / 'pdf'
PDF_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Hero', fontName='Helvetica-Bold', fontSize=22, leading=28, textColor=colors.HexColor('#0f172a'), spaceAfter=14))
styles.add(ParagraphStyle(name='Sub', fontName='Helvetica', fontSize=11, leading=16, textColor=colors.HexColor('#475569'), spaceAfter=10))
styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#0f172a'), spaceAfter=8))
styles.add(ParagraphStyle(name='Body2', fontName='Helvetica', fontSize=11, leading=16, textColor=colors.HexColor('#334155'), spaceAfter=6))

REPORTS = {
    'robotics-economics-brief': {
        'title': 'Robotics Economics Brief',
        'subtitle': 'A focused report on readiness, labor pressure, cost comparison, and ROI.',
        'intro': 'This report is about the practical questions that decide whether robotics looks useful or delusional: is the workflow ready, how does labor compare with machine cost, and when does the payback story become believable enough to survive real scrutiny?',
        'sections': [
            ('The core questions', [
                'Is the workflow repetitive and stable enough to automate?',
                'Is labor pain high enough to justify changing the process?',
                'Will maintenance drag erase the expected upside?',
                'How fast can the deployment pay back under realistic conditions?'
            ]),
            ('What operators should avoid', [
                'Buying around hype instead of a real operational need.',
                'Skipping workflow analysis and assuming the robot is the strategy.',
                'Ignoring maintenance, downtime, and integration costs.',
                'Confusing a polished demo with a durable deployment.'
            ]),
            ('What to look for instead', [
                'Clear repetitive workflows with obvious throughput or labor pressure.',
                'A credible implementation path, not just an exciting deck.',
                'A payback story that still works after maintenance and friction are included.',
                'A narrow, useful deployment before broader automation fantasies.'
            ])
        ]
    },
    'warehouse-robotics-brief': {
        'title': 'Warehouse Robotics Brief',
        'subtitle': 'A focused report on one of the clearest commercial wedges in robotics.',
        'intro': 'Warehouse robotics matters because the pain is obvious, the workflows are repetitive, and the economics are easier to explain than in more theatrical corners of the category.',
        'sections': [
            ('Why this category gets paid first', [
                'Repetition is high and throughput matters every day.',
                'Labor pressure is persistent and easier to quantify.',
                'Operational wins can often be measured clearly.',
                'The wedge is narrow enough to deploy before trying to automate everything.'
            ]),
            ('What to watch', [
                'Deployment density, not demo density.',
                'Integration and maintenance overhead.',
                'Payback period under operational stress.',
                'Whether the workflow is stable enough for automation.'
            ])
        ]
    },
    'humanoid-reality-brief': {
        'title': 'Humanoid Reality Brief',
        'subtitle': 'A focused report on one of the most over-watched corners of robotics.',
        'intro': 'Humanoids attract attention faster than almost any other robotics category. The harder question is where they fit in the real market, how deployment reality differs from public spectacle, and why narrower systems may still get paid first.',
        'sections': [
            ('What makes humanoids compelling', [
                'They match human-shaped environments.',
                'They compress many robotics fantasies into one machine.',
                'They attract unusual public and investor attention.'
            ]),
            ('What makes them hard', [
                'Reliability requirements are brutal.',
                'General-purpose utility is expensive to prove.',
                'Narrower systems may win earlier on economics.',
                'Deployment reality is harsher than demo culture.'
            ])
        ]
    }
}

slug = sys.argv[1] if len(sys.argv) > 1 else 'robotics-economics-brief'
report = REPORTS.get(slug)
if not report:
    raise SystemExit(f'Unknown report slug: {slug}')

out = PDF_DIR / f'{slug}.pdf'
story = []
story.append(Paragraph('Era of Robotics — Report', styles['Heading5']))
story.append(Spacer(1, 0.15 * inch))
story.append(Paragraph(report['title'], styles['Hero']))
story.append(Paragraph(report['subtitle'], styles['Sub']))
story.append(Paragraph(report['intro'], styles['Body2']))
story.append(Spacer(1, 0.2 * inch))

for title, bullets in report['sections']:
    story.append(Paragraph(title, styles['SectionTitle']))
    story.append(ListFlowable([ListItem(Paragraph(x, styles['Body2'])) for x in bullets], bulletType='bullet', leftIndent=16))
    story.append(Spacer(1, 0.18 * inch))

story.append(Paragraph('Era of Robotics is built for readers who want signal instead of theater.', styles['Sub']))

doc = SimpleDocTemplate(str(out), pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
doc.build(story)
print(out)
