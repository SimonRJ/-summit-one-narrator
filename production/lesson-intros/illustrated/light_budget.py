"""S051: physically double lit lamps, cancel matched powers, then spend a finite token budget."""
from math import floor
from captioned_film import cue, mix
ID='S051'
ORIGINAL='95db5170e67fc6c07623b8c3df67e3c2d0f86aeeaf583fe2dc0e7a5f355be0ad'
START=(0,17.72,35.,47.77,59.77,72.38,91.26,109.31,131.7,148.02,161.46)
POSTER=128.35
PAPER='#101f30';WHITE='#f6f4db';GOLD='#ffda72';TURQ='#6fe2db';BLUE='#90b9ff';PINK='#ffa497'
SOFT='#b9c9d3';RIM='#3e5364';OFF='#27394c';DARK='#0b1623';GLOW='#735e39'
def txt(c,s,x,y,z=29,col=WHITE,anchor='mm'):
    c.text(s,x,y,z,col,anchor,True)
def title(c,s):txt(c,s,62,60,40,WHITE,'lm')
def lamp(c,x,y,r,on):
    c.dot(x,y,r*1.27,GLOW if on else OFF);c.dot(x,y,r,GOLD if on else RIM)
    c.dot(x-r*.15,y-r*.18,r*.34,WHITE if on else OFF)
