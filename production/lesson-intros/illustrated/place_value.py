"""S002: compensation, a scaled area model, and strip-moving algebra."""
import math
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, bounds, ease, mix


def label(a,text,x,y,size=35,colour=WHITE,alpha=1):
    a.label(text,x,y,size,colour,alpha,bold=True)


def number_line(a,y,p,emphasis=1):
    a.path(((250,y),(1030,y)),SOFT,3,p)
    for i,n in enumerate((396,397,398,399,400,401,402,403,404)):
        x=250+i*97.5
        a.path(((x,y-12),(x,y+12)),SOFT,2,p)
        if n in (398,400):
            a.circle((x,y),10,GOLD if n==400 else BLUE,p)
            label(a,str(n),x,y-49,33,GOLD if n==400 else BLUE,p)
    a.arrow((445,y+52),(640,y+52),GOLD,emphasis)
    label(a,'+2',543,y+96,29,GOLD,emphasis)


def intro(a,c):
    a.heading('Round, then adjust',AQUA)
    p=c.after('close to a tidy round number',.9)
    number_line(a,335,c.opening(.8),p)
    label(a,'398 = 400 − 2',640,530,44,WHITE,c.after('put it back together exactly'))


def estimate(a,c):
    a.heading('Estimate before calculating',AQUA)
    p=c.after('Easy problem',.8)
    label(a,'398 + 207',640,242,60,WHITE,p)
    est=c.after('First estimate',.8)
    label(a,'≈',640,341,46,SOFT,est)
    label(a,'400 + 200 = 600',640,428,51,GOLD,est)
    label(a,'A useful size, not the exact answer',640,541,30,SOFT,c.after('sensible answer'))


def compensate(a,c):
    a.heading('Keep the correction',AQUA)
    p=c.after('Write 398',.8)
    q=c.after('Write 207',.8)
    label(a,'398 = 400 − 2',640,225,43,BLUE,p)
    label(a,'207 = 200 + 7',640,317,43,GOLD,q)
    t=c.after('Together that is 600',.8)
    label(a,'600 − 2 + 7 = 600 + 5',640,429,39,WHITE,t)
    label(a,'= 605',640,526,53,AQUA,c.after('giving 605'))


def rectangle(a,c,solve=False):
    # Coordinates use one common scale: the 100:57 rectangle is not stretched.
    if solve: x,y,u=190,250,4.0
    else: x,y,u=330,192,5.6
    w,h=100*u,57*u
    strip=2*u
    if solve:
        p=1
        cut=1
    else:
        p=c.after('imagine a rectangle',1)
        cut=c.after('remove a strip',1.4)
    a.rect(x,y,98*u,h,BLUE,.32*p)
    a.trace(bounds(x,y,98*u,h),p,BLUE,3,False)
    sx=x+98*u+cut*62
    a.rect(sx,y,strip,h,GOLD if cut>.02 else BLUE,.7*p)
    a.trace(bounds(sx,y,strip,h),p,GOLD if cut>.02 else BLUE,2,False)
    a.dimension((x,y-12),(x+w,y-12),'100',SOFT,p,offset=24,size=40)
    a.dimension((x-16,y),(x-16,y+h),'57',SOFT,p,offset=40,size=40)
    if not solve:
        a.arrow((sx+strip+10,y+h*.48),(sx+45,y+h*.48),GOLD,cut)
        label(a,'2 units',sx+115,y+h*.48,35,GOLD,cut)
        label(a,'98 units remain',x+49*u,y+h+38,36,AQUA,cut)
    else:
        first=c.after('large rectangle has area',.8)
        removed=c.after('removed strip has area',.8)
        ans=c.after('Subtracting gives',.8)
        label(a,'57 × 100 = 5,700',900,260,35,BLUE,first)
        label(a,'57 × 2 = 114',900,348,35,GOLD,removed)
        label(a,'5,700 − 114 = 5,586',900,469,36,WHITE,ans)


