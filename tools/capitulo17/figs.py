# -*- coding: utf-8 -*-
from reportlab.platypus import Flowable, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

BLUE = colors.Color(.106, .184, .271)
GREY = colors.Color(.88, .88, .88)
DK = colors.Color(.15, .15, .15)

def pst(size=7.2, align='c', bold=False, color=colors.black, lead=None):
    return ParagraphStyle('f', fontName='PagB' if bold else 'Pag', fontSize=size, leading=lead or size*1.22,
                          alignment=TA_CENTER if align == 'c' else TA_LEFT, textColor=color)

class Fig(Flowable):
    def __init__(self, w, h, fn, maxh=585):
        Flowable.__init__(self); self.w0 = w; self.h0 = h; self.fn = fn
        self.s = min(1.0, maxh/float(h)); self.width = w*self.s; self.height = h*self.s
    def wrap(self, aw, ah): return self.w0*self.s, self.h0*self.s
    def draw(self):
        self.canv.saveState(); self.canv.scale(self.s, self.s); self.fn(self.canv); self.canv.restoreState()
    def hAlign(self): pass

def txt(c, x, y, w, h, text, size=7.2, align='c', bold=False, valign='m', color=colors.black, pad=3):
    p = Paragraph(text.replace('\u2082', '<sub>2</sub>'), pst(size, align, bold, color))
    pw, ph = p.wrap(w-2*pad, 1000)
    if valign == 'm': yy = y + (h-ph)/2
    elif valign == 't': yy = y + h - ph - pad
    else: yy = y + pad
    p.drawOn(c, x+pad, yy)
    return ph

def box(c, x, y, w, h, text='', fill=colors.white, stroke=DK, r=4, size=7.2, bold=False, align='c', lw=.7, valign='m', color=colors.black, pad=3):
    c.setLineWidth(lw); c.setStrokeColor(stroke if stroke else colors.white); c.setFillColor(fill)
    if r: c.roundRect(x, y, w, h, r, stroke=1 if stroke else 0, fill=1)
    else: c.rect(x, y, w, h, stroke=1 if stroke else 0, fill=1)
    c.setFillColor(colors.black)
    if text: txt(c, x, y, w, h, text, size, align, bold, valign, color, pad)

def line(c, pts, arrow=True, lw=.7):
    c.setLineWidth(lw); c.setStrokeColor(DK); c.setFillColor(DK)
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)
    if arrow:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        import math
        a = math.atan2(y2-y1, x2-x1); s = 3.6
        p = c.beginPath(); p.moveTo(x2, y2)
        p.lineTo(x2 - s*math.cos(a-.4)*1.5, y2 - s*math.sin(a-.4)*1.5)
        p.lineTo(x2 - s*math.cos(a+.4)*1.5, y2 - s*math.sin(a+.4)*1.5)
        p.close(); c.drawPath(p, stroke=0, fill=1)

def circ(c, x, y, r, text, size=7):
    c.setLineWidth(.7); c.setStrokeColor(DK); c.setFillColor(colors.white); c.circle(x, y, r, stroke=1, fill=1)
    c.setFillColor(colors.black); c.setFont('Pag', size); c.drawCentredString(x, y-2.4, text)

T1 = {
 'es': dict(top="Cirugía bariátrica", c1="Sin AOS o AOS leve", c2="AOS moderada a grave<br/>IMC &gt; 60 kg/m²", c3="Síndrome de hipoventilación por obesidad",
   t1="• Oximetría de pulso basal", t2="• Oximetría y capnografía basales<br/>• Preparar el uso de su propia mascarilla de CPAP",
   t3="• Gasometría preoperatoria<br/>• Considerar monitorización con catéter de arteria pulmonar<br/>• Preparar el uso de su propia mascarilla de CPAP",
   a="Monitorización continua de la oximetría", hyp="¿Hipoxemia?", no="No", yes="Sí", fio="Aumentar la FiO₂", cpap="CPAP",
   icu="Monitorización continua con CPAP en la UCI",
   out="<b>Los pacientes pueden salir con seguridad del entorno monitorizado cuando:</b><br/>1. La SpO₂ se mantiene &gt; 90 % en aire ambiente, incluso durante el sueño.<br/>2. No hay hipoxemia ni obstrucción de la vía aérea cuando se deja al paciente sin estímulo.<br/>3. El paciente ya no requiere narcóticos parenterales."),
 'en': dict(top="Bariatric surgery", c1="No OSA or mild OSA", c2="Moderate to severe OSA<br/>BMI &gt; 60 kg/m²", c3="Obesity hypoventilation syndrome",
   t1="• Baseline pulse oximetry", t2="• Baseline oximetry and capnography<br/>• Prepare to use own CPAP mask",
   t3="• Preoperative blood gas<br/>• Consider pulmonary artery catheter monitoring<br/>• Prepare to use own CPAP mask",
   a="Continuous oximetry monitoring", hyp="Hypoxemia?", no="No", yes="Yes", fio="Increase FiO₂", cpap="CPAP",
   icu="Continuous monitoring with CPAP in the ICU",
   out="<b>Patients can be safely discharged from the monitored setting once:</b><br/>1. SpO₂ &gt; 90% can be maintained on room air, including during sleep.<br/>2. There is no hypoxemia or airway obstruction when the patient is left undisturbed.<br/>3. The patient no longer requires parenteral narcotics."),
}

