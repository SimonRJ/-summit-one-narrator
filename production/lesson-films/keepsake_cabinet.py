"""Two explicit rejected cabinet cases followed by an exhaustive uniqueness check."""
from itertools import permutations
BACKGROUND=('#423a32','#292d31')
PAPER,WOOD,INK,GOLD,MINT,RED,LINE='#fff0d4','#d6b991','#303537','#f2ca80','#b3dac2','#f1a293','#8c806e'
HEAD=('Read down the cabinet','Hang the three clues','Start with just two cases','Test the spaces left behind','Move the shell to the bottom','Fit the two-drawer pair','Separate existence from uniqueness','Loosen one word')
BRIDGE='Try the shell in drawer 2 and move the moon as far away as the clues require. Which two drawers are left, and why do those two spaces settle the case?'
NAMES=('Moon','Leaf','Star','Shell')
def check_maths():
    def valid(row,ordered):
        s=row.index('Shell');m=row.index('Moon');d=row.index('Star')-row.index('Leaf')
        return (s+1)%2==0 and abs(s-m)>1 and (d==1 if ordered else abs(d)==1)
    ordinary=[r for r in permutations(NAMES) if valid(r,True)]
    loose=[r for r in permutations(NAMES) if valid(r,False)]
    assert ordinary==[NAMES] and set(loose)=={NAMES,('Moon','Star','Leaf','Shell')}
def txt(a,s,x,y,size=34,k=PAPER,t=1):a.text(str(s),x,y,size,k,bold=True,opacity=t)
def cabinet(a,x,y,labels,marks=(),col=WOOD):
    a.box(x-15,y-14,234,341,fill='#574a40',edge=LINE,stroke=3,radius=9)
    hues={'Moon':'#efd68b','Leaf':'#a9d6a7','Star':'#acd5e2','Shell':'#e9b3a4'}
    for i,s in enumerate(labels):
        yy=y+80*i;colour=hues.get(s,col)
        a.box(x,yy,204,71,fill=colour,edge='#564d40',radius=4)
        txt(a,str(i+1),x+21,yy+35,24,INK);txt(a,s or '—',x+117,yy+34,30,INK)
        if i+1 in marks:
            a.line([(x+169,yy+10),(x+187,yy+25)],'#8b463e',4)
            a.line([(x+187,yy+10),(x+169,yy+25)],'#8b463e',4)
def draw(a,n,c):
    a.label(HEAD[n-1],65,69,43,PAPER,bold=True);a.line([(65,124),(1214,124)],LINE,3)
    if n==1:
        cabinet(a,260,199,['','Here','','']);txt(a,'Immediately below drawer 2',882,287,33,MINT,c.reveal('drawer two'))
        txt(a,'Drawer 3',885,389,46,GOLD,c.reveal('below is three'))
    elif n==2:
        cabinet(a,232,200,['']*4)
        for i,(s,cue) in enumerate([('Shell: drawer 2 or 4','even numbered drawer'),('Star: immediately below leaf','immediately below'),('Moon: never next to shell','never next')]):
            txt(a,s,884,253+i*99,31,PAPER,c.reveal(cue))
    elif n in (3,4):
        ls=['','Shell','','Moon' if n==4 or c.reveal('drawer four')>.2 else '']
        cabinet(a,265,203,ls,(1,3))
        if n==3:
            txt(a,'Shell in drawer 2',865,262,38,GOLD)
            txt(a,'Moon cannot go in 1 or 3.',867,357,30,RED,c.reveal('cannot use either'))
            txt(a,'Only drawer 4 is left for moon.',867,455,30,MINT,c.reveal('occupy drawer four'))
        else:
            txt(a,'Leaf and star need to touch.',877,294,31,MINT,c.reveal('remain for the leaf'))
            txt(a,'1 and 3 are separated.',872,404,38,RED,c.reveal('do not touch'))
    elif n==5:
        cabinet(a,198,203,['Moon','','','Shell'])
        cabinet(a,854,203,['','Moon','','Shell'])
        txt(a,'Try both positions for the moon.',640,558,35,GOLD,c.reveal('each choice'))
    elif n==6:
        ls=['Moon','','','Shell']
        if c.reveal('leaf must be in two')>.1:ls[1]='Leaf'
        if c.reveal('star directly below')>.1:ls[2]='Star'
        cabinet(a,284,202,ls)
        txt(a,'Moon in drawer 1',865,294,38,GOLD,c.reveal('moon is in drawer one'))
        txt(a,'The pair fits drawers 2 and 3.',865,408,30,MINT,c.reveal('Only drawers two and three'))
    elif n==7:
        cabinet(a,276,202,list(NAMES))
        for j,(s,cue) in enumerate([('Shell is in even drawer 4.','even drawer four'),('Star is immediately below leaf.','immediately below'),('Moon and shell are apart.','far apart')]):
            txt(a,s,875,254+92*j,30,MINT,c.reveal(cue))
    else:
        cabinet(a,211,203,list(NAMES))
        cabinet(a,839,203,['Moon','Star','Leaf','Shell'] if c.reveal('switch places')>.1 else ['Moon','','','Shell'])
        txt(a,'The same pair of drawers, two internal orders.',640,557,33,GOLD,c.reveal('Two cabinets fit'))
def poster(draw):return draw(9,1)
