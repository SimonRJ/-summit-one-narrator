"""Truth values, constraints and complete arguments."""

from itertools import permutations, product

from story import Example, Topic, chain, grid, say, spoken_list, table, tiles


def truth_liars(lesson):
    v=lesson.visit
    a,b,c,d=(("Ava","Ben","Chen","Dara"),("Iris","Kai","Lia","Mo"),
             ("Noor","Oli","Pia","Raj"),("Sam","Tess","Uri","Val"),("Wren","Xia","Yara","Zac"))[v]
    first=v%2==1
    next_=v%3!=1
    third=v<3
    relation=first==next_
    different=(v%2==0)
    fourth=relation!=different
    truth_c=fourth==third
    truth_b=truth_c==next_
    truth_a=truth_b==first
    labels={True:"truthful",False:"a liar"}
    mark=lambda value: "T" if value else "L"
    assert [(aa,bb,cc,dd) for aa,bb,cc,dd in product((False,True),repeat=4)
        if aa==(bb==first) and bb==(cc==next_) and cc==(dd==third)
        and dd==((aa!=cc)==different)]==[(truth_a,truth_b,truth_c,fourth)]
    comparison="different types" if different else "the same type"
    return Topic(
        (
            ("In a truth-teller puzzle, a person's type agrees with the truth of their statement. A truth-teller's statement is true, and a liar's statement is false.", "Type agrees with the truth of the statement."),
            ("Turn each sentence into a short condition. Then combine the conditions before assigning everyone's type.", "Link the statements and test a complete case."),
        ),
        (
            ("AMC logic practice can ask who made a correct statement or which claims can all hold at once. Keep a small table of cases.", "AMC Upper Primary · test consistent claims"),
            ("A Rossmoyne style argument may need to rule out every alternative. Use a contradiction if some proposed assignment cannot fit its own statements.", "Rossmoyne-style · rule out impossible cases"),
        ),
        (
            Example("Test a statement about yourself", (
                (f"Everyone in a puzzle is either always truthful or always lies. {a} says: I am a liar. Can {a} say that consistently?", f"{a}: I am a liar."),
                ("Check what would happen under each of the two possible types.", "Test both types."),
            ), (
                (f"If {a} is truthful, the claim of being a liar is false. That type cannot make the statement.", "Truthful person → sentence false"),
                (f"If {a} is a liar, the claim is true. That also contradicts the type. Neither case works.", "Liar → sentence true; impossible"),
            ), table(("Possible type","Sentence"),("Truthful","False"),("Liar","True"))),
            Example("Use a statement about both people", (
                (f"Two people are each truthful or a liar. {b} says that both of them are liars. Work out the types of both people.", f"{b}: We are both liars."),
                ("The second person makes no statement. Can the first claim its own type consistently?", "Which types are forced?"),
            ), (
                (f"If {b} were truthful, both would be liars by the statement. That contradicts the idea that {b} is truthful.", f"{b} must be a liar."),
                (f"The claim must be false. Since {b} really is a liar, the other person has to be truthful to make the pair different.", "The other person must be truthful."),
            ), tiles(b,"Other"),worked_art=tiles("Liar","Truthful",highlight=(1,))),
            Example("Solve a chain of four statements", (
                (f"{a} says {b} is {labels[first]}. {b} says {c} is {labels[next_]}.", f"{a} → {b}: {labels[first]}. {b} → {c}: {labels[next_]}."),
                (f"{c} says {d} is {labels[third]}.", f"{c} → {d}: {labels[third]}."),
                (f"{d} says that {a} and {c} are {comparison}. Everyone is either always truthful or always lies. Who is truthful?", f"{d}: {a} and {c} are {comparison}."),
            ), (
                (f"A claim that someone is truthful makes the two types match. A claim that they lie makes the types opposite. Follow the first two links from {a} to {c}.", "Claim truthful: same type. Claim liar: opposite."),
                (f"Those two links make {a} and {c} {'the same type' if relation else 'opposite types'}. This determines the final statement without guessing any individual type.", f"{a} and {c}: {'same' if relation else 'different'}"),
                (f"The statement by {d} is {'true' if fourth else 'false'}. So {d} is {labels[fourth]}.", f"{d}: {mark(fourth)}"),
            ), chain(a,b,c,d), proof=(
                (f"Now use the statement about {d} to identify {c}, which is {labels[truth_c]}. Then {b} is {labels[truth_b]} and {a} is {labels[truth_a]}.", f"{a} {mark(truth_a)}, {b} {mark(truth_b)}, {c} {mark(truth_c)}, {d} {mark(fourth)}"),
                ("Check each sentence with that assignment. The last statement fixed one type, and each link then forced the next, proving there is only one assignment.", "One forced type unlocks the entire chain."),
            ), proof_art=table((a,b,c,d),tuple(mark(t) for t in (truth_a,truth_b,truth_c,fourth)))),
        ),
        (
            ("A liar's entire stated sentence must be false. When the sentence says both people lie, one truthful person is enough to make it false.", "Negate each part separately", "Negate the whole sentence"),
            ("Checking one person's statement is a start. All statements must agree with the proposed types at the same time.", "Keep an assignment after one check", "Test every statement at the end"),
        ),
        (
            ("Mark each statement as a condition. Decide whether it gives same types, opposite types, or another relationship.", "Write the relationships", "Make the truth rule explicit."),
            ("Look for a type forced by several conditions. Then check the remaining assignments against all the statements.", "Prove a unique assignment", "Show why no alternative can fit."),
        ), cover=chain("Statement","True or false","Person's type"),
    )
