"""S039. Distances as slopes and as areas under a speed graph on one time scale."""
from fractions import Fraction as F
from math import hypot
from captioned_film import cue, mix, font

ID = 'S039'
ORIGINAL = '643bb5d6e2472b4f84b116f9bf925b1aacabe6c572710ad4cc044891eeb5df52'
START = (0,17.56,34.04,46.98,59.79,73.36,87.12,103.73,127.56,144.2,161.16)
POSTER = 125.5
PAPER = '#172635'
GRID = '#3e5260'
CREAM = '#fff4dc'
PALE = '#bdd1ce'
TEAL = '#82e2c3'
PEACH = '#ffba89'
SKY = '#a4c8ff'
TINT = '#274d4d'
LILAC = '#d2aff0'

def label(c,s,x,y,size=29,ink=CREAM,anchor='lm'):
    c.text(s,x,y,size,ink,anchor,True)

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1160*c.scale:size-=1
    label(c,s,58,58,size)

def dash(c,a,b,ink=PALE):
    dx=b[0]-a[0];dy=b[1]-a[1];length=hypot(dx,dy)
    if length<1:return
    for i in range(0,int(length),13):
        u=i/length;v=min(1,(i+6)/length)
        c.line([(a[0]+dx*u,a[1]+dy*u),(a[0]+dx*v,a[1]+dy*v)],ink,2)

def axes(c,xmax,ymax,xticks,yticks,xunit,yunit,x0=108,x1=780,top=163,bottom=483):
    def point(x,y):return (x0+(x1-x0)*x/xmax,bottom-(bottom-top)*y/ymax)
    for x,name in xticks:
        px,_=point(x,0)
        if x:c.line([(px,top),(px,bottom+6)],GRID,1)
        label(c,name,px,bottom+24,22,PALE,'mm')
    for y,name in yticks:
        _,py=point(0,y)
        if y:c.line([(x0-6,py),(x1,py)],GRID,1)
        label(c,name,x0-13,py,21,PALE,'rm')
    c.line([(x0,top-5),(x0,bottom),(x1+8,bottom)],PALE,2)
    label(c,yunit,x0,top-34,24);label(c,xunit,x1,bottom+64,24,CREAM,'rm')
    return point

def segment(c,project,a,b,p,ink=TEAL):
    start=project(*a);end=project(mix(a[0],b[0],p),mix(a[1],b[1],p))
    c.line([start,end],ink,5);c.dot(*end,7,ink)

def intro(c,t):
    title(c,'Watch distance grow as time passes')
    pt=axes(c,75,16,[(0,'0'),(30,'30'),(60,'60'),(75,'75')],[(0,'0'),(8,'8'),(16,'16')],'minutes','distance travelled (km)')
    segment(c,pt,(0,0),(60,16),cue(t,.65,5.5))
    if t>=6.6:label(c,'16 km in 1 hour',845,229,33,TEAL)
    if t>=9.2:label(c,'Average speed',845,328);label(c,'total km ÷ total hours',845,376,27,SKY)
    if t>=13.4:
        segment(c,pt,(60,16),(75,16),cue(t,13.4,2.2),PEACH)
        label(c,'Time still passes.',845,458,28,PEACH)

def units(c,t):
    title(c,'One position on the axis can have two time labels')
    x0,x1=159,1100;y=288;c.line([(x0,y),(x1,y)],PALE,4)
    for i in range(7):
        x=mix(x0,x1,i/6);c.line([(x,y-14),(x,y+14)],TEAL,3)
        label(c,str(i*10),x,y+45,28,TEAL,'mm')
        if t>=23.6:label(c,['0','1/6','1/3','1/2','2/3','5/6','1'][i],x,y-53,27,SKY,'mm')
    label(c,'minutes',x0,391,27,TEAL)
    if t>=23.6:label(c,'hours',x0,157,27,SKY)
    if t>=29.8:
        p=cue(t,29.8,1.7);end=mix(x0,x1,5/6*p)
        c.line([(x0,464),(end,464)],PEACH,6);c.dot(end,464,8,PEACH)
        label(c,'50 min and 5/6 h end at the same mark.',x0,530,31,PEACH)

