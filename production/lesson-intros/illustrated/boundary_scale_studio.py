"""T13.2. Slide equal edges onto each other, compare a notch, then scale in two and three dimensions."""
from math import floor
from collections import Counter
from itertools import product
from captioned_film import cue,mix,font
from folding_box import Camera
ID='T13.2';ORIGINAL='03494bd8e053d32cbd9d125ddc093b431448eb0112f26da1e22a70047496a9b5'
START=(0,12.60,22.05,34.66,51.62,66.5,84.1,94.51);POSTER=48.71
PAPER='#efeee5';INK='#293a44';SOFT='#536771';TILE='#c7ded4';EDGE='#49796f';GRID='#94b6a8';REMOVE='#ad4b3c';NEW='#28609a';GOLD='#ebac70';LILAC='#c6badb';WHITE='#fff9e9'
def label(c,s,x,y,sz=30,col=INK,anchor='lm'):c.text(s,x,y,sz,col,anchor,True)
def title(c,s):
    sz=42
    while font(round(sz*c.scale),True).getlength(s)>1145*c.scale:sz-=1
    label(c,s,60,60,sz)
def edges(cells):
    counts=Counter()
    for i,j in cells:
        vertices=((i,j),(i+1,j),(i+1,j+1),(i,j+1))
        for k,a in enumerate(vertices):counts[tuple(sorted((a,vertices[(k+1)%4])))]+=1
    return {e for e,v in counts.items() if v==1}
ALL=set(product(range(5),range(3)));CORNER=(0,0);NOTCH=(2,0)
def view(c,cells,x,y,u):
    def pt(v):return (x+u*v[0],y+u*v[1])
    for i,j in sorted(cells):c.rect(x+i*u,y+j*u,u,u,TILE,GRID,1.2)
    for a,b in edges(cells):c.line([pt(a),pt(b)],EDGE,3)
    return pt
def unit(c,x,y,u,k=1):
    c.rect(x+1,y+1,u-2,u-2,'#f0d2b0',REMOVE,2)
    if k:label(c,'1',x+u/2,y+u/2,max(16,round(u*.45)),REMOVE,'mm')
def legend(c,x,y,col,s):
    c.line([(x,y),(x+48,y)],col,5);label(c,s,x+65,y,26,col)
def cut(c,omit,p,origin=(171,213),u=69):
    x,y=origin;cells=ALL if not p else ALL-{omit};pt=view(c,cells,x,y,u)
    q,r=pt(omit);unit(c,q+42*p,r-69*p,u)
    return pt
def highlight(c,pt,e,col,p=1):
    for a,b in sorted(e):
        aa=pt(a);bb=pt(b);c.line([aa,(mix(aa[0],bb[0],p),mix(aa[1],bb[1],p))],col,6)
def dimension(c,pt,width=5,height=3):
    x,y=pt((0,height));a,b=pt((width,height))
    c.line([(x,y+12),(x,y+21),(a,b+21),(a,b+12)],SOFT,2)
    label(c,str(width)+' units',.5*(x+a),y+49,24,SOFT,'mm')
    x,y=pt((width,0));a,b=pt((width,height))
    c.line([(x+10,y),(x+21,y),(a+21,b),(a+10,b)],SOFT,2);label(c,str(height),x+42,(y+b)/2,24,SOFT,'mm')
def intro(c,t):
    title(c,'One missing square can change the boundary in two different ways')
    p=cue(t,.65,2.2)
    for x,cell in ((136,CORNER),(741,NOTCH)):
        cut(c,cell,p,(x,245),56)
        if t>=3.5:label(c,'Corner' if cell==CORNER else 'Middle of a side',x+134,451,28,EDGE,'mm')
    if t>=8.0:label(c,'Each has lost exactly one unit square.',300,539,31,REMOVE)
def uses(c,t):
    title(c,'What is the question measuring?')
    cells=set(product(range(4),range(2)));pt=view(c,cells,139,236,63)
    if t<16.7:highlight(c,pt,edges(cells),NEW,cue(t,12.7,2.2))
    else:
        for x,y in cells:
            if x+4*y<8*cue(t,16.7,2.2):c.rect(140+x*63,237+y*63,61,61,GOLD,WHITE,1)
    label(c,'Walk the edge',675,227,34,NEW)
    if t>=16.7:label(c,'Cover the region',675,343,34,REMOVE)
