"""Horizontal tomography slices emerge from real stacks of unit cubes."""
from stage import clamp
BACKGROUND=('#222337','#323451')
TOP,LEFT,RIGHT='#c9b9e6','#8479ab','#615b92'
INK,GREEN,AMBER,WHITE='#302b47','#96ddbb','#efc47d','#f3eef9'
BRIDGE='The missing photograph is a horizontal slice. Which of its marks are forced by the three marks on the sheet above it?'
TITLES=['Photograph one height','One tall stack on three sheets','How many actual cubes?',
        'A missing photograph','The four sheets must total fourteen','Which stacks stop here?',
        'Could the smudged scan work?','Two ways to read the scans']
MODEL=[[4,3,3],[2,1,1]]


def layers(heights):
    return [{(r,c) for r,row in enumerate(heights) for c,value in enumerate(row) if value>=z}
            for z in range(1,max(map(max,heights))+1)]


def check_maths():
    assert list(map(len,layers([[1,3]])))==[2,1,1]
    sheets=layers(MODEL);counts=list(map(len,sheets))
    assert counts==[6,4,3,1] and sum(counts)==14
    assert [counts[i]-(counts+[0])[i+1] for i in range(4)]==[2,1,2,1]
    assert all(b<=a for a,b in zip(sheets,sheets[1:]))


def sculpture(a,x,y,s,model,pulse=0):
    def at(r,c,z):return (x+(c-r)*s*.70,y+(r+c)*s*.32-z*s*.73)
    for r in range(len(model)):
        for c,height in enumerate(model[r]):
            for z in range(height):
                p=at(r,c,z+1);q=at(r,c+1,z+1);t=at(r+1,c+1,z+1);u=at(r+1,c,z+1)
                a.polygon([u,t,at(r+1,c+1,z),at(r+1,c,z)],LEFT,INK)
                a.polygon([t,q,at(r,c+1,z),at(r+1,c+1,z)],RIGHT,INK)
                a.polygon([p,q,t,u],GREEN if pulse==z+1 else TOP,INK)


def scan(a,x,y,size,positions,cols,rows,label,unknown=False):
    a.box(x-10,y-12,cols*size+20,rows*size+24,radius=7,fill='#373c53',edge='#a5afca',stroke=2)
    for r in range(rows):
        for c in range(cols):
            xx=x+c*size;yy=y+r*size
            a.box(xx+2,yy+2,size-4,size-4,radius=3,fill='#434959' if unknown or (r,c) not in positions else GREEN)
    a.label(label,x+size*cols/2,y+rows*size+40,24,AMBER,align='center',bold=True)
    if unknown:a.label('?',x+size*cols/2,y+size*rows/2,40,WHITE,align='center',bold=True)


def draw(a,n,m):
    phase=clamp(m.local/(m.scene['end']-m.start));a.label('MUSEUM IMAGING ROOM',73,50,20,GREEN,bold=True)
    a.label(TITLES[n-1],72,103,45,WHITE,bold=True)
    if n in (1,2,3):
        simple=[[1,3]];sheets=layers(simple)
        sculpture(a,265,459,88,simple,1+min(2,int(phase*3)))
        for i,data in enumerate(sheets):
            if n==1 and i>int(phase*3):continue
            scan(a,621+i*173,294-30*i,54,data,2,1,'Level '+str(i+1))
        if n==3:a.label('2 + 1 + 1 = 4 cubes',716,501,37,WHITE,m.reveal('Two plus one'),align='center',bold=True)
        return
    sheets=layers(MODEL)
    if n in (4,5,7):
        for i,data in enumerate(sheets):
            unknown=n==4 and i==1 or n==5 and i==1 and not m.reveal('Four cubes remain')
            if n==7 and i==1:data={(0,0),(0,1)}
            x=135+i*262;scan(a,x,235,56,data,3,2,'Level '+str(i+1),unknown)
            if not unknown:a.label(str(len(data))+(' mark' if len(data)==1 else ' marks'),x+85,436,28,WHITE,align='center')
        if n==5:a.label('14 − (6 + 3 + 1) = 4',640,522,39,GREEN,m.reveal('Four cubes remain'),align='center',bold=True)
        elif n==7:
            x=135+2*262+2*56+28;y=235+28
            a.dot(x,y,9,AMBER,m.reveal('three cube positions'))
            a.label('The third mark has no supporting position below.',640,516,31,AMBER,m.reveal('cannot support'),align='center')
    else:
        sculpture(a,323,472,72,MODEL,0 if n==8 else min(4,1+int(phase*4)))
        if n==6:
            for i,line in enumerate(['Height 1:  6 − 4 = 2 stacks','Height 2:  4 − 3 = 1 stack','Height 3:  3 − 1 = 2 stacks','Height 4:  1 stack']):
                a.label(line,652,243+69*i,29,WHITE,clamp(phase*5-i),bold=i==3)
        else:
            a.label('Add layer counts',670,236,33,GREEN,bold=True)
            a.label('6 + 4 + 3 + 1 = 14 cubes',670,292,27,WHITE)
            a.label('Subtract neighbouring counts',670,398,30,AMBER,bold=True)
            a.label('4 − 3 = 1 stack of height 2',670,452,26,WHITE)


def poster(draw):
    return draw(11.0,1.5)