def fig_monitor(lang, W):
    t = T1[lang]; H = 455
    def draw(c):
        box(c, 162.5, 428, 110, 22, t['top'], r=0, bold=True, size=8.2, lw=1.1)
        line(c, [(217.5, 428), (217.5, 412)], False); line(c, [(70, 412), (362, 412)], False)
        for cx in (70, 217.5, 362): line(c, [(cx, 412), (cx, 392)], False)
        box(c, 8, 358, 124, 34, t['c1'], size=7.6); box(c, 150, 358, 135, 34, t['c2'], size=7.6); box(c, 297, 358, 130, 34, t['c3'], size=7.6)
        txt(c, 8, 322, 124, 32, t['t1'], 7.2, 'l', valign='t', pad=2)
        txt(c, 150, 310, 135, 44, t['t2'], 7.2, 'l', valign='t', pad=2)
        txt(c, 297, 270, 132, 84, t['t3'], 7.2, 'l', valign='t', pad=2)
        line(c, [(70, 332), (70, 318)])
        box(c, 8, 292, 124, 26, t['a'], size=7.4)
        line(c, [(70, 292), (70, 274)])
        box(c, 28, 252, 84, 22, t['hyp'], size=7.4)
        line(c, [(112, 263), (150, 263)]); circ(c, 158, 263, 8, t['no'], 6.6)
        line(c, [(166, 263), (172, 263), (172, 197), (190, 197)])
        line(c, [(70, 252), (70, 236)]); c.setFont('Pag', 6.8); c.drawString(75, 241, t['yes'])
        box(c, 28, 216, 84, 20, t['fio'], size=7.4)
        line(c, [(70, 216), (70, 204)])
        box(c, 8, 178, 124, 26, t['a'], size=7.4)
        line(c, [(70, 178), (70, 168)])
        box(c, 28, 146, 84, 22, t['hyp'], size=7.4)
        line(c, [(112, 157), (150, 157)]); circ(c, 158, 157, 8, t['no'], 6.6); line(c, [(166, 157), (190, 157)])
        line(c, [(70, 146), (70, 128)]); c.setFont('Pag', 6.8); c.drawString(75, 133, t['yes'])
        box(c, 40, 108, 60, 20, t['cpap'], size=7.4)
        line(c, [(100, 118), (190, 118)])
        line(c, [(217.5, 312), (217.5, 282)], False); line(c, [(362, 268), (362, 282)], False); line(c, [(217.5, 282), (362, 282)], False)
        line(c, [(290, 282), (290, 262)])
        box(c, 185, 238, 210, 24, t['icu'], r=0, size=7.4)
        line(c, [(290, 238), (290, 214)])
        box(c, 190, 20, 240, 194, t['out'], r=14, size=7.8, align='l', valign='m', pad=9, lw=.9)
    return Fig(W, H, draw)

