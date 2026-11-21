"""Rotate a record, read its two-sided credits, and fold the sleeve into a rehearsal ledger."""
from itertools import combinations
from math import cos, pi, sin

from stage import blend, clamp, mix

BACKGROUND = ('#242037', '#171725')
CHALK, LILAC, PINK, LIME = '#fcf1da', '#b2a5ef', '#fd8693', '#c9db79'
WAX, GROOVE, CYAN, MUTED = '#1b1c2a', '#46475d', '#8dd4ca', '#9c97a7'
BRIDGE = 'Pick one track and follow both singer credits. On the rehearsal sheet, follow one mark from its row to its column.'
SINGERS = ('Ada','Ben','Cleo','Dev')
PAIRS = tuple(combinations(range(4),2))
REHEARSALS = ((0,1),(0,1),(0,2),(0,2),(0,3),(1,2),(1,2),(2,3),(2,3))
INKS=(PINK,CYAN,LIME,LILAC)


def check_maths():
    assert len(PAIRS)==6 and all(sum(i in pair for pair in PAIRS)==3 for i in range(4))
    credits=[4,3,2,3,1,3]
    example=((0,1),(0,2),(0,3),(0,5),(1,3),(1,5),(2,4),(3,5))
    assert [sum(i in track for track in example) for i in range(6)]==credits
    assert sum(credits)==2*len(example)==16
    assert [(d,5-d) for d in range(6) if 2*d+5-d==8]==[(3,2)]
    assert len(REHEARSALS)==9 and all(len(set(pair))==2 for pair in REHEARSALS)
    assert [sum(s in p for p in REHEARSALS) for s in range(4)]==[5,4,6,3]


def label(a,text,x,y,size=35,colour=CHALK,t=1,align='left'):
    a.label(text,x,y,size,colour,t,align=align,bold=True)


def circle(a,x,y,r,colour,width=2):
    box=tuple(a.px(v) for v in (x-r,y-r,x+r,y+r))
    a.draw.ellipse(box,outline=colour,width=max(1,a.px(width)))


def record(a,x,y,r,t=0,colour=PINK,credits=(),label_text=None):
    a.dot(x,y,r,WAX)
    for k in (1,.93,.88,.80,.76,.71,.65,.59,.56,.51):
        circle(a,x,y,r*k,GROOVE,2 if k<1 else 4)
    a.dot(x,y,r*.43,colour)
    a.dot(x,y,max(2,r*.024),WAX)
    phi=-.75+t*.19
    for turn in (phi,phi+pi):
        a.line([(x+r*.55*cos(turn),y+r*.55*sin(turn)),(x+r*.89*cos(turn),y+r*.89*sin(turn))],MUTED,2)
    if label_text:label(a,label_text,x,y-r*.17,max(18,int(r*.17)),WAX,align='center')
    if credits:
        for i,name in enumerate(credits):
            label(a,name,x,y+r*(.10+(i-(len(credits)-1)/2)*.23),max(18,int(r*.18)),WAX,align='center')


def sleeve(a,x,y,w,h,colour):
    a.box(x+8,y+10,w,h,radius=5,fill='#10131d')
    a.box(x,y,w,h,radius=5,fill=colour)
    a.line([(x+8,y+12),(x+w-8,y+12)],blend(colour,CHALK,.32),2)
    a.line([(x+12,y+h-9),(x+w-12,y+h-9)],blend(colour,WAX,.28),2)


def track(a,x,y,num,names,amount=1):
    a.box(x,y,258,60,fill=blend(WAX,'#3c3650',amount),edge='#555268',radius=7)
    if amount:
        a.dot(x+29,y+30,13,blend(GROOVE,LILAC,amount))
        a.dot(x+29,y+30,4,WAX)
        label(a,names,x+55,y+30,25,CHALK,amount)


def header(a,title):
    # The continuous meter and tonearm rest are specific to the recording desk.
    a.line([(62,130),(1215,130)],GROOVE,2)
    for n in range(7):
        a.box(65+n*11,48-(n%4)*4,6,6+(n%4)*4,radius=1,fill=(PINK,LILAC,CYAN)[n%3])
    label(a,title,62,94,47)


def ledger(a,x,y,show_last,t):
    space=76
    for j,v in enumerate(('A','B','C','D','E','F')):
        label(a,v,x+j*space,y,34,LILAC,align='center')
    for j,v in enumerate((4,3,2,3,1,3)):
        txt='?' if j==5 and not show_last else str(v)
        label(a,txt,x+j*space,y+82,47,PINK if j==5 else CHALK,t if j==5 and show_last else 1,align='center')


def attendance(a,x,y,amount,missing=True):
    w,h=64,34
    for j in range(4):
        label(a,str(j+1),x+j*w+w/2,y-24,24,INKS[j],align='center')
    for i,pair in enumerate(REHEARSALS):
        label(a,chr(65+i),x-20,y+i*h+h/2,21,MUTED,align='center')
        for j in range(4):
            a.box(x+j*w,y+i*h,w-2,h-2,fill='#302e43',radius=2)
            if j in pair:
                a.dot(x+(j+.5)*w,y+(i+.5)*h,7,blend(GROOVE,INKS[j],amount))
    for j,n in enumerate((5,4,6,3)):
        label(a,'?' if missing and j==3 else str(n),x+j*w+w/2,y+9*h+24,28,INKS[j],align='center')


