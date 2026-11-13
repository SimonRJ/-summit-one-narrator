"""Deep, reproducible content and mathematical consistency scan.

Validates all 566 authored standard lesson problems generated from the
canonical 372-session map. It is separate from visual/manual AMC fidelity review.
Run: python tools/content/audit_all_lessons.py
"""
import json
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from build_original_lessons import build,capstone
ROOT=Path(__file__).resolve().parents[2]
CAPSTONE={361:"COUNT-06",362:"ALG-03",365:"GEO-02",366:"SPATIAL-01",367:"DIV-04",368:"RATE-03",370:"GEO-05"}

def map_course():
    sessions=json.loads((ROOT/"data/sessions-372.json").read_text())["sessions"]
    taxonomy=json.loads((ROOT/"data/taxonomy-52.json").read_text())
    by_name={s["name"]:s["id"] for c in taxonomy["categories"] for s in c["subskills"]}
    mapping=[]
    for s in sessions:
        if s["type"]!="LESSON":continue
        k=CAPSTONE.get(s["slot"],by_name.get(s["focus"]))
        assert k,(s["slot"],s["focus"],"Missing skill mapping")
        mapping.append({"slot":s["slot"],"skill":k})
    assert len(mapping)==283,(len(mapping),"expected 283 lessons")
    return mapping

def numeric_skeleton(s):
    return re.sub(r"[0-9]+(?:[.,][0-9]+)?","N",s.lower()).replace("–","-")

def check_problems(rows,mapping):
    errors=[];warnings=[]
    ids=set();templates=defaultdict(list);seen=set();counts=Counter()
    titles=Counter()
    mapping_slots={s["slot"] for s in mapping}
    for row in rows:
        pid=row["id"];role=pid[-1];skill=row["category"];text=row["prompt"];sol=row["solution_text"]
        counts[role]+=1
        if pid in ids:errors.append(f"{pid} duplicate ID")
        ids.add(pid)
        if int(pid[1:4]) not in mapping_slots:errors.append(f"{pid} missing canonical lesson")
        if not text.strip().endswith("?"):errors.append(f"{pid} question does not end in a clear ask")
        if text in seen:errors.append(f"{pid} exact duplicate question")
        seen.add(text)
        if text.count("?")>2: warnings.append(f"{pid} too many question marks")
        if len(text)<35 or len(text)>1150:errors.append(f"{pid} unexpected length: {len(text)}")
        if re.search(r"\b(?:a meter should add|robot spends|odometer log writes|badge machine triples|a machine processes .+ tokens|in your working|transfer reflection)\b",text,re.I):
            errors.append(f"{pid} old or artificial problem context")
        if re.search(r"\b(?:in your working|explain your method|show your reasoning|prove your answer)\b",text,re.I):
            errors.append(f"{pid} requires typed reasoning")
        if row["title"] in ("A new setting","Workshop problem","Practice problem","Transfer challenge"):
            errors.append(f"{pid} generic title")
        titles[row["title"]]+=1
        if not sol.startswith("Recognise:") and "Final answer:" not in sol:
            errors.append(f"{pid} missing final answer")
        if "Final answer:" not in sol:errors.append(f"{pid} absent final-answer line")
        else:
            last=sol.rsplit("Final answer:",1)[1].strip().rstrip(".")
            if not last:errors.append(f"{pid} blank final answer")
            elif str(row["answer"]) not in last and ("$"+str(row["answer"])) not in last:
                errors.append(f"{pid} final answer {last!r} differs from key {row['answer']!r}")
        if re.search(r"(?:Each of the x cross-sections|width 2x\+2|supplied by the generator|adjusted even parameter)",sol):
            errors.append(f"{pid} source-code placeholder in solution")
        if "<svg" in text and "</svg>" not in text:errors.append(f"{pid} unclosed diagram markup")
        templates[(skill,role)].append(numeric_skeleton(text))
    assert counts["T"]==283 and counts["X"]==283,counts
    for (skill,role),variants in templates.items():
        if len(variants)>2 and len(set(variants))==1:
            warnings.append(f"{skill}/{role}: {len(variants)} revisits share identical mathematical setup")
    return errors,warnings,dict(counts),templates,titles

def main():
    mapping=map_course()
    with tempfile.TemporaryDirectory() as t:
        build(mapping,Path(t))
        questions=json.loads((Path(t)/"original-problems.json").read_text())
        assert len(questions)==566,len(questions)
        errors,warnings,counts,templates,titles=check_problems(questions,mapping)
    print(json.dumps({"total_questions":len(questions),
      "techniques":len(set(x["category"] for x in questions)),
      "lesson_sessions":len(mapping),"role_counts":counts,
      "numeric_structures":len(set(k for vars in templates.values() for k in vars)),
      "distinct_titles":len(titles),
      "structure_warnings":len(warnings),
      "examples_needing_diversification":warnings[:22],
      "errors":errors[:45]},indent=2))
    if errors:
        raise AssertionError(f"{len(errors)} critical question and solution defects")
    print("PASS: all 566 generated lessons have consistent IDs, answer explanations, natural problem context, and fully formed single questions")
if __name__=="__main__":main()
