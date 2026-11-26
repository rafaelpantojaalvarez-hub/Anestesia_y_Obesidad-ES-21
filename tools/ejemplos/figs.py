import sys, io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
lang, src, dst, S = sys.argv[1:5]
pdfmetrics.registerFont(TTFont('Pag', S+'/fonts/pagella-regular.ttf'))
if lang=='es':
    jobs=[ # (physical page of the old figure page, image, imgW,imgH px, width pt, label, caption, number side)
     (120,'fig610.jpg',2000,1500,400,'FIGURA',"Ecografía de la vena cava inferior en modo M. Arriba, imagen en modo B con la línea de exploración; abajo, trazado en modo M con tres mediciones del diámetro (1: 2,42 cm; 2: 1,85 cm; 3: 2,48 cm).",'L'),
     (118,'fig68.jpg',1376,768,470,'FIGURA',"Ecografía pulmonar en el paciente con obesidad. Izquierda: pulmón normal con línea pleural y líneas A. Centro: consolidación subpleural con broncogramas aéreos y líneas B. Derecha: atelectasia con derrame pleural. Abajo: zonas de exploración, hallazgos clave y evaluación rápida. Los broncogramas dinámicos sugieren neumonía.",'L')]
    cx=293.6; num='6.'
else:
    jobs=[
     (119,'fig610.jpg',2000,1500,400,'FIGURE',"Inferior vena cava ultrasound in M-mode. Top, B-mode image with the scanning line; bottom, M-mode tracing with three diameter measurements (1: 2.42 cm; 2: 1.85 cm; 3: 2.48 cm).",'R'),
     (117,'fig68.jpg',1376,768,470,'FIGURE',"Lung ultrasound in the patient with obesity. Left: normal lung with pleural line and A lines. Center: subpleural consolidation with air bronchograms and B lines. Right: atelectasis with pleural effusion. Bottom: where to scan, key findings, and rapid assessment. Dynamic air bronchograms suggest pneumonia.",'R')]
    cx=301.6
fignum={'fig610.jpg':'6.10.','fig68.jpg':'6.8.'}
FS=9.0; SC=7.2; LH=11.2; TW=435
def overlay(img,iw,ih,W,label,body):
    H=W*ih/iw; buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(595.28,841.89))
    top=842-77; c.drawImage(S+'/'+img, cx-W/2, top-H, W, H)
    lab=(label,fignum[img]); sp=pdfmetrics.stringWidth(' ','Pag',FS)
    lw=pdfmetrics.stringWidth(label[0],'Pag',FS)+pdfmetrics.stringWidth(label[1:],'Pag',SC)+pdfmetrics.stringWidth(' '+lab[1],'Pag',FS)
    lines=[];cur=[];curw=lw;first=True
    for w in body.split(' '):
        ww=pdfmetrics.stringWidth(w,'Pag',FS)
        if cur and curw+sp+ww>TW: lines.append((cur,first)); cur=[w]; curw=ww; first=False
        else: curw+=sp+ww; cur.append(w)
    lines.append((cur,first)); y=top-H-18
    for i,(ws,isf) in enumerate(lines):
        last=i==len(lines)-1
        tw=sum(pdfmetrics.stringWidth(w,'Pag',FS) for w in ws)+(lw if isf else 0)
        gaps=len(ws)-1+(1 if isf else 0)
        gap=(TW-tw)/gaps if (not last and gaps>0) else sp
        x=cx-TW/2 if not last else cx-(tw+gap*gaps)/2
        if isf:
            c.setFont('Pag',FS); c.drawString(x,y,label[0]); x+=pdfmetrics.stringWidth(label[0],'Pag',FS)
            c.setFont('Pag',SC); c.drawString(x,y,label[1:]); x+=pdfmetrics.stringWidth(label[1:],'Pag',SC)
            c.setFont('Pag',FS); c.drawString(x,y,' '+lab[1]); x+=pdfmetrics.stringWidth(' '+lab[1],'Pag',FS)+gap
        for w in ws:
            c.setFont('Pag',FS); c.drawString(x,y,w); x+=pdfmetrics.stringWidth(w,'Pag',FS)+gap
        y-=LH
    c.showPage(); c.save(); buf.seek(0); return PdfReader(buf)
w=PdfWriter(src, incremental=True)
for pn,img,iw,ih,W,label,body,side in jobs:   # descending order
    idx=pn-1
    pg=w.pages[idx]; hdr=pg['/Resources']['/XObject']['/fzFrm0'].indirect_reference
    ov=overlay(img,iw,ih,W,label,body)
    newp=w.insert_page(ov.pages[0], idx)
    r=newp['/Resources']
    if '/XObject' not in r: r[NameObject('/XObject')]=DictionaryObject()
    r['/XObject'][NameObject('/fzFrm0')]=hdr
    mask="60 783 60 18 re f" if side=='L' else "490 783 50 18 re f"
    st=DecodedStreamObject(); st.set_data(("q /fzFrm0 Do Q 1 1 1 rg %s 0 g\n"%mask).encode()+newp.get_contents().get_data())
    newp[NameObject('/Contents')]=w._add_object(st)
    old=w.pages[idx+1]; assert old['/Resources']['/XObject']['/fzFrm0'].indirect_reference==hdr
    xo=old['/Resources']['/XObject']
    mx=-1e9
    for k,v in xo.items():
        if k in ('/fzFrm0','/fzFrm1'): continue
        o=v.get_object(); mx=max(mx,float(o['/BBox'][3])+float(o['/Matrix'][5]))
    shift=761.346-mx
    lines=[l for l in old.get_contents().get_data().decode('latin1').split('\n') if l.strip()]
    assert 'fzFrm0' in lines[0] and 'fzFrm1 ' in lines[1], lines[:2]
    st2=DecodedStreamObject(); st2.set_data(("\n".join([lines[0],"q 1 0 0 1 0 %.5f cm"%shift]+lines[2:]+["Q"])).encode('latin1'))
    old[NameObject('/Contents')]=w._add_object(st2)
    print(pn,img,'shift',round(shift,2))
w.write(dst); print('pages',len(w.pages))
