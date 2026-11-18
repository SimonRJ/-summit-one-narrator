"""S061. Join rectangles, lift the actual corner triangle, then overlay two coloured sheets on a numbered board."""
from captioned_film import cue,mix
ID='S061'
ORIGINAL='28d893f341329fb94a252526c7ddc1e269a24f3c502034e7c3511f48eb10aea7'
START=(0,17.24,33.56,48.09,60.73,75.58,87.11,106.92,126.76,142.6,157.16)
POSTER=117.5
PAPER='#f7eedc';INK='#302f40';LIGHT='#78746a';LINE='#635e60';TEAL='#73bbb0';CORAL='#e9a278';BOTH='#ad91ae';BARE='#fffaf0';TEALINK='#276e65';REDINK='#95492f';PLUM='#684b72'
def heading(c,s):c.text(s,61,60,40,INK,'lm',True)
def note(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)
def patch(c,x,y,n,m,u,col):
    c.rect(x,y,n*u,m*u,col,LINE,2.5)
    for i in range(1,n):c.line([(x+i*u,y),(x+i*u,y+m*u)],'#8e8c81',1.3)
    for j in range(1,m):c.line([(x,y+j*u),(x+n*u,y+j*u)],'#8e8c81',1.3)
def measure(c,p,q,label,dx,dy):
    x,y=p;X,Y=q;a=(x+dx,y+dy);b=(X+dx,Y+dy)
    c.line([p,a,b,q],LINE,1.6)
    c.text(label,(a[0]+b[0])/2+dx*.79,(a[1]+b[1])/2+dy*.84,24,INK,bold=True)
def pair(c,p,labels=True):
    x,y,u=159,199,64
    patch(c,x,y,5,4,u,TEAL)
    bx=x+5*u+mix(112,0,p);by=y+u
    patch(c,bx,by,2,3,u,CORAL)
    if labels:
        measure(c,(x,y),(x+5*u,y),'5',0,-24)
        measure(c,(x,y),(x,y+4*u),'4',-23,0)
        measure(c,(bx,by+3*u),(bx+2*u,by+3*u),'2',0,22)
        measure(c,(bx+2*u,by),(bx+2*u,by+3*u),'3',22,0)
def cut(c,lift=0,guide=False,measures=True):
    x,y,u=154,163,41
    def at(p):return x+p[0]*u,y+p[1]*u
    rest=[(0,0),(6,0),(10,3),(10,8),(0,8)]
    c.poly([at(p) for p in rest],TEAL,LINE,3)
    # Grid segments are clipped to the exact 3:4 diagonal of the missing corner.
    for i in range(1,10):
        high=max(0,(i-6)*3/4)
        c.line([at((i,high)),at((i,8))],'#76a495',1.5)
    for j in range(1,8):
        end=min(10,6+j*4/3)
        c.line([at((0,j)),at((end,j))],'#76a495',1.5)
    if guide:
        c.line([at((6,0)),at((10,0)),at((10,3))],REDINK,2)
        c.line([at((6,0)),at((6,3)),at((10,3))],REDINK,2)
    tri=[at(p) for p in [(6,0),(10,0),(10,3)]]
    dx=74*lift;dy=-33*lift
    tri=[(a+dx,b+dy) for a,b in tri]
    c.poly(tri,CORAL,REDINK,2.5)
    v=tri[1]
    c.line([(v[0]-13,v[1]),(v[0]-13,v[1]+13),(v[0],v[1]+13)],REDINK,2.2)
    if measures:
        measure(c,at((0,8)),at((10,8)),'10',0,19)
        measure(c,at((0,0)),at((0,8)),'8',-22,0)
        measure(c,tri[0],tri[1],'4',0,-16)
        measure(c,tri[1],tri[2],'3',19,0)
FIRST={(x,y) for x in range(6) for y in range(5)}
SECOND={(x,y) for x in range(3,9) for y in range(2,8)}
FULL={(x,y) for x in range(9) for y in range(8)}
LOW={(x,y) for x in range(6,9) for y in range(2)}
HIGH={(x,y) for x in range(3) for y in range(5,8)}
def overlay(c,phase_a,phase_b,cross=False,focus=None):
    u=47;ox,oy=160,138
    for x,y in sorted(FULL):
        left=(x,y) in FIRST and y+1<=5*phase_a+.0001
        right=(x,y) in SECOND and x-2<=6*phase_b+.0001
        col=BOTH if left and right else TEAL if left else CORAL if right else BARE
        if focus:col=('#f5c86f' if (x,y) in focus else '#d7d2c5' if left or right else BARE)
        X=ox+x*u;Y=oy+(7-y)*u
        c.rect(X,Y,u,u,col,LINE,1)
        if cross and left and right:
            c.line([(X+3,Y+u-3),(X+u-3,Y+3)],PLUM,1.8)
            c.line([(X+u/2,Y+u-3),(X+u-3,Y+u/2)],PLUM,1.5)
    c.rect(ox,oy,9*u,8*u,None,LINE,3)
    for i in range(9):c.text(str(i+1),ox+(i+.5)*u,oy+8*u+24,19,INK,bold=True)
    for j in range(8):c.text(str(j+1),ox-22,oy+(7.5-j)*u,19,INK,bold=True)
    c.text('column',ox+4.5*u,oy+8*u+60,22,LIGHT);c.text('row',ox-64,oy+4*u,21,LIGHT)
