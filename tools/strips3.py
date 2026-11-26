import sys,re
from pypdf import PdfReader
r=PdfReader(sys.argv[1]); kids=r.trailer['/Root']['/Pages']['/Kids']
for ki in map(int,sys.argv[2:]):
    p=kids[ki].get_object(); ct=p['/Contents'].get_object()
    c=ct.get_data().decode('latin1') if not isinstance(ct,list) else ''.join(x.get_object().get_data().decode('latin1') for x in ct)
    mm=re.search(r'1 0 0 1 0 ([\-\d\.]+) cm',c); shift=float(mm.group(1)) if mm else 0.0
    print('KID',ki,kids[ki].idnum,'shift',shift)
    xo=p['/Resources']['/XObject']
    for name in re.findall(r'/(fzFrm\d+) Do',c):
        o=xo['/'+name].get_object(); b=o['/BBox']; mt=o['/Matrix']
        sh=0 if name=='fzFrm0' else shift
        top=float(b[3])+float(mt[5])+sh; bot=float(b[1])+float(mt[5])+sh
        print(name[5:],'%.0f-%.0f'%(842-top,842-bot),end='; ')
    print()
