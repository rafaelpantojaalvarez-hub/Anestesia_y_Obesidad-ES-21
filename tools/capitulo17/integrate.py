import sys, json, io
sys.path.insert(0, '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/ch17')
import typeset  # registra fuentes
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
H = 841.89
lang, src, chap, dst = sys.argv[1:5]
toc = json.load(open(chap.replace('.pdf', '_toc.json')))
f = lambda t, s: pdfmetrics.stringWidth(t, 'Pag', s)
if lang == 'es':
    P = dict(ins=251, abbr_kid=252, remove_blank=None, toc_kid=14, ref_base=483.8, x0=76.3, xs=92.9, xt=120.2, dots_end=483.1, pr=517.0,
             chap_title=["Cuidados posanestésicos, criterios de alta y tromboprofilaxis", "en el paciente con obesidad"],
             secs=["Principios generales", "Estratificación del riesgo antes del alta de la URPA", "Consideraciones ventilatorias", "Consideraciones cardiovasculares",
                   "Consideraciones analgésicas y quirúrgicas", "Criterios de alta de la URPA a la sala", "Alta el mismo día", "Tromboprofilaxis tras la cirugía bariátrica",
                   "Trombosis portomesentérica", "Caso clínico"], ref="Referencias", tail="Siglas", abbr_new='240', abbr_title='SIGLAS', abbr_mirror=False)
else:
    P = dict(ins=249, abbr_kid=251, remove_blank=249, toc_kid=14, ref_base=504.0, x0=84.2, xs=100.8, xt=128.9, dots_end=491.0, pr=516.2,
             chap_title=["Postanesthesia Care, Discharge Criteria, and", "Thromboprophylaxis in the Patient with Obesity"],
             secs=["General Principles", "Risk Stratification Before PACU Discharge", "Ventilatory Considerations", "Cardiovascular Considerations",
                   "Analgesic and Surgical Considerations", "Criteria for Discharge from the PACU to the Ward", "Same-Day Discharge", "Thromboprophylaxis After Bariatric Surgery",
                   "Portomesenteric Vein Thrombosis", "Clinical Case"], ref="References", tail="Abbreviations", abbr_new='238', abbr_title='ABBREVIATIONS', abbr_mirror=True)
nchap = len(PdfReader(chap).pages)
w = PdfWriter(clone_from=src)
kids = w._root_object['/Pages']['/Kids']
def overlay(fn):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(595.28, H)); fn(c); c.showPage(); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]
# --- 1) cabecera de la 2.a pagina de Siglas/Abbreviations
def hdr(c):
    c.setFillColorRGB(1, 1, 1)
    if P['abbr_mirror']: c.rect(66, 778, 470, 22, stroke=0, fill=1)
    else: c.rect(70, 779, 36, 20, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0); c.setFont('Pag', 9.9626); c.drawString(76.7, 787, P['abbr_new'])
    if P['abbr_mirror']:
        c.setFont('Pag', 7.9); c.drawRightString(511.2, 787, P['abbr_title'])
w.pages[P['abbr_kid']].merge_page(overlay(hdr))
# --- 2) indice general
def tocdraw(c):
    rb = P['ref_base']; step = 14.3; gap = 24.4
    c.setFillColorRGB(1, 1, 1); c.rect(P['x0']-8, H-(rb+gap+6), 470, 22, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)
    def dots(x1, x2, y):
        c.setFont('Pag', 10.9091); x = x1
        while x < x2: c.drawString(x, y, '.'); x += 4.35
    def pnum(n, y, size=10.9091):
        c.setFont('Pag', size); c.drawRightString(P['pr'], y, str(n))
    y = H - (rb + gap)
    c.setFont('Pag', 10.9091); c.drawString(P['x0'], y, '17'); c.drawString(P['x0']+17.5, y, P['chap_title'][0])
    y -= step
    c.drawString(P['x0']+17.5, y, P['chap_title'][1]); xe = P['x0']+17.5+f(P['chap_title'][1], 10.9091)
    dots(xe+5, P['dots_end'], y); pnum(toc['17.1.'], y + step) if False else pnum(toc['17.1.'], y, 10.9091)
    for i, t in enumerate(P['secs']):
        y -= step; lab = '17.%d.' % (i+1)
        c.setFont('Pag', 10.9091); xt = max(P['xt'], P['xs']+f(lab, 10.9091)+3.5); c.drawString(P['xs'], y, lab); c.drawString(xt, y, t)
        dots(xt+f(t, 10.9091)+5, P['dots_end'], y); pnum(toc[lab], y)
    y -= step; c.setFont('Pag', 10.9091); c.drawString(P['xs'], y, P['ref']); dots(P['xs']+f(P['ref'], 10.9091)+4, P['dots_end'], y); pnum(toc['REF'], y)
    y -= gap; c.setFont('Pag', 10.9091); c.drawString(P['x0'], y, P['tail']); dots(P['x0']+f(P['tail'], 10.9091)+5, P['dots_end'] + 0, y)
w.pages[P['toc_kid']].merge_page(overlay(tocdraw))
# --- 3) insertar capitulo y retirar la pagina en blanco (EN)
rdr = PdfReader(chap)
for i in range(nchap):
    w.insert_page(rdr.pages[i], P['ins'] + i)
if P['remove_blank'] is not None:
    idx = P['remove_blank'] + nchap
    blank = w.pages[idx]
    c0 = blank.get_contents()
    assert c0 is None or len(c0.get_data()) < 200, 'la pagina no esta en blanco'
    w.remove_page(idx)
w.write(dst); print('ok', dst, len(w.pages))
