#!/usr/bin/env python3
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/pdf/robotics-brief-real.pdf'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Hero', fontName='Helvetica-Bold', fontSize=22, leading=28, textColor=colors.HexColor('#0f172a'), spaceAfter=14))
styles.add(ParagraphStyle(name='Sub', fontName='Helvetica', fontSize=11, leading=16, textColor=colors.HexColor('#475569'), spaceAfter=10))
styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#0f172a'), spaceAfter=8))
styles.add(ParagraphStyle(name='Body2', fontName='Helvetica', fontSize=11, leading=16, textColor=colors.HexColor('#334155'), spaceAfter=6))

story = []
story.append(Paragraph('Era of Robotics — Free Brief', styles['Heading5']))
story.append(Spacer(1, 0.15 * inch))
story.append(Paragraph('The robotics era is here. Cute if you thought it would ask permission.', styles['Hero']))
story.append(Paragraph('This brief is the fast, useful version of what people actually need to know about robotics right now: what is changing, where the money is forming, what is hype, and what builders, operators, and investors should actually pay attention to.', styles['Sub']))
story.append(Paragraph('Robotics stopped being just a cool demo category. It is becoming an economic one.', styles['Body2']))
story.append(Spacer(1, 0.2 * inch))

sections = [
    ('1. Why robotics matters now', [
        'AI is making machines less rigid and more commercially useful.',
        'Labor pressure is making automation economically attractive in more industries.',
        'Hardware, sensors, and software tooling are finally stacking in the same direction.',
        'The conversation is shifting from novelty to operational payoff.'
    ]),
    ('2. The sectors moving fastest', [
        'Warehousing and fulfillment remain one of the clearest commercial wedges.',
        'Industrial automation upgrades continue where throughput and reliability matter most.',
        'Healthcare and service robotics are opening where staffing and repetitive support work collide.',
        'AI-enabled machine tooling may quietly become one of the most valuable layers.'
    ]),
    ('3. Where hype outruns reality', [
        'Humanoids get attention faster than they get repeatable deployment density.',
        'Demo quality is not deployment quality.',
        'A painfully useful wedge use case is usually better than a grand theory of everything.',
        'If the economics need interpretive dance to explain, the category probably is not ready yet.'
    ]),
    ('4. What to watch next', [
        'Deployment density in real workflows',
        'Clearer ROI narratives tied to labor and throughput',
        'Tooling that makes robotics easier to build, simulate, and integrate',
        'Education and operator resources that help people stop guessing'
    ]),
]

for title, bullets in sections:
    story.append(Paragraph(title, styles['SectionTitle']))
    story.append(ListFlowable([ListItem(Paragraph(x, styles['Body2'])) for x in bullets], bulletType='bullet', leftIndent=16))
    story.append(Spacer(1, 0.18 * inch))

story.append(Paragraph('Era of Robotics is built for people who want signal instead of theater.', styles['Sub']))

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
doc.build(story)
print(OUT)
