"""A mast of floodlights cuts horizontal plans through an isometric yard of unit cubes."""
from stage import blend, clamp, mix

BACKGROUND=('#102942','#102134')
INK,SKY,LIGHT,COPPER,BLUE='#f0f5ed','#9dd8e2','#ffca72','#e98b72','#4a7797'
DIM,GRID,WATER='#31516a','#36596f','#338da7'
BRIDGE='Follow one stack as the floodlight climbs. Count which bays reach the beam, then which cubes rise above the waterline.'
YARD=((1,4,2),(3,0,4))
STAIR=((1,2,3,4,5),(1,2,3,4,5))


def check_maths():
    heights=[h for row in YARD for h in row]
    counts=[sum(h>=level for h in heights) for level in range(1,5)]
    assert counts==[5,4,3,2] and sum(counts)==sum(heights)==14
    assert sum(max(0,h-2) for h in heights)==5 and sum(h>2 for h in heights)==3
    assert 12-sum((1,2,4))==5
    assert sum(map(sum,STAIR))==2*sum(range(1,6))==30
    assert [sum(h>=k for row in STAIR for h in row) for k in range(1,6)]==[10,8,6,4,2]


def txt(a,text,x,y,size=36,col=INK,t=1,align='left'):
    a.label(text,x,y,size,col,t,align=align,bold=True)


def iso(origin,x,y,z,s):
    return origin[0]+(x-y)*s,origin[1]+(x+y)*s*.45-z*s*.9


def face(a,points,fill,edge):
    a.polygon(points,fill,edge,2)


def block(a,org,x,y,z,s,colour):
    corners=[iso(org,x+i,y+j,z+1,s) for i,j in ((0,0),(1,0),(1,1),(0,1))]
    low=[iso(org,x+i,y+j,z,s) for i,j in ((0,0),(1,0),(1,1),(0,1))]
    edge=blend(colour,'#132b40',.63)
    face(a,[corners[1],corners[2],low[2],low[1]],blend(colour,'#132e44',.28),edge)
    face(a,[corners[2],corners[3],low[3],low[2]],blend(colour,'#152737',.42),edge)
    face(a,corners,colour,edge)


def model(a,rows,org,s,level=0,water=0,shown_rows=None):
    for y,row in enumerate(rows):
        for x,h in enumerate(row):
            p=[iso(org,x+i,y+j,0,s) for i,j in ((0,0),(1,0),(1,1),(0,1))]
            face(a,p,GRID,DIM)
    cells=sorted(((x+y,x,y,h) for y,row in enumerate(rows) for x,h in enumerate(row)),key=lambda t:(t[0],t[2]))
    for _,x,y,h in cells:
        if shown_rows is not None and y not in shown_rows:continue
        for z in range(h):
            if water:
                colour=LIGHT if z>=water else blend(BLUE,WATER,.70)
            elif level:
                colour=LIGHT if z+1==level else blend(BLUE,DIM,.22)
            else:
                colour=(BLUE,'#6699ab','#80adb6','#a0c4bb','#c0cfc2')[(z)%5]
            block(a,org,x,y,z,s,colour)


def height_plan(a,rows,x,y,s,level=0,show_values=True,masked=()):
    for j,row in enumerate(rows):
        for i,h in enumerate(row):
            xx,yy=x+i*s,y+j*s
            fill=LIGHT if level and h>=level else (DIM if h else '#233c50')
            a.box(xx,yy,s-3,s-3,fill=fill,edge=GRID,radius=2)
            if show_values:
                txt(a,'?' if (i,j) in masked else str(h),xx+s*.48,yy+s*.46,round(s*.49),BACKGROUND[1] if fill==LIGHT else INK,align='center')
            elif level and h>=level:
                a.dot(xx+s*.48,yy+s*.46,max(3,s*.13),BACKGROUND[1])


def mast(a,x,base,s,k,levels=5):
    a.line([(x,base),(x,base-levels*s)],GRID,7)
    for n in range(1,levels+1):
        y=base-(n-.5)*s
        a.line([(x-9,y),(x+10,y)],SKY,2)
        txt(a,str(n),x-19,y,22,SKY,align='right')
    yy=base-(k-.5)*s
    a.box(x-12,yy-9,27,18,fill=LIGHT,radius=3)
    a.polygon([(x+14,yy-6),(x+60,yy-15),(x+60,yy+15),(x+14,yy+6)],'#8b835f')


def header(a,title):
    a.line([(68,119),(1208,119)],GRID,2)
    for x in range(75,1205,90):
        a.line([(x,119),(x,126)],BLUE,2)
    txt(a,title,65,72,48)


