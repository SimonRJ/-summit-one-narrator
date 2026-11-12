from importlib import import_module
from core import write_papers
from refinements import refine
from coverage_refinements import apply_coverage
import sys
modules=['amc_01_02','amc_03_04','amc_05_06','amc_07_08','amc_09_10','rossmoyne_01_03','rossmoyne_04_06','rossmoyne_07_09']
papers=[apply_coverage(refine(p)) for m in modules for p in import_module(m).papers()]
write_papers(papers,sys.argv[1]);print(len(papers),'papers;',sum(len(p['questions']) for p in papers),'questions')
