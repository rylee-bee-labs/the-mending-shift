"""The Mending Shift, round 2. Original integer-grid raster art; Pillow only.
Run: python3 generate_pixel_art_v2.py. Seeds, palettes and geometry are fixed.
No external assets, fonts, image APIs, filtering or antialiasing.
"""
from PIL import Image, ImageDraw
from pathlib import Path
import random, json, math
ROOT=Path(__file__).resolve().parent
ROLES=['Deep crease / eyes','Cool cast shadow','Wet basalt','Stone shade','Dry stone','Stone sun edge','Salt / foam','Deep channel','Water body','Ripple light','Weed shadow','Weed tips','Timber shadow','Timber body','Worn wood edge','Hair / leather shade','Satchel / rust','Jacket shadow','Jacket light','Skin shadow','Skin light','Linen / bone','Lamp amber','Lamp core']
PALETTES=[
['#202632','#343a4b','#424957','#626775','#8d8b88','#b7ad95','#ded6b5','#2c485c','#426b7c','#7c9d9f','#354a44','#78816a','#493f43','#766052','#aa8864','#49352f','#b66c43','#365168','#628393','#bb7c59','#e4ae7c','#f4dfaf','#d89a55','#ffe6a8'],
['#313c50','#4b566e','#596d7a','#81909a','#a8afa9','#cdc7ae','#eee3c8','#496b81','#7096a2','#a7c3c2','#4d6b65','#8da380','#655860','#9a7d70','#c6a385','#614c4c','#b87859','#45637b','#83a3b2','#c28e7d','#edbfa0','#fff0ce','#deb47d','#fff3d9'],
['#111923','#22283d','#293c4b','#415563','#687577','#98947e','#c4b999','#172e45','#294d61','#517e8a','#253e3d','#647458','#302e38','#625049','#9d7756','#30252d','#b16d43','#2d485e','#668292','#ad7159','#e2a675','#e8d4a2','#dc943e','#ffdd87']]
TITLES=['A · Salt & Rivet','B · The Long Morning','C · The Turning']
DESCS=[
'A compact, elevated three-quarter yard with the shed on the left, a long bench under a pitched lean-to at the back, and a narrow slipway descending to the right. Afternoon light falls from upper left. Firm broken outlines and short ramps give this direction a low-colour handheld-era rhythm; chips and clustered marks carry the age of the yard.',
'A wider, open diagonal quay: the shed sits at the upper right, the bench shelters beside it, and a broad black slip crosses the lower left. Morning light comes from upper right. Soft coloured edges, irregular stone clusters and quiet pools of colour replace the heavier contours; pale tide foam opens space around the working objects.',
'A close, tall cutaway at the Turning, before dawn. The shed and long lean-to occupy the left bank; the wall drops across the foreground and the slip cuts down through its right edge. A single work lamp catches tools, worn boards and Bryn’s face. Hard silhouettes, cold reflected water and small amber edges make the yard feel occupied without making it magical.']
NAMES=['Dry setts','Wet setts','Cliff masonry','Weed / basalt','Tidal water','Foam edge','Worn boards','Hook / rope','Shed planks']
class Art:
 def __init__(self,k,w=384,h=320,transparent=False):
  self.k=k;self.p=PALETTES[k];self.im=Image.new('RGBA' if transparent else 'RGB',(w,h),(0,0,0,0) if transparent else self.p[7]);self.d=ImageDraw.Draw(self.im);self.r=random.Random(881+k)
 def rect(self,b,c):self.d.rectangle(tuple(map(int,b)),fill=self.p[c])
 def line(self,pts,c,w=1):self.d.line(pts,fill=self.p[c],width=w)
 def poly(self,pts,c):self.d.polygon(pts,fill=self.p[c])
 def dot(self,x,y,c):self.d.point((x,y),fill=self.p[c])
 def stone(self,box,wet=False,wall=False):
  x,y,X,Y=box; base=2 if wet else 3; self.rect(box,2 if self.k==1 else 1)
  for row,yy in enumerate(range(y,Y,9 if wall else (18 if self.k==1 else 12))):
   xx=x-(8 if row%2 else 0)
   while xx<X:
    w=self.r.randint(18,38) if self.k==1 and not wall else self.r.randint(12,24);h=self.r.randint(12,18) if self.k==1 and not wall else self.r.randint(7,10 if wall else 12);end=min(xx+w-2,X);bot=min(yy+h-1,Y)
    c=base if wet else self.r.choice([3,4,4,4] if self.k==0 else [3,3,4,4,4] if self.k==1 else [2,3,3,3]);self.poly([(xx+2,yy),(end-2,yy),(end,yy+2),(end-1,bot-1),(xx+1,bot),(xx,yy+3)],c)
    self.line([(xx+3,yy),(end-3,yy)],3 if wet else (5 if self.k==0 else 4))
    if self.k==0:self.line([(xx+1,bot),(end-2,bot)],1)
    for _ in range(3 if self.k!=1 else 5):
     px=self.r.randint(xx+2,max(xx+2,end-2));py=self.r.randint(yy+2,max(yy+2,bot-1));self.line([(px,py),(px+self.r.randint(0,2),py)],self.r.choice([2,3] if wet else [3,5] if self.k==0 else [3,4]))
    xx+=w
 def water(self):
  self.rect((0,0,383,319),7)
  for y in range(1,320,3):
   for _ in range(5):
    x=self.r.randrange(384);w=self.r.randrange(3,24);c=self.r.choice([7,8,8,9]);self.line([(x,y),(x+w,y)],c)
    if self.k==1:self.line([(x+2,y+1),(x+w-3,y+1)],8)
 def weed(self,x,y,size=12):
  for _ in range(size):
   xx=x+self.r.randint(-9,9);yy=y+self.r.randint(-4,4);hh=self.r.randint(3,11)
   self.line([(xx,yy),(xx-2,yy-hh//2),(xx+1,yy-hh)],10)
   self.poly([(xx,yy-hh),(xx+3,yy-hh+2),(xx+2,yy-hh+5),(xx,yy-hh+3)],11)
   if _%3==0:self.poly([(xx,yy),(xx-4,yy-3),(xx-3,yy-6),(xx+1,yy-2)],10)
 def wood(self,box,vertical=False):
  x,y,X,Y=box;self.rect(box,12)
  if vertical:
   for xx in range(x+1,X,7):
    self.rect((xx,y, min(xx+5,X),Y),13);self.line([(xx,y+2),(xx,Y-2)],14)
    for _ in range(3):
     yy=self.r.randint(y,max(y,Y-8));self.line([(xx+3,yy),(xx+3,yy+5)],12)
  else:
   for yy in range(y+1,Y,5):
    self.rect((x,yy,X,min(yy+3,Y)),13);self.line([(x+2,yy),(X-3,yy)],14)
    for _ in range(5):
     xx=self.r.randint(x,max(x,X-15));self.line([(xx,yy+2),(xx+self.r.randint(3,12),yy+2)],12)
 def shed(self,x,y,w=83,h=68):
  self.poly([(x+5,y+h),(x+w+9,y+h),(x+w+24,y+h+11),(x+16,y+h+15)],1)
  self.wood((x,y+17,x+w,y+h),True);self.poly([(x+w,y+17),(x+w+15,y+9),(x+w+15,y+h-9),(x+w,y+h)],12)
  self.poly([(x-7,y+17),(x+12,y-7),(x+w-9,y-7),(x+w+19,y+14)],0 if self.k==0 else 1)
  for yy in range(y-4,y+15,4):
   left=x+10-(yy-y+4)//2;self.line([(left,yy),(x+w-7+(yy-y+4)//2,yy)],2)
   for xx in range(left+5,x+w-7,13):self.line([(xx,yy),(xx+4,yy)],3)
  self.line([(x-7,y+17),(x+w+19,y+17)],14)
  self.rect((x+17,y+28,x+43,y+h),0);self.wood((x+19,y+30,x+40,y+h),True)
  self.rect((x+36,y+48,x+38,y+50),21);self.rect((x+51,y+29,x+72,y+45),12);self.rect((x+53,y+31,x+70,y+42),8)
  self.line([(x+62,y+30),(x+62,y+44)],14)
 def lean(self,x,y,w=114):
  for xx in (x+4,x+w-6):self.rect((xx+3,y+28,xx+7,y+71),1);self.wood((xx,y+21,xx+3,y+66),True)
  self.poly([(x-6,y+25),(x+8,y),(x+w-15,y),(x+w+8,y+25)],12)
  for yy in range(y+2,y+25,4):
   self.line([(x+6-(yy-y)//2,yy),(x+w-14+(yy-y)//1,yy)],13)
   self.line([(x+8-(yy-y)//2,yy),(x+w-15+(yy-y)//1,yy)],14 if self.k!=2 else 3)
  self.line([(x-6,y+25),(x+w+8,y+25)],0 if self.k==0 else 12)
  self.rect((x+10,y+61,x+w-7,y+66),1)
  self.wood((x+9,y+43,x+w-11,y+51));self.rect((x+14,y+52,x+18,y+65),12);self.rect((x+w-23,y+52,x+w-19,y+65),12)
  # A repaired ceramic mug, rag, vice: warmth belongs to objects.
  self.rect((x+24,y+37,x+29,y+42),21);self.line([(x+30,y+38),(x+32,y+38),(x+32,y+41),(x+30,y+41)],5)
  self.poly([(x+46,y+42),(x+59,y+39),(x+66,y+44),(x+52,y+45)],18)
  self.rect((x+w-37,y+39,x+w-29,y+44),2);self.rect((x+w-34,y+44,x+w-31,y+54),0)
 def rack(self,x,y,w=58):
  self.wood((x,y,x+w,y+5));self.wood((x+2,y+5,x+5,y+39),True);self.wood((x+w-5,y+5,x+w-2,y+39),True)
  for n in range(4):
   xx=x+11+n*11;self.line([(xx,y+3),(xx,y+10),(xx-3,y+11),(xx-3,y+8)],5)
   self.rect((xx-1,y+13,xx+1,y+27),16);self.line([(xx,y+13),(xx,y+23)],14)
   self.poly([(xx-3,y+26),(xx+4,y+26),(xx+2,y+31),(xx-3,y+30)],2);self.line([(xx-3,y+26),(xx+3,y+26)],6)
  self.d.ellipse((x+w-3,y+15,x+w+9,y+32),outline=self.p[14],width=2);self.d.ellipse((x+w,y+18,x+w+6,y+29),outline=self.p[13]);self.line([(x+w+7,y+28),(x+w+11,y+38)],14)
 def save(self,name):self.im.save(ROOT/name)

def sprite(k,view):
 a=Art(k,32,32,True)
 # Tapered shoulders, asymmetrical satchel, short adolescent build.
 a.poly([(12,3),(19,3),(22,6),(21,11),(19,13),(12,12),(10,8)],15)
 a.poly([(12,4),(18,4),(21,6),(20,8),(17,7),(15,9),(11,8)],16)
 if view!='back':
  a.poly([(12,8),(20,8),(20,12),(18,14),(13,13)],19);a.rect((13,8,19,11),20)
  if view=='front':
   a.dot(14,10,0);a.dot(18,10,0);a.dot(16,12,19);a.line([(13,7),(15,7)],15)
  else:a.dot(19,9,0);a.rect((20,10,21,11),20)
 else:a.rect((12,7,20,11),15);a.line([(12,5),(16,4),(19,5)],16)
 a.poly([(11,14),(19,14),(23,18),(22,23),(10,23),(8,18)],17)
 a.poly([(11,14),(16,14),(16,21),(10,21),(10,17)],18)
 a.line([(12,15),(14,16),(14,19)],21)
 a.rect((9,18,11,22),18);a.rect((21,18,23,22),17)
 a.rect((9,22,11,24),20);a.rect((21,22,23,24),19)
 a.poly([(12,23),(16,23),(15,28),(11,28)],2);a.poly([(18,23),(21,23),(22,28),(18,28)],1)
 a.rect((10,28,15,29),0);a.rect((18,28,23,29),0);a.dot(11,28,14);a.dot(19,28,14)
 a.line([(11,14),(20,22)],15,2);a.line([(12,14),(21,22)],14)
 a.rect((19,21,25,26),15);a.rect((20,21,24,24),16);a.line([(20,21),(24,21)],14);a.dot(22,24,21)
 if view=='side':
  a.rect((8,15,10,21),17);a.rect((11,24,12,27),17)
 if view=='back':a.line([(13,16),(18,20)],18);a.rect((14,12,18,13),21)
 return a.im

def scene(k):
 a=Art(k);a.water()
 # Construct a full textured raised yard, then mask its silhouette over water.
 ground=Art(k);ground.stone((0,0,383,319));
 if k==0:
  boundary=[(0,0),(383,0),(383,129),(346,153),(322,190),(281,213),(237,231),(193,238),(140,239),(93,248),(0,245)]
  edge=[(0,245),(93,248),(140,239),(193,238),(237,231),(281,213),(322,190),(346,153),(383,129)];slip=[(260,165),(299,155),(374,279),(325,299)]
 elif k==1:
  boundary=[(0,0),(383,0),(383,219),(344,218),(295,197),(246,176),(197,161),(145,146),(93,128),(42,110),(0,98)]
  edge=[(0,98),(42,110),(93,128),(145,146),(197,161),(246,176),(295,197),(344,218),(383,219)];slip=[(132,116),(184,133),(92,274),(26,252)]
 else:
  boundary=[(0,0),(383,0),(383,75),(344,108),(313,158),(278,193),(237,206),(195,214),(143,221),(93,227),(0,223)]
  edge=[(0,223),(93,227),(143,221),(195,214),(237,206),(278,193),(313,158),(344,108),(383,75)];slip=[(258,156),(288,132),(375,271),(327,297)]
 mask=Image.new('L',(384,320));ImageDraw.Draw(mask).polygon(boundary,fill=255);a.im.paste(ground.im,(0,0),mask);a.d=ImageDraw.Draw(a.im)
 # Cliff face follows the irregular bank; low water exposes several masonry courses.
 wall=Art(k);wall.stone((0,0,383,319),True,True)
 wm=Image.new('L',(384,320));wd=ImageDraw.Draw(wm);wd.polygon(edge+[(x,y+36) for x,y in reversed(edge)],fill=255);a.im.paste(wall.im,(0,0),wm);a.d=ImageDraw.Draw(a.im)
 a.line(edge,5,3);a.line([(x,y+34) for x,y in edge],2,3)
 for j in range(len(edge)-1):
  x,y=edge[j];X,Y=edge[j+1]
  for t in range(0,100,9):
   xx=int(x+(X-x)*t/100);yy=int(y+(Y-y)*t/100)+36
   a.line([(xx,yy),(xx+5,yy+1),(xx+8,yy)],6 if t%2 else 9)
   if t%3==0:a.weed(xx,yy-3,4)
 # Slipway: independently textured diagonal black-rock plane.
 basalt=Art(k);basalt.stone((0,0,383,319),True)
 sm=Image.new('L',(384,320));ImageDraw.Draw(sm).polygon(slip,fill=255);a.im.paste(basalt.im,(0,0),sm);a.d=ImageDraw.Draw(a.im)
 a.line([slip[0],slip[3]],3,2);a.line([slip[1],slip[2]],5,1)
 for t in range(1,9):
  p=t/10;x=int(slip[0][0]*(1-p)+slip[3][0]*p);y=int(slip[0][1]*(1-p)+slip[3][1]*p)
  a.weed(x+5,y,7);a.line([(x+13,y+2),(x+24,y+3)],9)
 if k==0:
  a.poly([(31,105),(112,105),(146,139),(61,139)],1)
  a.poly([(175,85),(300,85),(320,109),(192,109)],1)
  a.shed(30,38,83,76);a.lean(170,29,130);a.rack(181,104,58);hero=(151,160)
 elif k==1:
  a.poly([(267,96),(355,96),(323,119),(234,120)],3)
  a.poly([(113,71),(238,71),(219,89),(93,89)],3)
  a.shed(267,24,86,77);a.lean(112,12,126);a.rack(236,112,55);hero=(203,137)
 else:
  a.shed(23,31,83,76);a.lean(28,122,131);a.rack(177,60,57);hero=(182,157)
 # Yard clutter: coils, chipped bucket, discarded planks; local wear, not noise.
 for x,y in ([(57,151),(285,112)] if k==0 else [(287,159),(57,67)] if k==1 else [(116,107),(211,117)]):
  a.d.ellipse((x,y,x+17,y+8),outline=a.p[14],width=2);a.d.ellipse((x+4,y+2,x+13,y+6),outline=a.p[13]);a.line([(x+14,y+5),(x+25,y+10),(x+29,y+9)],14)
  a.poly([(x-18,y-3),(x-7,y-3),(x-9,y+9),(x-16,y+9)],2);a.line([(x-18,y-3),(x-7,y-3)],5)
 if k==2:
  # Pool is stepped opaque palette clusters, never an alpha blur.
  # Recolour only existing stone clusters in a stepped ellipse; retain joints.
  rgb={tuple(int(c[i:i+2],16) for i in (1,3,5)):n for n,c in enumerate(a.p)}
  for yy in range(157,204):
   for xx in range(145,223):
    distance=((xx-181)/39)**2+((yy-181)/23)**2
    idx=rgb.get(a.im.getpixel((xx,yy)))
    if distance<1 and idx in (2,3,4):
     if distance<.6 or (xx+yy)%4==0:a.dot(xx,yy, {2:3,3:4,4:14}[idx])
  a.line([(125,142),(125,126),(132,126)],0,2);a.rect((129,128,136,137),22);a.rect((131,129,134,134),23);a.line([(128,138),(137,138)],12)
  for x,y in [(179,258),(204,277),(229,292)]:a.line([(x,y),(x+13,y)],14)
 # Ground shadow + hero. Position deliberately avoids props.
 hx,hy=hero;a.d.ellipse((hx+6,hy+26,hx+29,hy+31),fill=a.p[1]);a.im.paste(sprite(k,'front'),hero,sprite(k,'front'))
 # Edge-weight varies by direction; coloured rim never a universal black stroke.
 return a

def tile(k,n):
 a=Art(k,32,32);a.rect((0,0,31,31),3)
 if n<3:a.stone((0,0,31,31),n==1,n==2)
 elif n==3:a.stone((0,0,31,31),True);a.weed(13,24,18);a.line([(21,24),(28,24)],9)
 elif n in (4,5):
  a.water()
  if n==5:
   a.poly([(0,0),(13,0),(8,12),(2,19),(0,26)],2);a.line([(14,0),(11,8),(9,11),(9,15),(4,19),(3,23),(0,27)],6,2)
 elif n==6:a.wood((0,0,31,31));a.d.ellipse((8,11,19,16),outline=a.p[12]);a.line([(11,13),(16,13)],14);a.dot(3,3,0);a.dot(28,27,0)
 elif n==7:a.rect((0,0,31,31),1);a.rack(-4,1,28)
 else:
  a.wood((0,0,31,31),True);a.line([(0,28),(31,9)],14,2);a.rect((24,14,27,17),2);a.dot(25,14,6)
 return a.im

def luminance(h):
 vals=[int(h[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in vals];return sum(x*y for x,y in zip(v,[.2126,.7152,.0722]))
def contrast(a,b):
 x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)

def build():
 audit={}
 for k,key in enumerate('abc'):
  stem=f'option-{key}2';s=scene(k);s.save(stem+'-scene.png')
  ts=Image.new('RGB',(288,32));
  for n in range(9):
   t=tile(k,n);t.save(ROOT/f'{stem}-tile-{n}.png');ts.paste(t,(n*32,0))
  ts.save(ROOT/(stem+'-tiles.png'))
  bs=Image.new('RGBA',(96,32))
  for n,v in enumerate(['front','back','side']):
   b=sprite(k,v);b.save(ROOT/f'{stem}-bryn-{v}.png');bs.paste(b,(n*32,0))
  bs.save(ROOT/(stem+'-bryn.png'))
  fid=Art(k,32,32,True);fid.poly([(9,25),(11,17),(21,6),(24,4),(25,7),(19,17),(13,25)],15);fid.poly([(10,24),(12,17),(23,5),(23,9),(17,19),(12,24)],21);fid.line([(12,21),(20,10)],5);fid.dot(12,23,0);fid.save(stem+'-bone-fid.png')
  # Readability is dual-edge contrast: a light face/linen edge and dark silhouette.
  grounds={name:idx for name,idx in [('dry',4),('wet',2),('wall',3),('weed',10),('water',8),('wood',13),('lit stone',5)]}
  checks={name:{'light_edge':round(contrast(PALETTES[k][21],PALETTES[k][idx]),2),'dark_edge':round(contrast(PALETTES[k][0],PALETTES[k][idx]),2)} for name,idx in grounds.items()}
  audit[key]={'palette':dict(zip(ROLES,PALETTES[k])),'grounds':checks,'method':'Local luminance contrast for both silhouette extremes; at least one edge exceeds 3:1 on each ground. This is an art legibility aid, not a text WCAG claim.'}
  palette=''.join(f'<div class="swatch"><i style="background:{c}"></i><code>{c}</code><span>{r}</span></div>' for c,r in zip(PALETTES[k],ROLES))
  tiles=''.join(f'<figure><img width="96" height="96" src="{stem}-tile-{n}.png" alt="{name} tile"><figcaption>{n+1:02} · {name}</figcaption></figure>' for n,name in enumerate(NAMES))
  sprites=''.join(f'<figure><img width="128" height="128" src="{stem}-bryn-{v}.png" alt="Bryn {v} view"><figcaption>{v.title()} · 4×</figcaption></figure>' for v in ['front','back','side'])
  rows=''.join(f'<tr><td>{name}</td><td>{v["light_edge"]}:1</td><td>{v["dark_edge"]}:1</td><td>{"PASS" if max(v.values())>=3 else "REVIEW"}</td></tr>' for name,v in checks.items())
  html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLES[k]} — The Mending Shift</title><style>{CSS}</style><body><nav><a href="index-v2.html">← Round 2 / three directions</a><a href="option-{key}.html">Round 1 {key.upper()}</a></nav><header><div class="eyebrow">THE MENDING SHIFT / VISUAL DEVELOPMENT / ROUND 02 / MOCKUP</div><h1>{TITLES[k]}</h1><p>{DESCS[k]}</p><div class="meta">Sallowquay Boat-yard · Bryn Aukett, 15 · Kit-runner · Native tile 32 × 32</div></header><main><section><h2>01 / The yard <small>12 × 10 tiles</small></h2><div class="viewport"><img src="{stem}-scene.png" width="768" height="640" alt="{TITLES[k]} Sallowquay yard, enlarged twice"></div><p class="caption">2× / 768 × 640 · fixed integer scale, scroll on smaller screens</p><details open><summary>Native 1× / 384 × 320</summary><div class="viewport"><img src="{stem}-scene.png" width="384" height="320" alt="Native resolution yard scene"></div></details></section><section><h2>02 / Material vocabulary <small>nine 32 × 32 tiles at 3×</small></h2><div class="tiles">{tiles}</div><p class="caption">Standalone material studies. The scene uses bespoke prop silhouettes and irregular masonry, rather than repeating a single ground tile.</p></section><section><h2>03 / Bryn Aukett <small>32 × 32 per view</small></h2><div class="sprites">{sprites}<figure><img width="128" height="128" src="{stem}-bone-fid.png" alt="Carved bone fid"><figcaption>Bone fid · 4×</figcaption></figure></div><p>Rust-brown cropped hair, blue work jacket, linen collar, split trouser silhouette, bare hands and a leather satchel with a diagonal strap. Transparent sprite backgrounds; eyes are single pixels.</p></section><section><h2>04 / Working palette <small>24 colours · no blended pixels</small></h2><div class="palette">{palette}</div></section><section><h2>05 / Ground readability</h2><p>Both bright linen and the deep silhouette were compared with each ground. One edge clears 3:1 on every listed surface; the face, jacket and satchel add internal separation. These figures assess edge contrast, not complete perceptual visibility.</p><table><tr><th>Ground</th><th>Linen edge</th><th>Dark edge</th><th>≥ 3:1 edge</th></tr>{rows}</table></section></main><footer>MOCKUP · Original code-drawn pixel art · Fixed seeds · Upper {"right" if k==1 else "left"} light{ " + local work lamp" if k==2 else ""} · <a href="generate_pixel_art_v2.py">Reproducible generator</a></footer></body></html>'''
  (ROOT/(stem+'.html')).write_text(html)
 (ROOT/'palette-readability-v2.json').write_text(json.dumps(audit,indent=2))
 cards=''.join(f'<article><a href="option-{key}2.html"><img src="option-{key}2-scene.png" width="384" height="320" alt="{TITLES[k]}"><h2>{TITLES[k]}</h2></a><p>{DESCS[k]}</p><a href="option-{key}2.html">Open full board →</a> · <a href="option-{key}.html">Round 1</a></article>' for k,key in enumerate('abc'))
 (ROOT/'index-v2.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Mending Shift — Round 2</title><style>{CSS} .cards{{display:flex;flex-wrap:wrap;gap:32px}}article{{width:384px}}article p{{font-size:14px}}article img{{border:1px solid #6b716e}}</style><body><header><div class="eyebrow">ORIGINAL PIXEL ART / ROUND 02 / MOCKUP</div><h1>The Mending Shift</h1><p>One working tidal yard. Three different ways to see it.</p><p class="meta">384 × 320 scenes · 32 × 32 tiles and sprites · integer scaling · code drawn</p></header><main><div class="cards">{cards}</div></main><footer><a href="index.html">Round 1 comparison</a> · <a href="generate_pixel_art_v2.py">Generator source</a> · <a href="palette-readability-v2.json">Palette contrast data</a></footer></body></html>')
 print('Generated three boards, overview, scenes, nine tiles per option, turnarounds and palette data.')
CSS='''*{box-sizing:border-box}body{margin:0;background:#161e25;color:#e4dfce;font:15px/1.6 system-ui,sans-serif}nav{display:flex;justify-content:space-between;padding:20px 5vw;border-bottom:1px solid #45505a}a{color:#d4c095;text-underline-offset:4px}header,main,footer{max-width:1440px;margin:auto;padding:32px 5vw}header{padding-top:55px}h1{font:500 clamp(36px,5vw,68px)/1.05 Georgia,serif;margin:20px 0}p{max-width:78ch;color:#bcc4c4}.eyebrow,.meta,.caption,figcaption,code{font:12px/1.6 ui-monospace,monospace}.eyebrow{letter-spacing:.13em;color:#d4c095}section{border-top:1px solid #45505a;padding:24px 0 34px}h2{font-size:19px;font-weight:500}h2 small{font:12px ui-monospace,monospace;color:#a5b1b4;margin-left:16px}.viewport{overflow:auto;padding:16px;background:#10171d;width:max-content;max-width:100%}img{display:block;image-rendering:pixelated;image-rendering:crisp-edges;flex-shrink:0}details{margin-top:20px}summary{cursor:pointer;margin-bottom:12px}.tiles,.sprites{display:flex;flex-wrap:wrap;gap:20px}figure{margin:0}figure img{background:repeating-conic-gradient(#303c46 0% 25%,#28333c 0% 50%) 0 0/16px 16px}figcaption{margin-top:8px;color:#c1c9c7}.palette{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px}.swatch i{display:block;height:40px;margin-bottom:5px}.swatch span{display:block;font-size:12px;color:#bbc4c4}.swatch code{color:#e4dfce}table{border-collapse:collapse;font:13px ui-monospace,monospace}td,th{text-align:left;padding:9px 20px 9px 0;border-bottom:1px solid #45505a}footer{border-top:1px solid #45505a;font-size:12px;color:#a6b1b6}'''
if __name__=='__main__':build()
