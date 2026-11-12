"""Build teaching metadata from the private, authentic 2007–2025 inventory.

Input contains source text/scans and is deliberately not committed. Output rows
contain no answers; upload these to question metadata. Public output is aggregate
only, so unopened papers remain useful independent assessments.
These are editorial teaching labels, not AMT labels or predictions.
"""
import json,re,sys
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROFILES=json.loads((ROOT/'data/recognition-profiles.json').read_text())
VERSION='recognition-20261113'

# Corrections after reading source problems and diagram contact sheets. The skill
# names describe the lesson to revisit; strategy can be more precise than a name.
CORRECTIONS={
 2008:{4:'FRAC-01',7:'FRAC-01',20:'FRAC-01'},
 2009:{12:'COUNT-06',20:'ALG-05',26:'GEO-02'},
 2010:{27:'GEO-05',30:'COUNT-06'},
 2011:{14:'SPATIAL-02',17:'DIV-01',18:'SOLID-03',22:'SPATIAL-04'},
 2012:{7:'SPATIAL-03',9:'COUNT-04',23:'LOGIC-02',29:'COUNT-06'},
 2013:{18:'SOLID-03',25:'GEO-05',26:'GEO-05'},
 2014:{5:'DIG-01',10:'DIG-01'},
 2015:{16:'SEQ-04',26:'GEO-05',27:'GEO-05'},
 2016:{3:'SPATIAL-02',17:'GEO-03'},
 2017:{5:'GEO-03',20:'GEO-02',22:'COUNT-05',28:'GEO-05'},
 2018:{22:'SEQ-04',25:'DIG-05',27:'LOGIC-02'},
 2019:{5:'SPATIAL-02',8:'RATE-01',16:'GEO-02'},
 2020:{25:'SOLID-03'},
 2021:{17:'FRAC-04',22:'SOLID-03',23:'GEO-04'},
 2022:{19:'ALG-01',20:'DATA-03',21:'FRAC-04',27:'SPATIAL-02'},
 2023:{4:'FRAC-01',8:'FRAC-01',28:'GEO-05'},
 2024:{26:'GEO-05',27:'GEO-05'},
 2025:{10:'SPATIAL-02',26:'DIV-03'}
}
# Different methods can solve one problem. These are useful primary routes,
# never a claim that an alternative valid method is wrong.
SPECIAL={
 (2007,4):('Apply operation order',[], 'Do multiplication and division before addition and subtraction.'),
 (2007,20):('Optimise digit positions',['DIG-02'],'Place values matter more than making one factor as large as possible.'),
 (2007,29):('Count placements by orientation',['COUNT-06','SPATIAL-02'],'Include distinct rotations and reflections as the question specifies.'),
 (2008,11):('Build the worst case, then force a match',[],'Certain means every possible draw, not the most likely draw.'),
 (2008,24):('Prove a bound using the shortest boundary gap',['GEO-01'],'Both sides of every village need the required coastline.'),
 (2009,12):('Build the worst case, then force the target',[],'Count the most unhelpful draws before the guaranteed target.'),
 (2009,26):('Partition overlapping triangles',['FRAC-02'],'Use the stated lengths; appearance alone is not a measurement.'),
 (2010,21):('Write numbers in place-value form',['ALG-03','DIG-02'],'The reversed number must satisfy the stated digit conditions.'),
 (2010,27):('Bound crossings, then construct a triangle',['SPATIAL-02'],'A crossing through a grid vertex needs separate care.'),
 (2010,29):('Write numbers in place-value form',['ALG-01'],'Appending a digit and adding that digit have different effects.'),
 (2010,30):('Classify colourings up to cube rotations',['GEO-04','SOLID-03'],'Do not count a rotation as a new solid.'),
 (2011,17):('Use a greatest common divisor',['SPATIAL-02'],'Count interior dividing lines, not the number of squares.'),
 (2012,17):('List side triples and test triangle inequalities',['GEO-03'],'Equilateral triangles are included; the two shorter sides must exceed the third.'),
 (2012,29):('Classify joins up to the permitted symmetries',['GEO-04','SPATIAL-03'],'Check exactly which rotations or reflections count as the same.'),
 (2013,25):('Choose a largest subsequence greedily',['DIG-02'],'Remaining digits must keep their original order.'),
 (2013,26):('Bound the number of bags and compare weighted costs',['FRAC-04','COUNT-06'],'Average dollars per kilogram uses total price divided by total mass.'),
 (2013,27):('Split choices by remainders',['DIV-03','COUNT-02'],'Choose three different numbers; selection order does not matter.'),
 (2015,26):('Use the largest attainable square tiling',['SPATIAL-03','DIV-01'],'The design must fit the exact basketweave pattern.'),
 (2015,27):('Balance a product under distinctness constraints',['COUNT-01'],'An upper bound must also be attained by three different positive integers.'),
 (2017,28):('Optimise the leading difference, then later digits',['DIG-02'],'Use every digit once and disallow leading zeros.'),
 (2018,25):('Track borrowing in repeated digits',['DIG-03'],'Count the resulting digits, including the endpoints of the borrow chain.'),
 (2018,27):('Pair opposite faces under digit constraints',['DIG-02','GEO-05'],'All face numbers must be different and every opposite sum must match.'),
 (2019,8):('Compare distances with the halfway point',['DIG-01'],'Use distance from the starting town, not the largest sign number.'),
 (2020,25):('Compare conserved liquid and empty volume',['FRAC-02'],'The neck is not the same width as the cylindrical portion.'),
 (2021,23):('Track gear direction and tooth ratios',['FRAC-02'],'Adjacent gears turn in opposite directions and unequal gears turn different amounts.'),
 (2022,27):('Count face grids and shared edges',['SOLID-03','COUNT-05'],'Shared edge dots are counted once; the bottom is not decorated.'),
 (2023,28):('Minimise weighted digit positions',['DIG-02'],'Three leading digits cannot be zero; one digit is unused.'),
 (2024,27):('Optimise place-value contributions',['DIG-02'],'Find both extreme sums before taking their difference.'),
 (2024,26):('Compare operation orders and verify an optimum',['ALG-04','COUNT-06'],'Operations do not commute; a good order alone is not proof it is best.'),
 (2025,1):('Trace and count vertices',[],'Count corners once, including the less familiar angles.'),
 (2025,10):('Cancel opposite moves on a hexagonal grid',['GEO-04'],'Use the key directions, not rectangular-grid directions.'),
 (2025,12):('Count face-edge incidences twice',['SOLID-03'],'Each solid edge borders two faces.'),
 (2025,17):('Count contributions and optimise their weights',['COUNT-05','ALG-03'],'A middle entry contributes more than an endpoint entry.'),
 (2025,25):('Bound a common total by shared contributions',['GEO-05','LOGIC-02'],'Prove the bound and exhibit a placement reaching it.'),
 (2025,27):('Count one orientation, then use rotational symmetry',['SEQ-01','GEO-04'],'The tile covers two edge-adjacent triangles; rotations are allowed.'),
 (2025,28):('Count compatible row states',['SEQ-04','LOGIC-02'],'Every overlapping 2-by-2 block must satisfy the rule.'),
 (2025,29):('Pair successive square borders',['SPATIAL-02','COUNT-04'],'Corners belong to one border and the central square needs separate treatment.'),
 (2025,30):('Use symmetry to locate the crossing and subtract areas',['GEO-04','FRAC-02'],'The diagram is not a scale measurement; derive the crossing height.')
}
SUPPORT={
 'DIG-02':['COUNT-01'],'DIG-03':['SEQ-01'],'DIG-04':['DIG-02'],'DIG-05':['DIG-01'],
 'DIV-02':['DIV-01'],'DIV-03':['DIG-01'],'DIV-05':['DIV-03'],
 'FRAC-02':['FRAC-01'],'FRAC-03':['FRAC-01'],'FRAC-04':['FRAC-01'],
 'RATE-02':['FRAC-01','RATE-01'],'RATE-03':['RATE-01'],'RATE-04':['RATE-03'],
 'ALG-02':['ALG-01'],'ALG-03':['ALG-01'],'ALG-04':['DIG-01'],'ALG-05':['ALG-02'],
 'SEQ-01':['DIG-01'],'SEQ-02':['DIG-01'],'SEQ-03':['COUNT-06'],'SEQ-04':['COUNT-01'],
 'COUNT-02':['COUNT-01'],'COUNT-03':['COUNT-02'],'COUNT-04':['COUNT-01'],'COUNT-05':['ALG-01'],'COUNT-06':['COUNT-01'],
 'LOGIC-03':['ALG-03'],'LOGIC-04':['LOGIC-02'],
 'GEO-01':['RATE-01'],'GEO-02':['FRAC-01'],'GEO-05':['COUNT-01'],
 'SOLID-01':['SPATIAL-02'],'SOLID-02':['SOLID-03','COUNT-06'],'SOLID-03':['GEO-02'],
 'SPATIAL-01':['SEQ-03'],'SPATIAL-03':['GEO-04'],'SPATIAL-04':['COUNT-01'],
 'DATA-01':['FRAC-01','COUNT-01'],'DATA-02':['ALG-01'],'DATA-03':['DIG-01']
}
def source_text(r):
 return r.get('metadata',{}).get('source_text') or (r.get('problem_text','') if 'Read the original' in r.get('stem','') else r.get('stem',''))

