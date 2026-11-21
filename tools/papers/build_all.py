from importlib import import_module
from core import write_papers
from refinements import refine
from coverage_refinements import apply_coverage
import argparse
import json
from pathlib import Path


def apply_rossmoyne_review(papers, edition):
 # Keep the four current assessed questions in the private assessment edition.
 required = {(f'summit-rossmoyne-practice-v2-{i:02}', n) for i,n in [(5,11),(8,21),(9,11),(9,21)]}
 rows = json.loads(edition.read_text())
 by_key = {(row['exam_id'], row['question_number']): row for row in rows}
 if len(rows) != len(required) or set(by_key) != required:
  raise ValueError('The private four-question Rossmoyne review edition is incomplete')
 for paper in papers:
  for question in paper['questions']:
   row = by_key.get((question['exam_id'],question['question_number']))
   if row is None:
    continue
   for field in ('stem','explanation'):
    if not isinstance(row[field],str) or not row[field].strip():
     raise ValueError(f'Missing {field} in the private Rossmoyne review')
    question[field] = row[field]


parser = argparse.ArgumentParser(description='Build the archived authored paper fixtures or supply the private Rossmoyne edition for a current rebuild.')
parser.add_argument('output',type=Path)
parser.add_argument('--rossmoyne-review',type=Path,help='JSON export of the four revised authored questions from the private bank')
args=parser.parse_args()
modules=['amc_01_02','amc_03_04','amc_05_06','amc_07_08','amc_09_10','rossmoyne_01_03','rossmoyne_04_06','rossmoyne_07_09']
papers=[apply_coverage(refine(p)) for m in modules for p in import_module(m).papers()]
if args.rossmoyne_review:
 apply_rossmoyne_review(papers,args.rossmoyne_review)
else:
 print('Archived Rossmoyne fixtures. Supply --rossmoyne-review for the current assessment edition.')
write_papers(papers,args.output);print(len(papers),'papers;',sum(len(p['questions']) for p in papers),'questions')
