import sys, re, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
lang, src, dst = sys.argv[1:4]
S = '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/'
IM = ['/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/images/%d.jpg' % i for i in (7, 8, 9)]
IMS = [(1196, 2000), (1171, 2000), (1171, 2000)]
pdfmetrics.registerFont(TTFont('Pag', S+'fonts/pagella-regular.ttf'))
H = 841.89
if lang == 'es':
    Ai, Bi = 149, 150; lab = 'FIGURA'
    cap = "Secuencia de intubación despierta con fibrobroncoscopio en paciente obeso con vía aérea difícil."
else:
    Bi = 148; lab = 'FIGURE'
    cap = "Awake intubation sequence with a fiberoptic bronchoscope in a patient with obesity and a difficult airway."
x0, TW, cx = 76.68, 433.9, 293.6
FS, SC, LH = 9.93, 7.5, 12.55
f = lambda t, s: pdfmetrics.stringWidth(t, 'Pag', s)
IMH = 225.0; widths = [IMH*w/h for (w, h) in IMS]; gap = (435.0 - sum(widths))/2.0

def figure_overlay(img_top):
    """dibuja imagenes y leyenda; devuelve (pagina overlay, alto total hasta el fondo de la leyenda en coordenadas desde arriba)"""
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(595.28, H))
    x = cx - 435.0/2
    for p_, w_ in zip(IM, widths):
        c.drawImage(p_, x, H-img_top-IMH, w_, IMH); x += w_ + gap
    # leyenda
    sp = f(' ', FS); lw = f(lab[0], FS)+f(lab[1:], SC)+f(' 8.5.', FS)
    lines = []; curw = lw; cur = []; first = True
    for w_ in cap.split(' '):
        ww = f(w_, FS)
        if cur and curw+sp+ww > TW: lines.append((cur, first)); cur = [w_]; curw = ww; first = False
        else: curw += sp+ww; cur.append(w_)
    lines.append((cur, first))
    y = H - (img_top + IMH + 16 + 8)
    for i, (ws, isf) in enumerate(lines):
        last = i == len(lines)-1
        tw = sum(f(w_, FS) for w_ in ws) + (lw if isf else 0); gaps = len(ws)-1+(1 if isf else 0)
        g = (TW-tw)/gaps if (not last and gaps > 0) else sp
        xx = x0 if not last else x0 + (TW-(tw+g*gaps))/2
        if isf:
            c.setFont('Pag', FS); c.drawString(xx, y, lab[0]); xx += f(lab[0], FS)
            c.setFont('Pag', SC); c.drawString(xx, y, lab[1:]); xx += f(lab[1:], SC)
            c.setFont('Pag', FS); c.drawString(xx, y, ' 8.5.'); xx += f(' 8.5.', FS)+g
        for w_ in ws:
            c.setFont('Pag', FS); c.drawString(xx, y, w_); xx += f(w_, FS)+g
        y -= LH
    bottom_ft = H - (y + LH) + 3
    c.showPage(); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0], bottom_ft

w = PdfWriter(clone_from=src)
kids = w._root_object['/Pages']['/Kids']
B = kids[Bi].get_object()
def content(p):
    ct = p['/Contents'].get_object()
    return ct.get_data().decode('latin1') if not isinstance(ct, list) else ''.join(x.get_object().get_data().decode('latin1') for x in ct)
cB = content(B); xoB = B['/Resources']['/XObject']
names = [n for n in re.findall(r'q\s*/(fzFrm\d+) Do\s*Q', cB)]
geo = {}
for n in names:
    o = xoB['/'+n].get_object(); ty = float(o['/Matrix'][5])
    geo[n] = (float(o['/BBox'][3])+ty, float(o['/BBox'][1])+ty, xoB['/'+n].indirect_reference)
