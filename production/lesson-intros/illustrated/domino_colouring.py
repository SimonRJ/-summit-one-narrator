"""S019: exact paired counters and a four-by-four board with two missing corners."""
from math import sin,cos,pi
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def pairs(a,count,x0,y,space,col,p=1):
    for i in range(count):
        x=x0+i*space
        a.circle((x,y-13),9,col,p);a.circle((x,y+13),9,col,p)
        a.path(((x,y-5),(x,y+5)),col,2,p)


def pair_rows(a,p=1,q=1):
    text(a,'15',100,270,44,BLUE,p);pairs(a,7,220,270,115,BLUE,p)
    a.circle((1050,270),11,PINK,p)
    text(a,'20',100,440,44,GOLD,q);pairs(a,10,205,440,95,GOLD,q)


def number_line(a,token=15,arc=0,unreachable=0):
    x0=180;step=92;y=375
    a.path(((x0,y),(x0+10*step,y)),SOFT,3)
    for n in range(12,23):
        x=x0+(n-12)*step;col=BLUE if n%2 else GOLD
        a.path(((x,y-10),(x,y+10)),col,4);text(a,str(n),x,y+55,30,col)
    a.circle((x0+(token-12)*step,y-arc),16,AQUA)
    text(a,'start: 15',x0+3*step,235,30,AQUA);text(a,'target: 20',x0+8*step,235,30,PINK)
    a.path(((x0+8*step-30,275),(x0+8*step+30,335)),PINK,4,unreachable)
    a.path(((x0+8*step-30,335),(x0+8*step+30,275)),PINK,4,unreachable)


def board(a,x=250,y=185,u=78,colour=1,remove=1):
    """The missing cells are exactly top-left and bottom-right."""
    for row in range(4):
        for col in range(4):
            removed=(row,col) in ((0,0),(3,3))
            base=BLUE if (row+col)%2==0 else GOLD
            amount=(.60*colour+.12*(1-colour))*(1-remove if removed else 1)
            a.rect(x+col*u+2,y+row*u+2,u-4,u-4,base,amount)
            corners=((x+col*u,y+row*u),(x+(col+1)*u,y+row*u),
                     (x+(col+1)*u,y+(row+1)*u),(x+col*u,y+(row+1)*u),(x+col*u,y+row*u))
            a.path(corners,SOFT,2,.8)
            if removed:
                a.path(((x+col*u+14,y+row*u+14),(x+(col+1)*u-14,y+(row+1)*u-14)),PINK,3,remove)
                a.path(((x+col*u+14,y+(row+1)*u-14),(x+(col+1)*u-14,y+row*u+14)),PINK,3,remove)


def domino(a,cx,cy,u,theta=0,alpha=1,coloured=True):
    """Two congruent adjacent squares; the whole shape remains 2:1 when rotated."""
    def P(x,y):return (cx+x*cos(theta)-y*sin(theta),cy+x*sin(theta)+y*cos(theta))
    left=[P(-u,-u/2),P(0,-u/2),P(0,u/2),P(-u,u/2)]
    right=[P(0,-u/2),P(u,-u/2),P(u,u/2),P(0,u/2)]
    a.polygon(left,BLUE if coloured else SOFT,.72*alpha)
    a.polygon(right,GOLD if coloured else SOFT,.72*alpha)
    a.path(left+[left[0]],WHITE,3,alpha);a.path(right+[right[0]],WHITE,3,alpha)


def intro(a,c):
    a.heading('Pairing exposes parity',BLUE)
    p=c.after('even number as pairs')
    pairs(a,3,340,285,90,BLUE,p);text(a,'6: even',430,385,34,BLUE,p)
    q=c.after('odd number as pairs')
    pairs(a,3,730,285,90,GOLD,q);a.circle((1020,285),11,PINK,q)
    text(a,'7: odd',820,385,34,GOLD,q)
    text(a,'one counter remains unpaired',640,530,30,SOFT,c.after('one left over'))


def exams(a,c):
    a.heading('Colours can explain an impossibility',AQUA)
    p=c.after('two-colour pattern')
    if p>0:board(a,470,190,85,p,0)
    text(a,'adjacent squares have opposite colours',640,570,29,SOFT,p)