def teaching_map(r,authentic=True):
 y=int(r['exam_id'][-4:]) if authentic else None;n=r['question_number']
 old=r.get('metadata',{}).get('skill_id') or r['category']
 skill=CORRECTIONS.get(y,{}).get(n,old);p=PROFILES[skill]
 t=source_text(r).lower();representation=[]
 for pattern,label in [
  (r'graph|chart|thermometer|dial|meter|scale|tachometer','graph or scale'),
  (r'grid|row|column|square[s]? in|squares in|dots','grid or array'),
  (r'cube|prism|net\b|pyramid|cuboid|solid|faces','solid or net'),
  (r'fold|mirror|reflect|rotat|turn|flip','transformation'),
  (r'number line|clock|calendar|time.?table','number line or time display'),
  (r'triangle|rectangle|hexagon|perimeter|shaded|area|square of','plane geometry'),
  (r'digit|cryptarithm|number sentence|algorithm|addition|multiplication','symbolic calculation'),
  (r'road|route|joined|connect|network|keypad','network'),
  (r'table\b|ratio|equal|each|cost|price|money|age|years|litre|litr|gram|km|speed','word relationships')]:
  if re.search(pattern,t):representation.append(label)
 if not representation:representation=['verbal or numerical']
 strategy=p['strategy'];support=SUPPORT.get(skill,[])[:];traps=[p['avoid']]
 if skill=='DIG-01':strategy='Use place value and efficient calculation'
 if skill=='FRAC-01':strategy='Identify the whole and use fractional parts'
 if skill=='SOLID-01':strategy='Model dimensions, layers and volume'
 if (y,n) in SPECIAL:strategy,support,trap=SPECIAL[y,n];traps=[trap]
 for pattern,trap in [
  (r'\bnot\b|cannot|could not','Answer the negative question, rather than choosing a possible case.'),
  (r'\bexactly\b','Exactly excludes both fewer and more.'),
  (r'\bat least\b|\bat most\b','Check whether the boundary value is included.'),
  (r'different|distinct','Check what makes two outcomes different.'),
  (r'remain|left over','Track the remaining quantity and the whole it refers to.'),
  (r'largest|smallest|maximum|minimum|most possible|least number','Explain why the proposed extreme cannot be improved.')]:
  if re.search(pattern,t) and trap not in traps:traps.append(trap)
 band='Q1–10' if n<=10 else 'Q11–20' if n<=20 else 'Q21–25' if n<=25 else 'Q26–30'
 return {'version':VERSION,'topic':p['topic'],'strategy':strategy,'primary_skill':skill,
  'supporting_skills':[s for s in support if s!=skill], 'representation':representation,
  'common_traps':traps,'check':p['check'],'difficulty_band':band,
  'classification_basis':'Editorial review of the original question, source diagrams and existing worked solution' if authentic else 'Editorial classification of an original practice question',
  'official_classification':False}

