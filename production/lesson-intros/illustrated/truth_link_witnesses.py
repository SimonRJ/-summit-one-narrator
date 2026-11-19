"""A truth-type investigation, drawn against the approved S068 recording."""
from itertools import product

from captioned_film import cue, mix

ID = 'S068'
ORIGINAL = 'f6d8331504182bc498a45d0501b2217efc49a693a99e620ed88400bb0d38c844'
START = (0, 16.12, 34.04, 49.53, 62.33, 78.78, 92.86, 110.91, 132.98, 149.30, 165.30)
POSTER = 131.75
PAPER = '#172337'
PANEL = '#22324a'
EDGE = '#4b6278'
WHITE = '#faf6df'
MUTED = '#bdd0dc'
MINT = '#8ce0c9'
CORAL = '#ffb399'
GOLD = '#f5d474'
LILAC = '#ccbbfa'
SKINS = ('#bc785d', '#efb689', '#915a48', '#d29971', '#bf856a')
HAIR = ('#432f40', '#34313b', '#30293a', '#4a3431', '#3a3345')
COATS = (LILAC, '#7bc7ea', GOLD, '#db97b5', '#c0ced8')
PEOPLE = ('Iris', 'Kai', 'Lia', 'Mo', 'Partner')


def txt(c, value, x, y, size=32, ink=WHITE, bold=False):
    c.text(value, x, y, size, ink, bold=bold)


def title(c, value):
    c.text(value, 48, 51, 42, WHITE, 'lm', True)
    c.line([(50, 92), (1228, 92)], EDGE, 2)


def bar(c, x, y, w, h, value, ink=MINT, size=29):
    c.rect(x-w/2, y-h/2, w, h, PANEL, ink, 2)
    txt(c, value, x, y-1, size, ink, True)


def arrow(c, a, b, t, ink=MUTED, width=4):
    x,y = a
    dx,dy = b[0]-x,b[1]-y
    if t <= 0: return
    end = (x+t*dx, y+t*dy)
    c.line([a,end],ink,width)
    length = (dx*dx + dy*dy)**.5
    u,v = dx/length,dy/length
    ex,ey=end
    c.poly([(ex,ey),(ex-16*u+7*v,ey-16*v-7*u),(ex-16*u-7*v,ey-16*v+7*u)],ink,None)


def person(c, name, x, y, r=48):
    """Unique hair, collar and profile make each witness recognisable in monochrome."""
    i=PEOPLE.index(name)
    def pts(points): return [(x+r*a,y+r*b) for a,b in points]
    c.dot(x,y,r,COATS[i])
    c.dot(x,y,r*.91,HAIR[i])
    c.dot(x,y+r*.01,r*.67,SKINS[i])
    # Different fringe silhouettes: sloped, curled, plaited, and close cropped.
    fringes=[
        [(-.72,-.12),(-.61,-.71),(.21,-.86),(.70,-.37),(.66,-.12),(.27,-.53),(.01,-.31),(-.22,-.42)],
        [(-.71,-.17),(-.62,-.61),(-.43,-.73),(-.45,-.88),(-.08,-.74),(.28,-.88),(.31,-.72),(.68,-.58),(.63,-.28),(.19,-.43),(-.30,-.35)],
        [(-.67,-.07),(-.62,-.65),(-.16,-.78),(.43,-.68),(.70,-.41),(.64,-.08),(.46,-.33),(.21,-.44),(.0,-.54),(-.30,-.34)],
        [(-.66,-.10),(-.62,-.55),(-.29,-.68),(.37,-.68),(.65,-.44),(.67,-.15),(.40,-.46),(-.42,-.45)],
        [(-.68,-.22),(-.61,-.64),(.25,-.75),(.65,-.45),(.66,-.19),(.12,-.43),(-.22,-.32)]]
    c.poly(pts(fringes[i]),HAIR[i],None)
    if i==2:
        for xx,yy in ((-.68,.10),(-.70,.35),(.67,.10),(.70,.35)):
            c.dot(x+xx*r,y+yy*r,.17*r,HAIR[i])
    if i==3:
        c.line(pts([(-.48,-.04),(-.08,-.04),(.09,-.04),(.48,-.04)]),HAIR[i],max(2,.05*r))
    for xx in (-.245,.245): c.dot(x+xx*r,y-r*.035,max(2,.055*r),HAIR[i])
    c.line(pts([(-.18,.29),(-.04,.34),(.11,.33),(.20,.27)]),HAIR[i],max(2,r*.045))
    c.poly(pts([(-.73,.61),(-.36,.45),(0,.68),(.35,.45),(.72,.62),(.58,.83),(0,.97),(-.56,.85)]),COATS[i],None)