def question(c,t):
    title(c,'Cut 1 × 1 from the corner of a 5 × 3 rectangle')
    pt=cut(c,CORNER,cue(t,24.5,2.3));dimension(c,pt)
    if t>=26.5:label(c,'What is the new perimeter?',715,287,31,NEW)
    if t>=28.51:label(c,'Compare the two paths at the corner.',715,380,25)
def corner(c,t):
    title(c,'Slide each new edge onto the edge it replaced')
    pt=view(c,ALL-{CORNER},167,206,73)
    old=edges(ALL)-edges(ALL-{CORNER});new=edges(ALL-{CORNER})-edges(ALL)
    if t>=37.1:highlight(c,pt,old,REMOVE,cue(t,37.1,1.05))
    if t>=40.76:highlight(c,pt,new,NEW,cue(t,40.76,1.22))
    label(c,'Original boundary   16',754,166,30)
    if t>=37.1:legend(c,752,249,REMOVE,'Remove 2 unit edges')
    if t>=40.76:legend(c,752,321,NEW,'Expose 2 unit edges')
    if t>=45.02:label(c,'16 − 2 + 2 = 16',750,420,35,EDGE)
    if t>=47.3:
        p=cue(t,47.3,2.0)
        for a,b in new:
            dx,dy=(0,-p) if a[1]==b[1] else (-p,0)
            c.line([pt((a[0]+dx,a[1]+dy)),pt((b[0]+dx,b[1]+dy))],NEW,6)
        label(c,'Same lengths, same perimeter.',248,522,29,NEW)
def notch(c,t):
    title(c,'Cut the same unit square from the middle of the top side')
    pt=cut(c,NOTCH,cue(t,51.8,2.0))
    old=edges(ALL)-edges(ALL-{NOTCH});new=edges(ALL-{NOTCH})-edges(ALL)
    if t>=55.38:highlight(c,pt,old,REMOVE)
    if t>=57.5:highlight(c,pt,new,NEW,cue(t,57.5,1.45))
    if t>=55.38:legend(c,753,212,REMOVE,'Remove 1 unit edge')
    if t>=57.5:legend(c,753,288,NEW,'Expose 3 unit edges')
    if t>=59.76:label(c,'16 − 1 + 3 = 18',751,390,34,EDGE)
    if t>=62.64:label(c,'Both cutouts leave 14 square units.',257,520,29)
def scale2(c,t):
    title(c,'Double both side lengths on the same unit grid')
    x,y,u=133,181,57;factor=1+cue(t,69.24,2.9);w=3*factor;h=2*factor
    c.rect(x,y,w*u,h*u,TILE,EDGE,3)
    for i in range(1,6):
        if i<w:c.line([(x+i*u,y),(x+i*u,y+h*u)],GRID,1.5)
    for j in range(1,4):
        if j<h:c.line([(x,y+j*u),(x+w*u,y+j*u)],GRID,1.5)
    if t>=76.58:
        for n,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
            if t>=76.58+.65*n:
                c.rect(x+i*3*u+1,y+j*2*u+1,3*u-2,2*u-2,(TILE,'#d9d6eb','#eac9aa','#c4dce7')[n],EDGE,2)
                for a in (1,2):c.line([(x+(3*i+a)*u,y+2*j*u),(x+(3*i+a)*u,y+(2*j+2)*u)],GRID,1)
                c.line([(x+3*i*u,y+(2*j+1)*u),(x+(3*i+3)*u,y+(2*j+1)*u)],GRID,1)
    label(c,'2 × 3',771,201,34)
    if t>=72.1:label(c,'becomes 4 × 6',771,270,32,NEW)
    if t>=74.02:label(c,'Perimeter   10 → 20',771,368,30)
    if t>=76.58:label(c,'Area   6 → 24',771,453,32,EDGE)
    label(c,'1 square = 1 square unit',157,527,25,SOFT)
