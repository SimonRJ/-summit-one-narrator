"""A graduated tank and a two-worker loading bench share a visible time scale."""
BACKGROUND=("#122d38","#17383e")
PAPER, TEAL, GOLD, RED, RULE="#edf6ee","#78d7cd","#ffd38b","#ffa89a","#90acb8"
BRIDGE="The leak starts two minutes after the hoses. Read the gauge at that moment. Which rate belongs to the remaining part of the fill?"
HEAD=("Read a rate","One minute on the gauge","The packing bench","One shared clock","A valve opens","Mark the change","Finish the fill","Check each interval")


def check_maths():
    assert 12//2==6 and (8//4 + 9//3)*6==30
    assert 2*(9+6)+5*(9+6-3)==90 and 7*15-5*3==90


def gauge(a,x,y,level,maxlevel):
    width,height=275,276
    ratio=min(1,max(0,level/maxlevel))
    a.box(x,y,width,height,radius=5,fill="#204450",edge=RULE,stroke=4)
    if ratio>0:a.box(x+5,y+height-5-(height-10)*ratio,width-10,(height-10)*ratio,fill="#407c83",radius=2)
    for i in range(6):
        yy=y+height-8-i*(height-16)/5
        a.line([(x+width-28,yy),(x+width-4,yy)],PAPER,2)
    a.text(f"{round(level)} L",x+width/2,y+height*.59,47,PAPER,bold=True)


def draw(a,n,c):
    a.text(HEAD[n-1],62,75,46,PAPER,bold=True,align="left")
    a.line([(62,125),(1216,125)],RULE,2)
    if n in (1,2):
        for i,v in enumerate((9,18,27)):
            gauge(a,101+i*396,177,v,27)
            a.text(f"{i+1} min",238+i*396,495,36,GOLD,bold=True)
        if n==2:a.text("Second hose   12 L ÷ 2 min = 6 L/min",640,558,32,PAPER,opacity=c.reveal("six litres per minute"))
    elif n in (3,4):
        for y,worker,total,mins,rate in ((190,"Aya",8,4,2),(365,"Rob",9,3,3)):
            a.text(worker,84,y+32,35,PAPER,bold=True,align="left")
            for i in range(total):
                xx=220+i*50
                a.box(xx,y+4,41,46,fill="#bd935e",edge=GOLD,radius=4)
                a.line([(xx+20,y+5),(xx+20,y+23)],PAPER,3)
            a.text(f"{total} boxes in {mins} min",220,y+86,29,PAPER,align="left")
            if n==4:a.text(f"{rate} boxes / min",1020,y+44,35,TEAL,bold=True,opacity=c.reveal("two boxes" if rate==2 else "three"))
        if n==4:a.text("6 × (2 + 3) = 30 boxes",640,550,38,GOLD,bold=True,opacity=c.reveal("thirty"))
    else:
        if n==5:level=0
        elif n==6:level=30*c.reveal("thirty litres")
        else:level=30+60*c.reveal("five more minutes" if n==7 else "each change mark")
        gauge(a,109,183,level,90)
        a.text("Target   90 L",245,510,31,GOLD,bold=True)
        for y,col,label in ((211,TEAL,"Inlet A   +9 L/min"),(283,TEAL,"Inlet B   +6 L/min"),(355,RED,"Leak      −3 L/min")):
            a.line([(472,y),(505,y)],col,8)
            a.text(label,529,y,34,PAPER,align="left",bold=True)
        a.line([(481,492),(1165,492)],RULE,4)
        for x,label in ((481,"0 min"),(681,"2 min"),(1165,"7 min")):
            a.line([(x,479),(x,505)],PAPER,3)
            if label!="7 min" or n>=7:a.text(label,x,536,29,GOLD,bold=True)
        a.text("Valve opens",681,451,26,RED)
        if n>=7:a.text("15 − 3 = 12 L/min",1001,414,30,TEAL,bold=True,opacity=c.reveal("twelve litres") if n==7 else 1)


def poster(draw):
    return draw(7,1)
