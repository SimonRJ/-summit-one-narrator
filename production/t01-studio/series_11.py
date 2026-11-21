"""Track place value, digit remainders and trades between columns."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RIM, WHITE, board, cards,
                          chart, cue, equation, link, note, scene, tile)
from stage import mix
from studio_diagrams import bead, fit


def tens_units(stage,s):
    t=cue(s,"swap the digits",duration=.90)
    for n,x,y,z in ((42,345,220,1-t),(24,912,220,t)):
        fit(stage,str(n),x,y,56,302,MINT if n==24 else BLUE,z)
        a,b=divmod(n,10)
        for j in range(a):
            xx=x+27*j-72
            stage.box(xx,302,19,127,edge=BLUE,fill="#224a66",radius=2,opacity=z)
            for k in range(1,10):
                stage.line([(xx,302+12.7*k),(xx+19,302+12.7*k)],RIM,1,z)
        for j in range(b):
            stage.box(x+60+22*(j%3),388+22*(j//3),18,18,edge=GOLD,fill="#574837",radius=2,opacity=z)
    fit(stage,"4 tens + 2 units",345,488,31,442,WHITE,1-t)
    fit(stage,"2 tens + 4 units",912,488,31,442,WHITE,t)
    stage.arrow((529,358),(748,358),MINT,t,4)


def place_trade(stage,s, *, tens=False):
    n=12 if tens else 15
    q=cue(s,"make one hundred" if tens else "make one ten",duration=.9)
    xx=426 if tens else 849
    dst=393 if not tens else 198
    for i in range(n):
        y=283+72*(i//8)
        x=xx+49*(i%8-3.5)
        if tens:
            word="five tens" if i<5 else "six tens" if i<11 else "the carried ten"
        else:
            word="eight plus" if i<8 else "seven is"
        visible=cue(s,word,duration=.28)
        if i<10:
            x,y=mix(x,dst,q),mix(y,431,q)
        if tens:
            stage.box(x-12,y-26,24,52,edge=BLUE,fill="#264d69",radius=3,opacity=visible*(1-q if i<10 else 1))
        else:
            bead(stage,x,y,GOLD,visible*(1-q if i<10 else 1),17)
    tile(stage,dst,430,"100" if tens else "10",MINT,122,73,q,size=34)
    fit(stage,"Trade 10 tens for 1 hundred" if tens else "Trade 10 units for 1 ten",
        640,521,36,1050,MINT,q)


def digit_board(which=None, words=None, *, selected=None):
    def draw(stage,s):
        n=10
        width=40
        centers=515,375
        marks=[(r,c,str(10*r+c),WHITE,None) for r in range(10) for c in range(10) if r or c]
        tint=[]
        if which in ("units","both"):
            if which=="units":
                spoken=("ten numbers seven","seventeen","twenty-seven",*("up to ninety-seven",)*7)
                tint += [(r,7,BLUE,word) for r,word in enumerate(spoken)]
            else:
                tint += [(r,7,BLUE,words) for r in range(10)]
        if which in ("tens","both"):
            tint += [(7,c,GOLD,words) for c in range(10)]
        if selected:
            tint.append((7,7,MINT,selected))
        board(n,n,width=width,x=centers[0],y=centers[1],cells=tint,marks=marks)(stage,s)
        tile(stage,765,555,100,MUTED,80,47,size=25)
    return draw


def removing_nines(stage,s):
    amounts=(4,7,2,5)
    words=("four thousands leave four","seven hundreds leave seven","two tens leave two","the five units stay")
    for i,(n,word,k) in enumerate(zip(amounts,words,("Thousands","Hundreds","Tens","Units"))):
        x=264+251*i
        p=cue(s,word)
        tile(stage,x,243,n,BLUE,84,58,size=34)
        fit(stage,k,x,309,26,222,MUTED)
        for j in range(n):
            bead(stage,x+26*(j-(n-1)/2),407,GOLD,p,11)
        fit(stage,f"{n} remains" if n==1 else f"{n} remain",x,463,25,218,GOLD,p)


def reversals(stage,s):
    fit(stage,"Original",171,278,28,170,MUTED)
    fit(stage,"Reversed",171,389,28,170,MUTED)
    for i,word in enumerate(("fourteen","twenty-five","thirty-six","forty-seven","fifty-eight","sixty-nine")):
        value=14+11*i
        x=329+139*i
        show=cue(s,word,duration=.25)
        tile(stage,x,278,str(value),BLUE,99,65,show,36)
        tile(stage,x,389,str(value)[::-1],GOLD,99,65,show,36)
    fit(stage,"52 − 25 = 27",640,525,44,1090,MINT,cue(s,"fifty-two minus twenty-five"))


def double_units(stage,s):
    if s.t<s.at("notebook challenge"):
        scene("Write the digits as tens and units",
              note("Original: 10A + B","write numbers",y=224,colour=BLUE),
              note("Reverse − original = 9(B − A)","reversing and subtracting",y=360,colour=GOLD),
              note("Reverse + original = 11(A + B)","reversing and adding",y=492))(stage,s)
        return
    fit(stage,"Which numbers equal four times their digit sum?",640,87,44)
    fit(stage,"10A + B = 4(A + B)",640,205,44,1000,BLUE,cue(s,"four times"))
    fit(stage,"6A = 3B     →     B = 2A",640,289,38,1000,GOLD,cue(s,"sum of its digits"))
    for i in range(1,5):
        x=235+i*165
        show=cue(s,"find all",delay=(i-1)*.12)
        tile(stage,x,402,str(12*i),MINT,119,74,show,39)
        fit(stage,f"4 × ({i} + {2*i})",x,482,27,161,WHITE,show)
    fit(stage,"A = 5 would require B = 10, outside the digit range",640,561,31,1070,MUTED,cue(s,"all such numbers"))


double_units.chapter="Your turn"


def permutations(stage,s):
    for i,pair in enumerate((("126","162"),("216","261"),("612","621"))):
        x=365+275*i
        for j,value in enumerate(pair):
            tile(stage,x,279+j*86,value,(BLUE,GOLD,MINT)[i],175,68,
                 cue(s,"every arrangement",delay=(2*i+j)*.12),39)
    fit(stage,"1 + 2 + 6 = 9 in all six orders",640,480,36,1010,WHITE,cue(s,"digits one two and six"))
    fit(stage,"Each number is also divisible by 3",640,566,30,1000,MINT,cue(s,"since nine is a multiple"))


def fill_five(stage,s):
    given=cue(s,"five blank eight")
    answer=cue(s,"the blank must be five")
    for x,d in ((466,"5"),(814,"8")):
        tile(stage,x,315,d,BLUE,131,78,given,44)
    tile(stage,640,315,"?",GOLD,131,78,given*(1-answer),44)
    tile(stage,640,315,"5",MINT,131,78,answer,44)
    fit(stage,"5 + 8 = 13",640,444,36,1050,WHITE,cue(s,"known digits add to thirteen"))
    fit(stage,"13 + 5 = 18    →    558 = 9 × 62",640,552,36,1060,MINT,cue(s,"making eighteen"))


def missing_four(stage,s):
    if s.t<s.at("notebook challenge"):
        scene("Use a digit sum to check divisibility",
              note("4,725 and 18 have the same remainder","a number and its digit sum",y=290,colour=BLUE),
              note("18 = 2 × 9 = 6 × 3","on division by nine",y=423))(stage,s)
        return
    fit(stage,"Complete the four-digit multiple of nine",640,87,44)
    result=cue(s,"a multiple of nine")
    for i,(digit,word) in enumerate(zip("73?4",("seven","three blank","blank","four"))):
        x=396+i*165
        if digit=="?":
            tile(stage,x,302,"?",GOLD,129,92,cue(s,word)*(1-result),47)
            tile(stage,x,302,"4",MINT,129,92,result,47)
        else:
            tile(stage,x,302,digit,BLUE,129,92,cue(s,word),47)
    fit(stage,"7 + 3 + 4 = 14",640,419,38,1000,WHITE,cue(s,"four"))
    fit(stage,"14 + 4 = 18     →     7,344 = 9 × 816",640,525,36,1050,MINT,result)


missing_four.chapter="Your turn"


def count_threes(stage,s):
    if s.t<s.at("notebook challenge"):
        scene("Read what the count asks for",
              note("77 has two written sevens","numbers or occurrences",y=247,colour=BLUE),
              note("10 units + 10 tens = 20 occurrences","count each place",y=358,colour=GOLD),
              note("20 − 1 overlap = 19 numbers","remove any overlap",y=473))(stage,s)
        return
    fit(stage,"Count the written threes from 1 to 50",640,87,44)
    reveal=cue(s,"digit three")
    units=cue(s,"numbers from")
    tens=cue(s,"one to fifty")
    for n in range(1,51):
        r,c=divmod(n-1,10)
        x,y=157+64*c,229+65*r
        stage.box(x-29,y-26,58,52,edge=RIM,fill=None,radius=3,opacity=reveal)
        for j,d in enumerate(str(n)):
            pos=x+(j-(len(str(n))-1)/2)*17
            active=tens if n>=10 and j==0 else units
            colour=(GOLD if n>=10 and j==0 else BLUE) if d=="3" and active>.05 else WHITE
            fit(stage,d,pos,y,26,29,colour,reveal)
    fit(stage,"Units: 5 threes",991,283,33,342,BLUE,units)
    fit(stage,"Tens: 10 threes",991,362,33,342,GOLD,tens)
    fit(stage,"5 + 10 = 15",991,450,37,342,MINT,tens)
    fit(stage,"Both digits of 33 count",640,558,31,1050,WHITE,tens)


count_threes.chapter="Your turn"


def trade_again(stage,s):
    challenge=s.t>=s.at("then add")
    fit(stage,"Add 76 and 89" if challenge else "How a carry changes place",640,87,45)
    first="seventy-six" if challenge else "ten of one place"
    second="eighty-nine" if challenge else "one of the next place"
    total="what each carry means" if challenge else second
    for i,label in enumerate(("Hundreds","Tens","Units")):
        x=346+294*i
        fit(stage,label,x,188,30,266,MUTED)
        for j,n in enumerate((76,89) if challenge else (58,67)):
            digs=str(n).rjust(3)
            if digs[i]!=" ":
                tile(stage,x,265+j*73,digs[i],(BLUE,GOLD)[j],90,61,cue(s,(first,second)[j]),33)
        stage.line([(x-125,390),(x+125,390)],RIM,3)
        tile(stage,x,446,str(165 if challenge else 125)[i],MINT,97,67,cue(s,total,delay=(2-i)*.18),37)
    calc=("6 + 9 = 15 units → 1 ten and 5 units","7 + 8 + 1 = 16 tens → 1 hundred and 6 tens") if challenge else ("8 + 7 = 15 units → 1 ten and 5 units","5 + 6 + 1 = 12 tens → 1 hundred and 2 tens")
    fit(stage,calc[0],640,530,28,1070,BLUE,cue(s,second))
    fit(stage,calc[1],640,584,28,1100,GOLD,cue(s,total))


trade_again.chapter="Your turn"


FILMS = {
 "T11.1":(
    scene("A digit changes value when it moves",tens_units),
    scene("Use tens and units instead of guessing",
          cards((("Tens digit",BLUE),("Units digit",GOLD)),308,width=268,gap=346,words="first digit"),
          equation(("10 × first digit",BLUE,"ten times"),("+ second digit",GOLD,"plus its second"),y=546,size=38)),
    scene("The reversed number is 27 bigger",
          cards((("AB",BLUE),("BA",GOLD)),327,width=213,gap=361,words="number is reversed",size=53),
          link((574,327),(702,327),"the new number",arrow=True,colour=MINT),
          note("What is the relationship between the digits?", "what can you say")),
    scene("Write each number with place value",
          chart(("Digits","Tens","Units","Value"),
                [(("AB","A","B","10A + B"),"the number is ten a"),
                 (("BA","B","A","10B + A"),"the reverse is ten b")],
                y=224,row_height=101,highlight=((0,3),(1,3)))),
    scene("Subtract the original from its reverse",
          note("(10B + A) − (10A + B)", "subtract",y=218,colour=BLUE,size=44),
          note("9B − 9A = 9(B − A)", "nine b minus nine a",y=339,colour=GOLD,size=45),
          note("B − A = 27 ÷ 9 = 3", "the units digit is three more",y=479,size=45)),
    scene("List the digit pairs three apart",reversals),
    scene("The sum of a number and its reverse",
          note("(10A + B) + (10B + A)", "adding a number",y=213,colour=BLUE,size=44),
          note("= 11(A + B)", "eleven times the digit sum",y=347,colour=GOLD,size=46),
          note("47 + 74 = 121 = 11 × 11", "eleven times eleven")),
    scene("Each digit has a limited range",
          cards((("A can be 1 to 9",BLUE),("B can be 0 to 9",GOLD)),338,
                width=370,gap=454,words="the first digit runs",size=35),
          note("A is the tens digit of a two-digit number", "those limits often finish")),
    double_units,
 ),
 "T11.2":(
    scene("Each place value is one more than a multiple of nine",
          chart(("Place value","A multiple of 9","Extra"),
                [(("10","9","1"),"ten is one more"),(("100","99","1"),"a hundred is one more"),
                 (("1,000","999","1"),"a thousand is one more")],
                y=205,row_height=82,highlight=((0,2),(1,2),(2,2))),
          note("Units are 0 × 9 + 1 as well", "every place value",y=551,size=36)),
    scene("Digit sums test multiples of nine and three",
          cards(tuple("85432761"),330,width=84,gap=106,words="even for enormous numbers",size=32),
          note("Changing the order leaves the sum alone", "digits are rearranged")),
    scene("Is 4,725 divisible by nine?",
          cards(tuple("4725"),323,width=157,gap=169,words="four thousand",size=46),
          note("Try adding the digits", "pause and add its digits")),
    scene("Remove the nines from each place",removing_nines,
          note("The amount left is the digit sum", "exactly the digit sum")),
    scene("Collect the digit sum",
          cards((("4",BLUE),("7",BLUE),("2",BLUE),("5",BLUE)),295,width=114,gap=166),
          equation(("4 + 7 + 2 + 5",WHITE,"four plus seven"),("= 18",GOLD,"is eighteen"),
                   ("= 2 × 9",MINT,"a multiple of nine"),y=461,size=44),
          note("So 4,725 is also divisible by 9","the same remainder",y=574)),
    scene("Reduce the digit sum to find the remainder",
          cards(("5","8","3"),264,words="five hundred and eighty-three",width=113,gap=158),
          note("5 + 8 + 3 = 16", "digit sum sixteen",y=381,colour=BLUE,size=44),
          note("16 = 9 + 7, so the remainder is 7", "seven more than nine")),
    scene("Rearrange the digits without changing the sum",permutations),
    scene("Use the digit sum to complete a number",fill_five),
    missing_four,
 ),
 "T11.3":(
    scene("A number can contain the same digit twice",
          cards((("2",BLUE),("12",BLUE),("20",BLUE),("22",GOLD)),330,width=138,gap=175,words="twenty-two"),
          note("22 is one number and contains two twos", "contains two twos")),
    scene("Count each place separately",
          cards((("Tens",BLUE),("Units",GOLD)),324,width=305,gap=357,words="place separately",size=46),
          note("Repeated digits belong to two different places","repeated digits take care")),
    scene("How many times is the digit 7 written?",digit_board(),
          note("Write every number from 1 to 100", "one to one hundred",x=996,y=350,width=385,size=28)),
    scene("Units: one seven in each group of ten",digit_board("units","once in every ten"),
          note("10 units digits", "that is ten times",x=995,y=350,width=366)),
    scene("Tens: seven appears from 70 to 79",digit_board("both","seventy to seventy-nine",selected="seventy-seven was counted"),
          note("10 tens + 10 units", "twenty times",x=991,y=316,width=401,size=33,colour=BLUE),
          note("20 written sevens", "written twenty times",x=991,y=391,width=401,size=33),
          note("77 contributes twice", "it has two sevens",x=991,y=467,width=401,size=31,colour=GOLD)),
    scene("Counting numbers needs a different total",digit_board("both","the column has ten",selected="in both"),
          note("10 + 10 − 1 = 19", "nineteen",x=997,y=361,width=415,size=36),
          note("Count 77 only once", "seventy-seven is in both",x=997,y=450,width=415,size=29,colour=GOLD)),
    scene("Count every digit used in page numbers",chart(("Pages","Count","Digits per page","Digits"),
          [(("1 to 9","9","1","9"),"nine digits for the single-digit pages"),
           (("10 to 99","90","2","180"),"two digits each")],
          y=246,row_height=89,highlight=((0,3),(1,3))),
          note("9 + 180 = 189 digits", "one hundred and eighty-nine digits")),
    count_threes,
 ),
 "T11.E":(
    scene("Read each place in the addition",
          chart(("Hundreds","Tens","Units"),[(("","5","8"),"fifty-eight"),
                (("","6","7"),"sixty-seven"),(("","?","?"),None)],y=209,row_height=77,width=540),
          note("What does each carry really mean?", "what each carry really means",y=560)),
    scene("Trade ten units for a ten",lambda stage,s:place_trade(stage,s),
          note("8 + 7 = 15 units", "fifteen units",y=198,colour=BLUE),
          note("5 units remain", "five units remain",y=582,size=34)),
    scene("Trade ten tens for a hundred",lambda stage,s:place_trade(stage,s,tens=True),
          note("5 + 6 + 1 = 12 tens", "twelve tens",y=194,colour=BLUE),
          note("2 tens remain", "two tens remain",y=582,size=34)),
    scene("Read the three places in the answer",
          cards((("100",BLUE),("20",GOLD),("5",MINT)),332,words="one hundred two tens",gap=222,width=161),
          note("100 + 20 + 5 = 125", "one hundred and twenty-five")),
    scene("Check with an estimate and with exact totals",
          chart(("Method","Calculation","Result"),
                [(("Estimate","60 + 70","130"),"roughly sixty"),
                 (("Exact","110 + 15","125"),"together they make")],
                y=229,row_height=98,highlight=((0,2),(1,2))),
          note("50 + 60 = 110 and 8 + 7 = 15", "eight plus seven")),
    trade_again,
 ),
}
