"""Admission codes on tickets, a two-sided distance dial and a divisibility sieve."""
BACKGROUND=("#eee5d4","#e3d7c0")
INK, BLUE, RED, PAPER, LINE="#2b3036","#245978","#92432f","#fff8e7","#88765e"
BRIDGE="Undo the final stamp first. After subtracting two from the smudged range, which tickets could really have come out of the tripling stamp?"
HEAD=("The hidden first ticket","Walk the belt backwards","A code with two origins","Read the admission rule","The smudged exit label","Filter before dividing","Recover the four tickets","Run the tickets forwards")


def check_maths():
    assert 7*2+5==19
    assert [i for i in range(1,21) if abs(i-10)==4]==[6,14]
    assert [i for i in range(12,26) if 34<=(i-4)*3+2<=46]==[15,16,17,18]
    assert [(i-4)*3+2 for i in (15,16,17,18)]==[35,38,41,44]


def ticket(a,x,y,w,title,value,alpha=1):
    a.box(x,y,w,104,fill=PAPER,edge=LINE,stroke=3,radius=13)
    a.dot(x+15,y+52,6,RED);a.text(title,x+w/2,y+26,22,BLUE,bold=True)
    a.text(value,x+w/2,y+72,37,INK,bold=True,opacity=alpha)


def draw(a,n,c):
    a.text(HEAD[n-1],63,74,46,INK,bold=True,align="left");a.line([(63,124),(1215,124)],LINE,3)
    if n in (1,2):
        for i,(lab,val) in enumerate(zip(("Entrance","Between stamps","Exit"),(("?","?","19") if n==1 else ("7","14","19")))):
            alpha=1 if n==1 or i==2 else c.reveal("get seven" if i==0 else "get fourteen"); ticket(a,80+i*434,230,245,lab,val,alpha)
        for x,word in ((327,"× 2"),(761,"+ 5")):
            a.arrow((x+12,280),(x+168,280),BLUE,1,4);a.text(word,x+87,226,29,BLUE,bold=True)
        if n==2:
            a.arrow((1085,417),(208,417),RED,c.reveal("Undo the added five"),5)
            a.text("19 − 5 = 14     then     14 ÷ 2 = 7",640,492,37,INK,bold=True,opacity=c.reveal("get seven"))
    elif n in (3,4):
        a.text("Distance from 10",640,192,35,BLUE,bold=True)
        X=lambda t:110+(t-1)*66
        a.line([(X(1),366),(X(17),366)],INK,4)
        for t in range(1,18):
            a.line([(X(t),355),(X(t),378)],INK,3);a.text(str(t),X(t),405,24,INK)
        a.dot(X(10),366,10,BLUE)
        for num in (6,14):
            a.arrow((X(10),317),(X(num),317),RED,c.reveal("four places" if n==3 else "both lie"),4)
            if n==4:a.dot(X(num),366,10,RED)
        a.text("Exit stamp = 4" if n==3 else "Drawer admits numbers 1–9",640,492,35,INK,bold=True)
        if n==4:a.text("6 fits the drawer",640,549,31,BLUE,bold=True,opacity=c.reveal("Only six"))
    elif n==5:
        for i,(lab,val) in enumerate((("Entrance","12–25"),("Stamp 1","− 4"),("Stamp 2","× 3"),("Stamp 3","+ 2"),("Exit","34–46"))):
            ticket(a,62+i*245,257,193,lab,val)
            if i<4:a.arrow((260+i*245,309),(300+i*245,309),BLUE,1,4)
        a.text("Which whole tickets fit both ranges?",640,482,38,INK,bold=True)
    elif n==6:
        a.text("After undoing + 2",640,184,33,BLUE,bold=True)
        for i,v in enumerate(range(32,45)):
            x=72+89*i;ok=v%3==0;alpha=c.reveal("multiples of three") if ok else 1
            a.box(x,279,71,81,fill=PAPER,edge=RED if ok else LINE,stroke=5 if ok else 2,radius=8)
            a.text(str(v),x+36,320,31,RED if ok else INK,bold=ok,opacity=alpha)
        a.text("What can a tripling stamp print?",640,488,37,INK,bold=True)
    else:
        labs,arrs=(("After tripling","After dividing by 3","Original ticket"),((33,36,39,42),(11,12,13,14),(15,16,17,18))) if n==7 else (("Original ticket","After −4 and ×3","Exit reading"),((15,16,17,18),(33,36,39,42),(35,38,41,44)))
        for j,(lab,vals) in enumerate(zip(labs,arrs)):
            y=185+115*j;a.text(lab,75,y+40,28,BLUE,bold=True,align="left")
            for i,v in enumerate(vals):
                x=398+i*202;a.box(x,y,133,77,fill=PAPER,edge=LINE,radius=9,stroke=2)
                alpha=c.reveal("possible original tickets" if n==7 else "exit readings") if j==2 else 1
                a.text(str(v),x+66,y+40,34,INK,bold=True,opacity=alpha)
        a.text("Every surviving ticket passes the entrance rule." if n==7 else "All four exits fall from 34 through 46.",640,551,32,INK)


def poster(draw):
    return draw(6,1)