layer = [n for n in names if geo[n][0]-geo[n][1] > 800][0]       # capa de numero de pagina (pagina completa)
strips = [n for n in names if n != 'fzFrm0' and n != layer]
hdr = xoB['/fzFrm0'].indirect_reference
ft = lambda n: H - geo[n][0]; fb = lambda n: H - geo[n][1]
print('strips', [(n, round(ft(n)), round(fb(n))) for n in strips][:12])
def blank_with(ov, idx):
    p = w.insert_page(ov, idx)
    r = p['/Resources']
    if '/XObject' not in r: r[NameObject('/XObject')] = DictionaryObject()
    return p
if lang == 'es':
    pulled = strips[:8]; rest = strips[8:]
    assert abs(ft(pulled[0])-78) < 1.5 and abs(ft(rest[0])-472) < 1.5, (ft(pulled[0]), ft(rest[0]))
    ov, bottom = figure_overlay(78.0)
    new_top = bottom + 14
    dy = (H - new_top) - geo[pulled[0]][0]
    print('N: fig bottom', round(bottom), 'pulled last bottom', round(fb(pulled[-1]) + (new_top-78)))
    N = blank_with(ov, Bi)           # despues de A (A=Bi-1)
    xo = N['/Resources']['/XObject']; xo[NameObject('/fzFrm0')] = hdr
    ops = []
    for n in pulled:
        xo[NameObject('/b_'+n)] = geo[n][2]; ops.append('q 1 0 0 1 0 %.4f cm /b_%s Do Q' % (dy, n))
    st = DecodedStreamObject(); st.set_data(("q /fzFrm0 Do Q\n" + "\n".join(ops) + "\n").encode() + N.get_contents().get_data()); N[NameObject('/Contents')] = w._add_object(st)
    dyB = (H-81.0) - geo[rest[0]][0]
    st = DecodedStreamObject(); st.set_data("\n".join(["q /fzFrm0 Do Q", "q 1 0 0 1 0 %.4f cm" % dyB] + ["q /%s Do Q" % n for n in rest] + ["Q", "q /%s Do Q" % layer]).encode('latin1'))
    B[NameObject('/Contents')] = w._add_object(st)
else:
    keep = strips[:8]; rest = strips[8:]
    print('keep last bottom', round(fb(keep[-1])), 'rest first', round(ft(rest[0])))
    img_top = fb(keep[-1]) + 18
    ov, bottom = figure_overlay(img_top)
    print('fig bottom', round(bottom)); assert bottom < 748
    N = blank_with(ov, Bi+1)          # se clona el overlay en el writer; se reutiliza luego como pagina del resto
    ovres = N['/Resources']; ovc = N.get_contents().get_data().decode('latin1')
    rB = B['/Resources']
    for kind in ('/XObject', '/Font', '/ExtGState'):
        if kind in ovres:
            if kind not in rB: rB[NameObject(kind)] = DictionaryObject()
            for k_, v_ in ovres[kind].items():
                assert k_ not in rB[kind], k_
                rB[kind][NameObject(k_)] = v_
    st2 = DecodedStreamObject(); st2.set_data(("\n".join(["q /fzFrm0 Do Q"] + ["q /%s Do Q" % n for n in keep] + ["q /%s Do Q" % layer]) + "\nq\n" + ovc + "\nQ\n").encode('latin1'))
    B[NameObject('/Contents')] = w._add_object(st2)
    N[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'): DictionaryObject()})
    xo = N['/Resources']['/XObject']; xo[NameObject('/fzFrm0')] = hdr
    dyN = (H-81.0) - geo[rest[0]][0]; ops = []
    for n in rest:
        xo[NameObject('/b_'+n)] = geo[n][2]; ops.append('q 1 0 0 1 0 %.4f cm /b_%s Do Q' % (dyN, n))
    st = DecodedStreamObject(); st.set_data(("q /fzFrm0 Do Q\n" + "\n".join(ops) + "\n").encode()); N[NameObject('/Contents')] = w._add_object(st)
w.write(dst); print('ok', dst, len(w.pages))