def draw(a,n,c):
    titles=['One recording, two names','Four voices in the booth','Pair up the credits','A smudge on the sleeve','Restore the sixth entry','A change of ensemble','Five tracks, eight names','Rehearsal check-in','The same marks in two directions']
    header(a,titles[n-1])
    if n==1:
        sleeve(a,97,204,462,302,'#594c70')
        a.line([(102,482),(392,210)],'#d98b91',15)
        a.line([(177,495),(480,211)],'#b9d3ba',8)
        slide=c.reveal('one track',1.4)
        record(a,400+65*slide,352,183,c.local,PINK,('Ada','Ben'))
        label(a,'1 track',704,245,57,CHALK,c.reveal('one track'))
        label(a,'2 singer credits',704,349,47,PINK,c.reveal('two names'))
        label(a,'Ada   +   Ben',704,454,39,CYAN,c.reveal('ben does too'))
    elif n in (2,3):
        x,y=319,353
        record(a,x,y,181,c.local,LILAC,label_text='DUETS')
        coords=[(x,y-148),(x+148,y),(x,y+148),(x-148,y)]
        for i,(xx,yy) in enumerate(coords):
            a.dot(xx,yy,33,INKS[i]);label(a,SINGERS[i],xx,yy,22,WAX,align='center')
        if n==2:
            t=c.reveal('three possible partners',1.6)
            for j in (1,2,3):
                p=clamp(3*t-(j-1));u,v=coords[0],coords[j]
                a.line([u,(mix(u[0],v[0],p),mix(u[1],v[1],p))],PINK,4)
            for i,(xx,yy) in enumerate(coords):
                a.dot(xx,yy,33,INKS[i]);label(a,SINGERS[i],xx,yy,22,WAX,align='center')
            label(a,'4 singers × 3 credits',619,262,46,CHALK,c.reveal('other three singers'))
            label(a,'12 credits',619,375,57,LIME,c.reveal('twelve singer credits'))
            label(a,'How many tracks?',619,489,38,LILAC,c.reveal('distinct tracks'))
        else:
            for idx,(i,j) in enumerate(PAIRS):
                group=('three with ada','two new partners','one more')[min(i,2)]
                track(a,596+(idx%2)*284,200+(idx//2)*98,idx+1,SINGERS[i]+' + '+SINGERS[j],c.reveal(group,1))
            label(a,'3 + 2 + 1 = 6 tracks',598,528,42,LIME,c.reveal('three plus two'))
    elif n in (4,5):
        sleeve(a,85,195,538,342,'#3f3851')
        label(a,'Singer credits',137,262,39,PINK)
        ledger(a,161,350,n==5 and c.reveal('missing entry')>0,c.reveal('missing entry') if n==5 else 0)
        if n==4:
            label(a,'8 duets',728,271,57,CHALK,c.reveal('eight duets'))
            label(a,'6 singers',728,378,53,CYAN,c.reveal('six singers'))
            label(a,'What belongs at F?',728,483,37,LILAC,c.reveal('smudge'))
        else:
            label(a,'8 × 2 = 16',711,262,54,PINK,c.reveal('sixteen singer credits'))
            label(a,'Known total = 13',711,366,41,CHALK,c.reveal('total of thirteen'))
            label(a,'16 − 13 = 3',711,478,55,LIME,c.reveal('missing entry is three'))
    elif n==6:
        record(a,345,365,191,c.local,CYAN)
        for j in range(3):
            angle=-pi/2+2*pi*j/3
            xx,yy=345+125*cos(angle),365+125*sin(angle)
            a.dot(xx,yy,31,INKS[j]);label(a,str(j+1),xx,yy,29,WAX,align='center')
        label(a,'3 names per trio',673,269,45,CYAN,c.reveal('every track'))
        label(a,'18 ÷ 3 = 6 tracks',673,375,49,CHALK,c.reveal('eighteen divided'))
        label(a,'Does every track have 3?',673,481,34,LILAC,c.reveal('sizes vary'))
    elif n==7:
        for i in range(5):
            xx=155+225*i;yy=332
            record(a,xx,yy,91,c.local,INKS[i%4])
            for j in range(2 if i<3 else 1):
                visible=c.reveal('first singer') if j==0 else clamp(c.reveal('extra names',1.5)*3-i)
                if visible:
                    cx=xx+(-22 if j==0 else 22); ink=(CYAN,PINK)[j]
                    a.dot(cx,yy+108,8,ink)
                    a.box(cx-13,yy+119,26,11,fill=ink,radius=5)
        label(a,'8 − 5 = 3 extra names',117,517,42,CYAN,c.reveal('three extra'))
        label(a,'3 duets   +   2 solos',691,517,40,LIME,c.reveal('three duets'))
    else:
        t=c.reveal('eighteen entries') if n==9 else c.reveal('two different sessions')
        attendance(a,181,211,t,missing=n==8 or c.reveal('three singers')<=0)
        if n==8:
            label(a,'9 singers',649,267,52,CHALK,c.reveal('nine singers'))
            label(a,'2 sessions per singer',649,370,40,PINK,c.reveal('two different sessions'))
            label(a,'Fourth session = ?',649,465,42,LILAC,c.reveal('fourth sheet'))
        else:
            label(a,'9 × 2 = 18 entries',649,264,48,CYAN,c.reveal('eighteen entries'))
            label(a,'5 + 4 + 6 = 15',649,366,46,PINK,c.reveal('add to fifteen'))
            label(a,'18 − 15 = 3',649,474,54,LIME,c.reveal('three singers'))


def poster(draw):
    return draw(8,1.5)
