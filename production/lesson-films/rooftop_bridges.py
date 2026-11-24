"""Aerial bridge plans and the matching pairs of entrance signs."""
from collections import Counter
from stage import clamp, mix

BACKGROUND=('#162c37','#163c41')
INK,LIME,SAND,BLUE,WHITE='#193638','#c7e6a1','#edc18b','#8bcadd','#f6f6e5'
POINTS={'A':(415,203),'B':(672,218),'C':(750,421),'D':(464,484),'E':(245,394),'F':(510,336)}
FOUR=[('A','B'),('A','C'),('A','D'),('B','C')]
EIGHT=[('F',x) for x in 'ABCDE']+[('E','A'),('E','B'),('C','D')]
BRIDGE='Each rooftop counts its entrance signs. When the last bridge reaches the mainland, which end is missing from the gardeners’ reports?'
TITLES=['Entrance signs and spans','Four reports arrive','Pair the opposite entrances',
        'Eight bridges, a missing report','Count the unclaimed ends','Test the garden map',
        'One bridge leaves the survey','Which ends were counted?']


def check_maths():
    assert Counter(v for edge in FOUR for v in edge)==dict(A=3,B=2,C=2,D=1)
    degrees=Counter(v for edge in EIGHT for v in edge)
    assert degrees==dict(A=2,B=2,C=2,D=2,E=3,F=5)
    assert len({tuple(sorted(edge)) for edge in EIGHT})==8
    assert sum(degrees.values())+1==17 and (17+1)//2==9


def segment(a,p,q,hue,draw):
    if draw<=0:return
    end=(mix(p[0],q[0],draw),mix(p[1],q[1],draw))
    a.line([p,end],'#587478',15);a.line([p,end],hue,6)


def map_draw(a,keys,edges,count):
    for i,(u,v) in enumerate(edges):
        segment(a,POINTS[u],POINTS[v],SAND,clamp(count-i))
    for key in keys:
        x,y=POINTS[key]
        a.box(x-35,y-25,70,50,radius=9,fill='#315854',edge=LIME,stroke=2)
        a.label(key,x,y+2,23,WHITE,align='center',bold=True)


def ledger(a,values,reveal):
    for j,(key,val) in enumerate(values):
        y=189+48*j
        a.line([(897,y+22),(1160,y+22)],'#55716d',1)
        a.label('Roof '+key,908,y,22,WHITE)
        a.label(val,1120,y,26,LIME,clamp(reveal-j),align='right',bold=True)


def draw(a,n,m):
    p=clamp(m.local/(m.scene['end']-m.start))
    a.label('ROOF GARDENS    /    BRIDGE LEDGER',72,50,20,LIME,bold=True)
    a.label(TITLES[n-1],70,103,46,WHITE,bold=True)
    if n==1:
        # Spread the triangle apart so each bridge visibly has two distinct entrance signs.
        pts=[(300,415),(540,202),(775,415)]
        edges=[(0,1),(1,2),(2,0)]
        for i,(u,v) in enumerate(edges):
            segment(a,pts[u],pts[v],SAND,clamp(5*p-i+.2))
            for dist in (.19,.81):
                x=mix(pts[u][0],pts[v][0],dist);y=mix(pts[u][1],pts[v][1],dist)
                a.box(x-6,y-6,12,12,radius=1,fill=LIME,opacity=clamp(5*p-i))
        for j,(x,y) in enumerate(pts):
            a.dot(x,y,24,'#315854');a.label('ABC'[j],x,y,22,WHITE,align='center',bold=True)
        a.label('6 signs',918,294,33,LIME,m.reveal('six entrance signs'))
        a.label('3 bridges',918,369,33,SAND,m.reveal('three bridges'))
    elif n in (2,3):
        map_draw(a,'ABCD',FOUR,0 if n==2 else min(4,6*p))
        ledger(a,list(zip('ABCD','3221')),6*p if n==2 else 5)
        if n==3:a.label('8 signs ÷ 2 = 4 bridges',630,548,34,WHITE,m.reveal('give four'),align='center')
    elif n in (4,5,6):
        count=0 if n<6 else min(8,10*p)
        map_draw(a,'ABCDEF',EIGHT,count)
        vals=list(zip('ABCDEF','22223'+('?' if n==4 else '5')))
        ledger(a,vals,7 if n!=5 else 5+m.reveal('five unclaimed'))
        result={4:'8 bridges in the ledger',5:'16 − (2 + 2 + 2 + 2 + 3) = 5',6:'5 spokes + 3 outer spans = 8'}
        alpha=1 if n==4 else m.reveal('five unclaimed' if n==5 else 'Check the eight')
        a.label(result[n],630,552,31,SAND,alpha,align='center',bold=True)
    else:
        map_draw(a,'ABCDEF',EIGHT,8)
        start=POINTS['C'];end=(1020,429)
        segment(a,(start[0]+36,start[1]),end,BLUE,m.reveal('mainland') if n==7 else 1)
        a.box(991,402,170,55,radius=5,fill='#345a66')
        a.label('MAINLAND',1075,433,20,WHITE,align='center')
        if n==7:a.label('(17 + 1) ÷ 2 = 9 bridges',632,549,33,SAND,m.reveal('Eighteen signs'),align='center')
        else:a.label('Two reports here.   One report across the boundary.',640,554,28,WHITE,align='center')


def poster(draw):
    return draw(10.0,1.5)
