import sys, re, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from PIL import Image
lang, src, dst, Ai, nkeep_last = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
V = '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/v31/'
H = 841.89; cx = 293.6 if lang == 'es' else 301.6
w = PdfWriter(clone_from=src)
kids = w._root_object['/Pages']['/Kids']; A = kids[Ai].get_object()
ct = A['/Contents'].get_object()
c = ct.get_data().decode('latin1') if not isinstance(ct, list) else ''.join(x.get_object().get_data().decode('latin1') for x in ct)
shift = float(re.search(r'1 0 0 1 0 ([\-\d\.]+) cm', c).group(1))
names = [n for n in re.findall(r'q\s*/(fzFrm\d+) Do\s*Q', c) if n != 'fzFrm0']
xo = A['/Resources']['/XObject']; geo = {}
for n in names:
    o = xo['/'+n].get_object(); ty = float(o['/Matrix'][5]); geo[n] = (float(o['/BBox'][3])+ty, float(o['/BBox'][1])+ty)
ft = lambda n: H-(geo[n][0]+shift); fb = lambda n: H-(geo[n][1]+shift)
keep = [n for n in names if int(n[5:]) <= nkeep_last]; rest = [n for n in names if int(n[5:]) > nkeep_last]
print('keep bottom', round(fb(keep[-1])), 'rest top', round(ft(rest[0])), 'n', len(rest))
def asp(f): im = Image.open(V+f); return im.width/im.height
# fila 1 (imagenes 1 y 2)
h1 = 215.0; w1, w2 = asp('i1.jpg')*h1, asp('i2.jpg')*h1; g = 14.0
top1 = fb(keep[-1]) + 12; x1 = cx - (w1+w2+g)/2
rest_h = fb(rest[-1]) - ft(rest[0]); REST_TOP = 80.0
bufA = io.BytesIO(); cv = canvas.Canvas(bufA, pagesize=(595.28, H))
cv.drawImage(V+'i1.jpg', x1, H-top1-h1, w1, h1); cv.drawImage(V+'i2.jpg', x1+w1+g, H-top1-h1, w2, h1); cv.showPage(); cv.save(); bufA.seek(0)
body = ["q /fzFrm0 Do Q", "q 1 0 0 1 0 %.5f cm" % shift] + ["q /%s Do Q" % n for n in keep] + ["Q"]
st = DecodedStreamObject(); st.set_data("\n".join(body).encode('latin1')); A[NameObject('/Contents')] = w._add_object(st)
del xo['/ImgNew1']
A.merge_page(PdfReader(bufA).pages[0])
# pagina nueva: cuadricula 2x2
hh = 200.0; Wt = 435.0
rows = [('phL.jpg', 'i3.jpg'), ('phR.jpg', 'i4.jpg')]
bufN = io.BytesIO(); cv = canvas.Canvas(bufN, pagesize=(595.28, H)); y = REST_TOP + rest_h + 16
for a_, b_ in rows:
    wa, wb = asp(a_)*hh, asp(b_)*hh; gg = 8.0; sc = min(1.0, (Wt-gg)/(wa+wb)); ha = hh*sc
    wa *= sc; wb *= sc; x = cx - (wa+wb+gg)/2
    cv.drawImage(V+a_, x, H-y-ha, wa, ha); cv.drawImage(V+b_, x+wa+gg, H-y-ha, wb, ha); y += ha + 10
cv.showPage(); cv.save(); bufN.seek(0)
N = w.insert_page(PdfReader(bufN).pages[0], Ai+1)
r = N['/Resources']
if '/XObject' not in r: r[NameObject('/XObject')] = DictionaryObject()
r['/XObject'][NameObject('/fzFrm0')] = xo['/fzFrm0'].indirect_reference
mask = "1 1 1 rg 60 778 56 20 re f 0 g" if lang == 'es' else "1 1 1 rg 480 778 50 20 re f 0 g"
ops = []
for n in rest:
    r['/XObject'][NameObject('/b_'+n)] = xo['/'+n].indirect_reference
    ops.append('q 1 0 0 1 0 %.4f cm /b_%s Do Q' % ((H-REST_TOP) - geo[rest[0]][0], n))
st = DecodedStreamObject(); st.set_data(("q /fzFrm0 Do Q %s\n" % mask + "\n".join(ops) + "\n").encode() + N.get_contents().get_data()); N[NameObject('/Contents')] = w._add_object(st)
w.write(dst); print('ok', len(w.pages))
