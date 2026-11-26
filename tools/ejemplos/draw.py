import sys, math
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
F='/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/fonts/'
for n,f in (('Pag','regular'),('PagB','bold'),('PagI','italic')): pdfmetrics.registerFont(TTFont(n,F+'pagella-%s.ttf'%f))
pdfmetrics.registerFontFamily('Pag',normal='Pag',bold='PagB',italic='PagI',boldItalic='PagB')
lang,out=sys.argv[1:3]; W,H=1800,840
T={'es':dict(note_t="Matiz 2024",note="La revisión chilena sigue la pauta ASA 2023 (suspender 1 semana la dosis semanal). La guía multisociedad de 2024 permite continuar el fármaco en la mayoría, con dieta líquida 24 h en alto riesgo y ecografía gástrica si hay duda.",
 top="Paciente con agonista GLP-1 o GLP-1/GIP",q1="¿Síntomas digestivos?<br/>náuseas, vómitos, distensión",r1="Considerar diferir el procedimiento",yes="Sí",no="No",
 q2="¿Se suspendió según la pauta aplicable?",r2="Proceder con el manejo habitual",nod="No o dudoso",us="Ecografía gástrica a pie de cama",
 g1="Grado 0 o 1 y ≤ 1,5 mL/kg<br/>Proceder",g2="Grado 2, sólidos o imagen no concluyente<br/>Diferir o manejar como estómago lleno (secuencia rápida)",
 foot="Adaptado de Pérez-Ajami D, Viscasillas Navarro E, Estupiñan Valido E. Rev Chil Anest 2026;55(2), figura 2. doi:10.25237/revchilanestv55n2-04 (CC BY 4.0) | Kindel TL et al. Surg Obes Relat Dis 2024;20:1183-1186"),
 'en':dict(note_t="2024 nuance",note="The Chilean review follows the ASA 2023 guidance (withhold for 1 week if dosed weekly). The 2024 multisociety guidance allows continuing the drug in most patients, with a 24-h clear-liquid diet in high-risk patients and gastric ultrasound when in doubt.",
 top="Patient on a GLP-1 or GLP-1/GIP agonist",q1="Digestive symptoms?<br/>nausea, vomiting, bloating",r1="Consider postponing the procedure",yes="Yes",no="No",
 q2="Was it withheld per the applicable guidance?",r2="Proceed with usual management",nod="No or uncertain",us="Bedside gastric ultrasound",
 g1="Grade 0 or 1 and ≤ 1.5 mL/kg<br/>Proceed",g2="Grade 2, solids or inconclusive image<br/>Postpone or manage as a full stomach (RSI)",
 foot="Adapted from Pérez-Ajami D, Viscasillas Navarro E, Estupiñan Valido E. Rev Chil Anest 2026;55(2), figure 2. doi:10.25237/revchilanestv55n2-04 (CC BY 4.0) | Kindel TL et al. Surg Obes Relat Dis 2024;20:1183-1186")}[lang]
NAVY=colors.Color(.03,.13,.30); MID=colors.Color(.08,.28,.55); LT=colors.Color(.83,.89,.97); PALE=colors.Color(.92,.95,.99); INK=colors.Color(.05,.10,.25)
c=canvas.Canvas(out,pagesize=(W,H))
def rect(x0,y0,x1,y1,fill,stroke=None,r=14,lw=3):
    c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.roundRect(x0,H-y1,x1-x0,y1-y0,r,stroke=1 if stroke else 0,fill=1)
def txt(x0,y0,x1,y1,s,size,color=INK,bold=True,align=TA_CENTER,valign='m',lead=1.18):
    st=ParagraphStyle('s',fontName='PagB' if bold else 'Pag',fontSize=size,leading=size*lead,alignment=align,textColor=color)
    p=Paragraph(s,st); w,h=p.wrap(x1-x0-24,1000)
    y=H-y0-h-14 if valign=='t' else H-(y0+y1)/2-h/2
    p.drawOn(c,x0+12,y)
def arrow(pts):
    c.setStrokeColor(MID); c.setFillColor(MID); c.setLineWidth(4)
    p=c.beginPath(); p.moveTo(pts[0][0],H-pts[0][1])
    for q in pts[1:]: p.lineTo(q[0],H-q[1])
    c.drawPath(p,stroke=1,fill=0)
    (x1,y1),(x2,y2)=pts[-2],pts[-1]; a=math.atan2(-(y2-y1),x2-x1); s=22
    p=c.beginPath(); p.moveTo(x2,H-y2); p.lineTo(x2-s*math.cos(a-.4),H-y2-s*math.sin(a-.4)); p.lineTo(x2-s*math.cos(a+.4),H-y2-s*math.sin(a+.4)); p.close(); c.drawPath(p,stroke=0,fill=1)
rect(25,17,387,579,colors.white,stroke=colors.Color(.6,.78,.95))
txt(25,17,387,579,"<b>%s</b>"%T['note_t'],38,valign='t',align=TA_LEFT)
txt(25,75,387,579,T['note'],31,bold=False,valign='t',align=TA_LEFT,lead=1.2)
rect(428,17,1092,107,NAVY); txt(428,17,1092,107,T['top'],33,colors.white)
rect(428,153,1092,270,PALE); txt(428,153,1092,270,T['q1'],35)
rect(1170,160,1769,263,LT); txt(1170,160,1769,263,T['r1'],35,bold=False)
rect(428,319,1092,421,PALE); txt(428,319,1092,421,T['q2'],35)
rect(1170,319,1769,421,LT); txt(1170,319,1769,421,T['r2'],35,bold=False)
rect(428,470,1092,575,MID); txt(428,470,1092,575,T['us'],38,colors.white)
rect(25,650,747,788,LT); txt(25,650,747,788,T['g1'],36)
rect(832,650,1769,788,NAVY); txt(832,650,1769,788,T['g2'],31,colors.white)
arrow([(760,107),(760,152)]); arrow([(760,270),(760,318)]); arrow([(760,421),(760,469)])
arrow([(1092,212),(1169,212)]); arrow([(1092,370),(1169,370)])
arrow([(602,575),(602,648)]); arrow([(918,575),(1118,648)])
c.setFillColor(MID); c.setFont('PagB',34)
c.drawString(1128,H-190,T['yes']); c.drawString(1128,H-348,T['yes']); c.drawString(776,H-298,T['no']); c.drawString(776,H-450,T['nod'])
sz=24
while pdfmetrics.stringWidth(T['foot'],'Pag',sz)>1775: sz-=.5
c.setFillColor(colors.Color(.3,.3,.3)); c.setFont('Pag',sz); c.drawString(20,H-826,T['foot'])
c.showPage(); c.save(); print('foot size',sz)
