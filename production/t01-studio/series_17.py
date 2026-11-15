"""Make proof, counterexamples and complete case checks visible."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, board, cards, chart, cue,
                          equation, exercise, link, move, note, scene, tile)
from stage import mix
from studio_diagrams import bead, fit


def odd_pairing(stage,s, join=False):
    p=cue(s,"their two leftover counters",duration=.95) if join else 0
    for center,n,colour in ((390,2,BLUE),(866,3,GOLD)):
        for i in range(n):
            x=center+84*(i-(n-1)/2)
            stage.box(x-35,265,70,117,fill=None,edge=colour,radius=12)
            for y in (297,352):
                bead(stage,x,y,colour,1,18)
        x=mix(center,601 if center<640 else 678,p)
        bead(stage,x,mix(453,415,p),MINT,1,22)
    stage.box(557,378,166,74,fill=None,edge=MINT,radius=10,opacity=p)
    fit(stage,"One extra pair" if join else "One leftover in each group",640,528,37,1080,MINT,p if join else 1)


def coin_flips(stage,s):
    p=cue(s,"each move flips exactly two",duration=1.1)
    for i in range(9):
        x=256+96*i
        colour=GOLD if i<2 and p>.52 else BLUE
        bead(stage,x,337,colour,1,33)
        fit(stage,"T" if i<2 and p>.52 else "H",x,337,31,75,WHITE)
    fit(stage,"Head count can change by −2, 0 or +2",640,473,34,1090,GOLD,cue(s,"the number of heads by two"))
    fit(stage,"The head count stays odd",640,556,40,1090,MINT,cue(s,"stays odd"))


def stamps(stage,s):
    good={3:"3",5:"5",6:"3+3",8:"3+5",9:"3+3+3",10:"5+5",11:"5+3+3",12:"3+3+3+3"}
    for n in range(1,13):
        r,c=divmod(n-1,6)
        x,y=262+151*c,272+141*r
        allowed=n in good
        colour=MINT if allowed else RED
        p=cue(s,"three and five work",delay=.13*(n-1))
        tile(stage,x,y,n,colour,112,63,p)
        fit(stage,good.get(n,"No"),x,y+55,23,143,colour,p)


def add_stamps(stage,s):
    rows=((8,9,10),(11,12,13),(14,15,16))
    words=("eight nine and ten","eleven twelve and thirteen","fourteen fifteen and sixteen")
    for r,values in enumerate(rows):
        for c,n in enumerate(values):
            x,y=380+260*c,209+162*r
            p=cue(s,words[r],delay=.13*c)
            tile(stage,x,y,n,(BLUE,GOLD,MINT)[c],108,63,p)
            if r:
                stage.arrow((x,y-127),(x,y-40),(BLUE,GOLD,MINT)[c],p)
                fit(stage,"+3",x+64,y-83,28,105,(BLUE,GOLD,MINT)[c],p)


def directed_case(first_even):
    n,m=(4,5) if first_even else (5,6)
    rows,cols=m,n
    colours=tuple((r,c,BLUE if (c<n/2 if first_even else r<m/2) else GOLD,
                   "two lots of something") for r in range(rows) for c in range(cols))
    return board(rows,cols,width=52,x=640,y=356,cells=colours,
                 marks=tuple((r,c,"•",WHITE,None) for r in range(rows) for c in range(cols)))


FILMS={
 "T17.1":(
    scene("The claim determines what counts as proof",
          cards((("Can happen",BLUE),("Always happens",GOLD),("Never happens",MINT)),332,
                width=270,gap=302,words="different claims",size=32),
          note("For always or never, cover every case", "must cover every case")),
    scene("A pattern may fail at a later case",
          cards(("Yes","Yes","Yes","…",("No",RED)),339,width=133,gap=168,words="patterns can hold"),
          note("Find out what the claim requires you to prove", "what a claim actually requires")),
    scene("Do three examples prove an always claim?",
          chart(("First odd","Second odd","Sum"),
                [(("3","5","8"),"three and five"),(("7","9","16"),"seven and nine"),
                 (("11","1","12"),"eleven and one")],
                y=205,row_height=75,highlight=((0,2),(1,2),(2,2))),
          note("The claim covers every pair of odd numbers", "is that a proof")),
    scene("An odd number has one left over",odd_pairing,
          note("The number of original pairs can be anything","any odd number",y=591,size=30)),
    scene("The two leftovers form a pair",lambda stage,s:odd_pairing(stage,s,join=True),
          note("Everything is now in pairs", "the total is even",y=591,size=31)),
    scene("One counterexample disproves an always claim",
          board(3,3,width=70,x=640,y=338,
                marks=tuple((r,c,"•",GOLD,"nine is three times three") for r in range(3) for c in range(3))),
          note("9 is odd and equals 3 × 3", "nine is three times three")),
    scene("A condition can be needed without being enough",
          cards((("Multiples of 6 are even",BLUE),("14 is even",GOLD)),339,
                width=406,gap=453,words="every multiple of six",size=30),
          note("Evenness alone does not guarantee divisibility by 6", "being even is not enough",size=33)),
    exercise((("Can happen: show one","one example shows"),("Always: cover every case","a reason covering"),
              ("False: find a counterexample","one counterexample")),"notebook challenge",
             ("Is the sum of three odd numbers always odd?", "Give a reason that covers every case.")),
 ),
 "T17.2":(
    scene("Test a claim with a counterexample or contradiction",
          cards((("One case breaks the claim",BLUE),("An assumption fails",GOLD)),328,
                width=426,gap=480,words="one case that breaks",size=30),
          note("Follow the consequences of the supposition", "follows what it would imply")),
    scene("Decide what would prove a possibility",
          cards((("Possible: build one",BLUE),("Impossible: give a reason",MINT)),
                340,width=414,gap=470,words="if it is",size=32),
          note("A contradiction can prove that a case is impossible", "contradiction is the standard")),
    scene("Does multiplying always make a number bigger?",
          cards((("5",BLUE),("× 3",GOLD),("15",MINT)),338,width=139,gap=166,words="five times three"),
          note("Find one allowed case that breaks the claim", "a case that breaks it")),
    scene("Any one of these three cases breaks the claim",
          chart(("Product","Result","Compared with 6"),
                [(("6 × 1/2","3","Smaller"),"six times one half"),(("6 × 1","6","Equal"),"six times one is"),
                 (("6 × 0","0","Smaller"),"six times zero")],
                 y=223,row_height=78,highlight=((0,2),(1,2),(2,2))),
          note("One counterexample is enough", "any one of these")),
    scene("State the conditions of the claim precisely",
          cards((("Positive number",BLUE),("Multiplier greater than 1",MINT)),341,width=420,gap=471,
                words="multiplying a positive number",size=29),
          note("Check that every counterexample is allowed by the conditions", "must obey",y=554,size=33)),
    scene("Flip exactly two of nine coins",coin_flips),
    scene("An odd head count can never become zero",
          cards((("1",BLUE),"3","5","7","9"),335,width=106,gap=143,words="it starts at nine"),
          cards((("0",RED),),335,x=1073,width=101,words="zero heads"),
          note("All tails would have an even head count", "which is even",y=467,colour=GOLD),
          note("The odd count makes the goal impossible", "the task cannot be done")),
    exercise((("Find a legal counterexample","one allowed case"),("Follow the assumption","supposes something")),
             "notebook challenge",("Seven cups start upright. Each move flips exactly two.",
                                   "Can all seven end upside down?")),
 ),
 "T17.3":(
    scene("A complete check covers every case",
          cards(("Case 1","Case 2","Case 3","Case 4"),329,width=189,gap=216,words="check them all",size=29),
          note("For an infinite sequence, pass the result along", "passes the result along")),
    scene("Make sure nothing falls between your cases",
          cards((("1",BLUE),("2",BLUE),("?",RED),("4",BLUE)),331,width=126,gap=174,words="a missing case",size=43),
          note("Explain how your cases cover all possibilities", "cases cover everything")),
    scene("Which stamp totals can you make?",
          cards((("3 cents",BLUE),("5 cents",GOLD)),343,width=254,gap=339,words="three-cent and five-cent"),
          note("Try each total from 1 to 12", "test the totals")),
    scene("Check the first twelve totals",stamps,
          note("Each green total has a construction", "four threes",y=574)),
    scene("Add three to carry a whole block forward",add_stamps,
          note("Three consecutive starts reach every later total", "reach every total",y=577,size=34)),
    scene("Seven is the largest missing total",
          chart(("Five-cent stamps used","Amount left for threes"),
                [(("2","Too much"),"two fives"),(("1","2"),"with one five"),
                 (("0","7"),"with no fives")],y=220,row_height=83),
          note("Neither 2 nor 7 is divisible by 3", "neither works",y=569)),
    scene("Ten final digits cover every square",
          chart(("Last digit","0","1","2","3","4","5","6","7","8","9"),
                [(("n² ends","0","1","4","9","6","5","6","9","4","1"),"their squares end")],
                y=283,row_height=100,width=1100,font=29),
          note("The last digit of the square is never 7", "seven never appears")),
    exercise((("Check all finite cases","check them all"),("Find a starting block","a starting block"),
              ("Carry the result forward","carries the result forward")),
             "notebook challenge",("You have 4-cent and 5-cent stamps.","What is the largest total you cannot make?")),
 ),
 "T17.E":(
    scene("Why is the product of neighbours always even?",
          cards((("3 × 4 = 12",BLUE),("6 × 7 = 42",GOLD)),337,width=336,gap=391,
                words="three times four",size=37),
          note("Build a proof for every pair of neighbours", "the proof must cover")),
    scene("Every pair of neighbours has one even number",
          cards(tuple((str(i),BLUE if i%2==0 else GOLD) for i in range(8)),337,width=98,gap=118,
                words="whole numbers alternate"),
          note("Blue is even. Gold is odd.", "exactly one is even",y=523)),
    scene("Case 1: the first number is even",directed_case(True),
          note("Two equal groups of columns", "result is still two lots")),
    scene("Case 2: the next number is even",directed_case(False),
          note("Two equal groups of rows", "the product is even")),
    scene("The whole product splits into two staircases",
          board(4,5,width=68,y=358,
                cells=tuple((r,c,BLUE if c<=r else GOLD,"two identical staircases") for r in range(4) for c in range(5)),
                marks=tuple((r,c,"•",WHITE,None) for r in range(4) for c in range(5))),
          note("Each half has 1 + 2 + 3 + 4 dots", "each half is one plus two",y=565)),
    exercise((("Split into two cases","the two cases cover"),("Prove both products even","each gives an even product")),
             "then explain",("Why is the product of three whole numbers in a row",
                              "always a multiple of three?")),
 ),
}
