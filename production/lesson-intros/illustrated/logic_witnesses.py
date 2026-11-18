"""S033. Make the statement, test its truth, and trace the four speakers' implications."""
from itertools import product
from math import atan2,cos,pi,sin
from captioned_film import cue,mix,font
ID='S033';ORIGINAL='5b2e1b604343cb06f22374e7edb08cb268ace1d6ac037fdaee74ba2cc5dc7e23';START=(0,16.12,34.52,49.37,62.17,78.62,92.70,111.23,133.14,149.46,165.46);POSTER=137.9
PAPER='#24263a';INK='#fff2db';SOFT='#c9c8d3';VIOLET='#b29bde';TEAL='#87d4bc';RED='#eca29d';GOLD='#ecc579';LINE='#63647d';DARK='#302f47';HAIR='#383040'
NAMES=('Ava','Ben','Chen','Dara');SKIN=('#f2c3a5','#dba283','#d99e75','#ae765d');COAT=(VIOLET,GOLD,'#88b7d2','#dc9ab2')

def title(c,s):
    sz=42
    while font(round(sz*c.scale),True).getlength(s)>1150*c.scale:sz-=1
    c.text(s,63,63,sz,INK,'lm',True)
def say(c,s,x,y,sz=31,colour=INK):c.text(s,x,y,sz,colour,'lm',True)

def person(c,i,x,y,k=1,state=None):
    # Different silhouettes keep the speaker recognisable before a type is known.
    u=k;r=29*u;h=SKIN[i];col=COAT[i]
    c.poly([(x-45*u,y+63*u),(x-34*u,y+42*u),(x-15*u,y+32*u),(x+15*u,y+32*u),(x+34*u,y+42*u),(x+45*u,y+63*u)],col,None)
    if i in (0,3):c.dot(x+(9 if i==0 else -18)*u,y-6*u,32*u,HAIR)
    c.dot(x,y,r,h)
    if i==0:
        c.poly([(x-28*u,y),(x-23*u,y-24*u),(x-3*u,y-32*u),(x+26*u,y-15*u),(x+11*u,y-13*u),(x-1*u,y-21*u)],HAIR,None)
    elif i==1:
        c.poly([(x-26*u,y-8*u),(x-24*u,y-26*u),(x-12*u,y-32*u),(x-3*u,y-26*u),(x+11*u,y-31*u),(x+25*u,y-17*u),(x+23*u,y-7*u),(x+9*u,y-17*u)],HAIR,None)
    elif i==2:
        c.poly([(x-28*u,y-3*u),(x-24*u,y-23*u),(x-5*u,y-33*u),(x+23*u,y-22*u),(x+26*u,y-8*u),(x+7*u,y-18*u),(x-4*u,y-10*u)],HAIR,None)
        c.line([(x-20*u,y),(x+19*u,y)],HAIR,2*u)
    else:
        for j in range(7):
            a=pi+j*pi/6;c.dot(x+24*u*cos(a),y-2*u+24*u*sin(a),8*u,HAIR)
    for s in (-1,1):c.dot(x+s*10*u,y+2*u,2*u,HAIR)
    c.line([(x-5*u,y+14*u),(x+5*u,y+14*u)],HAIR,1.7*u)
    c.text(NAMES[i],x,y+88*u,round(26*u),INK,bold=True)
    if state is not None:c.text('Truthful' if state else 'Liar',x,y+123*u,round(22*u),TEAL if state else RED,bold=True)

def bubble(c,x,y,w,s,colour=INK):
    c.rect(x,y,w,66,DARK,LINE,2);c.poly([(x+26,y+65),(x+43,y+65),(x+22,y+83)],DARK,LINE,2)
    c.text(s,x+w/2,y+31,29,colour,bold=True)

def arrow(c,a,b,p,colour):
    if p<=0:return
    X=mix(a[0],b[0],p);Y=mix(a[1],b[1],p);c.line([a,(X,Y)],colour,3)
    angle=atan2(b[1]-a[1],b[0]-a[0]);n=12
    c.poly([(X,Y),(X-n*cos(angle-.45),Y-n*sin(angle-.45)),(X-n*cos(angle+.45),Y-n*sin(angle+.45))],colour,None)

