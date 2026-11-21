"""S075. Track every bead, align the two rulers and preserve all 56 counters during transfer."""
from fractions import Fraction
from math import sin, pi
from captioned_film import cue,mix
ID='S075'
ORIGINAL='48edad3b6e3b0ca99e3f007bd689a9d589bd63e1ed0da5ca636ba719cb0e6543'
START=(0,18.04,34.52,47.94,61.22,75.27,94.95,110.44,131.24,146.28,161.32)
POSTER=139
PAPER='#122a31'
WHITE,DIM,LINE,BOARD='#fff3d9','#b6cacc','#567678','#1a3740'
RED,BLUE,GOLD,MINT='#ff9d8a','#8dcbea','#ffcf6e','#9edab7'
def text(c,s,x,y,z=29,col=WHITE,anchor='mm'):
    c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    text(c,s,50,55,42,WHITE,'lm');c.line([(50,100),(1230,100)],LINE,2)
def bead(c,x,y,r,col):
    c.dot(x,y,r,col);c.dot(x-r*.19,y-r*.17,r*.26,PAPER)
def beadrow(c,x,y,f=1,scale=1):
    for j in range(9):
        p=max(0,min(1,f*10-j))
        if p:bead(c,x+j*49*scale,y,max(1,15*scale*p),RED if j<3 else BLUE)
def parts(c,x,y,red,sz=48,mark=0):
    for i in range(8):
        xx=x+i*sz
        col=RED if i<red else BLUE
        c.rect(xx,y,sz-3,sz*.82,col,GOLD if mark and 3<=i<5 else PAPER,3)
def intro(c,t):
    title(c,'Keep track of what one part means')
    for row in range(2):
        if t>row*2.0:beadrow(c,131,226+row*68,cue(t,row*2,1.1))
    text(c,'Same bead recipe',325,381,29,RED)
    if t>7:
        parts(c,739,236,3,51)
        text(c,'3 of 8 equal parts',944,381,29,BLUE)
    if t>12:text(c,'Moving some between piles keeps the total fixed.',640,530,32,MINT)
def cues(c,t):
    title(c,'What changes, and what stays the same?')
    c.rect(123,225,274,27,BLUE)
    for j in range(6):c.line([(123+j*54.8,256),(123+j*54.8,275)],BLUE,3)
    text(c,'Drawing scale',260,359,29,BLUE)
    if t>20.7:
        for j in range(3):bead(c,585+j*48,241,19,RED if j==0 else BLUE)
        text(c,'Recipe',630,359,29)
    if t>25:parts(c,873,220,5,37);text(c,'Two piles',1019,359,29,RED)
    if t>29:text(c,'Scaling a recipe changes the total. A transfer preserves it.',640,525,30,MINT)
