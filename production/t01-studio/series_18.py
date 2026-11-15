"""Choose a productive restriction, keep a record and check the answer."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, board, cards, chart, cue,
                          equation, exercise, link, move, note, scene, tile)
from stage import mix
from studio_diagrams import fit


SQUARES=(16,25,36,49,64,81)
OPTIONS=(54,64,72,81,90)
BORDER=tuple((r,c) for r in range(5) for c in range(5) if r in (0,4) or c in (0,4))
STRIPS=(tuple((0,c) for c in range(4)),tuple((r,4) for r in range(4)),
        tuple((4,c) for c in range(1,5)),tuple((r,0) for r in range(1,5)))
PALETTE=(BLUE,GOLD,MINT,"#c4abe7")


def short_list(stage,s):
    p=cue(s,"one of them usually cuts",duration=.98)
    for i in range(12):
        x=365+(i%6)*111
        y=234+100*(i//6)
        tile(stage,mix(x,640+(i-1.5)*141,p) if i<4 else x,mix(y,397,p),str(i+1),
             MINT if i<4 else MUTED,83,51,1 if i<4 else 1-p,27)


def square_check(stage,s):
    p=cue(s,"only sixty-four")
    for i,n in enumerate(SQUARES):
        x=276+i*145
        tile(stage,x,310,n,MINT if n==64 and p>.5 else BLUE,109,69,size=36)
        value=sum(map(int,str(n)))
        fit(stage,str(value),x,416,31,120,MINT if value==10 and p>.5 else GOLD,
            cue(s,"add the digits",delay=.14*i))
    fit(stage,"Digit sum",159,415,25,151,WHITE,cue(s,"add the digits"))


def lifted_middle(stage,s):
    w=68
    x=517
    y=342
    p=cue(s,"take away the inside",duration=1.13)
    board(5,5,width=w,x=x,y=y,cells=tuple((r,c,BLUE,None) for r,c in BORDER))(stage,s)
    for r in range(3):
        for c in range(3):
            cx=x+(c-1)*w+385*p
            cy=y+(r-1)*w+21*p
            stage.box(cx-w/2+1,cy-w/2+1,w-2,w-2,radius=2,fill="#574839",edge=GOLD,opacity=1,stroke=2)
    fit(stage,"3 × 3 inside",897,504,29,302,GOLD,cue(s,"nine squares"))


def choice_row(stage,s,mode):
    for i,n in enumerate(OPTIONS):
        x=286+177*i
        win=n==72
        if mode=="question":
            opacity=cue(s,"fifty-four",delay=.13*i)
        elif mode=="four":
            remove={81:"eighty-one goes",54:"half of fifty-four",90:"the same happens"}
            opacity=1-.78*cue(s,remove[n]) if n in remove else 1
        else:
            opacity=1 if win or n==64 else .20
            if n==64:
                opacity=1-.78*cue(s,"sixty-four gives ten")
        colour=MINT if win and mode=="nine" else BLUE
        tile(stage,x,344,str(n),colour,121,77,opacity,43)
        fit(stage,chr(65+i),x,257,29,123,WHITE,opacity)
        if mode=="four" and n not in (81,):
            fit(stage,f"Half: {n//2}",x,456,28,165,MINT if n in (64,72) else RED,cue(s,"half of fifty-four"))
        if mode=="nine" and n in (64,72):
            fit(stage,f"Digit sum {sum(map(int,str(n)))}",x,446,27,172,MINT if win else RED,
                cue(s,"add the digits"))


FILMS={
 "T18.1":(
    scene("A strong condition makes the search smaller",short_list,
          note("Start with the clue that narrows the possibilities", "start with that one")),
    scene("Choose where to begin",
          cards((("Many candidates",BLUE),("A short list",MINT)),340,width=305,gap=434,
                words="starting with a weak condition"),
          note("Save the broad checks for the short list", "the strongest can leave")),
    scene("Find a two-digit square with digit sum ten",
          cards((("Two-digit",BLUE),("Square",GOLD),("Digit sum 10",MINT)),336,
                width=249,gap=283,words="perfect square"),
          note("Which clue gives the shorter list?", "which clue to use first")),
    scene("The square clue allows fewer candidates",
          cards(tuple(str(10*a+10-a) for a in range(1,10)),247,width=88,gap=108,
                words="allows nine numbers",size=28),
          cards(tuple(map(str,SQUARES)),402,width=108,gap=142,face=GOLD,
                words="allows only six",size=33),
          note("Begin with the six two-digit squares", "start with the squares")),
    scene("Check the digit sums of the six squares",square_check,
          note("64 is the only one whose digits add to 10", "only sixty-four")),
    scene("Area gives a short list of factor pairs",
          chart(("Whole-number sides","Area","Perimeter"),
                [(("1 × 24","24","50"),"one by twenty-four"),(("2 × 12","24","28"),"two by twelve"),
                 (("3 × 8","24","22"),"three by eight"),(("4 × 6","24","20"),"four by six")],
                 y=205,row_height=73,highlight=((3,2),)),
          note("Only 4 by 6 fits both conditions", "it is four by six",y=568)),
    scene("A clue suggests a tool to try",
          chart(("Feature","Tool"),
                [(("Product","Factor pairs"),"a product suggests"),(("Fixed sum","Equal parts"),"a fixed total"),
                 (("Repeating process","A cycle"),"a repeating process"),(("Order","A line"),"an order suggests")],
                 y=205,row_height=72)),
    exercise((("List the conditions","list the conditions"),("Start with the tightest","start with the one"),
              ("Check the other clues","use the rest")),"notebook challenge",
             ("Find the odd multiples of 13 between 50 and 100.",)),
 ),
 "T18.2":(
    scene("Leave a trail you can return to",
          cards((("What is known",BLUE),("Cases done",GOLD),("What comes next",MINT)),336,
                width=278,gap=311,words="write what you have established",size=29),
          note("A clear record makes errors easier to find", "find a mistake")),
    scene("Keep your place and check independently",
          cards((("Record the stopping point",BLUE),("Check a different way",MINT)),335,width=417,gap=463,
                words="keep a clear trail",size=30),
          note("Use a separate method to catch errors", "independent check")),
    scene("How many border squares are shaded?",
          board(5,5,width=69,y=352,cells=tuple((r,c,BLUE,"border shaded") for r,c in BORDER)),
          note("Try to count them two different ways", "then in a second")),
    scene("Subtract the inside from the whole grid",lifted_middle,
          equation(("25",BLUE,"twenty-five squares"),("− 9",GOLD,"nine squares"),("= 16",MINT,"is sixteen"),
                   y=570)),
    scene("Split the border into four non-overlapping strips",
          board(5,5,width=68,y=354,cells=tuple((r,c,PALETTE[i],"four strips") for i,row in enumerate(STRIPS) for r,c in row)),
          equation(("4 × 4",BLUE,"four times four"),("= 16",MINT,"is sixteen"),y=565)),
    scene("A full-side count repeats every corner",
          board(5,5,width=68,y=348,cells=tuple((r,c,BLUE if (r+c)%4 else GOLD,"four sides of five") for r,c in BORDER),
                marks=tuple((r,c,"2",RED,"each corner twice") for r,c in ((0,0),(0,4),(4,0),(4,4)))),
          equation(("20 − 4",BLUE,"subtract the four"),("= 16",MINT,"get sixteen"),y=565)),
    scene("Label completed cases and the next action",
          chart(("Item","Record"),
                [(("Known","All border squares"),"label your cases"),
                 (("Finished","Outside minus inside"),"when it is finished"),
                 (("Next","Check by four strips"),"write one line")],
                y=220,row_height=83)),
    exercise((("Record the next step","record what you know"),("Mark finished cases","tick off finished"),
              ("Check a new way","check the answer")),"notebook challenge",
             ("Count the border squares in a 7 × 7 grid.","Show two different methods.")),
 ),
 "T18.3":(
    scene("The answer options give useful tests",
          cards(("A","B","C","D","E"),336,width=119,gap=168,words="the options are information"),
          note("Test each remaining choice against the whole question", "checked against the question")),
    scene("An intermediate result can look like an answer",
          cards((("Working result",GOLD),("Requested result",MINT)),329,width=353,gap=421,
                words="a step along the way"),
          note("Read the final question again", "rereading what was asked")),
    scene("Find a multiple of both four and nine",lambda stage,s:choice_row(stage,s,"question"),
          note("Which test quickly rules out an option?", "quickest way to rule options out")),
    scene("A multiple of four still has an even half",lambda stage,s:choice_row(stage,s,"four"),
          note("Only 64 and 72 pass the test for 4", "that leaves")),
    scene("Now apply the digit-sum test for nine",lambda stage,s:choice_row(stage,s,"nine"),
          note("72 is the only choice that passes both tests", "option c")),
    scene("Answer the quantity the question asks for",
          chart(("What it is","Cost"),
                [(("Book","$12"),"a book costs twelve"),(("One pen","$9"),"one pen costs nine"),
                 (("Two pens","$18"),"asks for two pens")],
                 y=219,row_height=73,highlight=((2,1),)),
          note("The request is for two pens", "always reread the request")),
    scene("A trial can tell you which direction to try",
          chart(("Choice for x","2x + 5","Target"),
                [(("6","17","19"),"try six"),(("7","19","19"),"try seven")],
                y=223,row_height=94,highlight=((1,1),(1,2))),
          note("Check how the expression changes as x grows", "check how the expression changes")),
    exercise((("Try quick tests","rule options out"),("Check the quantity","do not choose a number"),
              ("Reread the request","reread what was asked")),"notebook challenge",
             ("Which of 45, 60, 75 and 90 is a multiple of both 4 and 5?",)),
 ),
 "T18.E":(
    scene("Choose two different numbers from one to six",
          cards(tuple(str(i) for i in range(1,7)),333,width=105,gap=139,words="one two three"),
          note("Order does not matter", "the order does not matter",y=459,colour=BLUE),
          note("How many pairs sum to at least 9?", "a sum of at least nine")),
    scene("Give every pair one larger number",
          cards((("Larger is 6",BLUE),("Larger is 5",GOLD),("Larger is 4",MINT)),337,
                width=249,gap=282,words="organise the count",size=33),
          note("Writing the larger number first prevents repeats", "always name the larger")),
    scene("Count each possible larger number",
          chart(("Larger number","Possible smaller numbers","Pairs"),
                [(("6","3, 4, 5","3"),"if the larger number is six"),
                 (("5","4","1"),"if the larger number is five"),
                 (("4 or less","None","0"),"if the larger is four")],
                 y=223,row_height=78,highlight=((0,2),(1,2),(2,2))),
          note("Even the largest pair with 4 adds to only 7", "which is only seven",y=562,size=34)),
    scene("List the four qualifying pairs",
          cards(("3 and 6","4 and 6","5 and 6","4 and 5"),335,width=179,gap=214,words="the pairs are"),
          equation(("3 + 1",BLUE,"three plus one"),("= 4 pairs",MINT,"is four"))),
    scene("Check by sorting the pairs by their sum",
          chart(("Sum","Pairs","Count"),
                [(("9","3 + 6 and 4 + 5","2"),"nine comes"),
                 (("10","4 + 6","1"),"ten comes"),(("11","5 + 6","1"),"eleven comes")],
                 y=221,row_height=77,highlight=((0,2),(1,2),(2,2))),
          equation(("2 + 1 + 1",BLUE,"two plus one plus one"),("= 4",MINT,"is four"),y=565)),
    exercise((("Fix an order","fix an order"),("Sort into cases","sort into cases"),
              ("Check a second way","then check another")),"then count",
             ("Choose two different numbers from 1 to 6.","How many pairs have sum at most five?")),
 ),
}
