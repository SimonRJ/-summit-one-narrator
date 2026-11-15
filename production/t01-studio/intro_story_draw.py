"""Render speech-synchronised formula cards, diagrams and comparisons."""

from functools import lru_cache
import json
from math import cos, pi, sin

from intro_art import card, header, mistakes, steps
from intro_cubes import solids
from stage import BG, BLUE, GOLD, MINT, MUTED, PANEL, RIM, ROOT, WHITE, blend, mix
from studio_diagrams import fit, wrapped_text


COLOURS = (BLUE, GOLD, MINT, "#c2b0f5")
LEVELS = {"INTRO": "The idea", "EXAM": "Where it shows up", "BASIC": "Basic example",
          "MEDIUM": "Medium example", "HARD": "Exam-style challenge"}


def tile_diagram(stage, spec, box, p, flow=False):
    x, y, w, h = box
    values = spec["values"]
    per_row = min(6, len(values))
    row_count = (len(values) + per_row - 1) // per_row
    for row in range(row_count):
        line = values[row * per_row: (row + 1) * per_row]
        spacing = min(144, w / len(line))
        pos = x + (w - spacing * (len(line) - 1)) / 2
        for i, value in enumerate(line):
            opacity = min(1, max(0, 1.25 * p - .045 * (row*per_row + i)))
            index = row * per_row + i
            colours = spec.get("colours")
            colour = (colours[index] if colours else GOLD if index in spec.get("highlight", ())
                      else COLOURS[row % len(COLOURS)])
            cy = y + (row+.5)*h/row_count
            card(stage, pos + i*spacing, cy, value, colour, w=spacing*(.71 if flow else .87),
                 h=min(95,h/row_count*.68), size=53, opacity=opacity)
            if flow and i+1<len(line):
                stage.arrow((pos+i*spacing+.37*spacing,cy), (pos+i*spacing+.62*spacing,cy), MINT, opacity, 3)


def table_diagram(stage, spec, box, p, boxed=False):
    x, y, w, h = box
    rows = spec["rows"]
    columns = max(len(row) for row in rows)
    cell = min(w/columns, (h-5)/len(rows) * (1 if boxed else 1.6), 105 if boxed else 160)
    if boxed:
        height = cell
    else:
        height = min(h/len(rows), 58)
    left = x + (w - cell * columns) / 2
    top = y + (h - height * len(rows)) / 2
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            ordering = len(rows)-1-i if spec.get("bottom_up") else i
            delay = .48 * (ordering+j/columns) / max(1,len(rows))
            a = min(1, max(0, (p-delay)/(1-delay)))
            highlighted = [i,j] in spec.get("highlight", ()) or (i,j) in spec.get("highlight", ())
            colour = GOLD if highlighted else BLUE if i == 0 and not boxed else WHITE
            fill = "#263643" if highlighted else PANEL if boxed or i == 0 else None
            stage.box(left+j*cell+1, top+i*height+1, cell-3, height-3, radius=7,
                      fill=fill, edge=RIM if boxed or i == 0 else None, opacity=a)
            xx,yy=left+(j+.5)*cell,top+(i+.5)*height
            if i == 0 and not boxed:
                wrapped_text(stage,value,xx,yy,min(24,round(.38*height)),cell-8,colour,a,bold=True)
            else:
                fit(stage,value,xx,yy,min(43,round(.54*height)),cell-10,colour,a)


def bar_diagram(stage, spec, box, p):
    x,y,w,h = box
    rows = spec["rows"]
    tall = min(54, h/len(rows)*.53)
    widest = max(sum(piece[0] for piece in parts) for _,parts in rows)
    for i, (title, parts) in enumerate(rows):
        cy = y+(i+.5)*h/len(rows)+15
        a = min(1,max(0,1.4*p-.13*i))
        fit(stage, title, x+w/2, cy-tall/2-27, 26, w, MUTED, a)
        left = x + 8
        for j, (width, value) in enumerate(parts):
            segment = (w-16) * width/widest
            colour = COLOURS[j%4]
            stage.box(left, cy-tall/2, max(2,segment-2), tall, radius=8,
                      fill=blend(PANEL,colour,.24), edge=colour, opacity=a)
            if segment >= 39:
                fit(stage, str(value), left+segment/2, cy, 30, segment-7, colour, a)
            left += segment


