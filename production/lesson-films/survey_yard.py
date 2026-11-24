"""Two orthographic cameras constrain one unmeasured stack in an L-shaped plan."""
from itertools import product
BACKGROUND=('#29333f','#17232e')
PAPER,SKY,SEA,WOOD,EMPTY,GOLD,EDGE='#fcf0d1','#a9ddf3','#9dd6ca','#d7b28e','#37495a','#f7cb70','#667b89'
HEAD=('A camera sees an outline','Turn the camera','A yard shaped like an L','Read the front camera','Read the side camera','Rebuild every possible yard','Use the survey weight','What would the camera notice?')
BRIDGE='One stack in the L-shaped yard can change without either camera noticing. Which neighbours set the back-row and column-A outlines, and what does the scale add?'
CELLS=[(0,0),(1,0),(2,0),(0,1),(0,2)]
def profiles(p):
    return ([max(p.get((x,y),0) for y in range(3)) for x in range(3)],[max(p.get((x,y),0) for x in range(3)) for y in (2,1,0)])
def check_maths():
    sols=[]
    for v in product(range(1,5),repeat=5):
        p=dict(zip(CELLS,v))
        if profiles(p)==([4,2,3],[2,4,3]):sols.append(v)
    assert sorted(sols)==[(h,2,3,4,2) for h in (1,2,3)]
    assert [sum(v) for v in sols]==[12,13,14] and [v[0] for v in sols if sum(v)==13]==[2]
def text(a,s,x,y,size=34,col=PAPER,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def grid(a,values,front=None,side=None):
    left=389;top=209;size=85
    for x,lab in enumerate('ABC'):text(a,lab,left+x*size+42,top-27,26,SKY)
    for y,lab in enumerate(('Back','Middle','Front')):
        text(a,lab,left-81,top+y*size+42,25,SEA)
        for x in range(3):
            cell=(x,y);occ=cell in CELLS
            a.box(left+x*size,top+y*size,size-3,size-3,radius=3,fill=WOOD if occ else EMPTY,edge=EDGE)
            if occ:text(a,values.get(cell,'?'),left+42+x*size,top+40+y*size,41,'#182d39')
        if side:
            text(a,side[y],left+size*3+48,top+y*size+42,35,SEA)
    if front:
        for x,v in enumerate(front):text(a,v,left+42+x*size,top+size*3+32,35,SKY)
        text(a,'Front camera',left+size*1.5,top+size*3+76,26,SKY)
    if side:text(a,'Row peaks',left+size*3+55,top-26,24,SEA)
def bars(a,x,y,heights,caps,col,cell=32):
    for i,h in enumerate(heights):
        for j in range(h):a.box(x+i*120,y-(j+1)*cell,69,cell-2,fill=col,radius=2)
        text(a,caps[i],x+i*120+34,y+35,25,PAPER)
def draw(a,n,c):
    a.label(HEAD[n-1],64,70,44,PAPER,bold=True);a.line([(64,125),(1214,125)],EDGE,3)
    if n==1:
        bars(a,180,424,[4,2+int(c.reveal('raise the short')>.45)],['Front','Behind'],WOOD,48)
        a.arrow((89,453),(150,453),SKY,c.reveal('camera position'),4)
        bars(a,896,424,[4],['Photo'],SKY,48)
        text(a,'Side view of the two stacks',315,542,29,PAPER)
        text(a,'One outline in front',933,541,29,SKY)
    elif n==2:
        grid(a,{})
        a.arrow((516,560),(516,480),SKY,c.reveal('front camera'),5)
        a.arrow((824,336),(665,336),SEA,c.reveal('side'),5)
        text(a,'Front camera',519,584,25,SKY)
        text(a,'Side camera',937,338,27,SEA,c.reveal('side'))
    else:
        vals={}
        if n>4 or (n==4 and c.reveal('must be two')>.05):vals[(1,0)]=2
        if n>4 or (n==4 and c.reveal('Set it to three')>.05):vals[(2,0)]=3
        if n>5 or (n==5 and c.reveal('set it to two')>.05):vals[(0,2)]=2
        if n>5 or (n==5 and c.reveal('set it to four')>.05):vals[(0,1)]=4
        if n==6 and c.reveal('Try each')>.05:
            elapsed=c.t-c.at('Try each');vals[(0,0)]=min(3,1+int(elapsed/1.6))
        if n==7 and c.reveal('height of two')>.25:vals[(0,0)]=2
        if n==8:vals[(0,0)]=2+int(c.reveal('becomes three')>.2)+int(c.reveal('second cube')>.2)
        side=[3,4,2] if n>=5 else None
        if n==8 and vals[(0,0)]==4:side=[4,4,2]
        grid(a,vals,[4,2,3] if n>=4 else None,side)
        if n==3:
            text(a,'Five occupied positions',960,305,31,WOOD,c.reveal('five occupied'))
            text(a,'All other positions are empty.',948,381,25,PAPER,c.reveal('All other positions'))
        elif n==4:
            text(a,'Only one stack in B',964,290,29,SKY,c.reveal('only its back stack'))
            text(a,'Only one stack in C',964,371,29,SKY,c.reveal('just its back stack'))
        elif n==5:
            text(a,'Only one stack',953,269,30,SEA);text(a,'in each near row',953,319,30,SEA)
            text(a,'Back-left height?',951,427,34,GOLD,c.reveal('Which height'))
        elif n==6:
            text(a,'Back-left stack',960,274,30,GOLD)
            text(a,'1, 2 or 3',960,349,48,GOLD,c.reveal('one two or three'))
            text(a,'All three fit both views.',955,433,27,PAPER,c.reveal('already gives its row'))
        elif n==7:
            text(a,'Known cubes: 11',948,280,34,WOOD,c.reveal('eleven cubes'))
            text(a,'Scale: 13 cubes',945,356,34,SEA,c.reveal('scale records'))
            text(a,'13 − 11 = 2',944,439,43,GOLD,c.reveal('thirteen minus eleven'))
        else:
            text(a,'Watch the back-row peak',949,288,28,SEA)
            text(a,'Height 3 stays hidden.',956,375,25,PAPER,c.reveal('Neither outline changes'))
            text(a,'Height 4 changes the side view.',950,448,24,GOLD,c.reveal('rises to four'))
def poster(draw):return draw(8,1)
