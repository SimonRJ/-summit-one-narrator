"""T13.3. Disassemble solids and carry the same cubes into their paint classes."""
from collections import Counter
from itertools import product
from math import cos, radians, sin
from captioned_film import cue, mix

ID = 'T13.3'
ORIGINAL = '7fead578dafd3ef1c535d44deafad9cbcebe6d32538c5b632b64673351759d55'
START = (0.,12.44,21.89,34.99,46.67,66.66,84.26,97.38)
POSTER = 76.95
PAPER = '#132432'
WHITE, SUB, LINE = '#f3f2de','#a4c4cb','#173443'
SEA = ('#9be4dc','#4ca8b2','#337b93')
SUN = ('#f6ca74','#d19b4f','#b17b41')
RIND = ('#f1a888','#d27b64','#ae6456')
INNER = ('#c4e9a7','#82bc8b','#619a82')
GROUP = (INNER,SEA,SUN,RIND)
BLOCK = tuple(product(range(4),range(3),range(2)))
CUBE = tuple(product(range(3),repeat=3))
STAIR = tuple((x,y,z) for z in range(3) for x in range(3-z) for y in range(3-z))
def title(c,s):c.text(s,60,51,40,WHITE,'lm',True)
def note(c,s,x,y,sz=27,ink=SUB):c.text(s,x,y,sz,ink,'lm',True)
def faces(p,n):return sum(k in (0,n-1) for k in p)
def basis(angle=40):
    a,e=radians(angle),radians(26)
    return (cos(a), sin(a)*sin(e)), (-sin(a),cos(a)*sin(e)), (0,-cos(e))
def projected(p,d,origin,u,axes):
    v=[v-(n-1)/2 for v,n in zip(p,d)]
    return tuple(origin[i]+u*sum(q*b[i] for q,b in zip(v,axes)) for i in range(2))
def glyph(c,at,u,axes,colour,paint=None):
    x,y=at
    def v(a,b,d):return (x+u*(a*axes[0][0]+b*axes[1][0]+d*axes[2][0]),y+u*(a*axes[0][1]+b*axes[1][1]+d*axes[2][1]))
    corners=(((-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)),
             ((.5,-.5,-.5),(.5,.5,-.5),(.5,.5,.5),(.5,-.5,.5)),
             ((-.5,.5,-.5),(-.5,.5,.5),(.5,.5,.5),(.5,.5,-.5)))
    for i in (1,2,0):
        tone=colour[i] if paint is None or paint[i] else INNER[i]
        c.poly([v(*pt) for pt in corners[i]],tone,LINE,2)
def solid(c,cells,d,origin,u,*,angle=40,gap=0,spread=0,colour=None,paint=False):
    axes=basis(angle)
    for p in sorted(cells,key=lambda p:(sum(p),p[2],p[1])):
        x,y=projected(p,d,origin,u,axes)
        x+=(x-origin[0])*spread
        y+=(y-origin[1])*spread-((p[2]-(d[2]-1)/2)*gap)
        tone=colour(p) if colour else (SEA if p[2]%2 else SUN)
        glyph(c,(x,y),u,axes,tone, (p[2]==d[2]-1,p[0]==d[0]-1,p[1]==d[1]-1) if paint else None)
def plan(c,ox,oy,w,h,p,colour):
    for j in range(h):
        for i in range(w):
            k=j*w+i
            c.rect(ox+i*37,oy+j*37,34,34,colour if k+.5<=p else '#263e4a','#65828a',1)
def intro(c,t):
    title(c,'What is hiding inside the block?')
    angle=36+10*cue(t,1,4)
    layer=cue(t,6.4,2.8)
    solid(c,BLOCK,(4,3,2),(407,343),74,angle=angle,gap=108*layer)
    if t>=4:note(c,'One corner view',828,280)
    if t>=6.4:note(c,'Lift the top layer',828,335,31,SEA[0])
    if t>=9.6:
        plan(c,830,383,4,3,12*cue(t,9.6,1.5),SUN[0])
        note(c,'× 2 layers',1005,437,26,WHITE)
