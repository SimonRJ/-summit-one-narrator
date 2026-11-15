"""Counting choices, restrictions and events."""

from itertools import permutations
from math import comb, factorial

from story import Example, Topic, bars, chain, grid, say, spoken_list, table, tiles, venn


def restricted_arrangements(lesson):
    v=lesson.visit
    labels=("badges","name cards","keys","picture cards","pennants","locks")
    item=labels[v]
    count=5+v%3
    names="ABCDEFG"[:count]
    close=2*factorial(count-1)
    both=4*factorial(count-2)
    one=2*(close-both)
    neither=factorial(count)-2*close+both
    only_one=v%2==1
    choices=one if only_one else neither
    assert choices==sum(
        (abs(line.index("A")-line.index("B"))==1)+(abs(line.index("C")-line.index("D"))==1)==int(only_one)
        for line in permutations(names)
    )
    medium_n=4+v%3
    return Topic(
        (
            ("An arrangement depends on order. When two named objects must stay next to each other, treat them as one movable block first.", "Replace a required pair by one movable block."),
            ("Once you place the block, restore the allowed orders inside it. That internal choice is part of the count.", "Restore the orders inside each block."),
        ),
        (
            ("In AMC practice, neighbour rules may appear in seating plans, passwords, queues or objects on a shelf. Start with the rule that restricts the most.", "AMC Upper Primary · next to or apart"),
            ("Rossmoyne style counting can combine two neighbour conditions. A block count and an overlap check prevent double counting.", "Rossmoyne-style · two conditions at once"),
        ),
        (
            Example("See how order changes the result", (
                (f"Line up three distinct {item} named A, B and C. How many different orders can you make?", "Line up A, B and C."),
                ("Keep track of which objects are still free after you choose the first one.", "Count the choices at each position."),
            ), (
                ("There are three choices for the first position. Each first choice leaves two for the second and then one for the last.", "3 choices, then 2, then 1"),
                ("Multiply three times two times one. Each full set of choices produces a different line. There are six orders.", "3 × 2 × 1 = 6 orders"),
            ), tiles("A","B","C")),
            Example("Treat neighbours as one block", (
                (f"There are {say(medium_n)} distinct {item} in a row. A and B must be adjacent. How many arrangements are possible?", f"{medium_n} in a row; A and B must be together."),
                ("A might sit before or after B. Take both possibilities into account.", "Count the block and its internal orders."),
            ), (
                (f"Compress A and B into one block. Now there are just {say(medium_n-1)} objects to arrange.", f"Block AB plus {medium_n-2} single objects"),
                (f"Those objects can be ordered in {say(factorial(medium_n-1))} ways. In each arrangement the pair can be A B or B A.", f"{medium_n-1}! = {factorial(medium_n-1)} block orders"),
                (f"Multiply by two, giving {say(2*factorial(medium_n-1))} original arrangements. The block can be identified in each one.", f"{factorial(medium_n-1)} × 2 = {2*factorial(medium_n-1)}"),
            ), tiles(*("AB",*names[2:medium_n]))),
            Example("Handle two neighbour rules", (
                (f"Line up {say(count)} distinct {item}, including A, B, C and D. Consider two pairs: A with B, and C with D.", f"{count} distinct objects; test pairs AB and CD."),
                ((f"How many orders make exactly one of those pairs adjacent?"
                   if only_one else "How many orders leave both of those pairs nonadjacent?")+
                 " Draw the two possible adjacency conditions as overlapping sets.", "Exactly one pair adjacent" if only_one else "Neither pair adjacent"),
            ), (
                (f"There are {say(factorial(count))} total orders. The number making A and B adjacent is twice {say(factorial(count-1))}, or {say(close)}. The other pair has the same count.", f"Each single-pair count = 2 × {count-1}! = {close}"),
                (f"If both pairs are adjacent, arrange {say(count-2)} objects with two blocks. Each block has two internal orders, giving {say(both)} shared arrangements.", f"Overlap = 4 × {count-2}! = {both}"),
                ("The shared arrangements have been counted in both single-pair totals. Decide whether you need to remove the overlap once or twice.", "Use the overlap to correct the double count."),
            ), tiles("AB","CD",*names[4:]), worked_art=venn(close-both,close-both,both),proof=(
                ((f"In each single-pair total, remove the {say(both)} orders where both pairs are adjacent. Add the two remaining, disjoint counts."
                  if only_one else f"The number with at least one pair adjacent is the two individual counts minus the shared {say(both)}. Remove those from the grand total."),
                 f"2 × ({close} − {both}) = {choices}" if only_one else f"{factorial(count)} − ({close} + {close} − {both}) = {choices}"),
                (f"The answer is {say(choices)}. Check that your accepted arrangements satisfy the exact condition about how many adjacent pairs there are.", f"{choices} valid orders"),
            ),proof_art=venn(close-both,close-both,both)),
        ),
        (
            ("When a required adjacent pair is one block, count both internal orders if the problem allows them. The block is still a group of two distinct objects.", "Treat a pair as one permanently ordered object", "Multiply by the allowed orders inside it"),
            ("A pair that is forbidden to sit together is often easiest to count as a complement. The overlap of two forbidden conditions can be counted twice.", "Subtract both forbidden lists unchanged", "Add the shared orders back once"),
        ),
        (
            ("Mark whether order matters. For a required pair, draw a bracket around the neighbours and count what can move.", "Create a block", "An adjacent pair moves as one unit."),
            ("Work out the order inside each block. For multiple restrictions, choose disjoint cases or show the overlap explicitly.", "Check the overlap", "Give each allowed arrangement one count."),
        ), cover=tiles("A B","C","D","E"),
    )
