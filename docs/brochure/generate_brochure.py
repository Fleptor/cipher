#!/usr/bin/env python3
"""Build the one-page CIPHER brochure as PDF and editable Word documents.

Run with the packages in requirements.txt. Fonts and branding assets are local;
the generator makes no network requests. See BUILD_AND_SOURCES.txt for provenance.
"""
from pathlib import Path
import json
from xml.sax.saxutils import escape

import qrcode
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
BRAND = HERE.parents[1] / "website/brand"
THEME = json.loads((BRAND / "theme.json").read_text())
FONTS = BRAND / "fonts"
STEM = "CIPHER_Technical_Sheet"
SITE = "https://belalhamdan.com/cipher/"
BLUE, INK, MUTED, PALE, LINE = (THEME[k] for k in ("blue", "ink", "muted", "pale", "line"))
ORANGE, DARK = THEME["orange"], THEME["dark"]
INTRO = (
    "A security prototype for small offices, shops, and schools. CIPHER learns "
    "each device’s normal traffic pattern, flags unusual behavior, and explains "
    "the evidence so an operator can choose a response."
)
FLOW = [
    ("01  OBSERVE", "Linux router", "eBPF / XDP\nTraffic hook"),
    ("02  SUMMARIZE", "Rust sensor", "Sampled traffic\nmetadata"),
    ("03  ANALYZE", "Rust server", "Statistics +\nAI review"),
    ("04  RESPOND", "Web dashboard", "Review +\ndevice control"),
]
TRANSPORT = "FlatBuffers reports over a TLS WebSocket · Axum server · SQLite persistence"
DETECTION = [
    ("50 reports per device", " establish a baseline of normal activity."),
    ("Four signals: ", "incoming bytes, outgoing bytes, dropped events, and port entropy (how varied port use is)."),
    ("Statistics flag the change. ", "An optional AI reviewer explains the evidence and recommends a response."),
    ("", "Measurements are sampled observations. An anomaly is a reason to investigate, not proof of an attack."),
]
CONTROL = [
    ("Monitor and alert is the default. ", "Operators can trust devices, review incidents, and manually isolate or restore a device."),
    ("Cloud auto-isolation ", "requires enforcement mode, an untrusted device, at least two abnormal signals, and a valid block recommendation scored at least 85/100. The incident must remain open and policy unchanged."),
    ("", "The score is the model’s own assessment, not a measured probability."),
]
BOUNDARY = (
    "Local edge rules are separate. Monitor mode does not disable packet filters "
    "or clear existing blocks."
)
STATUS = [
    ("Working software: ", "detection, incident review, saved baselines, trust controls, acknowledgments, and retries."),
    ("Booth demo: ", "simulated sensor and scripted reviewer with the real backend; no live packet blocking. Hardware enforcement and detection accuracy still need validation."),
]


