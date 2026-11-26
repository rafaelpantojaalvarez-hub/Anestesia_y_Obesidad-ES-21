import sys, re, json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
lang, src, new, dst = sys.argv[1:5]; H = 841.89; Ai = 69
J = json.load(open(new.replace('.pdf', '.json'))); nP = J['pages']
w = PdfWriter(clone_from=src); kids = w._root_object['/Pages']['/Kids']
def info(p):
    ct = p['/Contents'].get_object()
    c = ct.get_data().decode('latin1') if not isinstance(ct, list) else ''.join(x.get_object().get_data().decode('latin1') for x in ct)
    xo = p['/Resources']['/XObject']; names = re.findall(r'q\s*/(fzFrm\d+) Do\s*Q', c)
    geo = {}
    for n in names:
        o = xo['/'+n].get_object(); geo[n] = (float(o['/BBox'][3])+float(o['/Matrix'][5]), float(o['/BBox'][1])+float(o['/Matrix'][5]), xo['/'+n].indirect_reference)
    return names, geo
A = kids[Ai].get_object(); namesA, geoA = info(A)
nums = lambda lst: [n for n in lst if n != 'fzFrm0']
if lang == 'es':
    keep = [n for n in nums(namesA) if int(n[5:]) <= 56]; restA = [n for n in nums(namesA) if int(n[5:]) > 56 and geoA[n][0]-geoA[n][1] < 100]
    restA = [n for n in nums(namesA) if int(n[5:]) in (57, 58, 59)]
else:
    keep = [n for n in nums(namesA) if int(n[5:]) <= 57]; restA = [n for n in nums(namesA) if int(n[5:]) in (58, 59, 60, 61, 62)]
print('keep', len(keep), 'rest', [(n, round(H-geoA[n][0])) for n in restA])
if lang == 'en':
    B = kids[Ai+1].get_object(); namesB, geoB = info(B)
    layer = [n for n in namesB if geoB[n][0]-geoB[n][1] > 800][0]
    tab = 'fzFrm1'; bul = [n for n in nums(namesB) if n not in (tab, layer)]
    print('table strip', round(H-geoB[tab][0]), round(H-geoB[tab][1]), 'bul first', round(H-geoB[bul[0]][0]), 'layer', layer)
    dyB = (H-81.0) - geoB[bul[0]][0]
    st = DecodedStreamObject(); st.set_data("\n".join(["q /fzFrm0 Do Q", "q 1 0 0 1 0 %.4f cm" % dyB] + ["q /%s Do Q" % n for n in bul] + ["Q", "q 80 781.89 400 16 re h 1 1 1 rg f Q", "q /%s Do Q" % layer]).encode()); B[NameObject('/Contents')] = w._add_object(st)
st = DecodedStreamObject(); st.set_data("\n".join(["q /fzFrm0 Do Q"] + ["q /%s Do Q" % n for n in keep]).encode()); A[NameObject('/Contents')] = w._add_object(st)
nr = PdfReader(new)
for i in range(nP): w.insert_page(nr.pages[i], Ai+1+i)
def add(page, strips, geo, top_new):
    r = page['/Resources']
    if '/XObject' not in r: r[NameObject('/XObject')] = DictionaryObject()
    dy = (H-top_new) - geo[strips[0]][0]; ops = []
    for n in strips:
        r['/XObject'][NameObject('/b_'+n)] = geo[n][2]; ops.append('q 1 0 0 1 0 %.4f cm /b_%s Do Q' % (dy, n))
    oc = page.get_contents().get_data(); st = DecodedStreamObject(); st.set_data(oc + ("\n" + "\n".join(ops) + "\n").encode()); page[NameObject('/Contents')] = w._add_object(st)
add(w.pages[Ai+J['R2'][0]], restA, geoA, J['R2'][1])
if lang == 'en': add(w.pages[Ai+J['R1'][0]], [tab], geoB, J['R1'][1])
w.write(dst); print('ok', len(w.pages))
