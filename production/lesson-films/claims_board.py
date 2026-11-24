"""A club noticeboard links speakers' claims to the truth values they force."""
from itertools import product

BACKGROUND = ("#f2e1c4","#e8cc9f")
INK, BLUE, RED, GREEN, PAPER = "#362a23", "#2d5c76", "#8d372f", "#276c52", "#fff9e9"
BRIDGE = "Try both badges on Ava’s first message. During the separate four-speaker puzzle, trace the chain from Ava to Dara before uncovering anyone’s badge."
HEAD = ("Test a self-description","Try both columns","Link two badges","The connecting line","Four new claims","Leave the badges covered","Uncover Dara","Check all four sentences")


def check_maths():
    assert not any(speaker==(not speaker) for speaker in (False,True))
    valid=[(a,b,c,d) for a,b,c,d in product((False,True),repeat=4)
           if a==(not b) and b==c and c==d and d==(a!=d)]
    assert valid==[(False,True,True,True)]


def note(a,x,y,w,person,statement):
    a.box(x,y,w,111,radius=6,fill=PAPER,edge="#7b644a",stroke=3)
    a.dot(x+w*.5,y+7,6,RED)
    a.text(person,x+22,y+33,29,BLUE,bold=True,align="left")
    a.text(statement,x+22,y+78,29,INK,align="left")


def badge(a,x,y,person,value,alpha=1):
    colour=GREEN if value=="Truth" else RED if value=="Lie" else BLUE
    a.box(x,y,196,114,radius=16,fill=PAPER,edge=colour,stroke=4)
    a.text(person,x+98,y+34,27,INK,bold=True)
    a.text(value,x+98,y+81,32,colour,bold=True,opacity=alpha)


def draw(a,n,c):
    a.text(HEAD[n-1],61,75,46,INK,bold=True,align="left")
    a.line([(61,125),(1216,125)],"#876e54",3)
    if n in (1,2):
        note(a,408,170,464,"Ava","“I am a liar.”")
        for x,v,reason in ((166,"Truth","Her sentence would be false."),(782,"Lie","Her sentence would be true.")):
            badge(a,x+74,333,"Try this badge",v)
            if n==2:
                a.text(reason,x+170,488,26,INK,opacity=c.reveal("would be false" if v=="Truth" else "would be true"))
        if n==2:a.text("Neither badge fits",640,554,34,RED,bold=True,opacity=c.reveal("Both badges fail"))
    elif n in (3,4):
        note(a,355,168,570,"Ben","“Chen tells the truth.”")
        badge(a,245,345,"Ben","?");badge(a,839,345,"Chen","?")
        if n==4:
            a.line([(448,400),(833,400)],GREEN,6)
            a.text("match",640,359,32,GREEN,bold=True,opacity=c.reveal("badges match"))
            a.text("Truth with truth      •      Lie with lie",640,535,33,INK,opacity=c.reveal("badges match"))
    elif n==5:
        for x,y,name,words in ((78,177,"Ava","“Ben lies.”"),(657,177,"Ben","“Chen tells the truth.”"),(78,355,"Chen","“Dara tells the truth.”"),(657,355,"Dara","“Ava and I have different types.”")):
            note(a,x,y,545,name,words)
    else:
        for i,(name,value) in enumerate(zip(("Ava","Ben","Chen","Dara"),("Lie","Truth","Truth","Truth"))):
            reveal=c.reveal("Dara tells the truth") if n==7 else 1
            badge(a,70+311*i,238,name,"?" if n==6 else value,reveal)
        for i,(label,col) in enumerate((("different",RED),("same",GREEN),("same",GREEN))):
            x=273+i*311
            a.line([(x,296),(x+101,296)],col,4)
            a.text(label,x+51,327,17,col,bold=True)
        if n==6:a.text("Ava and Dara must differ",640,486,40,RED,bold=True,opacity=c.reveal("opposite badge"))
        elif n==7:a.text("Dara’s statement is true",640,486,40,GREEN,bold=True,opacity=c.reveal("this is true"))
        else:a.text("Ava’s sentence fails. The other three fit.",640,486,38,INK,bold=True)


def poster(draw):
    return draw(8,1)
