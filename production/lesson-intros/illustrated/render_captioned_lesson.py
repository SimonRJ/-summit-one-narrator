from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path
from urllib.request import urlretrieve
from captioned_film import render
MODULES={'S023':'badge_arrangements','S043':'boundary_walk','S061':'paper_cut_area','S090':'folding_box'}
if __name__=='__main__':
    parser=ArgumentParser();parser.add_argument('id',choices=MODULES);parser.add_argument('--source',type=Path);parser.add_argument('--out',required=True,type=Path);args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    src=args.source or args.out/(args.id+'-original.mp4')
    if not src.exists():
        urlretrieve('https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'+args.id+'-Intro.mp4',src)
    print(render(import_module(MODULES[args.id]),src,args.out))
