"""Lesson 142. Move the actual equal groups and visibly redefine the whole."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, VIOLET, WHITE, clamp, ease, mix


INKS = (VIOLET, GOLD, AQUA, BLUE)


def groups(art, sizes, x, y, unit, *, inks=None, alpha=1, counts=1, tokens=False):
    """Widths are proportional to the number of pieces, including across different wholes."""
    inks = inks or (VIOLET,)*len(sizes)
    for index,(size,colour) in enumerate(zip(sizes,inks,strict=True)):
        w=unit*size
        art.rounded(x+2,y, w-4,70,12,colour,.34*alpha)
        if tokens and size >= 6:
            columns = (size+2)//3
            for i in range(size):
                xx = x+w*(.12+.76*((i % columns)+.5)/columns)
                yy = y+17+17*(i//columns)
                art.circle((xx,yy),3.1,colour,alpha)
            art.label(size,x+w/2,y+89,28,colour,counts*alpha,bold=True)
        else:
            art.label(size,x+w/2,y+35,29,colour,counts*alpha,bold=True)
        x+=w


def bracket(art, x, y, width, text, colour=SOFT, alpha=1, *, below=False):
    tick=9
    sign = -1 if below else 1
    art.path(((x,y+sign*tick),(x,y),(x+width,y),(x+width,y+sign*tick)),
             colour, 2, alpha)
    art.label(text,x+width/2,y-21*sign,27,colour,alpha,bold=True)


def tokens(art,c,solution=False):
    x,y,u=233,293,33
    a=c.opening() if solution else c.after("twenty-four tokens",1.6)
    split=c.opening() if solution else c.after("one of four equal parts",1.25)
    lift=c.after("remaining three parts",1.25) if solution else c.after("A player takes",1.45)
    return_piece=c.after("adding the removed part back",1.45) if solution else 0
    removed=lift*(1-return_piece)
    count=c.after("One part has six tokens") if solution else 0
    qty=c.says("eighteen tokens") if solution else 0
    for j in range(4):
        for i in range(6):
            appear=ease(a*1.55-(j*6+i)*.023)
            ox=x+j*6*u+i*u+u/2-36*(removed if j==0 else 0)
            oy=y+(1-appear)*22-93*(removed if j==0 else 0)
            fill=GOLD if j==0 and lift else VIOLET
            art.circle((ox,oy),13,fill,appear)
            art.circle((ox-3,oy-4),4,WHITE,.42*appear)
        pos=x+j*6*u
        if j:
            art.dashed((pos,y-26),(pos,y+37),SOFT,2,split)
    bracket(art,x,y+62,24*u,"24 tokens · original whole",VIOLET,a,below=True)
    if solution:
        art.label("24 ÷ 4 = 6",x+3*u,y+166,30,GOLD,count,bold=True)
        bracket(art,x+6*u,y-55,18*u,"3 × 6 = 18 tokens",AQUA,qty*(1-return_piece))
        art.label("18 + 6 = 24",640,550,48,WHITE,c.after("returns twenty-four"),bold=True)
    else:
        art.label("One group is taken",x+2*u,163,28,GOLD,lift,bold=True)
        art.label("How many remain?",705,472,44,WHITE,c.after("How many tokens remain"),bold=True)


def chalk(art,c,solution=False):
    x, y, u = 224, 264, 10.9
    first = c.opening(1) if solution else c.after("seventy-two chalk pieces",1.25)
    split = c.opening(1) if solution else c.after("four equal parts",1.2)
    take = c.after("After the first class",1.18) if solution else c.after("A class uses",1.10)
    carry = c.after("The next whole",1.55) if solution else c.after("what is left",1.5)
    third = c.after("three equal parts",1.35) if solution else c.after("another class uses",1.35)
    second_take = c.after("uses eighteen pieces",1.25) if solution else 0
    count1 = c.says("fifty-four") if solution else 0
    result = c.says("thirty-six") if solution else 0
    art.label("ORIGINAL", x,178,25,VIOLET,first,align="left",bold=True)
    bracket(art,x,y-25,72*u,"72 chalk pieces",VIOLET,first)
    if first and split<1:
        groups(art,(72,),x,y,u,alpha=first*(1-split),counts=0)
    if split:
        groups(art,(18,),x-38*take,y-38*take,u,inks=(GOLD,),alpha=first*split,tokens=True)
        groups(art,(18,18,18),x+18*u,y,u,alpha=first*split*(1-.64*carry),tokens=True)
    if carry:
        art.arrow((942,359),(942,419),AQUA,carry)
        art.label("Only what remains moves down",748,389,27,AQUA,carry)
        remaining_x=mix(x+18*u,x,carry)
        remaining_y=mix(y,482,carry)
        if solution:
            bracket(art, remaining_x,remaining_y-15,54*u,"54 becomes the new whole",AQUA,count1*carry)
        else:
            bracket(art, remaining_x,remaining_y-12,54*u,"New whole",AQUA,carry)
        art.label("54 ÷ 3 = 18",1033,490,32,GOLD,second_take,bold=True)
        if carry > .05:
            strip=mix(0,1,third)
            if strip<1:
                groups(art,(54,),remaining_x,remaining_y,u,inks=(AQUA,),alpha=(1-strip)*carry,counts=0)
            groups(art,(18,),remaining_x-38*second_take,remaining_y+26*second_take,u,inks=(GOLD,),
                   alpha=strip*carry,tokens=True)
            groups(art,(18,18),remaining_x+18*u,remaining_y,u,inks=(AQUA,AQUA),alpha=strip*carry,tokens=True)
        if solution:
            art.label("36 pieces left",1033,546,38,AQUA,result,bold=True)
        else:
            art.label("Split 54 into thirds",1030,554,29,WHITE,c.after("How many pieces remain"),bold=True)
    if take:
        art.label("First use",x+9*u-38*take,y+149-38*take,24,GOLD,take,bold=True)


def route(art,c,scene):
    y=322
    xs=(160,477,805,1122)
    if scene==7:
        events=[c.after("Take one of four"),c.after("Add a gift"),c.after("Then take one"),
                c.says("forty-two pieces left")]
        values=("?", "After the first use", "After the gift", "42")
        effects=("keep ¾", "+ 9", "keep ⅔")
    else:
        events=[c.after("Run the recipe"),c.says("get fifty-four"),c.says("get sixty-three"),
                c.says("leaves forty-two")]
        values=("72","54","63","42")
        effects=("−18  (¼ of 72)","+9","−21  (⅓ of 63)")
    for i,(x,a,text) in enumerate(zip(xs,events,values,strict=True)):
        if not a:
            continue
        art.circle((x,y),67,INKS[i],.13*a)
        art.circle((x,y),7,INKS[i],a)
        art.label(text,x,y+105,34 if len(text)<5 else 25,INKS[i],a,bold=True)
        if i:
            art.arrow((xs[i-1]+77,y),(x-77,y),INKS[i],a)
            art.label(effects[i-1],(x+xs[i-1])/2,y-39,25,INKS[i],a,bold=True)
    if scene==7:
        backwards=c.after("original pile",1.5)
        art.arrow((1116,521),(170,521),WHITE,backwards)
        art.label("Work from the finish back to the start",640,565,33,WHITE,backwards,bold=True)
    else:
        art.label("Each removal uses the whole in front of it",640,541,34,WHITE,c.after("has used its own whole"),bold=True)


def reverse(art,c):
    x,u=201,10.9
    a=c.after("ending forty-two pieces",1.0)
    partition=c.after("two of the last three equal parts")
    one=c.after("Find one part",.8)
    restore=c.after("rebuild that whole",1.3)
    strip=c.after("Undo the gift",1.0)
    second=c.after("remaining fifty-four pieces",1.0)
    early=c.after("three of the original four equal parts",1.1)
    answer=c.after("missing part",1.0)
    y=225
    if a:
        groups(art,(42,),x,y,u,inks=(AQUA,),alpha=a*(1-partition),counts=0)
        groups(art,(21,21),x,y,u,inks=(AQUA,AQUA),alpha=partition,tokens=True,counts=one)
        groups(art,(21,),x+42*u+34*(1-restore),y,u,inks=(GOLD,),alpha=restore,tokens=True)
        bracket(art,x,y-13,mix(42,63,restore)*u,"Rebuilt whole = 63" if restore>.8 else "42 pieces remain",AQUA,a)
        art.label("42 ÷ 2 = 21",1088,235,35,WHITE,one,bold=True)
        art.label("21 × 3 = 63",1088,292,31,GOLD,restore,bold=True)
    if strip:
        # The gift is nine of the 63 pieces, regardless of where the previous thirds were drawn.
        y=381
        art.arrow((x-39,304),(x-39,y+15),SOFT,strip)
        groups(art,(54,),x,y,u,alpha=strip*(1-early),counts=0)
        groups(art,(9,),x+54*u+83*strip,y-10*strip,u,inks=(GOLD,),alpha=strip*(1-.7*early))
        groups(art,(18,18,18),x,y,u,inks=(VIOLET,VIOLET,VIOLET),alpha=early,tokens=True)
        bracket(art,x,y-15,54*u,"Undo +9  →  54",VIOLET,second)
        art.label("63 − 9 = 54",1088,411,34,GOLD,strip,bold=True)
    if early:
        y=532
        art.arrow((x-39,451),(x-39,y+15),SOFT,early)
        groups(art,(18,18,18),x,y,u,inks=(VIOLET,VIOLET,VIOLET),alpha=early)
        groups(art,(18,),x+54*u+34*(1-answer),y,u,inks=(AQUA,),alpha=answer)
        bracket(art,x,y-12,72*u,"Original whole = 72",AQUA,answer)
        art.label("54 ÷ 3 = 18",1088,529,30,VIOLET,early,bold=True)
        art.label("18 × 4 = 72",1088,581,37,AQUA,c.says("seventy-two"),bold=True)


def opening(art,c,exam=False):
    a=c.after("fraction of the original pile") if exam else c.after("particular whole")
    b=c.after("fraction of what is left") if exam else c.after("whole changes",1.6)
    arrows=c.after("Reverse one change at a time") if exam else c.after("mark which amount becomes the whole")
    x,y,u=259,234,65
    groups(art,(1,1,1,1),x,y,u,alpha=a,counts=0)
    groups(art,(1,),x,y,u,inks=(GOLD,),alpha=a*.96,counts=0)
    bracket(art,x,y-20,4*u,"original whole" if not exam else "¼ of the original pile",VIOLET,a)
    groups(art,(1,1,1),x+u+mix(0,-u,b),y+154*b,u,inks=(AQUA,AQUA,AQUA),
           alpha=b,counts=0)
    bracket(art,x,y+234,3*u,"what is left" if not exam else "⅓ of what is left",AQUA,b,below=True)
    art.arrow((677,245),(677,427),AQUA,b)
    for i in range(3):
        art.label(("Original", "Remainder", "New whole")[i],955,232+92*i,36,INKS[i],
                  clamp((a,b,arrows)[i]),bold=True)
    if exam:
        art.arrow((1115,543),(786,543),WHITE,arrows)
        art.label("Reverse changes one at a time",953,583,26,WHITE,arrows)


def mistakes(art,c,recap=False):
    if recap:
        a=c.after("Write the word original")
        b=c.after("Draw equal parts")
        q=c.after("rebuild the last whole first")
        r=c.after("reverse any addition")
        art.label("1. Name the whole",364,266,38,VIOLET,a,bold=True)
        groups(art,(18,18,18,18),711,230,5.4,alpha=b,counts=0)
        art.label("2. Show equal parts",364,390,38,AQUA,b,bold=True)
        groups(art,(18,18,18),711,356,5.4,inks=(AQUA,AQUA,AQUA),alpha=b,counts=0)
        art.label("3. Rebuild backwards",364,526,38,GOLD,q,bold=True)
        art.arrow((1084,524),(714,524),GOLD,r)
    else:
        same=c.after("same original whole")
        new=c.after("uses a new whole")
        backwards=c.after("number of remaining parts")
        base=c.after("denominator names")
        art.label("¼ of 72",369,236,36,VIOLET,same,bold=True)
        art.label("⅓ of 54",919,236,36,AQUA,new,bold=True)
        groups(art,(18,18,18,18),152,289,6,inks=(GOLD,VIOLET,VIOLET,VIOLET),alpha=same)
        groups(art,(18,18,18),757,289,6,inks=(GOLD,AQUA,AQUA),alpha=new)
        art.label("Different wholes",640,390,31,WHITE,new,bold=True)
        art.label("42 known pieces ÷ 2 known parts = 21 each",640,482,33,AQUA,backwards,bold=True)
        art.label("3 is the total number of parts in the reconstructed whole",640,566,27,GOLD,base)


TITLES={
    1:("What is the whole?",None),
    2:("Read the words after ‘of’","AMC Upper Primary  ·  Rossmoyne-style reasoning"),
    3:("One quarter of 24 tokens",None),
    4:("Count the three remaining groups",None),
    5:("The second class has a new whole",None),
    6:("Follow the chalk that stays",None),
    7:("Start from the finish",None),
    8:("Rebuild one whole at a time",None),
    9:("Check the story forwards",None),
    10:("Which whole does each fraction use?",None),
    11:("Name it, split it, rebuild it",None),
}


def draw(art,c,scene):
    title, subtitle=TITLES[scene]
    art.heading(title,GOLD,subtitle)
    if scene in (1,2):
        opening(art,c,scene==2)
    elif scene in (3,4):
        tokens(art,c,scene==4)
    elif scene in (5,6):
        chalk(art,c,scene==6)
    elif scene in (7,9):
        route(art,c,scene)
    elif scene==8:
        reverse(art,c)
    else:
        mistakes(art,c,scene==11)