def easy(a,c):
    a.heading('15 + 20: odd or even?',BLUE)
    pair_rows(a,c.after('fifteen'),c.after('twenty'))
    text(a,'Look for an unpaired counter',640,550,30,SOFT,c.after('unpaired counters'))


def easy_answer(a,c):
    a.heading('One counter remains unpaired',BLUE)
    pair_rows(a,c.opening(),c.opening())
    text(a,'one extra',1090,335,29,PINK,c.after('one extra counter'))
    text(a,'15 + 20 = 35, odd',640,555,40,WHITE,c.after('thirty-five'))


def jump_prompt(a,c):
    a.heading('Can even moves reach 20?',GOLD)
    p=c.after('even number of steps',1.6);q=c.after('direction may change',1.6)
    if q>0:token=17-2*q;arc=75*sin(pi*q)
    else:token=15+2*p;arc=75*sin(pi*p)
    number_line(a,token,arc)
    text(a,'Each move may be any even length',640,535,31,SOFT,c.after('even number of steps'))


def jump_answer(a,c):
    a.heading('Even moves preserve oddness',GOLD)
    p=c.after('Adding an even number',1.8);q=c.after('Subtracting an even number',1.8)
    if q>0:token=19-2*q;arc=75*sin(pi*q)
    else:token=15+4*p;arc=75*sin(pi*p)
    number_line(a,token,arc,c.after('unreachable'))
    text(a,'odd ± even = odd',640,530,40,WHITE,c.after('remain odd'))


def puzzle(a,c):
    a.heading('Can dominoes cover this board?',VIOLET)
    p=c.after('corners removed',.8)
    board(a,230,185,80,0,p)
    q=c.after('two adjacent squares')
    domino(a,950,280,70,alpha=q,coloured=False)
    text(a,'one domino covers two adjacent cells',950,430,30,SOFT,q)
    text(a,'no overlap',950,520,33,PINK,c.after('No overlap'))


def proof(a,c):
    a.heading('Colour the board',VIOLET)
    colour=c.after('chessboard',.8)
    restore=c.after('grid began with eight',.8)
    remove=max(0,min(1,1-restore+c.after('Removing both corners',1.5)))
    board(a,230,185,80,colour,remove)
    p=c.after('one square of each colour')
    domino(a,950,280,70,alpha=p)
    text(a,'one of each colour',950,390,34,WHITE,p)
    before=c.after('eight squares of each colour')*(1-remove)
    after=c.after('six of one colour',.7)
    text(a,'8 blue   •   8 gold',950,480,33,WHITE,before)
    text(a,'6 blue   •   8 gold',950,480,33,WHITE,after)
    text(a,'cannot be balanced',950,555,31,PINK,c.after('cannot balance'))


def rotation(a,c):
    a.heading('Fourteen cells are not enough information',VIOLET)
    board(a,230,185,80,1,1)
    p=c.after('Rotating a domino',1.6)
    domino(a,950,280,70,theta=p*pi/2)
    text(a,'14 cells → 7 dominoes',950,430,33,WHITE,c.after('even number'))
    text(a,'7 need 7 blue and 7 gold',950,500,29,SOFT,c.after('split by colouring'))
    text(a,'only 6 blue remain',950,565,31,PINK,c.after('one square of each colour'))


def mistakes(a,c):
    a.heading('A parity check can rule a move out',PINK)
    text(a,'odd + even = odd',640,255,43,BLUE,c.after('odd or even'))
    text(a,'matching parity does not prove a route exists',640,390,32,PINK,c.after('does not prove'))
    text(a,'also construct a legal arrangement',640,520,32,WHITE,c.after('Use a construction'))


def recap(a,c):
    a.heading('Pairs, moves, and colour balance',AQUA)
    text(a,'15 + 20 = 35: odd',640,225,38,BLUE,c.after('one move'))
    text(a,'odd ± even stays odd',640,325,38,GOLD,c.after('stays fixed'))
    text(a,'6 blue ≠ 8 gold: no domino tiling',640,425,35,AQUA,c.after('colour balance'))
    text(a,'explain why each piece obeys the rule',640,525,30,SOFT,c.after('explaining why'))


SCENES=(intro,exams,easy,easy_answer,jump_prompt,jump_answer,puzzle,proof,rotation,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