def draw(a,n,c):
    titles=['Sweep a level with light','Look down on the six bays','Which bays reach level two?','One yard, two counts','The yard fills with water','Above the waterline','Restore a missing tag','Two strips form the stair','What exactly are you counting?']
    header(a,titles[n-1])
    if n==1:
        t=c.reveal('level three',1.8)
        mast(a,170,534,63,1+2*t)
        model(a,((5,),),(427,493),79,3 if t>.83 else max(1,round(1+2*t)))
        txt(a,'Height 5',713,257,54,SKY,c.reveal('five cubes'))
        txt(a,'Beam at level 3',713,373,48,LIGHT,t)
        txt(a,'How many cubes meet it?',713,486,34,INK,c.reveal('how many'))
    elif n in (2,3):
        model(a,YARD,(355,382),68,2 if n==3 and c.reveal('second level')>.6 else 0)
        height_plan(a,YARD,760,239,104,2 if n==3 and c.reveal('at least two')>.9 else 0)
        txt(a,'Far',737,285,26,SKY,align='right')
        txt(a,'Near',737,391,26,SKY,align='right')
        if n==2:txt(a,'0 = empty bay',770,535,35,COPPER,c.reveal('zero marks'))
        else:txt(a,'Height ≥ 2',775,535,39,LIGHT,c.reveal('at least two'))
    elif n==4:
        level=2
        for k,phrase in ((1,'first level'),(2,'reach the second'),(3,'reach the third'),(4,'reach the fourth')):
            if c.reveal(phrase)>.2:level=k
        model(a,YARD,(337,382),69,level);mast(a,109,500,47,level,4)
        for i,v in enumerate((5,4,3,2)):
            phrase=('first level','reach the second','reach the third','reach the fourth')[i]
            if not c.reveal(phrase):continue
            xx=664+(i%2)*248;yy=186+(i//2)*157
            height_plan(a,YARD,xx,yy,43,i+1,False)
            txt(a,'Level '+str(i+1)+'  ·  '+str(v),xx+63,yy+113,24,LIGHT,align='center')
        txt(a,'5 + 4 + 3 + 2 = 14',655,537,40,INK,c.reveal('add to fourteen'))
    elif n in (5,6):
        t=1 if n==6 else c.reveal('top of level two',1.2)
        model(a,YARD,(355,387),75,water=2 if t>.55 else 0)
        if t:
            corners=[iso((355,387),xx,yy,2,75) for xx,yy in ((-.25,-.25),(3.25,-.25),(3.25,2.25),(-.25,2.25),(-.25,-.25))]
            for left,right in zip(corners,corners[1:]):
                a.dashed(left,right,SKY,3,dash=11,gap=9,fraction=t)
        if n==5:
            txt(a,'Water hides levels 1 and 2',670,291,37,SKY,c.reveal('lowest two layers'))
            txt(a,'How many cubes stay dry?',670,412,36,LIGHT,c.reveal('remain visible'))
        else:
            height_plan(a,YARD,690,202,65,3,False)
            height_plan(a,YARD,957,202,65,4,False)
            txt(a,'Level 3',786,379,32,SKY,align='center');txt(a,'Level 4',1052,379,32,SKY,align='center')
            txt(a,'3 + 2 = 5 cubes',690,488,46,LIGHT,c.reveal('two more'))
    elif n==7:
        fixed=c.reveal('five remaining',1)
        height_plan(a,((1,2),(4,5)),205,197,150,masked=() if fixed>.85 else {(1,1)})
        txt(a,'Total = 12 cubes',703,244,49,SKY,c.reveal('twelve cubes'))
        txt(a,'1 + 2 + 4 = 7',703,356,46,INK,c.reveal('seven cubes'))
        txt(a,'12 − 7 = 5',703,466,51,LIGHT,fixed)
    elif n==8:
        t=c.reveal('two matching strips',.8)
        model(a,STAIR,(290,362),65,shown_rows={0,1} if t>.9 else {0})
        txt(a,'1 + 5 = 6',722,244,47,SKY,c.reveal('first and last'))
        txt(a,'2 + 4 = 6',722,346,47,COPPER,c.reveal('second and fourth'))
        txt(a,'6 + 6 + 3 = 15',722,453,46,LIGHT,c.reveal('middle adds three'))
    else:
        model(a,STAIR,(290,362),65)
        txt(a,'2 × 15 = 30 cubes',677,206,46,LIGHT,c.reveal('thirty cubes'))
        if c.reveal('one level'):
            txt(a,'Layer 3',678,307,35,SKY)
            height_plan(a,STAIR,916,275,34,3,False)
        txt(a,'Count by stack',678,418,42,SKY,c.reveal('each stack height'))
        txt(a,'Count by horizontal layer',678,513,34,INK,c.reveal('positions on every layer'))


def poster(draw):return draw(9,1.5)
