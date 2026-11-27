import sys, io
sys.path.insert(0,'/home/user/Anestesia_y_Obesidad-ES-21/tools/v38')
from ex import *
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from PIL import Image
S='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad/'
IMG='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/images/3.jpg'
H=841.89; ORG=769.89
def build(src,dst,idx,cx,split):
    w=PdfWriter(clone_from=src); p=w.pages[idx]
    ct=p['/Contents'].get_object(); st=ct[0].get_object() if isinstance(ct,list) else ct
    fonts=p['/Resources']['/Font']; cms={k[1:]:cmap(fonts[k].get_object()) for k in fonts}
    its=[i for i in explode(st.get_data().decode('latin1'),'x',cms) if not(i['kind']=='gfx' and i['y'] is None)]
    head=[i for i in its if i['kind']=='txt' and i['y']>0]
    wd=434.0; im=Image.open(IMG); ht=wd*im.height/im.width; top=-10.0
    if split is None: keep=None; move=[]
    else:
        keep=[i for i in its if i['y']>split]; move=[i for i in its if i['y']<=split]
        st.set_data(('q 1 0 0 1 72 769.89 cm\n'+emit(keep)+'\nQ\n').encode('latin1'))
    body=emit(head)
    if move: body+='\n'+emit(move,dy=(top-ht-30.0)-move[0]['y'])
    fontref=p['/Resources']['/Font']
    w.insert_blank_page(width=595.28,height=H,index=idx+1); pg=w.pages[idx+1]
    pg[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):fontref})
    s2=DecodedStreamObject(); s2.set_data(('q 1 0 0 1 72 769.89 cm\n'+body+'\nQ\n').encode('latin1'))
    pg[NameObject('/Contents')]=w._add_object(s2)
    buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(595.28,H)); cv.drawImage(IMG,cx-wd/2,ORG+top-ht,wd,ht); cv.showPage(); cv.save(); buf.seek(0)
    pg.merge_page(PdfReader(buf).pages[0])
    print(dst,len(w.pages)); w.write(dst)
build('Anestesia_y_Obesidad_ES_v38.pdf',S+'ES_v39t.pdf',239,292.0,None)
build('Anesthesia_and_Obesity_EN_v38.pdf',S+'EN_v39t.pdf',239,302.0,-380.0)
