import sys, re
sys.path.insert(0, '.')
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, Flowable, KeepTogether, NextPageTemplate)
import content
FD = '../fonts/'
for n, f in (('Pag','regular'),('PagB','bold'),('PagI','italic'),('PagBI','bolditalic')):
    pdfmetrics.registerFont(TTFont(n, FD+'pagella-%s.ttf' % f))
pdfmetrics.registerFontFamily('Pag', normal='Pag', bold='PagB', italic='PagI', boldItalic='PagBI')
BLUE = colors.Color(.106, .184, .271); TW = 435.0; OX, EX = 84.0, 76.0; H = 841.89
lang, out, rem1_h, rem2_h = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
import json; POS = {}
L = content.ES if lang == 'es' else content.EN; hy = 'es_ES' if lang == 'es' else 'en_US'
base = dict(fontName='Pag', hyphenationLang=hy, embeddedHyphenation=0, uriWasteReduce=0.0)
S = {}
S['p'] = ParagraphStyle('p', fontSize=10.9091, leading=14.2262, alignment=TA_JUSTIFY, firstLineIndent=15, **base)
S['p0'] = ParagraphStyle('p0', parent=S['p'], firstLineIndent=0)
S['li'] = ParagraphStyle('li', parent=S['p'], firstLineIndent=0, leftIndent=19, bulletIndent=5, spaceAfter=4)
S['h2'] = ParagraphStyle('h2', fontName='PagI', fontSize=10.9091, leading=14.2, spaceBefore=4, spaceAfter=8, keepWithNext=1, alignment=TA_LEFT)
S['h3'] = ParagraphStyle('h3', fontName='PagBI', fontSize=10.9091, leading=14.2, spaceBefore=11, spaceAfter=6, keepWithNext=1, alignment=TA_LEFT)
S['capL'] = ParagraphStyle('capL', fontSize=9.9626, leading=12.553, alignment=TA_LEFT, spaceBefore=8, spaceAfter=5, keepWithNext=1, **base)
S['cell'] = ParagraphStyle('cell', fontName='Pag', fontSize=8.7, leading=10.8, alignment=TA_LEFT, hyphenationLang=hy)
S['cellH'] = ParagraphStyle('cellH', parent=S['cell'], fontName='PagB')
S['note'] = ParagraphStyle('note', parent=S['p0'], fontSize=9.9626, leading=12.553)
def sc(txt, small):
    out = ''
    for i, w in enumerate(txt.split(' ')):
        if i: out += ' '
        out += w[0].upper() + ('<font size="%s">%s</font>' % (small, w[1:].upper()) if len(w) > 1 else '')
    return out
def deco(parity):
    def f(c, doc):
        c.saveState(); c.setFont('Pag', 7.9)
        if parity == 'even': c.drawRightString(EX+TW, 787, L['run_even'].upper())
        else: c.drawString(OX+0.7, 787, L['run_odd'].upper())
        c.restoreState()
    return f
class Rem(Flowable):
    def __init__(self, h, key): Flowable.__init__(self); self.h = h; self.key = key; self.width = 1; self.height = h
    def wrap(self, aw, ah): return 1, self.h
    def draw(self):
        x, y = self.canv.absolutePosition(0, 0)
        POS[self.key] = (self.canv.getPageNumber(), H-(y+self.h))
doc = BaseDocTemplate(out, pagesize=A4)
fe = Frame(EX, 94, TW, 765-94, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
fo = Frame(OX, 94, TW, 765-94, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='odd', frames=[fo], onPage=deco('odd')), PageTemplate(id='even', frames=[fe], onPage=deco('even'))])
st = [NextPageTemplate(['even', 'odd'])]
if rem1_h: st += [Rem(rem1_h, 'R1'), Spacer(1, 14)]
st.append(Paragraph('%s&nbsp;&nbsp;&nbsp;&nbsp;%s' % (L['num'], L['title']), S['h2']))
for b in L['blocks']:
    t = b[0]
    if t == 'img': st += [Image('slide.jpg', width=TW, height=TW*810/1440), Spacer(1, 12)]
    elif t in ('p', 'p0', 'h3', 'note'): st.append(Paragraph(b[1], S[t]))
    elif t == 'bul':
        for it in b[1]: st.append(Paragraph(it, S['li'], bulletText='–'))
    elif t == 'tab':
        cap = Paragraph('%s 3.8. &nbsp;%s' % (sc('tabla' if lang == 'es' else 'table', 7.5), b[1]), S['capL'])
        data = [[Paragraph(c_, S['cellH'] if r == 0 else S['cell']) for c_ in row] for r, row in enumerate(b[2])]
        tb = Table(data, colWidths=b[3], repeatRows=1)
        tb.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), .8, BLUE), ('LINEBELOW', (0,0), (-1,0), .4, BLUE), ('LINEBELOW', (0,-1), (-1,-1), .8, BLUE),
                                ('LINEBELOW', (0,1), (-1,-2), .25, colors.Color(.75,.78,.82)), ('VALIGN', (0,0), (-1,-1), 'TOP'),
                                ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4), ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5)]))
        st.append(KeepTogether([cap, tb, Spacer(1, 8)]))
st.append(Spacer(1, 14)); st.append(Rem(rem2_h, 'R2'))
doc.build(st); print('pages', doc.page, POS); json.dump({'pages': doc.page, **POS}, open(out.replace('.pdf', '.json'), 'w'))
