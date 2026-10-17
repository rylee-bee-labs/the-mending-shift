"""Bryn-only revision. Run python3 generate_pixel_art_v4.py.
Writes only option-anchor4-bryn*.png. Never invokes either earlier build().
Sheet: 96x64, front/back/side columns, idle/contact rows. Preview: six cells at 2x.
All drawing uses the unchanged A2 palette and integer coordinates.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from generate_pixel_art_v2 import Art, PALETTES
from generate_pixel_art_v3 import bryn as prior_bryn
ROOT=Path(__file__).resolve().parent

def bryn(view,walk=False):
 a=Art(0,32,32,True)
 dy=int(walk)
 def rect(b,c):a.rect((b[0],b[1]+dy,b[2],b[3]+dy),c)
 def poly(p,c):a.poly([(x,y+dy) for x,y in p],c)
 def line(p,c,w=1):a.line([(x,y+dy) for x,y in p],c,w)
 # Legs are drawn behind the torso. The two boots contact at distinct depths.
 if view=='side':
  if walk:
   poly([(14,22),(17,22),(14,26),(11,28),(9,28),(12,24)],1)
   rect((8,28,13,29),0)
   poly([(17,22),(20,22),(21,25),(23,28),(20,28),(17,25)],2)
   rect((20,28,25,29),0);rect((23,28,24,28),14)
  else:
   rect((14,23,16,27),1);rect((14,28,18,29),0)
   rect((17,23,19,28),2);rect((17,28,22,29),0)
  # Seven-pixel torso versus fourteen-pixel frontal shoulders.
  poly([(14,14),(18,14),(20,17),(20,23),(14,23),(13,18)],17)
  line([(14,15),(14,21)],18)
  # Far arm counter-swings toward the rear when near leg advances right.
  if walk:
   poly([(15,15),(17,16),(21,20),(23,20),(23,22),(20,22),(15,19)],17)
   rect((22,20,24,21),19)
  line([(16,14),(18,22)],15,2);line([(16,15),(18,21)],14)
  # Narrow side gusset; no broad frontal flap.
  rect((18,21,21,26),15);rect((19,22,20,25),16);line([(19,22),(19,24)],14)
  if walk:
   poly([(16,15),(18,16),(17,19),(13,22),(11,21),(14,18)],18)
   rect((10,21,12,23),20)
  else:
   poly([(16,15),(18,16),(18,20),(17,22),(15,21),(15,17)],18)
   rect((15,22,17,24),20)
 else:
  if walk:
   # Three-pixel depth difference, open gap and opposite arm swing.
   poly([(12,22),(16,23),(15,26),(13,29),(10,29),(11,26)],2)
   rect((9,29,14,30),0);rect((10,29,11,29),14)
   poly([(18,22),(21,22),(22,25),(22,26),(18,26)],1)
   rect((18,26,23,27),0);rect((19,26,20,26),14)
  else:
   rect((12,23,15,27),2);rect((18,23,21,27),1)
   rect((10,28,15,29),0);rect((18,28,23,29),0)
   rect((11,28,12,28),14);rect((19,28,20,28),14)
  poly([(11,14),(19,14),(23,17),(22,23),(10,23),(8,17)],17)
  poly([(11,14),(16,14),(16,22),(10,22),(10,17)],18)
  if view=='back':
   # Jacket back is uninterrupted except for shoulder seam and crossing strap.
   line([(11,16),(19,16)],17);line([(15,18),(15,21)],17)
   line([(20,14),(11,23)],15,2);line([(19,14),(10,23)],14)
   rect((7,22,10,26),15);rect((8,23,9,26),16)
  else:
   line([(12,15),(14,16),(14,18)],21)
   line([(11,14),(21,23)],15,2);line([(12,14),(22,23)],14)
   rect((20,22,25,26),15);rect((21,22,24,24),16);line([(21,22),(24,22)],14);rect((22,24,22,24),21)
  if walk:
   # Left arm recedes; right arm advances against left advancing leg.
   poly([(9,16),(11,17),(10,20),(8,21),(7,19)],17);rect((7,20,9,22),19)
   poly([(21,16),(23,17),(25,22),(24,24),(22,22)],18);rect((23,24,25,26),20)
  else:
   rect((9,18,11,22),18);rect((21,18,23,22),17)
   rect((9,22,11,24),20);rect((21,22,23,24),19)
 # Front/back cap and hair copied exactly from approved idle pixels.
 head=prior_bryn(view).crop((0,0,32,14))
 if view!='side':a.im.paste(head,(0,dy),head)
 else:
  # Right-facing head profile: brim and nose both project right, one eye.
  poly([(13,4),(16,2),(19,3),(21,5),(20,8),(12,8),(11,6)],0)
  poly([(13,4),(16,3),(19,4),(20,6),(19,7),(12,7)],16)
  line([(13,5),(18,5)],22);rect((11,7,22,8),12);line([(12,7),(23,7)],14)
  for x in (13,16,19):rect((x,6,x,6),14)
  rect((10,4,12,6),16);rect((10,4,10,4),14)
  rect((13,9,15,11),15)
  poly([(16,9),(20,9),(20,10),(22,10),(22,11),(20,11),(20,12),(18,13),(16,12)],20)
  rect((19,9,19,9),0);rect((16,11,16,11),19)
 return a.im

def build():
 sheet=Image.new('RGBA',(96,64));strip=Image.new('RGBA',(192,32))
 for row,walk in enumerate((False,True)):
  for col,view in enumerate(('front','back','side')):
   im=bryn(view,walk);suffix='-walk' if walk else ''
   im.save(ROOT/f'option-anchor4-bryn-{view}{suffix}.png')
   sheet.paste(im,(32*col,32*row));strip.paste(im,(32*(row*3+col),0))
 sheet.save(ROOT/'option-anchor4-bryn.png')
 strip.resize((384,64),Image.Resampling.NEAREST).save(ROOT/'option-anchor4-bryn-preview-2x.png')
 print('Saved six 32x32 frames, 96x64 sheet and 384x64 preview strip; terrain files untouched.')
if __name__=='__main__':build()
