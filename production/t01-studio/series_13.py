"""Measure area, perimeter and layers with exact geometric models."""

from geometry_marks import dashed, region, right_mark
from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, board, cards, change,
                          chart, cue, equation, exercise, link, note, scene, tile)
from stage import mix
from studio_diagrams import fit


def two_triangles(stage,s):
    shear=cue(s,"same area as a rectangle",duration=1.2)
    copy=cue(s,"fit together",duration=.85)
    x=mix(505,363,shear)
    a,b,c,d=(363,464),(784,464),(x,244),(x+421,244)
    region(stage,(a,b,c),BLUE)
    region(stage,((mix(885,b[0],copy),mix(432,b[1],copy)),d,c),GOLD,opacity=copy)
    q=cue(s,"straight up")
    height=(c[0],a[1])
    dashed(stage,c,height,MINT,q)
    right_mark(stage,height,colour=MINT,opacity=q)


def shared_height(stage,s,show=False):
    left, bottom, unit = 403, 453, 46
    right, high = left + 8 * unit, bottom - 5 * unit
    slide = cue(s, "sliding the top corner", duration=2.6) if show else 0
    tops = ((454,high), (626,high), (886,high))
    height = cue(s,"every one of them has height") if show else 0
    stage.line([(286,high),(1076,high)],RIM,3)
    stage.line([(286,bottom),(1076,bottom)],RIM,3)
    for top, colour in zip(tops, (BLUE,GOLD,MINT)):
        stage.line([(left,bottom),top,(right,bottom)],colour,3,1-slide)
        foot = (top[0],bottom)
        dashed(stage,top,foot,colour,height*(1-slide))
        right_mark(stage,foot,colour=colour,opacity=height*(1-slide))
    if slide:
        tip=(mix(tops[0][0],tops[-1][0],slide),high)
        region(stage,((left,bottom),tip,(right,bottom)),MINT,tint=.18)
        dashed(stage,tip,(tip[0],bottom),MINT)
        right_mark(stage,(tip[0],bottom),colour=MINT)
        stage.dot(*tip,7,MINT)
    fit(stage,"8 cm",(left+right)/2,505,35,400,WHITE)
    if show:
        fit(stage,"5 cm",992,(bottom+high)/2,36,201,WHITE,height)


def outer_triangles(stage,s,cut=False):
    x,y,u=381,473,67
    pt=lambda a,b:(x+a*u,y-b*u)
    stage.box(x,y-4*u,6*u,4*u,edge=BLUE,fill=None,radius=2,stroke=3)
    corners=(pt(0,0),pt(6,3),pt(2,4))
    region(stage,corners,MINT,tint=.21)
    all_parts=((pt(0,0),pt(6,0),pt(6,3)),(pt(0,0),pt(0,4),pt(2,4)),(pt(2,4),pt(6,4),pt(6,3)))
    t=cue(s,"twenty-four minus fifteen",duration=.85) if cut else 0
    q=1 if cut else cue(s,"three right-angled triangles")
    for i,(points,colour,lab,offset) in enumerate(zip(all_parts,(BLUE,GOLD,RED),("9","4","2"),
             ((141,67),(-113,-53),(138,-34)))):
        moved=[(xx+offset[0]*t,yy+offset[1]*t) for xx,yy in points]
        region(stage,moved,colour,opacity=q*(1-.78*t),tint=.25)
        cx=sum(x for x,y in moved)/3
        cy=sum(y for x,y in moved)/3
        fit(stage,lab,cx,cy,33,130,colour,q*(1-t))
    fit(stage,"6 cm",583,515,28,349,BLUE)
    fit(stage,"4 cm",311,337,27,138,BLUE)


def half_rectangle(stage,s):
    left,right,top,bottom=365,912,222,470
    p=cue(s,"wherever the point is",duration=1.1)
    x=mix(462,818,p)
    stage.box(left,top,right-left,bottom-top,edge=BLUE,fill=None,radius=1,stroke=3)
    region(stage,((left,bottom),(right,bottom),(x,top)),MINT,tint=.25)
    stage.dot(x,top,7,MINT)


