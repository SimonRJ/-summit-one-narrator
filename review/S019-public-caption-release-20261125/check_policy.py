"""Exercise the S019 gate with real returned payloads and isolated negative cases."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('release_gate',ROOT/'tools/prepare_spoken_film_release.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
NAMES=['S019'+suffix for suffix in ['.mp4','.vtt','-guide.json','-qa.json','-poster.jpg','-recording.zip']]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main(args):
 run=json.loads(args.run_report.read_text());release=json.loads(args.release_report.read_text())
 protected=['data/read-watch-practise.json','data/read-watch-practise-later.json','data/recorded-studies.json','tools/content/practice-revisions-20261121.json']
 before={name:digest(ROOT/name) for name in protected}
 plan=gate.prepare('S019',run,release,args.package)
 assert plan['production_run']==45524933207
 assert plan['production_commit']=='ac244dec713654fa7fb47693c8c179d9fb436479'
 assert plan['released_asset_sha256']['S019.mp4']=='5455c0c0119bedd897ddda6feb41002cf215575c8f8839565661674c42ad712c'
 assert [r['slot'] for r in plan['route_changes']]==[19,333]
 bridges=[]
 for change in plan['route_changes']:
  original=next(r for r in json.loads((ROOT/change['file']).read_text())['lessons'] if r['slot']==change['slot'])
  assert change['set']['bridge']==original['bridge']
  bridges.append({'slot':change['slot'],'bridge':original['bridge'],'preserved':True})
 revision=json.loads((ROOT/'tools/content/practice-revisions-20261121.json').read_text())['openings']['S019']['bridge']
 assert plan['canonical_opening_bridge']['bridge']==revision
 rejected=[]
 def rejection(label,mutate,expected,package_source=None):
  r=deepcopy(run);rel=deepcopy(release)
  with tempfile.TemporaryDirectory(prefix='s019-release-gate-') as directory:
   package=Path(directory)
   for name in NAMES:shutil.copyfile((package_source or args.package)/name,package/name)
   if package_source:
    for asset in rel['assets']:
     if asset['name'] in NAMES:
      file=package/asset['name'];asset['size']=file.stat().st_size;asset['digest']='sha256:'+digest(file)
   mutate(r,rel,package)
   try:gate.prepare('S019',r,rel,package)
   except ValueError as error:
    assert expected in str(error),(label,str(error))
    rejected.append({'case':label,'rejected':True,'reason':str(error)})
   else:raise AssertionError('Rejected case was admitted: '+label)
 def revise_json(filename,key,value):
  def mutate(run,release,package):
   path=package/filename;data=json.loads(path.read_text());data[key]=value;path.write_text(json.dumps(data)+'\n')
   asset=next(a for a in release['assets'] if a['name']==filename)
   asset['size']=path.stat().st_size;asset['digest']='sha256:'+digest(path)
  return mutate
 def alter_asset(filename):
  def mutate(run,release,package):
   path=package/filename;path.write_bytes(path.read_bytes()+b'\n')
   asset=next(a for a in release['assets'] if a['name']==filename)
   asset['size']=path.stat().st_size;asset['digest']='sha256:'+digest(path)
  return mutate
 rejection('queued workflow',lambda r,l,p:r.update(status='queued',conclusion=None),'have not all succeeded')
 rejection('wrong workflow run',lambda r,l,p:r.update(id=1),'Wrong production workflow run')
 rejection('wrong production source',lambda r,l,p:r.update(head_sha='0'*40),'Wrong production source commit')
 rejection('wrong release source',lambda r,l,p:l.update(target_commitish='0'*40),'Release source commit differs')
 rejection('wrong public movie digest',lambda r,l,p:next(a for a in l['assets'] if a['name']=='S019.mp4').update(digest='sha256:'+'0'*64),'Public GitHub digest does not match')
 rejection('held public 51545 master',lambda r,l,p:None,'Held or unpublished S019 candidate rejected',args.held_package)
 rejection('unpublished local 4a549 candidate',lambda r,l,p:None,'Held or unpublished S019 candidate rejected',args.local_candidate)
 rejection('wrong caption-repair source',revise_json('S019-qa.json','prior_candidate_sha256','0'*64),'does not identify its pinned source')
 rejection('changed recording archive',alter_asset('S019-recording.zip'),'original recording archive or VTT changed')
 rejection('changed VTT',alter_asset('S019.vtt'),'original recording archive or VTT changed')
 rejection('lost original AAC preservation',revise_json('S019-qa.json','audio_packet_bytes_and_timestamps_identical',False),'preservation is unverified')
 rejection('lost timeline preservation',revise_json('S019-qa.json','timeline_and_vtt_identical',False),'preservation is unverified')
 rejection('new synthesis',revise_json('S019-qa.json','new_synthesis',True),'saved-take or exact stream-length evidence differs')
 rejection('wrong caption-repair scene',revise_json('S019-qa.json','caption_repair_scene',6),'scoped scene-five caption repair')
 rejection('incomplete full-picture comparisons',revise_json('S019-qa.json','caption_repair_reference_comparisons',142),'lacks complete encoded-picture comparisons')
 rejection('incomplete retained-scene comparisons',revise_json('S019-qa.json','original_other_scene_comparisons',128),'lacks complete encoded-picture comparisons')
 rejection('picture difference outside acceptance bound',revise_json('S019-qa.json','caption_repair_largest_mean_picture_difference',[5,0]),'exceed the checked bounds')
 rejection('changed canonical lesson bridge',revise_json('S019-guide.json','bridge','Unreviewed replacement bridge.'),'would change the existing lesson bridge')
 assert before=={name:digest(ROOT/name) for name in protected}
 result={'positive_case':'Unmodified actual GitHub run/release API JSON and all six actual returned public assets','production_run':run['id'],'production_commit':run['head_sha'],'public_movie_sha256':plan['released_asset_sha256']['S019.mp4'],'positive_plan_passed':True,'rejected_cases':rejected,'negative_cases_are_isolated_synthetic_mutations':True,'lesson_bridges':bridges,'canonical_generator_bridge_preserved':True,'source_data_unchanged':True,'editorial_completion_awarded':False}
 args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'positive_passed':True,'negative_cases_rejected':len(rejected),'slots':[r['slot'] for r in bridges],'source_data_unchanged':True}))

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 for flag in ['package','held-package','local-candidate','run-report','release-report','output']:parser.add_argument('--'+flag,type=Path,required=True)
 main(parser.parse_args())