def medium_prompt(a,c):
    a.heading('57 × 98 as an area',BLUE)
    rectangle(a,c)


def medium_answer(a,c):
    a.heading('Remove the small strip',BLUE)
    rectangle(a,c,True)


def habit(a,c):
    a.heading('The correction must stay visible',AQUA)
    p=c.after('useful round number',.8)
    label(a,'98 = 100 − 2',640,241,48,GOLD,p)
    q=c.after('small adjustment',.8)
    a.arrow((640,293),(640,355),AQUA,q)
    label(a,'57 × 98 = 57 × (100 − 2)',640,435,42,WHITE,q)
    label(a,'5,700 − 114 = 5,586',640,535,40,AQUA,c.after('same relationship'))


def challenge_prompt(a,c):
    a.heading('Which expression is greater?',GOLD)
    p=c.after('Hard problem',.7)
    label(a,'49,996 × 50,004',640,220,51,BLUE,p)
    label(a,'or',640,295,34,SOFT,p)
    label(a,'50,000² − 17',640,365,51,GOLD,p)
    q=c.after('how far each factor',.8)
    a.path(((315,506),(965,506)),SOFT,3,q)
    for x,v,col in ((405,'49,996',BLUE),(640,'50,000',WHITE),(875,'50,004',GOLD)):
        a.circle((x,506),8,col,q);label(a,v,x,556,28,col,q)
    label(a,'−4',522,470,29,BLUE,q)
    label(a,'+4',758,470,29,GOLD,q)


def rotate_strip(a,p):
    # A 4-by-(N−4) strip rotates rigidly into a matching gap.
    # The magnification of 4 is explicitly disclosed on screen.
    cx,cy=mix(630,330,p),mix(390,190,p)
    angle=math.pi/2*p
    points=[]
    for dx,dy in ((-50,-150),(50,-150),(50,150),(-50,150)):
        points.append((cx+dx*math.cos(angle)-dy*math.sin(angle),
                       cy+dx*math.sin(angle)+dy*math.cos(angle)))
    a.polygon(points,GOLD,.55)
    a.path(points+[points[0]],GOLD,4)


def difference(a,c):
    a.heading('Move the extra strip',GOLD)
    label(a,'4-unit strip enlarged; not to scale',640,126,31,SOFT,1)
    a.rect(180,240,400,300,BLUE,.36)
    a.trace(bounds(180,240,400,300),1,BLUE,3,False)
    p=c.after('extra strips cancel',1.8)
    rotate_strip(a,p)
    if p>.96:
        a.trace(bounds(180,140,400,400),1,AQUA,3,False)
        a.rect(480,140,100,100,PINK,.28)
        a.path(((480,140),(580,240)),PINK,2,.6)
        a.path(((580,140),(480,240)),PINK,2,.6)
        label(a,'4 × 4',530,190,23,PINK,1)
    label(a,'N = 50,000',960,210,32,SOFT,1)
    label(a,'(N − 4)(N + 4)',960,280,39,WHITE,1)
    label(a,'= N² − 4²',960,355,39,AQUA,c.after('squared minus 4 squared'))
    label(a,'= N² − 16',960,427,41,BLUE,c.after('minus 16'))
    label(a,'N² − 17',960,491,39,GOLD,c.after('minus 17'))
    label(a,'The product is greater by 1',945,556,30,WHITE,c.after('greater by exactly one'))


def recap(a,c):
    a.heading('Choose a round number',AQUA)
    label(a,'398 + 207  →  605',640,245,42,BLUE,c.after('compensation'))
    label(a,'57 × (100 − 2)',640,360,43,GOLD,c.after('area model'))
    label(a,'(N − 4)(N + 4) = N² − 16',640,475,42,AQUA,c.after('hidden identity'))
    label(a,'Keep every adjustment',640,559,33,WHITE,c.after('small change'))


SCENES=(intro,estimate,compensate,medium_prompt,medium_answer,habit,challenge_prompt,difference,recap)


def draw(art,cues,scene):
    SCENES[scene-1](art,cues)
