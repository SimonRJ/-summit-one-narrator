"""S008: speech-timed animations for palindromes, repunits and divisibility."""

import math

from visuals import AQUA, BLUE, GOLD, PINK, SOFT, VIOLET, WHITE, ease, mix


def tile(a, x, y, value, colour=BLUE, opacity=1, scale=1):
    size = 76 * scale
    a.rounded(x-size/2, y-size/2+5, size, size, 11*scale, '#08121e', opacity*.65)
    a.rounded(x-size/2, y-size/2, size, size, 11*scale, colour, opacity*.22)
    a.path(((x-size/2+7,y+size/2-4),(x+size/2-7,y+size/2-4)), colour, 2, opacity)
    a.label(value, x, y, 44*scale, colour, opacity, bold=True)


def row(a, values, x, y, spacing=100, colours=None, opacity=1, scale=1):
    start = x-(len(values)-1)*spacing/2
    for i, value in enumerate(values):
        tile(a, start+i*spacing, y, value, (colours or [BLUE]*len(values))[i], opacity, scale)


def arc(a, x1, x2, y, height, colour, progress=1):
    pts=[]
    for i in range(41):
        u=i/40
        pts.append((mix(x1,x2,u), y-height*math.sin(math.pi*u)))
    a.trace(pts, progress, colour, 3, False)


def note(a, text, x, y, colour=SOFT, alpha=1, size=27):
    a.label(text, x, y, size, colour, alpha)


def introduction(a,c):
    a.heading('A number with a mirror', AQUA, 'Palindromes and repunits')
    rep=c.after('A repunit', .8)
    first=c.after('reads the same', .9)*(1-rep)
    paired=c.after('Matching digits', 1)*(1-rep)
    row(a, '12321', 640, 318, 112, [GOLD,BLUE,AQUA,BLUE,GOLD], first, 1.12)
    a.dashed((640,203),(640,425),SOFT,2,paired)
    arc(a,416,864,269,62,GOLD,paired)
    arc(a,528,752,292,40,BLUE,paired)
    note(a,'matching outer and inner pairs',640,455,SOFT,paired,29)
    repunit=c.after('made entirely of ones', .8)
    row(a,'11111',640,316,110,[AQUA]*5,repunit,1.12)
    note(a,'A repunit has a 1 in every place',640,436,AQUA,repunit,30)
    p=c.after('one multiplication')
    note(a,'11,111 × 3 = 33,333',640,526,GOLD,p,39)


def exams(a,c):
    a.heading('Find the hidden structure', AQUA)
    p=c.after('read the same', .8)
    rev=c.after('reversed', 1.4)
    start=[455,565,675,785]
    for i,(v,col) in enumerate(zip('1221',[GOLD,BLUE,BLUE,GOLD])):
        x=mix(start[i],start[3-i],rev)
        tile(a,x,260,v,col,p,1)
    note(a,'A palindrome reads the same backwards',640,351,SOFT,p,28)
    rep=c.after('a long row', .8)
    note(a,'11111',640,425,AQUA,rep,54)
    div=c.after('divisibility rule', .8)
    note(a,'Check the digit sum',640,506,GOLD,div,30)
    note(a,'AMC  •  Rossmoyne-style puzzles',640,573,SOFT,c.after('Use the mirror structure'),25)


def basic_prompt(a,c):
    a.heading('Build a repeated digit', AQUA)
    p=c.after('one hundred and eleven',.7)
    row(a,'111',570,264,126,[BLUE,AQUA,GOLD],p,1.15)
    a.label('× 3',850,264,58,WHITE,c.after('multiply by three'),bold=True)
    for x,place,col in zip((444,570,696),('100','10','1'),(BLUE,AQUA,GOLD)):
        note(a,place,x,365,col,c.after('each place separately'),31)
    note(a,'Will any column need a carry?',640,508,SOFT,c.after('need a carry'),32)