def visible(c,t):
    title(c,'A view from one corner hides six cubes')
    f=cue(t,15.4,2.7)
    visible=lambda p:p[0]==3 or p[1]==2 or p[2]==1
    solid(c,BLOCK,(4,3,2),(403,340),75,gap=133*f,spread=.12*f,colour=lambda p:SEA if visible(p) else RIND)
    note(c,'18 touch a visible face',790,241,32,SEA[0])
    if t>=15.4:
        note(c,'6 sit behind them',790,321,32,RIND[0])
        plan(c,790,370,3,2,6*f,RIND[0])
    if t>=19.1:note(c,'18 + 6 = 24',790,511,30,WHITE)
def puzzle(c,t):
    title(c,'How many unit cubes fit in this block?')
    # The three dimension arrows follow the same projected edges as the cubes.
    o=(505,336);a=basis();u=75;d=(4,3,2)
    solid(c,BLOCK,d,o,u)
    for start,end,label,when,offset in [((-.5,2.5,-.5),(3.5,2.5,-.5),'4 long',22.6,(-16,35)),((3.5,-.5,-.5),(3.5,2.5,-.5),'3 wide',24.2,(36,32)),((3.5,-.5,-.5),(3.5,-.5,1.5),'2 high',25.6,(36,-5))]:
        if t<when:continue
        p=projected(start,d,o,u,a);q=projected(end,d,o,u,a)
        off=[(x+offset[0],y+offset[1]) for x,y in (p,q)]
        c.line(off,WHITE,2)
        for x,y in off:c.dot(x,y,4,WHITE)
        x=(off[0][0]+off[1][0])/2;y=(off[0][1]+off[1][1])/2
        c.text(label,x+(48 if label=='2 high' else 0),y+(23 if label!='2 high' else 0),23,WHITE,'mm',True)
    if t>=29.8:note(c,'Picture one layer.',870,331,31,SUN[0])
def layers(c,t):
    title(c,'Give each cube a place in a layer')
    f=cue(t,35,2);solid(c,BLOCK,(4,3,2),(387,333),71,gap=124*f)
    plan(c,801,156,4,3,12*cue(t,35,2.4),SEA[0])
    if t>=37.4:note(c,'4 × 3 = 12',968,210,27,SEA[0])
    if t>=38.6:
        plan(c,801,340,4,3,12*cue(t,38.6,1.8),SUN[0])
        if t>=40:note(c,'12 + 12 = 24',968,394,27,SUN[0])
    if t>=42.2:note(c,'12 in the bottom layer',775,531,29,WHITE)
def peel(c,t):
    title(c,'Which cube never met the paint?')
    f=cue(t,51.8,1.8);peel=cue(t,59.8,2.75)
    cells=[p for p in CUBE if not peel or faces(p,3)==0 or peel<.97]
    axes=basis(38+7*cue(t,48.6,2.5));origin=(420,335);u=72
    for p in sorted(cells,key=lambda p:(sum(p),p[2],p[1])):
        centre=projected(p,(3,3,3),origin,u,axes)
        distance=1+.13*f+1.18*peel
        at=tuple(origin[i]+(centre[i]-origin[i])*distance for i in range(2))
        if faces(p,3)>0:at=(at[0]+(103 if sum(p)>=3 else -103)*peel,at[1])
        glyph(c,at,u*(1-.46*peel if faces(p,3)>0 else 1),axes,RIND if t>=48.6 else SEA,
              (p[2]==2,p[0]==2,p[1]==2) if t>=48.6 else None)
    if t>=51.8:note(c,'3 × 3 × 3 = 27',829,216,31,WHITE)
    if t>=57:note(c,'Outside faces carry paint.',829,310,25,RIND[0])
    if t>=62.2:note(c,'One unpainted centre',795,425,33,INNER[0])