def rule(c,x,y,person_type,value):
    a=TEAL if person_type else RED;b=TEAL if value else RED
    c.text('Truthful' if person_type else 'Liar',x,y,30,a,'lm',True)
    c.text('True' if value else 'False',x+255,y,30,b,'lm',True)
    c.text('Fits' if value==person_type else 'Contradiction',x+455,y,28,TEAL if value==person_type else GOLD,'lm',True)

def intro(c,t):
    title(c,'Can the speaker make that statement?');person(c,0,222,327,1.12)
    say(c,'Speaker’s type',440,190,25,SOFT);say(c,'Statement',700,190,25,SOFT)
    if t>=.6:rule(c,443,272,True,True)
    if t>=7:rule(c,443,362,False,False)
    if t>=10:say(c,'Every speaker’s type must fit their own words.',282,524,31,VIOLET)

def uses(c,t):
    title(c,'Test the proposed types against the claim');bubble(c,155,171,363,'“Ben is truthful.”');person(c,0,219,362,.87);person(c,1,508,362,.87)
    if t>=22.6:
        say(c,'Ava',656,180,26,SOFT);say(c,'Ben',821,180,26,SOFT);say(c,'Fits?',1003,180,26,SOFT)
        for j,(a,b) in enumerate(product((True,False),repeat=2)):
            if t<22.6+j*1.15:continue
            y=239+65*j
            for x,v in [(660,a),(824,b)]:say(c,'T' if v else 'L',x,y,31,TEAL if v else RED)
            say(c,'Yes' if a==b else 'No',1011,y,26,TEAL if a==b else GOLD)
        if t>=29:say(c,'Here, the two types must match.',571,534,29,VIOLET)

def ava(c,t):
    title(c,'Could Ava say this consistently?');person(c,0,292,337,1.4)
    if t>=38.8:bubble(c,184,151,348,'“I am a liar.”')
    if t>=42.8:say(c,'Suppose Ava is truthful.',646,257,32,TEAL)
    if t>=44.6:say(c,'Suppose Ava is a liar.',646,363,32,RED)

def ava_check(c,t):
    title(c,'Try each possible type for Ava');bubble(c,115,145,367,'“I am a liar.”');person(c,0,239,348,1.05)
    say(c,'Suppose',488,180,26,SOFT);say(c,'Her claim',741,180,26,SOFT)
    rule(c,478,273,True,False)
    if t>=55.8:rule(c,478,368,False,True)
    if t>=60.2:say(c,'Neither type fits.',552,515,38,GOLD)

def ben(c,t):
    title(c,'Ben speaks. The other person is silent.');person(c,1,249,350,1.15)
    # The second person is deliberately unnamed in the recording.
    c.dot(763,342,30,LINE);c.poly([(714,416),(732,384),(759,372),(787,381),(806,416)],LINE,None);c.text('Other person',762,455,27,SOFT,bold=True)
    if t>=65.4:bubble(c,144,156,458,'“We are both liars.”')
    if t>=70:say(c,'No statement',714,209,30,SOFT)
    if t>=72.4:say(c,'Could Ben be truthful?',361,544,32,GOLD)

def pairs(c,t,start):
    labels=('Ben','Other person','“Both lie”','Fits Ben?');XS=(159,391,670,938)
    for x,s in zip(XS,labels):say(c,s,x,176,26,SOFT)
    rows=[(True,True),(True,False),(False,False),(False,True)]
    for j,(a,b) in enumerate(rows):
        if t<start[j]:continue
        y=250+j*68;v=not a and not b;good=a==v
        if good:c.rect(131,y-27,1016,54,'#334a4e')
        for x,n in zip(XS,('Truthful' if a else 'Liar','Truthful' if b else 'Liar','True' if v else 'False','Yes' if good else 'No')):
            c.text(n,x,y,27,TEAL if n in ('Truthful','True','Yes') else RED if n in ('Liar','False') else GOLD,'lm',True)