def intro(c,t):
    heading(c,'What area does each piece cover?')
    if t<9.7:
        pair(c,1,False)
        if t>=4.2:
            y=262;p=cue(t,4.2,2.2)
            c.line([(479,y),(479,mix(y,455,p))],PLUM,5)
        note(c,'Count square units.',765,254,36,TEALINK)
        if t>=4.2:note(c,'Split along a useful line.',729,364,32)
    else:
        cut(c,cue(t,11.6,2.0),False,False)
        note(c,'Whole rectangle',733,248,34,TEALINK)
        if t>=12.3:note(c,'Lift the missing corner.',733,351,32,REDINK)
def uses(c,t):
    heading(c,'Count a region shared by two sheets')
    overlay(c,cue(t,17.6,1.7),cue(t,24.4,2.0),t>=28.8)
    note(c,'Start with the whole board.',700,215,32)
    if t>=24.5:note(c,'Lay one sheet over the other.',700,325,28,REDINK)
    if t>=28.8:note(c,'Their intersection counts once.',700,447,27,PLUM)
def join(c,t):
    heading(c,'How much do the two rectangles cover?')
    pair(c,cue(t,34.4,3.6))
    note(c,'5 × 4',771,236,45,TEALINK)
    if t>=35.6:note(c,'2 × 3',771,321,45,REDINK)
    if t>=41.1:note(c,'They share only an edge.',731,461,32)
def add(c,t):
    heading(c,'Joining along an edge preserves the area')
    pair(c,cue(t,53.0,3.7))
    note(c,'5 × 4 = 20',753,188,37,TEALINK)
    if t>=49.2:note(c,'2 × 3 = 6',753,271,37,REDINK)
    if t>=54.3:note(c,'20 + 6 = 26',753,380,43)
    if t>=56.8:note(c,'square units',753,448,28,LIGHT)
def triangle_problem(c,t):
    heading(c,'Lift the right triangle out of the corner')
    cut(c,cue(t,62.7,3.0),False,t>=64.8)
    note(c,'Whole rectangle',743,216,33,TEALINK)
    if t>=63.2:note(c,'Right triangle',743,292,33,REDINK)
    if t>=68.8:note(c,'How much area is left?',723,434,34)
def triangle_answer(c,t):
    heading(c,'The diagonal cuts a 4 by 3 rectangle in half')
    cut(c,cue(t,81.7,1.4),t>=78)
    note(c,'10 × 8 = 80',750,193,38,TEALINK)
    if t>=78.3:note(c,'½ × 4 × 3 = 6',750,292,38,REDINK)
    if t>=83.4:note(c,'80 − 6 = 74',750,400,45)
    if t>=84.2:note(c,'square units',750,468,28,LIGHT)
def challenge(c,t):
    heading(c,'Shade from the named columns and rows')
    overlay(c,cue(t,89.2,2.1),cue(t,94.2,3.1))
    note(c,'Lower left',755,188,31,TEALINK)
    if t>=90:note(c,'6 columns × 5 rows',755,244,31)
    if t>=94:note(c,'Second sheet',755,326,31,REDINK)
    if t>=95.5:note(c,'Columns 4–9, rows 3–8',755,382,29)
    if t>=101.5:note(c,'What stays unshaded?',755,488,33)
def shared(c,t):
    heading(c,'The overlap belongs to both shaded sheets')
    overlay(c,1,1,t>=110.7)
    note(c,'6 × 5 = 30',754,165,33,TEALINK)
    if t>=108.7:note(c,'6 × 6 = 36',754,226,33,REDINK)
    if t>=114:note(c,'Overlap  3 × 3 = 9',728,309,34,PLUM)
    if t>=118.8:note(c,'72 − (30 + 36 − 9)',728,404,34)
    if t>=123.3:note(c,'= 15 square units',728,480,36)
def second_check(c,t):
    heading(c,'Count the two untouched corners directly')
    selected=LOW if t<130 else LOW|HIGH
    overlay(c,1,1,focus=selected)
    note(c,'Bottom right   3 × 2 = 6',710,232,33)
    if t>=130:note(c,'Top left   3 × 3 = 9',710,323,33)
    if t>=135:note(c,'6 + 9 = 15',710,447,43,TEALINK)
def mistakes(c,t):
    heading(c,'Give each square the correct count')
    overlay(c,1,1,t>=149.5)
    note(c,'Area counts the inside.',736,217,33)
    if t>=149.7:note(c,'Subtract both sheets.',736,320,31)
    if t>=154.6:note(c,'Restore the shared 9 once.',709,435,30,PLUM)
def recap(c,t):
    heading(c,'Choose a split that you can check')
    if t<163.5:cut(c,cue(t,159.0,2.2),True)
    else:overlay(c,1,1,True,LOW|HIGH if t>=167 else None)
    note(c,'Draw the whole.',738,196,35,TEALINK)
    if t>=159.4:note(c,'Label the pieces.',738,274,34)
    if t>=163.5:note(c,'Find any overlap.',738,352,34,PLUM)
    if t>=167:note(c,'Check a second way.',738,450,34)
SCENES=(intro,uses,join,add,triangle_problem,triangle_answer,challenge,shared,second_check,mistakes,recap)
def verify():
    assert 5*4+2*3==26
    polygon=[(0,0),(6,0),(10,3),(10,8),(0,8)]
    assert abs(sum(x*Y-X*y for (x,y),(X,Y) in zip(polygon,polygon[1:]+polygon[:1])))/2==74
    assert (len(FULL),len(FIRST),len(SECOND),len(FIRST&SECOND))==(72,30,36,9)
    assert FULL-(FIRST|SECOND)==LOW|HIGH and not LOW&HIGH
    assert (len(LOW),len(HIGH))==(6,9)