def geometry_diagram(stage, spec, box, p):
    x,y,w,h = box
    nodes = spec["nodes"]
    xy = [point[:2] for point in nodes]
    lo = min(a for a,_ in xy), min(b for _,b in xy)
    hi = max(a for a,_ in xy), max(b for _,b in xy)
    xs = (w - 80)/max(.5,hi[0]-lo[0])
    ys = (h - 64)/max(.5,hi[1]-lo[1])
    if spec.get("keep_aspect", True):
        xs = ys = min(xs,ys)
    xx = x+(w-(hi[0]-lo[0])*xs)/2
    yy = y+(h+(hi[1]-lo[1])*ys)/2

    def as_point(a,b):
        return xx+(a-lo[0])*xs, yy-(b-lo[1])*ys

    coords = [as_point(a,b) for a,b in xy]
    for number, indexes in enumerate(spec.get("polygons", ())):
        colour = COLOURS[number%4]
        poly = [coords[i] for i in indexes]
        stage.draw.polygon([(stage.px(a),stage.px(b)) for a,b in poly],
                           fill=blend(BG,colour,p*.23))
    for a,b,colour_index in spec["segments"]:
        start,end = coords[a],coords[b]
        stage.line((start,(mix(start[0],end[0],p),mix(start[1],end[1],p))),
                   COLOURS[colour_index%4],3,p)
    for i, (_,_,label) in enumerate(nodes):
        if label:
            a,b=coords[i]
            stage.dot(a,b,4,WHITE,p)
            fit(stage, str(label),a+13,b-20,31,92,WHITE,p)
    for a,b,label,colour_index in spec.get("labels", ()):
        ax,ay=as_point(a,b)
        fit(stage,str(label),ax,ay,30,215,COLOURS[colour_index%4],p)


def cube_diagram(stage,spec,box,p):
    x,y,w,h=box
    paint_legend = "painted" in spec
    if paint_legend:
        h -= 45
    cells=frozenset(tuple(cell) for cell in spec["cells"])
    width=max(x+1 for x,_,_ in cells)
    depth=max(y+1 for _,y,_ in cells)
    levels=max(z+1 for _,_,z in cells)
    spread=spec.get("spread",0)*p
    zoom=min((w-20)/(39*(width+depth)), (h-24-spread*(levels-1))/(20*(width+depth)+48*levels))
    anchor_x=x+w/2-(width-depth)*39*zoom/2
    anchor_y=y+h/2+(48*levels*zoom+spread*(levels-1)-20*(width+depth)*zoom)/2
    painted = frozenset(map(tuple, spec["painted"])) if "painted" in spec else None
    solids(stage,cells,anchor_x,anchor_y,zoom=zoom,spread=spread,opacity=p,painted=painted)
    if paint_legend:
        fit(stage,"Painted surface",x+w*.28,y+h+24,23,w*.44,GOLD,p)
        fit(stage,"Unpainted surface",x+w*.73,y+h+24,23,w*.44,BLUE,p)


def spinner_diagram(stage, spec, box, p):
    if p <= 0:
        return
    x,y,w,h=box
    cx,cy=x+w/2,y+h/2
    radius=min(w,h)*.39
    bounds=tuple(map(stage.px,(cx-radius,cy-radius,cx+radius,cy+radius)))
    count=spec["sectors"]
    split=spec["green"]
    angle=360/count
    for i in range(count):
        opacity=min(1,max(0,p*1.45-.45*i/count))
        colour=MINT if i<split else BLUE
        stage.draw.pieslice(bounds,start=-90+i*angle,end=-90+(i+1)*angle,
                            fill=blend(BG,colour,opacity*.72),outline=blend(BG,RIM,opacity),
                            width=max(1,stage.px(2)))
    theta=(-.5+1.45*p)*pi
    pointer=(cx+.57*radius*cos(theta),cy+.57*radius*sin(theta))
    stage.arrow((cx,cy),pointer,WHITE,p,6)
    stage.dot(cx,cy,7,WHITE,p)


