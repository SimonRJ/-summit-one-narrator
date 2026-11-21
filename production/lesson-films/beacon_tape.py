"""A harbour light recorder. Pulse peaks are plotted at actual elapsed times."""
from stage import clamp, mix
from itertools import accumulate
from math import ceil, floor, pi, sin

BACKGROUND = ('#092536', '#0b1721')
WHITE = '#f3ebdc'
PAPER = '#eee3c5'
INK = '#183c40'
TICK = '#988d76'
GREEN = '#64e8bd'
AMBER = '#ffbc76'
CREAM = '#f7e8c4'
BRIDGE = 'Follow the pen from the first peak to the fifth. In the torn strip, the first peak you can see is already numbered four.'


def check_maths():
    first = list(range(0, 17, 4))
    assert len(first) == 5 and first[-1] - first[0] == 16
    peaks = list(range(0, 46, 3))
    assert peaks[10] - peaks[3] == 21 and peaks[15] == 45
    candidates = [(k, list(accumulate([5]*k + [3]*(18-k), initial=0))) for k in range(1,18)]
    solutions = [(k,t) for k,t in candidates if t[-1] == 70]
    assert len(solutions) == 1
    k, t = solutions[0]
    assert k+1 == 9 and t[8] == 40 and len(t) == 19 and t[-1]-t[8] == 30
    assert list(range(4,25,4)) == [4,8,12,16,20,24]


def header(a, number, title):
    a.label('HARBOUR SIGNAL RECORDER', 76, 48, 20, GREEN, bold=True)
    a.label(title, 76, 100, 48, WHITE, bold=True)
    a.label(f'RECORD  {number:02}', 1204, 54, 20, CREAM, align='right')


def paper(a, x, y, w, h):
    a.box(x-8,y-8,w+16,h+16,fill='#112125',edge='#426065',radius=10)
    a.box(x,y,w,h,fill=PAPER,radius=4)
    for k in range(16,int(w)-10,28):
        a.dot(x+k,y+13,3,INK)
        a.dot(x+k,y+h-13,3,INK)
    for k in range(30,int(w)-13,24):
        a.line([(x+k,y+27),(x+k,y+h-26)], '#d4cab0', 1)
    for k in range(33,int(h)-23,25):
        a.line([(x+8,y+k),(x+w-8,y+k)], '#d4cab0', 1)


def trace(a, x, y, width, times, maximum, elapsed, *, labels=None, numbers=True, first=1):
    """A peak is a diagrammatic time mark. Its tip has the exact horizontal time coordinate."""
    f = lambda t: x + width*t/maximum
    stop = f(elapsed) + (11 if abs(elapsed-times[-1]) < 0.0001 else 0)
    points = [(x-11, y)]
    amplitude = 48 if len(times)<13 else 38
    spread = min(8, width/max(1,len(times))*0.24)
    for n,t in enumerate(times):
        k = f(t)
        points += [(k-spread,y),(k-2,y-4),(k,y-amplitude),(k+2,y-6),(k+spread,y)]
        if k>stop+0.1: continue
        if numbers and (labels is None or n in labels):
            a.text(str(n+first),k,y-amplitude-19,22,INK,bold=True)
    points.append((x+width+7,y))
    rendered=[]
    for p,q in zip(points,points[1:]):
        if p[0]>stop: break
        rendered.append(p)
        if q[0]>stop:
            rendered.append((stop,mix(p[1],q[1],(stop-p[0])/(q[0]-p[0]))))
            break
    if len(rendered)>=2: a.line(rendered,INK,4)
    return f


def bracket(a,left,right,y,label,color=INK,size=25):
    a.line([(left,y-7),(left,y+6),(right,y+6),(right,y-7)],color,3)
    if label: a.text(label,(left+right)/2,y+28,size,color,bold=True)


def seconds(a,t,x=1082):
    a.box(x-98,395,196,115,radius=18,fill='#122c36',edge='#529d96',stroke=3)
    a.text('STOPWATCH',x,418,17,GREEN,bold=True)
    a.text(f'{int(round(t)):02} s',x,465,44,WHITE,bold=True)


def tower(a, t):
    # Tapered lighthouse on a small breakwater. Its fan stays anchored to the lamp.
    a.line([(75,466),(147,456),(246,461),(304,451)],'#80b8ba',3)
    a.polygon([(144,454),(158,299),(203,299),(220,454)],'#d7cbb4',INK,3)
    a.polygon([(151,374),(157,321),(205,321),(211,374)],'#cc7057')
    a.box(155,265,53,38,fill='#1b3741',radius=1,edge=CREAM,stroke=3)
    a.polygon([(148,266),(181,243),(215,266)],'#bd6e53')
    s = (sin(t*3-pi/2)+1)/2
    end_y = 261+20*sin(t*1.1)
    a.polygon([(188,282),(308,end_y-18),(308,end_y+23)],(round(71+104*s),round(83+74*s),round(68+36*s)))
    a.dot(181,283,7,AMBER)
    a.text('HARBOUR BEACON',181,505,18,CREAM,bold=True)


