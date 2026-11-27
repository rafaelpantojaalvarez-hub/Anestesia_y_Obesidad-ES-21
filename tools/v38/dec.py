import re
def cmap(f):
    tu=f['/ToUnicode'].get_object().get_data().decode('latin1'); cm={}
    for sec in re.findall(r'beginbfchar(.*?)endbfchar',tu,re.S):
        for a,b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>',sec):
            cm[int(a,16)]=bytes.fromhex(b).decode('utf-16-be')
    for sec in re.findall(r'beginbfrange(.*?)endbfrange',tu,re.S):
        for a,b,c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>',sec):
            a,b,c=int(a,16),int(b,16),int(c,16)
            for i in range(a,b+1): cm[i]=chr(c+i-a)
    return cm
def dec(t,cm):
    out=''
    for m in re.finditer(r'<([0-9A-Fa-f]+)>|(-?[\d\.]+)',t[1:-3]):
        if m.group(1):
            h=m.group(1); out+=''.join(cm.get(int(h[i:i+4],16),'?') for i in range(0,len(h),4))
        elif float(m.group(2))<-150: out+=' '
    return out