def pdf():
    for weight in ("Regular", "SemiBold", "Bold"):
        pdfmetrics.registerFont(TTFont(f"OpenSans-{weight}", str(FONTS / f"OpenSans-{weight}.ttf")))
    for weight in ("Medium", "Bold"):
        pdfmetrics.registerFont(TTFont(f"Montserrat-{weight}", str(FONTS / f"Montserrat-{weight}.ttf")))
    pdfmetrics.registerFontFamily("OpenSans-Regular", normal="OpenSans-Regular", bold="OpenSans-Bold")
    width, height = A4
    c = canvas.Canvas(str(HERE / f"{STEM}.pdf"), pagesize=A4, pageCompression=1,
                      invariant=1, initialFontName="OpenSans-Regular")
    c.setTitle("CIPHER | Network detection and response")
    c.setAuthor("The Four Horsemen / IEEE Computer Society")
    c.setSubject("One-page project technical sheet")
    c.setKeywords("CIPHER, IEEE Computer Society, eBPF, XDP, Rust, network security, prototype")
    c._doc.Catalog.Lang = "en-US"
    margin, usable = 42, width - 84

    def rect(x, top, w, h, fill):
        c.setFillColor(colors.HexColor(f"#{fill}"))
        c.rect(x, height-top-h, w, h, fill=1, stroke=0)

    def para(value, x, top, w, size=10.4, leading=14.5, color=INK, font="Regular", max_h=None):
        face = {"Display": "Montserrat-Medium", "DisplayBold": "Montserrat-Bold"}.get(font, f"OpenSans-{font}")
        style = ParagraphStyle("sheet", fontName=face, fontSize=size,
                               leading=leading, textColor=colors.HexColor(f"#{color}"),
                               spaceAfter=0, spaceBefore=0)
        p = Paragraph(value, style)
        _, h = p.wrap(w, height)
        if max_h is not None and h > max_h + 0.1:
            raise ValueError(f"Text exceeds its region ({h} > {max_h}): {value}")
        if top+h > height-24:
            raise ValueError(f"Text exceeds the page: {value}")
        p.drawOn(c, x, height-top-h)
        return h

    def body(items, x, top, w):
        y = top
        for lead, value in items:
            y += para(f"<b>{escape(lead)}</b>{escape(value)}", x, y, w) + 8
        return y - 8

    rect(margin, 39, usable, 132, DARK)
    rect(margin, 39, usable, 4, ORANGE)
    para("IEEE BAU COMPUTER SOCIETY", margin+12, 56, 345, 8.5, 11, ORANGE, "DisplayBold")
    para("TECHNICAL SHEET / 2026", 421, 56, 120, 8, 11, "FFFFFF")
    para("CIPHER", margin+12, 82, usable-24, 46, 56, "FFFFFF", "DisplayBold")
    para("Network detection and response", margin+12, 142, usable-24, 17.4, 23, "FFFFFF", "Display")
    para(INTRO, margin, 182, usable, 11.3, 16, max_h=48)

    para("FROM NETWORK TRAFFIC TO OPERATOR ACTION", margin, 247, usable, 9.3, 12, INK, "DisplayBold")
    gap = 15
    box_w = (usable - 3*gap)/4
    for i, (label, title, detail) in enumerate(FLOW):
        x = margin + i*(box_w+gap)
        rect(x, 269, box_w, 78, PALE)
        rect(x, 269, box_w, 2, ORANGE)
        para(label, x+10, 279, box_w-20, 7.2, 10, INK, "DisplayBold")
        para(title, x+10, 295, box_w-20, 10.2, 13, INK, "Bold", max_h=13)
        para(escape(detail).replace("\n", "<br/>"), x+10, 315, box_w-20, 9.1, 12, MUTED)
        if i < 3:
            y = height-307
            c.setStrokeColor(colors.HexColor(f"#{BLUE}"))
            c.setLineWidth(.8)
            c.line(x+box_w+3, y, x+box_w+12, y)
            c.line(x+box_w+9, y+2.5, x+box_w+12, y)
            c.line(x+box_w+9, y-2.5, x+box_w+12, y)
    para(TRANSPORT, margin, 357, usable, 8.4, 11.5, MUTED)

    col_w = (usable-30)/2
    right = margin+col_w+30
    rect(margin, 383, 32, 3, ORANGE)
    rect(right, 383, 32, 3, ORANGE)
    para("How detection works", margin, 398, col_w, 13.8, 19, INK, "DisplayBold")
    para("Operator control", right, 398, col_w, 13.8, 19, INK, "DisplayBold")
    end_left = body(DETECTION, margin, 423, col_w)
    end_right = body(CONTROL, right, 423, col_w)
    if max(end_left, end_right) > 627:
        raise ValueError(f"Columns exceed allotted space: {end_left}, {end_right}")

    para(BOUNDARY, margin, 628, usable, 8.5, 12, MUTED, max_h=24)
    rect(margin, 667, usable, 82, PALE)
    rect(margin, 667, 3, 82, ORANGE)
    para("PROTOTYPE AND DEMO", margin+12, 677, usable-24, 8.8, 12, INK, "DisplayBold")
    y = 696
    for lead, value in STATUS:
        y += para(f"<b>{escape(lead)}</b>{escape(value)}", margin+12, y, usable-24,
                  9.1, 12.5) + 5
    if y-5 > 743:
        raise ValueError(f"Status panel overflow: {y}")

    # The user's complete branch artwork replaces the generic IEEE master mark.
    c.drawImage(str(ASSETS / "project-qr.png"), margin, height-817, width=54, height=54)
    para("See the demo and explore the project", 111, 766, 303, 9.8, 14, INK, "SemiBold")
    para(f'<link href="{SITE}" color="#{BLUE}">{SITE.removeprefix("https://")}</link>',
         111, 785, 303, 8.7, 12)
    para("The Four Horsemen · @ieee_bau_cs", 111, 803, 303, 8, 11, MUTED)
    c.drawImage(str(BRAND / THEME["branch_logo"]), width-margin-114, height-821,
                width=114, height=114*876/1795, mask="auto")
    c.linkURL(SITE, (margin, height-817, margin+54, height-763), relative=0)
    c.showPage()
    c.save()


