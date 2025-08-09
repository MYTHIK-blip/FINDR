from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from textwrap import wrap

def render_pdf(md_text: str, out_path: str):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    margin = 2*cm
    y = height - margin
    # naive markdown-to-lines: treat as plain text with headings emphasized
    for line in md_text.splitlines():
        if line.startswith("# "): c.setFont("Helvetica-Bold", 14); text=line[2:]
        elif line.startswith("## "): c.setFont("Helvetica-Bold", 12); text=line[3:]
        elif line.startswith("### "): c.setFont("Helvetica-Bold", 11); text=line[4:]
        else: c.setFont("Helvetica", 10); text=line
        for wl in wrap(text, 100):
            if y < margin: c.showPage(); y = height - margin
            c.drawString(margin, y, wl); y -= 12
        if y < margin: c.showPage(); y = height - margin
        y -= 6
    c.save()
