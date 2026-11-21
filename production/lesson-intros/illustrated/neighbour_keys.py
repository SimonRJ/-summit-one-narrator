"""Key clips and an exact area model for the two overlapping adjacency events."""
from collections import Counter
from itertools import permutations

PAPER = '#172932'
WHITE, MUTED = '#fbf6e8', '#c5d6d6'
GOLD, BLUE, GREEN, ROSE = '#ffce75', '#8ad7fa', '#8ee8ad', '#ffaaa1'
OUTLINE, PANEL = '#55767b', '#243c46'
COLOURS = dict(A=GOLD, B=GOLD, C=BLUE, D=BLUE)


def title(c, s):
    c.text(s, 60, 62, 42, WHITE, 'lm', True)


def note(c, s, y=530, colour=WHITE):
    c.text(s, 640, y, 35, colour, bold=True)




def key(c, letter, x, y):
    colour = COLOURS.get(letter, MUTED)
    c.line([(x, y-55), (x, y-26)], MUTED, 4)
    c.rect(x-7, y+15, 14, 61, colour)
    c.rect(x+5, y+55, 14, 9, colour)
    c.rect(x+5, y+68, 20, 8, colour)
    c.dot(x, y, 32, colour)
    c.dot(x, y-23, 4, PAPER)
    c.text(letter, x, y+3, 34, PAPER, bold=True)


def bracket(c, x1, x2, y, colour):
    c.line([(x1, y-14), (x1, y), (x2, y), (x2, y-14)], colour, 5)


def rail(c, letters, y, clips=(), centre=640, advance=108):
    x0 = centre-(len(letters)-1)*advance/2
    c.line([(x0-45,y-56),(x0+(len(letters)-1)*advance+45,y-56)], OUTLINE, 6)
    for i,letter in enumerate(letters):
        key(c,letter,x0+i*advance,y)
    for start,colour in clips:
        bracket(c, x0+start*advance-32, x0+(start+1)*advance+32, y+94, colour)


def strip(c, a=False, b=False, union=False, keep=False):
    # The single-event brackets overlap on exactly two of the 21 equal squares.
    x, step, y = 125, 49, 277
    edges = [x+i*step for i in range(22)]
    for i in range(21):
        ink = PANEL
        if a and i<6: ink=GOLD
        if b and 4<=i<10: ink=BLUE
        if a and b and 4<=i<6: ink=ROSE
        if union and i<10: ink=MUTED
        if keep and i>=10: ink=GREEN
        c.rect(edges[i], y, step-2, step-2, ink, OUTLINE)
    if a:
        bracket(c,edges[0],edges[6]-2,y-14,GOLD)
        c.text('A beside B', (edges[0]+edges[6])/2, y-57, 29, GOLD, bold=True)
    if b:
        bracket(c,edges[4],edges[10]-2,y+78,BLUE)
        c.text('C beside D',(edges[4]+edges[10])/2,y+111,29,BLUE,bold=True)
    c.text('1 square = 240 rows', 640, 144, 30, WHITE)


def intro(c,q):
    title(c,'Which keys must travel together?')
    clipped=q.after('one movable block')>0
    flip=q.after('allowed orders')>0
    rail(c,'CBA' if flip else 'CAB',260,[(1,GOLD)] if clipped else [])
    if clipped: note(c,'1 clip + 1 loose key',451,GOLD)
    if flip: note(c,'Inside the clip     AB  or  BA',535)


def cues(c,q):
    title(c,'Read the exact restriction')
    turned=q.after('Next to')>0
    overlap=q.after('two named pairs')>0
    if overlap:
        rail(c,'ABCDE',260,[(0,GOLD),(2,BLUE)])
        note(c,'This row breaks both “stay apart” rules',480)
    else:
        rail(c,'BAC' if turned else 'ABC',260,[(0,GOLD)])
        note(c,'Next to     AB or BA' if turned else 'Immediately before     AB only',480)


def easy(c,q):
    title(c,'Three different keys')
    slide=q.after('sliding',1.5)
    c.line([(380,189),(900,189)],OUTLINE,6)
    # Lift C clear of the clip, slide AB as one piece, then lower C.
    lift=min(1,slide*4, (1-slide)*4)
    for letter,start,end in [('A',460,640),('B',640,820),('C',820,460)]:
        across=max(0,min(1,(slide-.25)*2))
        x=start+(end-start)*across
        key(c,letter,x,245-110*lift if letter=='C' else 245)
    if q.after('immediately before'):
        shift=180*max(0,min(1,(slide-.25)*2))
        bracket(c,428+shift,672+shift,339,GOLD)
    if q.after('How many'):
        note(c,'A immediately before B',435,GOLD)
    if slide:
        c.text('Move AB as a pair',640,567,28,MUTED)


def easy_work(c,q):
    title(c,'Place the ordered clip on either side of C')
    second=q.after('Place it after')>0
    rail(c,'ABC',245,[(0,GOLD)],centre=345)
    if second:
        rail(c,'CAB',245,[(1,GOLD)],centre=935)
    if q.after('two possible rows'):note(c,'2 positions × 1 internal order = 2',445,GREEN)
    if q.after('Turning the clip'):note(c,'BA would reverse the required order',535,ROSE)