def basic(a,c):
    a.heading('Each place grows threefold', AQUA)
    p=c.after('becomes a three',1.35)
    for x,col,label in zip((384,640,896),(BLUE,AQUA,GOLD),('hundreds','tens','ones')):
        note(a,label,x,210,SOFT,1,27)
        tile(a,x,315,'1',col,1-p,1.0)
        tile(a,x,315,'3',col,p,1.0)
        # One place-value unit visibly becomes three copies, then stays grouped.
        for j in range(3):
            spread=ease(max(0,p*1.5-j*.12))
            a.circle((x+(-40+j*40)*spread,mix(359,415,spread)),12,col,spread)
    no=c.after('below ten',.7)
    note(a,'3 in each column: no carry',640,485,SOFT,no,30)
    answer=c.after('three hundred and thirty-three',.7)
    note(a,'111 × 3 = 333',640,558,GOLD,answer,45)


def medium_prompt(a,c):
    a.heading('Split the matching pairs', BLUE)
    p=c.after('two thousand seven hundred',.8)
    row(a,'2772',640,296,135,[GOLD,BLUE,BLUE,GOLD],p,1.2)
    q=c.after('Divide it by eleven')
    note(a,'2,772 ÷ 11 = ?',640,423,WHITE,q,42)
    match=c.after('outer and inner pairs',1)
    arc(a,437.5,842.5,237,67,GOLD,match)
    arc(a,572.5,707.5,260,36,BLUE,match)
    note(a,'outer pair',403,536,GOLD,match,27)
    note(a,'inner pair',877,536,BLUE,match,27)


def medium(a,c):
    a.heading('Same digits, different place values', BLUE)
    row(a,'2772',640,190,98,[GOLD,BLUE,BLUE,GOLD],1,.7)
    outer=c.after('outer copies of two',.8)
    inner=c.after('inner copies of seven',.8)
    arc(a,493,787,157,38,GOLD,outer)
    arc(a,591,689,171,20,BLUE,inner)
    a.arrow((493,208),(545,247),GOLD,outer)
    a.arrow((787,208),(735,247),GOLD,outer)
    a.arrow((591,224),(553,305),BLUE,inner)
    a.arrow((689,224),(727,305),BLUE,inner)
    note(a,'2 × 1,001 = 2,002',640,267,GOLD,outer,37)
    note(a,'7 × 110  = 770',640,332,BLUE,inner,37)
    one=c.after('eleven times ninety-one',.7)
    ten=c.after('eleven times ten',.7)
    note(a,'1,001 = 11 × 91',360,413,GOLD,one,30)
    note(a,'110 = 11 × 10',920,413,BLUE,ten,30)
    common=c.after('share a factor of eleven')
    note(a,'2,772 = 11 × (2 × 91 + 7 × 10)',640,482,WHITE,common,33)
    answer=c.after('two hundred and fifty-two',.7)
    note(a,'2,772 ÷ 11 = 252',640,567,AQUA,answer,43)


def challenge_prompt(a,c):
    a.heading('Count five-digit palindromes', VIOLET, 'The whole number must be divisible by 9')
    p=c.after('five-digit palindromes',.8)
    row(a,'ABCBA',640,327,125,[GOLD,BLUE,AQUA,BLUE,GOLD],p,1.12)
    a.dashed((640,220),(640,432),SOFT,2,p*.7)
    arc(a,390,890,273,69,GOLD,c.after('first and last digits',.8))
    arc(a,515,765,291,40,BLUE,c.after('second and fourth',.8))
    note(a,'A: 1–9',370,513,GOLD,p,30)
    note(a,'B: 0–9',620,513,BLUE,p,30)
    note(a,'C: 0–9',870,513,AQUA,c.after('centre can be'),30)