def word():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.top_margin, sec.bottom_margin = Mm(14), Mm(12)
    sec.left_margin = sec.right_margin = Mm(15)
    sec.header_distance = sec.footer_distance = Mm(5)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "Open Sans", Pt(10)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.line_spacing = 1.13
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.widow_control = True
    for name in ("Title", "Subtitle", "Heading 1", "Heading 2"):
        doc.styles[name].font.name = "Montserrat"
    doc.core_properties.title = "CIPHER | Network detection and response"
    doc.core_properties.author = "The Four Horsemen / IEEE Computer Society"
    doc.core_properties.subject = "One-page project technical sheet"
    lang = OxmlElement("w:lang")
    lang.set(qn("w:val"), "en-US")
    normal.element.get_or_add_rPr().append(lang)

    def text(parent, value="", size=10, bold=False, color=INK, after=6, before=0, line=1.13, reuse=False, font="Open Sans"):
        p = parent.paragraphs[0] if reuse else parent.add_paragraph()
        p.paragraph_format.space_after, p.paragraph_format.space_before = Pt(after), Pt(before)
        p.paragraph_format.line_spacing = line
        r = p.add_run(value)
        r.font.name, r.font.size, r.font.bold = font, Pt(size), bold
        r.font.color.rgb = RGBColor.from_string(color)
        return p

    def mixed(parent, lead, value, size=10, after=7):
        p = text(parent, lead, size, True, after=after)
        r = p.add_run(value)
        r.bold = False
        r.font.size = Pt(size)
        return p

    def cell_setup(cell, fill=None, pad=100):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        pr = cell._tc.get_or_add_tcPr()
        margins = OxmlElement("w:tcMar")
        for side in ("top", "left", "bottom", "right"):
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:w"), str(pad))
            el.set(qn("w:type"), "dxa")
            margins.append(el)
        pr.append(margins)
        if fill:
            shd = OxmlElement("w:shd")
            shd.set(qn("w:fill"), fill)
            pr.append(shd)
        cell.paragraphs[0].paragraph_format.space_after = Pt(0)
        cell.paragraphs[0].paragraph_format.line_spacing = Pt(1)
        cell.paragraphs[0].add_run().font.size = Pt(1)

    def table(widths):
        t = doc.add_table(rows=1, cols=len(widths))
        t.autofit = False
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{edge}")
            el.set(qn("w:val"), "nil")
            borders.append(el)
        t._tbl.tblPr.append(borders)
        for col, cell, w in zip(t.columns, t.rows[0].cells, widths):
            col.width = cell.width = Mm(w)
        for row in t.rows:
            row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        return t

    hero = table([180]).cell(0, 0)
    cell_setup(hero, DARK, 160)
    p = text(hero, "IEEE BAU COMPUTER SOCIETY\tTECHNICAL SHEET / 2026",
             7.6, True, ORANGE, after=8, reuse=True, font="Montserrat")
    p.paragraph_format.tab_stops.add_tab_stop(Mm(174), WD_TAB_ALIGNMENT.RIGHT)
    borders = OxmlElement("w:pBdr")
    border = OxmlElement("w:top")
    for k, v in {"val":"single", "sz":"22", "space":"5", "color":ORANGE}.items():
        border.set(qn(f"w:{k}"), v)
    borders.append(border)
    p._p.get_or_add_pPr().append(borders)
    text(hero, "CIPHER", 39, True, "FFFFFF", after=4, line=1, font="Montserrat")
    text(hero, "Network detection and response", 16, False, "FFFFFF", after=2, font="Montserrat")
    text(doc, INTRO, 11, before=10, after=14, line=1.18)
    text(doc, "FROM NETWORK TRAFFIC TO OPERATOR ACTION", 8.8, True, INK, after=7, font="Montserrat")
    flow = table([41.25, 5, 41.25, 5, 41.25, 5, 41.25])
    for i, (label, title, detail) in enumerate(FLOW):
        cell = flow.cell(0, i*2)
        cell_setup(cell, PALE, 100)
        text(cell, label, 7.3, True, INK, 4, reuse=True, font="Montserrat")
        text(cell, title, 10, True, after=4)
        text(cell, detail, 9, color=MUTED, after=2)
        if i < 3:
            arrow = flow.cell(0, i*2+1)
            cell_setup(arrow, pad=0)
            arrow.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = text(arrow, "→", 9, color=BLUE, after=0, reuse=True)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    text(doc, TRANSPORT, 8.2, color=MUTED, before=5, after=13)

    columns = table([85, 10, 85])
    for index, heading, items in [(0, "How detection works", DETECTION), (2, "Operator control", CONTROL)]:
        cell = columns.cell(0, index)
        cell_setup(cell, pad=0)
        text(cell, heading, 13.3, True, INK, after=9, reuse=True, font="Montserrat")
        for lead, value in items:
            mixed(cell, lead, value, 10, 7)
    text(doc, BOUNDARY, 8.5, color=MUTED, after=10)

    status = table([180]).cell(0, 0)
    cell_setup(status, PALE, 130)
    text(status, "PROTOTYPE AND DEMO", 8.8, True, INK, after=5, reuse=True, font="Montserrat")
    for lead, value in STATUS:
        mixed(status, lead, value, 9, after=4)
    text(doc, "", size=1, after=4, line=1)

    footer = table([23, 108, 8, 41])
    for cell in footer.rows[0].cells:
        cell_setup(cell, pad=0)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = footer.cell(0, 0).paragraphs[0]
    p.paragraph_format.line_spacing = 1.0
    qr = p.add_run().add_picture(str(ASSETS / "project-qr.png"), width=Mm(20))
    qr._inline.docPr.set("descr", "QR code linking to the CIPHER project website")
    cell = footer.cell(0, 1)
    text(cell, "See the demo and explore the project", 10, True, after=4, reuse=True)
    p = text(cell, "", 8.5, after=5)
    link = OxmlElement("w:hyperlink")
    rel = doc.part.relate_to(SITE, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    link.set(qn("r:id"), rel)
    r, props = OxmlElement("w:r"), OxmlElement("w:rPr")
    for name, attr, val in [("color", "val", BLUE), ("sz", "val", "17")]:
        el = OxmlElement(f"w:{name}")
        el.set(qn(f"w:{attr}"), val)
        props.append(el)
    r.append(props)
    t = OxmlElement("w:t")
    t.text = SITE.removeprefix("https://")
    r.append(t)
    link.append(r)
    p._p.append(link)
    text(cell, "The Four Horsemen · @ieee_bau_cs", 8, color=MUTED, after=0)
    p = footer.cell(0, 3).paragraphs[0]
    p.paragraph_format.line_spacing = 1.0
    logo = p.add_run().add_picture(str(BRAND / THEME["branch_logo"]), width=Mm(40))
    logo._inline.docPr.set("descr", "IEEE Al-Balqa Applied University, Faculty of Engineering Technology branch logo")
    doc.save(HERE / f"{STEM}.docx")


def main():
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=4)
    qr.add_data(SITE)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(ASSETS / "project-qr.png")
    pdf()
    word()
    print(f"Created {HERE / (STEM + '.pdf')}")
    print(f"Created {HERE / (STEM + '.docx')}")


if __name__ == "__main__":
    main()