def classes(c,t):
    title(c,'Sort the same 27 cubes by painted faces')
    starts={3:69.,2:72.,1:74.6,0:77.2}
    slots={3:(576,173,4),2:(932,173,4),1:(576,398,3),0:(932,398,1)}
    labels={3:'3 faces · corners',2:'2 faces · edges',1:'1 face · face centres',0:'0 faces · inside'}
    groups={k:sorted((p for p in CUBE if faces(p,3)==k),key=lambda p:(sum(p),p)) for k in slots}
    for k,(xx,yy,cols) in slots.items():
        c.line([(xx-22,yy-48),(xx+230,yy-48)],GROUP[k][0],3)
        note(c,labels[k],xx-20,yy-74,22,GROUP[k][0])
    a=basis();items=[]
    for k,pts in groups.items():
        xx,yy,cols=slots[k]
        for j,p in enumerate(pts):
            f=cue(t,starts[k]+j*.045,.85);old=projected(p,(3,3,3),(251,320),56,a)
            dest=(xx+(j%cols)*47,yy+(j//cols)*43)
            at=tuple(mix(old[i],dest[i],f) for i in range(2))
            visible=(p[2]==2,p[0]==2,p[1]==2) if f<.55 else tuple(i<k for i in range(3))
            items.append((sum(p)+10*f,at,mix(56,26,f),GROUP[k] if f else RIND,visible))
    for _,at,s,tone,visible in sorted(items,key=lambda row:row[0]):glyph(c,at,s,a,tone,visible)
    note(c,'Pale green faces carry no paint.',705,548,22,INNER[0])
    if t>=78.8:note(c,'8 + 12 + 6 + 1 = 27',55,540,37,WHITE)
def stair(c,t):
    title(c,'A staircase has three different footprints')
    solid(c,STAIR,(3,3,3),(390,332),70,gap=59*cue(t,85.2,2.5),colour=lambda p:(SUN,SEA,INNER)[p[2]])
    for i,(w,when,col) in enumerate(((3,87.2,SUN),(2,90.6,SEA),(1,92.,INNER))):
        if t<when:continue
        x=725+i*171
        plan(c,x,260,w,w,w*w*cue(t,when,1.1),col[0])
        note(c,str(w*w),x+9,425,34,col[0])
    if t>=93.3:note(c,'9 + 4 + 1 = 14',732,508,36,WHITE)
def challenge(c,t):
    if t<105.8:
        title(c,'Count one real layer at a time')
        f=cue(t,97.5,2)
        solid(c,STAIR,(3,3,3),(428,335),72,gap=68*f,colour=lambda p:(SUN,SEA,INNER)[p[2]])
        if t>=99.6:note(c,'9 underneath',822,238,29,SUN[0])
        if t>=101.2:note(c,'4 above and 1 on top',822,310,29,SEA[0])
        if t>=103:note(c,'14 altogether',822,395,33,WHITE)
        return
    title(c,'Your turn · paint a 4 × 4 × 4 cube')
    cells=tuple(product(range(4),repeat=3))
    f=cue(t,114.5,2.5)
    chosen=[p for p in cells if not f or faces(p,4)==0]
    if f and f<.85:
        shell=[p for p in cells if faces(p,4)>0]
        # Lift the entire shell away as a unit, then leave its cross-section on the right.
        solid(c,shell,(4,4,4),(390-310*f,334-70*f),53*(1-.64*f),colour=lambda p:RIND,paint=True)
    solid(c,chosen,(4,4,4),(390,335),53,colour=lambda p:RIND,paint=True)
    if t>=111.8:note(c,'Which cubes have no paint?',743,260,30,WHITE)
    if t>=116.7:note(c,'2 × 2 × 2 = 8',780,394,39,INNER[0])
SCENES=(intro,visible,puzzle,layers,peel,classes,stair,challenge)
def verify():
    assert len(BLOCK)==24 and sum(x==3 or y==2 or z==1 for x,y,z in BLOCK)==18
    assert len({p for p in BLOCK if p[0]<3 and p[1]<2 and p[2]==0})==6
    assert Counter(faces(p,3) for p in CUBE)=={3:8,2:12,1:6,0:1}
    assert Counter(z for x,y,z in STAIR)=={0:9,1:4,2:1}
    assert sum(faces(p,4)==0 for p in product(range(4),repeat=3))==8
