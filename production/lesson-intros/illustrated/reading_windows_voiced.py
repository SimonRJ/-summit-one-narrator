"""Equal shares, unequal group sizes and one shared reading, timed on the released Voice C track."""
from fractions import Fraction
from statistics import mean

from captioned_film import mix

PAPER, INK, SOFT = '#102932', '#f7f8ef', '#bed0d0'
TEAL, GOLD, RED, GRID = '#66ddcf', '#ffcf82', '#ffa9a0', '#4f6d73'
BLUE = '#a6caff'


def title(c, words):
    c.text(words, 58, 57, 42, INK, 'lm', True)


def line(c, words, y, colour=INK):
    c.text(words, 640, y, 36, colour, bold=True)


def stacks(c, values, target=None, progress=0, visible=3):
    """Every counter stays visible and is transported from a donor to a receiver."""
    columns = [460, 640, 820]
    coords = [(i, level) for i, value in enumerate(values) for level in range(value)]
    moved = {}
    if target is not None:
        surplus = [(i,h) for i,v in enumerate(values) for h in reversed(range(target,v))]
        empty = [(i,h) for i,v in enumerate(values) for h in range(v,target)]
        for n,(src,dst) in enumerate(zip(surplus,empty,strict=True)):
            u = max(0,min(1,progress*len(surplus)-n));moved[src]=(dst,u)
    for i,x in enumerate(columns):
        c.line([(x-54,472),(x+54,472)],GRID,4)
        c.text(str(i+1),x,508,27,SOFT)
    for i,h in coords:
        if i>=visible: continue
        (j,k),u = moved.get((i,h),((i,h),0))
        # Lift the moving counter above occupied positions during transfer.
        x=mix(columns[i],columns[j],u)
        y=mix(451-17*h,451-17*k,u)-95*4*u*(1-u)
        c.rect(x-37,y-5,74,10,(TEAL,GOLD,BLUE)[i])
    for i in range(visible):
        if progress==0 or progress==1:
            count = target if progress==1 and target is not None else values[i]
            c.text(str(count),columns[i],425-17*(count-1),29,INK,bold=True)


def groups(c, second=True, progress=0, first_label='', second_label=''):
    left, dx, floor, scale = 227, 84, 465, 9
    for i in range(10):
        if i>=4 and not second:continue
        x=left+dx*i;v=mix(27 if i<4 else 7,15,progress)
        c.rect(x,floor-scale*v,49,scale*v,TEAL if i<4 else GOLD)
        c.text(str(i+1),x+24,floor+24,23,SOFT)
    c.line([(208,floor),(1046,floor)],GRID,3)
    c.text(first_label,378,169,28,TEAL,bold=True)
    if second:c.text(second_label,875,169,28,GOLD,bold=True)
    if progress==1:
        y=floor-15*scale
        c.line([(204,y),(1050,y)],INK,3)
        c.text('15',1078,y,30,INK,bold=True)


def windows(c, top='', bottom='', focus=False, shared='', first=True, last=True):
    """Both group rows use the same eight x coordinates; exactly column five occurs twice."""
    start,step=245,105
    for i in range(8):
        x=start+i*step
        c.text(str(i+1),x,177,30,INK,bold=True)
        c.line([(x,207),(x,415)],GRID,1)
        if first and i<5:c.rect(x-45,234,90,62,TEAL)
        if last and i>=4:c.rect(x-45,344,90,62,GOLD)
        if i==4 and focus:
            c.rect(x-48,219,96,203,None,RED,4)
            if shared:
                c.text(shared,x,265,32,PAPER,bold=True)
                c.text(shared,x,375,32,PAPER,bold=True)
    c.text('Position',62,177,27,SOFT,'lm')
    c.text('First five',42,264,26,TEAL,'lm',True)
    c.text('Last four',42,375,26,GOLD,'lm',True)
    if top:c.text(top,1010,263,30,TEAL,bold=True)
    if bottom:c.text(bottom,425,375,30,GOLD,bold=True)


def opening(c,q):
    title(c,'Share twelve counters equally')
    progress=q.after('Move one spare counter',2.6)
    stacks(c,[2,5,5],4,progress)
    if q.after('Multiply a mean'):
        line(c,'3 readings × mean 4 = total 12',563,TEAL)
    elif q.after('four is the mean'):
        line(c,'12 ÷ 3 = 4',563,TEAL)


def exams(c,q):
    title(c,'Look for the count attached to each mean')
    if not q.after('a Rossmoyne-style puzzle'):
        for i in range(4):
            x=355+i*190
            c.rect(x-75,239,150,105,'#23434b',GRID)
            c.text('Day '+str(i+1),x,288,30,INK,bold=True)
        if q.after('Four days'):line(c,'4 days × mean score = total score',459,TEAL)
    else:
        windows(c,first=bool(q.after('first five')),last=bool(q.after('last four')),
                focus=bool(q.after('which day')))
        if q.after('which day'):line(c,'Which day enters both totals?',540,RED)


def easy(c,q):
    title(c,'Share three readings equally')
    n=sum(bool(q.after(phrase)) for phrase in ('eight','fourteen','seventeen'))
    stacks(c,[8,14,17],visible=n)
    if q.after('Imagine redistributing'):line(c,'Move counters until all three stacks match.',564)


def share(c,q):
    title(c,'Keep all 39 counters')
    stacks(c,[8,14,17],13,q.after('Divide by three',2.25))
    if q.after('is thirteen'):line(c,'39 ÷ 3 = 13',563,TEAL)
    elif q.after('thirty-nine'):line(c,'8 + 14 + 17 = 39',563)


