#!/usr/bin/env python3
"""Generate a comprehensive SOP-style PDF for the Humanoid Reality Brief."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/pdf/humanoid-reality-brief.pdf"
IMG_DIR = ROOT / "assets/images"

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="DocTitle",
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="DocSub",
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=6,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallCap",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#475569"),
        spaceAfter=4,
    )
)


def add_image(story, filename, width=6.0 * inch):
    path = IMG_DIR / filename
    if not path.exists():
        return
    img = Image(str(path))
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = width
    img.drawHeight = width * ratio
    story.append(img)
    story.append(Spacer(1, 0.12 * inch))


def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["Body"])) for item in items],
        bulletType="bullet",
        leftIndent=16,
        bulletFontName="Helvetica",
        bulletFontSize=9,
    )


def numbered_list(items):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["Body"])) for item in items],
        bulletType="1",
        start="1",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=9,
    )


def build_story():
    story = []

    story.append(Paragraph("ERA OF ROBOTICS", styles["SmallCap"]))
    story.append(Paragraph("Humanoid Reality Brief: Standard Operating Procedure", styles["DocTitle"]))
    story.append(
        Paragraph(
            "Comprehensive deployment report and operating procedure for teams evaluating humanoid robots in real facilities.",
            styles["DocSub"],
        )
    )
    story.append(
        Paragraph(
            "Purpose: convert humanoid evaluation from demo-driven excitement to measurable operational decision-making.",
            styles["Body"],
        )
    )
    story.append(Spacer(1, 0.16 * inch))

    add_image(story, "home-robotics-future.png")

    story.append(Paragraph("1. Executive Summary", styles["Section"]))
    story.append(
        Paragraph(
            "Humanoids can be useful in narrow, structured workflows where human-shaped mobility is valuable and fixed automation is difficult. They are not yet a universal labor replacement category.",
            styles["Body"],
        )
    )
    story.append(
        bullet_list(
            [
                "Strong fit: repetitive assistive logistics tasks in human-designed environments.",
                "Weak fit: broad unsupervised autonomy across varied, high-complexity workflows.",
                "Core decision rule: scale only after KPI consistency and stable economics are proven.",
            ]
        )
    )
    story.append(Spacer(1, 0.14 * inch))

    story.append(Paragraph("2. Scope and Preconditions", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Pilot horizon: 90 days with explicit go/no-go gate at the end.",
                "Facility scope: warehouse, light industrial, or structured service floor.",
                "Required controls: incident logging, fallback runbook, safety owner, vendor SLA.",
                "Data baseline required before launch: throughput/hour, error rate, labor-hours/shift, downtime events.",
            ]
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("3. Standard Operating Procedure", styles["Section"]))
    story.append(Paragraph("Phase A: Baseline and Design (Week 0-2)", styles["Body"]))
    story.append(
        numbered_list(
            [
                "Define one target workflow and one bottleneck to improve.",
                "Capture baseline metrics and document current exception handling.",
                "Set pass/fail thresholds: uptime, throughput lift, MTTR, intervention hours.",
                "Approve safety controls and escalation matrix before first live run.",
            ]
        )
    )
    story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("Phase B: Controlled Pilot (Week 3-8)", styles["Body"]))
    story.append(
        numbered_list(
            [
                "Deploy in one zone with constrained task boundaries.",
                "Run with dual-shift supervision for first two weeks.",
                "Log every stop cause and classify by root category.",
                "Conduct weekly corrective-action review with operations and vendor teams.",
            ]
        )
    )
    story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("Phase C: Stabilization and Scale Decision (Week 9-12)", styles["Body"]))
    story.append(
        numbered_list(
            [
                "Remove underperforming tasks from pilot scope.",
                "Verify KPI consistency over four consecutive weeks.",
                "Rebuild economics model using observed maintenance and intervention data.",
                "Issue go/no-go decision for phased expansion.",
            ]
        )
    )

    story.append(Spacer(1, 0.14 * inch))
    add_image(story, "human-robot-collaboration.png", width=5.6 * inch)

    story.append(Paragraph("4. KPI Scorecard", styles["Section"]))

    kpi_data = [
        ["Metric", "Target", "Decision Use"],
        ["Operational uptime", ">= 92% by Week 8", "Minimum reliability threshold"],
        ["Mean time to recovery", "< 15 minutes", "Serviceability and support quality"],
        ["Throughput improvement", ">= 12% vs baseline", "Operational performance gate"],
        ["Economic payback", "<= 18 months", "Scale viability gate"],
    ]
    table = Table(kpi_data, colWidths=[2.0 * inch, 1.6 * inch, 2.6 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#1f2937")),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8.8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.16 * inch))

    story.append(Paragraph("5. Risk Controls and Mitigation", styles["Section"]))
    story.append(
        bullet_list(
            [
                "Technical risk: constrain initial task library and enforce exception handoff rules.",
                "Safety risk: maintain geofencing, hard-stop governance, and weekly safety drill cadence.",
                "Economic risk: update cost model using real pilot data, not vendor brochure assumptions.",
                "Organizational risk: assign clear ownership across operations, safety, and maintenance.",
            ]
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("6. Operating Checklist", styles["Section"]))
    story.append(Paragraph("Pre-Launch Checklist", styles["Body"]))
    story.append(
        bullet_list(
            [
                "Workflow scope approved and baseline metrics captured.",
                "Safety owner assigned and escalation matrix signed.",
                "Vendor SLA validated (response time, parts, and onsite support).",
                "Fallback runbook tested with live simulation exercise.",
            ]
        )
    )
    story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("Post-Pilot Scale Checklist", styles["Body"]))
    story.append(
        bullet_list(
            [
                "KPI thresholds met for four continuous weeks.",
                "Downtime and intervention hours within approved limits.",
                "Pilot economics validated against original business case.",
                "Phased zone-by-zone rollout plan approved.",
            ]
        )
    )

    add_image(story, "robotics-market-map.png", width=5.8 * inch)

    story.append(Spacer(1, 0.12 * inch))
    story.append(
        Paragraph(
            "Generated by Era of Robotics SOP pipeline. Pair this brief with automation-readiness-score and robot-vs-human-cost tools before deployment approval.",
            styles["DocSub"],
        )
    )

    return story


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54,
        title="Humanoid Reality Brief SOP",
        author="Era of Robotics",
        subject="Humanoid deployment SOP and implementation guide",
    )
    doc.build(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
