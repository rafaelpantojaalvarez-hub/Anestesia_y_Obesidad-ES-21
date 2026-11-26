# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0, '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/ch17')
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Flowable, KeepTogether, NextPageTemplate, CondPageBreak, PageBreak)
from reportlab.pdfgen import canvas as _canvas
import content, figs

FD = '/tmp/claude-0/-home-user-Anestesia-y-Obesidad-ES-21/75bc264e-db1f-5a2e-97e2-8d240df88e1f/scratchpad/fonts/'
for n, f in (('Pag','regular'),('PagB','bold'),('PagI','italic'),('PagBI','bolditalic')):
    pdfmetrics.registerFont(TTFont(n, FD+'pagella-%s.ttf' % f))
pdfmetrics.registerFontFamily('Pag', normal='Pag', bold='PagB', italic='PagI', boldItalic='PagBI')

PAGES = {}
BLUE = colors.Color(.106, .184, .271)
H = 841.89; W = 595.28
TW = 435.0
FIRST_PRINTED = 225  # se ajusta por idioma
OX, EX = 84.0, 76.0   # margen izquierdo en pagina impar / par
TOPY, BOTY = 765.0, 94.0

def build(lang, out, secmap=None):
    global FIRST_PRINTED
    FIRST_PRINTED = 225 if lang == 'es' else 223
    L = content.ES if lang == 'es' else content.EN
    hy = 'es_ES' if lang == 'es' else 'en_US'
    # ---- numeracion de citas por orden de aparicion
    order = []
    def scan(s):
        for m in re.finditer(r'\{([a-z0-9,]+)\}', s):
            for k in m.group(1).split(','):
                if k not in order: order.append(k)
    scan(L['note'])
    for b in L['sections']:
        t = b[0]
        if t in ('p',): scan(b[1])
        elif t in ('h1','h2'): pass
        elif t == 'bul':
            for i in b[1]: scan(i)
        elif t == 'tab':
            scan(b[1])
            for row in b[2]:
                for c in row: scan(c)
        elif t == 'fig': scan(b[2])
        elif t == 'case': scan(b[1])
        elif t == 'keys':
            for i in b[1]: scan(i)
    num = {k: i+1 for i, k in enumerate(order)}
    def cite(s):
        def rep(m):
            ns = sorted(set(num[k] for k in m.group(1).split(',')))
            parts = []; i = 0
            while i < len(ns):
                j = i
                while j+1 < len(ns) and ns[j+1] == ns[j]+1: j += 1
                if j-i >= 2: parts.append('%d–%d' % (ns[i], ns[j]))
                else: parts.extend(str(x) for x in ns[i:j+1])
                i = j+1
            return '[' + ','.join(parts) + ']'
        return re.sub(r'\{([a-z0-9,]+)\}', rep, s)

    def sc(txt, big, small):
        out = ''
        for w_i, w in enumerate(txt.split(' ')):
            if w_i: out += ' '
            if not w: continue
            if w[0].isalpha() or w[0].isdigit():
                out += w[0].upper() if w[0].isalpha() else w[0]
                rest = w[1:]
                # parte en minusculas -> versalitas
                buf = ''
                for ch in rest:
                    if ch.isalpha():
                        buf += ch.upper()
                    else:
                        if buf: out += '<font size="%s">%s</font>' % (small, buf); buf = ''
                        out += ch
                if buf: out += '<font size="%s">%s</font>' % (small, buf)
            else: out += w
        return out

    base = dict(fontName='Pag', hyphenationLang=hy, embeddedHyphenation=0, uriWasteReduce=0.0, wordWrap=None)
    S = {}
    S['p'] = ParagraphStyle('p', fontSize=10.9091, leading=14.2262, alignment=TA_JUSTIFY, firstLineIndent=15, spaceAfter=0, **base)
    S['p0'] = ParagraphStyle('p0', parent=S['p'], firstLineIndent=0)
    S['li'] = ParagraphStyle('li', parent=S['p'], firstLineIndent=0, leftIndent=19, bulletIndent=5, bulletFontName='Pag', bulletFontSize=10.9091, spaceAfter=4)
    S['h1'] = ParagraphStyle('h1', fontName='Pag', fontSize=14.3462, leading=17.5, spaceBefore=22, spaceAfter=11, keepWithNext=1, alignment=TA_LEFT)
    S['h2'] = ParagraphStyle('h2', fontName='PagI', fontSize=10.9091, leading=14.2, spaceBefore=13, spaceAfter=7, keepWithNext=1, alignment=TA_LEFT)
    S['cap'] = ParagraphStyle('cap', fontSize=9.9626, leading=12.553, alignment=TA_JUSTIFY, spaceBefore=6, spaceAfter=4, **base)
    S['capL'] = ParagraphStyle('capL', parent=S['cap'], alignment=TA_LEFT, spaceBefore=8, spaceAfter=5, keepWithNext=1)
    S['cell'] = ParagraphStyle('cell', fontName='Pag', fontSize=8.7, leading=10.8, alignment=TA_LEFT, hyphenationLang=hy)
    S['cellH'] = ParagraphStyle('cellH', parent=S['cell'], fontName='PagB')
    S['sm'] = ParagraphStyle('sm', fontSize=9.9626, leading=12.553, alignment=TA_JUSTIFY, **base)
    S['smli'] = ParagraphStyle('smli', parent=S['sm'], leftIndent=19, bulletIndent=5, bulletFontName='Pag', bulletFontSize=9.9626, spaceAfter=6)
    S['ref'] = ParagraphStyle('ref', parent=S['sm'], leftIndent=22, bulletIndent=0, bulletFontName='Pag', bulletFontSize=9.9626, spaceAfter=3.5, alignment=TA_LEFT)
    S['obj'] = ParagraphStyle('obj', parent=S['sm'], leftIndent=20, bulletIndent=10, bulletFontSize=9.9626, spaceAfter=3.49)

    SUB = lambda x: x.replace('\u2082', '<sub>2</sub>')
    _cite0 = cite
    cite = lambda x: SUB(_cite0(x))
    def P(txt, style): return Paragraph(cite(txt), S[style])

    # ---- opener metrics
    note_p = Paragraph(cite(L['note']), ParagraphStyle('note', fontName='PagI', fontSize=9.9626, leading=12.553, alignment=TA_LEFT))
    ow = 519.2 - 104.6
    items = [Paragraph(SUB(t), S['obj']) for t in L['objectives']]
    obj_h = 0; wraps = []
    for p_ in items:
        w_, h_ = p_.wrap(ow-10, 1000); wraps.append(h_); obj_h += h_
    box_top = 514.88
    items_top = 499.26 - 9   # primera linea de items
    box_bottom = items_top - obj_h - 3.49*len(items) - 3
    first_frame_top = box_bottom - 18

    # ---- decoracion de paginas
    sections_by_page = secmap or {}
    def small_title(c, txt, x, align, size=7.9):
        c.setFont('Pag', size)
        t = txt.upper()
        if align == 'r': c.drawRightString(x, 787, t)
        else: c.drawString(x, 787, t)
    def deco(c, doc):
        pg = doc.page; printed = FIRST_PRINTED + pg - 1
        odd = (pg % 2 == 1)
        if pg == 1: return
        c.saveState(); c.setFillColor(colors.black)
        if odd:
            sec = sections_by_page.get(pg)
            if sec:
                c.setFont('Pag', 7.9)
                c.drawString(OX+0.7, 787, sec[0] + '  ')
                x = OX+0.7 + pdfmetrics.stringWidth(sec[0] + '  ', 'Pag', 7.9)
                c.drawString(x, 787, sec[1].upper())
            c.setFont('Pag', 9.9626); c.drawRightString(OX+TW, 787, str(printed))
        else:
            c.setFont('Pag', 9.9626); c.drawString(EX+0.7, 787, str(printed))
            c.setFont('Pag', 7.9); c.drawRightString(EX+TW, 787, L['running'].upper())
        c.restoreState()
    def opener(c, doc):
        c.saveState()
        x0 = OX + 0.68
        c.setFillColor(colors.black); c.setFont('Pag', 9.4)
        c.drawString(x0, 667.84, L['label'])
        c.setFont('Pag', 20.6625)
        c.drawString(x0, 623.75, L['title'][0]); c.drawString(x0, 623.75-26.152, L['title'][1])
        c.setLineWidth(.3985); c.setStrokeColor(colors.black)
        c.line(x0, 567.67, x0+173.55, 567.67)
        w_, h_ = note_p.wrap(TW, 100); note_p.drawOn(c, x0, 543 - h_ + 10)
        c.setStrokeColor(BLUE); c.setLineWidth(.797); c.line(x0, box_top, OX+TW, box_top)
        c.setFillColor(BLUE); c.setFont('Pag', 10.9091)
        lab = L['objlabel']; c.drawString(x0+3, 499.26, lab[0].upper()); xx = x0+3+pdfmetrics.stringWidth(lab[0].upper(), 'Pag', 10.9091)
        c.setFont('Pag', 8.6); c.drawString(xx, 499.26, lab[1:].upper())
        c.setFillColor(colors.black)
        y = items_top
        for t_, p_, h_ in zip(L['objectives'], items, wraps):
            c.setFont('Pag', 9.9626); c.drawString(x0+9.5, y-9.2, '–')
            p_.wrapOn(c, ow-10, 1000); p_.drawOn(c, x0+20, y-h_)
            y -= h_ + 3.49
        c.setStrokeColor(BLUE); c.setLineWidth(.3985); c.line(x0, box_bottom, OX+TW, box_bottom)
        c.restoreState()

    class Doc(BaseDocTemplate):
        def afterFlowable(self, fl):
            if getattr(fl, '_sec', None):
                PAGES.setdefault(self.page, []).append(fl._sec)
    doc = Doc(out, pagesize=A4, title='Capitulo 17')
    fr_open = Frame(OX, BOTY, TW, first_frame_top-BOTY, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='f0')
    fr_odd = Frame(OX, BOTY, TW, TOPY-BOTY, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='fo')
    fr_even = Frame(EX, BOTY, TW, TOPY-BOTY, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='fe')
    doc.addPageTemplates([PageTemplate(id='open', frames=[fr_open], onPage=opener),
                          PageTemplate(id='odd', frames=[fr_odd], onPage=deco),
                          PageTemplate(id='even', frames=[fr_even], onPage=deco)])

    # ---- flowables
    story = [NextPageTemplate(['even', 'odd'])]
    counters = {'tab': 0, 'fig': 0}
    after_head = True
    def label_sc(word, number):
        return sc(word.capitalize() if word.isupper() and False else word.lower(), 9.9626, 7.5) + ' ' + number
    def mkcap(kind, text, style):
        counters[kind] += 1
        word = L['tabla'] if kind == 'tab' else L['figura']
        lab = '%s %d.%d.' % (sc(word.lower(), 9.9626, 7.5), 17, counters[kind])
        return Paragraph(lab + '&nbsp; ' + cite(text), S[style])
    class SecPara(Paragraph):
        pass
    for b in L['sections']:
        t = b[0]
        if t == 'h1':
            para = Paragraph('%s&nbsp;&nbsp;&nbsp;&nbsp;%s' % (b[1], b[2]), S['h1']); para._sec = (b[1], b[2])
            story.append(para); after_head = True
        elif t == 'h2':
            story.append(Paragraph('%s&nbsp;&nbsp;&nbsp;&nbsp;%s' % (b[1], b[2]), S['h2'])); after_head = True
        elif t == 'p':
            story.append(P(b[1], 'p0' if after_head else 'p')); after_head = False
        elif t == 'bul':
            for it in b[1]:
                story.append(Paragraph(cite(it), ParagraphStyle('x', parent=S['li'], bulletText='–'), bulletText='–'))
            after_head = False
        elif t == 'tab':
            cap = mkcap('tab', b[1], 'capL')
            data = []
            for ri, row in enumerate(b[2]):
                data.append([Paragraph(cite(c), S['cellH'] if ri == 0 else S['cell']) for c in row])
            tb = Table(data, colWidths=b[3], repeatRows=1)
            tb.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), .8, BLUE), ('LINEBELOW', (0,0), (-1,0), .4, BLUE),
                                    ('LINEBELOW', (0,-1), (-1,-1), .8, BLUE), ('LINEBELOW', (0,1), (-1,-2), .25, colors.Color(.75,.78,.82)),
                                    ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
                                    ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5)]))
            blk = [cap, tb, Spacer(1, 8)]
            if story and getattr(story[-1], '_sec', None) is not None or (story and isinstance(story[-1], Paragraph) and story[-1].style.name in ('h1', 'h2')):
                blk = [story.pop()] + blk
            story.append(KeepTogether(blk)); after_head = False
        elif t == 'fig':
            fl = figs.make(b[1], lang, TW)
            cap = mkcap('fig', b[2], 'cap')
            story.append(KeepTogether([Spacer(1, 6), fl, cap, Spacer(1, 6)])); after_head = False
        elif t == 'case':
            txt = b[1].replace("<font name='PagS'>%s</font>" % L['caselabel'], sc(L['caselabel'].lower(), 9.9626, 7.5))
            tb = Table([[Paragraph(cite(txt), S['sm'])]], colWidths=[TW])
            tb.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), .8, BLUE), ('LINEBELOW', (0,-1), (-1,-1), .4, BLUE),
                                    ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
                                    ('TOPPADDING', (0,0), (-1,-1), 12), ('BOTTOMPADDING', (0,0), (-1,-1), 12)]))
            story.append(tb); after_head = False
        elif t == 'keys':
            hh = Paragraph(L['keyh'], S['h1']); story.append(hh)
            cells = [Paragraph(sc(L['keylabel'].lower(), 10.9091, 8.6), ParagraphStyle('kl', fontName='Pag', fontSize=10.9091, leading=14, textColor=BLUE))]
            for it in b[1]:
                cells.append(Paragraph(cite(it), S['smli'], bulletText='–'))
            tb = Table([[c_] for c_ in cells], colWidths=[TW-8])
            tb.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), .8, BLUE), ('LINEBELOW', (0,-1), (-1,-1), .8, BLUE),
                                    ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 0),
                                    ('TOPPADDING', (0,0), (-1,0), 12), ('TOPPADDING', (0,1), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-2), 2), ('BOTTOMPADDING', (0,-1), (-1,-1), 14)]))
            story.append(tb)
    # referencias
    _rp = Paragraph(L['refs'], ParagraphStyle('rh', parent=S['h1'], spaceBefore=34)); _rp._sec = ('', L['refs']); story.append(_rp)
    for k in order:
        au, rest = content.REFS[k]
        if lang == 'en': au = au.replace(' y ', ' and ')
        story.append(Paragraph('%s. %s.' % (au, rest.replace('&', '&amp;')), S['ref'], bulletText='%d.' % num[k]))
    secs = {}
    class Collect:
        pass
    doc.build(story)
    return doc, num

if __name__ == '__main__':
    import io, json
    lang = sys.argv[1]; out = sys.argv[2]
    build(lang, io.BytesIO(), None)
    cur = None; secmap = {}
    for pg in range(1, 80):
        if pg in PAGES: cur = PAGES[pg][-1]
        if cur: secmap[pg] = cur
    first = {}
    for pg in sorted(PAGES):
        for lab, ttl in PAGES[pg]:
            first.setdefault(lab or 'REF', pg)
    PAGES.clear()
    build(lang, out, secmap)
    start = FIRST_PRINTED
    toc = {k: start + v - 1 for k, v in first.items()}
    json.dump(toc, open(out.replace('.pdf', '_toc.json'), 'w'))
    print('ok', out, toc)
