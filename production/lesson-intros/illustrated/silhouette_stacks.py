"""S072. Build and slice isometric models, then realise both bounds for two fixed views."""
from itertools import product
from captioned_film import cue, mix
ID='S072'
ORIGINAL='17ad080f06a98b6047e9c271db3f437d69dfe61d5d9c363012d71a3d211bdb7c'
START=(0,17.56,32.6,46.97,58.81,74.46,91.26,112.35,133.29,151.53,166.73)
POSTER=147.6
PAPER='#122b37'
WHITE, DIM, GRID, BASE='#fff2da','#c4d7dc','#52717c','#254651'
GOLD, MINT, CORAL='#ffd384','#89dfce','#ffa78a'
PALETTE=(('#8fe4d1','#52aeac','#357e8a'),('#ffc597','#d58d6c','#ac6e5a'),('#b1d7ff','#7b9fc5','#596eaa'),('#e8c4f1','#b192c4','#84699e'),('#f7df80','#c7ad56','#9d8748'),('#c4e89b','#8eba78','#658958'))
FULL=((2,2,2),(2,2,2),(2,2,2))
SIX=((2,4,3),(2,5,1))
LOW=((3,6,1),(1,1,3))
HIGH=((3,6,3),(3,3,3))

def label(c,s,x,y,z=29,colour=WHITE):
    c.text(s,x,y,z,colour,bold=True)
def header(c,s):
    c.text(s,55,54,41,WHITE,'lm',True)
    c.line([(55,99),(1225,99)],GRID,2)
