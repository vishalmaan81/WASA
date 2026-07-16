#!/usr/bin/env python3
"""Generate WASA Product Analysis & Vision PDF with embedded UI mockups."""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem, HRFlowable, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "pdf-assets"
OUT = ROOT / "WASA_Product_Vision_UIUX_Roadmap.pdf"

# Brand palette
NAVY = HexColor("#0B1220")
NAVY2 = HexColor("#111B2E")
CYAN = HexColor("#22D3EE")
INDIGO = HexColor("#6366F1")
SLATE = HexColor("#334155")
MUTED = HexColor("#64748B")
TEXT = HexColor("#0F172A")
LIGHT = HexColor("#F8FAFC")
SOFT = HexColor("#E2E8F0")
CRITICAL = HexColor("#E11D48")
HIGH = HexColor("#D97706")
MED = HexColor("#2563EB")
OK = HexColor("#059669")
PURPLE = HexColor("#7C3AED")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


class ColoredBox(Flowable):
    """Rounded card with title and body lines."""

    def __init__(self, title, lines, width, bg=LIGHT, accent=CYAN, height=None):
        super().__init__()
        self.title = title
        self.lines = lines
        self.box_width = width
        self.bg = bg
        self.accent = accent
        self._height = height

    def wrap(self, availWidth, availHeight):
        h = self._height or (28 + 14 * len(self.lines) + 16)
        self.height = h
        self.width = self.box_width
        return self.box_width, h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.setStrokeColor(self.accent)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, self.box_width, self.height, 8, fill=1, stroke=1)
        c.setFillColor(self.accent)
        c.rect(0, self.height - 6, self.box_width, 6, fill=1, stroke=0)
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10, self.height - 22, self.title)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(SLATE)
        y = self.height - 38
        for line in self.lines:
            c.drawString(10, y, line[:95])
            y -= 13


