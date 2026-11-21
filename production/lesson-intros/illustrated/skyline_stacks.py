"""S087. Build each stack from unit cubes and project the same model onto both views."""
from itertools import product
from hidden_cubes import solid, SEA, SUN, RIND, INNER

PAPER = '#152735'
INK, MUTED, LINE = '#fff4e1', '#c1d2d2', '#73949c'
AQUA, GOLD, RED = SEA[0], SUN[0], RIND[0]
MEDIUM = ((1, 3, 4), (2, 4, 1))
LOW = ((1, 6, 2), (2, 1, 1))
HIGH = ((2, 6, 2), (2, 2, 2))
FULL = ((2, 2, 2, 2), (2, 2, 2, 2))
COLOURS = (SUN, SEA, RIND, INNER)

def heading(c, value):
    c.text(value, 53, 60, 39, INK, 'lm', True)
    c.line([(53, 107), (1227, 107)], LINE)

def line(c, value, y, ink=INK, size=29):
    c.text(value, 943, y, size, ink, bold=True)

def cells(rows):
    # First spoken row is the front row. Increasing y points toward the viewer.
    return [(x, 1-r, z) for r,row in enumerate(rows) for x,height in enumerate(row) for z in range(height)]

def model(c, rows, *, gap=0, marked=None, cube=61, centre=(328,350), frame_height=None):
    colours = lambda p: COLOURS[p[2] % 4] if marked is None or p in marked else ('#91a5aa','#637c84','#4f6971')
    solid(c, cells(rows), (len(rows[0]), 2, frame_height or max(1,max(map(max,rows)))), centre, cube,
          angle=24, gap=gap, colour=colours)

def plan(c, rows, *, left=800, top=269, size=78, caps=False, mask=None):
    for r,row in enumerate(rows):
        y = top + (1-r)*size
        c.text(('Front','Back')[r],left-13,y+size/2,23,MUTED,'rm',True)
        for x,h in enumerate(row):
            xx=left+x*size
            fill='#2b5663' if mask is None or (r,x) in mask else '#213744'
            c.rect(xx,y,size-4,size-4,fill,LINE)
            if h is not None:c.text(str(h),xx+(size-4)/2,y+(size-4)/2,34,INK,bold=True)
        if caps:c.text(('≤ 6','≤ 2')[r],left+len(row)*size+8,y+size/2,24,GOLD,'lm',True)
    if caps:
        for x,v in enumerate((2,6,2)):c.text(f'≤ {v}',left+(x+.5)*size,top-25,24,AQUA,bold=True)

def profile(c, heights, left, bottom, unit, colour, label, names):
    c.text(label,left+len(heights)*unit/2,bottom-max(heights)*unit-27,23,INK,bold=True)
    for x,height in enumerate(heights):
        for z in range(height):
            c.rect(left+x*unit,bottom-(z+1)*unit,unit-2,unit-2,colour,LINE,1)
        c.text(str(names[x]),left+(x+.5)*unit,bottom+18,18,MUTED,bold=True)

def views(c, side=True):
    profile(c,(2,6,2),675,451,32,AQUA,'Front view',('L','M','R'))
    if side:profile(c,(6,2),982,451,32,GOLD,'Side view',('F','B'))

def intro(c,q):
    heading(c,'What does a silhouette tell us?')
    p=q.after('several solids may fit',1.8)
    h=1+int(2*p+.001)
    rows=((3,1,2),(h,1,1))
    model(c,rows,cube=65)
    if q.after('height of each stack'):plan(c,rows)
    if q.after('even where a view hides'):line(c,'Front peaks: 3, 1, 2',489,AQUA)
    if p:line(c,f'Cube total: {sum(map(sum,rows))}',548,GOLD)

def exam(c,q):
    heading(c,'Read the kind of clue the exam gives')
    if not q.after('just a front view'):
        model(c,MEDIUM)
        if q.after('mark the heights'):plan(c,MEDIUM)
        if q.after('horizontal layers'):line(c,'Layer 3 reaches three stacks',512,AQUA,25)
    else:
        model(c,LOW)
        views(c,bool(q.after('and a side view')))
        if q.after('a peak in both views'):line(c,'One stack supplies both sixes',536,AQUA,26)

def easy(c,q):
    heading(c,'A solid block of unit cubes')
    model(c,FULL,cube=65)
    line(c,'4 cubes wide',213,AQUA)
    if q.after('two deep'):line(c,'2 deep',291,AQUA)
    if q.after('two high'):line(c,'2 high',370,AQUA)
    if q.after('cells of one layer'):line(c,'How many in one layer?',491,GOLD,29)

def easy_answer(c,q):
    heading(c,'Trace the footprint, then lift the upper layer')
    split=q.after('Lift the top layer',1.7)
    model(c,FULL,cube=63,gap=79*split)
    front=q.after('four positions across the front',1)
    back=q.after('four across the back',1)
    for r,p in enumerate((front,back)):
        yy=307 if r==0 else 237
        for x in range(4):c.rect(788+68*x,yy,63,63,GOLD if x<round(4*p) else PAPER,LINE)
    if q.after('eight cubes on the bottom'):line(c,'8 positions on one floor',424)
    if q.after('sixteen cubes'):line(c,'8 + 8 = 16 cubes',512,AQUA,35)