T2 = {
 'es': dict(title="Trombosis de venas esplácnicas",
   sev="Signos clínicos graves: shock, sepsis, isquemia intestinal u oclusión completa de la vena porta, de las venas mesentéricas superiores (VMS) o de la vena esplénica (VE)",
   yes="Sí", no="No", icu="Ingreso en UCI", surg="Manejo quirúrgico",
   bl="• Líquidos intravenosos y analgesia<br/>• Estudio de trombofilia*<br/>• Iniciar anticoagulación (HBPM/HNF) guiada por el riesgo de sangrado y la necesidad de resección urgente<br/>• Evaluación multidisciplinaria urgente (cirujano bariátrico/abdominal, radiología intervencionista, cirugía vascular, según disponibilidad)",
   br="• Líquidos intravenosos y analgesia<br/>• Estudio de trombofilia*<br/>• Iniciar anticoagulación (HBPM/HNF) guiada por el riesgo de sangrado y la necesidad de resección urgente",
   dia="¿Evolución clínica favorable?",
   yl="• Pasar a anticoagulante oral y alta<br/>• Seguimiento ambulatorio a las 2-3 semanas con hematología para revisar el estudio de trombofilia y el plan de anticoagulación<br/>• Programar el seguimiento por imagen según el médico tratante",
   nr="• Marcadores inflamatorios; TC abdominopélvica con contraste para evaluar la progresión y signos de isquemia intestinal<br/>• Revisión multidisciplinaria urgente: radiología intervencionista ± cirugía<br/>• Considerar trombólisis o trombectomía endovascular ± resección intestinal según la isquemia y el riesgo de sangrado",
   stable="Evolución estable", rep="Repetir la TC abdominopélvica con contraste a los 1-3 meses para evaluar la recanalización",
   comp="Recanalización completa y sin condición protrombótica", inc="Recanalización incompleta o cavernomatosis portal",
   cl="• Seguimiento por imagen a los 6 meses (TC con contraste)<br/>• Considerar suspender la anticoagulación según la guía y el estudio de trombofilia",
   ir="• Evaluación por hepatología<br/>• Discutir anticoagulación continuada (considerar larga duración)<br/>• Endoscopia digestiva alta para valorar várices (manejo según Baveno VII)",
   rec="Si hay hemorragia digestiva alta recurrente, síntomas isquémicos crónicos o colangiopatía portal",
   shunt="Consultar a radiología intervencionista para posible recanalización o derivación (shunt)"),
 'en': dict(title="Splanchnic vein thrombosis",
   sev="Severe clinical signs: shock, sepsis, intestinal ischemia, or complete occlusion of the portal vein, superior mesenteric veins (SMV), or splenic vein (SV)",
   yes="Yes", no="No", icu="Admit to the ICU", surg="Surgical management",
   bl="• IV fluids and analgesia<br/>• Thrombophilia testing*<br/>• Initiate anticoagulation (LMWH/UFH) guided by bleeding risk and need for urgent resection<br/>• Urgent multidisciplinary evaluation (bariatric/abdominal surgeon, interventional radiology, vascular surgery, as available)",
   br="• IV fluids and analgesia<br/>• Thrombophilia testing*<br/>• Initiate anticoagulation (LMWH/UFH) guided by bleeding risk and need for urgent resection",
   dia="Clinical course favorable?",
   yl="• Convert to oral anticoagulant and discharge<br/>• Outpatient follow-up in 2-3 weeks with hematology to review thrombophilia results and anticoagulation plan<br/>• Arrange imaging follow-up per treating physician",
   nr="• Check inflammatory markers; obtain contrast-enhanced abdominal and pelvic CT to assess progression and signs of intestinal ischemia<br/>• Urgent multidisciplinary review: interventional radiology ± surgery<br/>• Consider endovascular thrombolysis or thrombectomy ± bowel resection depending on ischemia and bleeding risk",
   stable="Stable evolution", rep="Repeat contrast-enhanced abdominal and pelvic CT at 1-3 months to evaluate recanalization",
   comp="Complete recanalization and no prothrombotic condition", inc="Incomplete recanalization or portal cavernomatosis",
   cl="• Continue follow-up imaging at 6 months (contrast CT)<br/>• Consider stopping anticoagulation per guidance and thrombophilia results",
   ir="• Hepatology evaluation<br/>• Discuss continued anticoagulation (consider long-term anticoagulation)<br/>• Upper GI endoscopy to evaluate varices (manage per Baveno VII)",
   rec="If recurrent upper GI bleeding, chronic ischemic symptoms, or portal cholangiopathy",
   shunt="Consult interventional radiology for possible recanalization or shunt procedures"),
}