def batch_q(c,t):
    title(c,'Three red beads for every six blue beads')
    beadrow(c,151,233,cue(t,34.6,1.7),1.43)
    text(c,'One batch',455,336,31)
    for j in range(4):
        if t>38+j*.38:c.rect(843+(j%2)*92,186+(j//2)*83,78,68,BOARD,LINE,2)
    if t>40:text(c,'4 identical batches',935,427,29,GOLD)
    if t>43:text(c,'Which factor applies to both counts?',640,540,34)
def batch_a(c,t):
    title(c,'Copy the whole batch four times')
    for j in range(4):
        at=47.95+j*.75
        if t>=at:beadrow(c,135,179+93*j,cue(t,at,.9),1.18)
    if t>=50:text(c,'4 × 3 = 12 red',958,240,36,RED)
    if t>=51.4:text(c,'4 × 6 = 24 blue',958,342,36,BLUE)
    if t>=55:
        text(c,'Divide both counts by 4.',932,431,26,DIM)
        text(c,'12 : 24  →  3 : 6',932,485,34,GOLD)
    if t>=57:text(c,'Each row still has the same recipe.',640,568,28,MINT)
def ruler(c,x,y,width,div,top_label,real=False,f=1):
    c.rect(x,y,width,52,BOARD,LINE,2)
    step=width/div
    for j in range(div*10+1):
        xx=x+j*step/10
        c.line([(xx,y),(xx,y+(24 if j%10==0 else 14 if j%5==0 else 8))],DIM,2 if j%10==0 else 1)
    for j in range(div+1):
        if j<=div*f+.01:text(c,str(200*j if real else j),x+j*step,y+82,23,BLUE if real else GOLD)
    text(c,top_label,x,y-35,27,BLUE if real else GOLD,'lm')
def scale_q(c,t):
    title(c,'A 1 : 200 drawing')
    ruler(c,112,232,650,5,'Drawing length in centimetres')
    if t>64:
        c.line([(112,207),(mix(112,762,cue(t,64,1.8)),207)],GOLD,7)
        text(c,'5 cm',964,252,43,GOLD)
    if t>68:text(c,'How long is the real wall in metres?',640,485,37)
    if t>71:text(c,'First compare centimetres with centimetres.',640,561,28,MINT)
def scale_a(c,t):
    title(c,'Use the same units on both scales')
    ruler(c,116,193,660,5,'Drawing · cm')
    p=cue(t,76,.95);q=cue(t,78.7,1.6)
    ruler(c,116,390,660,5,'Real wall · cm',True,.2+.8*q)
    for j in range(1,6):
        if j==1 or q>(j-1)*.18:
            x=116+132*j
            c.line([(x,287),(x,mix(287,343,p))],DIM,2)
    if t>76:text(c,'1 cm → 200 cm',994,203,30,BLUE)
    if t>79.4:text(c,'5 cm → 1000 cm',994,306,30,GOLD)
    if t>83:text(c,'100 cm = 1 m',994,408,27,DIM)
    if t>86:text(c,'1000 ÷ 100 = 10 m',965,502,33,MINT)
    if t>90:text(c,'Scale first. Convert the units once.',640,578,27)
def strips(c,top,bottom,delta=False):
    text(c,'Before',153,226,29,DIM)
    text(c,'After',153,368,29,DIM)
    parts(c,259,203,top,78);parts(c,259,344,bottom,78,delta)
    text(c,f'{top} : {8-top}',1034,235,35)
    text(c,f'{bottom} : {8-bottom}',1034,375,35)
def transfer_q(c,t):
    title(c,'Move 14 counters from the red pile to the blue pile')
    if t<99.5:
        text(c,'Before',166,258,31,DIM);parts(c,289,224,5,78)
        text(c,'5 : 3',1036,257,37)
    else:strips(c,5,3,True)
    if t>102:text(c,'The ratios describe the sizes of the two piles.',640,502,30,MINT)
    if t>106:text(c,'How many counters are there altogether?',640,566,32)
def parts_a(c,t):
    title(c,'Compare equal parts of the same total')
    strips(c,5,3,t>=114)
    if t>=115:
        p=cue(t,115,.95);x=259+3*78;end=x+2*78-3
        c.line([(x,417),(x,433),(mix(x,end,p),433)],GOLD,4)
        if p==1:c.line([(end,433),(end,417)],GOLD,4)
    if t>=117:text(c,'2 parts = 14',394,506,32,GOLD)
    if t>=120:text(c,'1 part = 7',839,506,32,MINT)
    if t>=124:text(c,'8 × 7 = 56 counters',640,570,36)
def transfer_witness(c,t):
    title(c,'Follow the same 56 counters')
    for x,s,col in ((120,'Red pile',RED),(720,'Blue pile',BLUE)):
        text(c,s,x+207,150,31,col)
        c.rect(x,197,415,254,BOARD,col,3)
    # The 14 moving counters retain their colour as they change piles.
    moved=0
    for group in (0,1):
        n=35 if group==0 else 21
        for j in range(n):
            xx=(162 if group==0 else 762)+54*(j%7)
            yy=226+43*(j//7)
            if group==0 and j>=21:
                p=cue(t,134+.055*(j-21),2.1)
                xx=mix(xx,xx+600,p);yy-=64*sin(pi*p)
                moved+=int(p>=1)
            c.dot(xx,yy,14,RED if group==0 else BLUE)
    if t<134:text(c,'35 : 21  =  5 : 3',640,505,37)
    elif moved<14:text(c,'14 red counters cross to the blue pile.',640,505,30,GOLD)
    else:text(c,'21 : 35  =  3 : 5',640,505,37)
    if t>=139:text(c,'21 + 35 = 56. Only the pile sizes changed.',640,571,29,MINT)
def pitfalls(c,t):
    title(c,'Compare both parts, then compare with the whole')
    if t<152.9:
        text(c,'One batch',233,236,26,DIM);beadrow(c,378,235,1,1.2)
        text(c,'Double red alone',227,364,26,RED)
        for j in range(12):
            p=cue(t,147+j*.15,.45)
            if p:bead(c,380+j*54,364,14*p,RED if j<6 else BLUE)
        if t>150:text(c,'6 : 6 is different from 3 : 6.',640,505,33)
    else:
        parts(c,252,234,3,96)
        text(c,'3 red parts',395,378,31,RED);text(c,'5 blue parts',771,378,31,BLUE)
        if t>155:text(c,'Red fraction of the whole = 3 ÷ (3 + 5) = 3/8',640,508,33,GOLD)
def recap(c,t):
    title(c,'Choose the comparison that fits the question')
    if t<166.2:
        ruler(c,172,248,628,5,'Drawing · centimetres')
        text(c,'1 : 200',1000,257,38,GOLD)
        text(c,'Match units before applying a scale.',640,513,32)
    else:
        strips(c,5,3,True)
        if t<171:text(c,'One part represents seven counters.',640,526,32,GOLD)
        else:text(c,'Same 56 counters. Blue gains 2/8 of the whole.',640,528,31,MINT)
        if t>174:text(c,'2/8 × 56 = 14 transferred.',640,581,26)
SCENES=(intro,cues,batch_q,batch_a,scale_q,scale_a,transfer_q,parts_a,transfer_witness,pitfalls,recap)
def verify():
    assert (3*4,6*4)==(12,24) and Fraction(12,24)==Fraction(3,6)
    assert Fraction(5*200,100)==10
    assert 35-14==21 and 21+14==35 and 35+21==56
    # For total 8k, blue changes from 3k to 5k. The unique integer part is 7.
    assert Fraction(14,5-3)==7 and Fraction(2,8)*56==14 and Fraction(3,8)+Fraction(5,8)==1
