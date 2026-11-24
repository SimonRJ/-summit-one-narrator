"""Moving observatory chart paper shows the difference between a period and its first mark."""
import math
from stage import between

BACKGROUND = ('#142e39', '#213947')
PAPER, INK = '#f5edcf', '#263c3a'
RUST, TEAL, LEMON, WHITE = '#a33f27', '#006c72', '#ffd76c', '#fff8e9'
BRIDGE = 'Compare the two stopwatch strips. If a flash occurs at zero, how many six-second gaps lead to the third mark?'
TITLES = ['Three taps on the paper','Start now, or at the first flash?','Where does the third mark land?',
          'The observatory starts two signals','The first shared mark','How far to the next alignment?',
          'Cut the chart at one minute','Six marks, or seven?']


def check_maths():
    assert [0,3,6][-1] - [0,3,6][0] == 6
    assert [6*i for i in range(3)] == [0,6,12]
    assert [6*i for i in range(1,4)] == [6,12,18]
    light=set(range(6,121,6)); bell=set(range(3,121,9))
    assert sorted(light & bell) == [12,30,48,66,84,102,120]
    assert math.lcm(6,9)==18


def strip(a, y, end, tick, events, limit, colour, name):
    x0,x1=205,1150
    def x(t):return x0+(x1-x0)*t/end
    a.box(81,y-44,1110,109,radius=9,fill=PAPER)
    a.label(name,96,y-7,19,INK,bold=True)
    for t in range(0,end+1,tick):
        xx=x(t)
        a.line([(xx,y-36),(xx,y+27)],'#d4caaa',1)
        a.label(str(t),xx,y+44,17,INK,align='center')
    a.line([(x0,y),(x1,y)],'#b2aa90',2)
    points=[(x0,y)]
    for event in events:
        if event>limit:break
        xx=x(event)
        points.extend([(max(x0,xx-7),y),(xx,y-30),(min(x1,xx+6),y)])
    points.append((x(min(end,max(0,limit))),y))
    a.line(points,colour,4)
    return x


def bracket(a,x,t1,t2,y,txt,opacity):
    if opacity<=0:return
    left,right=x(t1),x(t2)
    a.line([(left,y+8),(left,y),(right,y),(right,y+8)],LEMON,3,opacity)
    a.label(txt,(left+right)/2,y-14,25,LEMON,opacity,align='center',bold=True)


def draw(a,n,m):
    span=max(.1,m.scene['end']-m.start); phase=min(1,max(0,m.local/span))
    a.label('OBSERVATORY   /   CHART RECORDER',78,53,21,'#b3d9cb',bold=True)
    a.label(TITLES[n-1],75,104,46,WHITE,bold=True)
    if n==1:
        x=strip(a,318,6,1,[0,3,6],6*min(1,phase*2.65),RUST,'TAPS')
        p=m.reveal('Two stretches')
        bracket(a,x,0,3,233,'3 s',p);bracket(a,x,3,6,233,'3 s',p)
        a.label('2 gaps × 3 seconds = 6 seconds',640,469,34,WHITE,p,align='center')
    elif n in (2,3):
        p=phase if n==2 else min(1,phase*2.6)
        x=strip(a,264,18,3,[0,6,12],18*min(1,2*p),RUST,'EARLY')
        strip(a,425,18,3,[6,12,18],18*min(1,max(0,2.3*p-.45)),TEAL,'DELAY')
        if n==3:
            for t,y in [(12,264),(18,425)]:a.dot(x(t),y-30,7,LEMON,m.reveal('twelve'))
            a.label('Same spacing.   A different first mark.',640,542,29,WHITE,m.reveal('Spacing agrees'),align='center')
    else:
        scale={4:60,5:24,6:36,7:66,8:120}[n]
        tick={4:6,5:3,6:6,7:6,8:12}[n]
        distance=min(1,phase*1.7)*scale
        if n==7:distance=12+min(1,phase*1.6)*(scale-12)
        x=strip(a,252,scale,tick,range(6,scale+1,6),distance,RUST,'LIGHT')
        strip(a,393,scale,tick,range(3,scale+1,9),distance,TEAL,'BELL')
        if n>4:
            for t in range(12,scale+1,18):
                if t<=distance:
                    a.dashed((x(t),224),(x(t),392),LEMON,3)
                    a.dot(x(t),224,5,LEMON)
            if n==5:a.label('12 seconds',x(12),497,34,LEMON,m.reveal('At twelve'),align='center')
            if n==6:bracket(a,x,12,30,173,'18 s',m.reveal('Eighteen seconds'))
            if n==7:
                a.line([(x(60),187),(x(60),462)],WHITE,4,m.reveal('The cut'))
                a.label('Through 60 s:  12, 30, 48',640,525,35,WHITE,m.reveal('three coincidences'),align='center')
            if n==8:a.label('t < 120 s   →   6                 t ≤ 120 s   →   7',640,504,32,WHITE,m.reveal('Strictly before'),align='center')
        else:a.label('Which two ink spikes share a time?',640,520,32,WHITE,m.reveal('how often'),align='center')


def poster(draw):
    return draw(9.0,1.5).crop((0,0,1920,1080))