def lamp_pos(i,day,centre=(405,337)):
    cols,rows=((2,1),(2,2),(4,2),(4,4))[day-1]
    return centre[0]+(i%cols-(cols-1)/2)*78,centre[1]+(i//cols-(rows-1)/2)*78
def panel(c,phase):
    c.rect(144,134,527,398,DARK,RIM,4)
    current=min(4,floor(phase)+1);p=phase-floor(phase)
    n=2**current
    if current==4:p=0
    for i in range(n):
        a=lamp_pos(i,current)
        if not p:lamp(c,*a,17,True);continue
        # Original lamps occupy the left (or upper) half of the enlarged arrangement.
        nextcols=(2,2,4,4)[current];oldcols=(2,2,4,4)[current-1];nextrows=n*2//nextcols
        col,row=i%oldcols,i//oldcols
        j=row*nextcols+col;k=j+(oldcols if nextcols!=oldcols else nextcols*(nextrows//2))
        b=lamp_pos(j,current+1);d=lamp_pos(k,current+1)
        lamp(c,mix(a[0],b[0],p),mix(a[1],b[1],p),17,True)
        if p>.015:lamp(c,mix(a[0],d[0],p),mix(a[1],d[1],p),17*p,True)
def prompt(c,t):
    title(c,'Two lamps on day one')
    panel(c,cue(t,37.8,2.1))
    txt(c,'Day 1     2 lamps',914,218,32,GOLD)
    if t>=37.8:txt(c,'Each lamp gains a partner.',913,324,26,TURQ)
    if t>=39.4:txt(c,'Day 4     ?',914,440,38)
def solution(c,t):
    title(c,'Every lamp gains a partner at each change')
    phase=sum(cue(t,s,1.05) for s in (48.2,50.1,52.7));panel(c,phase)
    for i,n in enumerate((2,4,8,16)):
        if phase>=i-.01:txt(c,f'Day {i+1}     {n} lamps',933,174+i*70,29,GOLD if i==3 else SOFT)
    if t>=54.2:txt(c,'2 × 2³ = 16',932,514,39,TURQ)
def array(c,x,y,n,col,size=11):
    cols=min(n,8);rows=(n+cols-1)//cols
    for j in range(n):
        c.dot(x+(j%cols-(cols-1)/2)*size,y+(j//cols-(rows-1)/2)*size,size*.35,col)
def intro(c,t):
    title(c,'Add the same amount, or double what is there?')
    for row,seq in enumerate(((2,4,6,8),(2,4,8,16))):
        yy=224+row*186;txt(c,('add 2','double')[row],202,yy,30,(BLUE,GOLD)[row])
        for i,n in enumerate(seq):
            if cue(t,.65+i*.75,1)>0:
                x=448+i*211;array(c,x,yy,n,(BLUE,GOLD)[row],17);txt(c,n,x,yy+65,27)
    if t>=10:txt(c,'Double every term and match equal groups.',640,555,29,TURQ)
def uses(c,t):
    title(c,'One day or all days so far?')
    for i,n in enumerate((1,2,4,8)):
        x=207+i*179;y=292
        if t>=18+i*.65:
            txt(c,'day '+str(i+1),x,y-85,24,SOFT);array(c,x,y,n,GOLD,15);txt(c,n,x,y+74,30,GOLD)
    if t>=24.9:txt(c,'Day 4    8',1004,236,30,GOLD)
    if t>=28:
        c.line([(131,402),(131,419),(814,419),(814,402)],TURQ,3);txt(c,'Through day 4    15',639,481,30,TURQ)
    if t>=32.6:txt(c,'Double the starting amount:  16 on day 4,  30 through day 4.',640,555,24)
def sum_board(c,t,solved):
    title(c,'Match the shared powers of two')
    for row in range(2):
        if row and (not solved and t<65.8 or solved and t<74):continue
        yy=240+row*150
        txt(c,('S','2S')[row],114,yy,37,(BLUE,TURQ)[row])
        progress=cue(t,78.6,3.1) if solved else 0
        for exp in range(row,5+row):
            n=2**exp;x=254+exp*174
            if row and solved and cue(t,74,2.1)<(exp-1)/5:continue
            dy=((-1)**row)*progress*56 if 1<=exp<=4 else 0
            col=(BLUE,TURQ)[row]
            if solved and 1<=exp<=4 and progress>.65:col=RIM
            if not (solved and 1<=exp<=4 and progress==1):
                array(c,x,yy+dy,n,col,12);txt(c,n,x,yy+dy+47,26,col)
            elif row==0:
                c.line([(x-10,311),(x+10,331)],RIM,3);c.line([(x-10,331),(x+10,311)],RIM,3)
    if solved and t>=82:txt(c,'2S − S = 32 − 1',640,510,36,TURQ)
    if solved and t>=86.8:txt(c,'S = 31',640,568,35,GOLD)
    if not solved and t>=65.8:txt(c,'Which groups appear in both rows?',642,528,30,SOFT)
def sum_q(c,t):sum_board(c,t,False)
def sum_a(c,t):sum_board(c,t,True)
COSTS=tuple(3*2**i for i in range(7))
def course_bar(c,shown,limit=True,measured=True):
    origin=133;unit=2.56;y=331
    end=0
    for i,n in enumerate(COSTS):
        width=n*max(0,min(1,shown-i));x=origin+end*unit
        if width:
            c.rect(x,y,width*unit,51,(BLUE,TURQ)[i%2] if i<6 else PINK,DARK,2)
            if width>23:txt(c,n,x+width*unit/2,y+26,22,DARK)
        end+=n
    for n in ((0,189,381) if measured else (0,100,200,300,400)):
        x=origin+n*unit;c.line([(x,y+52),(x,y+68)],SOFT,2);txt(c,n,x,y+94,22,SOFT)
    if limit:
        x=origin+237*unit;c.line([(x,y-65),(x,y+68)],GOLD,4);txt(c,'237 available',x,y-93,27,GOLD)
def stock(c,t,solved):
    title(c,'How many complete days fit inside the budget?')
    if solved:
        shown=6*cue(t,110.3,6.4)+cue(t,121.6,3)
        txt(c,'Total through day n    3 × (2ⁿ − 1)',640,156,31)
    else:
        shown=3*cue(t,94.8,2.6)
        txt(c,'Day 1    3 tokens',406,157,31,GOLD)
        if t>=94.8:txt(c,'Next days    6, 12, …',883,157,30,TURQ)
    course_bar(c,shown,solved or t>=96.6,solved)
    if not solved and t>=102.8:txt(c,'A day counts when its full allotment fits.',640,528,30)
    if solved and t>=117:txt(c,'Through day 6    189',363,500,29,TURQ)
    if solved and t>=121.6:txt(c,'Through day 7    381',918,500,29,PINK)
    if solved and t>=128.4:txt(c,'237 − 189 = 48 left',640,563,31,GOLD)
def project_q(c,t):stock(c,t,False)
def project_a(c,t):stock(c,t,True)
def next_day(c,t):
    title(c,'Can the remaining tokens pay for day seven?')
    # Four equal 48-token packets make exactly 192. The remaining balance fills only one.
    for i in range(192):
        group=i//48;j=i%48;col=GOLD if group==0 else RIM
        x=155+group*246+(j%8)*22;y=214+(j//8)*23
        c.dot(x,y,7,col)
    for i in range(4):txt(c,'48',231+i*246,390,29,GOLD if i==0 else SOFT)
    if t>=134.8:txt(c,'Day 7 needs 192.',640,463,33,PINK)
    if t>=137.4:txt(c,'48 left  <  192 needed',640,528,34,GOLD)
def mistakes(c,t):
    title(c,'Keep the amount for one day separate from the total')
    for i,n in enumerate((2,4,8,16)):
        x=206+i*216;array(c,x,280,n,GOLD,17);txt(c,'day '+str(i+1),x,194,25,SOFT)
    if t>=151.4:txt(c,'On day 4    16',640,412,33,GOLD)
    if t>=153.4:txt(c,'Through day 4    2 + 4 + 8 + 16 = 30',640,492,32,TURQ)
    if t>=156.2:txt(c,'Day 1 has zero doublings.',640,561,25,SOFT)
def finish(c,t):
    title(c,'Prove the stopping day with two consecutive totals')
    course_bar(c,6+cue(t,168.6,2.1))
    if t>=164.6:txt(c,'Day 6 uses 96. Through day 6 uses 189.',640,164,29)
    if t>=170.6:txt(c,'189 ≤ 237 < 381',640,508,42,TURQ)
    if t>=171.6:txt(c,'Six complete days',640,566,30,GOLD)
SCENES=(intro,uses,prompt,solution,sum_q,sum_a,project_q,project_a,next_day,mistakes,finish)
def verify():
    assert [2*2**i for i in range(4)]==[2,4,8,16]
    assert sum(2**i for i in range(5))==32-1==31
    assert sum(COSTS[:6])==189<=237<sum(COSTS)==381
    assert COSTS[6]==192 and 237-189==48
    for d in range(1,5):assert len({lamp_pos(i,d) for i in range(2**d)})==2**d
