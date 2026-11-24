"""Render the four changed learner journeys with the original welcome film's artwork."""
import importlib.util
from pathlib import Path
from PIL import Image

source = Path(__file__).resolve().parents[1] / 'amc-introduction' / 'render.py'
spec = importlib.util.spec_from_file_location("welcome_art", source)
art = importlib.util.module_from_spec(spec)
spec.loader.exec_module(art)
original = art.content


def learner_route(index, time):
    if index not in (13, 14, 15, 16):
        return original(index, time)
    image = Image.new('RGB', (art.W, art.H), art.BLACK)

    def on(phrase):
        return art.anim(time, art.cue(index, phrase), .55)

    def text(label, x, y, size=30, color=art.WHITE, opacity=1):
        art.text(image, label, x, y, size, color, a=opacity)

    if index == 13:
        art.heading(image, 'Read the example', 'Your lesson · Read')
        # Leave the working area empty until the separate reveals are spoken.
        art.rect(image, 640, 349, 800, 320, c=art.DARK, outline=art.CYAN)
        text('A small example', 640, 235, 30)
        text('Try it on paper', 640, 310, 34, art.GOLD, on('on paper'))
        art.line(image, [(332,369), (948,369)], art.DIM, 2)
        text('Show the first step', 640, 415, 30, art.CYAN, on('reveal the first step'))
        text('Show all steps', 640, 474, 30, art.CYAN, on('uncover the rest'))
    elif index == 14:
        art.heading(image, 'Watch one rectangle take shape', 'Your lesson · Watch')
        x, y, cell = 208, 224, 88
        art.grid(image, x, y, 4, 3, cell)
        h, v = on('two horizontal boundaries'), on('two vertical boundaries')
        for row in (0,2):
            art.line(image, [(x-14,y+cell*row),(x+4*cell+14,y+cell*row)], art.GOLD, 5,h)
        for col in (1,4):
            art.line(image, [(x+cell*col,y-14),(x+cell*col,y+3*cell+14)], art.CYAN, 5,v)
        for row in (0,2):
            for col in (1,4):
                art.dot(image,x+cell*col,y+cell*row,9,art.WHITE,on('Their intersections'))
        text('2 horizontal boundaries', 927, 270, 30, art.GOLD, h)
        text('2 vertical boundaries', 927, 350, 30, art.CYAN, v)
        text('1 rectangle', 927, 437, 38, art.WHITE, on('one rectangle'))
        text('Pause and predict', 640, 574, 29, art.GOLD, on('Pause to predict'))
    elif index == 15:
        art.heading(image, 'Check the first step that changed', 'Your lesson · Practise')
        art.rect(image,349,311,438,186,c=art.DARK,outline=art.CYAN)
        text('Final answer',349,270,30)
        text('Check answer',349,351,33,art.GOLD,on('Check it'))
        art.arrow(image,(600,312),(677,312),art.CYAN,on('compare your working'))
        art.rect(image,927,311,438,186,c=art.DARK,outline=art.GOLD,a=on('compare your working'))
        text('Your working',927,270,30,art.WHITE,on('compare your working'))
        text('Worked solution',927,351,30,art.GOLD,on('with the solution'))
        text('Used help? Record it.',640,469,29,art.CYAN,on('record that too'))
        text('Which step would you change?',640,563,31,art.WHITE,on('For a missed answer'))
    else:
        art.heading(image, 'Two clocks for AMC practice', 'Test Centre')
        left=on('Part A');right=on('Part B')
        art.rect(image,350,323,485,324,c=art.DARK,outline=art.CYAN,a=left)
        art.rect(image,930,323,485,324,c=art.DARK,outline=art.GOLD,a=right)
        text('Part A · Questions 1–20',350,211,29,art.CYAN,left)
        text('Counts up from 0:00',350,288,31,art.WHITE,on('clock counts up'))
        text('Target: 20 out of 20',350,359,30,art.GOLD,on('every answer correct'))
        text('in 20 minutes or less',350,415,29,art.GOLD,on('twenty minutes or less'))
        text('Part B · Questions 21–30',930,211,29,art.GOLD,right)
        text('40-minute limit',930,322,36,art.WHITE,on('forty-minute limit'))
        text('After either part, open your report',640,558,29,art.CYAN,on('open your report'))
    return image


if __name__ == '__main__':
    art.content=learner_route
    art.main()
