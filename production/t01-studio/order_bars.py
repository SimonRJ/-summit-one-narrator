"""T02.3. All bar widths use the same unit; x can vary while the gold five stays fixed."""
from math import pi, sin
from stage import BLUE, GOLD, MINT, MUTED, PANEL, WHITE, between, blend, mix

UNIT = 29
LEFT = 237


def length(stage, left, y, value, ink, symbol, opacity=1):
    width = UNIT*value
    if width < 1 or opacity <= 0:
        return
    stage.box(left, y-33, width, 66, radius=2, fill=blend(PANEL, ink, .26), edge=ink, stroke=3, opacity=opacity)
    for unit in range(1, int(value)+1):
        if unit < value-.02:
            position=left+unit*UNIT
            stage.line(((position,y+24),(position,y+31)), ink, 1.5, opacity*.8)
    if width > 44:
        stage.text(symbol, left+width/2, y, 37, WHITE, bold=True, opacity=opacity)


def double_sum(stage, moment):
    t=moment.t
    x=3+5*between(t,moment.start+.35,2.15)
    add=moment.reveal('adding five makes a bar',1.0)
    duplicate=moment.reveal('doubling makes two copies',1.65)
    collect=moment.reveal('collect its parts',1.15)
    result=moment.reveal('two x plus ten',.6)
    stage.heading('Double the whole bar')
    stage.text('The blue length can vary. Each gold length is 5.',640,145,31,MUTED)
    stage.text('Start',151,255,29,MUTED,bold=True)
    length(stage,LEFT,255,x,BLUE,'x')
    length(stage,LEFT+x*UNIT,255,5*add,GOLD,'5',add)
    stage.text('Two copies',138,428,27,MUTED,bold=True,opacity=duplicate)
    if duplicate:
        for copy in range(2):
            anchor=LEFT+copy*(x+5)*UNIT*duplicate
            y=mix(255,428,duplicate)-20*sin(pi*duplicate)
            if copy==0:
                length(stage,anchor,y,x,BLUE,'x',duplicate)
                length(stage,anchor+x*UNIT+collect*x*UNIT,y+47*sin(pi*collect),5,GOLD,'5',duplicate)
            else:
                length(stage,anchor-collect*5*UNIT,y-48*sin(pi*collect),x,BLUE,'x',duplicate)
                length(stage,anchor+x*UNIT,y,5,GOLD,'5',duplicate)
    stage.terms([('2(x + 5)',WHITE,result),('=',MUTED,result),('2x',BLUE,result),('+ 10',GOLD,result)],555,52)


def compare_orders(stage,moment):
    t=moment.t
    built=moment.reveal('that gives two copies',.9)
    add=moment.reveal('add five once',.85)
    pair=moment.reveal('pair those matching pieces',1.0)
    difference=moment.reveal('the extra five',.7)
    x=8-5*between(t,moment.at('the extra five')+.60,1.25)
    stage.heading('What stays different as x changes?')
    stage.text('Both rows use the same starting length.',640,145,31,MUTED)
    stage.text('Order A',145,250,31,MUTED,bold=True)
    stage.text('Order B',145,425,31,MUTED,bold=True)
    for y,b in [(250,False),(425,True)]:
        length(stage,LEFT,y,x,BLUE,'x')
        length(stage,LEFT+x*UNIT,y,x,BLUE,'x',built if b else 1)
        length(stage,LEFT+2*x*UNIT,y,5,GOLD,'5',add if b else 1)
    edge=LEFT+(2*x+5)*UNIT
    length(stage,edge,250,5,GOLD,'5')
    for xx in (LEFT,LEFT+x*UNIT,LEFT+2*x*UNIT,edge):
        stage.line(((xx,287),(xx,386)),MINT,2,pair*.8)
    stage.bracket(edge,edge+5*UNIT,318,'5 extra',GOLD,difference)
    stage.text('2(x + 5) = (2x + 5) + 5',640,554,44,WHITE,bold=True,opacity=difference)
