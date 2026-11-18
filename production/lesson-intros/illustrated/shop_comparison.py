"""S041. Pair original objects across two till rolls and remove only quantities that actually match."""
from math import cos,sin,pi
from captioned_film import mix,font
PAPER='#263437';INK='#fff0d7';SOFT='#c6d0bf';WHITE='#f1dfbf';TAPE='#e6d5b2';DARK='#263437';RULE='#877e68';TEAL='#91dac3';RUST='#f6a17e';BLUE='#a7c9f6';XINK='#387187';YINK='#aa602e'
def label(c,s,x,y,size=29,col=INK,anchor='lm'):c.text(s,x,y,size,col,anchor,True)
def title(c,s):
    z=42
    while font(round(z*c.scale),True).getlength(s)>1148*c.scale:z-=1
    label(c,s,59,58,z)
def icon(c,k,x,y,s=1):
    def pt(a,b):return x+s*a,y+s*b
    def poly(pts,fill,edge=DARK):c.poly([pt(a,b) for a,b in pts],fill,edge,max(1,1.8*s))
    def stroke(pts,col,w=2):c.line([pt(a,b) for a,b in pts],col,max(1,w*s))
    if k=='bun':
        dome=[(-25,6)]+[(25*cos(pi-j*pi/18),5-21*sin(pi-j*pi/18)) for j in range(19)]+[(23,12),(-22,12)]
        poly(dome,'#e3995d');stroke([(-22,6),(22,6)],'#a3563c',2)
        for a,b in ((-12,-3),(-4,-9),(5,-6),(11,-1)):stroke([(a,b),(a+3,b-1)],WHITE,1.5)
    elif k=='drink':
        poly([(-14,-15),(14,-15),(11,18),(-10,18)],'#78b7ad')
        stroke([(-18,-16),(18,-16)],DARK,4);stroke([(4,-18),(7,-27),(13,-28)],'#a54c3a',3)
        stroke([(-6,-4),(8,-4)],WHITE,2)
    elif k=='pen':
        poly([(-26,10),(14,-12),(18,-5),(-22,17)],'#8ab8d2')
        poly([(-29,20),(-26,10),(-22,17)],'#55574a');poly([(14,-12),(22,-16),(26,-10),(18,-5)],'#46798d')
    elif k=='marker':
        poly([(-20,14),(13,-17),(24,-6),(-9,25)],'#ddaa68')
        poly([(10,-15),(18,-23),(29,-11),(21,-3)],'#795e55')
        stroke([(-13,12),(-6,18)],'#8e654e',3)
    else:
        shape=[(-22,-13),(0,-21),(22,-13),(22,13),(0,21),(-22,13)] if k=='X' else [(-22,-16),(16,-16),(25,0),(16,16),(-22,16)]
        poly(shape,XINK if k=='X' else YINK)
        label(c,k,x,y+1,max(12,round(23*s)),INK,'mm')
def tape(c,x,y,w,h=76):
    c.rect(x,y,w,h,TAPE)
    for i in range(11):
        a=x+w*i/11;b=x+w*(i+.5)/11;d=x+w*(i+1)/11
        c.poly([(a,y+h),(b,y+h-4),(d,y+h)],PAPER,None)
def smallorders(c,top,bottom,a,b,matched=0,step=0,prices=True):
    width=789;tape(c,127,180,width);tape(c,127,354,width)
    label(c,'1',151,214,26,DARK);label(c,'2',151,389,26,DARK)
    num=min(len(top),len(bottom));spacing=min(112,460/max(1,max(len(top),len(bottom))-1))
    for row,items,yy in ((0,top,217),(1,bottom,391)):
        for j,k in enumerate(items):
            p=matched if j<num and top[j]==bottom[j] else 0
            if p>.99:continue
            x=246+spacing*j;y=mix(yy,304,p)
            icon(c,k,x,y,1.22*(1-.57*p))
    if prices:
        label(c,'$'+str(a),829,219,31,DARK,'mm');label(c,'$'+str(b),829,393,31,DARK,'mm')
    if step:label(c,'Compare what is left.',341,494,31,TEAL)
def intro(c,q):
    title(c,'Remove the same objects from both till rolls')
    p=q.after('Slide each matching pair',2.1)
    smallorders(c,['drink','drink','bun'],['drink','drink','bun','bun'],18,22,p,prices=False)
    if q.after('objects are left'):label(c,'One extra bun',940,271,29,RUST)
    if q.after('difference between'):label(c,'Difference in cost',940,368,25,TEAL)
def exam(c,q):
    title(c,'An extra item explains the difference between receipts')
    smallorders(c,['bun','drink'],['bun','drink','drink'],0,0,q.after('extra item',1.7),prices=False)
    label(c,'Compare units.',933,229,28,TEAL)
    if q.after('copy a whole order'):label(c,'Copy all items.',933,334,27,RUST)
    if q.after('full price'):label(c,'Copy the price.',933,425,27,RUST)
def buns(c,q):
    title(c,'One more bun, the same two drinks')
    smallorders(c,['drink','drink','bun'],['drink','drink','bun','bun'],18,22)
    if q.after('price of a bun'):label(c,'One bun costs …',932,282,28)
