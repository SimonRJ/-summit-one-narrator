"""Show ratios, combined rates and weighted means as amounts."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blocks, cards, chart,
                          cue, equation, exercise, link, move, note, scene, tile)
from stage import mix
from studio_diagrams import bead, fit, rail


def ratio_five(stage,s, *, count=None, amount="", labels=("First share","Second share"), difference=None):
    xs=[308+166*i for i in range(5)]
    for i,x in enumerate(xs):
        mark=amount if count and cue(s,count)>.45 else ""
        tile(stage,x,348,mark,BLUE if i<3 else GOLD,149,93,size=42)
    p=cue(s,"three equal parts") if s.scene["n"]==1 else 1
    stage.bracket(xs[0]-68,xs[2]+68,440,labels[0],BLUE,p)
    stage.bracket(xs[3]-68,xs[4]+68,440,labels[1],GOLD,p)
    if difference:
        stage.bracket(xs[2]-73,xs[2]+73,250,difference,MINT,cue(s,"nine more than ben"))


def shared_ratio(stage,s):
    p=cue(s,"so that b is twelve parts",duration=.9)
    for y,left,mid,right,colour in ((270,"A","B","2 : 3",BLUE),(411,"B","C","4 : 5",GOLD)):
        tile(stage,337,y,left,colour,104,65)
        tile(stage,509,y,mid,colour,104,65)
        fit(stage,right,699,y,39,198,WHITE,1-p)
        label="8 : 12" if y<400 else "12 : 15"
        fit(stage,label,699,y,39,198,WHITE,p)
        fit(stage,"× 4" if y<400 else "× 3",973,y,32,170,MINT,p)


def tank(stage,s, *, slices, fill, x=640, y=348, colour=BLUE, label=""):
    left,top,w,h=x-213,y-138,426,276
    stage.box(left,top,w,h,radius=4,fill="#162631",edge=BLUE,stroke=3)
    for i in range(slices):
        f=max(0,min(1,fill-i))
        height=h/slices
        base=top+h-i*height
        stage.box(left+2,base-height*f,w-4,height*f,radius=2,fill="#315b79",edge=colour,opacity=f)
        if i:
            stage.line([(left,base),(left+w,base)],RIM,1)
    if label:
        fit(stage,label,x,y+173,33,w+40,colour)


def runners(stage,s):
    p=cue(s,"they meet after ten",duration=1.2)
    xa,xb=mix(296,701,p),mix(971,701,p)
    rail(stage,[296,431,566,701,836,971],363,["0 m","20","40","60","80","100 m"])
    bead(stage,xa,326,BLUE,1,23)
    bead(stage,xb,326,GOLD,1,23)
    fit(stage,"6 m/s",xa-65,248,29,168,BLUE)
    fit(stage,"4 m/s",xb+65,248,29,168,GOLD)
    fit(stage,"Gap closes at 6 + 4 = 10 m/s",640,511,35,1020,MINT,cue(s,"ten metres per second"))


def level_scores(stage,s):
    scores=(3,4,7,9,12)
    p=cue(s,"shared equally",duration=1.25)
    for i,n in enumerate(scores):
        x=337+151*i
        h=19*mix(n,7,p)
        stage.box(x-43,461-h,86,h,fill="#274d64",edge=BLUE,radius=4,stroke=2)
        fit(stage,f"{round(mix(n,7,p))}",x,460-h-19,27,81,GOLD)
    stage.line([(251,461-7*19),(1031,461-7*19)],MINT,3,p)
    fit(stage,"35 points in total across 5 scores",640,559,33,1080,MINT,cue(s,"the mean multiplied"))


def points(stage,s, *, equal=False, mean=None):
    a,b=353,923
    xs=[a+i*(b-a)/4 for i in range(5)]
    rail(stage,xs,430,["6","7","8","9","10"])
    for i in range(2):
        bead(stage,xs[1],395-49*i,BLUE,1,20)
    for i in range(2 if equal else 3):
        bead(stage,xs[3],395-49*i,GOLD,1,20)
    if mean is not None:
        word="would be exactly eight" if equal else "pulled towards nine"
        p=cue(s,word,duration=.9)
        x=mix(xs[2],a+(mean-6)*(b-a)/4,p)
        stage.line([(x,403),(x,459)],MINT,6,p)
        fit(stage,f"{mean:g}",x,516,37,122,MINT,p)


FILMS={
 "T16.1":(
    scene("A ratio counts equal parts",ratio_five,
          note("Find the size of one part", "find the size of one part")),
    scene("Find what one part is worth",
          cards((("Recipe",BLUE),("Map",GOLD),("Mixture",MINT)),337,width=237,gap=263,words="recipes maps mixtures"),
          note("The scale is set by one equal part", "what one part is worth")),
    scene("Share forty stickers in the ratio 3 to 2",
          lambda stage,s:ratio_five(stage,s,labels=("Ana: 3 parts","Ben: 2 parts")),
          note("The five parts make 40 stickers", "forty stickers",y=218,colour=BLUE),
          note("How many stickers go to each person?", "how many does each get")),
    scene("Divide the total by the number of parts",
          lambda stage,s:ratio_five(stage,s,count="eight per part",amount="8",labels=("Ana: 24","Ben: 16")),
          note("40 ÷ 5 = 8 in each part", "eight per part",y=224,colour=BLUE),
          equation(("3 × 8 = 24",BLUE,"ana gets three parts"),("     2 × 8 = 16",GOLD,"ben gets two parts"),
                   y=567,size=41)),
    scene("A difference can tell you one part",
          lambda stage,s:ratio_five(stage,s,count="one part is nine",amount="9",labels=("Ana","Ben"),difference="9 more"),
          note("Ana gets 27. Ben gets 18.", "ana has twenty-seven")),
    scene("Make the shared quantity match",shared_ratio,
          equation(("A : B : C",WHITE,"a to b to c"),("= 8 : 12 : 15",MINT,"eight to twelve to fifteen"))),
    scene("Read each share as a fraction of the whole",
          lambda stage,s:ratio_five(stage,s,labels=("3/5 of the whole","2/5 of the whole")),
          note("There are five equal parts in all", "the first share is three fifths")),
    exercise((("Count equal parts","count the parts"),("Find one part","find one part"),("Multiply to get each share","then multiply")),
             "notebook challenge",("Red and blue beads are in the ratio 5 to 3.","There are 16 more red. How many beads are there?")),
 ),
 "T16.2":(
    scene("Turn time into amount per minute",
          lambda stage,s:tank(stage,s,slices=10,fill=cue(s,"one tenth of the tank"),x=573,y=346),
          note("1/10 of a tank per minute", "one tenth",x=1000,y=367,width=425,size=31)),
    scene("Add what the taps fill in one minute",
          cards((("Tap 1 per minute",BLUE),("Tap 2 per minute",GOLD)),329,width=286,gap=373,
                words="in one minute",size=30),
          equation(("First amount",BLUE,"the two amounts"),("+ second amount",GOLD,"can be added"),
                   ("= combined rate",MINT,"combined amount"),size=32)),
    scene("How long will both taps take?",
          cards((("Tap 1: 6 min",BLUE),("Tap 2: 3 min",GOLD)),330,width=294,gap=355,words="one tap fills"),
          note("Both taps run at constant rates", "constant rates",y=465,colour=BLUE),
          note("Work out the amount each fills in a minute", "pause and work out")),
    scene("One minute fills three of six slices",
          lambda stage,s:tank(stage,s,slices=6,fill=cue(s,"fills one slice")+
                             2*cue(s,"two slices a minute"),x=573,y=343),
          note("1 + 2 = 3 slices", "three slices a minute",x=990,y=350,width=400,size=35)),
    scene("Fill all six slices in two minutes",
          lambda stage,s:tank(stage,s,slices=6,fill=3*cue(s,"three slices a minute")+
                             3*cue(s,"takes two minutes"),x=574,y=343),
          note("6 ÷ 3 = 2 minutes", "takes two minutes",x=992,y=350,width=420,size=36)),
    scene("Subtract the amount flowing out",
          lambda stage,s:tank(stage,s,slices=12,fill=3*cue(s,"adds three slices")-
                             cue(s,"removes one")+10*cue(s,"fills in six minutes"),x=523,y=343),
          note("3 in − 1 out = 2 slices/min", "the net gain",x=1005,y=315,width=424,size=32),
          note("12 ÷ 2 = 6 minutes", "fills in six minutes",x=1005,y=430,width=424,size=31)),
    scene("Add the rates that close the gap",runners,
          note("100 metres ÷ 10 metres per second = 10 seconds", "meet after ten seconds",y=575,size=32)),
    exercise((("Convert to rates","convert each time"),("Combine the rates","add rates"),
              ("Divide the whole job","divide the job")),"notebook challenge",
             ("One painter takes 4 hours. The other takes 12 hours.","How long together at constant rates?")),
 ),
 "T16.3":(
    scene("The mean is the result of sharing equally",level_scores),
    scene("Different group sizes carry different weight",
          blocks(((2,"Group of 2",BLUE,None),(3,"Group of 3",GOLD,None)),words="different sizes"),
          note("Find each group's total before combining", "recover the total")),
    scene("What is the fifth score?",
          chart(("Scores","Mean"),[(("4 scores","7"),"four scores"),(("5 scores","8"),"the mean becomes eight")],
                y=222,row_height=96,highlight=((0,1),(1,1))),
          note("Find the original total and the new total", "find the totals")),
    scene("The mean and number of scores give the total",
          blocks(((1,"7",BLUE,None),)*4,y=251,width=645,words="four scores"),
          blocks(((1,"8",GOLD,None),)*5,y=423,width=645,words="five scores"),
          note("28", "twenty-eight",x=1082,y=251,width=188,colour=BLUE,size=39),
          note("40", "forty",x=1082,y=423,width=188,colour=GOLD,size=39)),
    scene("The added score is the difference",
          blocks(((28,"Original 28",BLUE,None),(12,"New score",GOLD,None)),words="supplies the difference"),
          equation(("40 − 28",WHITE,"forty minus twenty-eight"),("= 12",MINT,"is twelve"),y=487),
          note("12 = 8 + 4", "eight points and those four extra points",y=565,colour=GOLD)),
    scene("Combine group totals before dividing",
          chart(("Learners","Mean","Total"),
                [(("2","6","12"),"two people average six"),(("3","10","30"),"three people average ten")],
                y=211,row_height=94,highlight=((0,2),(1,2))),
          note("(12 + 30) ÷ 5 = 8.4", "eight point four")),
    scene("The median reads the middle of the sorted list",
          cards(("2","3",("5",MINT),"9",("31",GOLD)),327,width=111,gap=149,words="for two three"),
          note("Median = 5", "the median is five",x=454,y=503,width=308,colour=MINT),
          note("Mean = 10", "the mean is ten",x=845,y=503,width=308,colour=GOLD)),
    exercise((("Recover the total","mean times the number"),("Reason with totals","do your reasoning"),
              ("Find the middle for the median","the median is the middle")),"notebook challenge",
             ("Six numbers have mean 9. After removing one, the mean is 8.",
              "Which number was removed?")),
 ),
 "T16.E":(
    scene("Find the mean score of all five learners",points,
          note("Two learners score 7. Three learners score 9.", "three learners",y=557)),
    scene("Add up the points each group contributes",
          chart(("Learners","Points each","Total"),
                [(("2","7","14"),"the first group"),(("3","9","27"),"the second group")],
                y=229,row_height=95,highlight=((0,2),(1,2)))),
    scene("Share all forty-one points among five learners",
          blocks(((1,"8.2",BLUE,None),)*5,y=334,width=860,words="the mean score"),
          equation(("41 ÷ 5",WHITE,"forty-one divided by five"),("= 8.2",MINT,"eight point two"))),
    scene("The larger group has more weight",lambda stage,s:points(stage,s,mean=8.2),
          note("8.2 is closer to the group of three at 9", "pulled towards nine",y=587,size=30)),
    scene("Equal group sizes have an equal weight",lambda stage,s:points(stage,s,equal=True,mean=8),
          note("Two at 7 and two at 9 have mean 8", "their simple average works",y=587,size=30)),
    exercise((("Combine the totals","combine the totals"),("Divide by all the people","the total number of people")),
             "then find",("Four learners score 5 each and one learner scores 10.","What is their mean score?")),
 ),
}