def steady(c,t,worked):
    title(c,'A straight line for a 24 km ride')
    pt=axes(c,3,24,[(i,str(i)) for i in range(4)],[(i,str(i)) for i in (0,8,16,24)],'hours','distance travelled (km)')
    p=1 if worked else cue(t,34.2,3.0);segment(c,pt,(0,0),(3,24),p)
    if not worked:
        label(c,'24 km in 3 hours',844,250,34,TEAL)
        if t>=39.2:label(c,'Distance in 1 hour?',844,356,28,SKY)
        if t>=41.4:dash(c,pt(1,0),pt(1,8),SKY);c.dot(*pt(1,8),8,SKY)
        return
    for i in range(3):
        p=cue(t,47+i*.66,1.15)
        if p:
            c.line([pt(i,8*i),pt(i+p,8*i)],PEACH,3)
            c.line([pt(i+p,8*i),pt(i+p,8*i+8*p)],SKY,3);c.dot(*pt(i+p,8*i+8*p),6,SKY)
    if t>=51:label(c,'1 hour → 8 km',842,222,33,SKY)
    if t>=53.2:label(c,'24 ÷ 3 = 8 km/h',842,326,31,TEAL)
    if t>=55.8:label(c,'3 × 8 km = 24 km',842,427,28,PEACH)

def ride_question(c,t):steady(c,t,False)
def ride_answer(c,t):steady(c,t,True)

def fast(c,t,answer):
    title(c,'Read 50 minutes on a 16 km/h line')
    pt=axes(c,60,16,[(0,'0'),(10,'10'),(20,'20'),(30,'30'),(40,'40'),(50,'50'),(60,'60')],[(0,'0'),(8,'8'),(16,'16')],'minutes','distance travelled (km)')
    segment(c,pt,(0,0),(60,16),1 if answer else cue(t,59.85,2.0))
    p=cue(t,75.6 if answer else 62.2,2.0);y=40/3
    if p:
        a=pt(50,0);b=pt(50,y*p);dash(c,a,b,PEACH);c.dot(*b,7,PEACH)
    if answer:
        label(c,'50/60 = 5/6 h',847,222,31,PEACH)
        if t>=78.2:dash(c,pt(50,y),pt(0,y),PEACH);label(c,'16 × 5/6 = 40/3 km',847,326,28,TEAL)
        if t>=82.4:label(c,'13⅓ km < 16 km',847,432,30,SKY)
    else:
        label(c,'1 hour → 16 km',847,222,32,TEAL)
        if t>=63.8:label(c,'50 min → ?',847,335,36,PEACH)
        if t>=65.4:label(c,'Which part of an hour?',847,435,25,SKY)

def fast_question(c,t):fast(c,t,False)
def fast_answer(c,t):fast(c,t,True)

def outlines(c):
    return axes(c,238,60,[(0,'0'),(50,'50'),(100,'100'),(150,'150'),(200,'200'),(238,'238')],[(i,str(i)) for i in (0,15,30,45,60)],'elapsed minutes','distance travelled (km)')

def three_legs(c,pt,k1,k2,k3):
    segment(c,pt,(0,0),(100,30),k1)
    if k2>0:segment(c,pt,(100,30),(118,30),k2,PEACH)
    if k3>0:segment(c,pt,(118,30),(238,60),k3,SKY)

def challenge(c,t):
    title(c,'Out, rest, return. Keep counting distance on the way home.')
    pt=outlines(c);three_legs(c,pt,cue(t,87.25,2.9),cue(t,90.1,2.4),cue(t,92.65,3.1))
    label(c,'Out   30 km at 18 km/h',837,191,27,TEAL)
    if t>=90:label(c,'Stop   18 min',837,276,29,PEACH)
    if t>=92.6:label(c,'Back   30 km at 15 km/h',837,360,26,SKY)
    if t>=97:label(c,'Whole-trip average?',837,466,30)