def fig_svt(lang, W):
    t = T2[lang]; H = 632
    RED = colors.Color(.92, .62, .55); PINK = colors.Color(.96, .75, .72); GRN = colors.Color(.80, .88, .76); GRN2 = colors.Color(.72, .84, .70)
    AMB = colors.Color(.93, .72, .35); YEL = colors.Color(.99, .95, .55); BLU = colors.Color(.62, .78, .95); LBL = colors.Color(.82, .90, .98)
    def Y(top, h): return H - top - h
    def draw(c):
        S = 6.9
        box(c, 142, Y(2, 20), 150, 20, t['title'], fill=AMB, bold=True, size=7.6, stroke=None)
        line(c, [(217, H-22), (217, H-32)])
        box(c, 62, Y(32, 34), 310, 34, t['sev'], fill=RED, size=S, stroke=None)
        line(c, [(217, H-66), (217, H-76)], False); line(c, [(110, H-76), (324, H-76)], False)
        line(c, [(110, H-76), (110, H-84)], False); line(c, [(324, H-76), (324, H-84)], False)
        box(c, 94, Y(84, 12), 32, 12, t['yes'], fill=RED, size=6.6, stroke=None, r=3); box(c, 308, Y(84, 12), 32, 12, t['no'], fill=GRN, size=6.6, stroke=None, r=3)
        line(c, [(110, H-96), (110, H-106)]); line(c, [(324, H-96), (324, H-106)])
        box(c, 58, Y(106, 17), 104, 17, t['icu'], fill=PINK, size=S, stroke=None); box(c, 272, Y(106, 17), 104, 17, t['surg'], fill=GRN, size=S, stroke=None)
        line(c, [(110, H-123), (110, H-131)]); line(c, [(324, H-123), (324, H-131)])
        box(c, 8, Y(131, 80), 205, 80, t['bl'], fill=GREY, size=6.7, align='l', valign='m', stroke=None, r=3, pad=5)
        box(c, 222, Y(131, 80), 205, 80, t['br'], fill=GREY, size=6.7, align='l', valign='m', stroke=None, r=3, pad=5)
        line(c, [(110, H-211), (110, H-219)], False); line(c, [(324, H-211), (324, H-219)], False); line(c, [(110, H-219), (324, H-219)], False)
        line(c, [(217, H-219), (217, H-227)])
        # rombo
        d = c.beginPath(); cx, cy = 217, H-250; d.moveTo(cx-52, cy); d.lineTo(cx, cy+22); d.lineTo(cx+52, cy); d.lineTo(cx, cy-22); d.close()
        c.setFillColor(YEL); c.setStrokeColor(colors.Color(.8, .75, .3)); c.setLineWidth(.6); c.drawPath(d, fill=1, stroke=1)
        txt(c, cx-40, cy-12, 80, 24, t['dia'], 6.8)
        line(c, [(165, H-250), (100, H-250), (100, H-286)], True); line(c, [(269, H-250), (330, H-250), (330, H-286)], True)
        box(c, 82, Y(286, 12), 36, 12, t['yes'], fill=GRN, size=6.6, stroke=None, r=3); box(c, 312, Y(286, 12), 36, 12, t['no'], fill=RED, size=6.6, stroke=None, r=3)
        line(c, [(100, H-298), (100, H-308)]); line(c, [(330, H-298), (330, H-308)])
        box(c, 8, Y(308, 62), 205, 62, t['yl'], fill=GREY, size=6.7, align='l', stroke=None, r=3, pad=5)
        box(c, 222, Y(308, 88), 205, 88, t['nr'], fill=GREY, size=6.7, align='l', stroke=None, r=3, pad=5)
        line(c, [(222, H-338), (213, H-338)])
        line(c, [(110, H-370), (110, H-384)])
        box(c, 62, Y(384, 15), 96, 15, t['stable'], fill=BLU, size=S, stroke=None)
        line(c, [(110, H-399), (110, H-408)])
        box(c, 40, Y(408, 25), 300, 25, t['rep'], fill=LBL, size=S, stroke=None)
        line(c, [(190, H-433), (190, H-441)], False); line(c, [(90, H-441), (330, H-441)], False)
        line(c, [(90, H-441), (90, H-449)]); line(c, [(330, H-441), (330, H-449)])
        box(c, 8, Y(449, 28), 165, 28, t['comp'], fill=GRN2, size=S, stroke=None); box(c, 240, Y(449, 28), 175, 28, t['inc'], fill=PINK, size=S, stroke=None)
        line(c, [(90, H-477), (90, H-486)]); line(c, [(327, H-477), (327, H-486)])
        box(c, 8, Y(486, 62), 165, 62, t['cl'], fill=GREY, size=6.7, align='l', stroke=None, r=3, pad=5)
        box(c, 222, Y(486, 70), 205, 70, t['ir'], fill=GREY, size=6.7, align='l', stroke=None, r=3, pad=5)
        line(c, [(222, H-515), (173, H-515)])
        line(c, [(327, H-556), (327, H-564)])
        box(c, 232, Y(564, 28), 190, 28, t['rec'], fill=GREY, size=6.7, stroke=None, r=3)
        line(c, [(327, H-592), (327, H-602)])
        box(c, 232, Y(602, 28), 190, 28, t['shunt'], fill=GREY, size=6.7, stroke=None, r=3)
    return Fig(W, H, draw)

def make(key, lang, W):
    if key == 'monitor': return fig_monitor(lang, W)
    return fig_svt(lang, W)
