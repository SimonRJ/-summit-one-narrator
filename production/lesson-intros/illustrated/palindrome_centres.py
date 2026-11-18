"""S055: mirror typesetter, split place values and a live table of every permitted centre."""
from captioned_film import cue,mix
ID='S055'
ORIGINAL='53ca544307dd158b98da75dcf9da664f4c940f6e3d8d10cb8f6133fe5d0d73a1'
START=(0,14.36,29.72,44.57,59.93,75.1,99.25,116.5,146.24,162.08,178.88)
POSTER=157.7
PAPER='#2b253c';INK='#f8eff3';GOLD='#ffc98a';LILAC='#d4b2ff';GREEN='#98dfcb'
DIM='#b6abc5';EDGE='#655773';BOX='#392f49';RED='#ff9c9f'
def word(c,s,x,y,z=29,col=INK,anchor='mm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):word(c,s,60,62,40,INK,'lm')
def key(c,x,y,v,col,r=43):
    c.rect(x-r,y-r,2*r,2*r,BOX,col,3);word(c,v,x,y+2,r*1.05,col)
def dotted(c,x,y0,y1):
    for y in range(y0,y1,14):c.line([(x,y),(x,min(y+7,y1))],EDGE,2)
def reflection(c,t,chars='27372',starts=(1,2,3),home=640,y=306,dx=143,show=False):
    xl=[home+(i-2)*dx for i in range(5)];cols=(GOLD,LILAC,GREEN,LILAC,GOLD)
    dotted(c,home,135,478)
    for i in range(5):
        value=chars[i] if i<=2 or show else ''
        key(c,xl[i],y,value,cols[i])
    for i,at in [(1,starts[1]),(0,starts[2])]:
        p=cue(t,at,1.45)
        if p:
            xx=mix(xl[i],xl[4-i],p);yy=y-95*4*p*(1-p)
            if p<1:c.dot(xx,yy,29,BOX)
            word(c,chars[i],xx,yy+1,45,cols[i])
def intro(c,t):
    if t<7.4:
        title(c,'A mirror fixes the matching digit positions')
        reflection(c,t,'27372',(0,3.6,4.8))
    else:
        title(c,'A repunit has a 1 in every place')
        for i in range(4):
            x=352+i*175;key(c,x,281,'1',LILAC)
            if t>=10.0:word(c,('1000','100','10','1')[i],x,382,29,DIM)
        if t>=12:word(c,'1111 is the sum of these four place values.',640,512,31,GREEN)
def exam(c,t):
    title(c,'The right-hand digits are determined by the left')
    reflection(c,t,'45154',(0,16.8,18.2),y=299)
    if t>=22.4:word(c,'Digit sum   4 + 5 + 1 + 5 + 4 = 19',639,477,31)
    if t>=26.2:word(c,'Changing one outer digit changes its partner.',639,545,27,GOLD)
def places(c,t,solved):
    title(c,'Multiply four independent places')
    for i,place in enumerate(('thousands','hundreds','tens','ones')):
        x=255+245*i;word(c,place,x,158,24,DIM)
        key(c,x,243,'1',LILAC,40)
        word(c,'× 4',x,329,29,GOLD)
        visible=solved and t>=44.6+(3-i)*.5
        if visible:key(c,x,421,'4',GREEN,39)
        elif not solved:word(c,'?',x,421,39,DIM)
    if solved and t>=50.2:word(c,'4 < 10 in every column. No carry.',640,513,29,GOLD)
    if solved and t>=52.6:word(c,'1111 × 4 = 4444',640,568,34,GREEN)
def basic_q(c,t):places(c,t,False)
def basic_a(c,t):places(c,t,True)
def pair_q(c,t):
    title(c,'Split 3663 into its outer and inner places')
    for i,(v,col) in enumerate(zip('3663',(GOLD,LILAC,LILAC,GOLD))):
        x=379+174*i;key(c,x,302,v,col)
    if t>=65.6:word(c,'3663 ÷ 11 = ?',640,181,34)
    if t>=67.4:
        c.line([(379,355),(379,432),(901,432),(901,355)],GOLD,3)
        c.line([(553,355),(553,393),(727,393),(727,355)],LILAC,3)
def pair_a(c,t):
    title(c,'Place value turns the pairs into multiples of eleven')
    for i,(v,col) in enumerate(zip('3663',(GOLD,LILAC,LILAC,GOLD))):
        outer=i in (0,3);x=166+i*133;y=348
        p=cue(t,75.2 if outer else 79.6,2.0);target=241 if outer else 423
        key(c,x,mix(y,target,p),v,col,36)
        if p>.9:word(c,'0',x,423 if outer else 241,36,EDGE)
    if t>=78:word(c,'3003 = 3 × 1001',922,222,30,GOLD)
    if t>=81.8:word(c,'660 = 6 × 110',922,303,30,LILAC)
    if t>=83.6:word(c,'1001 ÷ 11 = 91',922,391,26,GOLD)
    if t>=87:word(c,'110 ÷ 11 = 10',922,445,26,LILAC)
    if t>=92.4:word(c,'3 × 91 + 6 × 10'+(' = 333' if t>=96.2 else ''),661,544,33,GREEN)
def digit_q(c,t):
    title(c,'Count five-digit palindromes divisible by 9')
    reflection(c,t,'ABCBA',(0,107.2,105.0),y=293)
    if t>=102.8:word(c,'A can be 1, 2, 3, 4 or 5.',640,453,29,GOLD)
    if t>=109.2:word(c,'Which centre digits C work?',640,524,30,GREEN)
def formula(c,t):
    title(c,'Make the digit sum divisible by 9')
    if t<132.2:
        chars='ABCBA' if t<127.8 else '24642'
        reflection(c,t,chars,(0,0,0),y=266,show=True)
        if t>=124.2:word(c,'digit sum = 2A + 2B + C',640,416,35,GREEN)
        if t>=127.8:word(c,'A = 2,  B = 4     12 + C = 18',640,509,29,LILAC)
    else:
        for i in range(10):
            x=179+i*101;col=GOLD if i in (0,9) and t>=137.4 else LILAC
            key(c,x,307,i,col,32);word(c,i%9,x,399,26,col)
        word(c,'centre digit C',640,195,27,DIM);word(c,'remainders modulo 9',640,467,25,DIM)
        if t>=139.6:word(c,'0 and 9 share the same remainder.',640,530,31,GOLD)
def centre(a,b):return (-2*(a+b))%9
def all_pairs(c,t):
    title(c,'Count every legal centre digit')
    y0=192;x0=214;dx=76;dy=58
    word(c,'B',x0+4.5*dx,119,24,LILAC);word(c,'A',82,y0+2*dy,25,GOLD)
    for b in range(10):word(c,b,x0+b*dx,y0-43,22,DIM)
    for a in range(1,6):
        y=y0+(a-1)*dy;word(c,a,133,y,25,GOLD)
        for b in range(10):
            x=x0+b*dx;c.rect(x-32,y-23,64,46,BOX,EDGE,1)
            extra=centre(a,b)==0
            word(c,centre(a,b),x,y,25,GREEN)
            if extra and t>=146.45+.55*(a-1):
                c.rect(x-32,y-23,64,46,BOX,GOLD,3);word(c,'0, 9',x,y,21,GOLD)
    if t>=149.4:word(c,'5 rows × 10',1072,214,26)
    if t>=151.8:word(c,'5 extra centres',1072,303,24,GOLD)
    if t>=154.2:word(c,'50 + 5',1072,391,34,GREEN)
    if t>=156.2:word(c,'55 palindromes',640,550,36,GREEN)
def caution(c,t):
    title(c,'Check the first digit and the two endpoints')
    if t<170.2:
        reflection(c,t,'03230',(0,0,0),y=285,show=True)
        if t>=164:word(c,'The leading 0 drops away. 3230 has four digits.',640,474,31,RED)
    else:
        for row,s in enumerate(('27072','27972')):
            for i,v in enumerate(s):key(c,363+i*137,237+row*151,v,GREEN if i==2 else LILAC,33)
        word(c,'sum 18',1101,237,27,GOLD);word(c,'sum 27',1101,388,27,GOLD)
        if t>=176:word(c,'Both centre digits give multiples of 9.',640,524,31,GREEN)
def final(c,t):
    title(c,'Three choices determine all five places')
    reflection(c,t,'24642',(0,182.0,183.1),y=285)
    if t>=184.8:word(c,'2 × 2 + 2 × 4 + 6 = 18',640,455,34,GREEN)
    if t>=188.6:word(c,'Only C = 6 works for this outer pair.',640,534,29,LILAC)
SCENES=(intro,exam,basic_q,basic_a,pair_q,pair_a,digit_q,formula,all_pairs,caution,final)
def verify():
    candidates={10001*a+1010*b+100*c for a in range(1,6) for b in range(10) for c in {centre(a,b),9} if (2*a+2*b+c)%9==0}
    brute={n for n in range(10000,60000) if str(n)==str(n)[::-1] and n%9==0}
    assert candidates==brute and len(brute)==55
    assert [(a,b) for a in range(1,6) for b in range(10) if centre(a,b)==0]==[(1,8),(2,7),(3,6),(4,5),(5,4)]
    assert 1111*4==4444 and 3663==3003+660==11*(3*91+6*10)