def solution(c,t):
    title(c,'The slope from the first point to the last gives the average')
    pt=outlines(c);three_legs(c,pt,1,1,1)
    for x,s in ((100,106.8),(118,111.2),(238,112.6)):
        if t>=s:dash(c,pt(x,0),pt(x,30 if x!=238 else 60))
    if t>=106.8:label(c,'100 min out',850,181,28,TEAL)
    if t>=109.4:label(c,'120 min back',850,229,28,SKY)
    if t>=111.2:label(c,'18 min stopped',850,278,28,PEACH)
    if t>=112.6:label(c,'238 min in total',850,341,29)
    if t>=115.6:label(c,'60 km travelled',850,391,29)
    if t>=119.4:
        p=cue(t,119.4,2.1);dash(c,pt(0,0),pt(238*p,60*p),LILAC)
        label(c,'60 ÷ (238/60)',850,450,29,LILAC)
    if t>=122.2:label(c,'= 1800/119 km/h',850,506,30,LILAC)

def speed_area(c,t):
    title(c,'Time determines the width of each speed block')
    pt=axes(c,238,20,[(0,'0'),(50,'50'),(100,'100'),(150,'150'),(200,'200'),(238,'238')],[(0,'0'),(5,'5'),(10,'10'),(15,'15'),(20,'20')],'elapsed minutes','speed (km/h)')
    for x1,x2,speed,ink,start in ((0,100,18,TEAL,127.6),(118,238,15,SKY,128.8)):
        p=cue(t,start,1.7);a=pt(x1,speed);b=pt(x1+(x2-x1)*p,0)
        if p:c.rect(a[0],a[1],b[0]-a[0],b[1]-a[1],TINT,ink,2)
        if p>=1:label(c,'30 km',*(pt((x1+x2)/2,speed/2)),26,ink,'mm')
    if t>=132.6:label(c,'Equal areas',841,200,33,TEAL);label(c,'Different widths in time',841,249,26,SKY)
    if t>=136.8:
        a,b=pt(100,0),pt(118,0);c.line([a,b],PEACH,8)
        label(c,'18 min at 0 km/h',841,331,28,PEACH)
    if t>=139.8:
        y=1800/119;dash(c,pt(0,y),pt(238,y),LILAC)
        label(c,'Whole-trip average',841,426,29,LILAC);label(c,'≈ 15.13 km/h',841,473,28,LILAC)

def units_check(c,t):
    title(c,'Convert the rate or convert the time')
    label(c,'16 kilometres per hour for 50 minutes',120,162,37)
    if t>=146.8:label(c,'50 min = 5/6 h',124,270,35,PEACH)
    if t>=149:label(c,'16 × 5/6 = 40/3 km',652,270,35,TEAL)
    if t>=151.8:label(c,'16/60 = 4/15 km/min',124,375,34,SKY);label(c,'(4/15) × 50 = 40/3 km',652,375,31,TEAL)
    if t>=156.6:label(c,'A stop belongs in the total time.',124,500,32,LILAC)

def summary(c,t):
    title(c,'Keep one row for each stage')
    for x,s in ((133,'Stage'),(430,'Speed'),(695,'Distance'),(972,'Time')):label(c,s,x,145,28,PALE)
    for j,(stage,speed,km,mins,ink) in enumerate((('Out','18 km/h','30 km','100 min',TEAL),('Stopped','0 km/h','0 km','18 min',PEACH),('Return','15 km/h','30 km','120 min',SKY))):
        if t<161.16+j*.65:continue
        y=211+j*67
        for x,s in ((133,stage),(430,speed),(695,km),(972,mins)):label(c,s,x,y,29,ink)
    if t>=167.4:c.line([(122,397),(1135,397)],GRID,3)
    if t>=171.4:
        for x,s in ((133,'Whole trip'),(695,'60 km'),(972,'238 min')):label(c,s,x,446,30)
        label(c,'60 ÷ (238/60) = 1800/119 km/h',238,552,35,LILAC)

SCENES=(intro,units,ride_question,ride_answer,fast_question,fast_answer,challenge,solution,speed_area,units_check,summary)

def verify():
    assert F(24,3)==8 and F(16)*F(50,60)==F(40,3)
    trip=((F(100,60),18),(F(18,60),0),(F(120,60),15))
    assert [t*v for t,v in trip]==[30,0,30]
    assert sum(t for t,_ in trip)==F(238,60)
    assert sum(t*v for t,v in trip)/sum(t for t,_ in trip)==F(1800,119)
