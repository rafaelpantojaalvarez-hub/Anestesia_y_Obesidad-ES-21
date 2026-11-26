import sys, io, re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject, ArrayObject, FloatObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
lang, src, dst, figpage, S = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
pdfmetrics.registerFont(TTFont('Pag', S+'/fonts/pagella-regular.ttf'))
cx = 293.6 if lang=='es' else 301.6
W=470; IMGW=W; IMGH=IMGW*768/1376
if lang=='es':
    label=('FIGURA','6.8.'); body="Ecografía pulmonar en el paciente con obesidad. Izquierda: pulmón normal con línea pleural y líneas A. Centro: consolidación subpleural con broncogramas aéreos y líneas B. Derecha: atelectasia con derrame pleural. Abajo: zonas de exploración, hallazgos clave y evaluación rápida. Los broncogramas dinámicos sugieren neumonía."
else:
    label=('FIGURE','6.8.'); body="Lung ultrasound in the patient with obesity. Left: normal lung with pleural line and A lines. Center: subpleural consolidation with air bronchograms and B lines. Right: atelectasis with pleural effusion. Bottom: where to scan, key findings, and rapid assessment. Dynamic air bronchograms suggest pneumonia."
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(595.28,841.89))
top=842-77; c.drawImage(S+'/fig68.jpg', cx-W/2, top-IMGH, W, IMGH)
FS=9.0; SC=7.2; LH=11.2; TW=435
# small caps label
lab_w = pdfmetrics.stringWidth(label[0][0],'Pag',FS)+pdfmetrics.stringWidth(label[0][1:],'Pag',SC)+pdfmetrics.stringWidth(' '+label[1],'Pag',FS)
words=body.split(' ')
sp=pdfmetrics.stringWidth(' ','Pag',FS)
lines=[]; cur=[]; curw=lab_w; first=True
for w in words:
    ww=pdfmetrics.stringWidth(w,'Pag',FS)
    if cur and curw+sp+ww>TW:
        lines.append((cur,first)); cur=[w]; curw=ww; first=False
    else:
        curw+= sp+ww; cur.append(w)
lines.append((cur,first))
y=top-IMGH-18
for i,(ws,isfirst) in enumerate(lines):
    last = i==len(lines)-1
    tw=sum(pdfmetrics.stringWidth(w,'Pag',FS) for w in ws)+(lab_w if isfirst else 0)
    gaps=len(ws)-1+(1 if isfirst else 0)
    gap = (TW-tw)/gaps if (not last and gaps>0) else sp
    total = tw+gap*gaps
    x = cx-TW/2 if not last else cx-total/2
    if isfirst:
        c.setFont('Pag',FS); c.drawString(x,y,label[0][0]); x+=pdfmetrics.stringWidth(label[0][0],'Pag',FS)
        c.setFont('Pag',SC); c.drawString(x,y,label[0][1:]); x+=pdfmetrics.stringWidth(label[0][1:],'Pag',SC)
        c.setFont('Pag',FS); c.drawString(x+sp*0,y,' '+label[1]); x+=pdfmetrics.stringWidth(' '+label[1],'Pag',FS)+gap
    for w in ws:
        c.setFont('Pag',FS); c.drawString(x,y,w); x+=pdfmetrics.stringWidth(w,'Pag',FS)+gap
    y-=LH
c.showPage(); c.save(); buf.seek(0)
ov=PdfReader(buf)
w=PdfWriter(src, incremental=True)
pg=w.pages[figpage-1]
res=pg['/Resources']['/XObject']
hdr=res['/fzFrm0'].indirect_reference
# new page
newp=w.insert_page(ov.pages[0], figpage-1)
r=newp['/Resources']
if '/XObject' not in r: r[NameObject('/XObject')]=DictionaryObject()
r['/XObject'][NameObject('/fzFrm0')]=hdr
old=newp.get_contents().get_data()
st=DecodedStreamObject(); st.set_data(b"q /fzFrm0 Do Q 1 1 1 rg 60 783 60 18 re f 0 g\n"+old)
newp[NameObject('/Contents')]=w._add_object(st)
# old fig page (now index figpage): drop fig strip, shift text up
pg=w.pages[figpage]
assert pg['/Resources']['/XObject']['/fzFrm0'].indirect_reference==hdr
cont=pg.get_contents().get_data().decode('latin1').split('\n')
lines=[l for l in cont if l.strip()]
assert 'fzFrm0' in lines[0] and 'fzFrm1 ' in lines[1], lines[:3]
new="\n".join([lines[0],"q 1 0 0 1 0 163.90161 cm"]+lines[2:]+["Q"])
st2=DecodedStreamObject(); st2.set_data(new.encode('latin1'))
pg[NameObject('/Contents')]=w._add_object(st2)
w.write(dst)
print('ok',len(w.pages))
