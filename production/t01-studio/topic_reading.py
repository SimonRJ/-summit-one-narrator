"""Topic film chapter menus and transcripts share the measured narration scene starts."""
from html import escape

# Keys are one-based narration scene numbers, also used in the sound alignment reports.
CHAPTERS = {
    "T01.1": {
        1: "Label packets, counters and loose pieces", 3: "Open Mia’s four packets",
        6: "Add ribbon lengths in centimetres", 7: "Count every nine on pages 95–105",
        9: "Find the pencils that still work",
    },
    "T01.2": {
        1: "Choose a line, table or sketch", 3: "Place posts along a straight fence",
        5: "Join the ends of the fence", 6: "Count Sam once in the queue",
        7: "Compare the price per pencil", 8: "Trace the outside edges of two mats",
        9: "Plant trees at both ends of a path",
    },
    "T01.3": {
        1: "Predict the units and size of an answer", 3: "Estimate seats for 130 students",
        4: "Fill buses in groups of forty", 6: "Show why three buses fall short",
        7: "Count only the completely full buses", 8: "Pack 100 eggs into boxes of twelve",
    },
    "T01.E": {
        1: "Locate the two ends of the ribbon", 3: "Count centimetre gaps from 2 to 9",
        4: "Subtract the starting mark", 5: "Slide both ends back to zero and seven",
        6: "Time a film from 7:15 to 9:05", 8: "Measure a recording across noon",
    },
    "T02.1": {
        1: "Find a quantity one move preserves", 4: "Transfer counters between two piles",
        10: "Add two counters to each pile", 13: "Prove the changes cancel",
        17: "Test two targets from four and nine", 20: "Write an equation for one move",
    },
    "T02.2": {
        1: "Undo the last operation first", 3: "Recover the machine’s input from 23",
        6: "Check the reversed steps forwards", 8: "Rebuild the pile from eight counters",
        12: "Check that each pile contains whole counters", 16: "Trace the route back from 17",
    },
    "T02.3": {
        1: "Swap addition and doubling", 3: "Predict which rule gives more",
        4: "Make two copies of the whole bar", 5: "Pair the matching parts",
        6: "Compare the rules with a negative multiplier", 7: "Decide which steps can swap",
        8: "Compare tripling before and after subtraction",
    },
    "T02.E": {
        1: "Try both rules with one starting number", 2: "Make four copies of the sum",
        4: "Cancel the matching tiles", 5: "Test the gap at zero and at ten",
        6: "Draw the two add-and-scale rules",
    },
    "T03.1": {
        1: "Group seventeen counters in fives", 3: "Mark the four-bead cycle",
        4: "Locate bead 50", 5: "Place bead 48 at remainder zero",
        6: "Subtract two numbers with the same remainder", 7: "Filter a list by two remainders",
        8: "Move 100 days beyond Tuesday",
    },
    "T03.2": {
        1: "Compare the four- and six-second lights", 3: "Start both lights at zero",
        4: "Find the gap between shared flashes", 5: "Give the second light a two-second delay",
        6: "Use parity to rule out a meeting", 7: "Find the next shared bus departure",
    },
    "T03.3": {
        1: "Fit four counters into three boxes", 3: "Delay a matching pair of socks",
        5: "Sort four numbers into remainder boxes", 6: "Pair the numbers that sum to eleven",
        7: "Force two birthdays into one month",
    },
    "T03.E": {
        1: "Find a multiple-of-three difference", 2: "Give each number a remainder box",
        4: "Subtract numbers from the same box", 5: "Test four numbers and then three",
        6: "Find the guarantee for divisor ten",
    },
}


def reading_sections(lesson, starts, paragraphs):
    headings = CHAPTERS[lesson]
    if len(starts) != len(paragraphs) or max(headings) > len(starts) or starts[0] != 0:
        raise ValueError(f"{lesson}: chapter map no longer matches the recorded narration")
    buttons, transcript = [], []
    for number, (start, paragraph) in enumerate(zip(starts, paragraphs), 1):
        if number in headings:
            seconds = int(start + 0.5)
            clock = f"{seconds // 60}:{seconds % 60:02}"
            title = escape(headings[number])
            buttons.append(
                f'<button type="button" data-time="{start:.3f}">'
                f'<span class="chapter-clock">{clock}</span> {title}</button>'
            )
            transcript.append(f'<h2><span class="chapter-clock">{clock}</span> {title}</h2>')
        transcript.append(f'<p>{escape(paragraph)}</p>')
    return "\n".join(buttons), "\n".join(transcript)
