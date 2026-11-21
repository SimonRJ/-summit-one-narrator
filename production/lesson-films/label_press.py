"""A paper feed, a corner die and an order book explain three different counting questions."""
from itertools import combinations, product

from stage import blend, clamp, mix

BACKGROUND = ('#f1e7d6', '#e7d6bf')
INK, PLUM, RED, TEAL = '#33263a', '#653957', '#a53638', '#146869'
PAPER, BLANK, GUIDE, BRASS = '#fff8e5', '#f7eed7', '#b9a986', '#b67b2b'
BRIDGE = 'Watch the ink stains split the paper. Compare a limit on the number of labels with a cut that really reaches it.'
CORNERS = {(0,0), (2,0), (0,2), (2,2)}
STAMP_A = {(0,0), (1,0), (0,1)}
STAMP_B = {(2,2), (2,1), (1,2)}
OUTLINE = [(0,0),(1,0),(2,0),(2,1),(1,1),(1,2),(0,2),(0,1),(0,0)]
D2 = [(((0,0),(0,1)),((1,0),(1,1))),(((0,0),(1,0)),((0,1),(1,1)))]
D3 = [(((0,0),(0,1)),((1,0),(1,1)),((2,0),(2,1))),
      (((0,0),(0,1)),((1,0),(2,0)),((1,1),(2,1))),
      (((0,0),(1,0)),((0,1),(1,1)),((2,0),(2,1)))]


def check_maths():
    clean = set(range(16)) - {2,8}
    rows = [{i,i+1,i+2} for i in range(14) if {i,i+1,i+2} <= clean]
    legal = lambda group: sum(map(len,group)) == len(set().union(*group))
    assert max(k for k in range(1,6) if any(legal(p) for p in combinations(rows,k))) == 3
    assert legal([set(range(i,i+3)) for i in (3,9,12)])
    windows = [{(x+dx,y+dy) for dx,dy in product(range(2),repeat=2)} for x,y in product(range(2),repeat=2)]
    stamps = [p - {c} for p in windows for c in p]
    assert max(len(s & CORNERS) for s in stamps)==1
    assert not any(legal(p) for p in combinations(stamps,3))
    assert STAMP_A in stamps and STAMP_B in stamps and STAMP_A.isdisjoint(STAMP_B)
    assert sum((x+dx,y+dy) not in STAMP_A for x,y in STAMP_A for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) == len(OUTLINE)-1 == 8
    for cols,groups in ((2,D2),(3,D3)):
        field = set(product(range(cols),range(2)))
        def cover(cells):
            if not cells:
                return 1
            x,y = min(cells)
            return sum(cover(cells-{(x,y),v}) for v in ((x+1,y),(x,y+1)) if v in cells)
        assert cover(field) == len(groups)
        for p in groups:
            assert set().union(*p) == field and legal(p)
            assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in p)


def words(a,text,x,y,size=37,ink=INK,amount=1,align='left'):
    a.label(text,x,y,size,ink,amount,align=align,bold=True)


def furniture(a,title):
    for x in (38,1242):
        for y in (45,596):
            a.line([(x-10,y),(x+10,y)],BRASS,2)
            a.line([(x,y-10),(x,y+10)],BRASS,2)
    words(a,title,75,90,48)
    a.dashed((76,145),(1204,145),GUIDE,2,dash=5,gap=8)


def roll(a,x,y,n,size,blocked=()):
    w=n*size
    a.box(x-10,y-24,w+20,size+48,radius=3,fill=PAPER,edge=GUIDE)
    for i in range(n):
        left=x+i*size
        for yy in (y-12,y+size+12):
            a.dot(left+size/2,yy,3.7,GUIDE)
        a.box(left,y,size,size,radius=0,fill=BLANK,edge=GUIDE,stroke=1)
        if i in blocked:
            for rx,ry,r in ((.40,.40,.20),(.63,.57,.23),(.38,.67,.14),(.72,.29,.05)):
                a.dot(left+rx*size,y+ry*size,r*size,PLUM)


def impression(a,x,y,w,h,colour,t,with_mark=True):
    if t<=0:
        return
    a.box(x+3,y+3,(w-6)*t,h-6,radius=4,fill=blend(BLANK,colour,t),edge=colour,stroke=2)
    if with_mark and t>.85:
        a.line([(x+w*.37,y+h*.52),(x+w*.48,y+h*.66),(x+w*.67,y+h*.33)],PAPER,4)


