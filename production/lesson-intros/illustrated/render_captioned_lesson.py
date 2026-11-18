from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path
from urllib.request import urlretrieve
from captioned_film import render
MODULES={'S023':'badge_arrangements','S025':'percentage_bases','S026':'mean_balance','S027':'starred_collections','S029':'percent_register','S030':'trail_and_signals','S031':'pumps_and_packing','S033':'logic_witnesses','S034':'cycling_odometer','S037':'runner_meetings','S038':'ticket_counter','S039':'journey_graph','S040':'paired_boxes','S043':'boundary_walk','S044':'rewind_counters','S047':'theatre_rows','S053':'fence_survey','S054':'repeating_machine','S061':'paper_cut_area','S081':'angle_instrument','S089':'painted_layers','S090':'folding_box','S131':'angle_pieces'}
if __name__=='__main__':
    parser=ArgumentParser();parser.add_argument('id',choices=MODULES);parser.add_argument('--source',type=Path);parser.add_argument('--out',required=True,type=Path);args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    src=args.source or args.out/(args.id+'-original.mp4')
    if not src.exists():
        urlretrieve('https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'+args.id+'-Intro.mp4',src)
    print(render(import_module(MODULES[args.id]),src,args.out))
