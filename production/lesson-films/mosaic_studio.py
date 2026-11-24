"""Mosaic panels with real domino placements, chips and a colour-inventory proof."""
from stage import between

BACKGROUND=('#202c2d','#364543')
CREAM,INK,WOOD='#f7e9c6','#162b2a','#aa805a'
DARK,LIGHT,CHIP='#407572','#e3cda6','#192524'
COLORS=['#e4aa68','#9bdbb7','#daa0b0','#b9b1ec','#ead275','#8ac5dc','#d29d79']
BRIDGE='Watch the maker lift two opposite corners from the four-by-four panel. Which colour runs out before the last domino can go down?'
RING=[((0,0),(0,1)),((0,2),(1,2)),((2,1),(2,2)),((1,0),(2,0))]
SIX=[((0,1),(0,2)),((1,0),(2,0)),((1,1),(1,2)),((2,1),(2,2)),((3,0),(3,1)),((1,3),(2,3))]
SEVEN=[((0,1),(0,2))]+[((r,c),(r,c+1)) for r in (1,2,3) for c in (0,2)]
TITLES=['A narrow offcut','Can four dominoes turn the corners?','A placement around the hole',
        'Two corners chip away','Which colour runs out?','Six pieces fit','The second chip moves','A bound needs a placement']


def check_layout(m, pieces, chips):
    covered=set()
    for p,q in pieces:
        assert all(0<=v<m for v in (*p,*q)) and sum(abs(a-b) for a,b in zip(p,q))==1
        assert {p,q}.isdisjoint(covered|set(chips))
        covered.update([p,q])
    return covered


def check_maths():
    assert len(check_layout(3,RING,[(1,1)]))==8
    chips=[(0,0),(3,3)];board={(r,c) for r in range(4) for c in range(4)}-set(chips)
    assert sum((r+c)%2==0 for r,c in board)==6
    assert board-check_layout(4,SIX,chips)=={(0,3),(3,2)}
    assert len(check_layout(4,SEVEN,[(0,0),(0,3)]))==14


def board(a,x,y,size,cols,rows,chips,pieces,progress,checkered):
    a.box(x-10,y-10,cols*size+20,rows*size+20,fill=WOOD,radius=6)
    for row in range(rows):
        for col in range(cols):
            empty=(row,col) in chips
            colour=CHIP if empty else DARK if checkered and (row+col)%2==0 else LIGHT
            a.box(x+col*size+2,y+row*size+2,size-4,size-4,radius=3,fill=colour)
            if empty:
                xx,yy=x+col*size+size*.5,y+row*size+size*.5
                a.line([(xx-9,yy-9),(xx+9,yy+9)],WOOD,2);a.line([(xx-9,yy+9),(xx+9,yy-9)],WOOD,2)
    for i,(p,q) in enumerate(pieces):
        fade=min(1,max(0,progress-i))
        if not fade:continue
        r,c=min(p[0],q[0]),min(p[1],q[1]);rows2=abs(p[0]-q[0])+1;cols2=abs(p[1]-q[1])+1
        xx=x+c*size+5+(1-fade)*18;yy=y+r*size+5-(1-fade)*16
        a.box(xx,yy,cols2*size-10,rows2*size-10,radius=9,fill=COLORS[i],edge=INK,stroke=3,opacity=fade)
        for rr,cc in (p,q):
            a.dot(xx+(cc-c+.5)*size-5,yy+(rr-r+.5)*size-5,max(2,size*.065),INK,fade)


def draw(a,n,m):
    phase=min(1,max(0,m.local/(m.scene['end']-m.start)))
    a.label('MOSAIC WORKSHOP',78,52,22,'#c6b995',bold=True)
    a.label(TITLES[n-1],75,102,46,CREAM,bold=True)
    if n==1:
        board(a,186,257,130,5,1,[],[((0,0),(0,1)),((0,2),(0,3))],3*phase,False)
        a.label('5 spaces   /   2 dominoes   /   1 uncovered',645,468,31,CREAM,m.reveal('one space'),align='center')
        return
    if n in (2,3):
        k=min(2,phase*2.4) if n==2 else min(4,2+phase*3.4)
        board(a,182,179,115,3,3,[(1,1)],RING,k,False)
        a.label('3 × 3',729,261,46,CREAM,bold=True)
        a.label('9 spaces − 1 hole = 8',729,341,29,CREAM)
        a.label('4 dominoes',729,425,39,COLORS[1],m.reveal('All eight') if n==3 else 0,bold=True)
        return
    if n==8:
        for i,(chips,pieces,count) in enumerate([([(0,0),(3,3)],SIX,'6 fit'), ([(0,0),(0,3)],SEVEN,'7 fit')]):
            xx=210+562*i;board(a,xx,190,67,4,4,chips,pieces,len(pieces),True)
            a.label(count,xx+134,503,40,COLORS[i],align='center',bold=True)
        return
    chips=[(0,0),(0,3) if n==7 else (3,3)]
    if n==4:
        chips=chips[:(2 if m.reveal('top left')>.3 else 0)]
    k=0
    if n==6:k=6*min(1,max(0,(m.t-m.at('watch six'))/(m.scene['end']-m.at('watch six'))*1.8))
    if n==7:k=7*min(1,max(0,(m.t-m.at('Join the two'))/(m.scene['end']-m.at('Join the two'))*1.25))
    board(a,190,180,87,4,4,chips,SEVEN if n==7 else SIX,k,n!=4)
    if n==4:
        a.label('16 − 2 = 14 spaces',693,275,34,CREAM,m.reveal('Fourteen spaces'))
        a.label('Can 7 actually fit?',693,367,35,COLORS[0],m.reveal('Seven is'),bold=True)
    if n in (5,6):
        a.label('Dark squares',697,252,28,CREAM);a.label('Light squares',697,337,28,CREAM)
        count=m.reveal('leaving six') if n==5 else 1
        a.label('6',970,252,50,COLORS[1],count,bold=True);a.label('8',970,337,50,COLORS[0],count,bold=True)
        if n==6:a.label('Placed: '+str(min(6,int(k+.01))),697,449,36,CREAM,bold=True)
    if n==7:
        a.label('Dark  7       Light  7',700,264,33,CREAM,m.reveal('opposite colours'))
        a.label('1 + 2 + 2 + 2 = 7',700,378,35,COLORS[1],m.reveal('other three rows'),bold=True)


def poster(draw):
    return draw(8.0,1.5)
