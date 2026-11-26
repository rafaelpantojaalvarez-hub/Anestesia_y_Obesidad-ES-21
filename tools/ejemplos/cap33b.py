import sys, io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
lang, src, dst, idx = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
pdfmetrics.registerFont(TTFont('Pag', '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/fonts/pagella-regular.ttf'))
cap = ("Acceso venoso central de la vena yugular interna del lado derecho en paciente obeso bajo guía ecográfica fuera de plano, con transductor lineal de alta frecuencia." if lang == 'es'
       else "Central venous access of the right internal jugular vein in a patient with obesity under out-of-plane ultrasound guidance, with a high-frequency linear transducer.")
cx = 293.6 if lang == 'es' else 301.6; x0 = cx - 435/2; TW = 435.0
FS, LH, H = 9.93, 12.55, 841.89
f = lambda t: pdfmetrics.stringWidth(t, 'Pag', FS)
sp = f(' '); lines = []; cur = []; cw = 0
for w_ in cap.split(' '):
    ww = f(w_)
    if cur and cw+sp+ww > TW: lines.append(cur); cur = [w_]; cw = ww
    else: cw += (sp if cur else 0)+ww; cur.append(w_)
lines.append(cur)
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(595.28, H)); c.setFont('Pag', FS); y = H-(562+16+8)
for i, ws in enumerate(lines):
    last = i == len(lines)-1; tw = sum(f(w_) for w_ in ws); gaps = len(ws)-1
    g = (TW-tw)/gaps if (not last and gaps) else sp
    x = x0 if not last else cx-(tw+g*gaps)/2
    for w_ in ws: c.drawString(x, y, w_); x += f(w_)+g
    y -= LH
c.showPage(); c.save(); buf.seek(0)
w = PdfWriter(clone_from=src); w.pages[idx].merge_page(PdfReader(buf).pages[0]); w.write(dst); print(len(lines), 'lineas')