def card(c,name,x,y,claim,width=510):
    c.rect(x-width/2,y-65,width,130,PANEL,EDGE,2)
    person(c,name,x-width/2+72,y,42)
    c.text(name,x-width/2+134,y-27,26,COATS[PEOPLE.index(name)],'lm',True)
    c.text(claim,x-width/2+134,y+23,30,WHITE,'lm',True)


def mark(c,x,y,ok,p=1):
    if p<=0:return
    col=MINT if ok else CORAL
    if ok:
        c.line([(x-12,y),(x-4,y+8),(x-4+20*p,y+8-23*p)],col,5)
    else:
        c.line([(x-10,y-10),(x-10+20*p,y-10+20*p)],col,5)
        c.line([(x-10,y+10),(x-10+20*p,y+10-20*p)],col,5)


def intro(c,t):
    title(c, 'Match the speaker to the truth of the claim')
    bar(c,275,187,340,64,'Speaker’s type',MUTED)
    bar(c,984,187,397,64,'Value of the statement',MUTED)
    if t<5.3:
        arrow(c,(460,187),(770,187),cue(t,.8,2.2),GOLD)
        if t>=2.7: txt(c,'The type must agree with the statement.',640,385,38,GOLD,True)
    for y,name,val,at,color in [(303,'Truth-teller','true',5.36,MINT),(416,'Liar','false',7.6,CORAL)]:
        if t<at:continue
        txt(c,name,275,y,42,color,True)
        arrow(c,(455,y),(784,y),cue(t,at,.85),color)
        if t>at+.38: txt(c,val,984,y,46,color,True)
    if t>=10.0:
        txt(c,'Read the sentence as a condition.',640,542,34,WHITE,True)


def exam(c,t):
    title(c,'Which claims can hold together?')
    card(c,'Iris',642,184,'“Kai is truthful.”',600)
    if t<21.8:return
    yy=308
    for x,v in [(294,'Suppose Iris is…'),(680,'For her claim to fit…'),(1020,'Kai must be…')]:
        txt(c,v,x,yy,25,MUTED,True)
    for j,(who,v,peer,at) in enumerate([('truthful','true','truthful',22.46),('a liar','false','a liar',23.4)]):
        if t < at:continue
        y=386+83*j;col=(MINT,CORAL)[j]
        txt(c,who,294,y,31,col,True)
        arrow(c,(405,y),(551,y),cue(t,at,.6),col)
        txt(c,v,680,y,34,col,True)
        arrow(c,(788,y),(899,y),cue(t,at+.25,.6),col)
        txt(c,peer,1020,y,31,col,True)
    if t>=28.78:
        txt(c,'Same types fit. Opposite types contradict the statement.',640,554,31,GOLD,True)


def iris_claim(c):
    person(c,'Iris',259,251,83)
    txt(c,'Iris',259,376,41,LILAC,True)
    c.poly([(363,248),(412,224),(412,275)],PANEL,EDGE,2)
    c.rect(409,174,709,144,PANEL,EDGE,2)
    txt(c,'“I am a liar.”',765,244,58,WHITE,True)


def paradox(c,t):
    title(c,'Could someone say this about themself?')
    if t<38.84:
        txt(c,'Each person is either truthful or a liar.',640,266,39,MUTED,True)
    else: iris_claim(c)
    if t>=43.08:
        bar(c,449,483,280,65,'Try truthful',MINT,31)
    if t>=44.76:
        bar(c,851,483,280,65,'Try liar',CORAL,31)
    if t>=46:
        txt(c,'Compare the claim with the proposed type.',640,564,28,MUTED)