def draw(a,n,c):
    headings=['What does the clock count?','Five flashes','A tear between two pulse numbers',
              'Rebuild the missing interval','When did the beacon speed up?',
              'A strip of short gaps','Find the changeover peak','Start the clock in the right place']
    header(a,n,headings[n-1])
    if n==1:
        tower(a,c.t)
        paper(a,354,200,837,181)
        extent = 12*c.reveal('draws a sharp peak',3.2)
        trace(a,399,334,744,[0,4,8,12],12,extent)
        freeze=c.reveal('starting a stopwatch')
        if freeze>0: a.text('First peak = stopwatch starts',752,430,32,GREEN,opacity=freeze,bold=True)
        a.text('Elapsed at the first peak: 0 s',751,496,32,WHITE,opacity=c.reveal('zero'),bold=True)
    elif n==2:
        paper(a,79,181,1122,212)
        phrases=['from one to two','two to three','three to four','four to five']
        p=[c.reveal(s,.68) for s in phrases]
        x=trace(a,143,302,986,[0,4,8,12,16],16,4*sum(p))
        for i,amount in enumerate(p):
            if amount>.01: bracket(a,x(4*i),x(4*i+4*amount),328,'4 s' if amount>.94 else '',INK,20)
        a.label('4 gaps × 4 s = 16 s',125,459,41,GREEN,c.reveal('four gaps'),bold=True)
        seconds(a,4*sum(p))
    elif n==3:
        paper(a,194,201,892,199)
        x=trace(a,252,321,774,list(range(8)),7,7*c.reveal('pulse numbers',2),first=4)
        for edge in (194,1086):
            a.line([(edge+(6 if k%2 else -2),221+k*12) for k in range(14)],'#596c69',4)
        if c.reveal('twenty one seconds')>0:
            bracket(a,x(0),x(7),345,'21 seconds')
        a.text('How long is one space?',640,487,41,WHITE,opacity=c.reveal('what is the time'),bold=True)
    elif n==4:
        paper(a,85,179,1110,208)
        grow=c.reveal('now fit the paper',2.2)
        # Retained ordinal marks 4 and 11 stay at their correct relative positions.
        minimum,maximum=mix(3,0,grow),mix(10,15,grow)
        pos=lambda i: 149+(i-minimum)/(maximum-minimum)*982
        t0,t1=ceil(minimum),floor(maximum)
        mapped=[i-minimum for i in range(t0,t1+1)]
        shown={idx for idx in range(len(mapped)) if (idx+t0+1) in {1,4,11,16} or grow<.01}
        trace(a,149,305,982,mapped,maximum-minimum,maximum-minimum,first=t0+1,labels=shown)
        bracket(a,pos(3),pos(10),335,'7 gaps',size=22)
        a.label('21 ÷ 7 = 3 s per gap',116,449,36,GREEN,c.reveal('each gap takes three'),bold=True)
        a.label('15 × 3 = 45 s',116,516,36,WHITE,c.reveal('fifteen lots of three'),bold=True)
    elif n in (5,6,7):
        paper(a,65,187,1150,212)
        if n==5:
            x=trace(a,111,308,1058,list(range(19)),18,18*c.reveal('nineteen flashes',2.1),labels={0,18})
            a.text('Pulse order only · spacing hidden',640,349,22,INK)
            a.label('Early gaps: 5 s',94,437,34,AMBER,c.reveal('gaps last five'),bold=True)
            a.label('Later gaps: 3 s',658,437,34,GREEN,c.reveal('shorten to three'),bold=True)
            a.text('First to last: 1 min 10 s',640,525,39,WHITE,opacity=c.reveal('one minute and ten'),bold=True)
        else:
            k=0 if n==6 else 8
            growth=0 if n==6 else c.reveal('eight long gaps',2.6)
            times=list(accumulate([3+2*growth]*k+[3]*(18-k),initial=0))
            x=trace(a,111,301,1058,times,70,times[-1],labels={0,8,18} if n==7 else {0,18})
            if n==6:
                bracket(a,x(0),x(54),330,'18 × 3 s = 54 s')
                if c.reveal('the real strip')>0:bracket(a,x(54),x(70),330,'+16 s',INK,22)
                a.label('Measured: 70 s',94,430,32,CREAM,c.reveal('the real strip'),bold=True)
                a.label('5 − 3 = 2 s extra per long gap',94,505,37,AMBER,c.reveal('changing one short gap'),bold=True)
            else:
                split=times[8]
                bracket(a,x(0),x(split),330,'8 long gaps')
                bracket(a,x(split),x(times[-1]),330,'10 short gaps')
                a.dot(x(split),263,8,INK,c.reveal('pulse nine'))
                a.label('16 ÷ 2 = 8 long gaps',94,434,34,AMBER,c.reveal('eight long gaps'),bold=True)
                a.label('Change after pulse 9',732,434,33,GREEN,c.reveal('pulse nine'),bold=True)
                a.label('8 × 5 + 10 × 3 = 70 s',94,514,37,WHITE,c.reveal('ten gaps of three'),bold=True)
    else:
        paper(a,79,176,1122,211)
        points=list(range(4,25,4))
        x=trace(a,137,297,1001,points,24,24*c.reveal('first flash',2.4))
        a.label('ON',x(0),235,18,INK,bold=True)
        bracket(a,x(4),x(24),325,'Five gaps between the flashes',size=22)
        a.label('Switch on → sixth flash',96,444,29,CREAM,c.reveal('from switch on'))
        a.label('24 s',924,444,39,AMBER,c.reveal('from switch on'),bold=True)
        a.label('First flash → sixth flash',96,509,29,CREAM,c.reveal('from the first flash'))
        a.label('20 s',924,509,39,GREEN,c.reveal('from the first flash'),bold=True)


def poster(draw):
    return draw(4.5,1.5)