def medium(c,q):
    title(c,'Six different keys on one rail')
    reverse=q.after('or after')>0
    rail(c,'DBAECF' if reverse else 'DABECF',260,[(1,GOLD)] if q.after('must be adjacent') else [])
    if q.after('How many'):note(c,'A beside B',447,GOLD)
    if reverse:note(c,'Both directions fit',526)


def medium_work(c,q):
    title(c,'Count external and internal choices')
    rail(c,'BACDEF' if q.after('or B A') else 'ABCDEF',205,[(0,GOLD)])
    if q.after('five objects'):
        note(c,'[ pair ]     C     D     E     F',376)
    if q.after('one hundred and twenty'):note(c,'5 × 4 × 3 × 2 × 1 = 120',453,BLUE)
    if q.after('Multiply by two'):note(c,'120 × 2 = 240 rows',538,GREEN)


def hard(c,q):
    title(c,'Seven keys and two forbidden pairs')
    clips=[]
    if q.after('A with B'): clips.append((0,GOLD))
    if q.after('C with D'): clips.append((2,BLUE))
    rail(c,'ABCDEFG',235,clips)
    if q.after('both of those pairs'):note(c,'Allowed only when neither pair touches',452)
    if q.after('overlapping sets'):note(c,'This row belongs to both forbidden sets',535,ROSE)


def hard_work(c,q):
    title(c,'Count rows that break each rule')
    both=q.after('Now use both clips')>0
    cd=q.after('same count')>0
    ab=q.after('Clip A and B')>0
    clips=[]
    if ab and (not cd or both):clips.append((0,GOLD))
    if cd:clips.append((2,BLUE))
    rail(c,'ABCDEFG',204,clips)
    if q.after('five thousand and forty'):note(c,'All rows     7! = 5,040',369)
    if both:
        note(c,'[AB]     [CD]     E     F     G',451)
        if q.after('four times'):note(c,'Both touch     5! × 2 × 2 = 480',534,ROSE)
    elif q.after('Six objects'):
        note(c,'6 objects     6! = 720',452)
        if q.after('one thousand four hundred'):note(c,'One pair touches     720 × 2 = 1,440',534,GOLD)


def hard_answer(c,q):
    title(c,'Keep the rows outside both brackets')
    a=q.after('first bracket')>0
    b=q.after('second spans')>0
    union=q.after('ten different squares')>0
    keep=q.after('Eleven squares remain')>0
    strip(c,a,b,union,keep)
    if keep:note(c,'11 × 240 = 2,640 allowed rows',532,GREEN)
    elif union:note(c,'6 + 6 − 2 = 10 squares   ·   2,400 forbidden rows',532)
    elif q.after('share two'):note(c,'2 shared squares = 480 rows',532,ROSE)


def mistake(c,q):
    title(c,'Track one row through the subtraction')
    twice=q.after('subtract it again')>0
    once=q.after('Subtract it for')>0
    restore=q.after('Put it back')>0
    rail(c,'ABCDEFG',220,[(0,GOLD),(2,BLUE)])
    expr='1' + (' − 1' if once else '') + (' − 1' if twice else '') + (' + 1' if restore else '')
    note(c,expr+' = '+str(1-int(once)-int(twice)+int(restore)) if once else 'Start with 1 copy',423, GREEN if restore else WHITE)
    note(c,'Contribution of this row to the allowed count',514,MUTED)


def recap(c,q):
    title(c,'Try the rule on a fresh row')
    final=q.after('Finally test')>0
    if final:
        rail(c,'ACEBFDG',255)
        if q.after('Neither named pair'):
            note(c,'A and B apart     •     C and D apart',486,GREEN)
    else:
        both=q.after('two pairs are forbidden')>0
        rail(c,'ABCDE' if both else 'ABC',250,[(0,GOLD),(2,BLUE)] if both else [(0,GOLD)])
        if both:note(c,'Both clips fit here: count the shared rows',486)
        elif q.after('Count the objects'):note(c,'AB and C     →     2 movable objects',486)
        else:note(c,'“Immediately before” fixes AB',486,GOLD)


SCENES=[intro,cues,easy,easy_work,medium,medium_work,hard,hard_work,hard_answer,mistake,recap]


def verify():
    def touching(row,a,b):
        return abs(row.index(a)-row.index(b))==1
    assert [''.join(p) for p in permutations('ABC') if p.index('B')==p.index('A')+1]==['ABC','CAB']
    assert sum(touching(p,'A','B') for p in permutations('ABCDEF'))==240
    regions=Counter((touching(p,'A','B'),touching(p,'C','D')) for p in permutations('ABCDEFG'))
    assert regions=={(True,False):4*240,(True,True):2*240,(False,True):4*240,(False,False):11*240}
    assert not any(touching('ACEBFDG',a,b) for a,b in ['AB','CD'])
