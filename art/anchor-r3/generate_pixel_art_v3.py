"""Round 3 anchor. Run python3 generate_pixel_art_v3.py beside the v2 module.
Original integer-coordinate raster drawing. No APIs, resampling or external art.
Imports only the A2 palette, prop drawing code and board CSS; preserves all v2 files.
"""
from PIL import Image, ImageDraw
from generate_pixel_art_v2 import Art, PALETTES, ROLES, CSS, sprite, tile as old_tile
from pathlib import Path
import random
ROOT=Path(__file__).resolve().parent
P=PALETTES[0]

def material(kind,variant=0):
 a=Art(0,32,32);r=random.Random(400+variant)
 if kind=='paving':
  a.rect((0,0,31,31),4)
  # Four broad, nearly flush flags. Midtone joints, never dark mortar.
  a.line([(0,17),(31,17)],3);a.line([(19,0),(19,17)],3);a.line([(10,17),(10,31)],3)
  for x,y,w in [(2,1,12),(21,1,7),(1,19,6),(13,19,14)]:a.line([(x,y),(x+w,y)],5)
  a.line([(20,1),(20,5)],5);a.line([(11,19),(11,22)],5)
  for _ in range(9):
   x=r.randrange(2,30);y=r.randrange(3,30);a.line([(x,y),(min(x+2,31),y)],5 if _%3==0 else 4)
  a.line([(27,24),(25,26),(25,28)],3)
 elif kind=='wall':
  a.rect((0,0,31,31),1)
  # Tall rough blocks distinguish the vertical plane from broad yard flags.
  for x,y,w,h in [(0,2,10,17),(12,2,9,17),(23,2,8,17),(0,21,16,10),(18,21,13,10)]:
   a.poly([(x+1,y),(x+w-1,y),(x+w,y+3),(x+w-1,y+h),(x,y+h-1),(x,y+2)],2)
   a.line([(x+2,y),(x+w-2,y)],3);a.line([(x+1,y+2),(x+1,y+h-3)],3)
   a.line([(x+4,y+h-5),(x+5,y+h-2)],1)
  a.rect((0,0,31,1),5);a.line([(2,2),(15,2)],4)
  a.line([(0,29),(31,29)],10);a.line([(4,30),(10,30)],11)
 elif kind=='rock':
  a.rect((0,0,31,31),0)
  # Massive fractured basalt; no horizontal courses or enclosed brick shapes.
  a.poly([(0,2),(10,0),(17,5),(14,12),(20,22),(13,31),(0,31)],1)
  a.poly([(20,0),(31,0),(31,26),(27,19),(21,17),(25,8)],1)
  a.line([(2,5),(8,3),(11,4)],2);a.line([(26,21),(29,25),(31,25)],2)
  a.line([(19,1),(17,7),(21,12),(18,18),(22,24)],0)
  a.weed(7,27,9);a.weed(27,10,5)
 elif kind=='water':
  a.rect((0,0,31,31),7)
  for x,y,w,c in [(0,4,11,8),(19,9,12,8),(6,15,15,8),(2,23,6,9),(18,29,13,8),(12,6,4,9)]:a.line([(x,y),(x+w,y)],c)
 elif kind=='foam':
  a.im=material('water');a.d=ImageDraw.Draw(a.im)
  for x,y,w in [(0,2,7),(9,3,4),(16,1,9),(28,3,3),(4,5,3),(20,5,4)]:a.line([(x,y),(x+w,y)],6 if y<4 else 9)
 return a.im

