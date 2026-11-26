import sys, io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
src, dst = sys.argv[1:3]; items = [(int(a.split(':')[0]), a.split(':')[1]) for a in sys.argv[3:]]
pdfmetrics.registerFont(TTFont('Pag', '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/fonts/pagella-regular.ttf'))
w = PdfWriter(clone_from=src)
for idx, num in items:
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(595.28, 841.89))
    c.setFillColorRGB(1, 1, 1); c.rect(60, 778, 56, 20, stroke=0, fill=1); c.setFillColorRGB(0, 0, 0)
    if num != '-': c.setFont('Pag', 9.9626); c.drawString(76.7, 787, num)
    c.showPage(); c.save(); buf.seek(0)
    w.pages[idx].merge_page(PdfReader(buf).pages[0])
w.write(dst)