def iris_cases(c,t):
    title(c,'Test both possibilities for Iris')
    card(c,'Iris',641,181,'“I am a liar.”',550)
    for j,(lhs,rhs,at,fail,col) in enumerate([('Iris is truthful','claim is false',49.53,53.61,MINT),('Iris is a liar','claim is true',55.77,58.35,CORAL)]):
        y=313+j*99
        if t>=at: bar(c,305,y,326,64,lhs,col,32)
        if t>=at+.6:arrow(c,(476,y),(680,y),cue(t,at+.6,.7))
        if t>=at+1.1:txt(c,rhs,850,y,36,WHITE,True)
        mark(c,1098,y,False,cue(t,fail,.6))
    if t>=60.53:
        txt(c,'Neither type fits this sentence.',640,541,39,GOLD,True)


def kai_question(c,t):
    title(c,'One statement about two people')
    for i,name in enumerate(('Kai','Partner')):
        x=345+608*i
        person(c,name,x,209,71)
        txt(c,'Kai' if not i else 'Silent partner',x,315,38,COATS[PEOPLE.index(name)],True)
    if t>=65.49:
        bar(c,640,414,780,82,'Kai: “We are both liars.”',WHITE,44)
    if t>=70.11:
        txt(c,'Only Kai speaks. “Both” requires two liars.',640,523,35,GOLD,True)


def kai_proof(c,t):
    title(c,'What makes “both liars” false?')
    xs=(253,552,863,1094)
    for x,v in zip(xs,('Kai','Partner','Both liars?','Fits Kai?')):
        txt(c,v,x,151,29,MUTED,True)
    rows=[('truthful','truthful','false',False,78.9),('truthful','liar','false',False,80.2),('liar','liar','true',False,85.1),('liar','truthful','false',True,87.6)]
    for idx,(a,b,v,ok,at) in enumerate(rows):
        y=225+idx*78
        if t<at:continue
        c.rect(110,y-30,1060,60,('#2b4845' if ok else PANEL),MINT if ok else EDGE,2)
        for x,label in zip(xs,(a,b,v)):
            txt(c,label,x,y,34,MINT if label in ('truthful','true') else CORAL,True)
        mark(c,xs[-1],y,ok,cue(t,at+.15,.35))
    if t>=90:
        txt(c,'Kai lies. The partner tells the truth.',640,563,34,WHITE,True)


CLAIMS=(('Iris','“Kai is truthful.”'),('Kai','“Lia is a liar.”'),('Lia','“Mo is truthful.”'),('Mo','“Iris and Lia are the same type.”'))