def medium(c,q):
    title(c,'Combine two groups of different sizes')
    groups(c,second=bool(q.after('a second group')),
           first_label='4 readings · mean 27' if q.after('mean twenty-seven') else '',
           second_label='6 readings · mean 7' if q.after('mean seven') else '')
    line(c,'Bars show equal shares within each group.',552,SOFT)


def weighted(c,q):
    title(c,'Ten readings share one total')
    groups(c,progress=q.after('Divide this total',2.6),
           first_label='4 × 27 = 108' if q.after('one hundred and eight') else '4 × 27',
           second_label='6 × 7 = 42' if q.after('forty-two') else '6 × 7')
    if q.after('It lies between'):line(c,'7  <  15  <  27      ·      distances 8 and 12',552)
    elif q.after('mean is fifteen'):line(c,'150 ÷ 10 = 15',552,TEAL)
    elif q.after('one hundred and fifty'):line(c,'108 + 42 = 150',552)


def hard(c,q):
    title(c,'Eight readings in two overlapping groups')
    windows(c,top='mean 13' if q.after('mean thirteen') else '',
            bottom='mean 51/4' if q.after('fifty-one over four') else '',
            focus=bool(q.after('Exactly one reading')),first=bool(q.after('The first five')),
            last=bool(q.after('The last four')))
    if q.after('one hundred and one'):line(c,'Mean of all eight = 101/8',537)


def overlap(c,q):
    title(c,'Restore the totals before comparing')
    a='5 × 13 = 65' if q.after('sixty-five') else '5 × 13'
    b='4 × 51/4 = 51' if q.after('fifty-one') else '4 × 51/4'
    windows(c,a,b,bool(q.after('Adding the first and last totals')),
            '15' if q.after('list is fifteen') else '')
    if q.after('list is fifteen'):line(c,'65 + 51 − 101 = 15',536,RED)
    elif q.after('reading twice'):line(c,'65 + 51 counts position 5 twice.',536,RED)
    elif q.after('one hundred and one'):line(c,'All eight total 8 × 101/8 = 101',536)


def check(c,q):
    title(c,'Check with three disjoint pieces')
    parts=[(4,'50',TEAL,'The first four','or fifty'),(1,'15',RED,'shared reading','shared reading'),
           (3,'36',GOLD,'The last three','or thirty-six')]
    x=231
    for n,value,colour,arrive,total in parts:
        if q.after(arrive):
            for i in range(n):
                c.rect(x+102*i,252,96,74,colour)
            middle=x+51*n-3
            c.text(str(n)+(' position' if n==1 else ' positions'),middle,204,25,SOFT,bold=True)
            if q.after(total):
                c.text('15' if n==1 else 'total '+value,middle,361,32,colour,bold=True)
        x+=102*n
    if q.after('one hundred and one'):
        line(c,'50 + 15 + 36 = 101    ·    4 + 1 + 3 = 8',522,TEAL)
    elif q.after('last three'):line(c,'51 − 15 = 36',515,GOLD)
    elif q.after('sixty-five minus fifteen'):line(c,'65 − 15 = 50',515,TEAL)


def mistakes(c,q):
    title(c,'Two checks before you divide')
    if not q.after('another trap'):
        groups(c,progress=q.after('weighted answer',1.0),first_label='4 readings',second_label='6 readings')
        if q.after('weighted answer'):line(c,'(4 × 27 + 6 × 7) ÷ 10 = 15',550,TEAL)
        elif q.after('gives seventeen'):line(c,'(27 + 7) ÷ 2 = 17   weights groups equally',550,RED)
    else:
        windows(c,focus=bool(q.after('overlapping windows')),shared='15')
        if q.after('Keep it once'):line(c,'Only one copy belongs in the total.',545,RED)


def recap(c,q):
    title(c,'Keep count, mean and total together')
    if not q.after('Before combining groups'):
        for x,word,val,wordcue in [(370,'Count','4','Four readings'),(640,'Mean','27','averaging twenty-seven'),
                                   (910,'Total','108','one hundred and eight')]:
            c.text(word,x,227,32,SOFT)
            if q.after(wordcue):c.text(val,x,324,53,TEAL if word!='Total' else GOLD,bold=True)
        if q.after('one hundred and eight'):line(c,'4 × 27 = 108',482)
    elif not q.after('If groups overlap'):
        groups(c,first_label='4 readings',second_label='6 readings')
        if q.after('Combine disjoint totals'):line(c,'Disjoint groups     108 + 42 = 150',548,TEAL)
    else:
        windows(c,focus=True,shared='15')
        if q.after('number of distinct'):line(c,'Divide the total by 8 distinct readings.',545,TEAL)
        elif q.after('extra copy'):line(c,'65 + 51 − 15 = 101',545,RED)


SCENES=(opening,exams,easy,share,medium,weighted,hard,overlap,check,mistakes,recap)


def verify():
    assert mean((8,14,17))==13 and 8+14+17==39
    assert 27*4==108 and 7*6==42 and (108+42)/10==15
    assert Fraction(101,8)*8==101 and Fraction(51,4)*4==51
    front,last=set(range(1,6)),set(range(5,9))
    assert front & last=={5} and len(front|last)==8
    assert 65+51-101==15
    witness=[11,12,13,14,15,10,12,14]
    assert sum(witness)==101 and sum(witness[:5])==65 and sum(witness[4:])==51