def cut_shape(stage,s, *, x=431,y=235,u=78,a=5,b=3,mode="corner",mark=None,slide=None,exposed=None):
    right,bottom=x+a*u,y+b*u
    if mode=="uncut":
        region(stage,((x,y),(right,y),(right,bottom),(x,bottom)),BLUE,tint=.16)
        return
    if mode=="corner":
        path=((x+u,y),(right,y),(right,bottom),(x,bottom),(x,y+u),(x+u,y+u))
        old=(((x,y),(x+u,y)),((x,y),(x,y+u)))
        new=(((x+u,y),(x+u,y+u)),((x+u,y+u),(x,y+u)))
    else:
        m=x+2*u
        path=((x,y),(m,y),(m,y+u),(m+u,y+u),(m+u,y),(right,y),(right,bottom),(x,bottom))
        old=(((m,y),(m+u,y)),)
        new=(((m,y),(m,y+u)),((m,y+u),(m+u,y+u)),((m+u,y+u),(m+u,y)))
    region(stage,path,BLUE,tint=.17)
    if not mark:
        return
    p=cue(s,mark)
    for q,r in old:
        dashed(stage,q,r,RED,p)
    for q,r in new:
        stage.line([q,r],MINT,6,cue(s,exposed) if exposed else p)
    if slide:
        t=cue(s,slide,duration=.85)
        for i,(q,r) in enumerate(new):
            offset=(-u*t,0) if i==0 else (0,-u*t)
            stage.line([(q[0]+offset[0],q[1]+offset[1]),(r[0]+offset[0],r[1]+offset[1])],
                       GOLD,5,t)