def roller(a,x,y,t):
    # A section through the handle shows where the steel die descends.
    bottom=y+mix(-25,4,t)
    a.box(x+33,bottom-75,23,66,fill=PLUM,radius=3)
    a.box(x+5,bottom-81,81,14,fill=PLUM,radius=7)
    a.box(x,bottom-20,90,15,fill=BRASS,radius=3)


def sheet(a,x,y,size,corner=False):
    a.box(x-9,y-9,size*3+18,size*3+18,fill=PAPER,edge=GUIDE,radius=2)
    for col,row in product(range(3),repeat=2):
        left,top=x+size*col,y+size*row
        a.box(left,top,size,size,fill=BLANK,edge=GUIDE,radius=0,stroke=2)
        if corner and (col,row) in CORNERS:
            a.dot(left+size/2,top+size/2,size*.13,RED)


def poly(a,x,y,size,cells,colour,t):
    if t<=0:return
    for col,row in cells:
        a.box(x+col*size+1,y+row*size+1,size-2,size-2,fill=blend(BLANK,colour,t),radius=0)
    for col,row in cells:
        for dx,dy,p,q in ((0,-1,(0,0),(1,0)),(1,0,(1,0),(1,1)),(0,1,(1,1),(0,1)),(-1,0,(0,1),(0,0))):
            if (col+dx,row+dy) not in cells:
                a.line([(x+(col+p[0])*size,y+(row+p[1])*size),(x+(col+q[0])*size,y+(row+q[1])*size)],blend(BLANK,INK,t),4)
        if t>.8:
            a.dot(x+(col+.5)*size,y+(row+.5)*size,3,PAPER)


def order(a,x,y,size,tiling,amount=1):
    if amount<=0:
        width=1+max(x for pair in tiling for x,y in pair)
        for col,row in product(range(width),range(2)):
            a.box(x+col*size,y+row*size,size-2,size-2,fill=BLANK,edge=GUIDE,radius=0)
        return
    for i,(u,v) in enumerate(tiling):
        left,top=min(u[0],v[0]),min(u[1],v[1])
        w,h=1+abs(u[0]-v[0]),1+abs(u[1]-v[1])
        colour=(TEAL,PLUM,BRASS)[i]
        a.box(x+left*size,y+top*size,w*size-2,h*size-2,fill=blend(BLANK,colour,amount),edge=INK,radius=3,stroke=2)