def puzzle(c,t):
    title(c,'Four witnesses. Who tells the truth?')
    for i,((name,claim),at) in enumerate(zip(CLAIMS,(92.86,95.44,96.70,99.50))):
        if t<at:continue
        x=335+610*(i%2);y=205+181*(i//2)
        w=558
        c.rect(x-w/2,y-73,w,146,PANEL,EDGE,2)
        person(c,name,x-196,y,44)
        c.text(name,x-121,y-38,27,COATS[i],'lm',True)
        if i<3: c.text(claim,x-121,y+15,32,WHITE,'lm',True)
        else:
            c.text('“Iris and Lia are',x-123,y+1,30,WHITE,'lm',True)
            c.text('the same type.”',x-123,y+39,30,WHITE,'lm',True)
    if t>=102.72:
        txt(c,'Each speaker is always truthful or always lies.',640,552,32,GOLD,True)


NODES=(194,485,778,1073)


def link(c,i,j,t,at,kind):
    a=NODES[i];b=NODES[j]
    col=MINT if kind=='same' else CORAL
    # Matching claims have parallel rails. Opposite types cross over.
    p=cue(t,at,1.0)
    if not p:return
    l,r=a+54,b-54
    for k in (-1,1):
        end=1 if kind=='same' else -1
        c.line([(l,233+12*k),(mix(l,r,p),233+12*k*mix(1,end,p))],col,4)
    txt(c,kind,(a+b)/2,177,28,col,True)


def band(c,labels=None):
    for x,(name,_),i in zip(NODES,CLAIMS,range(4)):
        person(c,name,x,233,48)
        txt(c,name,x,312,32,COATS[i],True)
        if labels and labels[i]:
            value=labels[i]
            bar(c,x,376,185,55,value,MINT if value=='truthful' else CORAL,29)


def chain(c,t):
    title(c,'Translate each statement into a link')
    band(c)
    link(c,0,1,t,110.91,'same')
    link(c,1,2,t,115.05,'opposite')
    if t>=117.89:
        # A bracket connects Iris directly to Lia as the two links are composed.
        p=cue(t,117.89,2.8)
        c.line([(NODES[0],352),(NODES[0],390),(mix(NODES[0],NODES[2],p),390)],GOLD,4)
        if p==1:c.line([(NODES[2],352),(NODES[2],390)],GOLD,4)
        if t>=120.69: txt(c,'Iris and Lia are opposite.',486,438,34,GOLD,True)
    if t>=124.01:
        txt(c,'Mo says “same”.',1035,428,30,COATS[3],True)
    if 128.37<=t<130.83: txt(c,'False',1035,482,31,CORAL,True)
    if t>=130.83:
        bar(c,640,544,815,63,'Mo’s claim is false, so Mo is a liar.',CORAL,32)


def backsolve(c,t):
    title(c,'Work back from the one forced type')
    times=(138.55,137.14,135.7,132.98)
    labels=[value if t>=at else '' for value,at in zip(('truthful','truthful','liar','liar'),times)]
    band(c,labels)
    for i,k,at in ((2,'same',133.15),(1,'opposite',137.14),(0,'same',138.55)):
        link(c,i,i+1,t,at,k)
    if t<140.08: return
    lines=(('Iris: Kai truthful','true',140.08),('Kai: Lia a liar','true',140.7),('Lia: Mo truthful','false',140.4),('Mo: Iris = Lia','false',141.2))
    for i,(claim,value,at) in enumerate(lines):
        if t<at:continue
        x=188+i*302
        txt(c,claim,x,481,24,WHITE,True)
        txt(c,value,x,525,26,MINT if value=='true' else CORAL,True)
        mark(c,x+73,526,True,cue(t,at+.15,.35))
    if t>=146.5:txt(c,'All four claims fit. Each reverse step was forced.',640,582,28,GOLD,True)


def warning(c,t):
    title(c,'Negate the whole sentence')
    bar(c,640,163,706,62,'Claim: “Both people lie.”',WHITE,32)
    for i,(a,b) in enumerate((('liar','liar'),('liar','truthful'),('truthful','liar'),('truthful','truthful'))):
        at=(149.7,153,154.1,155.3)[i]
        if t<at:continue
        x=180+i*310
        col=MINT if i==0 else CORAL
        c.rect(x-129,266,258,158,PANEL,col,2)
        txt(c,a,x,305,31,WHITE,True)
        txt(c,b,x,352,31,WHITE,True)
        txt(c,'true' if i==0 else 'false',x,395,25,col,True)
    if t>=156.5:
        txt(c,'One or two truthful people make “both lie” false.',640,496,36,GOLD,True)
    if t>=161.04:
        txt(c,'Then check the type of the person who actually spoke.',640,554,30,MUTED)


def recap(c,t):
    title(c,'A routine for the next logic puzzle')
    rows=[('1','Translate','“Kai is truthful” means the speaker and Kai match.',165.4,MINT),
          ('2','Link','“Lia lies” means the speaker and Lia are opposite.',167.44,CORAL),
          ('3','Force','A chain can settle another claim before you guess.',171.96,GOLD),
          ('4','Check','Test every sentence against its own speaker’s type.',174.82,LILAC)]
    for i,(n,verb,words,at,col) in enumerate(rows):
        y=181+i*110
        if t<at:continue
        x=mix(34,75,cue(t,at,.5))
        c.dot(x,y,25,col)
        txt(c,n,x,y,29,PAPER,True)
        c.text(verb,133,y,32,col,'lm',True)
        c.text(words,327,y,28,WHITE,'lm')


SCENES=(intro,exam,paradox,iris_cases,kai_question,kai_proof,puzzle,chain,backsolve,warning,recap)


def verify():
    possibilities=tuple(product((False,True),repeat=2))
    assert not any(iris==(not iris) for iris in (False,True))
    assert [(k,p) for k,p in possibilities if k==((not k) and (not p))]==[(False,True)]
    consistent=[]
    for i,k,l,m in product((False,True),repeat=4):
        if (i,k,l,m)==(k,not l,m,i==l): consistent.append((i,k,l,m))
    assert consistent==[(True,True,False,False)]
    assert len(START)==len(SCENES)==11
