"""S005: highlight the written digits that contribute to each tally."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, ease


def label(a,text,x,y,size=35,colour=WHITE,alpha=1):
    a.label(text,x,y,size,colour,alpha,bold=True)


def number(a,value,x,y,size=45,highlight=(),alpha=1):
    s=str(value);step=size*.75;left=x-step*(len(s)-1)/2
    for i,ch in enumerate(s):
        label(a,ch,left+i*step,y,size,GOLD if i in highlight else WHITE,alpha)


def falling_number(a,value,x,y,size,highlight,progress):
    """Move each permitted number into its counting position as it is named."""
    number(a,value,x,y-62*(1-progress),size,highlight,progress)


def four_places(a,y,alpha=1):
    for x,v,name,col in zip((320,535,750,965),'5724',('thousands','hundreds','tens','ones'),(BLUE,AQUA,GOLD,PINK)):
        a.rounded(x-58,y-51,116,102,12,col,.2*alpha)
        label(a,v,x,y,55,col,alpha)
        label(a,name,x,y+83,25,SOFT,alpha)


def intro(a,c):
    a.heading('A digit has a value and a place',AQUA)
    p=c.after('a place-value column',.8)
    four_places(a,300,p)
    q=c.after('value of a digit',.8)
    label(a,'2 tens = 20',640,480,39,GOLD,q)
    label(a,'The digit 2 appears once',640,548,32,SOFT,c.after('a position where a digit can appear'))


def exams(a,c):
    a.heading('What exactly are you counting?',AQUA)
    p=c.after('times a digit is written',.8)
    number(a,'44',500,290,92,(0,1),p)
    label(a,'two written 4s',790,290,40,GOLD,p)
    q=c.after('divisibility test',.8)
    label(a,'or test which numbers qualify',640,446,34,BLUE,q)
    label(a,'Count each position separately',640,548,34,WHITE,c.after('column-by-column count'))


def sum_prompt(a,c):
    a.heading('Is 5,724 divisible by 9?',GOLD)
    four_places(a,310,c.after('five thousand',.8))
    label(a,'Add the digits',640,515,39,WHITE,c.after('Add its four digits'))


def sum_answer(a,c):
    a.heading('Why the digit sum works',GOLD)
    p=c.after('Ten, one hundred',.8)
    label(a,'10 = 9 + 1',330,245,34,BLUE,p)
    label(a,'100 = 99 + 1',640,245,34,AQUA,c.after('one hundred',.8))
    label(a,'1,000 = 999 + 1',960,245,34,GOLD,c.after('one thousand',.8))
    for x,txt,cue in ((390,'5','Five'),(520,'7','seven'),(650,'2','two'),(780,'4','four')):
        p=c.after(cue,.65)
        a.circle((x,390-72*(1-p)),32,GOLD,.13*p)
        label(a,txt,x,390-72*(1-p),49,GOLD,p)
    for x,txt,cue in ((455,'+','plus seven'),(585,'+','plus two'),
                      (715,'+','plus four'),(845,'=','is eighteen'),(930,'18','eighteen')):
        label(a,txt,x,390,49,WHITE,c.after(cue,.35))
    label(a,'18 is divisible by 9',640,520,39,AQUA,c.after('Eighteen is a multiple of nine'))


def fours_prompt(a,c):
    a.heading('Count written 4s from 1 to 65',BLUE)
    p=c.after('one through sixty-five',.8)
    label(a,'1, 2, 3, …, 65',640,262,52,WHITE,p)
    label(a,'How many times is 4 written?',640,385,38,GOLD,c.after('digit four'))
    q=c.after('Which number in the range',.8)
    number(a,'44',640,516,64,(0,1),q)


def fours_answer(a,c):
    a.heading('One tally for each position',BLUE)
    units=c.after('units column',.8)
    label(a,'ones',125,245,30,SOFT,units)
    numbers=('4','14','24','34','44','54','64')
    timings=(c.after('Four, fourteen',.35),c.after('fourteen',.35),
             c.after('twenty-four',.35),c.after('so on',.4),
             c.after('so on',.4,.2),c.after('so on',.4,.4),c.after('sixty-four',.35))
    for i,(n,p) in enumerate(zip(numbers,timings)):
        x=235+i*135
        falling_number(a,n,x,245,40,(len(n)-1,),p)
        a.circle((x,285),7,GOLD,p)
    label(a,'7',1165,245,38,GOLD,c.after('seven marks',.45))
    tens=c.after('tens column',.8)
    label(a,'tens',125,385,30,SOFT,tens)
    for i,n in enumerate(range(40,50)):
        x=250+(i%5)*155;y=350+(i//5)*75
        p=c.after('forty through',.4) if i==0 else c.after('forty-nine',.4,(i-1)*.07)
        falling_number(a,n,x,y,38,(0,),p)
        a.circle((x,y+28),6,GOLD,p)
    label(a,'10',1130,385,38,GOLD,c.after('ten more',.45))
    label(a,'7 + 10 = 17 written 4s',640,540,38,WHITE,c.after('Seven plus ten'))
    p=c.after('two fours',1.1)
    a.arrow((790,280),(850,320),PINK,p)


def twos_prompt(a,c):
    a.heading('Count the 2s in multiples of 9',AQUA)
    p=c.after('one through two hundred and fifty',.8)
    label(a,'1 ≤ number ≤ 250',640,240,44,WHITE,p)
    for i,n in enumerate((9,18,27,36,45,54)):
        label(a,str(n),300+i*135,380,40,AQUA,ease(p*1.7-i*.12))
    label(a,'Only multiples of 9 qualify',640,535,34,SOFT,c.after('divisibility rule'))


def units(a,c):
    a.heading('Start with the ones place',AQUA)
    first=c.after('seventy-two',.8);next_=c.after('one hundred and sixty-two',.8);out=c.after('two hundred and fifty-two',.8)
    falling_number(a,'72',300,310,58,(1,),first)
    falling_number(a,'162',640,310,58,(2,),next_)
    falling_number(a,'252',980,310,58,(2,),out)
    a.arrow((390,310),(540,310),BLUE,next_);a.arrow((730,310),(880,310),BLUE,out)
    label(a,'+90',465,255,30,BLUE,next_);label(a,'+90',805,255,30,BLUE,out)
    a.path(((910,355),(1050,265)),PINK,5,out)
    label(a,'Outside 1–250',980,414,28,PINK,out)
    label(a,'2 ones marks',640,545,41,GOLD,c.after('two marks in the units'))


def tens(a,c):
    a.heading('Now the tens place',AQUA)
    p=c.after('twenties',.8)
    for i,(band,n,hi) in enumerate((('20–29','27',0),('120–129','126',1),('220–229','225',1))):
        x=300+i*340
        label(a,band,x,230,30,SOFT,p)
        falling_number(a,n,x,340,62,(hi,),c.after(('twenty-seven','one hundred and twenty-six','two hundred and twenty-five')[i],.8))
    label(a,'3 tens marks',640,520,42,GOLD,c.after('Three tens marks'))


def hundreds(a,c):
    a.heading('Finally the hundreds place',AQUA)
    cues=('two hundred and seven','two hundred and sixteen','two hundred and twenty-five',
          'two hundred and thirty-four','two hundred and forty-three')
    for i,n in enumerate(('207','216','225','234','243')):
        falling_number(a,n,235+i*205,325,49,(0,),c.after(cues[i],.8))
    label(a,'5 hundreds marks',640,445,39,GOLD,c.after('Five hundreds marks'))
    label(a,'2 + 3 + 5 = 10 written 2s',640,535,40,WHITE,c.after('ten written twos'))


def mistakes(a,c):
    a.heading('One number can give two marks',PINK)
    p=c.after('contributes once',.8)
    number(a,'225',500,280,80,(0,1),p)
    label(a,'2 marks',820,280,42,GOLD,p)
    q=c.after('two hundred and fifty-two',.8)
    number(a,'252',500,472,60,(0,2),q)
    a.path(((420,525),(580,419)),PINK,5,q)
    label(a,'past 250',820,472,36,PINK,q)


def recap(a,c):
    a.heading('Count positions, then add',AQUA)
    p=c.after('one tally line per position',.8)
    for i,(name,count) in enumerate((('ones','2'),('tens','3'),('hundreds','5'))):
        x=310+i*330
        label(a,name,x,270,32,SOFT,p)
        label(a,count,x,360,60,(BLUE,GOLD,AQUA)[i],p)
    label(a,'2 + 3 + 5 = 10',640,525,45,WHITE,c.after('before adding'))


SCENES=(intro,exams,sum_prompt,sum_answer,fours_prompt,fours_answer,
        twos_prompt,units,tens,hundreds,mistakes,recap)


def draw(art,cues,scene):
    SCENES[scene-1](art,cues)
