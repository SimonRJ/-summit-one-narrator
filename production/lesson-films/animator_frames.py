"""Frame perforations distinguish drawings from the joins of an arithmetic sequence."""
BACKGROUND=('#3a3542','#222732')
PAPER,INK,BLUE,GOLD,ORANGE,TRACK='#fff1d9','#28313e','#b0d8eb','#edcd89','#f1ac96','#807d89'
HEAD=('Freeze the moving mark','Count joins between drawings','Rewind from a known position','A reel running the other way','Recover a descending step','One drawing is on the wrong step','The reel has an end','Check distance and position')
BRIDGE='When the animator measures from frame 4 to frame 10, count the joins between those drawings. On the second reel, can a reading follow the seven-millimetre step and still lie beyond the last frame?'
def check_maths():
    first=[10+4*i for i in range(10)]; assert first[3]==22 and first[9]==46 and len(first[3:])-1==6
    second=[82-7*i for i in range(10)]; assert second[2]==68 and second[8]==26 and second[9]==19
    assert [v for v in (53,40,5) if v in second]==[40] and second.index(40)+1==7
def txt(a,s,x,y,size=34,k=PAPER,t=1):a.text(str(s),x,y,size,k,bold=True,opacity=t)
def cart(a,x,y,w=66):
    a.box(x-w/2,y-23,w,28,fill=ORANGE,radius=5)
    a.dot(x-w*.3,y+7,7,INK);a.dot(x+w*.3,y+7,7,INK)
def strip(a,frames,values,y,show_cart=True):
    left=114;full=1052;n=len(frames);w=full/n
    a.box(left,y,full,171,radius=5,fill='#18232e',edge=TRACK,stroke=2)
    for idx,(label,v) in enumerate(zip(frames,values)):
        x=left+idx*w
        a.box(x+4,y+19,w-8,131,radius=2,fill='#c8d1ce')
        for p in (x+w*.29,x+w*.71):
            a.box(p-7,y+4,14,9,fill=TRACK,radius=2);a.box(p-7,y+155,14,9,fill=TRACK,radius=2)
        txt(a,'F'+str(label),x+w*.5,y+42,24,INK)
        if show_cart:
            a.line([(x+13,y+91),(x+w-13,y+91)],'#66777b',2);cart(a,x+22+(w-47)*v/90,y+76,30)
        if v is not None:txt(a,str(v)+' mm',x+w*.5,y+120,22,INK)
def draw(a,n,c):
    a.label(HEAD[n-1],64,70,42,PAPER,bold=True);a.line([(64,124),(1214,124)],TRACK,3)
    if n in (1,2):
        f=list(range(4,11));vals=[22,26,30,34,38,42,46]
        if n==1:
            strip(a,[4,10],[22,46],235)
            txt(a,'How much movement in one join?',640,493,39,GOLD,c.reveal('How far'))
        else:
            strip(a,f,vals,228)
            for i in range(6):
                x=114+(i+1)*(1052/7);a.arrow((x-22,420),(x+22,420),GOLD,c.reveal('six joins',.45,.08*i),3)
            txt(a,'(46 − 22) ÷ 6 = 4 mm per frame',640,523,39,BLUE,c.reveal('four millimetres per frame'))
    elif n==3:
        strip(a,[1,2,3,4],[10,14,18,22],222)
        a.arrow((953,431),(287,431),GOLD,c.reveal('back twelve'),5)
        txt(a,'22 − 3 × 4 = 10 mm',640,536,43,BLUE,c.reveal('ten millimetres'))
    elif n==4:
        strip(a,[3,9],[68,26],204)
        txt(a,'Loose readings:  53 mm, 40 mm, 5 mm',640,462,39,GOLD,c.reveal('Three loose drawings'))
        txt(a,'Frames 1 through 10 only',640,544,31,BLUE,c.reveal('could belong'))
    elif n==5:
        strip(a,range(3,10),[68,61,54,47,40,33,26],226)
        txt(a,'Six joins → 42 mm lower',640,451,35,BLUE,c.reveal('falls by forty two'))
        txt(a,'Change per frame: −7 mm',640,541,40,GOLD,c.reveal('seven millimetres lower'))
    elif n==6:
        strip(a,[5,6,7],[54,47,40],213)
        txt(a,'53 is between two adjacent readings.',640,439,33,ORANGE,c.reveal('Fifty three cannot occur'))
        txt(a,'40 is at frame 7.',640,541,40,BLUE,c.reveal('belongs to frame seven'))
    elif n==7:
        strip(a,[9,10],[26,19],204)
        txt(a,'Last frame: 10',640,426,38,BLUE,c.reveal('stops at frame ten'))
        txt(a,'5 mm would need frame 12.',640,521,41,ORANGE,c.reveal('frame twelve'))
    else:
        txt(a,'Step check',347,262,44,BLUE);txt(a,'Range check',930,262,44,GOLD)
        txt(a,'A whole number of joins?',350,353,31,PAPER,c.reveal('whole number of steps'))
        txt(a,'A frame on the actual reel?',924,353,31,PAPER,c.reveal('must actually exist'))
        txt(a,'Both checks are needed.',640,508,41,PAPER,c.reveal('frame number'))
def poster(draw):return draw(9,1)
