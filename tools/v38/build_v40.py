import sys, io
sys.path.insert(0,'/home/user/Anestesia_y_Obesidad-ES-21/tools/v38')
from ex import *
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from PIL import Image
S='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad/'
IMG='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/images/4.jpg'
H=841.89
def build(src,dst,idx,rule,mask):
    w=PdfWriter(clone_from=src); p=w.pages[idx]; nxt=w.pages[idx+1]
    ct=p['/Contents'].get_object(); st=ct[0].get_object() if isinstance(ct,list) else ct
    fonts=p['/Resources']['/Font']; cms={k[1:]:cmap(fonts[k].get_object()) for k in fonts}
    its=[i for i in explode(st.get_data().decode('latin1'),'x',cms) if not(i['kind']=='gfx' and i['y'] is None)]
    keep=[i for i in its if i['y']>rule-20]; rest=[i for i in its if i['y']<rule-20]
    st.set_data(('q 1 0 0 1 72 769.89 cm\n'+emit(keep)+'\nQ\n').encode('latin1'))
    wd=400.0; im=Image.open(IMG); ht=wd*im.height/im.width; top=rule-16.0
    buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(595.28,H)); cv.drawImage(IMG,301.7-wd/2,769.89+top-ht,wd,ht); cv.showPage(); cv.save(); buf.seek(0)
    p.merge_page(PdfReader(buf).pages[0])
    body='q /fzFrm0 Do Q\nq 1 1 1 rg %s re f Q\n'%mask+'q 1 0 0 1 72 769.89 cm\n'+emit(rest,dy=-30.0-rest[0]['y'],dx=-8.0)+'\nQ\n'
    w.insert_blank_page(width=595.28,height=H,index=idx+1); pg=w.pages[idx+1]
    pg[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):p['/Resources']['/Font'],NameObject('/XObject'):DictionaryObject({NameObject('/fzFrm0'):nxt['/Resources']['/XObject'].raw_get('/fzFrm0')})})
    s2=DecodedStreamObject(); s2.set_data(body.encode('latin1')); pg[NameObject('/Contents')]=w._add_object(s2)
    print(dst,len(w.pages),'rest',len(rest),'last',min(i['y'] for i in rest)-rest[0]['y']); w.write(dst)
build('Anestesia_y_Obesidad_ES_v39.pdf',S+'ES_v40t.pdf',168,-372.6,'76.198 783.33926 15.87108 10.42972')
build('Anesthesia_and_Obesity_EN_v39.pdf',S+'EN_v40t.pdf',167,-398.7,'76.198 783.33926 16.20972 10.42972')
