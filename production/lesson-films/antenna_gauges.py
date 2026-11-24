"""A restorer's gauge rack pairs divisor lengths and tests a three-drawer inventory."""
from math import isqrt
BACKGROUND=('#222946','#111527')
WHITE, BRASS, WIRE, BLUE, INK='#eee9db','#eac182','#c48f4b','#98cae9','#343a52'
BRIDGE='Watch the two gauge drawers meet in the centre. Why does a prime middle gauge make the inventory stop at three lengths?'
TITLES=['Fit a gauge to the rod','Scan the short gauges','The drawer with no twin','Count the shared drawer once','A label falls off','What can the middle gauge be?','Return the correct label','Test a second square']


def factors(n):
    return [d for d in range(1,n+1) if n%d==0]


def check_maths():
    assert factors(12)==[1,2,3,4,6,12]
    assert len(factors(30))==8 and len(factors(36))==9
    candidates=[n for n in range(101,200) if len(factors(n))==3 and sum(map(int,str(factors(n)[1])))==4]
    assert candidates==[169] and factors(169)==[1,13,169]
    assert {2,7,14}<set(factors(196))


def ruler(a,x,y,width,n,d,phase):
    a.box(x,y,width,20,fill=WIRE,edge=BRASS,stroke=2,radius=6)
    part=width*d/n
    for j in range(min(n//d,int(phase*(n//d+1)))):
        a.box(x+j*part+2,y+26,part-4,32,radius=2,fill=BLUE)
    a.label(f'{n} cm',x+width,y-34,26,WHITE,align='right')
    a.label(f'{d} cm per gauge',x,y+76,25,BLUE)


def drawer(a,x,y,text,highlight=False):
    a.box(x,y,130,57,radius=7,fill=BRASS if highlight else INK,edge=BRASS)
    a.label(str(text),x+65,y+10,31,INK if highlight else WHITE,bold=True,align='center')


def draw(a,n,m):
    phase=min(1,max(0,m.local/(m.scene['end']-m.start)))
    a.label('RADIO RESTORATION LAB',74,50,22,BRASS,bold=True)
    a.label(TITLES[n-1],72,103,45,WHITE,bold=True)
    if n==1:
        ruler(a,135,246,940,12,3,phase*2)
        ruler(a,135,420,940,12,4,max(0,phase*2-1))
        return
    if n in (2,3,4):
        length=30 if n==2 else 36
        pairs=[(i,length//i) for i in range(1,isqrt(length)+1) if length%i==0]
        a.label(f'{length} cm',130,185,34,BRASS,bold=True)
        shown=min(len(pairs),int(phase*(len(pairs)+1))+1) if n!=4 else len(pairs)
        for j,(p,q) in enumerate(pairs[:shown]):
            x=134+j*208
            drawer(a,x,269,p,p==q)
            if p!=q:
                a.line([(x+65,330),(x+65,365)],WIRE,3)
                drawer(a,x,369,q)
            else:
                a.label('shared',x+65,378,22,BRASS,align='center')
        if n==4:a.label('4 pairs × 2 + 1 middle = 9',615,493,35,WHITE,m.reveal('nine lengths'),align='center')
        return
    if n in (5,6):
        keys=['1','?','N'] if n==5 else ['1','p','p²']
        for i,label in enumerate(keys):
            x=235+321*i
            drawer(a,x,285,label,i==1)
            if i<2:a.dashed((x+145,312),(x+308,312),WIRE,3)
        if n==5:
            a.label('100 < N < 200',335,410,32,WHITE,align='center')
            a.label('Middle digit sum = 4',860,410,32,BLUE,align='center')
        else:
            a.label('middle × middle = full rod',610,410,32,WHITE,align='center')
            a.label('Another factor of p would open a fourth drawer.',610,478,26,BLUE,m.reveal('fourth entry'),align='center')
        return
    if n==7:
        for j,p in enumerate((11,12,13,14)):
            x=150+j*258
            drawer(a,x,245,p,p==13 and phase>.4)
            a.label(f'{p}² = {p*p}',x+65,345,23,WHITE,align='center')
            a.label(f'digit sum {p//10+p%10}',x+65,395,20,BLUE,align='center')
        a.label('The gauges  /  1, 13, 169 cm',620,495,32,BRASS,m.reveal('three gauge'),align='center')
        return
    ruler(a,163,237,902,196,14,phase*1.5)
    for j,p in enumerate((1,2,7,14,196)):
        if phase*7>j:drawer(a,145+j*208,444,p,p==14)


def poster(draw):
    return draw(8.1,1.5)
