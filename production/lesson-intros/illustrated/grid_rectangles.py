"""S017: draw the exact cell grids and count their permissible boundaries."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def grid(a,x,y,cols,rows,u,pv=1,ph=1,marks=False,labels=False):
    if marks:
        # Rows are numbered from the bottom: A=(2,3), B=(5,3).
        for col,label,colour in ((2,'A',AQUA),(5,'B',PINK)):
            cx=x+(col-.5)*u;cy=y+(rows-3+.5)*u
            a.rect(cx-u/2+3,cy-u/2+3,u-6,u-6,colour,.23)
            text(a,label,cx,cy,35,colour)
    for i in range(cols+1):a.trace(((x+i*u,y),(x+i*u,y+rows*u)),pv,BLUE,3,False)
    for i in range(rows+1):a.trace(((x,y+i*u),(x+cols*u,y+i*u)),ph,GOLD,3,False)
    if labels:
        for i in range(cols):text(a,str(i+1),x+(i+.5)*u,y+rows*u+24,21,SOFT)
        for i in range(rows):text(a,str(rows-i),x-24,y+(i+.5)*u,21,SOFT)


def rectangle(a,x,y,u,left,right,bottom,top,rows=5,col=AQUA,alpha=1):
    """Edges are grid-line coordinates, with the bottom line at coordinate zero."""
    l=x+left*u;r=x+right*u;t=y+(rows-top)*u;b=y+(rows-bottom)*u
    a.path(((l,t),(r,t),(r,b),(l,b),(l,t)),col,7,alpha)


def intro(a,c):
    a.heading('Lines, cells and crossing points',BLUE)
    grid(a,345,215,3,2,145,c.opening(),c.opening())
    p=c.after('points where the lines meet')
    for i in range(4):
        for j in range(3):a.circle((345+i*145,215+j*145),8,AQUA,p)
    text(a,'3 columns',965,270,36,BLUE,c.after('spaces between'))
    text(a,'2 rows',965,350,36,GOLD,c.after('spaces between'))
    text(a,'crossing points',965,450,32,AQUA,p)


def exams(a,c):
    a.heading('Mark the object you are counting',AQUA)
    grid(a,235,175,6,5,60,marks=True,labels=True)
    p=c.after('include one marked cell')
    rectangle(a,235,175,60,1,4,2,4,col=AQUA,alpha=p)
    text(a,'contains A',930,290,36,AQUA,p)
    text(a,'avoids B',930,375,36,PINK,c.after('avoiding another'))
    text(a,'edges lie on grid lines',930,500,29,SOFT,c.after('possible boundaries'))


def crossing_prompt(a,c):
    a.heading('How many crossing points?',BLUE)
    p=c.after('three columns and two rows',.7)
    grid(a,300,230,3,2,135,p,p)
    text(a,'3 columns',930,285,41,BLUE,p)
    text(a,'2 rows',930,390,41,GOLD,p)
    text(a,'Include the outside edges',930,510,30,SOFT,c.after('outside edges'))


def crossing_answer(a,c):
    a.heading('Count the lines first',BLUE)
    v=c.after('four vertical lines',1.0);h=c.after('three horizontal lines',1.0)
    grid(a,300,230,3,2,135,v,h)
    q=c.after('crosses all three',1.5)
    for i in range(4):
        for j in range(3):a.circle((300+i*135,230+j*135),10,AQUA,ease(q*2-(i*3+j)*.06))
    text(a,'4 vertical lines',950,260,36,BLUE,v)
    text(a,'3 horizontal lines',950,345,36,GOLD,h)
    text(a,'4 × 3 = 12 points',950,465,40,WHITE,c.after('twelve crossing points'))


def rectangle_prompt(a,c):
    a.heading('Count every grid-line rectangle',GOLD)
    p=c.after('four columns and three rows',.7)
    grid(a,275,215,4,3,105,p,p)
    text(a,'4 columns × 3 rows',930,250,35,SOFT,p)
    text(a,'Any size counts',930,365,36,WHITE,c.after('any size'))
    text(a,'Squares count too',930,455,36,AQUA,c.after('square counts'))


def rectangle_answer(a,c):
    a.heading('Two lines choose each pair of edges',GOLD)
    grid(a,275,215,4,3,105)
    p=c.after('left and right edge',1)
    rectangle(a,275,215,105,1,4,1,3,rows=3,col=AQUA,alpha=p)
    text(a,'5 vertical lines → 10 pairs',960,255,31,BLUE,c.after('ten choices'))
    text(a,'4 horizontal lines → 6 pairs',960,350,30,GOLD,c.after('six horizontal pairs'))
    text(a,'10 × 6 = 60 rectangles',960,465,34,WHITE,c.after('sixty'))


def challenge(a,c):
    a.heading('Contain A, avoid B',AQUA)
    p=c.after('six column by five row',.7)
    if p>0:grid(a,240,165,6,5,66,p,p,marks=True,labels=True)
    text(a,'rows count from the bottom',920,235,29,SOFT,c.after('rows are numbered'))
    q=c.after('containing all of A',.8)
    rectangle(a,240,165,66,1,4,2,4,col=AQUA,alpha=q)
    text(a,'include all of A',930,335,34,AQUA,q)
    text(a,'exclude the interior of B',930,415,31,PINK,c.after('none of the interior'))
    text(a,'How many rectangles?',930,520,34,WHITE,c.after('Count the grid-line rectangles'))


def boundary_choices(a,c):
    a.heading('Choose one boundary at a time',AQUA)
    x,y,u=240,165,66;grid(a,x,y,6,5,u,marks=True,labels=True)
    both=c.after('Now require it to contain both cells',.8)
    rectangle(a,x,y,u,1,4,2,4,col=AQUA,alpha=1-both)
    rectangle(a,x,y,u,1,5,2,4,col=PINK,alpha=both)
    v=c.after('left and right edges',.8);h=c.after('lower and upper edges',.8)
    # Dots are candidate grid lines: left {0,1}, right {2,3,4,5,6},
    # lower {0,1,2}, upper {3,4,5}. Rows count upward from the bottom.
    for i in (0,1):a.circle((x+i*u,y+5*u+26),7,BLUE,v*(1-both))
    for i in (2,3,4,5,6):a.circle((x+i*u,y-26),7,GOLD,v*(1-both))
    for n in (0,1,2):a.circle((x+6*u+25,y+(5-n)*u),7,AQUA,h*(1-both))
    for n in (3,4,5):a.circle((x-25,y+(5-n)*u),7,VIOLET,h*(1-both))
    text(a,'left 2  ×  right 5',945,265,32,WHITE,v*(1-both))
    text(a,'lower 3  ×  upper 3',945,350,32,WHITE,h*(1-both))
    text(a,'2 × 5 × 3 × 3 = 90',945,445,34,WHITE,c.after('ninety rectangles')*(1-both))
    text(a,'now contain both A and B',945,360,31,PINK,both)


def subtract(a,c):
    a.heading('Subtract rectangles that contain B',PINK)
    grid(a,240,165,6,5,66,marks=True,labels=True)
    rectangle(a,240,165,66,1,5,2,4,col=PINK)
    p=c.after('two two three and three',.7)
    text(a,'2 × 2 × 3 × 3 = 36',945,280,35,PINK,p)
    text(a,'contain both A and B',945,350,30,SOFT,p)
    q=c.after('subtract those',.8)
    text(a,'90 − 36 = 54',945,465,45,WHITE,q)
    text(a,'contain A, avoid B',945,535,29,AQUA,c.after('fifty-four rectangles'))


def mistakes(a,c):
    a.heading('Count the outside lines',BLUE)
    grid(a,345,250,5,1,105)
    p=c.after('six lines')
    for i in range(6):a.circle((345+i*105,250),9,AQUA,p)
    text(a,'5 cells',640,425,38,BLUE,c.after('five cells'))
    text(a,'6 boundary lines',640,515,38,AQUA,p)


def recap(a,c):
    a.heading('Choose lines and check constraints',BLUE)
    text(a,'3 × 2 cells → 4 × 3 = 12 points',640,230,37,WHITE,c.after('crossing points'))
    text(a,'4 × 3 cells → 10 × 6 = 60 rectangles',640,330,35,GOLD,c.after('outer boundaries'))
    text(a,'contain A, avoid B → 90 − 36 = 54',640,440,35,AQUA,c.after('cell to be excluded'))
    text(a,'subtract only rectangles that include B',640,535,29,SOFT,c.after('subtract exactly'))


SCENES=(intro,exams,crossing_prompt,crossing_answer,rectangle_prompt,rectangle_answer,
        challenge,boundary_choices,subtract,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