def terrain(kind):
 if kind in ('paving','wall','rock','water','foam'):return material(kind)
 if kind.startswith('rim'):
  a=Art(0,32,32);a.im=material('paving');a.d=ImageDraw.Draw(a.im)
  if kind in ('rim-s','rim-se','rim-inner'):
   a.rect((0,30,31,31),0);a.line([(0,29),(31,29)],5)
  if kind in ('rim-e','rim-se'):
   a.rect((30,0,31,31),1);a.line([(29,0),(29,29)],5)
  if kind=='rim-inner':
   a.rect((24,24,31,31),1);a.line([(24,24),(31,24)],5);a.line([(24,24),(24,28)],5)
  return a.im
 if kind.startswith('slip'):
  a=Art(0,32,32);a.im=material('rock');a.d=ImageDraw.Draw(a.im)
  if kind in ('slip-w','slip-nw'):a.line([(0,0),(0,31)],3)
  if kind in ('slip-e','slip-ne'):a.line([(31,0),(31,31)],2)
  if kind in ('slip-nw','slip-ne'):a.line([(0,0),(31,0)],3)
  if kind=='slip-foot':
   for x,y,w in [(0,29,7),(9,30,9),(22,28,8)]:a.line([(x,y),(x+w,y)],6)
  return a.im
 if kind=='wall-east':
  im=material('wall');d=ImageDraw.Draw(im);d.rectangle((0,0,2,31),fill=P[5]);return im
 return old_tile(0,{'boards':6,'rack':7,'door':8}[kind])

TILES=[('paving','01 · Worn flags'),('wall','02 · Vertical cliff'),('rock','03 · Black basalt'),('water','04 · Open channel'),('foam','05 · Tide foam'),('rim-s','06 · South coping'),('rim-e','07 · East coping'),('rim-se','08 · Outer corner'),('rim-inner','09 · Inner coping detail'),('wall-east','10 · Cliff return'),('slip-w','11 · Slip west'),('slip-e','12 · Slip east'),('slip-nw','13 · Slip entry L'),('slip-ne','14 · Slip entry R'),('slip-foot','15 · Slip toe'),('boards','16 · Bench grain'),('rack','17 · Hook & rope'),('door','18 · Shed planks')]
# 12 columns × 10 rows. Shore and slip turn only at whole tile boundaries.
MAP=['PPPPPPPPPPPP']*5+['PPPPPPPPPSSW','PPPPPPPPFSS~','FFFFFFFF~~SS','~~~~~~~~~~SS','~~~~~~~~~~~~']

def bryn(view,walking=False):
 a=Art(0,32,32,True);a.im=sprite(0,view);a.d=ImageDraw.Draw(a.im)
 # Remove the old entire head: clean chin and no dark lower-face band.
 a.d.rectangle((8,0,24,13),fill=(0,0,0,0))
 a.poly([(11,4),(14,2),(19,2),(22,5),(22,8),(10,8)],0)
 a.poly([(12,4),(15,3),(19,3),(21,5),(21,7),(11,7)],16)
 a.line([(12,5),(19,5)],22);a.rect((10,7,22,8),12);a.line([(11,7),(21,7)],14)
 for x in (12,15,18,20):a.dot(x,6,14)
 # A little slouched crown extends the silhouette to the left.
 a.rect((9,4,11,6),16);a.dot(9,4,14)
 if view=='back':
  a.rect((12,9,20,11),15);a.line([(12,9),(15,9)],16);a.rect((14,12,18,13),20)
 elif view=='front':
  a.poly([(12,9),(20,9),(20,11),(18,13),(14,13),(12,11)],20)
  a.dot(13,9,15);a.dot(14,10,0);a.dot(18,10,0);a.dot(20,10,19);a.dot(16,12,19)
 else:
  a.rect((13,9,20,12),20);a.rect((20,10,21,11),20);a.dot(19,9,0);a.rect((12,9,13,10),15);a.dot(17,12,19)
 if walking:
  a.d.rectangle((9,24,24,31),fill=(0,0,0,0))
  a.poly([(12,24),(16,24),(15,27),(12,29),(10,28)],2);a.rect((8,28,13,29),0);a.dot(9,28,14)
  a.poly([(18,24),(21,24),(22,26),(23,26),(23,27),(18,27)],1);a.rect((20,27,25,28),0);a.dot(21,27,14)
  a.rect((8,21,10,23),20);a.rect((22,20,24,22),20)
  a.rect((19,23,25,26),15);a.rect((20,23,24,24),16);a.dot(22,24,21)
 return a.im