def medium(c,q):
    heading(c,'Reconstruct the six stacks')
    first,_=q.find('one three and four'); second,_=q.find('two four and one')
    marks=[first,first+1,first+3,second,second+1,second+3]
    heights=list(sum(MEDIUM,()))
    shown=[h if q.t>=q.scene['words'][i]['start'] else None for i,h in zip(marks,heights)]
    rows=(shown[:3],shown[3:])
    model(c,[[h or 0 for h in row] for row in rows],frame_height=4);plan(c,rows)
    if q.after('Count the cubes'):line(c,'How many cubes altogether?',511,GOLD,28)

def levels(c,q):
    heading(c,'Count the stacks reaching each level')
    words=q.scene['words'];start,_=q.find('six four three and two')
    level=sum(q.t>=words[start+d]['start'] for d in (0,1,2,4))
    marked=None if not level else {p for p in cells(MEDIUM) if p[2]==level-1}
    model(c,MEDIUM,marked=marked,gap=12*q.after('For every level'))
    mask={(r,x) for r,row in enumerate(MEDIUM) for x,h in enumerate(row) if h>=level}
    plan(c,MEDIUM,mask=mask)
    if level:line(c,f'Level {level}: {len(mask)} cubes',176,AQUA)
    if q.after('giving fifteen'):line(c,'6 + 4 + 3 + 2 = 15',506,GOLD,34)

def hard(c,q):
    heading(c,'Two views of six nonempty stacks')
    plan(c,((None,)*3,)*2,left=183,top=263)
    if q.after('From the front'):views(c,bool(q.after('From the side')))
    if q.after('least and greatest'):line(c,'What totals are possible?',551,AQUA)

def minimum(c,q):
    heading(c,'Find the least total and build a model')
    vals=[[0]*3 for _ in range(2)]
    if q.after('six in the front middle'):vals[0][1]=6
    if q.after('two at the back left'):vals[1][0]=2
    if q.after('two at the front right'):vals[0][2]=2
    if q.after('Fill the remaining cells'):vals=[list(row) for row in LOW]
    model(c,vals,frame_height=6);plan(c,[[v or None for v in row] for row in vals],caps=True)
    if q.after('two six and two'):
        line(c,'2 + 6 + 2',161,AQUA)
        if not any(map(any,vals)):
            profile(c,(2,6,2),178,442,29,AQUA,'Required peaks',('L','M','R'))
            if q.after('one cube each'):
                for i in range(3):c.rect(341+41*i,413,28,28,GOLD,LINE)
                c.text('Other stacks',396,466,23,INK,bold=True)
    if q.after('one cube each'):line(c,'+ 1 + 1 + 1',201,GOLD)
    if q.after('lower bound of thirteen'):line(c,'At least 13 cubes',481)
    if q.after('thirteen is attainable'):line(c,'This model has 13',540,AQUA)

def maximum(c,q):
    heading(c,'Use the lower of the two caps at each cell')
    vals=[[0]*3 for _ in range(2)]
    i,_=q.find('two six two in the first row')
    for x in range(3):
        if q.t>=q.scene['words'][i+x]['start']:vals[0][x]=HIGH[0][x]
    if q.after('and two in every position',1):
        vals[1]=[2 if x<round(3*q.after('and two in every position',1)) else 0 for x in range(3)]
    model(c,vals,frame_height=6);plan(c,[[v or None for v in row] for row in vals],caps=True)
    if q.after('both views still fit'):line(c,'Front: 2, 6, 2     Side: 6, 2',497,AQUA,25)
    if q.after('sixteen cubes'):line(c,'10 + 6 = 16 cubes',548,GOLD)

def mistakes(c,q):
    heading(c,'Test a proposed model from the other side')
    p=q.after('Remove four cubes',1.7)
    h=6-int(4*p+.001);rows=(HIGH[0],(2,h,2));model(c,rows)
    plan(c,rows,caps=True)
    if q.after('six cubes high'):line(c,f'Back peak: {h}',488,RED if h>2 else AQUA)
    if q.after('front peak stays six'):line(c,'Front middle still reaches 6',545,AQUA,26)

def recap(c,q):
    heading(c,'Choose a check for an unfamiliar solid')
    if not q.after('only the views'):
        model(c,MEDIUM,gap=17*q.after('one floor at a time'))
        if q.after('heights are known'):plan(c,MEDIUM)
    else:
        rows=HIGH if q.after('For a maximum') else LOW
        model(c,rows);plan(c,rows,caps=True)
        if q.after('For a minimum'):line(c,'Minimum 13' if rows==LOW else 'Maximum 16',497,GOLD)
        if q.after('both directions'):line(c,'Front: 2, 6, 2     Side: 6, 2',548,AQUA,25)

SCENES=(intro,exam,easy,easy_answer,medium,levels,hard,minimum,maximum,mistakes,recap)

def verify():
    assert len(cells(FULL))==16 and len(cells(MEDIUM))==15
    assert [sum(p[2]==i for p in cells(MEDIUM)) for i in range(4)]==[6,4,3,2]
    def fits(rows):
        return tuple(map(max,rows))==(6,2) and tuple(map(max,zip(*rows)))==(2,6,2)
    totals=[sum(row) for row in product(*(range(1,h+1) for h in (2,6,2,2,2,2))) if fits((row[:3],row[3:]))]
    assert fits(LOW) and fits(HIGH) and (min(totals),max(totals))==(len(cells(LOW)),len(cells(HIGH)))==(13,16)