def venn_diagram(stage,spec,box,p):
    x,y,w,h=box
    rad=min(w*.29,h*.37)
    cx,cy=x+w/2,y+h/2
    gap=.55*rad
    stage.dot(cx-gap,cy,rad,blend(PANEL,BLUE,.25),p)
    stage.dot(cx+gap,cy,rad,blend(PANEL,GOLD,.29),p)
    left,right,shared=spec["values"]
    for pos,value,colour in ((cx-rad,left,BLUE),(cx+rad,right,GOLD),(cx,shared,MINT)):
        fit(stage,value,pos,cy,47,.85*rad,colour,p)


ARTISTS = {
    "tiles": tile_diagram,
    "chain": lambda stage,spec,box,p: tile_diagram(stage,spec,box,p,flow=True),
    "grid": lambda stage,spec,box,p: table_diagram(stage,spec,box,p,boxed=True),
    "table": table_diagram, "bars": bar_diagram, "geometry": geometry_diagram,
    "cubes": cube_diagram, "venn": venn_diagram, "spinner": spinner_diagram,
}


def draw_scene(stage, moment, scene, lesson, section):
    slot = lesson["course_slot"]
    phase = scene["stage"]
    heading = scene["heading"]
    beats = scene["beats"]
    if phase == "MISTAKES":
        mistakes(stage,moment,slot,heading,zip(
            (beat["cue"] for beat in beats), (beat["line"] for beat in beats), scene["pairs"],
        ))
        return
    if phase == "RECAP":
        steps(stage,moment,slot,heading,zip(
            (beat["cue"] for beat in beats), (beat["line"] for beat in beats), scene["pairs"],
        ))
        return
    header(stage,slot,section,heading)
    art = scene.get("art")
    if art:
        build_time=.9
        if art.get("bottom_up"):
            build_time=max(.9,moment.at(beats[-1]["cue"])-moment.at(beats[0]["cue"]))
        ARTISTS[art["kind"]](stage,art,(80,203,510,382),moment.reveal(beats[0]["cue"],build_time))
    first = 225 if len(beats) >= 4 else 260
    spacing = min(132, (565-first)/max(1,len(beats)-1))
    for i, beat in enumerate(beats):
        p = moment.reveal(beat["cue"],.68)
        y = first + i*spacing + (1-p)*13
        x = 906 if art else 640
        max_width = 524 if art else 1000
        colour = MINT if i == len(beats)-1 and phase in ("BASIC","MEDIUM","HARD") else WHITE
        stage.box(x-max_width/2-18,y-48,max_width+36,96,radius=20,fill=PANEL,
                  edge=blend(RIM,colour,.18),opacity=p)
        wrapped_text(stage,beat["line"],x,y,39 if art else 42,max_width-14,colour,p,
                bold=phase in ("BASIC","MEDIUM","HARD"))


@lru_cache(maxsize=8)
def narrative(lesson):
    return json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())


def movie(lesson):
    """Create one callable per scene from the compiled narration and illustration plan."""
    data = narrative(lesson)
    stages = [s["stage"] for s in data["scenes"]]
    assert stages[:7] == ["INTRO", "EXAM", "PUZZLE", "BASIC", "PUZZLE", "MEDIUM", "PUZZLE"]
    assert stages[-2:] == ["MISTAKES", "RECAP"]
    levels = ["Basic example", "Medium example", "Exam-style challenge"]
    storyboard = []
    for shot in data["scenes"]:
        phase = shot["stage"]
        section = levels.pop(0) if phase == "PUZZLE" else LEVELS.get(phase, "")
        storyboard.append(lambda stage, moment, shot=shot, section=section:
                          draw_scene(stage,moment,shot,data,section))
    end = len(storyboard)
    return tuple(storyboard), (
        (1,"The technique"), (2,"Where it shows up"), (3,"Basic example"), (5,"Medium example"),
        (7,"Exam-style challenge"), (end-1,"Common mistakes"), (end,"Exam checklist"),
    )