def ben_result(c,t):
    title(c,'A liar can make a false claim about the pair');pairs(c,t,(78.7,80,85.4,87.4))
    if t>=90.2:say(c,'Ben lies. The other person tells the truth.',211,553,33,TEAL)

X=(182,484,785,1085)
def network(c,t,known,show):
    for i in range(4):person(c,i,X[i],309,.94,known[i])
    for i,(txt,col) in enumerate((('opposite',RED),('same',TEAL),('same',TEAL))):
        if show[i]<=0:continue
        arrow(c,(X[i]+53,310),(X[i+1]-55,310),show[i],col)
        c.text(txt,(X[i]+X[i+1])/2,270,23,col,bold=True)

def challenge(c,t):
    title(c,'Four people. Which statements fit together?')
    links=[cue(t,s,1.1) for s in (92.75,95.4,97.4)];network(c,t,[None]*4,links)
    if t<95.4:bubble(c,107,148,389,'“Ben is a liar.”')
    elif t<97.4:bubble(c,319,148,449,'“Chen is truthful.”')
    elif t<99.6:bubble(c,667,148,483,'“Dara is truthful.”')
    else:
        bubble(c,580,148,575,'“Ava and Chen are different.”',GOLD)
        if t>=106.6:say(c,'Who is truthful?',421,531,39)

def logic(c,t):
    title(c,'Follow Ava’s and Ben’s claims before guessing a type')
    network(c,t,[None,None,None,True if t>=128.8 else None],(cue(t,115.4,1.4),cue(t,111.4,1.5),1 if t>=124.4 else 0))
    if t>=118.4:
        p=cue(t,118.4,2.45);x=mix(X[0],X[2],p);c.line([(X[0],223),(X[0],190),(x,190)],VIOLET,3)
        if p==1:c.line([(X[2],190),(X[2],223)],VIOLET,3)
    if t>=121.2:c.text('Ava and Chen must be opposite',486,150,28,VIOLET,bold=True)
    if t>=128.8:say(c,'Dara’s statement is true.',354,525,36,TEAL)

def solution(c,t):
    title(c,'Work back from Dara’s true statement');states=[False if t>=138.75 else None,True if t>=137.6 else None,True if t>=134.1 else None,True]
    network(c,t,states,(1,1,1))
    if t<140.4:say(c,'Dara → Chen → Ben → Ava',328,523,33,VIOLET)
    else:
        say(c,'Ava’s claim: false.',148,506,29,RED);say(c,'The other three claims: true.',628,506,29,TEAL)
        if t>=145.8:say(c,'One assignment fits all four statements.',288,566,27,SOFT)

def mistakes(c,t):
    title(c,'A liar’s whole sentence must be false');pairs(c,t,(149.5,150.2,151,155.6))
    if t>=158.8:say(c,'Check the speaker against the entire claim.',251,548,31,GOLD)

def finish(c,t):
    title(c,'Translate, follow the links, then check every claim')
    states=[None]*4 if t<175 else [False,True,True,True]
    network(c,t,states,(cue(t,165.6,1.0),cue(t,167.6,1.0),cue(t,169.2,1.0)))
    if t>=172.2:say(c,'Dara’s claim fixes the first known type.',281,508,31,GOLD)
    if t>=175:say(c,'Each of the four statements now fits its speaker.',233,565,27,SOFT)
SCENES=(intro,uses,ava,ava_check,ben,ben_result,challenge,logic,solution,mistakes,finish)
def verify():
    assert not [a for a in (False,True) if a==(not a)]
    assert [(a,b) for a,b in product((False,True),repeat=2) if a==(not a and not b)]==[(False,True)]
    good=[]
    for a,b,c,d in product((False,True),repeat=4):
        if (a,b,c,d)==(not b,c,d,a!=c):good.append((a,b,c,d))
    assert good==[(False,True,True,True)]