def cubefaces(c,n,progress,azimuth):
    cam=Camera(404,327,58,azimuth,29)
    items=[]
    for i,j,k in product(range(n),repeat=3):
        step=k*n*n+j*n+i
        amount=max(0,min(1,progress-step))
        if not amount:continue
        x=(i-(n-1)/2)*1.10;y=(j-(n-1)/2)*1.10;z=(k-(n-1)/2)*1.10+(1-amount)*1.25
        items.append((cam.depth((x,y,z)),x,y,z))
    for _,x,y,z in sorted(items):
        a=x-.5;b=y-.5;h=z-.5
        faces=(((a,b,h),(a+1,b,h),(a+1,b,h+1),(a,b,h+1)),((a+1,b,h),(a+1,b+1,h),(a+1,b+1,h+1),(a+1,b,h+1)),((a,b,h+1),(a+1,b,h+1),(a+1,b+1,h+1),(a,b+1,h+1)))
        for points,col in zip(faces,('#9ab6b2','#79a49e','#c9ded1')):c.poly([cam.project(p) for p in points],col,EDGE,2)
def solids(c,t):
    title(c,'Scale length, width and height')
    n=1 if t<87.2 else 2 if t<91.22 else 3
    count=1 if n==1 else 1+(n**3-1)*cue(t,87.21 if n==2 else 91.23,2.65 if n==2 else 2.05)
    # An array of unit cubes makes each dimension countable.
    cubefaces(c,n,count,31+16*cue(t,84.1,8.5));label(c,'Original   1 × 1 × 1 = 1',764,193,26)
    if t>=87.2:label(c,'Double   2 × 2 × 2 = 8',764,307,28,EDGE)
    if t>=91.22:label(c,'Triple   3 × 3 × 3 = 27',764,412,28,NEW)
def picture(c,x,y,u):
    c.rect(x,y,3*u,2*u,'#b9dbe0',INK,3)
    c.dot(x+2.34*u,y+.48*u,.21*u,'#edba66')
    c.poly([(x,y+1.69*u),(x+u*.94,y+.47*u),(x+1.8*u,y+1.53*u),(x+2.32*u,y+.95*u),(x+3*u,y+1.69*u),(x+3*u,y+1.97*u),(x,y+1.97*u)],'#6d9994',None)
    c.rect(x+1,y+1.78*u,3*u-2,.19*u,'#679198')
def finish(c,t):
    if t<105.45:
        title(c,'Cuts and enlargements use different measurements')
        pt=view(c,ALL-{NOTCH},157,231,58);highlight(c,pt,edges(ALL-{NOTCH})-edges(ALL),NEW)
        if t>=98.79:label(c,'Length   × k',765,208,32,NEW)
        if t>=102.13:label(c,'Area   × k²',765,302,32,EDGE);label(c,'Volume   × k³',765,394,32,REMOVE)
    else:
        title(c,'Enlarge every length of the photograph threefold')
        picture(c,136,334,35);s=1+2*cue(t,106.1,3.4);u=35*s
        picture(c,601,371-u,u)
        if t>=110.75:
            for i in (1,2):c.line([(601+i*u,371-u),(601+i*u,371+u)],WHITE,2.6)
            for j in (1,2):c.line([(601,371-u+2*j*u/3),(601+3*u,371-u+2*j*u/3)],WHITE,2.6)
            label(c,'How many original photos fit inside?',240,538,32,NEW)
SCENES=(intro,uses,question,corner,notch,scale2,solids,finish)
def verify():
    old=edges(ALL);assert len(old)==16
    for k,removed,added,total in ((CORNER,2,2,16),(NOTCH,1,3,18)):
        region=ALL-{k};new=edges(region);assert len(region)==14 and (len(old-new),len(new-old),len(new))==(removed,added,total)
    moved=set()
    for a,b in edges(ALL-{CORNER})-old:
        dx,dy=(0,-1) if a[1]==b[1] else (-1,0);moved.add(tuple(sorted(((a[0]+dx,a[1]+dy),(b[0]+dx,b[1]+dy)))))
    assert moved==old-edges(ALL-{CORNER})
    assert 2*(3+2)==10 and 2*(6+4)==20 and 24==4*(2*3)
    assert [len(list(product(range(n),repeat=3))) for n in (1,2,3)]==[1,8,27]
