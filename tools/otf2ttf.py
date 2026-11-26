import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
src,dst=sys.argv[1:3]
f=TTFont(src); gs=f.getGlyphSet(); order=f.getGlyphOrder()
glyf={}
for n in order:
    pen=TTGlyphPen(gs); gs[n].draw(Cu2QuPen(pen,1.0,reverse_direction=True)); glyf[n]=pen.glyph()
f['loca']=newTable('loca'); t=f['glyf']=newTable('glyf'); t.glyphOrder=order; t.glyphs=glyf
del f['CFF ']
if 'VORG' in f: del f['VORG']
f['maxp'].tableVersion=0x00010000
for a in ('maxZones','maxTwilightPoints','maxStorage','maxFunctionDefs','maxInstructionDefs','maxStackElements','maxSizeOfInstructions','maxComponentElements'): setattr(f['maxp'],a,0)
f['maxp'].maxZones=1
f['post'].formatType=2.0; f['post'].extraNames=[]; f['post'].mapping={}; f['post'].glyphOrder=order
f['head'].glyphDataFormat=0
f.sfntVersion='\x00\x01\x00\x00'
f.save(dst)
