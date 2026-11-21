"""Mirrored odometer drums; the number line changes scale visibly at a carry."""
from fractions import Fraction
from stage import blend, clamp, mix

BACKGROUND=('#282d37','#141c29')
WHITE, AQUA, GOLD, DIM, CASING, RIM = '#f3eedd','#8ad8cf','#ffcc82','#a8b3bf','#19212c','#536375'
BRIDGE='Predict the display after 3993. Watch the gap on the number line when the hundreds wheel carries.'


def check_maths():
    values=[v for v in range(1000,10000) if str(v)==str(v)[::-1]]
    assert len(values)==90 and values==[int(str(i)+str(i)[::-1]) for i in range(10,100)]
    assert [v for v in values if v>3993][0]==4004
    gaps=[b-a for a,b in zip(values,values[1:])]
    assert gaps.count(110)==81 and gaps.count(11)==8
    assert len({Fraction(a+b,2) for a,b in zip(values,values[1:]) if (a+b)%2==0})==81


def drum(a,x,y,old,new,t,col):
    w,h=103,132
    a.box(x-w/2,y-h/2,w,h,radius=11,fill='#27323e',edge=RIM,stroke=3)
    # Clip the moving glyphs to the drum window before putting its rim back on.
    from PIL import Image
    from stage import lettering
    window=Image.new('RGBA',(a.px(w-12),a.px(h-18)))
    for digit,position in ((old,-t),(new,1-t)) if old!=new else ((old,0),):
        glyph=lettering(str(digit),a.px(81),col,True)
        window.alpha_composite(glyph,((window.width-glyph.width)//2,
                               round((window.height-glyph.height)/2 + position*window.height)))
    a.paste(window,a.px(x-(w-12)/2),a.px(y-(h-18)/2))
    a.line([(x-w/2+3,y),(x+w/2-3,y)],'#202933',1)


def display(a,old,new,t,y=293):
    xs=(419,547,733,861)
    a.box(320,y-94,640,188,radius=24,fill=CASING,edge=RIM,stroke=4)
    for i,x in enumerate(xs):
        drum(a,x,y,old[i],new[i],t,AQUA if i<2 else GOLD)
    a.dashed((640,y-81),(640,y+81),GOLD,width=2,dash=10,gap=7)


def gap_line(a,one,two,amount,show,mid=False):
    x1,x2,y=360,920,468
    a.line([(x1,y),(x2,y)],RIM,4,show)
    for x,v in ((x1,one),(x2,two)):
        a.dot(x,y,7,GOLD,show);a.text(str(v),x,y+42,27,WHITE,opacity=show)
    a.text(amount,640,y-37,32,AQUA,opacity=show,bold=True)
    if mid:a.dot((x1+x2)/2,y,8,AQUA,show)


def groups(a,progress,carries,grad=False):
    for row in range(9):
        if row>progress*9:continue
        y=179+row*38
        a.text(str(row+1),174,y,22,DIM)
        for col in range(10):
            x=231+col*52
            a.dot(x,y,6,AQUA)
            if col<9:
                a.line([(x+6,y),(x+46,y)],RIM,2)
                if grad:a.dot(x+26,y,3,GOLD)
        if row<8 and carries>.01:
            a.label('carry',735,y+17,17,GOLD,carries)
    a.label('First digit',107,129,18,DIM)
    a.label('Second digit runs from 0 to 9',229,131,22,AQUA)


def draw(a,n,c):
    titles=['Read the odometer in a mirror','Turn the first pair','What follows 3993?','Cross a carry',
            'How many whole-number midpoints?','Ten displays give nine gaps','Separate even and odd gaps','Test the carry']
    a.label(titles[n-1],78,74,46,WHITE,bold=True)
    if n==1:
        display(a,'3443','3443',0)
        a.label('Choose',417,432,29,AQUA,c.reveal('choose freely'),bold=True)
        a.label('Reflect',723,432,29,GOLD,c.reveal('already determined'),bold=True)
    elif n==2:
        t=c.reveal('advancing the first pair',1.65)
        display(a,'3443','3553',t)
        gap_line(a,3443,3553,'110',c.reveal('a hundred and ten apart'))
    elif n==3:
        display(a,'3993','3993',0)
        a.text('39     →     ?',640,490,38,AQUA,opacity=c.reveal('next palindrome'),bold=True)
    elif n==4:
        t=c.reveal('next possible first pair',1.8)
        display(a,'3993','4004',t)
        gap_line(a,3993,4004,'11',c.reveal('gap is just eleven'))
    elif n==5:
        for j,v in enumerate((1001,1111,1221,1331)):
            x=196+j*277;a.dot(x,299,10,AQUA)
            a.text(str(v),x,353,32,WHITE,bold=True)
            if j<3:
                a.line([(x+10,299),(x+267,299)],RIM,4)
                a.dot(x+138.5,299,7,GOLD,c.reveal('exactly halfway'))
        a.text('1 001  …  9 999',640,470,36,GOLD,opacity=c.reveal('count the gaps'))
    elif n==6:
        layers=c.reveal('nine possible nonzero',1.25)
        groups(a,max(.01,layers),0,c.reveal('whole number')>.1)
        a.label('Each row',847,225,25,DIM);a.label('10 displays',847,270,34,WHITE,bold=True)
        a.label('9 even gaps',847,330,34,GOLD,c.reveal('nine gaps'),bold=True)
        a.label('9 rows',847,435,34,AQUA,layers,bold=True)
    elif n==7:
        groups(a,1,c.reveal('eight carries'),True)
        a.label('9 × 9 = 81',844,226,40,GOLD,bold=True)
        a.label('8 odd gaps',844,334,31,AQUA,c.reveal('eight carries'),bold=True)
        a.label('81 + 8 = 89',844,445,35,WHITE,c.reveal('eighty nine gaps'),bold=True)
    else:
        display(a,'3993','4004',c.reveal('increase the first pair',1.8))
        a.text('Reflect the new pair',640,461,34,AQUA,opacity=c.reveal('reflect it again'),bold=True)
        a.text('A carry changes the size of the gap.',640,535,28,GOLD,opacity=c.reveal('test the change'))


def poster(draw):return draw(4,1.5)