def model(c,board,ox,oy,size=49,levels=None,explosion=0,colour_by_layer=False):
    # Positive row and column directions both move toward the camera.
    def vertex(col,row,z,offset=0):
        return (ox+(col-row)*size,oy+(col+row)*size*.45-z*size*1.03-offset)
    for r,row in enumerate(board):
        for k,h in enumerate(row):
            a,b,d,e=[vertex(k+dx,r+dy,0) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
            c.poly([a,b,d,e],BASE,GRID,1)
    for z in range(max(map(max,board))):
        if levels is not None and z>=levels:break
        for r,row in enumerate(board):
            for k,h in enumerate(row):
                if z>=h:continue
                offset=z*explosion
                top=[vertex(k+dx,r+dy,z+1,offset) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
                bottom=[vertex(k+dx,r+dy,z,offset) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
                bright,mid,dark=PALETTE[z%6 if colour_by_layer else (0 if r==0 else 2 if r==1 else 3)]
                a,b,d,e=top
                c.poly([e,d,bottom[2],bottom[3]],mid,PAPER,2)
                c.poly([b,d,bottom[2],bottom[1]],dark,PAPER,2)
                c.poly([a,b,d,e],bright,PAPER,2)

def grid(c,b,x,y,step=66,active=None,format_level=False):
    for r,row in enumerate(b):
        for col,h in enumerate(row):
            xx,yy=x+step*col,y+step*r
            highlight=active is None or (r,col)==active
            colour=PALETTE[(r*3+col)%6][0] if format_level and h else MINT if highlight and h else DIM
            c.rect(xx,yy,step-4,step-4,BASE if h else PAPER,colour if h else GRID,2)
            if h:label(c,str(h) if not format_level else '●',xx+(step-4)/2,yy+(step-4)/2,round(step*.41),colour)
def silhouettes(c,values,x,y,unit,name):
    for col,h in enumerate(values):
        for z in range(h):
            c.rect(x+col*unit,y-(z+1)*unit,unit-2,unit-2,'#6396a6',PAPER,1)
        label(c,str(h),x+(col+.5)*unit,y-h*unit-18,23,GOLD)
    c.line([(x-7,y),(x+len(values)*unit+6,y)],DIM,2)
    label(c,name,x+len(values)*unit/2,y+33,22,DIM)

def open_scene(c,t):
    header(c,'A solid has a height at every footprint cell')
    model(c,SIX,339,412,48,levels=max(1,min(5,1+int(t/1.1))),colour_by_layer=True)
    if t>3:
        grid(c,SIX,708,184,80)
        label(c,'Stack heights',829,390,30)
    if t>9:
        silhouettes(c,(2,5,3),1003,476,27,'Column view')
        label(c,'A silhouette keeps only the tallest stack on each sightline.',640,560,27,MINT)
def context(c,t):
    header(c,'What information does the picture give?')
    model(c,SIX,270,401,45)
    label(c,'Solid',285,544)
    if t>20:
        grid(c,SIX,555,241,66)
        label(c,'Footprint',652,519)
    if t>24:
        silhouettes(c,(2,5,3),995,409,34,'Three columns')
        label(c,'View',1046,519)
    if t>29:label(c,'Exact stack heights or only the skyline?',640,576,25,MINT)
def easy_q(c,t):
    header(c,'Three wide, three deep, two high')
    model(c,FULL,405,332,71)
    label(c,'3 columns × 3 rows',932,234,34)
    if t>36:label(c,'2 layers',932,320,36,GOLD)
    if t>40:label(c,'How many unit cubes?',932,424,32)
def easy_a(c,t):
    header(c,'Lift the top layer to see what is hidden')
    model(c,FULL,385,349,61,levels=1 if t<48.2 else 2,explosion=55*cue(t,48.4,1.85),colour_by_layer=True)
    grid(c,((1,1,1),)*3,775,163,58,format_level=True)
    label(c,'9 per layer',868,398,32)
    if t>51:label(c,'2 × 9 = 18',868,481,43,GOLD)
    if t>54:label(c,'The centre cube counts in each layer.',640,566,27,MINT)
def medium_q(c,t):
    header(c,'Six stacks, six different positions')
    model(c,SIX,323,422,51,levels=1+min(4,int(max(0,t-59)/.93)),colour_by_layer=True)
    grid(c,SIX,789,220,76)
    label(c,'First and second rows',900,432,28)
    if t>68:label(c,'Count every cube, including the ones behind.',640,554,32,MINT)
def layers(c,t):
    header(c,'Take a horizontal slice at each level')
    layer=min(5,1+int(max(0,t-74.6)/1.45))
    model(c,SIX,280,425,48,levels=layer,colour_by_layer=True)
    for level in range(1,layer+1):
        x=606+((level-1)%3)*202;y=172+((level-1)//3)*146
        plane=tuple(tuple(int(h>=level) for h in row) for row in SIX)
        grid(c,plane,x,y,34,format_level=True)
        label(c,f'L{level}: {sum(map(sum,plane))} ' + ('cube' if level==5 else 'cubes'),x+48,y+93,20,DIM)
    if t>82:label(c,'6 + 5 + 3 + 2 + 1 = 17',904,475,33,GOLD)
    if t>86:label(c,'Height check: 2 + 4 + 3 + 2 + 5 + 1 = 17',640,568,30,MINT)
def skyline_question(c,t):
    header(c,'Two views of six nonempty stacks')
    silhouettes(c,(3,6,3),153,410,35,'Columns 1, 2, 3')
    if t>96:silhouettes(c,(6,3),464,410,35,'Rows 1, 2')
    if t>99:
        for r in range(2):
            for k in range(3):
                x,y=768+k*92,205+r*92
                c.rect(x,y,86,86,BASE,GRID,2)
                label(c,'?',x+43,y+43,36,DIM)
    if t>103:label(c,'What is the least possible total? The greatest?',640,551,34,GOLD)
def minimum(c,t):
    header(c,'For the minimum, make the tall stacks do two jobs')
    board=[[1]*3 for _ in range(2)]
    for at,r,k in ((113,0,0),(115,0,1),(117,1,2)):
        if t>=at:board[r][k]=LOW[r][k]
    model(c,board,319,447,49)
    grid(c,board,757,190,72)
    if t>118:label(c,'3 + 6 + 3 in three columns',900,408,29)
    if t>121:label(c,'Three other stacks need 1 each.',900,464,27,MINT)
    if t>126:label(c,'Minimum = 12 + 3 = 15 cubes',881,540,32,GOLD)
def maximum(c,t):
    header(c,'For the maximum, respect both height limits')
    step=min(6,int(max(0,t-133.3)/1.25)+1)
    b=tuple(tuple(HIGH[r][k] if 3*r+k<step else LOW[r][k] for k in range(3)) for r in range(2))
    model(c,b,312,451,50)
    grid(c,b,760,193,72)
    if t>136:label(c,'Use the lower of the two caps.',901,391,28,MINT)
    if t>141:label(c,'12 in row 1 + 9 in row 2',901,448,29)
    if t>145:label(c,'Maximum = 21 cubes',891,540,36,GOLD)
def pitfall(c,t):
    header(c,'A skyline gives a maximum along a sightline')
    model(c,LOW,268,405,42)
    if t>155:model(c,HIGH,744,405,42)
    if t>158:silhouettes(c,(3,6,3),1001,401,29,'Same columns')
    label(c,'15 cubes',287,511,30,MINT)
    if t>155:label(c,'21 cubes',755,511,30,GOLD)
    if t>162:label(c,'The back stack can be shorter than the silhouette.',640,575,28)
def recap(c,t):
    header(c,'For a bound, draw a model that reaches it')
    if t<173:
        grid(c,LOW,332,203,74)
        silhouettes(c,(3,6,3),788,393,31,'Column maxima')
        silhouettes(c,(6,3),1030,393,31,'Row maxima')
        label(c,'Mark the footprint and both sets of limits.',640,537,32,MINT)
        return
    model(c,LOW,272,395,42);model(c,HIGH,798,395,42)
    label(c,'Least: 15',290,503,32,MINT);label(c,'Greatest: 21',813,503,32,GOLD)
    if t>178:label(c,'Each model has column maxima 3, 6, 3 and row maxima 6, 3.',640,566,27)
SCENES=(open_scene,context,easy_q,easy_a,medium_q,layers,skyline_question,minimum,maximum,pitfall,recap)
def verify():
    assert sum(map(sum,FULL))==18
    assert [sum(h>=z for row in SIX for h in row) for z in range(1,6)]==[6,5,3,2,1]
    assert sum(map(sum,SIX))==17
    def views(b):return tuple(map(max,b)),tuple(map(max,zip(*b)))
    totals=[]
    for cells in product(*(range(1,h+1) for row in HIGH for h in row)):
        b=(cells[:3],cells[3:])
        if views(b)==((6,3),(3,6,3)):totals.append(sum(cells))
    assert views(LOW)==views(HIGH)==((6,3),(3,6,3))
    assert min(totals)==sum(map(sum,LOW))==15 and max(totals)==sum(map(sum,HIGH))==21