def draw_scene():
 a=Art(0)
 for y,row in enumerate(MAP):
  for x,c in enumerate(row):
   if c=='P':
    south=y==9 or MAP[y+1][x]!='P';east=x==11 or row[x+1]!='P'
    kind='rim-se' if south and east else 'rim-s' if south else 'rim-e' if east else 'paving'
   elif c=='F':kind='wall-east' if x==8 else 'wall'
   elif c=='W':kind='wall'
   elif c=='S':
    left=x==0 or row[x-1]!='S';right=x==11 or row[x+1]!='S';top=y==0 or MAP[y-1][x]!='S'
    kind='slip-nw' if top and left else 'slip-ne' if top and right else 'slip-w' if left else 'slip-e' if right else 'rock'
    if y==8:kind='slip-foot'
   else:kind='foam' if y>0 and MAP[y-1][x] in 'FW' else 'water'
   a.im.paste(terrain(kind),(32*x,32*y))
 a.d=ImageDraw.Draw(a.im)
 # A2 geometry retained for all major props. Only surface topology changes.
 a.poly([(31,105),(112,105),(146,139),(61,139)],3)
 a.poly([(175,85),(300,85),(320,109),(192,109)],3)
 a.shed(30,38,83,76);a.lean(170,29,130);a.rack(181,104,58)
 # Loose objects moved away from reserved circulation strip y=160..191.
 x,y=58,147
 a.d.ellipse((x,y,x+17,y+8),outline=P[14],width=2);a.d.ellipse((x+4,y+2,x+13,y+6),outline=P[13]);a.line([(x+15,y+5),(x+24,y+9)],14)
 a.poly([(272,113),(283,113),(281,125),(274,125)],2);a.line([(272,113),(283,113)],5)
 a.d.ellipse((157,186,180,191),fill=P[3]);b=bryn('front');a.im.paste(b,(151,160),b)
 return a.im