def difference(c,q):
    title(c,'Slide the identical purchases together')
    smallorders(c,['drink','drink','bun'],['drink','drink','bun','bun'],18,22,q.after('drinks occur',2))
    if q.after('additional bun'):label(c,'1 bun remains',933,236,28,RUST)
    if q.after('four dollars'):label(c,'$22 − $18 = $4',932,340,26,TEAL)
def pens(c,q):
    title(c,'Match the number of markers before subtracting')
    smallorders(c,['marker','pen','pen'],['marker','marker','pen','pen','pen'],15,26)
    if q.after('same number'):label(c,'1 marker',941,212,27,RUST);label(c,'2 markers',941,390,27,RUST)
def medium_work(c,q):
    title(c,'Two whole copies of the first order cost $30')
    copied=q.after('four pens and two markers',1.45)
    if copied<1:
        tape(c,159,183,873,88)
        for j,k in enumerate(('pen','pen','marker')):icon(c,k,276+85*j,225)
        for j,k in enumerate(('pen','pen','marker')):
            if copied:icon(c,k,mix(276+85*j,629+85*j,copied),mix(225,215,copied))
        label(c,'$30' if q.after('four pens') else '$15',924,227,29,DARK,'mm')
    else:
        top=['marker','marker','pen','pen','pen','pen'];bottom=['marker','marker','pen','pen','pen']
        p=q.after('Match those two markers',3.4);smallorders(c,top,bottom,30,26,p)
    if q.after('One pen stays'):label(c,'1 pen   $4',944,225,30,TEAL)
    if q.after('Two pens cost eight'):label(c,'2 pens   $8',944,322,27,BLUE)
    if q.after('seven dollars'):label(c,'Marker   $7',944,419,28,RUST)
def packs(c,rows,matched=0):
    for r,(xs,ys,price) in enumerate(rows):
        yc=227+155*r;tape(c,70,yc-45,1135,87)
        n0=min(row[0] for row in rows);n1=min(row[1] for row in rows)
        for k,n,first,delta,equal in (('X',xs,119,53,n0),('Y',ys,702,52,n1)):
            for j in range(n):
                p=matched if j<equal else 0
                if p>=.99:continue
                icon(c,k,first+j*delta,mix(yc,304.5,p),.83*(1-.5*p))
        label(c,'$'+str(price),1153,yc,26,DARK,'rm')
def hard(c,q):
    title(c,'Price two kinds of packs from two complete orders')
    first=q.after('three X packs');second=q.after('five X packs')
    if first:packs(c,[(3,2,26)]+([(5,3,41)] if second else []))
    if q.after('unit price'):label(c,'What is one X worth? And one Y?',299,533,31,TEAL)
def hard_work(c,q):
    title(c,'Make both rows contain exactly six Y packs')
    a=q.after('three copies',1.8);b=q.after('two copies',1.7)
    if not a:rows=[(3,2,26),(5,3,41)]
    else:
        na=1+min(2,int(a*2+.0001));nb=1+min(1,int(b+.0001))
        rows=[(na*3,na*2,na*26),(nb*5,nb*3,nb*41)]
    remove=q.after('Match the packs',1.8);packs(c,rows,remove)
    if q.after('four dollars'):label(c,'1 X   $82 − $78 = $4',102,513,29,TEAL)
    if q.after('remaining fourteen'):label(c,'2 Y   $26 − $12 = $14',614,493,27,BLUE)
    if q.after('each Y pack'):label(c,'1 Y   $14 ÷ 2 = $7',614,550,28,RUST)
def check(c,q):
    title(c,'Rebuild each original purchase')
    packs(c,[(3,2,26),(5,3,41)])
    if q.after('twenty-six'):label(c,'3 × $4 + 2 × $7 = $26',91,508,28,TEAL)
    if q.after('forty-one'):label(c,'5 × $4 + 3 × $7 = $41',671,508,28,BLUE)
def pitfalls(c,q):
    title(c,'A copied order includes the entire price')
    for j in range(2 if q.after('Scale an equation') else 1):
        y=187+j*124;tape(c,173,y,770,74)
        for i,k in enumerate(('X','X','X','Y','Y')):icon(c,k,252+i*92,y+35,.93)
        label(c,'$26',886,y+36,28,DARK,'rm')
    if q.after('every coefficient'):label(c,'6 X + 4 Y',245,502,31,TEAL);label(c,'2 × $26 = $52',700,502,31,RUST)
def finish(c,q):
    title(c,'Choose a matching part and rebuild both original totals')
    compare=q.after('copy a whole bundle',1.7)
    if compare and not q.after('rebuild both'):packs(c,[(9,6,78),(10,6,82)],q.after('Subtract',1.5))
    else:packs(c,[(3,2,26),(5,3,41)])
    if q.after('price what remains'):label(c,'X costs $4',208,502,29,TEAL)
    if q.after('rebuild both'):label(c,'Y costs $7',703,502,29,RUST)
SCENES=(intro,exam,buns,difference,pens,medium_work,hard,hard_work,check,pitfalls,finish)
def verify():
    assert 4+2*7==18 and 2*4+2*7==22
    assert [(p,m) for p in range(16) for m in range(16) if 2*p+m==15 and 3*p+2*m==26]==[(4,7)]
    assert [(x,y) for x in range(42) for y in range(42) if 3*x+2*y==26 and 5*x+3*y==41]==[(4,7)]
    assert (3*3,3*2,3*26)==(9,6,78) and (5*2,3*2,2*41)==(10,6,82)
