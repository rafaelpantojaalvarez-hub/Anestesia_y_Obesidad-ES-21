import sys, re, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
lang, src, dst, Ai = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
IMG = '/root/.claude/uploads/75bc264e-db1f-5a2e-97e2-8d240df88e1f/e8f1fb5a-image.png'
H = 841.89; cx = 293.6 if lang == 'es' else 301.6
w = PdfWriter(clone_from=src)
kids = w._root_object['/Pages']['/Kids']
A = kids[Ai].get_object()
ct = A['/Contents'].get_object()
c = ct.get_data().decode('latin1') if not isinstance(ct, list) else ''.join(x.get_object().get_data().decode('latin1') for x in ct)
shift = float(re.search(r'1 0 0 1 0 ([\-\d\.]+) cm', c).group(1))
names = re.findall(r'q\s*/(fzFrm\d+) Do\s*Q', c); xo = A['/Resources']['/XObject']
geo = {}
for n in names:
    o = xo['/'+n].get_object(); ty = float(o['/Matrix'][5]); geo[n] = (float(o['/BBox'][3])+ty, xo['/'+n].indirect_reference)
strips = [n for n in names if n != 'fzFrm0']
ft = lambda n: H - (geo[n][0] + shift)
split = next(i for i, n in enumerate(strips) if abs(ft(n)-285) < 2)
keep, rest = strips[:split], strips[split:]
print('keep', len(keep), 'rest', len(rest), [round(ft(n)) for n in rest[:2]])
W = 435.0; h = W*1333/2000
buf = io.BytesIO(); cv = canvas.Canvas(buf, pagesize=(595.28, H)); cv.drawImage(IMG, cx-W/2, H-77-h, W, h); cv.showPage(); cv.save(); buf.seek(0)
ov = PdfReader(buf).pages[0]
N = w.insert_page(ov, Ai+1)
hdr = xo['/fzFrm0'].indirect_reference
r = N['/Resources']
if '/XObject' not in r: r[NameObject('/XObject')] = DictionaryObject()
nx = r['/XObject']; nx[NameObject('/fzFrm0')] = hdr
newtop = 77 + h + 14
dy = (H - newtop) - (geo[rest[0]][0] + shift)
ops = []
for n in rest:
    nx[NameObject('/b_'+n)] = geo[n][1]; ops.append('q 1 0 0 1 0 %.4f cm /b_%s Do Q' % (dy + shift, n))
mask = "1 1 1 rg 60 778 56 20 re f 0 g" if lang == 'es' else "1 1 1 rg 480 778 50 20 re f 0 g"
st = DecodedStreamObject(); st.set_data(("q /fzFrm0 Do Q %s\n" % mask + "\n".join(ops) + "\n").encode() + N.get_contents().get_data())
N[NameObject('/Contents')] = w._add_object(st)
# A: conservar solo hasta 6.5.2
body = "\n".join(["q /fzFrm0 Do Q", "q 1 0 0 1 0 %.5f cm" % shift] + ["q /%s Do Q" % n for n in keep] + ["Q"])
st = DecodedStreamObject(); st.set_data(body.encode()); A[NameObject('/Contents')] = w._add_object(st)
print('last bottom', round(newtop + (ft(rest[-1]) - ft(rest[0])) + 14))
w.write(dst)