def build():
 draw_scene().save(ROOT/'option-anchor-scene.png')
 sheet=Image.new('RGB',(192,96))
 for n,(kind,label) in enumerate(TILES):
  t=terrain(kind);t.save(ROOT/f'option-anchor-tile-{n:02}.png');sheet.paste(t,((n%6)*32,(n//6)*32))
 sheet.save(ROOT/'option-anchor-tiles.png')
 chars=Image.new('RGBA',(96,64))
 for n,v in enumerate(['front','back','side']):
  for walking in (False,True):
   b=bryn(v,walking);suffix='-walk' if walking else '';b.save(ROOT/f'option-anchor-bryn-{v}{suffix}.png');chars.paste(b,(n*32,32*walking))
 chars.save(ROOT/'option-anchor-bryn.png')
 # Reuse original code-drawn bone fid without changing round 2.
 fid=Art(0,32,32,True);fid.poly([(9,25),(11,17),(21,6),(24,4),(25,7),(19,17),(13,25)],15);fid.poly([(10,24),(12,17),(23,5),(23,9),(17,19),(12,24)],21);fid.line([(12,21),(20,10)],5);fid.dot(12,23,0);fid.save('option-anchor-bone-fid.png')
 roles=ROLES.copy();roles[22]='Knit cap / warm yarn highlight';roles[23]='Reserved brightest warm accent'
 palette=''.join(f'<div class="swatch"><i style="background:{c}"></i><code>{c}</code><span>{r}</span></div>' for c,r in zip(P,roles))
 tiles=''.join(f'<figure><img src="option-anchor-tile-{n:02}.png" width="96" height="96" alt="{label}"><figcaption>{label}</figcaption></figure>' for n,(_,label) in enumerate(TILES))
 sprites=''.join(f'<figure><img src="option-anchor-bryn-{v}{suffix}.png" width="128" height="128" alt="Bryn {v} {pose}"><figcaption>{v.title()} / {pose}</figcaption></figure>' for suffix,pose in [('', 'idle'),('-walk','walk contact')] for v in ['front','back','side'])
 html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Mending Shift — Visual Anchor</title><style>{CSS} .legend{{display:flex;gap:20px;flex-wrap:wrap}}.legend span{{border-left:12px solid var(--c);padding-left:8px}}.tiles figure{{width:145px}}pre{{font:13px/1.7 monospace;overflow:auto}}.callout{{border-left:3px solid #b7ad95;padding:0 18px}} </style><body><nav><a href="index-v2.html">← Round 2</a><a href="option-a2.html">Compare A2</a></nav><header><div class="eyebrow">THE MENDING SHIFT / ROUND 03 / VISUAL ANCHOR / MOCKUP</div><h1>Salt & Rivet</h1><p>Sallowquay Boat-yard, afternoon. A compact outlined working yard: the shed on the left, worn bench under the lean-to at the back, finished tools on the rack, and the black slip descending on the right. Warm light from upper left; cool shade under the structures.</p><div class="meta">384 × 320 scene · 12 × 10 cells · 32px native tiles · original code-drawn art</div></header><main><section><h2>01 / The anchor</h2><div class="legend"><span style="--c:{P[4]}">Light flags / walkable yard</span><span style="--c:{P[2]}">Dark cliff / drop</span><span style="--c:{P[0]}">Black basalt / tidal slip</span><span style="--c:{P[8]}">Horizontal ripples / water</span></div><h3>2× / 768 × 640</h3><div class="viewport"><img src="option-anchor-scene.png" width="768" height="640" alt="Anchor scene at twice native resolution"></div><h3>1× / 384 × 320</h3><div class="viewport"><img src="option-anchor-scene.png" width="384" height="320" alt="Anchor at native resolution"></div></section><section><h2>02 / What changed from A2</h2><ul><li>Large, low-contrast worn flags replace the yard’s brick stamp. The cliff uses tall dark blocks with a sunlit coping; the slip is fractured matte basalt with weed, and water uses horizontal ripples and tide foam.</li><li>The shore and slip now turn at 32px cell boundaries. Repeatable coping, return, corner, slip-entry and toe tiles build the contour.</li><li>A continuous 32px circulation row at y=160–191 runs in front of the shed, bench and rack to the slip entry. Loose objects sit above it.</li><li>Bryn’s jaw is clean skin, without the dark chin band. A rust knitted cap with a slouched crown identifies him in all three views; each view also has a walking contact pose.</li></ul></section><section><h2>03 / Full tile sheet <small>18 tiles · 6 columns × 3 rows</small></h2><div class="viewport"><img src="option-anchor-tiles.png" width="576" height="288" alt="Full anchor tile atlas, enlarged three times"></div><p class="caption">Sheet native size 192 × 96. Tiles below shown at 3×. Corner 09 is an optional inset coping detail; the scene uses whole-cell outer corners.</p><div class="tiles">{tiles}</div></section><section><h2>04 / Bryn Aukett, fifteen <small>32 × 32 frames · 4× display</small></h2><div class="sprites">{sprites}<figure><img src="option-anchor-bone-fid.png" width="128" height="128" alt="Bone fid tool"><figcaption>Bone fid</figcaption></figure></div><p>Knitted rust cap, cropped hair, clean cheeks and chin, blue work jacket, linen collar, bare hands and leather satchel. A single walking contact frame accompanies each idle view; these are pose studies, not a complete walk cycle.</p><p class="caption">Combined transparent sheet: 96 × 64. Columns front / back / side; rows idle / walk contact.</p><div class="viewport"><img src="option-anchor-bryn.png" width="384" height="256" alt="Bryn six-frame sheet at four times native scale"></div></section><section><h2>05 / A2 palette retained <small>24 exact colours</small></h2><div class="palette">{palette}</div></section><section><h2>06 / Tile topology & circulation</h2><p>Every character below is one 32px cell. P = walkable yard; F/W = vertical cliff; S = tidal slip; ~ = water. Row 06 (zero-based row 5) is the uninterrupted yard route to the slip. Bryn stands on it. The slip is a tidal work surface, not ordinary yard paving.</p><pre>{chr(10).join(MAP)}</pre><p class="callout">A visual anchor, labelled MOCKUP. The grid describes terrain and a clear route; it is not an implemented collision map.</p></section></main><footer>MOCKUP · <a href="generate_pixel_art_v3.py">Anchor generator</a> + <a href="generate_pixel_art_v2.py">A2 drawing primitives</a> · Run python3 generate_pixel_art_v3.py · Integer drawing only; no external image assets or APIs.</footer></body></html>'''
 (ROOT/'option-anchor.html').write_text(html)
 print('Wrote anchor board, scene, 18-tile atlas, six character frames and combined sheet.')
if __name__=='__main__':build()