def main(source,out):
 rows=json.loads(Path(source).read_text());assert len(rows)==570
 assert {(r['exam_id'],r['question_number']) for r in rows}=={(f'amc-up-{y}',n) for y in range(2007,2026) for n in range(1,31)}
 mapped=[];topics=Counter();bands=defaultdict(Counter);skills=Counter();byyear=defaultdict(Counter)
 for r in rows:
  m=teaching_map(r);mapped.append({'exam_id':r['exam_id'],'question_number':r['question_number'],'skill_id':m['primary_skill'],'learning_map':m})
  topics[m['topic']]+=1;bands[m['topic']][m['difficulty_band']]+=1;skills[m['primary_skill']]+=1;byyear[int(r['exam_id'][-4:])][m['topic']]+=1
  assert m['strategy'] and m['representation'] and m['common_traps'] and all(s in PROFILES for s in m['supporting_skills'])
 Path(out).write_text(json.dumps(mapped,ensure_ascii=False,indent=2))
 public={'version':VERSION,'years':list(range(2007,2026)),'papers':19,'questions':570,
  'basis':'Editorial classifications of all 570 authentic Upper Primary questions, including diagram-dependent questions. One primary topic per question; methods and supporting skills are recorded separately. These are not official AMT classifications, predictions or empirical difficulty ratings.',
  'topics':[{'topic':k,'questions':v,'bands':dict(bands[k]),'minimum_per_paper':min(z.get(k,0) for z in byyear.values()),'maximum_per_paper':max(z.get(k,0) for z in byyear.values())} for k,v in sorted(topics.items())],
  'skills':[{'id':k,'questions':skills[k],**v} for k,v in PROFILES.items()],
  'holdout_policy':'Authentic questions are confined to the test centre. Lessons and quick checks use original problems. Keep several unopened papers for later independent checks; topic labels and written solutions appear only in the submitted report.',
  'limitations':'A topic can use several methods; editorial labels are not uniquely determined. Historical frequency does not predict 2027. Difficulty calibration is editorial until independent student attempt data are available.'}
 (ROOT/'data/amc-coverage.json').write_text(json.dumps(public,ensure_ascii=False,indent=2))
 print('Mapped',len(mapped),'questions;',sum(CORRECTIONS.get(int(r['exam_id'][-4:]),{}).get(r['question_number'],r['metadata'].get('skill_id') or r['category'])!=(r['metadata'].get('skill_id') or r['category']) for r in rows),'primary-skill corrections')

if __name__=='__main__':main(*sys.argv[1:])