def draw(a,n,c):
    titles=['The label press','What can the printer promise?','Two stains in the roll','Separate the clean runs','A different cutting die','Look at the four corners','Two labels come free','Walk the edge','One seam, two independent sheets','Choose a left and a right']
    furniture(a,titles[n-1])
    if n in (1,2):
        x,y,s=127,320,124
        roll(a,x,y,8,s)
        if n==1:
            t=c.reveal('a single stroke',.85)
            roller(a,x+s*1.13,y,t)
            impression(a,x,y,3*s,s,TEAL,t)
            words(a,'3 joined squares per label',130,530,36,TEAL,c.reveal('every square'))
        else:
            words(a,'3 × 3 = 9',130,223,47,RED,c.reveal('nine squares'))
            words(a,'Only 8 available',560,224,39,RED,c.reveal('one more'))
            impression(a,x,y,3*s,s,TEAL,c.reveal('first three',.8))
            impression(a,x+3*s,y,3*s,s,PLUM,c.reveal('next three',.8))
            words(a,'2 labels fit',130,535,39,TEAL,c.reveal('two labels fit'))
            words(a,'2 left over',865,535,33,INK,c.reveal('two squares remain'))
    elif n in (3,4):
        x,y,s=91,305,68
        roll(a,x,y,16,s,{2,8})
        for start,k,tint in ((0,2,PLUM),(3,5,TEAL),(9,7,PLUM)):
            cx=x+s*(start+k/2)
            words(a,str(k),cx,240,46,tint,align='center')
        if n==3:
            words(a,'14 clean squares',104,490,42,TEAL,c.reveal('fourteen clean'))
            words(a,'Could 4 labels fit?',646,490,41,RED,c.reveal('four labels'))
        else:
            t1=c.reveal('one from the middle',.9);t2=c.reveal('two from the last',1.2)
            for start,t,tint in ((3,t1,TEAL),(9,clamp(t2*2),PLUM),(12,clamp(t2*2-1),TEAL)):
                impression(a,x+start*s,y,3*s,s,tint,t)
            for start,k,v,phrase in ((0,2,0,'too short'),(3,5,1,'only one label'),(9,7,2,'only two')):
                words(a,str(v),x+s*(start+k/2),457,48,TEAL,c.reveal(phrase),align='center')
            words(a,'0 + 1 + 2 = 3 labels',640,555,38,INK,c.reveal('limits add'),align='center')
    elif n in (5,6,7):
        x,y,s=154,194,112
        show_corners=n==6 or (n==5 and c.reveal('outside corners')>0)
        sheet(a,x,y,s,show_corners)
        if n==5:
            poly(a,708,230,75,STAMP_A,TEAL,c.reveal('a bent label'))
            words(a,'3 × 3 sheet',708,454,38,PLUM,c.reveal('three squares by three'))
            words(a,'Can 3 labels fit?',708,527,38,RED,c.reveal('three bent labels'))
        elif n==6:
            window=c.reveal('two by two window',1)
            if window:
                step=c.reveal('two corners',2)
                ax=x+s*step
                a.box(ax+2,y+2,s*2-4,s*2-4,fill=None,edge=TEAL,radius=1,stroke=6)
            words(a,'At most 1 corner per label',588,252,37,TEAL,c.reveal('at most one'))
            words(a,'3 labels → at most 3 corners',588,363,34,INK,c.reveal('with three labels'))
            words(a,'The sheet has 4 corners',588,470,36,RED,c.reveal('four corners'))
        else:
            poly(a,x,y,s,STAMP_A,TEAL,c.reveal('upper left corner',.8))
            poly(a,x,y,s,STAMP_B,PLUM,c.reveal('lower right corner',.8))
            words(a,'3 cannot fit',675,267,45,RED,c.reveal('three labels cannot'))
            words(a,'2 do fit',675,375,48,TEAL,c.reveal('these two can'))
            words(a,'Maximum = 2',675,479,44,INK,c.reveal('maximum is two'))
    elif n==8:
        x,y,s=224,212,143
        poly(a,x,y,s,STAMP_A,TEAL,1)
        t=c.reveal('each join hides',1.2)
        if t:
            a.dashed((x+s,y),(x+s,y+s),PAPER,6,fraction=t)
            a.dashed((x,y+s),(x+s,y+s),PAPER,6,fraction=t)
        words(a,'3 squares × 4 sides = 12',640,253,35,PLUM,c.reveal('twelve sides'))
        words(a,'2 joins hide 4 sides',640,354,39,RED,t)
        words(a,'Perimeter = 8 units',640,463,40,TEAL,c.reveal('eight edge units'))
        walk=c.reveal('trace them',1.8)*8
        for i,(p,q) in enumerate(zip(OUTLINE,OUTLINE[1:])):
            d=clamp(walk-i)
            if d:a.line([(x+p[0]*s,y+p[1]*s),(x+mix(p[0],q[0],d)*s,y+mix(p[1],q[1],d)*s)],BRASS,11)
    elif n==9:
        words(a,'2 × 2',324,220,39,TEAL,align='center')
        words(a,'2 × 3',884,220,39,PLUM,align='center')
        a.dashed((552,195),(552,544),RED,5,dash=16,gap=9)
        for i,p in enumerate(D2):order(a,100+i*220,302,83,p,c.reveal('two tilings on the left'))
        for i,p in enumerate((D3[0],D3[2])):
            xx,yy,sz=610+i*300,304,76
            order(a,xx,yy,sz,p,0)
            when=c.reveal('either upright' if i==0 else 'two horizontal strips',.9)
            for k in range(i+1):
                u,v=p[k]; left,top=min(u[0],v[0]),min(u[1],v[1])
                w,h=1+abs(u[0]-v[0]),1+abs(u[1]-v[1])
                if when:a.box(xx+left*sz,yy+top*sz,w*sz-2,h*sz-2,fill=blend(BLANK,(TEAL,PLUM)[k],when),edge=INK,radius=3)
            words(a,('2 × 2 remains','1 column remains')[i],xx+sz*1.5,519,27,PLUM,when,align='center')
    else:
        for j in range(3):
            for i in range(2):
                x=96+548*i;y=195+121*j
                p=c.reveal('six pairs',1.8);opacity=clamp(p*6-(2*j+i))
                order(a,x,y,43,D2[i],opacity)
                a.dashed((x+108,y+4),(x+108,y+80),RED,3,dash=6,gap=6)
                order(a,x+128,y,43,D3[j],opacity)
        words(a,'2 × 3 = 6 arrangements',644,570,36,INK,c.reveal('six different'),align='center')


def poster(draw):
    return draw(8,1.5)
