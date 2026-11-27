import sys, io
sys.path.insert(0,'/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad')
from ex import *
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from PIL import Image
S='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad/'
IM='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/images/'
H=841.89; ORG=769.89
def build(lang, src, dst, A, N, P2, split2):
    # A: idx pagina inicio cap. 14 ; N: idx pagina siguiente ; P2: idx pagina con 14.4.1 ; split2: y bajo el cual se mueve contenido a la pagina nueva
    w=PdfWriter(clone_from=src)
    def main(p):
        ct=p['/Contents'].get_object(); return ct[0].get_object() if isinstance(ct,list) else ct
    def ex(p):
        fonts=p['/Resources']['/Font']; cms={k[1:]:cmap(fonts[k].get_object()) for k in fonts}
        its=[i for i in explode(main(p).get_data().decode('latin1'),'x',cms) if not(i['kind']=='gfx' and i['y'] is None)]
        return its
    def setc(p,items): main(p).set_data(('q 1 0 0 1 72 769.89 cm\n'+emit(items)+'\nQ\n').encode('latin1'))
    def newpage(after_idx, ref, body, img=None):
        pg=w.insert_blank_page(width=595.28,height=H,index=after_idx+1); pg=w.pages[after_idx+1]
        pg[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):ref['/Resources']['/Font']})
        st=DecodedStreamObject(); st.set_data(('q 1 0 0 1 72 769.89 cm\n'+body+'\nQ\n').encode('latin1'))
        pg[NameObject('/Contents')]=w._add_object(st)
        if img:
            f,cx,wd,top=img; im=Image.open(IM+f); ht=wd*im.height/im.width
            buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(595.28,H)); cv.drawImage(IM+f,cx-wd/2,top-ht,wd,ht); cv.showPage(); cv.save(); buf.seek(0)
            pg.merge_page(PdfReader(buf).pages[0])
        return pg
    # ---- tarea 2: imagen 2 tras 14.4.1 ----
    p2=w.pages[P2]; it=ex(p2); head=[i for i in it if i['kind']=='txt' and i['y']>0]
    keep=[i for i in it if i not in [m for m in it if (m['y'] is not None and m['y']<=split2)]]
    move=[i for i in it if i['y'] is not None and i['y']<=split2]
    h2=360*Image.open(IM+'2.jpg').height/Image.open(IM+'2.jpg').width
    top2=-10.0; dy=(top2-h2-26.0)-move[0]['y']
    ref=p2
    setc(p2,keep)
    newpage(P2,ref,emit(head)+'\n'+emit(move,dy=dy),img=('2.jpg',293.6,360,ORG+top2))
    # ---- tarea 1: imagen 1 tras objetivos ----
    pa=w.pages[A]; ita=ex(pa); pn=w.pages[N]; itn=ex(pn)
    headn=[i for i in itn if i['kind']=='txt' and i['y']>0]
    keepA=[i for i in ita if i['y']>-460]; rest=[i for i in ita if i['y']<-470]
    pull=[i for i in itn if i['kind']=='txt' and -60<i['y']<0 and i['y']>PULL_MIN[lang]]
    pullset=pull
    # lineas a subir: las del parrafo que continua (hasta la ultima antes del titulo 14.2)
    nxt=[i for i in itn if i['kind']=='txt' and i['y']<0]
    first_head=[i for i in nxt if i['size']>14][0]['y']
    pull=[i for i in nxt if i['y']>first_head]
    restN=[i for i in itn if i not in pull and i['y']<=first_head]
    resty=sorted(set(round(i['y'],2) for i in rest if i['kind']=='txt'))
    HEAD_Y=-30.0
    dy1=HEAD_Y-rest[0]['y']; last=min(i['y'] for i in rest if i['kind']=='txt')+dy1
    dy2=(last-14.2)-pull[0]['y']
    body=emit(headn)+'\n'+emit(rest,dy=dy1,dx=-8.02)+'\n'+emit(pull,dy=dy2)
    newpage(A,pn,body)
    # imagen 1 en pagina A
    setc(pa,keepA)
    wd=280; im=Image.open(IM+'1.jpg'); ht=wd*im.height/im.width; top=-468.0
    buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(595.28,H)); cv.drawImage(IM+'1.jpg',301.6-wd/2,ORG+top-ht,wd,ht); cv.showPage(); cv.save(); buf.seek(0)
    pa.merge_page(PdfReader(buf).pages[0])
    # pagina siguiente (original): quitar lineas subidas y subir el resto
    shift=restN[0]['y']-HEAD_Y   # titulo 14.2 a HEAD_Y
    setc(pn,[ {**i} for i in restN] if False else restN)
    main(pn).set_data(('q 1 0 0 1 72 769.89 cm\n'+emit(headn)+'\n'+emit(restN,dy=HEAD_Y-restN[0]['y'])+'\nQ\n').encode('latin1'))
    print(lang,'ok pages',len(w.pages),'pull',len(pull),'shift',HEAD_Y-restN[0]['y'])
    w.write(dst)
PULL_MIN={'es':-60,'en':-60}
build('es',sys.argv[1],S+'ES_v38t.pdf',206,207,211,-640.0)
build('en',sys.argv[2],S+'EN_v38t.pdf',205,206,210,-390.0)
