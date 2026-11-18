"""S047. Keep a seat’s identity as each of twelve auditorium rows moves into an end-pair."""
from captioned_film import cue,mix,font
ID='S047';ORIGINAL='5120d8464c1435b640f1f018d45790e9f2ad9274d01c32d4cce8d6df101f4806'
START=(0,15.16,32.44,43.78,56.74,69.04,84.08,98.13,117.16,131.4,145.16);POSTER=113.5
PAPER='#302a32';CREAM='#f8edcd';PALE='#dacfc7';MUSTARD='#f0c077';PINK='#e9958f';TEAL='#94d0c2';SHADOW='#241f25';LINE='#6f6267';BERRY='#945552'
N=[4+3*i for i in range(12)]
def label(c,s,x,y,z=29,col=CREAM,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    z=42
    while font(round(z*c.scale),True).getlength(s)>1145*c.scale:z-=1
    label(c,s,62,60,z)
def seat(c,x,y,u,col):
    # Seen from above, the dark gap separates the upholstered back from the cushion.
    w=.8*u;h=.75*u;c.rect(x-w/2,y-h/2,w,h,SHADOW)
    c.rect(x-w*.45,y-h*.37,w*.9,h*.21,col)
    c.rect(x-w*.43,y-h*.07,w*.86,h*.46,col)
    if u>15:
        c.line([(x-w*.48,y-h*.02),(x-w*.48,y+h*.38)],col,max(1,u*.06))
        c.line([(x+w*.48,y-h*.02),(x+w*.48,y+h*.38)],col,max(1,u*.06))
def stage(c,x,y,w):
    c.line([(x,y),(x+w,y)],LINE,3);label(c,'STAGE',x+w/2,y-14,18,PALE,'mm')
def miniplan(c,counts,x,y,u,built=1,newseats=True):
    for i,n in enumerate(counts):
        if built<i+1:continue
        for j in range(n):
            col=MUSTARD if i and j>=counts[i-1] and newseats else PINK
            seat(c,x+j*u,y+i*(u+18),u,col)
        label(c,str(n),x-25,y+i*(u+18),25,TEAL,'rm')
def intro(c,t):
    title(c,'An arithmetic sequence adds the same amount in each gap')
    p=1+3*cue(t,.6,3.1);miniplan(c,(4,7,10,13),195,179,29,p)
    if t>=4.8:label(c,'4 rows',763,192,35,PINK)
    if t>=7.6:label(c,'3 gaps of +3',763,282,32,MUSTARD)
    if t>=9.6:label(c,'4 + 13 = 17',763,382,31,TEAL)
    if t>=12.2:label(c,'7 + 10 = 17',763,459,31,TEAL)
def discover(c,t):
    title(c,'Look for a fixed increase in the seating plan')
    miniplan(c,(5,8,11),179,210,33,1+2*cue(t,15.2,3.2))
    if t>=22.2:label(c,'8 − 5 = 3',775,205,32,MUSTARD);label(c,'11 − 8 = 3',775,293,32,MUSTARD)
    if t>=29.2:label(c,'Outer rows   5 + 11 = 16',775,410,27,TEAL)
def question(c,t):
    title(c,'Four seats in row one, then three more each time')
    miniplan(c,(4,7),184,228,38,1+cue(t,34.1,1.8))
    label(c,'First term   4',763,232,34,PINK)
    if t>=36.2:label(c,'What are the first four terms?',763,366,26)
def answer(c,t):
    title(c,'Each new row keeps the old seats and adds three')
    miniplan(c,(4,7,10,13),175,168,31,1+3*cue(t,43.8,3.4))
    if t>=46.8:label(c,'4, 7, 10, 13',770,196,38,PINK)
    if t>=50.6:label(c,'4 entries, 3 increases',770,303,29,MUSTARD)
    if t>=53.6:label(c,'3 seats per increase',770,404,28,TEAL)
def strip(c,t,solved):
    title(c,'How many changes separate rows 1 and 14?')
    x0,x1,y=119,1137,302;dx=(x1-x0)/13
    p=13*cue(t,69.2 if solved else 62.4,4.0);c.line([(x0,y),(x1,y)],LINE,3)
    for j in range(14):
        x=x0+j*dx;c.dot(x,y,9,TEAL if j<=p else PALE);label(c,str(j+1),x,y+41,21,PALE,'mm')
        if j<13 and p>j:
            q=min(1,p-j);xx=x+dx*q;c.line([(x,y-23),(x,y-38),(xx,y-38),(xx,y-23)],MUSTARD,2)
    label(c,'Row number',x0,408,25,PALE);label(c,'4 seats at the start',122,176,31,PINK)
    if not solved:
        if t>=60.8:label(c,'Seats in row 14?',751,176,31)
    else:
        if t>=73.4:label(c,'13 × 3 = 39 more seats',637,176,32,MUSTARD)
        if t>=77.2:label(c,'4 + 39 = 43 seats',747,456,34,TEAL)
        if t>=81.2:label(c,'Row 1 has zero gaps.',154,518,28)
def long_q(c,t):strip(c,t,False)
def long_a(c,t):strip(c,t,True)
def start(i,j):
    return (136+(37-N[i])/2*18+j*18,152+i*32)
def target(i,j):
    r=min(i,11-i);col=j if i<6 else N[r]+j
    return (113+col*23.0,165+r*65)
def seatmap(c,built=12,positions=None):
    for i,n in enumerate(N):
        if i>=built:continue
        p=positions[i] if positions is not None else 0
        for j in range(n):
            px,py=start(i,j);xx,yy=target(i,j);seat(c,mix(px,xx,p),mix(py,yy,p),mix(18,23,p),MUSTARD if i<6 else TEAL)
def puzzle(c,t):
    title(c,'Count the seats in a twelve-row theatre section')
    stage(c,205,119,503)
    built=1+11*cue(t,87.9,3.63);seatmap(c,built)
    label(c,'Front row   4',858,209,33,MUSTARD)
    if t>=88:label(c,'Each new row   +3',858,303,29,PINK)
    if t>=91:label(c,'12 rows altogether',858,391,29,TEAL)
    if t>=93:label(c,'Total seats?',858,487,31)
def move_rows(c,t):
    title(c,'Bring the front and back rows together')
    phases=[]
    for i in range(12):
        r=min(i,11-i);at=102.4 if r==0 else 106.0+(r-1)*.76
        phases.append(cue(t,at,1.42))
    seatmap(c,12,phases)
    if t<102.4:
        label(c,'Back row   37',858,224,33,TEAL);label(c,'4 + 11 × 3',858,322,30,MUSTARD)
    else:
        for r in range(6):
            if phases[r]>.99:label(c,'41',1102,165+r*65,27,CREAM,'mm')
    if t>=112.4:label(c,'6 × 41 = 246 seats',646,558,34,CREAM,'mm')
def mean(c,t):
    title(c,'Check the total with the mean row length')
    # These rectangles measure row lengths in seats. The average can be fractional.
    p=cue(t,117.3,3.55);x=194;u=14.2
    for i,n in enumerate(N):
        y=160+i*32;w=mix(n,20.5,p)*u;c.rect(x,y,w,17,MUSTARD if i<6 else TEAL);label(c,str(i+1),x-13,y+8,17,PALE,'rm')
    if t>=121:label(c,'(4 + 37) ÷ 2 = 20½',768,212,30,TEAL)
    if t>=123.2:label(c,'Mean seats per row',768,282,27)
    if t>=125:label(c,'12 × 20½ = 246',768,386,33,MUSTARD)
    if t>=128:label(c,'Original seats stay whole.',768,463,26,PALE)
def mistakes(c,t):
    title(c,'Check that the differences really are constant')
    vals=(4,7,10,13) if t<138 else (4,7,10,15)
    miniplan(c,vals,155,171,30,4)
    label(c,'Row 1 is the start.',760,185,30,PINK)
    if t>=134.4:label(c,'Row 4 is 3 changes later.',760,278,27,MUSTARD)
    if t>=138:label(c,'The last gap is now +5.',760,384,28,MUSTARD)
    if t>=139.4:label(c,'The +3 rule has stopped.',760,466,27,TEAL)
def finish(c,t):
    title(c,'Pair opposite rows and look for any middle row')
    # Use a five-row example to make the unpaired centre visible.
    rows=(4,7,10,13,16)
    for i,n in enumerate(rows):
        y=175+i*78;forw=i if i<3 else 4-i
        col=(MUSTARD,TEAL,PINK)[forw]
        for j in range(n):seat(c,150+j*23,y,23,col)
        label(c,str(n),573,y,26,col)
    if t>=149.2:label(c,'5 rows, 4 gaps',755,192,30)
    if t>=151.4:label(c,'4 + 16 = 20',755,272,30,MUSTARD)
    if t>=153.0:label(c,'7 + 13 = 20',755,349,30,TEAL)
    if t>=154.2:label(c,'Row 3 alone has 10.',755,428,28,PINK)
    if t>=156:label(c,'20 + 20 + 10 = 50',755,508,30)
SCENES=(intro,discover,question,answer,long_q,long_a,puzzle,move_rows,mean,mistakes,finish)
def verify():
    assert N[0]==4 and N[-1]==37 and 4+13*3==43
    assert all(a+b==41 for a,b in zip(N[:6],reversed(N[6:])))
    assert sum(N)==246==6*41==12*(4+37)/2
    assert len({target(i,j) for i,n in enumerate(N) for j in range(n)})==246
    assert len({start(i,j) for i,n in enumerate(N) for j in range(n)})==246
    assert sum([4,7,10,13,16])==50