class SectionBar(Flowable):
    def __init__(self, text, width):
        super().__init__()
        self.text = text
        self.box_width = width

    def wrap(self, aw, ah):
        self.width = self.box_width
        self.height = 22
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 0, self.box_width, 22, 4, fill=1, stroke=0)
        c.setFillColor(CYAN)
        c.rect(0, 0, 5, 22, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(14, 7, self.text)


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(
        name="CoverTitle", fontName="Helvetica-Bold", fontSize=28,
        leading=34, textColor=white, alignment=TA_LEFT, spaceAfter=8
    ))
    s.add(ParagraphStyle(
        name="CoverSub", fontName="Helvetica", fontSize=13,
        leading=18, textColor=HexColor("#A5F3FC"), alignment=TA_LEFT, spaceAfter=6
    ))
    s.add(ParagraphStyle(
        name="H1", fontName="Helvetica-Bold", fontSize=18,
        leading=22, textColor=NAVY, spaceBefore=4, spaceAfter=10
    ))
    s.add(ParagraphStyle(
        name="H2", fontName="Helvetica-Bold", fontSize=13,
        leading=17, textColor=NAVY2, spaceBefore=10, spaceAfter=6
    ))
    s.add(ParagraphStyle(
        name="H3", fontName="Helvetica-Bold", fontSize=11,
        leading=14, textColor=INDIGO, spaceBefore=8, spaceAfter=4
    ))
    s.add(ParagraphStyle(
        name="Body", fontName="Helvetica", fontSize=9.5,
        leading=13.5, textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=6
    ))
    s.add(ParagraphStyle(
        name="BodyBullet", fontName="Helvetica", fontSize=9.2,
        leading=12.8, textColor=TEXT, leftIndent=8, spaceAfter=2
    ))
    s.add(ParagraphStyle(
        name="Caption", fontName="Helvetica-Oblique", fontSize=8,
        leading=10, textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10
    ))
    s.add(ParagraphStyle(
        name="Footer", fontName="Helvetica", fontSize=8,
        textColor=MUTED, alignment=TA_CENTER
    ))
    s.add(ParagraphStyle(
        name="Callout", fontName="Helvetica", fontSize=9,
        leading=12.5, textColor=NAVY, leftIndent=6, rightIndent=6
    ))
    s.add(ParagraphStyle(
        name="Small", fontName="Helvetica", fontSize=8.5,
        leading=11.5, textColor=SLATE, spaceAfter=3
    ))
    s.add(ParagraphStyle(
        name="TableCell", fontName="Helvetica", fontSize=8,
        leading=10.5, textColor=TEXT
    ))
    s.add(ParagraphStyle(
        name="TableHead", fontName="Helvetica-Bold", fontSize=8,
        leading=10.5, textColor=white
    ))
    return s


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, PAGE_H - 12 * mm, PAGE_W, 1.2, fill=1, stroke=0)
        canvas.setFillColor(white)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(MARGIN, PAGE_H - 8 * mm, "WASA · Product Vision & UI/UX Roadmap")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 8 * mm, "Confidential · Design + Engineering")
        canvas.setStrokeColor(SOFT)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 12 * mm, PAGE_W - MARGIN, 12 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(MARGIN, 7 * mm, "Web Application Security Automation")
        canvas.drawRightString(PAGE_W - MARGIN, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    """Drawn only on first page via onFirstPage."""
    canvas.saveState()
    # Full navy background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Accent gradient-ish bars
    canvas.setFillColor(HexColor("#0F1A2E"))
    canvas.rect(0, 0, PAGE_W * 0.38, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, PAGE_H * 0.22, 6, PAGE_H * 0.45, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    canvas.rect(0, PAGE_H * 0.22, 6, PAGE_H * 0.12, fill=1, stroke=0)

    # Hero image if available
    hero = ASSETS / "hero.jpg"
    if hero.exists():
        try:
            canvas.drawImage(
                str(hero), PAGE_W * 0.42, PAGE_H * 0.42,
                width=PAGE_W * 0.52, height=PAGE_H * 0.42,
                preserveAspectRatio=True, mask="auto"
            )
        except Exception:
            pass

    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(MARGIN, PAGE_H - 28 * mm, "PRODUCT ANALYSIS  ·  UI/UX VISION  ·  AI SECURITY ROADMAP")

    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawString(MARGIN, PAGE_H - 48 * mm, "WASA")
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(MARGIN, PAGE_H - 58 * mm, "Web Application Security Automation")

    canvas.setFillColor(HexColor("#A5F3FC"))
    canvas.setFont("Helvetica", 11)
    y = PAGE_H - 72 * mm
    for line in [
        "Thesis prototype → Enterprise-ready AI security platform",
        "Current-state analysis · Experience redesign · Capability expansion",
        "Designed for founders, security engineers, and product teams",
    ]:
        canvas.drawString(MARGIN, y, line)
        y -= 6 * mm

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(MARGIN, 22 * mm, "Prepared as a product vision document for WASA")
    canvas.drawString(MARGIN, 16 * mm, "Stack today: React · Flask · Wappalyzer · Vulners · Nmap · Paramiko")
    canvas.setFillColor(CYAN)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(MARGIN, 10 * mm, "Think bigger than the code. Build the security OS teams actually use.")
    canvas.restoreState()


def img(path, max_w, max_h):
    p = Path(path)
    if not p.exists():
        return Spacer(1, 1)
    im = Image(str(p))
    im.hAlign = "CENTER"
    # scale
    iw, ih = im.imageWidth, im.imageHeight
    scale = min(max_w / iw, max_h / ih)
    im.drawWidth = iw * scale
    im.drawHeight = ih * scale
    return im


def bullet_list(items, st):
    flow = []
    for it in items:
        flow.append(Paragraph(f"•  {it}", st["BodyBullet"]))
    return flow


def make_table(headers, rows, col_widths, st):
    data = [[Paragraph(h, st["TableHead"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), st["TableCell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT, HexColor("#EEF2FF")]),
        ("GRID", (0, 0), (-1, -1), 0.4, SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def build():
    st = styles()
    content_w = PAGE_W - 2 * MARGIN
    story = []

    # ========== Cover (empty flowable content; drawing on first page) ==========
    story.append(Spacer(1, PAGE_H * 0.75))
    story.append(PageBreak())

    # ========== 1. Executive Summary ==========
    story.append(SectionBar("01  ·  Executive Summary", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("What WASA is today", st["H1"]))
    story.append(Paragraph(
        "WASA (Web Application Security Automation) is a master's thesis full-stack product that lets a user "
        "paste a target URL and run four security checks from a browser UI: <b>Reflected XSS</b>, "
        "<b>Error-based SQL Injection</b>, <b>Web technology fingerprinting with CVE lookup</b>, and "
        "<b>network-level credential attack on SSH/Telnet</b> (with post-exploitation file transfer intent). "
        "The experience is intentionally simple — one URL field and four action buttons — but under the hood "
        "it already combines frontend orchestration (React + MUI), a Flask API, and Python security tooling "
        "(BeautifulSoup, Wappalyzer, Vulners, nmap, paramiko).",
        st["Body"]
    ))
    story.append(Paragraph(
        "The strategic opportunity is large: the scaffolding of a <b>security automation product</b> exists, "
        "but the UX, scanner depth, safety controls, data model, and AI layer are still at prototype stage. "
        "This document treats WASA not only as current code, but as a product that can become a modern "
        "<b>AI-assisted AppSec + light Attack Surface Management</b> platform for students, freelancers, "
        "MSSPs, and engineering teams who need fast, explainable vulnerability feedback.",
        st["Body"]
    ))

    # KPI cards as table of colored boxes
    cards = [
        ColoredBox("Current value", [
            "One-click multi-module scans",
            "Web + network coverage mix",
            "CVE intel via Vulners",
            "Thesis-grade end-to-end demo",
        ], (content_w - 12) / 2, LIGHT, CYAN),
        ColoredBox("Primary gaps", [
            "UI is functional, not product-grade",
            "Shallow payloads / false positives",
            "No auth, jobs, history, reports",
            "Dangerous network abuse surface",
        ], (content_w - 12) / 2, LIGHT, CRITICAL),
    ]
    story.append(Spacer(1, 4))
    story.append(Table([[cards[0], cards[1]]], colWidths=[(content_w - 12) / 2, (content_w - 12) / 2],
                       hAlign="LEFT"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("North-star product statement", st["H2"]))
    story.append(Paragraph(
        "<i>“WASA is the fastest path from a URL to a trusted, explainable security brief — "
        "with AI that triages noise, narrates attack paths, and drafts fixes developers can ship.”</i>",
        st["Callout"]
    ))
    story.append(Spacer(1, 8))
    story.append(img(ASSETS / "hero.jpg", content_w, 58 * mm))
    story.append(Paragraph("Figure 1 — Brand / product mood: protection, automation, modern SaaS.", st["Caption"]))
    story.append(PageBreak())

    # ========== 2. Current System Analysis ==========
    story.append(SectionBar("02  ·  Current System Analysis", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Architecture as implemented", st["H1"]))
    story.append(Paragraph(
        "Today's WASA is a <b>two-process system</b> with Create React App on the frontend (proxying to "
        "Flask on port 5000). The React app (<font face='Courier'>src/App.js</font>) owns all scan UX state. "
        "Flask routes dispatch to Python modules for each scan type. An unused Express helper and an "
        "alternate <font face='Courier'>SecurityTester</font> component indicate exploratory iterations.",
        st["Body"]
    ))

    arch_rows = [
        ["React UI", "URL input + 4 scan buttons + result renderers", "src/App.js"],
        ["Flask API", "POST /scanXss, /scanSQLI, /detectTechnologies, /scanNetwork", "api/venv/api.py"],
        ["XSS engine", "Find forms, inject &lt;script&gt;alert, check reflection", "xssTest.py"],
        ["SQLi engine", "Append ' / \" ; detect SQL error strings", "sqliTest.py"],
        ["Tech intel", "Wappalyzer versions → Vulners softwareVulnerabilities", "api.py helpers"],
        ["Network", "Resolve host → nmap 22/23 → paramiko/telnet brute → optional SFTP put", "newNetAttack.py"],
    ]
    story.append(make_table(
        ["Layer", "Responsibility", "Primary file"],
        arch_rows,
        [28 * mm, content_w - 68 * mm, 40 * mm],
        st
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Feature-by-feature capability audit", st["H2"]))
    feat_rows = [
        ["Reflected XSS", "Medium", "Forms only; single payload; no DOM/stored/context awareness"],
        ["SQL Injection", "Low–Med", "Error-based only; tiny payload set; no blind/time-based/UNION"],
        ["Web Tech + CVE", "Medium", "Solid idea; depends on version detection quality + API key"],
        ["Network / Post-ex", "High risk", "Credential stuffing on 22/23 + file drop — powerful but unsafe without guardrails"],
        ["Reporting", "None", "Results are ephemeral UI text only"],
        ["Auth / multi-user", "None", "Open API; CORS * ; no tenancy"],
        ["Job system", "None", "Synchronous long scans can hang the browser"],
    ]
    story.append(make_table(
        ["Module", "Maturity", "Assessment"],
        feat_rows,
        [32 * mm, 22 * mm, content_w - 54 * mm],
        st
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Critical engineering & safety findings", st["H2"]))
    for b in [
        "<b>Hardcoded third-party API key</b> in source (Vulners) — rotate immediately; move to secrets manager / env.",
        "<b>Committed virtualenv</b> under <font face='Courier'>api/venv</font> bloats the repo and ships binaries/packages — replace with requirements.txt + clean install.",
        "<b>Network module performs real credential attacks</b> and can transfer files — must be gated by ownership proof, allowlists, and explicit lab mode.",
        "<b>No authentication / authorization</b> turns the product into an open scanning proxy if exposed publicly.",
        "<b>SQLi detector imports re inconsistently</b> (uses re without import in active path) — reliability risk.",
        "<b>UX state bugs</b> (e.g. web-tech empty result still marks testing true; mixed MUI v4/v5 styling) reduce trust.",
        "<b>Results are not structured</b> (free-text / ad-hoc objects) — blocks history, triage, and AI later.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("User experience of the current UI", st["H2"]))
    story.append(Paragraph(
        "The current interface is a <b>developer demo console</b>, not a security product. There is no brand shell, "
        "no progressive disclosure, no severity language, no empty/loading/error system design, and no path from "
        "finding → evidence → remediation. Four green buttons compete for attention with equal weight even though "
        "their risk profiles are radically different (XSS vs live network brute force). Visual design relies on "
        "light-blue body background and default Material inputs — functional, but not memorable or trustworthy "
        "for security buyers.",
        st["Body"]
    ))
    story.append(PageBreak())

    # ========== 3. UI/UX Vision ==========
    story.append(SectionBar("03  ·  UI/UX Design Vision", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Design principles", st["H1"]))
    principles = [
        ("Clarity over cleverness", "Every scan type states what it does, what it touches, and residual risk before launch."),
        ("Severity-first hierarchy", "Critical findings and live exploitability always surface above raw logs."),
        ("Evidence you can defend", "Each finding has request/response proof, confidence, and CWE/OWASP mapping."),
        ("Safe by default", "Network/post-ex modules require explicit lab mode + target ownership confirmation."),
        ("AI as copilot, not black box", "Models explain ranking and propose fixes; humans stay in control."),
        ("Calm dark operations aesthetic", "Navy/cyan system UI signals precision; reduce visual noise during long scans."),
    ]
    for title, body in principles:
        story.append(Paragraph(f"<b>{title}.</b> {body}", st["Body"]))

    story.append(Paragraph("Proposed information architecture", st["H2"]))
    for b in [
        "<b>Dashboard</b> — risk score, recent scans, trend sparklines, module health",
        "<b>New Scan wizard</b> — target → scope → modules → safety checks → launch",
        "<b>Findings inbox</b> — filterable by severity, asset, status, assignee",
        "<b>Finding detail</b> — evidence, AI narrative, remediations, retest",
        "<b>Attack surface map</b> — hosts, ports, tech stack, trust boundaries",
        "<b>AI Assistant</b> — chat over a scan corpus; “what should I fix first?”",
        "<b>Reports</b> — executive PDF, developer markdown, compliance exports",
        "<b>Integrations & Settings</b> — Jira/Slack/SIEM, API keys, org policy",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Spacer(1, 8))
    story.append(img(ASSETS / "moodboard.jpg", content_w, 52 * mm))
    story.append(Paragraph("Figure 2 — Visual direction: dark ops, cyan/indigo accents, modular cards.", st["Caption"]))

    story.append(Paragraph("Command Center UI (proposed)", st["H2"]))
    story.append(Paragraph(
        "The redesigned home is a <b>Security Command Center</b>: sticky scan bar, KPI strip (Critical / High / "
        "Medium / Risk Score), module grid with enable/disable + roadmap tags, and a priority findings rail "
        "auto-ranked by severity × confidence × exploitability. This replaces the flat four-button layout with "
        "progressive structure while preserving one-URL speed.",
        st["Body"]
    ))
    story.append(img(ASSETS / "mock-dashboard.png", content_w, 95 * mm))
    story.append(Paragraph(
        "Figure 3 — High-fidelity dashboard mock: modules, KPIs, and prioritized findings.",
        st["Caption"]
    ))
    story.append(PageBreak())

    story.append(Paragraph("Finding detail + AI remediation workspace", st["H1"]))
    story.append(Paragraph(
        "Security products win when a finding page answers four questions in under 30 seconds: "
        "<b>What is wrong?</b> <b>How bad is it?</b> <b>Prove it.</b> <b>How do I fix it?</b> "
        "The proposed detail view pairs classic evidence (HTTP request/response, parameters, CWE/OWASP) with an "
        "<b>AI Security Copilot</b> panel that writes an attack narrative, business impact, and copy-paste fix "
        "snippets in the project's language.",
        st["Body"]
    ))
    story.append(img(ASSETS / "mock-findings.png", content_w, 95 * mm))
    story.append(Paragraph(
        "Figure 4 — Finding detail with evidence and AI copilot remediation.",
        st["Caption"]
    ))

    story.append(Paragraph("Micro-UX specifications", st["H2"]))
    ux_rows = [
        ["Empty state", "Illustrate first scan; sample demo target; estimated time per module"],
        ["Loading", "Per-module progress stream; cancel; partial results as they arrive"],
        ["Errors", "Human messages + retry; never dump stack traces to end users"],
        ["Safety modal", "For network scans: confirm IP ownership, lab-only checkbox, rate limits"],
        ["Severity chips", "CRIT / HIGH / MED / LOW with consistent color tokens"],
        ["Accessibility", "WCAG AA contrast, keyboard scan launch, focus rings, reduced motion"],
        ["Mobile", "Read findings on phone; launch full scans on desktop/tablet primarily"],
    ]
    story.append(make_table(
        ["Moment", "Specification"],
        ux_rows,
        [32 * mm, content_w - 32 * mm],
        st
    ))
    story.append(PageBreak())

    # ========== 4. Functionality expansion ==========
    story.append(SectionBar("04  ·  Functionality Expansion (Beyond Current Code)", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Think like an AI cybersecurity product leader", st["H1"]))
    story.append(Paragraph(
        "WASA should evolve from four independent scripts into a <b>modular scanner fabric</b> with shared "
        "crawling, authentication contexts, evidence storage, and policy. Below is a capability backlog that "
        "intentionally goes far beyond the thesis implementation — because the market gap is not “another XSS "
        "button,” it is trustworthy automation + explanation + developer action.",
        st["Body"]
    ))

    story.append(Paragraph("A. Deepen existing modules", st["H2"]))
    for b in [
        "<b>XSS:</b> multi-context payloads (HTML, attribute, JS, URL); DOM XSS via headless browser; stored XSS crawl; CSP bypass checks; polyglots; mutation XSS.",
        "<b>SQLi:</b> boolean & time-based blind; UNION column enumeration; second-order; JSON/API parameter injection; ORM-aware heuristics; out-of-band where allowed.",
        "<b>Tech/CVE:</b> CPE normalization; EPSS + KEV prioritization; SBOM for detected JS libs; exploit-available flags; patch version guidance.",
        "<b>Network:</b> full service fingerprinting (not only 22/23); safe banner grab; credential checks only in authenticated lab mode; remove automatic file drop from default path.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("B. New AppSec scanner packs", st["H2"]))
    packs = [
        ["Auth & session", "Cookie flags, JWT alg confusion, session fixation, logout invalidate, password reset poisoning"],
        ["CSRF / CORS", "Token presence, SameSite, preflight reflection, null origin issues"],
        ["SSRF", "Webhook/URL fetch parameters, cloud metadata probe (lab-only)"],
        ["Access control", "IDOR heuristics, forced browsing, role swap testing with dual sessions"],
        ["Injection+", "Command, template (SSTI), LDAP, header injection, CRLF"],
        ["Client secrets", "API keys in JS bundles, source maps, exposed .git/.env"],
        ["API security", "OpenAPI-driven fuzzing, mass assignment, rate-limit absence, GraphQL introspection abuse"],
        ["TLS & headers", "HSTS, CSP quality score, cookie security, mixed content"],
        ["Upload & files", "Content-type bypass, path traversal, unrestricted extension"],
        ["Business logic", "Race conditions, coupon/price tamper patterns (semi-auto with AI hints)"],
    ]
    story.append(make_table(
        ["Pack", "Example checks"],
        packs,
        [32 * mm, content_w - 32 * mm],
        st
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("C. Attack Surface Management (light ASM)", st["H2"]))
    for b in [
        "Domain → subdomain discovery, live host detection, screenshotting, tech inventory over time.",
        "Change detection: new port, new tech version, new endpoint → auto re-scan.",
        "Asset ownership tags and environment labels (prod / staging / lab).",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("D. Platform product features", st["H2"]))
    for b in [
        "Async job queue, scan history, multi-target projects, RBAC, SSO.",
        "Evidence vault (requests, HTML snapshots, HAR) with retention policies.",
        "Exports: executive PDF, SARIF for GitHub code scanning, CSV, JSON API.",
        "Integrations: Jira, Linear, Slack, Teams, SIEM webhooks, GitHub PR comments.",
        "Policy engine: fail CI if Critical > 0; allowlist false positives; compliance maps (OWASP Top 10, PCI themes).",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))
    story.append(PageBreak())

    # ========== 5. AI Cybersecurity layer ==========
    story.append(SectionBar("05  ·  AI Cybersecurity Layer", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Where AI multiplies WASA", st["H1"]))
    story.append(Paragraph(
        "Scanners produce volume; humans need judgment. AI should sit <b>above</b> deterministic engines — "
        "never replace evidence-based detection as the sole truth. The winning pattern is: "
        "<b>classic engines find → AI explains, prioritizes, and remediates drafts → human approves.</b>",
        st["Body"]
    ))
    story.append(img(ASSETS / "ai-paths.jpg", content_w * 0.85, 70 * mm))
    story.append(Paragraph("Figure 5 — AI correlating assets into attack-path reasoning.", st["Caption"]))

    story.append(Paragraph("AI feature set", st["H2"]))
    ai_rows = [
        ["Smart triage", "Cluster duplicates, suppress known FP patterns, confidence calibration"],
        ["Attack path graph", "Chain XSS → session theft → admin; or SQLi → data access narratives"],
        ["Risk scoring", "Blend CVSS, EPSS, asset criticality, exposure, and exploit chatter"],
        ["Natural language brief", "CISO summary + developer ticket body in one click"],
        ["Fix generation", "Language-aware patches, unit tests, WAF virtual patch rules"],
        ["Payload synthesis", "LLM proposes next payloads when baseline checks fail (sandbox)"],
        ["Chat with scan", "RAG over findings + evidence: “Any path to PII?”"],
        ["Threat intel fusion", "Map tech stack to active campaigns / CISA KEV"],
        ["Anomaly reviews", "Diff consecutive scans; highlight meaningful deltas only"],
        ["Compliance mapping", "Auto tag controls (OWASP ASVS themes, ISO-style statements)"],
    ]
    story.append(make_table(
        ["AI capability", "Product behavior"],
        ai_rows,
        [38 * mm, content_w - 38 * mm],
        st
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Responsible AI & safety constraints", st["H2"]))
    for b in [
        "Never auto-execute destructive post-exploitation without multi-step confirmation and lab flag.",
        "Show model uncertainty; separate <b>observed evidence</b> from <b>inferred narrative</b>.",
        "Redact secrets in logs/prompts; do not train on customer traffic without contract.",
        "Rate-limit AI-generated active testing; default to passive analysis on production scopes.",
        "Maintain audit trail: who ran what, against which target, with which modules.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Spacer(1, 6))
    story.append(img(ASSETS / "ops-center.jpg", content_w, 55 * mm))
    story.append(Paragraph("Figure 6 — Future SOC-style visualization for multi-target risk.", st["Caption"]))
    story.append(PageBreak())

    # ========== 6. Target architecture ==========
    story.append(SectionBar("06  ·  Target Architecture", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("From prototype to platform", st["H1"]))
    story.append(Paragraph(
        "The target architecture separates <b>experience</b>, <b>API/policy</b>, <b>scan workers</b>, "
        "<b>AI intelligence</b>, and <b>data/integrations</b>. This allows horizontal scale of scanners, "
        "safer isolation of network modules, and pluggable AI providers without rewriting the UI.",
        st["Body"]
    ))
    story.append(img(ASSETS / "mock-architecture.png", content_w, 100 * mm))
    story.append(Paragraph(
        "Figure 7 — Target layered architecture and capability matrix (Now / Next / Vision).",
        st["Caption"]
    ))

    story.append(Paragraph("Recommended tech evolution", st["H2"]))
    tech_rows = [
        ["Frontend", "React 18+/Next.js, design system (tokens), charts, virtualized findings tables"],
        ["API", "FastAPI or hardened Flask, OpenAPI, JWT/OIDC, per-org API keys"],
        ["Workers", "Celery/RQ/Arq + Redis; browser pool (Playwright) for DOM XSS"],
        ["Data", "Postgres (findings), object store (evidence), optional OpenSearch"],
        ["AI", "Gateway with tool calling over findings DB; structured outputs for tickets"],
        ["Ops", "Docker Compose → K8s; secret manager; SBOM; CI SARIF gate"],
    ]
    story.append(make_table(
        ["Area", "Direction"],
        tech_rows,
        [28 * mm, content_w - 28 * mm],
        st
    ))
    story.append(PageBreak())

    # ========== 7. Roadmap ==========
    story.append(SectionBar("07  ·  Phased Roadmap", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("90-day to 12-month plan", st["H1"]))

    story.append(Paragraph("Phase 0 — Stabilize & secure the thesis (2–3 weeks)", st["H2"]))
    for b in [
        "Remove committed venv; add requirements.txt / lockfiles; env-based secrets; rotate exposed keys.",
        "Fix SQLi module imports/reliability; normalize all scanner outputs to a Finding schema (JSON).",
        "Add basic auth for API; disable network module unless LAB_MODE=true.",
        "Loading/error/empty states; disable buttons while scanning; cancel support.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("Phase 1 — Product UX shell (1–2 months)", st["H2"]))
    for b in [
        "Implement Command Center + Findings list + Finding detail from the mocks in this document.",
        "Scan history, project/target entities, PDF export of a single scan.",
        "Severity model, OWASP/CWE tags, evidence attachment for HTTP based modules.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("Phase 2 — Scanner depth (2–4 months)", st["H2"]))
    for b in [
        "Headless browser XSS; blind SQLi; security headers/TLS pack; secrets-in-JS.",
        "Authenticated scanning (cookie/session import).",
        "Async workers + progress events (SSE/WebSocket).",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("Phase 3 — AI copilot (parallel after schema exists)", st["H2"]))
    for b in [
        "Summaries, prioritization, fix drafts, chat-with-findings RAG.",
        "Attack path graph v1 for multi-finding correlation.",
        "Human-in-the-loop controls and prompt/audit logging.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("Phase 4 — Platform & GTM (6–12 months)", st["H2"]))
    for b in [
        "SSO, multi-tenant, integrations, CI SARIF, continuous ASM light.",
        "Marketplace of scanner packs; on-prem option for regulated customers.",
        "Positioning: “AI AppSec for teams who outgrew one-off scripts.”",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Spacer(1, 10))
    # Timeline visual via table
    story.append(make_table(
        ["Phase", "Focus", "Exit criteria"],
        [
            ["0", "Safety & schema", "No secrets in git; Finding JSON; lab gate"],
            ["1", "UI shell", "Dashboard + history + PDF users trust"],
            ["2", "Scanner depth", "≥8 modules; async jobs; auth scan"],
            ["3", "AI layer", "Triage + fixes reduce MTTR measurably"],
            ["4", "Platform", "Multi-tenant pilot / CI integration"],
        ],
        [18 * mm, 40 * mm, content_w - 58 * mm],
        st
    ))
    story.append(PageBreak())

    # ========== 8. UX writing & design system ==========
    story.append(SectionBar("08  ·  Design System & UX Writing", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Visual language", st["H1"]))
    story.append(Paragraph(
        "Use a dark operational canvas (<font face='Courier'>#0B1220</font>) with cyan/indigo accents for "
        "primary actions, rose/amber/blue/emerald for severity, Inter or system UI fonts, 12–16px radii, "
        "and card-based layout. Avoid playful illustrations in the scan path; reserve motion for progress "
        "and success confirmation only.",
        st["Body"]
    ))
    # Color swatches as table
    swatch_data = [[
        Paragraph("<b>Navy</b><br/>#0B1220", st["Small"]),
        Paragraph("<b>Cyan</b><br/>#22D3EE", st["Small"]),
        Paragraph("<b>Indigo</b><br/>#6366F1", st["Small"]),
        Paragraph("<b>Critical</b><br/>#E11D48", st["Small"]),
        Paragraph("<b>High</b><br/>#D97706", st["Small"]),
        Paragraph("<b>OK</b><br/>#059669", st["Small"]),
    ]]
    sw = Table(swatch_data, colWidths=[content_w / 6.0] * 6)
    sw.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), NAVY),
        ("BACKGROUND", (1, 0), (1, 0), CYAN),
        ("BACKGROUND", (2, 0), (2, 0), INDIGO),
        ("BACKGROUND", (3, 0), (3, 0), CRITICAL),
        ("BACKGROUND", (4, 0), (4, 0), HIGH),
        ("BACKGROUND", (5, 0), (5, 0), OK),
        ("TEXTCOLOR", (0, 0), (0, 0), white),
        ("TEXTCOLOR", (1, 0), (1, 0), NAVY),
        ("TEXTCOLOR", (2, 0), (2, 0), white),
        ("TEXTCOLOR", (3, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 0.5, SOFT),
    ]))
    story.append(sw)
    story.append(Paragraph("Figure 8 — Core color tokens for UI consistency.", st["Caption"]))

    story.append(Paragraph("Voice & microcopy", st["H2"]))
    for b in [
        "Prefer precise verbs: <i>Run scan</i>, <i>Retest finding</i>, <i>Export evidence</i> — not “Hack now.”",
        "Network module copy must say <b>Credential security audit (lab only)</b>, never “Attack server.”",
        "Error: “We couldn’t reach the target (timeout). Check URL and network.” + Retry.",
        "Success: “Scan complete · 3 critical · 7 high · View prioritized fix plan.”",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))

    story.append(Paragraph("Component inventory to build first", st["H2"]))
    for b in [
        "ScanBar, ModuleCard, SeverityChip, FindingRow, EvidenceBlock, AiPanel, SafetyConfirmModal, ProgressStream, EmptyState, ReportShell.",
    ]:
        story.append(Paragraph(f"•  {b}", st["BodyBullet"]))
    story.append(PageBreak())

    # ========== 9. Competitive & success ==========
    story.append(SectionBar("09  ·  Positioning, Metrics & Success", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph("How WASA can win a niche", st["H1"]))
    story.append(Paragraph(
        "Enterprise scanners (Burp Enterprise, Invicti, etc.) are heavy and expensive. Raw scripts are free but "
        "unusable for non-experts. WASA can own the middle: <b>beautiful, explainable, AI-assisted automation</b> "
        "for labs, education, indie hackers, and small product teams — with a clear ethical boundary and "
        "export paths into professional workflows.",
        st["Body"]
    ))

    story.append(Paragraph("Success metrics", st["H2"]))
    metrics = [
        ["Time-to-first-finding", "< 60s on a demo DVWA-like target"],
        ["False positive rate", "Track & drive down with AI+rules; publish confidence"],
        ["MTTR assist", "% of criticals with accepted fix draft within 1 day"],
        ["Activation", "% users who complete second scan within 7 days"],
        ["Safety", "0 unauthenticated public abuse incidents; 100% lab-gated network runs"],
        ["Trust", "NPS / “would show this report to my manager” qualitative score"],
    ]
    story.append(make_table(
        ["Metric", "Target intent"],
        metrics,
        [45 * mm, content_w - 45 * mm],
        st
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Immediate next actions (this week)", st["H2"]))
    for i, b in enumerate([
        "Rotate any committed API keys; scrub git history if needed.",
        "Define Finding JSON schema shared by all scanners.",
        "Prototype the Command Center UI in the existing React app (even static).",
        "Wrap network module behind LAB_MODE + confirmation dialog.",
        "Write one golden-path demo script (DVWA/Juice Shop) for UX testing.",
        "Decide AI provider strategy (gateway + structured outputs) after schema lands.",
    ], 1):
        story.append(Paragraph(f"<b>{i}.</b>  {b}", st["BodyBullet"]))

    story.append(Spacer(1, 14))
    story.append(SectionBar("Closing", content_w))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "WASA already proves the hardest early thesis claim: a person can drive meaningful security checks "
        "from a browser against a live target. The next leap is product craft — structured findings, "
        "safety, depth, and an AI layer that turns raw detections into decisions. With the UI direction "
        "and capability roadmap in this document, WASA can grow from a master's project into a distinctive "
        "security automation product that people trust enough to run every week.",
        st["Body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Design thesis:</b> Security tools fail when they dump noise. WASA will win when every screen "
        "reduces cognitive load, every module declares its blast radius, and every finding ends in a fix.",
        st["Callout"]
    ))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=CYAN, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(
        "Document artifacts: high-fidelity HTML/PNG mocks in docs/pdf-assets/ · regenerate via docs/generate_wasa_vision_pdf.py",
        st["Small"]
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="WASA Product Vision, UI/UX & AI Security Roadmap",
        author="WASA Product Design",
        subject="Analysis and future vision for Web Application Security Automation",
    )
    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    print(f"Wrote {OUT}")
    return OUT


if __name__ == "__main__":
    build()