def challenge(a,c):
    a.heading('Three free digits', VIOLET)
    example=c.after('There is always a choice',.7)
    extra=c.after('Nine is a second choice',.7)
    row(a,'ABCBA',640,230,105,[GOLD,BLUE,AQUA,BLUE,GOLD],1-example,.82)
    p=c.after('digit sum is',.6)
    note(a,'2A + 2B + C',640,322,WHITE,p*(1-example),43)
    n=c.after('for each outer pair',.7)
    note(a,'9 choices for A  ×  10 choices for B',640,414,SOFT,n*(1-example),31)
    base=c.after('zero through eight',.7)
    example_alpha=example*(1-extra)
    note(a,'Example: A = 2, B = 3',640,223,SOFT,example_alpha,32)
    note(a,'2A + 2B = 10',640,296,WHITE,example_alpha,39)
    # Sweep the nine possible centre digits; their sums cover all nine residues.
    begin=c.scene['words'][c.find('zero through eight')[0]]['start']
    chosen=min(8,max(0,int((c.t-begin)*3.4)))
    for i in range(9):
        tile(a,320+i*80,410,str(i),GOLD if i==chosen else BLUE,base*(1-extra),.72)
    result=10+chosen
    note(a,f'10 + {chosen} = {result}',640,510,AQUA,base*(1-extra),38)
    note(a,'A multiple of 9!' if chosen==8 else 'Try the next centre digit',640,561,SOFT,base*(1-extra),27)
    note(a,'Example: A = 1, B = 8  →  2A + 2B = 18',640,245,WHITE,extra,34)
    tile(a,490,389,'0',BLUE,extra,1.1)
    tile(a,790,389,'9',GOLD,extra,1.1)
    note(a,'18 + 0 = 18',490,490,BLUE,extra,31)
    note(a,'18 + 9 = 27',790,490,GOLD,extra,31)
    note(a,'Both centre digits work',640,561,SOFT,extra,29)


def challenge_count(a,c):
    a.heading('Count the extra centre digits', VIOLET)
    diagonal=c.after('sum to nine',1.5)
    last=c.after('nine and nine',.7)
    note(a,'A + B = 9',640,194,GOLD,diagonal,34)
    for i in range(1,10):
        r=(i-1)//5
        column=(i-1)%5
        x=380+column*130+(65 if r else 0)
        y=271+r*93
        a.rounded(x-53,y-31,106,62,10,GOLD,diagonal*.2)
        note(a,f'{i} + {9-i}',x,y,GOLD,diagonal,29)
    note(a,'And: 9 + 9 = 18',640,473,AQUA,last,33)
    total=c.after('Add ninety and ten',.8)
    note(a,'90 + 10 = 100',640,575,WHITE,total,44)


def mistakes(a,c):
    a.heading('Watch the two zero traps', PINK)
    first=c.after('Starting with zero',.7)
    row(a,'01010',640,242,92,[PINK,BLUE,AQUA,BLUE,GOLD],first,.88)
    a.path(((388,188),(430,293)),PINK,5,first)
    note(a,'A leading zero does not make a five-digit number',640,336,PINK,first,27)
    second=c.after('both zero and nine',.7)
    note(a,'18,081',475,454,BLUE,second,45)
    note(a,'18,981',805,454,AQUA,second,45)
    note(a,'digit sums: 18 and 27 — both divisible by 9',640,545,SOFT,second,27)


def recap(a,c):
    a.heading('Your palindrome toolkit', AQUA)
    row(a,'ABCBA',640,244,107,[GOLD,BLUE,AQUA,BLUE,GOLD],c.opening(),1)
    pair=c.after('mirror pairs',.8)
    arc(a,426,854,194,52,GOLD,pair)
    arc(a,533,747,211,32,BLUE,pair)
    sum_=c.after('divisibility test',.7)
    note(a,'digit sum = 2A + 2B + C',640,403,WHITE,sum_,38)
    end=c.after('two single digits',.7)
    note(a,'If zero works in the centre, test 9 too.',640,523,GOLD,end,30)


SCENES=(introduction,exams,basic_prompt,basic,medium_prompt,medium,
        challenge_prompt,challenge,challenge_count,mistakes,recap)


def draw(art, cues, scene):
    SCENES[scene-1](art,cues)
