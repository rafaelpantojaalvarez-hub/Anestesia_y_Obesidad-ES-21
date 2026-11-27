import re, sys
sys.path.insert(0,'/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/502ba37a-38d7-5840-85ea-e54864412c7c/scratchpad')
from dec import cmap, dec
TOK=re.compile(r'\[[^\]]*\]|<[0-9A-Fa-f]*>|\([^)]*\)|/[^\s/\[\]<>()]+|-?[\d.]+|[A-Za-z\*\'"]+')
def explode(c, tag, cms):
    toks=TOK.findall(c); items=[]; operands=[]
    fill='0 g'; stroke='0 G'; first=True; cap=None; depth=0
    lx=ly=lead=0.0; font=None; size=0.0
    for t in toks:
        if re.match(r'^(\[|<|\(|/|-?[\d.])',t):
            operands.append(t); continue
        op=t; o=operands; operands=[]
        if cap is not None:
            cap.append((op,o))
            if op=='q': depth+=1
            elif op=='Q':
                depth-=1
                if depth==0:
                    y=None
                    for op2,o2 in cap:
                        if op2 in('m','re'): y=float(o2[1]); break
                    items.append(dict(kind='gfx',y=y,tag=tag,cap=cap,stroke=stroke,fill=fill)); cap=None
            continue
        if op=='q':
            if first: first=False
            else: cap=[('q',[])]; depth=1
        elif op=='cm' or op=='Q': pass
        elif op=='Tf': font=o[0]; size=float(o[1])
        elif op in('Td','TD'):
            lx+=float(o[0]); ly+=float(o[1])
            if op=='TD': lead=-float(o[1])
        elif op=='T*': ly-=lead
        elif op=='BT': lx=ly=0.0
        elif op in('g','rg'): fill=' '.join(o+[op])
        elif op in('G','RG'): stroke=' '.join(o+[op])
        elif op=='TJ':
            arr=o[0]
            items.append(dict(kind='txt',x=lx,y=ly,font=font,size=size,fill=fill,arr=arr,tag=tag,text=dec(arr+'TJ',cms[font[1:]])))
    return items
def emit(items,dy=0.0,dx=0.0,fmap=None):
    out=[]
    for it in items:
        if it['kind']=='txt':
            f=it['font'][1:]; f=(fmap(it['tag'],f) if fmap else f)
            out.append('%s BT /%s %s Tf %.3f %.3f Td %sTJ ET'%(it['fill'],f,it['size'],it['x']+dx,it['y']+dy,it['arr']))
        else:
            s=[it['stroke'],it['fill']]
            for op,o in it['cap']:
                o=list(o)
                if op in('m','l'): o[1]='%.3f'%(float(o[1])+dy); o[0]='%.3f'%(float(o[0])+dx)
                elif op=='re': o[1]='%.3f'%(float(o[1])+dy); o[0]='%.3f'%(float(o[0])+dx)
                s.append(' '.join(o+[op]))
            out.append(' '.join(s))
    return '\n'.join(out)
