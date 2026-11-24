"""Build the photographer's contact sheet and its smaller map of starting corners."""
BACKGROUND = ('#183431', '#0e2421')
PAPER, INK, SEA, GRID = '#ecdfbb', '#20322c', '#aecfc4', '#6c9181'
COPPER, BLUE, WHITE = '#f5ad72', '#83ceff', '#fff3da'
BRIDGE = 'Watch the two marked animals. What does a point on the smaller map stand for, and why do four points have two colours?'
HEAD = ['A six-square strip', 'A map of legal corners', 'One seal or one ray', 'Six windows reach the seal', 'Twelve windows reach the ray', 'Four corners qualify twice', 'Find the empty crop', 'Turn the print upright']
ANIMALS = [(3, 2), (5, 3)]


def covers(corner, animal, width=4, height=3):
    x, y = corner
    u, v = animal
    return x <= u < x + width and y <= v < y + height


def check_maths():
    corners = [(x, y) for x in range(1, 6) for y in range(1, 4)]
    seal, ray = [{c for c in corners if covers(c, animal)} for animal in ANIMALS]
    assert (len(seal), len(ray), len(seal & ray), len(seal ^ ray)) == (6, 12, 4, 10)
    assert set(corners) - seal - ray == {(1, 3)}
    assert len([(x, y) for x in range(1, 7) for y in range(1, 3)]) == 12


def critter(a, species, x, y, u):
    if species == 0:
        a.polygon([(x-u*.34,y+u*.13),(x-u*.20,y-u*.04),(x+u*.02,y-u*.02),(x+u*.13,y-u*.24),(x+u*.26,y-u*.21),(x+u*.30,y-u*.08),(x+u*.18,y+u*.08),(x+u*.04,y+u*.17)],INK)
        a.dot(x+u*.22,y-u*.17,u*.024,WHITE)
    else:
        a.polygon([(x-u*.37,y),(x-u*.06,y-u*.20),(x+u*.09,y-u*.13),(x+u*.33,y),(x+u*.05,y+u*.18)],INK)
        a.line([(x+u*.03,y+u*.13),(x+u*.21,y+u*.30),(x+u*.29,y+u*.26)],INK,2)


def sheet(a, x, y, size, cols, rows, animals=True):
    for r in range(rows):
        for c in range(cols):
            a.box(x+c*size,y+r*size,size-1,size-1,radius=1,fill=SEA if (c+2*r)%3 else '#b8d5c4')
    for c in range(cols):
        a.label(str(c+1),x+(c+.5)*size,y-19,17,PAPER,align='center')
    for r in range(rows):
        a.label(str(r+1),x-19,y+(r+.5)*size-6,17,PAPER,align='center')
    if animals:
        for k,(c,r) in enumerate(ANIMALS):
            critter(a,k,x+(c-.5)*size,y+(r-.5)*size,size)


def window(a,x,y,size,c,r,w,h):
    left, top = x+(c-1)*size, y+(r-1)*size
    right, bottom = left+w*size,top+h*size
    a.line([(left,top),(right,top),(right,bottom),(left,bottom),(left,top)],'#a6491e',6)
    a.dot(left,top,7,WHITE)


def draw(a,n,m):
    f = min(1,max(0,m.local / (m.scene['end'] - m.start)))
    a.label('CONTACT SHEET  /  WILDLIFE DESK',76,52,21,SEA,bold=True)
    a.label(HEAD[n-1],76,99,47,WHITE,bold=True)
    if n==1:
        sheet(a,170,259,126,6,1,False)
        window(a,170,259,126,1+min(3,int(f*4)),1,3,1)
        a.label('6 cells    /    a 3-cell window',176,433,31,PAPER)
        a.label('4 legal starts',930,433,31,COPPER,m.reveal('four starting'),align='right')
        return
    sx,sy,size=103,215,57
    sheet(a,sx,sy,size,8,5)
    starts={2: [(c,r) for r in range(1,4) for c in range(1,6)],3:[(3,1),(4,3)],4:[(c,r) for r in (1,2) for c in (1,2,3)],5:[(c,r) for r in (1,2,3) for c in (2,3,4,5)],6:[(2,1),(3,1),(2,2),(3,2)],7:[(1,3)],8:[(c,r) for r in (1,2) for c in range(1,7)]}[n]
    c,r=starts[min(len(starts)-1,int(f*len(starts)))]
    w,h=(3,4) if n==8 else (4,3)
    window(a,sx,sy,size,c,r,w,h)
    a.label('PHOTOGRAPH',104,525,22,PAPER,bold=True)
    cols,rows=9-w,6-h
    ox,oy,dx,dy=737,229,79,81
    a.label('STARTING CORNERS',706,170,22,PAPER,bold=True)
    for rr in range(1,rows+1):
        for cc in range(1,cols+1):
            x,y=ox+(cc-1)*dx,oy+(rr-1)*dy
            corner=(cc,rr)
            left=covers(corner,ANIMALS[0]) and n in (4,5,6,7)
            right=covers(corner,ANIMALS[1]) and n in (5,6,7)
            a.dot(x,y,16,GRID)
            if left:a.dot(x-6 if right else x,y,10,COPPER)
            if right:a.dot(x+6 if left else x,y,10,BLUE)
            if corner==(c,r):
                a.line([(x-22,y-17),(x-22,y+21),(x+20,y+21)],WHITE,3)
    captions={2:'5 × 3 = 15',3:'Which starts show exactly one?',4:'Seal  /  3 × 2 = 6',5:'Ray  /  4 × 3 = 12',6:'6 + 12 − 2 × 4 = 10',7:'15 − 10 − 4 = 1',8:'6 × 2 = 12'}
    cue={2:'fifteen crops',4:'give six',5:'twelve possible',6:'ten crops',7:'one empty',8:'twelve crops'}.get(n)
    a.label(captions[n],930,485,31,WHITE,m.reveal(cue) if cue else 1,align='center')


def poster(draw):
    return draw(9,1.5)
