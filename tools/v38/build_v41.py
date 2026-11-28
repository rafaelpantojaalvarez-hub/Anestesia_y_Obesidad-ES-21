import sys, io, re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
from reportlab.pdfgen import canvas
from PIL import Image
S='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad/'
IM='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/images/'
H=841.89
def drawimg(f,cx,wd,top):
    im=Image.open(IM+f); ht=wd*im.height/im.width
    buf=io.BytesIO(); cv=canvas.Canvas(buf,pagesize=(595.28,H)); cv.drawImage(IM+f,cx-wd/2,H-top-ht,wd,ht); cv.showPage(); cv.save(); buf.seek(0)
    return PdfReader(buf).pages[0], ht
def streams(p):
    ct=p['/Contents'].get_object(); return [x.get_object() for x in ct] if isinstance(ct,list) else [ct]
def sform(st):
    m=re.search(r'/fzFrm(\d+) Do',st.get_data().decode('latin1')); return int(m.group(1)) if m else None
def top(p,n):
    o=p['/Resources']['/XObject']['/fzFrm%d'%n].get_object(); return H-(float(o['/BBox'][3])+float(o['/Matrix'][5]))
def build(src,dst,cfg):
    w=PdfWriter(clone_from=src)
    p97=w.pages[127]; p98=w.pages[128]; p99=w.pages[129]
    # --- imagen 1 en 6.10 ---
    pg,h1=drawimg('5.jpg',cfg['cx1'],300.0,260.0); D=h1+14.0
    st=streams(p97)[0]; c=st.get_data().decode('latin1')
    n=0
    for k in range(20,40):
        c,m=re.subn(r'q /fzFrm%d Do Q'%k,'q 1 0 0 1 0 %.3f cm /fzFrm%d Do Q'%(-D,k),c); n+=m
    print('shifted strips',n)
    st.set_data(c.encode('latin1')); p97.merge_page(pg)
    # --- imagen 2 en 6.14 ---
    hd=cfg['head']; lines=cfg['lines']; pulled=cfg['pulled']; nh=cfg['nexthead']
    xo98=p98['/Resources']['/XObject']; xo99=p99['/Resources']['/XObject']
    t_h=top(p98,hd); t_l=[top(p98,k) for k in lines]; t_p=[top(p99,k) for k in pulled]
    wd=240.0; imtop=81.0+17.0+10.0
    pg2,h2=drawimg('6.jpg',293.6,wd,imtop)
    ops=['q /h0 Do Q','q 1 1 1 rg 60 778 56 20 re f Q']
    res={'/h0':cfg['hdr'](w)}
    def place(name,ref,oldtop,newtop,dx=0.0):
        res['/'+name]=ref; ops.append('q 1 0 0 1 %.3f %.3f cm /%s Do Q'%(dx,oldtop-newtop,name))
    place('a%d'%hd,xo98.raw_get('/fzFrm%d'%hd),t_h,81.0,dx=cfg['dxa'])
    t0=imtop+h2+14.0
    for k,t in zip(lines,t_l): place('a%d'%k,xo98.raw_get('/fzFrm%d'%k),t,t0+(t-t_l[0]),dx=cfg['dxa'])
    last=t0+(t_l[-1]-t_l[0])
    for i,(k,t) in enumerate(zip(pulled,t_p)): place('b%d'%k,xo99.raw_get('/fzFrm%d'%k),t,last+14.2*(i+1),dx=cfg['dxp'])
    # quitar de pagina 98 y subir la 99
    for s_ in streams(p98):
        if sform(s_) in [hd]+lines: s_.set_data(b' ')
    up=top(p99,nh)-81.0
    for s_ in streams(p99):
        f=sform(s_)
        if f in pulled: s_.set_data(b' ')
        elif f is not None and f!=0 and f not in pulled: s_.set_data(('q 1 0 0 1 0 %.3f cm /fzFrm%d Do Q'%(up,f)).encode('latin1'))
    w.insert_blank_page(width=595.28,height=H,index=129); B=w.pages[129]
    B[NameObject('/Resources')]=DictionaryObject({NameObject('/XObject'):DictionaryObject({NameObject(k):v for k,v in res.items()})})
    sb=DecodedStreamObject(); sb.set_data('\n'.join(ops).encode('latin1')); B[NameObject('/Contents')]=w._add_object(sb)
    B.merge_page(pg2)
    print(dst,len(w.pages),'D',round(D,1),'h2',round(h2,1),'up',round(up,1))
    w.write(dst)
# ES
build('Anestesia_y_Obesidad_ES_v40.pdf',S+'ES_v41t.pdf',dict(cx1=301.6,head=10,lines=[11,12,13,14,15],pulled=[1,2],nexthead=3,dxp=-8.0,dxa=0.0,hdr=lambda w:w.pages[128]['/Resources']['/XObject'].raw_get('/fzFrm0')))
# EN
build('Anesthesia_and_Obesity_EN_v40.pdf',S+'EN_v41t.pdf',dict(cx1=293.6,head=11,lines=[12,13,14,15],pulled=[1,2,3],nexthead=4,dxp=0.0,dxa=-8.0,hdr=lambda w:w.pages[129]['/Resources']['/XObject'].raw_get('/fzFrm0')))
