"""Pressed specimens, numbered cabinet tickets and a transposed accession label."""
BACKGROUND = ("#3d443b", "#29332e")
PAPER, INK, CARD, GREEN, GOLD, RED, LINE = (
    "#f5f0dc", "#293932", "#e9d9b8", "#b9d7a0", "#e7c484", "#eab1a3", "#82907c")
HEADINGS = (
    "How the herbarium files a specimen", "Start on the correct shelf", "Step through one tray",
    "Read the torn collection slip", "Strike labels that miss the note",
    "The assistant reverses two digits", "Make a short list from the error", "Restore the missing label",
)
BRIDGE = "Lay out just the tray-3 labels on the shelf from 320 to 370. Which one fits the digit note? For the second leaf, explain how an error of 18 helps you decide which labels to test."


def check_maths():
    assert [n for n in range(100, 141) if n % 8 == 3] == [107, 115, 123, 131, 139]
    labels = [n for n in range(320, 371) if n % 8 == 3]
    assert labels == [323, 331, 339, 347, 355, 363]
    assert [n for n in labels if n // 10 % 10 == 2 * (n % 10)] == [363]

    def reversed_copy(number):
        hundreds, last_two = divmod(number, 100)
        tens, units = divmod(last_two, 10)
        return hundreds * 100 + units * 10 + tens

    candidates = [n for n in range(400, 500) if n - reversed_copy(n) == 18]
    assert candidates == [420, 431, 442, 453, 464, 475, 486, 497]
    assert [n % 8 for n in candidates] == [4, 7, 2, 5, 0, 3, 6, 1]
    assert [n for n in candidates if n % 8 == 3] == [475] and reversed_copy(475) == 457


def label(board, value, x, y, size, colour=PAPER, opacity=1):
    board.text(str(value), x, y, size, colour, bold=True, opacity=opacity)


def specimen(board, x, y, number):
    board.box(x, y, 314, 282, fill=CARD, edge=LINE, stroke=3, radius=13)
    stem = "#627753"
    board.line([(x+101,y+178),(x+168,y+110),(x+214,y+51)], stem, 5)
    for dx, dy, orientation in ((126,151,-1),(148,128,1),(167,105,-1),(188,82,1)):
        board.polygon([(x+dx,y+dy), (x+dx+orientation*35,y+dy-5),
                       (x+dx+orientation*50,y+dy-37), (x+dx+orientation*16,y+dy-29)], stem)
    board.box(x+57,y+200,200,55,fill="#fbf1db",edge="#9d8869",radius=5)
    label(board,number,x+157,y+228,33,INK)


def tickets(board, values, y, *, selected=(), rejected=(), size=120):
    step = size+20
    first = 640 - (len(values)-1)*step/2
    for i,value in enumerate(values):
        x = first+i*step
        colour = GREEN if value in selected else CARD
        board.box(x-size/2,y-35,size,70,fill=colour,edge=LINE,radius=6,stroke=3)
        label(board,value,x,y,33,INK)
        if value in rejected:
            board.line([(x-size*.34,y+22),(x+size*.34,y-20)],"#996055",4)


def draw(board, scene, cue):
    board.label(HEADINGS[scene-1],64,70,40,PAPER,bold=True)
    board.line([(64,124),(1216,124)],LINE,3)
    if scene == 1:
        specimen(board,198,193,"? ? ?")
        label(board,"Specimen number ÷ 8",870,252,38)
        label(board,"Remainder 3 → tray 3",870,360,37,GREEN,cue.reveal("Tray three holds"))
        label(board,"Read the tray before guessing the label.",640,548,34,GOLD,cue.reveal("start a search"))
    elif scene == 2:
        label(board,"Shelf 100 through 140",640,199,38)
        tickets(board,(99,107),318,selected=(107,),rejected=(99,))
        label(board,"104 + 3 = 107",640,440,43,GREEN,cue.reveal("Move three places"))
        label(board,"107 − 8 = 99 is outside.",640,545,33,GOLD,cue.reveal("outside the shelf"))
    elif scene == 3:
        tickets(board,(107,115,123,131,139),301)
        label(board,"One tray step adds eight.",640,430,39,GREEN,cue.reveal("Adding eight"))
        label(board,"Next: 147, beyond this shelf",640,536,33,GOLD,cue.reveal("exactly eight"))
    elif scene == 4:
        specimen(board,178,188,"3 ? ?")
        label(board,"Shelf 320–370   •   Tray 3",876,243,36,GREEN)
        label(board,"Tens digit = 2 × units digit",874,351,31,GOLD,cue.reveal("tens digit is twice"))
        label(board,"First tray label: 320 + 3",865,452,32,PAPER,cue.reveal("then add three"))
    elif scene == 5:
        values=(323,331,339,347,355,363)
        solved=cue.reveal("Only the last one")>.15
        tickets(board,values,296,selected=(363,) if solved else (),rejected=values[:-1] if solved else ())
        label(board,"363 has tens digit 6 and units digit 3.",640,430,36,GREEN,cue.reveal("tens digit is six"))
        label(board,"Next tray label: 371. The shelf ends at 370.",640,540,32,GOLD,cue.reveal("already past the shelf"))
    elif scene == 6:
        specimen(board,137,190,"4  T  U")
        specimen(board,828,190,"4  U  T")
        board.arrow((494,326),(787,326),GOLD,cue.reveal("in reverse order"),5)
        label(board,"original",292,506,32)
        label(board,"copy",985,506,32)
        label(board,"18 less",641,375,33,RED,cue.reveal("eighteen smaller"))
    elif scene == 7:
        label(board,"Original − copy = 9 × (tens − units)",640,209,39)
        label(board,"18 ÷ 9 = 2",640,302,42,GREEN,cue.reveal("Eighteen divided by nine"))
        tickets(board,("20","31","42","53","64","75","86","97"),423,size=99)
        label(board,"Each ending has tens digit two greater than units.",640,547,31,GOLD,cue.reveal("exceeds the units digit"))
    else:
        values=(420,431,442,453,464,475,486,497)
        tickets(board,values,254,selected=(475,) if cue.reveal("Only four hundred")>.1 else (),size=99)
        for i,value in enumerate(values):
            x=640-(len(values)-1)*119/2+i*119
            colour=GREEN if value%8==3 else PAPER
            label(board,f"r {value%8}",x,342,29,colour,cue.reveal("Their remainders"))
        label(board,"475 = 8 × 59 + 3",640,459,40,GREEN,cue.reveal("belongs in tray three"))
        label(board,"475 − 457 = 18",640,558,38,GOLD,cue.reveal("eighteen smaller"))


def poster(draw_frame):
    return draw_frame(10,1)