def scale_plane(stage,s):
    board(2,3,width=69,x=405,y=355,cells=tuple((r,c,BLUE,None) for r in range(2) for c in range(3)))(stage,s)
    if cue(s,"four by six"):
        cells=tuple((r,c,(BLUE,GOLD,MINT,"#c4aae4")[(r//2)*2+(c//3)],"four times as big")
                    for r in range(4) for c in range(6))
        board(4,6,width=62,x=897,y=355,cells=cells)(stage,s)
    fit(stage,"Perimeter 10, area 6",405,513,27,391,BLUE,cue(s,"from ten to twenty"))
    fit(stage,"Perimeter 20, area 24",897,513,27,404,MINT,cue(s,"twenty-four"))


def iso(stage, layers, *, x=640,y=435,u=44,spread=0,paint=False,isolated=False):
    height=len(layers)
    dims=layers[0]
    def point(a,b,c,z):
        extra=spread*(z-(height-1)/2)
        return x+.80*u*(a-b-(dims[0]-dims[1])/2)+extra*.7, y+.42*u*(a+b-sum(dims)/2)-u*c-extra
    for z,(a,b) in enumerate(layers):
        col=(BLUE,GOLD,MINT)[z%3]
        for r in range(b):
            for c in range(a):
                if isolated and (z,r,c)!=(1,1,1):
                    continue
                top=[point(c+i,r+j,z+1,z) for i,j in ((0,0),(1,0),(1,1),(0,1))]
                bot=[point(c+i,r+j,z,z) for i,j in ((0,0),(1,0),(1,1),(0,1))]
                colour=MINT if paint and (z,r,c)==(1,1,1) else GOLD if paint else col
                region(stage,top,colour,tint=.28)
                if r==b-1 or isolated:
                    region(stage,(top[3],top[2],bot[2],bot[3]),colour,tint=.15)
                if c==a-1 or isolated:
                    region(stage,(top[1],top[2],bot[2],bot[1]),colour,tint=.19)


def cube_scale(stage,s):
    for n,x,words in ((1,271,None),(2,631,"eight times"),(3,1004,"twenty-seven times")):
        if cue(s,words)>0:
            iso(stage,[(n,n)]*n,x=x,y=442,u=45)
            fit(stage,f"{n} × {n} × {n} = {n**3}",x,520,30,280,MINT if n>1 else BLUE)


def layers_scene(stage,s,shape,words=None,*,x=653,y=419,u=53):
    p=cue(s,words,duration=1.05) if words else 0
    iso(stage,shape,x=x,y=y,u=u,spread=95*p)


def painted(stage,s):
    p=cue(s,"peel off the outer layer",duration=.95)
    iso(stage,[(3,3)]*3,x=624,y=465,u=43,spread=87*p,paint=True,isolated=p>.89)
    if p>.89:
        fit(stage,"One middle cube touches no outside face",640,560,36,1070,MINT,p)


def both_cut(stage,s):
    cut_shape(stage,s,x=201,y=229,u=61,a=6,b=4,mode="corner")
    cut_shape(stage,s,x=725,y=229,u=61,a=6,b=4,mode="edge")


def measured_notch(stage,s):
    challenge=s.t>=s.at("then find")
    width=2 if challenge else 1
    fit(stage,"Cut a 2 cm by 1 cm notch" if challenge else "Trace the replacement boundary",640,87,43)
    u=66;x,y=335,223
    m=x+(6-width)*u/2;end=m+width*u
    marked=cue(s,"cut from the middle" if challenge else "minus the boundary removed")
    new=cue(s,"long side along the edge" if challenge else "plus the boundary created")
    notch=u*marked
    path=((x,y),(m,y),(m,y+notch),(end,y+notch),(end,y),(x+6*u,y),(x+6*u,y+4*u),(x,y+4*u))
    region(stage,path,BLUE,tint=.15)
    fit(stage,"6 cm",x+3*u,y+4*u+32,30,228,BLUE)
    fit(stage,"4 cm",x-65,y+2*u,30,105,BLUE)
    dashed(stage,(m,y),(end,y),RED,marked)
    for a,b in zip(path[1:4],path[2:5]):
        stage.line([a,b],MINT,5,new)
    fit(stage,f"{width} cm",(m+end)/2,y-30,25,136,RED,marked)
    fit(stage,"1 cm",m-48,y+u/2,21,86,MINT,new)
    fit(stage,"1 cm",end+48,y+u/2,21,86,MINT,new)
    fit(stage,f"{width} cm",(m+end)/2,y+u+29,23,108,MINT,new)
    fit(stage,f"Remove {width} cm",985,278,32,385,RED,marked)
    fit(stage,f"Add 1 + {width} + 1 cm",985,363,32,407,MINT,new)
    fit(stage,f"20 − {width} + {width+2} = 22 cm",640,584,36,1080,WHITE,new)


measured_notch.chapter="Your turn"


def opening_cut(stage,s):
    for x,mode,word in ((201,"corner","from a corner"),(725,"edge","middle of an edge")):
        chosen=mode if s.t>=s.at(word) else "uncut"
        cut_shape(stage,s,x=x,y=229,u=61,a=6,b=4,mode=chosen)


FILMS={
 "T13.1":(
    scene("Two equal triangles give a parallelogram",two_triangles,
          note("Triangle area = half × base × perpendicular height", "half its base",y=559,size=35)),
    scene("The height is perpendicular to the base",
          lambda stage,s:region(stage,((394,486),(903,486),(618,224)),BLUE,tint=.18),
          lambda stage,s:dashed(stage,(618,224),(618,486),MINT,cue(s,"using a slanted side")),
          lambda stage,s:right_mark(stage,(618,486),colour=MINT),
          note("The slanted side is a different length", "using a slanted side")),
    scene("Three triangles share a base and height",shared_height,
          note("Which triangle has the largest area?", "which triangle has the largest",y=568)),
    scene("Sliding the top corner preserves the area",lambda stage,s:shared_height(stage,s,show=True),
          equation(("1/2 × 8 × 5",BLUE,"half of eight"),("= 20 cm²",MINT,"twenty square centimetres"),y=571)),
    scene("Use an enclosing rectangle",outer_triangles,
          note("The whole rectangle has area 6 × 4 = 24", "area twenty-four",y=561)),
    scene("Remove the three outer triangles",lambda stage,s:outer_triangles(stage,s,cut=True),
          equation(("24",BLUE,"twenty-four minus"),("− (9 + 4 + 2)",GOLD,"those three take up fifteen"),
                   ("= 9 cm²",MINT,"leaves nine"),y=575,size=39)),
    scene("A triangle can be half the rectangle",half_rectangle,
          note("Same base and height, wherever the top point goes", "wherever the point is")),
    exercise((("Use perpendicular height","perpendicular height"),("Compare bases and heights","same base and height"),
              ("Subtract simple regions","subtract from a rectangle")),"notebook challenge",
             ("A triangle has base 10 cm and area 35 cm².","What is its height?")),
 ),
 "T13.2":(
    scene("Cuts affect area and perimeter differently",
          change("or even grow",
              (lambda stage,s:cut_shape(stage,s,mode="corner",mark="might stay the same"),),
              (lambda stage,s:cut_shape(stage,s,mode="edge",mark="or even grow"),)),
          note("Compare the old and new boundary", "completely different ways")),
    scene("The same area can have different perimeters",
          board(2,3,width=66,x=397,y=344),board(1,6,width=64,x=888,y=343),
          note("Both have area 6", "mixing them up",x=639,y=488,colour=BLUE),
          note("Perimeters 10 and 14", "mixing them up")),
    scene("Cut a unit square from the corner",lambda stage,s:cut_shape(stage,s),
          note("Original rectangle 5 × 3. What is the new perimeter?", "what is its perimeter now")),
    scene("Two old edges are replaced by two new edges",
          lambda stage,s:cut_shape(stage,s,mark="removes two short pieces",slide="slid out"),
          equation(("16 − 2 + 2",WHITE,"perimeter is still sixteen"),("= 16",MINT,"perimeter is still sixteen"),y=560)),
    scene("An edge notch adds two to the perimeter",
          lambda stage,s:cut_shape(stage,s,mode="edge",mark="one piece of length one"),
          equation(("16 − 1 + 3",WHITE,"three new pieces"),("= 18",MINT,"to eighteen"),y=560)),
    scene("Doubling lengths quadruples the area",scale_plane,
          note("Length × 2, area × 4", "both the length and the width",y=582)),
    scene("Volume scales in three directions",cube_scale,
          note("Volume scales by the cube of the length factor", "twenty-seven times")),
    exercise((("Compare old and new edges","compare the boundary"),("Scale each direction","lengths multiply")),
             "notebook challenge",("Every length of a photograph is tripled.","How many times as large is its area?")),
 ),
 "T13.3":(
    scene("Separate a block into layers",lambda stage,s:layers_scene(stage,s,[(4,3)]*2,"slice the solid"),
          note("Count one layer, then count the layers", "count one layer")),
    scene("Some cubes are hidden",lambda stage,s:layers_scene(stage,s,[(4,3)]*2,"layer by layer"),
          note("Count every cell of each layer","counting layer by layer")),
    scene("Count the unit cubes in the block",lambda stage,s:layers_scene(stage,s,[(4,3)]*2),
          note("4 long, 3 wide, 2 high", "four cubes long",y=545),
          note("How many cubes do the layers hold?", "how many small cubes",y=597,size=31)),
    scene("Two layers of twelve make twenty-four",lambda stage,s:layers_scene(stage,s,[(4,3)]*2,"there are two layers"),
          equation(("4 × 3",BLUE,"four by three"),("× 2",GOLD,"there are two layers"),
                   ("= 24",MINT,"twenty-four cubes"),y=566)),
    scene("Paint reaches only the outside",painted,
          note("How many untouched cubes?", "how many have no paint",x=991,y=311,width=398,size=28)),
    scene("Every cube belongs to one surface class",chart(("Position","Painted faces","Number"),
          [(("Corners","3","8"),"eight corner cubes"),(("Edge middles","2","12"),"twelve cubes"),
           (("Face centres","1","6"),"six in the middle"),(("Interior","0","1"),"one in the centre")],
          y=207,row_height=64,highlight=((0,2),(1,2),(2,2),(3,2))),
          note("8 + 12 + 6 + 1 = 27", "make twenty-seven")),
    scene("Count uneven layers as they are",
          lambda stage,s:layers_scene(stage,s,[(3,3),(2,2),(1,1)],"on the bottom layer",x=478,y=424,u=48),
          note("Top: 1 cube", "one on top", x=915, y=235, width=380, size=32),
          note("Middle: 4 cubes", "four on the next", x=915, y=328, width=380, size=32, colour=GOLD),
          note("Bottom: 9 cubes", "nine cubes", x=915, y=426, width=380, size=32, colour=BLUE),
          note("9 + 4 + 1 = 14", "fourteen altogether", x=915, y=534, width=380, size=40)),
    exercise((("Slice into layers","slice the solid"),("Count the hidden cubes","include the hidden cubes"),
              ("Check the total","add up to the total")),"notebook challenge",
             ("Paint the outside of a 4 × 4 × 4 cube and separate its unit cubes.",
              "How many small cubes have no paint?")),
 ),
 "T13.E":(
    scene("Two equal cuts in different places",opening_cut,
          note("Each original rectangle is 6 cm by 4 cm", "six centimetres by four",y=536,size=33),
          note("Find the two new perimeters", "what are the two new perimeters",y=587,size=33)),
    scene("The original boundary measures twenty",
          lambda stage,s:cut_shape(stage,s,x=408,y=211,u=74,a=6,b=4,mode="uncut"),
          note("6 cm","six plus four",x=630,y=176,size=30),
          note("4 cm","four plus six",x=320,y=359,size=30),
          equation(("6 + 4 + 6 + 4",BLUE,"six plus four"),("= 20 cm",MINT,"twenty centimetres"),y=570)),
    scene("A corner cut gives two edges back",
          lambda stage,s:cut_shape(stage,s,x=408,y=211,u=74,a=6,b=4,mark="removes two",exposed="exposes two new"),
          equation(("20 − 2 + 2",WHITE,"the change is zero"),("= 20 cm",MINT,"still twenty"),y=570)),
    scene("An edge notch gives three edges back",
          lambda stage,s:cut_shape(stage,s,x=408,y=211,u=74,a=6,b=4,mode="edge",mark="removes only one",exposed="exposes three new"),
          equation(("20 − 1 + 3",WHITE,"exposes three"),("= 22 cm",MINT,"twenty-two centimetres"),y=570)),
    scene("Same area removed, different boundary",both_cut,
          note("Each area is 24 − 1 = 23 cm²", "each has area twenty-three",y=533),
          note("The perimeters are 20 cm and 22 cm", "their perimeters differ",y=589,size=33)),
    measured_notch,
 ),
}
