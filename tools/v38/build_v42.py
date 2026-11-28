import io, re
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
S='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad/'
pdfmetrics.registerFont(TTFont('Pag',S+'pagella.ttf'))
H=841.89; FS=9.9626; LH=12.0
def wrap(t,wd):
    out=[]; cur=''
    for w in t.split():
        if pdfmetrics.stringWidth((cur+' '+w).strip(),'Pag',FS)<=wd: cur=(cur+' '+w).strip()
        else: out.append(cur); cur=w
    out.append(cur); return out
def build(src,dst,cx,text):
    w=PdfWriter(clone_from=src); p=w.pages[127]
    st=p['/Contents'].get_object(); st=st[0].get_object() if isinstance(st,list) else st
    c=st.get_data().decode('latin1')
    lines=wrap(text,380.0); extra=8.0+LH*len(lines)
    m=re.search(r'1 0 0 1 0 -(234\.\d+) cm',c); D=float(m.group(1))
    c=re.sub(r'1 0 0 1 0 -234\.\d+ cm',lambda k:'1 0 0 1 0 %.3f cm'%-(D+extra),c)
    st.set_data(c.encode('latin1'))
    buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(595.28,H)); cv.setFont('Pag',FS)
    y=260.0+300.0*575/783+14.0
    for ln in lines:
        cv.drawCentredString(cx,H-y,ln); y+=LH
    cv.showPage(); cv.save(); buf.seek(0); p.merge_page(PdfReader(buf).pages[0])
    print(dst,len(w.pages),len(lines),'D',D,'->',D+extra); w.write(dst)
build('Anestesia_y_Obesidad_ES_v41.pdf',S+'ES_v42t.pdf',301.6,"Ventana de ultrasonido en la fosa hepatorrenal, espacio de Morrison. Ideal para visualizar colecciones líquidas o sangre posquirúrgica o por trauma.")
build('Anesthesia_and_Obesity_EN_v41.pdf',S+'EN_v42t.pdf',293.6,"Ultrasound window of the hepatorenal fossa, Morrison’s pouch. Ideal for visualizing fluid collections or blood after surgery or trauma.")
